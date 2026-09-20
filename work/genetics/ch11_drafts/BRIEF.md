# Genetics chapter 11 (Transcription and RNA Processing) — drafting brief

You are one drafter in a fan-out. You draft Anki cloze cards for ONE assigned group of
Parker's marks, write them to your unit file, and stop. An independent editor will
adversarially review your file afterwards; a consolidation pass then dedupes across units.

## 0. Read these first, fully (they are the standard; nothing here overrides them)
Repo root: /Users/parkerregner/.claude/skills/zotero-to-anki
1. reference/card-rules.md          (all of it — Layer A, Layer B, rules 0–35)
2. reference/parker-preferences.md  (wins over card-rules on conflict)
3. reference/card-recipes.md        (the archetype playbook; §4 two-way definitions, §5 numbers, §6 lists, §7 sequences, §8 comparisons)
4. reference/editor-checklist.md    (run it on your own cards before you hand off)
5. reference/note-format.md         (the card object, allowed HTML, Back Extra labels)
6. reference/profiles/science.md    (the subject emphasis: mechanism-heavy)

## 1. The inputs
- Marks: work/genetics/chapter_11_highlights.json (index = position in the list, 0–69).
  A readable dump of every mark (highlight text + Parker's margin comment + the extractor's
  context paragraph) is work/genetics/ch11_drafts/MARKS_DUMP.txt.
- Full page text (pdftotext -layout, PHYSICAL page numbers): work/genetics/ch11_pages/pNNN.txt
  (p274–p301). Printed page = physical − 22. ALWAYS read the full page(s) your marks sit on —
  the extractor's context is a 450-char window and lists/sentences cross page breaks.
- Page renders (170 dpi) for pages the text layer could not read:
  /private/tmp/claude-501/-Users-parkerregner/93c1419e-ecdb-483b-a557-c23367e50728/scratchpad/renders/p{277,282,283,286,288}.png
  and 100-dpi renders of every page p275–p298 in .../scratchpad/pages100/pNNN.png
- Evidence crops (already cut, verified verbatim by the orchestrator) for the four marks the
  text layer did NOT locate (grounding NOT_FOUND, context empty):
    mark 30 → work/genetics/figures/evidence/p282_mark30_recognition_sequence.png
    mark 31 → work/genetics/figures/evidence/p283_mark31_rho_terminator_types.png
    mark 32 → work/genetics/figures/evidence/p283_mark32_hairpin_pauses.png
    mark 57 → work/genetics/figures/evidence/p288_mark57_TFIIH_helicase.png
  A card built from one of these MUST carry `visual_source` (see schema) naming the crop.

## 2. The four rules that override everything
0. Cards come ONLY from Parker's marks. Never card unmarked text, however testable. Unmarked
   neighbouring sentences may feed a Back Extra teaching line ONLY (and you cite them in
   `verified_against` prefixed "Back Extra (unmarked, teaching only) pNNN: '…'"). A cloze
   ANSWER must always come from a marked span (or from the authorized lane, unit D7 only).
1. Ground every claim in the page. Quote the page verbatim in `verified_against` for every
   card, one quote per fact, in the form  p281: 'exact sentence' | p282: 'exact sentence'.
2. Zero guessing. If a number, sequence, or claim is not on the page, it is not on the card.
3. Nothing is final — Parker judges in review — but ship your best.

## 3. The card object (write EXACTLY these keys; extra `_`-prefixed keys are fine)
{
  "Text": "…cloze text…",
  "Back Extra": "Label: …<br><br>Label: …",
  "source": "genetics",
  "segment": 11,
  "from_idx": [<mark indices this card is built from>],
  "block": "U6_rna_polymerase_subunits",
  "numeric": false,
  "verified_against": "p281: '…' | p281: '…'",
  "verified_by": "drafter-D2",
  "needs_human_check": false,
  "visual_source": null,
  "image": null,
  "_unit": "D2",
  "_unit_idx": 0,
  "_fact_pass": {"must_test": ["…"], "supporting": ["…"], "skip": ["…"]},
  "_archetype": "two-way definition | mechanism | list | comparison | numeric | sequence | vignette",
  "_figure_request": "FIGURE 11.8"   (optional: which book plate should sit on the BACK; the orchestrator attaches it)
}
- `visual_source` when a fact was read off a render/crop:
  {"pages": ["283"], "figures": ["work/genetics/figures/evidence/p283_mark31_rho_terminator_types.png"], "labels": [], "note": "mark not located by the text layer; sentence read verbatim on the rendered page"}
- `numeric: true` on any card stating a number, count, size, position, percentage, or a
  nucleotide SEQUENCE (TATAAT etc. count as values). Verify every digit/letter against the page text.
- `needs_human_check` is DERIVED later by verify_report.py — leave false unless grounding is
  genuinely weak.
- Back Extra: 1–3 labeled lines (Distinguish: / Pitfall: / Why: / Mechanism: / Ex: / Cue: /
  Pathway: / Mnemonic: / Roster: / Meaning:), separated by <br><br>, each adding an edge the
  Text does not state. Never re-define a term the Text defines. Plain words.
- HTML allowed: <b>, <i>, <br>, <img> only. Italicize species names (<i>E. coli</i>).
- Cloze syntax: {{c1::answer::hint}}; hints are slot-labels (category/form/forced-choice),
  never synonyms; a direction/binary blank MUST carry a ::A or B hint; a bare count in front
  of its noun needs a ::number of … hint (rule 27).

## 4. Method, per unit (do this in order, and write your notes into `_fact_pass`)
a. Rule 0 — group adjacent parallel marks into ONE unit before drafting anything.
b. Fact pass — list every atomic proposition in the marked span(s) + their context and tag
   MUST-TEST / SUPPORTING / SKIP. Every MUST-TEST fact gets clozed somewhere.
c. Pick the archetype (recipes §1 table), then draft.
d. Size it (rule 23): ≤4 uncued answers per cloze group; ≥8 must be chunked into separate
   NOTES (never c1..cN on one note, rule 24). A keyed panel of NUMBERS = one note per key (rule 25).
e. Definitions are TWO-WAY by default: {{c1::TERM::hint}} is {{c2::crisp meaning}} (c2 ≤ ~8 words).
   Do NOT two-way lists, sequences, numbers, scenarios.
f. Cold-solve every card AND every row: cover the answer — could a knower write exactly it,
   cold? No open-set blanks (rule 16), no husks (rule 17), no first-letter hints (rule 18),
   no row that restates its label (rule 20), no absolute with a lone unhinted blank (rule 21).
g. Under-clozing check (rule 7): no testable fact left as visible scenery.
h. Run reference/editor-checklist.md on each card yourself; fix; then hand off.
i. Dedupe by MEANING within your unit (rule 12). Do not worry about other units — the
   consolidation pass handles cross-unit duplicates.

## 5. Volume and tone
A yellow mark is Parker's decision that it matters: never drop one, never pad. Typical yield is
0.7–1.2 cards per yellow mark after grouping. Sentences read like a tutor quizzing him, 12–35
words, hard max 60. Scientific register is fine; jargon defined once in the Back Extra.

## 6. Output
Write ONLY your unit file: work/genetics/ch11_drafts/<UNIT>_cards.json — a JSON list of card
objects. Then reply with a 10-line summary: cards drafted, which marks each cites, anything
you could not ground, any margin comment you honoured, and any mark you believe deserves a
figure on its back (name the FIGURE). Write the file BEFORE the summary.
