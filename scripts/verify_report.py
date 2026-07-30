#!/usr/bin/env python3
"""
verify_report.py — derive `needs_human_check` honestly, and split the verification
report into "you must look at this" and "you may skim this".

The problem this fixes: `needs_human_check` was ASSERTED by whoever wrote the card, and
in practice it meant "this card contains a digit." On a recall-heavy chapter that fired
on 1-5% of cards and was a useful triage list. On EMT Chapter 6 (anatomy, wall-to-wall
numbers) it fired on 72 of 202 cards — 35% — and the run's own report conceded it was
"a confirmation pass, not a list of suspected errors." A flag that fires on a third of
the deck is not triage, and 72 items is more than anyone actually checks before promoting.

The fix is not to weaken the safety rule. It is to record WHAT VERIFICATION HAPPENED, and
then compute the flag from that:

    numeric            -> this card states a value, dose, threshold, or time window
    verified_against   -> the page its digits were checked against, e.g. "p531"
    verified_by        -> who checked ("judge", "agent", "parker")

    needs_human_check  = (numeric or weak grounding) AND NOT verified_against

So a number that was genuinely verified against a named page stops competing for Parker's
attention with one that nobody checked. The safety principle survives intact — every digit
still gets surfaced — but Section A becomes the short list that actually needs his eyes,
and Section B stays available to skim.

Run this BEFORE the gate (it rewrites the cards file, which invalidates any stamp):

    python3 scripts/verify_report.py work/emt/chapter_6_cards.json
    python3 scripts/verify_report.py work/emt/chapter_6_cards.json --dry-run
"""
import argparse, json, os, re, sys

import check_cards as C
import sources as S


def cited_grounding(card, highlights):
    """Worst grounding/content status among the marks this card cites."""
    worst, visual = "EXACT", False
    for j in card.get("from_idx") or []:
        if not (isinstance(j, int) and 0 <= j < len(highlights)):
            continue
        h = highlights[j]
        if h.get("grounding") == "NOT_FOUND":
            worst = "NOT_FOUND"
        elif h.get("grounding") == "PARTIAL" and worst != "NOT_FOUND":
            worst = "PARTIAL"
        if h.get("needs_visual"):
            visual = True
    return worst, visual


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards_json")
    ap.add_argument("--highlights", default=None)
    ap.add_argument("--out", default=None, help="report path (default: <cards>_VERIFY.md alongside)")
    ap.add_argument("--dry-run", action="store_true", help="report only; do not rewrite the cards file")
    args = ap.parse_args()

    cards = json.load(open(args.cards_json))
    highlights, hlpath = C.highlights_for(cards, args.highlights)
    highlights = highlights or []

    changed = 0
    section_a, section_b = [], []
    for i, c in enumerate(cards):
        text_plain = C.readable(c.get("Text", ""))
        numeric = bool(C.VALUE.search(text_plain))
        ground, needs_visual = cited_grounding(c, highlights) if highlights else ("EXACT", False)
        weak = ground in ("PARTIAL", "NOT_FOUND")
        verified = bool(c.get("verified_against"))

        derived = bool((numeric or weak) and not verified)
        if c.get("numeric") != numeric:
            c["numeric"] = numeric
        if c.get("needs_human_check") != derived:
            c["needs_human_check"] = derived
            changed += 1

        if not (numeric or weak):
            continue
        page = ", ".join(f"p{highlights[j]['page']}" for j in (c.get("from_idx") or [])
                         if isinstance(j, int) and 0 <= j < len(highlights)) or "?"
        entry = {"i": i, "page": page, "text": text_plain,
                 "verified_against": c.get("verified_against"),
                 "verified_by": c.get("verified_by"),
                 "ground": ground, "needs_visual": needs_visual}
        (section_b if verified else section_a).append(entry)

    if not args.dry_run:
        with open(args.cards_json, "w") as f:
            json.dump(cards, f, indent=1, ensure_ascii=False)
            f.write("\n")

    out = args.out or args.cards_json.replace("_cards.json", "_VERIFY.md")
    label = os.path.basename(args.cards_json).replace("_cards.json", "")
    lines = [f"# {label} — verification report", ""]
    lines += [f"{len(section_a) + len(section_b)} of {len(cards)} cards state a value, dose, threshold, "
              f"or time window, or rest on weak grounding.", ""]
    lines += ["## Section A — needs your eyes", ""]
    if section_a:
        lines += [f"Nothing recorded a verification source for these {len(section_a)} cards. "
                  f"Check each digit against the page before promoting.", ""]
        for e in section_a:
            tag = " **[weak grounding]**" if e["ground"] != "EXACT" else ""
            tag += " **[from an image]**" if e["needs_visual"] else ""
            lines.append(f"- **[{e['page']}]**{tag} {e['text']}")
    else:
        lines += ["_Empty — every numeric card records the page its digits were checked against._"]
    lines += ["", "## Section B — verified, skim if you like", ""]
    if section_b:
        lines += [f"{len(section_b)} cards whose digits were checked against a named page. "
                  f"Listed for your confidence, not because anything is suspected.", ""]
        for e in section_b:
            lines.append(f"- [{e['verified_against']} · {e['verified_by'] or 'checked'}] {e['text']}")
    else:
        lines += ["_Empty._"]
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"{len(cards)} cards | numeric-or-weak: {len(section_a) + len(section_b)}")
    print(f"  Section A (needs your eyes): {len(section_a)}")
    print(f"  Section B (verified, skim) : {len(section_b)}")
    if changed and not args.dry_run:
        print(f"  rewrote needs_human_check on {changed} card(s) -> re-run check_cards.py to re-stamp")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
