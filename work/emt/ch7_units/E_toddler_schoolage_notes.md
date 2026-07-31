# Unit E — Toddlers, Preschoolers & School-Age Children (marks 23–36)

10 notes written to `E_toddler_schoolage_cards.json`. `check_cards.py` is clean (0 hard, 0
warn) and every cloze answer is **100% grounded** in the context of the mark(s) it cites
(verified by re-running the R13 support calculation per answer, not just the ≥50% gate).

---

## Fact pass — per mark

| Mark | Verdict | Where it landed |
|---|---|---|
| 23 | MUST-TEST | card 0 — lung musculature limit |
| 24 | MUST-TEST | card 1 — passive → acquired immunity chain |
| 25 | MUST-TEST | card 2 — brain 90% of adult weight |
| 26 | MUST-TEST | card 3 — merged with 27 (toilet training) |
| 27 | MUST-TEST | card 3 — merged with 26 |
| 28 | **DUPLICATE — deliberately not carded** | covered by unit D's card on mark 21 |
| 29 | MUST-TEST | card 4 — language milestones |
| 30 | MUST-TEST | card 5 — cause and effect |
| 31 | MUST-TEST | card 6 — parent as secondary patient (application) |
| 32 | MUST-TEST | card 7 — annual growth; teeth + hemispheres → Back Extra |
| 33 | MUST-TEST | card 8 — merged with 34, 35 (moral reasoning) |
| 34 | MUST-TEST | card 8 — merged with 33, 35 |
| 35 | MUST-TEST | card 8 — merged with 33, 34 |
| 36 | MUST-TEST | card 9 — self-concept vs self-esteem |

SUPPORTING (used as grounding / Back Extra teaching, not carded on its own): the
gross-motor → fine-motor play transition (mark 25 context), the
autonomy-versus-shame-and-doubt framing (marks 26/27 context), the creative/playful shift
in language use (mark 29 context), watching other children → rules, competitiveness,
gender differences (mark 30 context), baby → permanent teeth and increased brain activity
in both hemispheres (mark 32 context).

SKIP: nothing was skipped.

---

## Merges (Rule 0)

- **26 + 27 → one card.** One passage, one teaching point: the physiologic milestone
  (neuromuscular bladder control, 12–15 months) and the psychological one (readiness,
  18–30 months; average completion 28 months) are only meaningful against each other.
  Three cloze numbers so each number is independently answerable, never a husk.
