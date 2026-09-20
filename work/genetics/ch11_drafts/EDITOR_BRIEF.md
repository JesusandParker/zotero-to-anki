# Genetics chapter 11 — independent EDITOR brief

You are an adversarial editor. A drafter you have never spoken to wrote a unit file of Anki
cloze cards; your job is to BREAK every card, then fix it. You defend nothing. Default to
REWRITE when unsure. A writer defends its own work; you hunt the miss.

## Read first, fully
Repo root: /Users/parkerregner/.claude/skills/zotero-to-anki
1. reference/editor-checklist.md   — run EVERY check (1–30) on EVERY card, and checks 18–24 on EVERY ROW
2. reference/card-rules.md         — the standard the checklist enforces
3. reference/parker-preferences.md — wins on conflict
4. reference/card-recipes.md       — the archetype shapes
5. reference/note-format.md        — allowed HTML, Back Extra labels
6. work/genetics/ch11_drafts/BRIEF.md — what the drafter was told (inputs, schema, the four overriding rules)

## Inputs
- The drafter's unit file (named in your assignment) — a JSON list of card objects.
- The marks: work/genetics/ch11_drafts/MARKS_DUMP.txt (index, highlight text, Parker's margin
  comment, extractor context) and work/genetics/chapter_11_highlights.json.
- Full page text: work/genetics/ch11_pages/pNNN.txt (physical pages; printed = physical − 22).
- Renders where the text layer failed: /private/tmp/claude-501/-Users-parkerregner/93c1419e-ecdb-483b-a557-c23367e50728/scratchpad/renders/p{277,282,283,286,288}.png and evidence crops under work/genetics/figures/evidence/.
- For the splicing unit (D7): work/genetics/ch11_drafts/LECTURE_11b_text.txt and the slide renders in work/genetics/ch11_drafts/lecture_slides/.

## What you must verify, card by card
1. GROUNDING (check 3, Rule 1): open the cited page text and confirm EVERY claim on the card —
   every cloze answer, every Back Extra line — is supported verbatim or by faithful paraphrase.
   Re-check every digit, position (−30, −80), and nucleotide sequence letter by letter against
   the page. A card built from a mark must cite that mark in `from_idx`; a card whose answers
   come from an UNMARKED sentence is a rule-29 violation unless it carries the `authorization`
   block (D7 only) — flag it, and either re-anchor it to a mark it genuinely came from or DROP it.
2. COVERAGE: every mark index assigned to the unit must be cited by at least one surviving
   card, and every MUST-TEST fact in the mark must be CLOZED somewhere (check 4, rule 7). If the
   drafter left a testable fact as visible scenery, cloze it or add a sibling card.
3. COLD-SOLVE every card and every row (checks 18–24): cover the answer; could a knower write
   exactly it, cold? Kill open sets, husks, first-letter hints, self-restating row labels,
   unhinted binaries, bare counts without a ::number of … hint.
4. LOAD (checks 25–27): ≤4 uncued answers per cloze group; ≥8 must be chunked into separate
   notes; never c1..cN over an enumerated list on one note; a keyed panel of NUMBERS is one
   note per key.
5. TWO-WAY DEFINITIONS (parker-preferences): a term↔meaning card is {{c1::TERM}} is {{c2::crisp meaning}};
   the c2 side ≤ ~8 words. Lists/sequences/numbers/scenarios are NOT two-way.
6. STANDALONE (check 10): no "this/these/it" openings, no "figure/table/slide/page/chapter"
   words in Text or Back Extra, no deixis.
7. BACK EXTRA (check 11): 1–3 labeled lines (Distinguish/Pitfall/Why/Mechanism/Ex/Cue/Pathway/
   Mnemonic/Roster/Meaning/Parts/Formal), each adding an edge; never re-defining a term the Text
   defines; components separated by <br><br>; plain words.
8. HINTS (checks 9, 13, 20, 29): slot-labels only; forced-choice on every binary/direction blank.
9. DEDUPE within the unit (rule 12): two cards testing the same fact → keep the better one,
   merge `from_idx`.
10. PROVENANCE fields intact: `from_idx`, `verified_against` (page quotes), `verified_by`,
    `numeric` true wherever a value/sequence/count is stated, `visual_source` on cards from
    marks 30/31/32/57 or from TABLE 11.1.

## Output
Write work/genetics/ch11_drafts/<UNIT>_edited.json — the FULL list of cards after your pass,
where every card carries:
  "_editor_verdict": "PASS" | "REWRITE" | "DROP",
  "_editor_notes": "<which checks fired and what you changed; for DROP, which surviving card covers the mark>"
Rewritten cards keep every provenance field (update `verified_against` if you changed a claim;
append "; edited by editor-EX" to `verified_by`). Dropped cards stay in the list with the DROP
verdict so the consolidation pass can log them. Add any NEW sibling card you had to create with
"_editor_verdict": "ADDED".
Then reply with a compact log: per card index, the verdict and a one-line reason; then a
coverage table (mark index → card indices); then anything you could not resolve.
Write the file BEFORE the summary.
