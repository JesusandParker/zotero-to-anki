#!/usr/bin/env python3
"""
check_cards.py — deterministic pre-flight GATE for generated cards (any source).

Runs the checks that CAN be mechanical, so they can never be skipped or
forgotten. Semantic checks (under-clozing, yield, subtle leaks) are the LLM
judge's job; this catches structure, format, literal leaks, missing flags, and
in-batch duplicates — including the exact shapes that have bitten us before
(see reference/regression-cases.md).

Three ways to run it:
  * GATE (default) — check a staged JSON file and, on a HARD-clean pass, write a
    `.verified` stamp so anki_write.py will let the file be staged. Strict HTML gate.
        python3 scripts/check_cards.py work/<source>/<file>_cards.json
  * AUDIT a file (--audit) — same, but for PRE-EXISTING/rich cards: skip the
    minimal-HTML HARD gate (embedded reference images/links, tables, the Ch5
    clinical-ex blocks) while keeping every meaningful check.
        python3 scripts/check_cards.py --audit work/emt/chapter_5_cards.json
  * LIVE AUDIT (--live) — pull cards straight from the Anki deck and check them, so
    cards HAND-EDITED in Anki (Mac + iPhone) still get audited. Relaxed HTML like
    --audit. Diagnostic only — it never stamps or writes.
        python3 scripts/check_cards.py --live 3   --source emt   # one segment
        python3 scripts/check_cards.py --live all --source emt   # the whole source
    (Added 2026-07-19 after a live audit found <a> anchor tags that had drifted
    into two cards via mobile paste-edits — the gate had never seen them because
    it only ever checked the pre-staging JSON.)

Exit 1 on any HARD error (blocks staging). WARNINGS print but don't block —
they are routed to the LLM judge / Parker.
"""
import argparse, hashlib, json, os, re, sys, unicodedata, urllib.request
from difflib import SequenceMatcher

import sources as S


def stamp_path(cards_json):
    return cards_json + ".verified"


def file_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

ANKI = "http://localhost:8765"
ALLOWED_TAGS = {"b", "i", "br", "img"}
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")
TAG = re.compile(r"</?([a-zA-Z0-9]+)[^>]*>")
# a real VALUE/dose/threshold (number + unit, comparison, or range) — NOT a bare
# list ordinal like "1. Detection" or a year inside a name.
VALUE = re.compile(r"[<>≤≥]\s*\d|\d+\s*(?:mg|mcg|g|mmHg|mL|%|/min|bpm|hours?|minutes?|seconds?|"
                   r"mph|miles?|feet|ft|inch|in|MHz|watts?|L/min|°|degrees?)\b|"
                   r"\d+\s*(?:to|-|–)\s*\d+", re.I)
# "N <list-noun>" where the card should then cloze exactly N items. A mismatch means
# the card states one count but tests another number of items — the exact shape of the
# Ch3 "consider 7 factors" bug (source had 8). Catch it mechanically.
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
LIST_NOUNS = (r"factors|signs|steps|elements|questions|items|types|ways|routes|hazards|"
              r"circumstances|stages|consequences|forms|principles|functions|components|"
              r"categories|reasons|examples|cases|situations|conditions|features|actions|"
              r"criteria|rights|duties|methods|phases|properties|kinds|zones|levels|classes")
COUNT_RE = re.compile(r"\b(\d+|" + "|".join(NUMWORDS) + r")\s+(?:\w+\s+){0,2}?(?:" + LIST_NOUNS + r")\b", re.I)
# a single blank hiding this many words is almost never recallable verbatim: it is
# either a fuzzy scenario→action clause (R8) or a bloated two-way-definition c2 side
# that should be tightened to a crisp discriminator (card-recipes §4, parker-preferences).
LONG_CLOZE_WORDS = 9
# double-escaped markup that renders as literal "&lt;br&gt;" text (a real bug); &amp;
# inside a URL and &nbsp; are legitimate and NOT flagged.
BAD_ENTITY = re.compile(r"&(?:lt|gt);")


def readable(t):
    t = CLOZE.sub(lambda m: m.group(2), t)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s).lower()).strip()


