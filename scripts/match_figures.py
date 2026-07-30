#!/usr/bin/env python3
"""
match_figures.py — propose which cards should carry a figure, and which figure.

Not every card is better with a picture. A dose, a legal definition, or an etymology gains
nothing from art, while "where is the occipital bone" is barely a card without it. This
proposes attachments and shows its reasoning; it never writes to Anki.

A figure is proposed only when THREE independent signals agree:

  1. PROXIMITY  the figure sits on (or beside) the page the card's mark came from, so it
                is the plate the book itself put next to that sentence.
  2. COVERAGE   the card's CLOZE ANSWERS appear in the figure's caption/long description.
                This is the load-bearing test: it asks "does this picture actually show
                the thing he has to produce from memory?" rather than "is it nearby?"
  3. ARCHETYPE  the fact is spatial/structural (where a thing is, what it looks like, how
                parts connect) rather than numeric, procedural, or definitional.

Anything that clears 1+2 but not 3, or is close on coverage, is reported as a MAYBE for a
human call rather than silently attached or silently dropped.

Usage
    python3 match_figures.py --source emt --segment 6
    python3 match_figures.py --source emt --segment 6 --json proposals.json
"""
import argparse, json, os, re, sys
import sources as S

STOPWORDS = {
    "the", "and", "with", "from", "that", "this", "are", "for", "its", "into", "which",
    "illustration", "shows", "labeled", "view", "left", "right", "top", "bottom", "figure",
    "image", "side", "part", "parts", "above", "below", "between", "front", "back", "each",
    "also", "have", "has", "can", "may", "one", "two", "three", "other", "than", "when",
    "these", "there", "their", "them", "not", "all", "any", "such", "both", "where",
}

# Words that mark a fact as SPATIAL/STRUCTURAL — the kind a picture actually teaches.
SPATIAL = re.compile(
    r"\b(anterior|posterior|superior|inferior|medial|lateral|proximal|distal|dorsal|"
    r"ventral|cranial|caudal|surface|located|location|lies|sits|above|below|behind|"
    r"beneath|underneath|adjacent|border|margin|attach|attaches|articulat|connects|"
    r"junction|joint|between|forms|consists|comprises|composed|divided|region|"
    r"quadrant|plane|axis|shape|shaped|structure|extends|runs|passes|branch)\b", re.I)
# Words that mark a fact as NOT picture-shaped.
ABSTRACT = re.compile(
    r"\b(consent|liability|negligence|law|legal|ethic|protocol|policy|document|"
    r"report|refus|scope of practice|confidential|mandat|abandon|per minute|mm hg|"
    r"mg|mcg|percent|ratio|rate of|derived from|means|term|prefix|suffix|root word)\b", re.I)


def words(*texts):
    ws = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", " ".join(t or "" for t in texts).lower())
    return {w for w in ws if w not in STOPWORDS}


def cloze_answers(text):
    """The strings the card makes him produce — the only thing a figure must actually show."""
    return [re.sub(r"::.*$", "", a).strip()
            for a in re.findall(r"\{\{c\d+::(.+?)\}\}", text or "", re.S)]


def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s or "")


def card_pages(card, marks):
    """The physical pages this card's marks came from."""
    out = set()
    for i in card.get("from_idx") or []:
        if 0 <= i < len(marks):
            p = re.sub(r"[^0-9]", "", str(marks[i].get("page", "")))
            if p:
                out.add(int(p))
    vs = card.get("visual_source") or {}
    for p in vs.get("pages") or []:
        p = re.sub(r"[^0-9]", "", str(p))
        if p:
            out.add(int(p))
    return out


def archetype(card):
    """Is this fact the kind a picture teaches? Returns (verdict, why)."""
    body = strip_html(card.get("Text", "")) + " " + strip_html(card.get("Back Extra", ""))
    if card.get("numeric"):
        return False, "numeric fact — a picture does not teach a value"
    if ABSTRACT.search(body) and not SPATIAL.search(body):
        return False, "abstract/procedural fact"
    if SPATIAL.search(body):
        return True, "spatial/structural fact"
    return None, "neither clearly spatial nor clearly abstract"


