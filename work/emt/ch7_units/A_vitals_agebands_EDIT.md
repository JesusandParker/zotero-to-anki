# Unit A — editor verdicts (adversarial pass)

Drafted 8 notes → **5 REWRITE · 2 PASS · 1 DROP → 7 ship.**
`check_cards.py` against `chapter_7_highlights.json`: **0 hard errors**, 2 warnings, both
cleared below. Re-stamped `A_vitals_agebands_cards.json.verified`.

## Digit re-verification (done first, independently)

Every number on every card was re-read off the extracted plate
`work/emt/figures/TABLE_7_1.png` — not off the brief. **The SHARED_BRIEF transcription is
correct in all 36 cells**; no discrepancy between the brief and the plate. The p683 prose
was also re-read off `work/emt/page_683.png`.

All four column collapses were checked cell-by-cell and all four are **valid**:

| Card | Collapsed row | Rows it merges | Verdict |
|---|---|---|---|
| #0 pulse | "Adolescent through older adult — 60 to 100" | adolescent / early / middle / older all 60–100 | valid |
| #1 resp | "Adolescent through older adult — 12 to 20" | adolescent / early / middle / older all 12–20 | valid |
| #2 SBP | "Toddler and preschool age — 80 to 100" | both 80–100 | valid |
| #2 SBP | "Early, middle, and older adult — 90 to 130" | all three 90–130 | valid |
| #3 temp | "Infant and toddler — 96.8 to 99.6" | both identical | valid |
| #3 temp | "Preschool age through older adult — 98.6" | six rows all 98.6 | valid |

The trap the brief warned about — the systolic column NOT collapsing the way pulse and
respirations do — **the drafter got right**: adolescent is its own row at 90 to 110, and
the 90 to 130 collapse starts at early adult. Left intact, and reinforced (see #2).

---

## Per-card verdicts

Indices are the DRAFT numbering; the shipped file is 0–6 after the drop.

### #0 — pulse ladder → **REWRITE** (check 3 grounded / safety overlay, Back Extra)
Text and all six ranges verified correct; cold-solve passes per row (band name cues, the
range is the answer, no label restates its answer). **The `Cue:` line was false**: "pulse
steps down by roughly 10 to 20 beats/min from one age group to the next" — the neonate→
infant floor does not step down at all (100 → 100). Replaced with a pattern that is exactly
true and more useful: the *lower* bound walks 100, 100, 90, 80, 70, 60. Also absorbed the
one non-duplicated teaching line from the dropped #4 (an older adult's range is identical to
a 20-year-old's — no geriatric allowance) by merging it into the existing Pitfall.

### #1 — respiratory ladder → **REWRITE** (check 11 Back Extra earns its place)
Digits and collapse correct; rows cold-solve individually. `Cue:` claimed the range "both
falls and tightens" — not true across the last step (school age 15–20 is 5 wide, adult
12–20 is 8 wide). Replaced with an exactly-true and sharper fact: a neonate's *slowest*
normal (30) is faster than an adult's *fastest* normal (20) — the bands never overlap.
Pitfall kept (40 breaths/min normal in an infant, double the adult ceiling of 20 — verified).

### #2 — systolic ladder → **REWRITE** (check 11 + absorbing the dropped card's content)
Digits, the six rows and both collapses verified. The `Distinguish:` line was a verbatim
answer key for sibling card #6 ("pulse and respirations drop, blood pressure rises"), so it
was re-aimed at something only this card can teach (systolic is the only one of the four
that climbs; neonate floor 50 vs adult floor 90). The `Pitfall:` now carries the dropped
#4's unique fact — an adolescent reaches adult pulse and respiratory values but not adult
pressure; the systolic ceiling holds at 110 until 19, then rises to 130.