def visible_stem(text, group):
    """The card's front for cloze GROUP: that group blanked, the others shown."""
    out, pos = [], 0
    for m in CLOZE.finditer(text):
        out.append(text[pos:m.start()])
        if m.group(1) == group:
            out.append("___")  # blank WITHOUT the hint: an answer inside its own
            # forced-choice hint ("federal or state?") is legitimate, not a leak
        else:
            out.append(m.group(2))
        pos = m.end()
    out.append(text[pos:])
    return re.sub(r"<[^>]+>", " ", "".join(out))


# --- Cold-Solve Gate mechanical proxies (card-rules #16-18 / regression R9-R11) ---
# R9 (open-set) is semantic and left to the LLM judge + the cold-solve test — no
# reliable mechanical proxy. R10 (husk) and R11 (letter-hint leak) are catchable.

ACRONYM = re.compile(r"\b[A-Z][A-Za-z]*[A-Z][A-Za-z/\-]*\b")  # SAMPLE, DCAP-BTLS, ABCs
LIST_MARKERS = re.compile(r"<br\s*/?>|(?:^|\s)\d+\.\s|:\s*$", re.I)


def first_letter_hint_leaks(text):
    """R11: a hint that is just the leading letter(s) of its own answer is a giveaway
    UNLESS the card is teaching a spelled mnemonic. The mere PRESENCE of an acronym in
    the stem licenses nothing (EMT/EMS/CPR sit in half this book's stems): the group's
    hint letters, joined in document order, must actually spell INTO a token visible in
    the stem — 'sample' into SAMPLE, 'dcapbtls' into DCAP-BTLS. Otherwise ::D/::B/::C
    on a plain list is the copout Parker ranted about, whatever else the stem mentions."""
    stem_plain = re.sub(r"<[^>]+>", " ", CLOZE.sub(lambda m: " ", text))
    tokens = [re.sub(r"[^a-z]", "", t.lower()) for t in ACRONYM.findall(stem_plain)]
    tokens = [t for t in tokens if len(t) >= 3]
    letter_hints = {}  # cloze group -> [(answer, hint, normalized letters)] in order
    for m in CLOZE.finditer(text):
        ans, hint = m.group(2), (m.group(3) or "")
        h = re.sub(r"[^a-z]", "", norm(hint))
        a = re.sub(r"[^a-z]", "", norm(ans))
        # a genuine forced-choice hint contains "/" or " or " (len guards those out)
        if 1 <= len(h) <= 2 and a.startswith(h) and "/" not in hint and " or " not in hint.lower():
            letter_hints.setdefault(m.group(1), []).append((ans, hint, h))
    def _subseq(needle, hay):
        it = iter(hay)
        return all(ch in it for ch in needle)

    leaks = []
    for g, items in letter_hints.items():
        joined = "".join(h for _, _, h in items)
        # licensed only if these letters, in order, spell into a stem token: a
        # contiguous run of >=2 (SAMPLE's 'sam'), or an in-order subsequence of >=3
        # (CHART's C-H-A-T, whose Rx item breaks contiguity). A lone letter never
        # self-licenses off e.g. 'EMT' — and when the acronym itself is co-clozed
        # (hidden), a letter hint leaks its spelling, so hidden answers are not tokens.
        licensed = any((len(joined) >= 3 and _subseq(joined, t)) or
                       (len(joined) >= 2 and joined in t) for t in tokens)
        if not licensed:
            leaks.extend((ans, hint) for ans, hint, _ in items)
    return leaks


STOP = set("a an the of to and or but in on at by for with as is are was were be been "
           "that this these those it its their his her they you your we our not only "
           "generally usually often may can will would should must also both either".split())


