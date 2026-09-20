# Genetics chapter 11 — FINAL JUDGE brief

You are the last independent pair of eyes before these cards are written into Parker's Anki.
Drafters wrote them, independent editors rewrote them, and a consolidation pass deduped them.
You have seen none of that. Your job is to run the FULL editor checklist on every card in the
consolidated file, as an adversary, and to report only defects you can point at.

## Read first, fully
Repo root: /Users/parkerregner/.claude/skills/zotero-to-anki
1. reference/editor-checklist.md (all checks; 18–24 per ROW)
2. reference/card-rules.md
3. reference/parker-preferences.md
4. reference/card-recipes.md (§4, §4b, §5, §6, §7, §8, §10)
5. reference/note-format.md
6. work/genetics/ch11_drafts/BRIEF.md (what drafters were told) and EDITOR_BRIEF.md

## Inputs
- The consolidated file: work/genetics/chapter_11_cards.json
- Marks: work/genetics/ch11_drafts/MARKS_DUMP.txt · work/genetics/chapter_11_highlights.json
- Page text: work/genetics/ch11_pages/pNNN.txt (physical pages; printed = physical − 22)
- Lecture: work/genetics/ch11_drafts/LECTURE_11b_text.txt + lecture_slides/*.png
- The gate's own warnings for this file (given in your assignment) — adjudicate each one:
  CLEAR (say why the detector is wrong here) or FIX (say the fix).

## Verdict rules
- For each card index: PASS, FIX (with the exact replacement Text and/or Back Extra), or DROP
  (with the sibling card that keeps the mark covered — never leave a yellow mark uncovered).
- Check grounding by OPENING the cited page text; a claim you cannot find on the cited page is a
  FIX or DROP, never a PASS. Re-verify every digit, position and nucleotide sequence.
- Check the whole batch for CROSS-CARD give-aways (check 16) and same-fact duplicates (rule 12):
  list any pair that tests the same fact.
- Check every lexicon (purple) card against check 30: plain · crisp (≤ ~8 words) · faithful to the
  anchor quote in `verified_against`.
- Check every authorized-lane card (has an `authorization` block): its `verified_against` must
  quote the book page or the slide it came from; the block is verbatim Parker.

## Output
Write work/genetics/ch11_drafts/JUDGE_verdicts.json — a JSON list, one object per card index in
the consolidated file: {"idx": N, "verdict": "PASS|FIX|DROP", "checks_fired": ["18","25"],
"reason": "…", "Text": "<replacement, only for FIX>", "Back Extra": "<replacement, only for FIX>"}.
Then reply with: counts (PASS/FIX/DROP), the list of FIX/DROP indices with one-line reasons,
the duplicate/give-away pairs, and your adjudication of each gate warning.
Write the file BEFORE the summary.