def score(card, fig, pages):
    ans = cloze_answers(card.get("Text", ""))
    if not ans:
        return None
    awords = words(*ans)
    if not awords:
        return None
    fwords = set(fig.get("terms") or [])
    coverage = len(awords & fwords) / len(awords)
    hit = sorted(awords & fwords)
    fp = {fig.get("art_page"), fig.get("caption_page")}
    dist = min((abs(p - q) for p in pages for q in fp if q), default=99)
    return {"coverage": round(coverage, 3), "page_dist": dist, "matched": hit}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--segment", type=int)
    ap.add_argument("--cards", help="cards JSON (default: work/<src>/<seg>_cards.json)")
    ap.add_argument("--json", help="write proposals here")
    ap.add_argument("--min-coverage", type=float, default=0.34)
    ap.add_argument("--max-page-dist", type=int, default=2)
    args = ap.parse_args()

    src = S.get_source(args.source)
    work = os.path.join(S.SKILL, "work", src["id"])
    seg = args.segment
    cards_p = args.cards or os.path.join(work, f"chapter_{seg}_cards.json")
    marks_p = os.path.join(work, f"chapter_{seg}_highlights.json")
    index_p = os.path.join(work, "figure_index.json")
    for p in (cards_p, index_p):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing {p}")
    cards = json.load(open(cards_p))
    marks = json.load(open(marks_p)) if os.path.exists(marks_p) else []
    figs = json.load(open(index_p))["figures"]

    yes, maybe, no = [], [], []
    for ci, c in enumerate(cards):
        pages = card_pages(c, marks)
        if not pages:
            continue
        best, bs = None, None
        for f in figs:
            s = score(c, f, pages)
            if not s or s["page_dist"] > args.max_page_dist:
                continue
            if bs is None or (s["coverage"], -s["page_dist"]) > (bs["coverage"], -bs["page_dist"]):
                best, bs = f, s
        if not best or bs["coverage"] <= 0:
            continue
        arch, why = archetype(c)
        rec = {"card_index": ci, "text": strip_html(c["Text"])[:110],
               "figure": best["label"], "file": best["file"],
               "coverage": bs["coverage"], "page_dist": bs["page_dist"],
               "matched_terms": bs["matched"], "archetype": arch, "why": why,
               "has_description": bool(best.get("description"))}
        if bs["coverage"] >= args.min_coverage and arch is True:
            yes.append(rec)
        elif bs["coverage"] >= args.min_coverage or arch is True:
            maybe.append(rec)
        else:
            no.append(rec)

    yes.sort(key=lambda r: -r["coverage"])
    maybe.sort(key=lambda r: -r["coverage"])
    print(f"{len(cards)} cards | {len(figs)} figures indexed\n")
    print(f"  ATTACH  {len(yes):>3}   coverage>={args.min_coverage} AND spatial fact")
    print(f"  MAYBE   {len(maybe):>3}   one signal only — needs a human call")
    print(f"  SKIP    {len(no):>3}   matched a figure but earns no picture")
    print(f"  (cards with no nearby figure at all: {len(cards)-len(yes)-len(maybe)-len(no)})\n")
    print("=" * 78)
    print("ATTACH — strongest first")
    for r in yes[:18]:
        print(f"\n  [{r['coverage']:.2f}] {r['figure']}  (±{r['page_dist']}p)"
              f"{'' if r['has_description'] else '  [no long-desc]'}")
        print(f"    {r['text']}")
        print(f"    shows: {', '.join(r['matched_terms'][:9])}")
    if maybe:
        print("\n" + "=" * 78)
        print("MAYBE — first 8")
        for r in maybe[:8]:
            print(f"\n  [{r['coverage']:.2f}] {r['figure']}  — {r['why']}")
            print(f"    {r['text']}")
            print(f"    shows: {', '.join(r['matched_terms'][:9])}")
    if args.json:
        json.dump({"attach": yes, "maybe": maybe, "skip": no}, open(args.json, "w"), indent=1)
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
