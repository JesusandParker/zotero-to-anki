# Unit O — Logroll onto a blanket, Skill Drill 8-12 (mark 22, p836)

2 notes, 3 Anki cards. File: `work/emt/ch8_units/O_logroll_blanket_cards.json`

Mark 22 is the drill caption; its context also carries the lead-in sentence that
grounds the drill's PURPOSE (logroll onto a blanket → lift by the blanket → carry to
the nearby stretcher), which the stems use as framing. This drill has captions only —
no separate numbered list in the context. Per card-rules #26 / recipes §12: the two
discriminating setup values + the lifting end-state; no step recitation.

---

## Fact pass

| Proposition (mark 22 context) | Call | Where it went |
|---|---|---|
| Purpose: logroll onto a blanket, lift by the blanket, carry to the nearby stretcher | MUST-TEST (as framing) | visible framing of cards #0 and #1 — grounded, per the drafting brief |
| Prepare the blanket by rolling it up BY HALF | MUST-TEST | card #0, c1 (numeric "half", verified) |
| Logroll the patient (motion) | SKIP as motion | visible scaffolding in #0 + Back Extra `Cue:` |
| Position the rolled-up half underneath the patient | SUPPORTING | card #0, visible stem ("position the rolled portion under the logrolled patient") |
| Roll the patient back onto the blanket, then in the OPPOSITE direction to unroll it | MUST-TEST | card #0, c2 (forced-choice same/opposite) |
| Roll the patient back onto his or her back | SUPPORTING | card #0 Back Extra (`Cue:` — "finishing with the patient supine") |
| Center the patient on the blanket; roll up the excess material on each side | SUPPORTING | card #1 stem ("lies centered") + Back Extra (`Cue:`) |
| Roll up the ENDS of the blanket for lifting | MUST-TEST | card #1, c1 |
| Lift the blanket / lift the patient by the blanket, carry to the nearby stretcher | MUST-TEST (as framing) | card #1 visible stem |
| Chair → stair chair sentence at the tail | UNMARKED / SKIP | unrelated cross-reference, not this drill |

---

## Cards + archetypes

- **#0 (`c1` by half, `c2` opposite direction)** — §12d setup values. c1 is the
  discriminating prep quantity (numeric, hint `::how much` per card-rules #27);
  c2 is the counterintuitive two-roll move (the step people get wrong), carried as a
  direction blank with the mandatory forced-choice hint. "The rolled portion" is used
  everywhere the source says "the blanket that has been rolled up half way" — writing
  "the rolled HALF" would leak c1's answer.
- **#1 (`c1` roll up the ends)** — §12d end-state / §12a-flavored transition ("patient
  lies centered — before you lift, what?"). The purpose (carry to the nearby
  stretcher) stays visible as grounded framing.

---

## THE NEXT STAGE MUST KNOW

1. **Numeric verification:** card #0's "by half" is verbatim in mark 22's context
   ("Prepare the blanket by rolling it up by half", p836) — `numeric: true`,
   `verified_against: "p836"`, `verified_by: "agent"`. `verify_report.py` should
   derive `needs_human_check: false`.
2. **"Ends" vs "each side" ambiguity, flagged rather than resolved:** the drill's
   Step 4 says "roll up the ends of the blanket for lifting"; the lead-in says
   "rolling up the excess material on each side." These are probably the same act
   loosely worded (roll the slack into grips), but the source never says whether
   "ends" means head/foot or the side edges. Card #1 clozes the drill's own wording
   ("roll up the ends of the blanket") and the Back Extra carries the each-side
   variant as a `Cue:`. If Parker asks which it is, the honest answer is the book is
   loose here.
3. **Cross-unit Back Extra link:** card #1's `Distinguish:` (scoop = rigid, assembled
   around the patient, locked and strapped vs blanket = no frame, rolled ends as
   handholds) grounds in marks 22 + 21 — `from_idx [22, 21]`.
4. **The chair/stair-chair tail sentence** in the context belongs to earlier-chapter
   material (stair chair), not this drill — skipped, not dropped.
5. **Figure stage:** attach the Skill Drill 8-12 composite (4 panels per the fig
   index) to both card backs.
