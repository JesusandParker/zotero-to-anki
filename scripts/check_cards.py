#!/usr/bin/env python3
"""
check_cards.py — deterministic pre-flight GATE for EMT cards.

Runs the checks that CAN be mechanical, so they can never be skipped or
forgotten. Semantic checks (under-clozing, yield, subtle leaks) are the LLM
judge's job; this catches structure, format, literal leaks, missing flags, and
in-batch duplicates — including the exact shapes that have bitten us before
(see reference/regression-cases.md).

Usage: python3 scripts/check_cards.py work/chapter_N_cards.json
Exit 1 on any HARD error (blocks staging). WARNINGS print but don't block —
they are routed to the LLM judge / Parker.
"""
import hashlib, json, os, re, sys, unicodedata
from difflib import SequenceMatcher


def stamp_path(cards_json):
    return cards_json + ".verified"


def file_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

ALLOWED_TAGS = {"b", "i", "br", "img"}
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")
TAG = re.compile(r"</?([a-zA-Z0-9]+)[^>]*>")
# a real VALUE/dose/threshold (number + unit, comparison, or range) — NOT a bare
# list ordinal like "1. Detection" or a year inside a name.
VALUE = re.compile(r"[<>≤≥]\s*\d|\d+\s*(?:mg|mcg|g|mmHg|mL|%|/min|bpm|hours?|minutes?|seconds?)\b|\d+\s*(?:to|-|–)\s*\d+", re.I)
# "N <list-noun>" where the card should then cloze exactly N items. A mismatch means
# the card states one count but tests another number of items — the exact shape of the
# Ch3 "consider 7 factors" bug (source had 8). Catch it mechanically.
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
LIST_NOUNS = (r"factors|signs|steps|elements|questions|items|types|ways|routes|hazards|"
              r"circumstances|stages|consequences|forms|principles|functions|components|"
              r"categories|reasons|examples|cases|situations|conditions|features|actions|"
              r"criteria|rights|duties|methods|phases|properties|kinds")