### #3 — temperature ladder → **REWRITE** (check 3 grounded — a FACTUAL ERROR)
**The Back Extra asserted something the table contradicts:** *"the neonate is the only group
whose normal reaches above 98.6°F."* False — the infant and toddler band runs to **99.6°F**,
which is above 98.6°F. The neonate is the only group that reaches **100°F**. Corrected to two
claims that are each exactly and uniquely true: the neonate is the only group reaching 100°F
(38°C), and the infant/toddler are the only ones dipping below 98°F (96.8). Text digits were
correct and are unchanged.

### #4 — "normal adult vital signs" → **DROP** (R2 / card-rules #12, dedupe by meaning)
All three of its answers are already the last row of a sibling in this same unit — pulse
60 to 100 = #0 row 6, respirations 12 to 20 = #1 row 6, systolic 90 to 130 = #2 row 6. Same
cue, same target, three duplicate answers in one batch: the exact "carded verbatim twice"
shape R2 exists for, and it creates interference rather than coverage. Nothing is lost —
the four adult values remain tested by #0/#1/#2/#3, and both of its Back Extra lines were
migrated rather than discarded (adolescent-BP exception → #2 Pitfall; no-geriatric-allowance
→ #0 Pitfall). The drafter's own notes name this as the cut to make if it is judged a
duplicate, and specify exactly this migration.

### #5 — the nine age bands → **REWRITE** (check 3 grounded, Back Extra overgeneralized)
All nine ranges verified against the plate; "birth to 1 month" is grounded in mark 1's own
sentence. Nine rows, each cold-solved individually — every label is a band name and every
answer is its numeric span, so no row answers itself. The `Pitfall:` claimed *"consecutive
groups share a boundary year"* — true of the childhood bands (1, 3, 6, 12) but **false of the
adult bands** (adolescence ends at 18 and early adulthood starts at 19; 40/41; 60/61).
Corrected to state both halves, which is the more useful fact. `Distinguish:` → `Why:`,
reordered to lead with the edge (nothing changes as fast as the first year) rather than
restating rows 1–2.

### #6 — direction of change with age → **REWRITE** (check 11, duplicate Back Extra)
Text passes and is unchanged. It is **not** an R10 husk: both blanks are c1, but the three
entity anchors (pulse rate, respiratory rate, systolic blood pressure) stay visible, both
blanks carry a forced-choice `::increase or decrease` hint (check 13), and "whereas" is a
visible contrast anchor — a knower produces it cold. Grounded verbatim in mark 0's context
("unlike pulse and respiratory rates, blood pressure values tend to increase with age").
The `Pitfall:` was a near-verbatim duplicate of #2's, and the `Cue:` merely restated this
card's own answer. Both replaced with material nothing else in the unit carries (the climb
has a ceiling — systolic is identical in early, middle and older adults, so a high reading
in a 70-year-old is a finding, not an age effect).

### #7 — 140 beats/min: infant vs 30-year-old → **REWRITE** (check 3 grounded; internal source contradiction)
**This is the substantive catch of the unit.** The p683 prose says a pulse of 140 *and
respirations of 60* are "usually normal for an infant." TABLE 7-1 caps infant respirations at
**25 to 50**; 60 breaths/min falls only in the **neonate** band (30 to 60). The textbook
contradicts itself, and sibling card #1 in this very batch teaches infant respirations = 25
to 50 — so keeping the prose as drafted would have put two cards in one shuffled deck
teaching opposite things about the same fact.

Of the three options, I took **reword so the card does not hinge on the disputed digit**:
the respiratory figure is removed and the card keeps only the pulse of 140. Reasoning:

- **It stays grounded twice over, and invents nothing.** The prose's own sentence supplies
  140 beats/min, "infant," "30-year-old adult" and "life-threatening"; TABLE 7-1
  independently confirms 140 is inside the infant band (100 to 160) and far outside the
  adult band (60 to 100). No claim on the card is disputed by either source.
- **Re-anchoring to the neonate was rejected**: 140/60 does sit inside both neonate bands, so
  it would be table-true, but the prose says "infant," and swapping the age group would be
  the editor asserting a pairing no source states.
