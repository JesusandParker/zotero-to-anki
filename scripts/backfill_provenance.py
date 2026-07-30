#!/usr/bin/env python3
"""
backfill_provenance.py — recover `from_idx` for a segment whose cards predate provenance.

Chapters 1-5 were generated before `from_idx` existed, so their cards do not record which
marks they came from. That is what the figure matcher needs (a card with no mark has no
page, and a card with no page cannot be near a figure), and it is what R13 grounding
needs. This reconstructs it.

Two passes, because text similarity alone is not enough:

  1. ANCHOR — score each card against each mark by how much of the MARKED SPAN the card
     reproduces. A card that clears both an absolute bar and a margin over the runner-up
     is trusted outright. These are unambiguous and verify by eye.

  2. INTERPOLATE — the generator walks the chapter in order, so card order tracks mark
     order almost perfectly. A card sitting between two anchored cards must have come
     from a mark between THEIR marks. Re-scoring only inside that window rescues the
     cards that pass 1 fails: scenario/application cards, which paraphrase a concept
     instead of reproducing its words and so score low against every mark globally, but
     win easily inside their true neighbourhood.

Anything still unresolved is left `null` and REPORTED, never guessed. A wrong from_idx is
worse than a missing one: it silently attaches the wrong page's figure and mis-grounds
R13.

    python3 backfill_provenance.py --source emt --segment 4 --dry-run
    python3 backfill_provenance.py --source emt --segment 4
"""
import argparse, bisect, json, os, re, subprocess, sys
import sources as S

WORD = re.compile(r"[A-Za-z][A-Za-z\-]{2,}")
STOP = set("the and with from that this are for its into which also have has can may one two "
           "three other than when these there their them not all any such both where who how "
           "you your they what will would should each more most some only very been being "
           "use used using make makes made give gives given take takes may might must".split())
ANCHOR_SCORE = 0.45      # share of the marked span the card reproduces
ANCHOR_MARGIN = 0.08     # lead over the runner-up; a near-tie is not an anchor
WINDOW_SCORE = 0.20      # inside its true neighbourhood a much weaker match is credible


def words(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"\{\{c\d+::(.+?)(?:::.*?)?\}\}", r"\1", s, flags=re.S)
    return {w.lower() for w in WORD.findall(s) if w.lower() not in STOP}


