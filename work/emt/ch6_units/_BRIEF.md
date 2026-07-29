# Chapter 6 drafting brief (read this first, in full)

You are drafting Anki cloze cards for **one block** of AAOS EMT 12e **Chapter 6 — The Human Body**
(physical PDF pages 515–680). Parker highlighted these spans in yellow, which is his decision
that they matter. Your job is to render them into excellent cards, not to re-decide importance.

Skill root: `/Users/parkerregner/.claude/skills/zotero-to-anki`

## 1. Read the standards BEFORE drafting (mandatory, in this order)
1. `reference/card-rules.md` — the full standard. Rule 0 (connected-highlight synthesis) and
   rules 16–18 (the Cold-Solve Gate) are the ones most often violated.
2. `reference/parker-preferences.md` — his tastes; these WIN over card-rules on conflict.
3. `reference/card-recipes.md` — the archetype playbook. Consult the matching § for every card.
4. `reference/profiles/emt.md` — subject emphasis.
5. `reference/editor-checklist.md` — the 20 adversarial checks you must run on your own drafts.

## 2. Chapter 6 is a RECALL-HEAVY chapter — this changes the mix
`profiles/emt.md` §2 names "The Human Body" explicitly as recall-heavy: it flips toward
**definitions, anatomy, structure→function, and normal values**, with **far less scenario**.
Do NOT force clinical vignettes onto anatomy. The auto-pair scenario rule is *light* here —
use it only where the fact genuinely drives a field decision (e.g. a normal range an EMT acts
on, an organ whose location predicts an injury pattern, a nerve whose damage stops breathing).
Anatomy trivia does not get a fake ambulance story wrapped around it.

Two-way definitions (`{{c1::TERM}} is {{c2::crisp meaning}}`) are the workhorse here — that is
Parker's default for foundational vocabulary, and this chapter is almost entirely foundational
vocabulary. Keep the c2 side to ~3–6 discriminating words.

## 3. Your input
`work/emt/ch6_units/<BLOCK>.json` — `{block, scope, items[]}`. Each item has:
`_idx` (its global position), `page`, `highlight` (the exact yellow span), `context` (the
grounded page paragraph — **every claim on your card must be supported by this**),
`grounding` (EXACT / PARTIAL / NOT_FOUND), `list_lead_in`, and sometimes `user_comment`.

### `user_comment` is Parker talking directly to you. It is binding.
Obey it exactly, and report in your summary how you honored it. It overrides your judgment.

### Reading the real source page (you WILL need this)
The 450-char `context` truncates lists and never contains table bodies. For any
`list_lead_in: true` item, any highlight that is a **TABLE title**, and any card that states a
count, read the actual page(s):

```
pdftotext -layout -f <PAGE> -l <PAGE> "/Users/parkerregner/Zotero/storage/Z98PW7AT/Pollak et al. - 2021 - Emergency care and transportation of the sick and injured.pdf" -
```
Lists that spill across a page break are the classic failure (card-rules #14, editor check #17):
always read the next page too. A stated count that ≠ the number of clozed items is a defect.

**A highlighted TABLE title means "card the table's content."** Dump the page, read the whole
table, and build the card(s) from the rows — never make a card that refers to "the table."

## 4. Method — one unit at a time, never bulk
0. **Group first (card-rules Rule 0).** Scan neighbouring items (same page, consecutive,
   overlapping context). Parallel pieces of one idea = ONE unified card, not fragments.
   A cohesive list stays whole in one grouped card no matter its length.
1. **Classify** the fact type, open the matching § of `card-recipes.md`, use its template.
2. **Fact pass, THEN draft.** List every atomic proposition in the span + context and tag each
   MUST-TEST (definition, goal/function, number, discriminating feature, ordered step, location)
   / SUPPORTING / SKIP. Then draft so every MUST-TEST fact is clozed *somewhere*. A must-test
   fact left visible as scenery is the under-clozing bug — the single most common defect.
3. **Adversarially edit** each draft against all 20 checks in `editor-checklist.md`. Try to
   BREAK the card. Default to rewrite when unsure.

## 5. Hard requirements
- **Never drop a yellow span.** If one still looks uncardable after Rule 0 grouping, emit it
  with `needs_human_check: true` and explain — never silently discard.
- **Zero guessing.** Every claim traceable to `context` or the source page you read. If the
  source doesn't support it, don't write it.
- **Every number, measurement, threshold, range, percentage, or time window → `needs_human_check: true`**,
  and verify the digits verbatim against the source first. This chapter is full of them.
- Also flag `needs_human_check: true` for any item whose `grounding` is PARTIAL or NOT_FOUND.
- Back Extra is required on every card: 1–3 lines, each opening with one of
  `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:`.
  Separate distinct components with `<br><br>`. It must teach an edge the Text does not state;
  for a definition card it may NOT re-define the term (use Distinguish/Pitfall/Cue).
- HTML allowed: `<b>`, `<i>`, `<br>` only. No `<u>`, no entities, no tables, no divs.
- 12–35 words typical, hard max 60. Max 2 sentences.
- Hints label the answer's FORM only. No first-letter hints unless the stem teaches a spelled
  acronym. Any bare direction/binary blank MUST carry a forced-choice `::a or b` hint.

## 6. Output
Write `work/emt/ch6_units/<BLOCK>_draft.json` — a JSON array of card objects:
```json
{
  "Text": "The {{c1::sagittal (lateral) plane::body plane}} divides the body into {{c2::left and right}} sections.",
  "Back Extra": "Distinguish: the midsagittal plane is the sagittal plane drawn exactly at midline, giving equal halves.",
  "source": "emt",
  "segment": 6,
  "needs_human_check": false,
  "image": null,
  "from_idx": [2]
}
```
`from_idx` = the `_idx` values of every item the card covers (this is how coverage is audited —
every one of your block's indices must appear in at least one card's `from_idx`).

Then print a short report: card count, how you grouped, how you honored any `user_comment`,
which cards are flagged and why, and anything you could not ground.

**Quality over speed. Parker will gladly wait for better cards.** A card he cannot answer cold —
on first sight, knowing the material — is his single loudest complaint. Test every card that way
before you emit it: cover the answer, and ask "could I have produced exactly this?"
