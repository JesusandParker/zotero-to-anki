# Unit D — Infant psychosocial development (marks 20, 21, 22)

5 notes → 8 Anki cards (notes 1, 2, 5 are single-cloze; note 3 is c1/c2/c3; note 4 is c1/c2).
`check_cards.py` (with `--highlights work/emt/chapter_7_highlights.json`) is HARD- and WARN-clean.

## Fact pass

| Mark | Fact | Verdict | Where it landed |
|---|---|---|---|
| 20 | TABLE 7-2 caption + its eleven age→characteristic rows (2–12 months) | **MUST-TEST** | Notes 1 and 2 (the two match cards) |
| 20 | Teething is painful, sometimes with low-grade fever (context, un-highlighted) | SKIP | Not yellow. Teething appears only as the 6-month row. |
| 20 | Crying is the infant's primary way to signal distress; parents read the tone (context, un-highlighted) | SKIP | Not yellow; used as a `Cue:` on note 3 instead. |
| 20 | Bonding / secure attachment / anxious-avoidant attachment (context, un-highlighted) | SUPPORTING | Anxious-avoidant became the `Distinguish:` line on note 3. |
| 21 | Separation anxiety in older infants = clinginess + fear of unfamiliar places and people; peaks 10–18 months | **MUST-TEST** | Note 3 (c1 term / c2 meaning / c3 age window) |
| 22 | Trust versus mistrust = the psychosocial stage from birth to ~18 months | **MUST-TEST** | Note 4 (two-way: c1 name ↔ c2 window) |
| 22 | "…children learn whether they can trust the people around them" | **UNTESTABLE — deliberately not clozed** | Back Extra `Meaning:` on note 4. See below. |
| 22 | Trust is built by the quality and **consistency** of care; needs met consistently in a stable environment → trust | **MUST-TEST** | Note 5 |
| 22 | Inconsistent / emotionally unavailable / rejecting caregivers → mistrust | SUPPORTING | `Distinguish:` on note 5 (kept off the front on purpose — see below). |

Every mark is covered by at least one card. Nothing was dropped or flagged un-cardable.

## Decisions worth reviewing

**1. TABLE 7-2 is carded milestone → age, not age → milestone.** The brief allowed either
direction. I went with the reverse for four reasons:

- *Crisp-cloze (R5).* Age → milestone means producing ~35 words of behavioral prose per
  card, verbatim. Milestone → age means producing one number per row while the long,
  discriminating cue stays visible and free.
- *Row-level cold-solve (R16/R20).* "At 4 months → ___" is open-set: countless true
  statements fit a 4-month-old, and nothing visible singles out the book's entry. That is
  exactly the R9 shape. "Reaches arms out to people; drools → ___" forces one age.
- *R22 blesses this exact shape* — `description = {{c1::category}}` is the named
  classify/match exemption, not a fragment-clozed list.
- It is the direction the material is actually used in: you observe what the infant is
  doing and infer whether it is age-appropriate.

**2. Row order inside each card is deliberately scrambled.** In book order the answers run
2,3,4,5,6 (and 7…12) straight down the card, so after one review Parker could count them
off without knowing anything. Scrambling also hides the range, so the answer set stays the
full 2–12 months rather than a five-element menu he can solve by elimination. **Do not
"fix" these back into ascending order.**

**3. The split is 2–6 months (5 rows) and 7–12 months (6 rows)** — eleven rows in one note
would violate card-recipes §6 ("split a long list by logical subset"), and eleven micro-cards
would shred a cohesive table. Both cards share a lead-in, so expect a **similar-Text warning**
at consolidation; they are not duplicates.

**4. Three look-alike row pairs exist inside TABLE 7-2 and are handled, not ignored:**
- 3 mo "brings objects to the mouth" vs 9 mo "explores objects with the mouth" → split
  across the two cards, and cross-linked in note 1's `Distinguish:`.
- 10 mo "responds to his or her name" vs 12 mo "knows his or her name" → same card,
  disambiguated by the crawls/walks clause and named in note 2's `Distinguish:`.
- 11 mo "begins to walk without assistance" vs 12 mo "walks" → same card, same `Distinguish:`.
Each row keeps both of the book's clauses precisely because the second clause is what makes
the age forced. Don't trim the visible labels.

**5. Mark 22's "children learn whether they can trust the people around them" is not clozed
on purpose.** The book itself says "as the name implies" — the term *trust versus mistrust*
states its own content, so clozing it is a pure R3 tautology (and clozing the term with that
clause visible would leak "trust" straight back). It sits in note 4's `Meaning:` line, which
is legitimate because note 4's Text is a name↔age-window card, not a meaning card.

**6. Note 5 keeps the negative arm off the front on purpose.** A visible contrast
("…whereas caregivers who are **inconsistent**…") would leak the answer "consistency" and
vice-versa — the axis is self-leaking in either direction. The positive mechanism is the
cloze; the inconsistent/unavailable/rejecting arm is the `Distinguish:` line.

## What the consolidation stage must know

**A. Mark 18 (unit C) restates three TABLE 7-2 rows — my cards already cover them.**
Mark 18's body prose says: "by 2 months of age, infants can track objects with their eyes
and recognize familiar faces. At 6 months, they can sit upright, and they begin to make
cooing and babbling sounds. By 12 months the infant can walk with minimal assistance and
knows his or her name." The 2-month and 12-month claims are straight duplicates of my
note 1 and note 2 rows — **dedupe toward the table cards** (R12).

Two deltas that are NOT duplicates, and one real conflict:
- "cooing and babbling sounds" at 6 months is prose-only; the table's 6-month row says
  "speaks one-syllable words." Related but not the same claim.
- "walk with **minimal assistance**" at 12 months (prose) vs the table's **11 months**
  "begins to walk **without** assistance" and 12 months "walks." The textbook is internally
  inconsistent here. **A mark-18 card asserting a walking age would contradict my note 2**
  — if unit C drafted one, drop it in favor of the table rows, or reconcile explicitly.

**B. Mark 28 (a different unit) is the same fact as my note 3 c3** — "Separation anxiety
peaks between 10 and 18 months of age." Carded ONCE here, as instructed. Drop the mark-28
card, but keep mark 28 *covered*: add `28` to note 3's `from_idx` so the mark is not
recorded as silently dropped.

**C. Numeric flags.** Notes 1–4 all carry ages → `numeric: true`, `needs_human_check: true`.
Every age was read out of mark 20's / 21's / 22's own `context`, not from memory. Note 5 has
no number in its Text (the `::2 properties` hint is a count slot-label, stripped by
`readable()`), so it is correctly unflagged.

**D. Mark 20 is flagged `needs_visual` but needs no image.** Unlike TABLE 7-1, TABLE 7-2's
body came through in the text layer and lives inside mark 20's own `context`, so the R13
hard-block does not fire — every clozed answer is 100% text-supported. `visual_source` is
therefore left `null`. If the figure pipeline does extract a TABLE 7-2 plate, it would be a
congruent **back-side** image for both table cards (never the front — the plate is a complete
answer key). Not requested; noted only because Parker prefers to overshoot on pictures.

**E. Nothing in this unit needs FIGURE 7-2** (fontanelles) — that request belongs to unit C.
FIGURE 7-3 sits at the end of mark 22's context but is only a photo reference for the
trust/mistrust passage; no card here depends on seeing it.