def score_all(cw, marks):
    """(total, span_share, index) per mark, best first."""
    out = []
    for i, (hw, cx) in enumerate(marks):
        if not hw:
            continue
        span = len(cw & hw) / len(hw)
        ctx = len(cw & cx) / max(1, len(cx))
        out.append((span + 0.25 * ctx, span, i))
    out.sort(reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int, required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-pages", action="store_true",
                    help="skip the direct page-location pass (pass 3)")
    args = ap.parse_args()

    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    cards_p = os.path.join(work, f"chapter_{args.segment}_cards.json")
    hl_p = os.path.join(work, f"chapter_{args.segment}_highlights.json")
    for p in (cards_p, hl_p):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing {p}")
    cards = json.load(open(cards_p))
    hls = json.load(open(hl_p))
    marks = [(words(h.get("highlight", "")), words(h.get("context", ""))) for h in hls]

    # ---- pass 1: anchors
    best = []
    for c in cards:
        cw = words(c.get("Text", "")) | words(c.get("Back Extra", ""))
        s = score_all(cw, marks) if cw else []
        best.append(s)
    anchor = [None] * len(cards)
    for i, s in enumerate(best):
        if not s:
            continue
        top = s[0]
        runner = s[1][0] if len(s) > 1 else 0.0
        if top[1] >= ANCHOR_SCORE and (top[0] - runner) >= ANCHOR_MARGIN:
            anchor[i] = top[2]
    n_anchor = sum(a is not None for a in anchor)

    # The spine must be non-decreasing. Take the LONGEST non-decreasing subsequence rather
    # than sweeping greedily: greedily keeping the first of every conflicting pair lets one
    # early false anchor evict every later correct one (on EMT ch4 that cost 67 anchors ->
    # 27). Solving for the longest consistent run instead keeps 59 and discards precisely
    # the handful that break the pattern -- which, inspected, are the wrong matches.
    idxs = [i for i, a in enumerate(anchor) if a is not None]
    seq = [anchor[i] for i in idxs]
    tails, prev, tail_idx = [], [None] * len(seq), []
    for k, x in enumerate(seq):
        j = bisect.bisect_right(tails, x)
        if j == len(tails):
            tails.append(x); tail_idx.append(k)
        else:
            tails[j] = x; tail_idx[j] = k
        prev[k] = tail_idx[j - 1] if j > 0 else None
    keep_pos = set()
    k = tail_idx[-1] if tail_idx else None
    while k is not None:
        keep_pos.add(k); k = prev[k]
    kept = [idxs[k] for k in sorted(keep_pos)]
    dropped = [i for i in idxs if i not in set(kept)]
    for i in dropped:
        anchor[i] = None
    n_spine = len(kept)

    # ---- pass 2: interpolate inside the window each anchor pair implies
    resolved = list(anchor)
    for i in range(len(cards)):
        if resolved[i] is not None or not best[i]:
            continue
        lo_i = max((k for k in kept if k < i), default=None)
        hi_i = min((k for k in kept if k > i), default=None)
        lo = anchor[lo_i] if lo_i is not None else 0
        hi = anchor[hi_i] if hi_i is not None else len(marks) - 1
        lo, hi = max(0, lo - 1), min(len(marks) - 1, hi + 1)   # a little slack
        inwin = [t for t in best[i] if lo <= t[2] <= hi]
        if inwin and inwin[0][1] >= WINDOW_SCORE:
            resolved[i] = inwin[0][2]
    n_total = sum(r is not None for r in resolved)

    # ---- pass 3: locate the PAGE directly, independent of card order
    #
    # Passes 1-2 lean on the generator having walked the chapter in order. That held for
    # Chapter 4 (67 anchors, 59 of them one consistent run) and collapses for Chapter 1,
    # whose cards were reordered by heavy consolidation: its anchors are all CORRECT yet
    # run 0->30, 1->3, 2->20, 4->8 — no monotone structure to interpolate along, so the
    # spine fell to 6 and only 12 of 32 cards resolved.
    #
    # But the matcher does not actually need the mark. It needs the PAGE. That can be read
    # straight off the source by asking which page's text this card's content best matches
    # — no ordering assumption, and it works the same on a legacy chapter and a fresh one.
    # So `source_page` is resolved for EVERY card, and `from_idx` stays whatever passes 1-2
    # could prove.
    pages = {}
    if not args.no_pages:
        first, last, _n = S.segment_range(src, args.segment)
        _id, pdf = S.resolve_attachment(src)
        page_words = {}
        for pno in range(first, last + 1):
            txt = subprocess.run(["pdftotext", "-layout", "-f", str(pno), "-l", str(pno),
                                  pdf, "-"], capture_output=True, text=True,
                                 timeout=60).stdout
            w = words(txt)
            if w:
                page_words[pno] = w
        for i, c in enumerate(cards):
            cw = words(c.get("Text", ""))
            if not cw:
                continue
            ranked = sorted(((len(cw & pw) / len(cw), pno)
                             for pno, pw in page_words.items()), reverse=True)
            if not ranked:
                continue
            best_s = ranked[0][0]
            # BREAK TIES TOWARD THE EARLIEST PAGE. A chapter restates itself at the end —
            # the glossary and the "Ready for Review" recap condense every definition — so
            # a definition card matches those as well as the prose that introduced it. On
            # EMT ch1 that produced exact ties (0.73 vs 0.73) where the runner-up was the
            # real body page and the winner was the p125 glossary. The body always precedes
            # the recap, so the earliest page among near-equals is the one that taught it —
            # and it is the one that has a figure beside it.
            near = [pno for s, pno in ranked if best_s - s <= 0.03]
            best_p = min(near)
            # A card's own wording is a rewrite of the page, so overlap is partial by
            # design; require a real majority before believing it.
            if best_s >= 0.55:
                pages[i] = (best_p, round(best_s, 2))

    unresolved = [i for i, r in enumerate(resolved) if r is None]
    print(f"{len(cards)} cards | {len(hls)} marks")
    print(f"  pass 1 anchors          : {n_anchor}  (monotonic spine: {n_spine})")
    print(f"  pass 2 window-resolved  : {n_total - n_spine}")
    print(f"  RESOLVED TOTAL          : {n_total}/{len(cards)}")
    print(f"  left null (reported)    : {len(unresolved)}")
    if unresolved:
        print("\n  unresolved cards — no confident mark, left null on purpose:")
        for i in unresolved[:12]:
            print(f"    #{i}: {re.sub(r'<[^>]+>', '', cards[i]['Text'])[:88]}")

    print(f"  pass 3 page-located     : {len(pages)}/{len(cards)}  "
          f"(direct text match, order-independent)")
    frommark = {}
    for i, r in enumerate(resolved):
        if r is not None:
            frommark[i] = hls[r].get("page")
    # Where BOTH methods spoke, do they agree? A disagreement means one of them is wrong,
    # and silently preferring either would hide it.
    agree = dis = 0
    for i, (pg, _sc) in pages.items():
        fm = frommark.get(i)
        if fm is None:
            continue
        if abs(int(re.sub(r"[^0-9]", "", str(fm)) or 0) - pg) <= 1:
            agree += 1
        else:
            dis += 1
    if agree or dis:
        print(f"  cross-check: {agree} agree, {dis} disagree (mark-page vs located-page)")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return
    for i, r in enumerate(resolved):
        cards[i]["from_idx"] = [r] if r is not None else None
        cards[i]["provenance_backfilled"] = True
        if i in pages:
            cards[i]["source_page"] = pages[i][0]
    json.dump(cards, open(cards_p, "w"), indent=1)
    stamp = cards_p + ".verified"
    if os.path.exists(stamp):
        os.remove(stamp)          # the file changed; the gate must be re-run
    print(f"\nwrote from_idx to {cards_p}")
    print("  .verified stamp cleared — re-run check_cards.py before any write")


if __name__ == "__main__":
    main()