- **33 + 34 + 35 → one card, two directions.** The three levels of moral reasoning are one
  taxonomy. Built as a single note with `c1` = the three level names and `c2` = the three
  drivers, so it yields **two cards from one note**: description → level, and level →
  driver. Because they share a note, bury-siblings spaces them across days — which two
  separate notes would NOT have done, and a mirror-image pair on the same day is a
  cross-card giveaway (card-rules #13). Not fragmented into three.
- **23 is cited by two cards** (`from_idx [23]` and `[23, 24]`, plus `[23, 25]`). Mark 23's
  context paragraph is the grounding for the neighbouring facts; that is provenance, not
  duplication. Only card 0 tests mark 23's own highlighted clause.

## Mark 28 — covered, not dropped

Mark 28's highlight, *"Separation anxiety peaks between 10 and 18 months of age"* (p701), is
the **same fact, same numbers** as mark 21 (p692, *"it typically reaches its peak between
the ages of 10 and 18 months"*), which **unit D is carding**. Verified directly against
`chapter_7_highlights.json[21]`. Per card-rules #12 (dedupe by meaning), the fact is carded
once. Mark 28 adds no new qualifier — it is the toddler-chapter restatement of the infant
section's statement.

**Consolidation must log this as a merge: mark 28 → unit D's mark-21 card.** If unit D did
NOT card mark 21, this becomes an uncovered fact and unit E owes a card — please check.
Suggested action if so: add `28` to unit D's card `from_idx` rather than making a second
card.

---

## Judgment calls the next stage should know about

1. **Kohlberg is never named on the cards, on purpose.** The string "Kohlberg" appears
   **zero times** anywhere in `chapter_7_highlights.json` — the AAOS text calls these
   "types of reasoning" without attribution. Naming him would be a true-but-ungrounded
   addition (Rule 1). Card 8 says "three levels of moral reasoning" instead. If a later
   pass wants the name, it needs a source read, not an assumption.

2. **Mark 32's teeth + hemispheres facts are in the Back Extra, not clozed.** Only the
   growth-rate sentence is highlighted yellow; the other two sit in the same paragraph as
   context. "Baby teeth are replaced by permanent teeth" is near-universal knowledge and
   would be a self-answering card (Parker, 2026-07-30: *"a row that answers itself is
   padding, not coverage"*), and the hemisphere fact alone does not carry a card. Both are
   preserved verbatim in card 7's `Cue:` line. Flagging in case consolidation wants the
   hemisphere fact promoted to its own cloze.

3. **Mark 36 deliberately hides BOTH definitions or BOTH terms — never one of each.**
   The brief's no-crutch constraint drove the structure: if self-esteem's name *and*
   definition were visible while asking for self-concept, the answer falls out by
   elimination. So `c1` hides both term names (definitions visible) and `c2` hides all three
   discriminators (both names visible). Neither card can be answered by elimination.
   **Weakest cold-solve in the batch:** `c2`'s first blank, *"Self-concept is our ___ of
   ourselves"* → "perception"; *view / image / opinion* are near-synonyms a knower might
   produce instead. Mitigated by the parallel hidden "feel" (the axis is think-vs-feel) and
   by the `Distinguish:` line. Worth a judge look; I did not add a hint because any hint
   specific enough to force "perception" would leak it.

4. **Mark 31 is flagged `needs_visual: true` but needs no visual.** It is `page_sparse`
   (p702 is 331 characters — the page is mostly a figure), yet the Street Smarts box is
   captured **complete** in the mark's context. Card 6's answer ("a secondary patient")
   sits verbatim in that context, so R13's hard block does not fire and `visual_source`
   is correctly `null`. Same situation for mark 32 / card 7 (p703, 368 chars, paragraph
   complete). Neither needs a page render.

5. **Card 6 is the unit's only application card, by design.** Per `profiles/emt.md` §2 and
   the shared brief, Life Span Development is a recall-heavy chapter and vignettes must not
   be forced onto developmental definitions. Mark 31 earns one because it is about what you
   *do* on scene. The source does **not** state a management action for the panicking
   parent, so the card asks what the parent has *become* rather than inventing a "next
   step" the book never gives.

6. **No figure is wanted on any unit-E card.** FIGURE 7-5 (preschooler photo), 7-6 (toddler
   walking) and 7-7 (school-age child) are illustrative age-group photos appearing in these
   marks' contexts. Parker's standing preference is to overshoot on pictures, so if the
   figure matcher wants to attach 7-5/7-6/7-7 to cards 0–5 or 7, that is congruent and fine
   — but nothing here *requires* an image. The FIGURE 7-2 fontanelle request from the
   shared brief belongs to unit C, not this unit.

7. **Numeric flags.** Cards 2, 3, 4, 5 and 7 carry `numeric: true` + `needs_human_check:
   true` (ages, month ranges, percentage, pounds/kg, inches/cm). Every digit was
   transcribed from the mark's own `context`, not from memory: 90% · 12 to 15 / 18 to 30 /
   28 months · 36 months / 3 or 4 years · 18 to 24 months · 4 pounds (2 kg) / 2.5 inches
   (6 cm) · the age bands 3 to 6 and 6 to 12 (also confirmed against the shared brief's
   verified age-band block). Cards 0, 1, 6, 8, 9 carry no numbers and are unflagged.

8. **Possible overlap with other units to check at consolidation:** the
   "autonomy versus shame and doubt" stage is named in card 3's Back Extra only (not
   clozed) — if unit D cards Erikson's stages, make sure that is one card, not two. Card
   9's Back Extra mentions moral reasoning developing further in adolescence; unit F
   (adolescents) may own that fact.