COUNT_RE = re.compile(r"\b(\d+|" + "|".join(NUMWORDS) + r")\s+(?:\w+\s+){0,2}?(?:" + LIST_NOUNS + r")\b", re.I)


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
    """R11: a hint that is just the leading letter(s) of its own answer, with NO
    spelled acronym visible in the stem (which would license it as a mnemonic)."""
    stem_plain = re.sub(r"<[^>]+>", " ", CLOZE.sub(lambda m: " ", text))
    has_acronym = bool(ACRONYM.search(stem_plain))
    if has_acronym:
        return []  # SAMPLE/DCAP-BTLS style — first-letter hints are licensed
    leaks = []
    for m in CLOZE.finditer(text):
        ans, hint = m.group(2), (m.group(3) or "")
        h = re.sub(r"[^a-z]", "", norm(hint))
        a = re.sub(r"[^a-z]", "", norm(ans))
        # a genuine forced-choice hint contains "/" or " or " (len guards those out)
        if 1 <= len(h) <= 2 and a.startswith(h) and "/" not in hint and " or " not in hint.lower():
            leaks.append((ans, hint))
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
    operated by' = 5 content words). Also excludes <br>-listed or counted sets."""
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


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit("usage: check_cards.py [--audit] <cards.json>")
    # --audit: verifying PRE-EXISTING cards, which may legitimately carry rich HTML the
    # generation pipeline forbids (embedded reference images/links, formatted tables, the
    # Ch5 clinical-ex blocks). Skip the minimal-HTML gate; keep every meaningful check.
    # Default (no flag) stays strict, so NEW generated cards are still held to <b>/<i>/<br>/<img>.
    audit = "--audit" in flags
    cards = json.load(open(args[0]))
    hard, warn = [], []
    reads = []
    for i, c in enumerate(cards):
        t, be = c.get("Text", ""), c.get("Back Extra", "")
        # HARD: legal HTML (strict mode only)
        bad = [g for g in (TAG.findall(t) + TAG.findall(be)) if g.lower() not in ALLOWED_TAGS]
        if bad and not audit:
            hard.append(f"#{i}: disallowed HTML tag(s): {sorted(set(bad))}")
        # HARD: must contain a cloze
        if not CLOZE.search(t):
            hard.append(f"#{i}: no cloze markup in Text")
        # WARN: literal answer visible in the stem (a leak)
        for g in {m.group(1) for m in CLOZE.finditer(t)}:
            stem = norm(visible_stem(t, g))
            for m in CLOZE.finditer(t):
                if m.group(1) == g:
                    a = norm(m.group(2))
                    if a and len(a.split()) <= 4 and re.search(r"\b" + re.escape(a) + r"\b", stem):
                        warn.append(f"#{i}: answer '{m.group(2)}' is visible in its own stem (leak)")
        # WARN: parenthetical hanging right off a cloze (the pathway-card leak shape)
        if re.search(r"\}\}\s*\(", t):
            warn.append(f"#{i}: parenthetical right after a cloze — verify it is NOT the answer's definition (leak risk)")
        # WARN: first-letter hint on a non-mnemonic list (R11, the ::r/::k/::s leak)
        for ans, hint in first_letter_hint_leaks(t):
            warn.append(f"#{i}: hint '::{hint}' is the first letter of its answer '{ans}' with no acronym in the stem — first-letter leak (card-rules #18)")
        # WARN: all-blanks-at-once husk — mutually-dependent spans under one number (R10)
        for g in husk_groups(t):
            warn.append(f"#{i}: cloze c{g} hides 2-3 multi-word spans in an inline template — possible husk; verify each blank is answerable with the other shown, else split into c1/c2 (card-rules #17)")
        # WARN: synonym-equation husk — both sides of 'X = also called Y' under one number (R10)
        for g in equation_husk_groups(t):
            warn.append(f"#{i}: cloze c{g} hides BOTH sides of a synonym/equation ('___ = also called ___') — husk; renumber so each card shows one side as the anchor (card-rules #17)")
        # WARN: looks numeric but not flagged
        if VALUE.search(readable(t)) and not c.get("needs_human_check"):
            warn.append(f"#{i}: looks numeric/dose but needs_human_check is false")
        # WARN: stated list-count != number of clozed items (the "7 vs 8 factors" bug)
        m = COUNT_RE.search(readable(t))
        if m:
            stated = NUMWORDS.get(m.group(1).lower(), None)
            if stated is None:
                try: stated = int(m.group(1))
                except ValueError: stated = None
            if stated and 2 <= stated <= 20:
                # Count members of the dominant cloze group (the list group) and warn only
                # on an UNDERCOUNT — fewer clozed items than the stated number, i.e. a
                # dropped list item (the real "7 vs 8 factors" bug). An OVERCOUNT is almost
                # always a branch/alternative ("recovery, or exhaustion" = one stage, two
                # outcomes) and is safe, so it isn't flagged (avoids false positives).
                by_group = {}
                for cm in CLOZE.finditer(t):
                    by_group.setdefault(cm.group(1), 0)
                    by_group[cm.group(1)] += 1
                dom = max(by_group.values()) if by_group else 0
                if dom > 1 and dom < stated:
                    warn.append(f"#{i}: says '{m.group(0)}' but clozes only {dom} items "
                                f"— a list item may be missing; verify against the full source page")
        reads.append(readable(t))
    # WARN: in-batch near-duplicates
    for i in range(len(reads)):
        for j in range(i + 1, len(reads)):
            r = SequenceMatcher(None, norm(reads[i]), norm(reads[j])).ratio()
            if r > 0.80:
                warn.append(f"#{i} & #{j}: {r:.0%} similar Text — possible duplicate")

    print(f"checked {len(cards)} cards")
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

    # Verification stamp: on a HARD-clean pass, write a hash of THIS exact file so
    # anki_write.py can confirm the file it's about to stage is the one that passed
    # the gate. This makes Stage 2.75 physically unskippable (the writer refuses an
    # unstamped/edited file) without any global hook. Warnings don't block the stamp
    # — they're routed to the judge/human, per the pipeline contract.
    src = args[0]
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
