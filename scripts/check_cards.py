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
import json, re, sys, unicodedata
from difflib import SequenceMatcher

ALLOWED_TAGS = {"b", "i", "br", "img"}
CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}")
TAG = re.compile(r"</?([a-zA-Z0-9]+)[^>]*>")
# a real VALUE/dose/threshold (number + unit, comparison, or range) — NOT a bare
# list ordinal like "1. Detection" or a year inside a name.
VALUE = re.compile(r"[<>≤≥]\s*\d|\d+\s*(?:mg|mcg|g|mmHg|mL|%|/min|bpm|hours?|minutes?|seconds?)\b|\d+\s*(?:to|-|–)\s*\d+", re.I)


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


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: check_cards.py <cards.json>")
    cards = json.load(open(sys.argv[1]))
    hard, warn = [], []
    reads = []
    for i, c in enumerate(cards):
        t, be = c.get("Text", ""), c.get("Back Extra", "")
        # HARD: legal HTML
        bad = [g for g in (TAG.findall(t) + TAG.findall(be)) if g.lower() not in ALLOWED_TAGS]
        if bad:
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
        # WARN: looks numeric but not flagged
        if VALUE.search(readable(t)) and not c.get("needs_human_check"):
            warn.append(f"#{i}: looks numeric/dose but needs_human_check is false")
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
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