def _content_words(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return [w for w in re.findall(r"[a-zA-Z]+", s.lower()) if w not in STOP]


def husk_groups(text):
    """R10: a single cloze number hiding EXACTLY 2 multi-word spans that sit in
    different clausal roles of an inline template — 'the ___ of X applies to ___' —
    so each blank's only cue is the other (the governmental-immunity husk).

    The discriminator vs a legitimate grouped PAIR (verbal/nonverbal; the two goals of
    therapeutic communication) is the CONNECTIVE between the two blanks: a coordinate
    pair is joined by 'and'/'or'/',' (~0 content words between them) and stays; a husk
    has a substantial templating phrase between the spans ('applies only to EMS systems
    operated by' = 5 content words). Also excludes <br>-listed or counted sets.

    Deliberately GENEROUS on multi-number contrast cards (cover/concealment, women one
    drink/men two drinks): it may flag a group whose sibling cloze number would anchor
    it. Suppressing those risks a FALSE NEGATIVE — a real husk that merely coexists with
    an unrelated cloze — which is the costly error on the exact class Parker rants about.
    So the checker over-flags and the LLM judge (editor #19) clears the benign ones."""
    if LIST_MARKERS.search(text):
        return []
    if COUNT_RE.search(readable(text)):
        return []
    # positions of each deletion, grouped by cloze number; s[4] = forced-choice hint?
    def is_forced(hint):
        return bool(hint) and ("/" in hint or " or " in hint.lower())
    spans = [(m.group(1), m.start(), m.end(), m.group(2), is_forced(m.group(3) or ""))
             for m in CLOZE.finditer(text)]
    hits = []
    for g in {s[0] for s in spans}:
        gs = [s for s in spans if s[0] == g]
        multiword = [s for s in gs if len(s[3].split()) >= 2]
        if len(gs) != 2 or len(multiword) < 2:
            continue  # a coordinate pair of short items, or a 3+ list — not a husk
        if all(s[4] for s in gs):
            continue  # both blanks carry a forced-choice hint — answerable by design
        between = text[gs[0][2]:gs[1][1]]
        if len(_content_words(between)) >= 2:  # real templating between the spans
            hits.append(g)
    return hits


EQ_CONNECTIVE = re.compile(r"=|also called|also known as|\baka\b|stands for", re.I)


def equation_husk_groups(text):
    """R10 variant the word-count husk misses: a single cloze number hiding BOTH sides
    of an identity/synonym equation — '___ = also called ___' — regardless of span
    length or count (the off-line/indirect + online/direct card, and the Expressed =
    actual consent card). Blank the group; if a synonym connective ends up flanked by
    two blanks, flag it.
    Deliberately GENEROUS: it cannot tell 'the two hidden spans are synonyms of each
    other' (a real husk) from 'they are different things each anchored by a visible
    label' (an acronym card, POLST/MOLST stands-for; a grouped two-way def, SOAP
    Subjective=/Objective=) without semantics. So it over-flags those two shapes, and the
    LLM judge / human clears them — the same review-not-block contract as the word-count
    husk. Missing a real synonym husk is the costly error; a spare 'verify' warning is not."""
    hits = []
    for g in {m.group(1) for m in CLOZE.finditer(text)}:
        blanked = re.sub(r"<[^>]+>", " ",
                         re.sub(CLOZE, lambda m: (" ¤ " if m.group(1) == g else m.group(2)), text))
        if re.search(r"¤[^¤]{0,40}?(?:" + EQ_CONNECTIVE.pattern + r")[^¤]{0,40}?¤",
                     blanked, re.I):
            hits.append(g)
    return hits


def per_card(idx, c, strict_html=True):
    """All per-card mechanical checks. Returns (hard_list, warn_list) of message
    strings. `strict_html=False` (set by --audit and --live) downgrades the
    disallowed-HTML check from HARD to a warning, because pre-existing / hand-edited
    cards (esp. Chapter 5's clinical-example blocks, or a reference image Parker pasted)
    legitimately carry richer HTML; the default strict gate keeps NEW generated cards on
    b/i/br/img."""
    t, be = c.get("Text", ""), c.get("Back Extra", "")
    hard, warn = [], []
    # disallowed HTML
    bad = [g for g in (TAG.findall(t) + TAG.findall(be)) if g.lower() not in ALLOWED_TAGS]
    if bad:
        msg = f"#{idx}: disallowed HTML tag(s): {sorted(set(bad))}"
        if strict_html:
            hard.append(msg)
        else:
            warn.append(msg + " (rich/pre-existing: verify it renders; the generator must stay on b/i/br/img)")
    # must contain a cloze
    if not CLOZE.search(t):
        hard.append(f"#{idx}: no cloze markup in Text")
    # empty/whitespace cloze answer
    for m in CLOZE.finditer(t):
        if not m.group(2).strip():
            hard.append(f"#{idx}: empty cloze c{m.group(1)}")
    # double-escaped markup rendering as literal text
    if BAD_ENTITY.search(t) or BAD_ENTITY.search(be):
        warn.append(f"#{idx}: contains &lt;/&gt; — markup may be double-escaped and rendering as literal text")
    # literal answer visible in the stem (a leak)
    for g in {m.group(1) for m in CLOZE.finditer(t)}:
        stem = norm(visible_stem(t, g))
        for m in CLOZE.finditer(t):
            if m.group(1) == g:
                a = norm(m.group(2))
                if a and len(a.split()) <= 4 and re.search(r"\b" + re.escape(a) + r"\b", stem):
                    warn.append(f"#{idx}: answer '{m.group(2)}' is visible in its own stem (leak)")
    # parenthetical hanging right off a cloze (the pathway-card leak shape)
    if re.search(r"\}\}\s*\(", t):
        warn.append(f"#{idx}: parenthetical right after a cloze — verify it is NOT the answer's definition (leak risk)")
    # first-letter hint on a non-mnemonic list (R11, the ::r/::k/::s leak)
    for ans, hint in first_letter_hint_leaks(t):
        warn.append(f"#{idx}: hint '::{hint}' is the first letter of its answer '{ans}' with no acronym in the stem — first-letter leak (card-rules #18)")
    # all-blanks-at-once husk — mutually-dependent spans under one number (R10)
    for g in husk_groups(t):
        warn.append(f"#{idx}: cloze c{g} hides 2 multi-word spans in an inline template — possible husk; verify each blank is answerable with the other shown, else split into c1/c2 (card-rules #17)")
    # synonym-equation husk — both sides of 'X = also called Y' under one number (R10)
    for g in equation_husk_groups(t):
        warn.append(f"#{idx}: cloze c{g} hides BOTH sides of a synonym/equation ('___ = also called ___') — husk; renumber so each card shows one side as the anchor (card-rules #17)")
    # a single blank hiding a whole clause — fuzzy (R8) or a bloated two-way-def c2 side
    by_group = {}
    for m in CLOZE.finditer(t):
        by_group.setdefault(m.group(1), []).append(m.group(2))
    for g, answers in by_group.items():
        if len(answers) == 1 and len(answers[0].split()) >= LONG_CLOZE_WORDS:
            warn.append(f"#{idx}: cloze c{g} hides {len(answers[0].split())} words in ONE blank — hard to recall verbatim; "
                        f"tighten to the load-bearing words (R8), or if this is a two-way definition, crisp up the c2 meaning side (card-recipes §4)")
    # looks numeric but not flagged
    if VALUE.search(readable(t)) and not c.get("needs_human_check"):
        warn.append(f"#{idx}: looks numeric/dose but needs_human_check is false")
    # stated list-count != number of clozed items (the "7 vs 8 factors" bug)
    m = COUNT_RE.search(readable(t))
    if m:
        stated = NUMWORDS.get(m.group(1).lower(), None)
        if stated is None:
            try:
                stated = int(m.group(1))
            except ValueError:
                stated = None
        if stated and 2 <= stated <= 20:
            # Count members of the dominant cloze group (the list group) and warn only
            # on an UNDERCOUNT — fewer clozed items than the stated number (a dropped
            # list item). An OVERCOUNT is almost always a branch/alternative and is safe.
            gc = {}
            for cm in CLOZE.finditer(t):
                gc[cm.group(1)] = gc.get(cm.group(1), 0) + 1
            dom = max(gc.values()) if gc else 0
            if dom > 1 and dom < stated:
                warn.append(f"#{idx}: says '{m.group(0)}' but clozes only {dom} items "
                            f"— a list item may be missing; verify against the full source page")
    return hard, warn


def load_live(which, source_id):
    """Pull cards from the live Anki deck(s) for a --live audit.

    The deck to sweep comes from the source registry, so this works for any registered
    source, not just the EMT textbook. `--live all` sweeps the whole source root;
    `--live N` sweeps that segment INCLUDING both the staging deck and the deck Parker
    promotes into, since hand-edit drift happens in whichever one he is studying."""
    def call(action, **params):
        req = urllib.request.Request(
            ANKI, data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
            headers={"Content-Type": "application/json"})
        try:
            res = json.loads(urllib.request.urlopen(req, timeout=30).read())
        except Exception as e:
            sys.exit(f"ERROR: cannot reach AnkiConnect at {ANKI}. Is Anki open? ({e})")
        if res.get("error"):
            raise RuntimeError(res["error"])
        return res["result"]
    src = S.get_source(source_id)
    if which == "all":
        query = f'deck:{src["deck_root"]}::*'
    else:
        try:
            seg = int(which)
        except ValueError:
            sys.exit(f"ERROR: --live expects a segment number or 'all', got {which!r}")
        query = f'deck:"{S.audit_deck(src, seg)}"'
    ids = call("findNotes", query=query)
    notes = call("notesInfo", notes=ids)
    cards = []
    for n in notes:
        f = n["fields"]
        text = f.get("Text", {}).get("value", "")
        cards.append({"noteId": n["noteId"], "Text": text,
                      "Back Extra": f.get("Back Extra", {}).get("value", ""),
                      "needs_human_check": bool(VALUE.search(readable(text)))})
    return cards


def main():
    ap = argparse.ArgumentParser(description="Deterministic gate / live audit for generated cards.")
    ap.add_argument("cards_json", nargs="?", help="staged JSON file to gate (default mode)")
    ap.add_argument("--live", metavar="N|all", help="audit live Anki cards instead of a file (diagnostic; no stamp)")
    ap.add_argument("--source", default=None,
                    help="source id for --live (see: sources.py list). Defaults to the "
                         "cards' own 'source' field in file mode.")
    ap.add_argument("--audit", action="store_true",
                    help="verifying PRE-EXISTING/rich cards: skip the minimal-HTML HARD gate (keep every other "
                         "check). Default (no flag) stays strict so NEW generated cards are held to b/i/br/img.")
    args = ap.parse_args()
    if not args.cards_json and not args.live:
        sys.exit("usage: check_cards.py [--audit] <cards.json>   |   "
                 "check_cards.py --live <N|all> --source <id>")

    live = bool(args.live)
    strict_html = not (args.audit or live)  # rich pre-existing / hand-edited cards relax the HTML gate
    if live:
        if not args.source:
            sys.exit("ERROR: --live needs --source <id> so it knows which deck to sweep.\n"
                     "See: python3 scripts/sources.py list")
        cards = load_live(args.live, args.source)
        label = [str(c["noteId"]) for c in cards]  # identify by noteId in live mode
    else:
        cards = json.load(open(args.cards_json))
        label = None

    hard, warn, reads = [], [], []
    for i, c in enumerate(cards):
        ident = label[i] if label else i
        h, w = per_card(ident, c, strict_html=strict_html)
        hard += h
        warn += w
        reads.append(readable(c.get("Text", "")))
    # in-batch near-duplicates
    for i in range(len(reads)):
        for j in range(i + 1, len(reads)):
            if len(reads[i]) < 20 or len(reads[j]) < 20:
                continue
            r = SequenceMatcher(None, norm(reads[i]), norm(reads[j])).ratio()
            if r > 0.82:
                a = label[i] if label else i
                b = label[j] if label else j
                warn.append(f"#{a} & #{b}: {r:.0%} similar Text — possible duplicate")

    print(f"checked {len(cards)} cards" + (f" (live: {args.live})" if live else ""))
    if hard:
        print("HARD ERRORS (block staging):")
        for h in hard:
            print("  x", h)
    if warn:
        print(f"WARNINGS ({len(warn)} — route to the LLM judge / human):")
        for w in warn:
            print("  !", w)
    if not hard and not warn:
        print("  deterministic checks clean")

    if live:
        sys.exit(0)  # diagnostic only: never stamp, never block

    # Verification stamp: on a HARD-clean pass, write a hash of THIS exact file so
    # anki_write.py can confirm the file it's about to stage is the one that passed
    # the gate. This makes Stage 2.75 physically unskippable (the writer refuses an
    # unstamped/edited file) without any global hook. Warnings don't block the stamp
    # — they're routed to the judge/human, per the pipeline contract.
    src = args.cards_json
    sp = stamp_path(src)
    if hard:
        if os.path.exists(sp):
            os.remove(sp)  # a previously-clean file went dirty; invalidate its stamp
    else:
        with open(sp, "w") as f:
            f.write(json.dumps({"sha256": file_hash(src), "warnings": len(warn)}))
        print(f"  stamped OK -> {os.path.basename(sp)}")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