- **Keeping the prose as-is was rejected**: it is grounded, but it would teach Parker that 60
  breaths/min is a normal infant rate — wrong on the NREMT, wrong against this chapter's own
  table, and in direct conflict with card #1.
- **Nothing testable is lost.** The fact under test is that identical numbers mean opposite
  things at different ages; the pulse carries that entirely.

Also updated `verified_against` / `verified_by` to record the removal and the contradiction,
and gave the card the canonical `visual_source` dict (it is built on mark 0, which is
`needs_visual`, and its Back Extra now quotes plate-derived ranges).

---

## The two checker warnings — both CLEARED, do not "fix" them

- **`#4 (was #5): row label 'Older adult' shares ['older'] with its own answer '61 years and
  older'` (R15).** Cleared. The tested content is the number **61**, and "Older adult" cues
  nothing numeric. This is the documented MUST-NOT-OVER-FLAG side of a detector that is
  deliberately generous; distorting the book's own wording to silence it would make the card
  worse. Agreeing with the drafter here.
- **`#0 & #1: 86% similar Text — possible duplicate`.** Cleared. Pulse and respirations are
  two different columns of the same table with an intentionally identical row skeleton.
  R12 meaning-dedupe must not merge them.

---

## What the consolidation stage must know

1. **The infant-respirations contradiction is a real source defect, not a card defect.**
   p683 prose: 60 breaths/min "usually normal for an infant." TABLE 7-1: infant 25 to 50, and
   60 is the neonate ceiling. **The grid governs.** If any other unit or a recap card asserts
   60 breaths/min as a normal *infant* rate, it is wrong — kill it. Worth surfacing to Parker
   at hand-off, because he may hit the same sentence while reading.

2. **The adult-collapse framing in the drafting brief is wrong for blood pressure** (the
   drafter caught this and I confirmed it against the plate). Pulse and respirations reach
   adult values at adolescence; **systolic does not until 19** (adolescent 90 to 110, early
   adult 90 to 130). Any sibling card saying "90 to 130 from adolescence on" is wrong.

3. **Card #4 was dropped as a duplicate, and its content was migrated, not discarded.** If
   consolidation wants a single cross-column "normal adult vitals" card restored, it must be
   added once globally and the three ladder cards' final rows re-scoped, or the duplication
   comes straight back.

4. **`visual_source` is the canonical DICT on all 7 cards** (including #7, which was `null`
   in the draft). Verified programmatically before write. Sibling units that followed the
   brief literally will have **bare strings** — `attach_figures.py:307` does
   `vs.get("figures")` on a truthy value, so a bare string is an `AttributeError` that crashes
   the figure stage for the whole segment. Normalize them before that stage runs.

5. **TABLE_7_1 belongs on the BACK of every card in this unit** (`image_side` default). It is
   a complete answer key for six of the seven; front placement would destroy them all at once.
   It is congruent for #7 as well (that card's answers are the words normal / life-threatening,
   not a number the plate shows).

6. **`numeric: false` on card #6 was preserved as instructed**, but its Back Extra now quotes
   ranges (90 to 130, 70, 90, 20). Its Text carries no digits, so no detector fires either
   way and `needs_human_check` is already `true`. Flagging in case `verify_report.py` should
   see it as numeric.

7. **Detector gap confirmed (the drafter's finding is real).** `check_cards.VALUE` matches
   neither `140 beats/min` nor `60 breaths/min` nor `30-year-old` — `/min` is a listed unit
   but the regex needs the digits adjacent to it, and `30-year-old` has no second digit for
   the range branch. `N beats/min` is the most common numeric notation in this textbook, so
   such cards silently escape the numeric gate. One-line fix to `VALUE` in
   `scripts/check_cards.py`; worth doing before Chapter 8.

8. **Both marks are covered; nothing was silently dropped.** Mark 0 → cards 0,1,2,3,4,5,6
   (new numbering); mark 1 → card 4 (the age-band ladder), merged per Rule 0.
