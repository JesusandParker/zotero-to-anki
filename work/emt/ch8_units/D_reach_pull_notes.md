# D_reach_pull — fact pass and drafting notes

Unit: marks 4–5 (p763 never move yourself and the patient simultaneously; p765 kneel on the bed when dragging across it).
Cards drafted: 2 notes, 2 cards.

## Fact pass — mark 4 (_idx 4, p763)

- P1 (highlight): do not move yourself and the patient simultaneously — move one at a time, alternating. **MUST-TEST** → D1 c1 (forced-choice polarity blank).
- P2 (highlight): why (a) — prevents undesirable jostling of the patient. **SUPPORTING** → D1 Back Extra (Why line). See flag 1 for why the whys are not clozed.
- P3 (highlight): why (b) — prevents the chance of sudden force across your spine. **SUPPORTING** → D1 Back Extra (Why line), same reasoning.
- P4 (context, unmarked): the drag cycle — pull by slowly flexing your arms; stop when your hands reach the front of your torso; move back another 15 to 20 inches (38 to 50 cm); reposition so your arms are again extended, hands about 15 inches (38 cm) in front of the torso; repeat, alternating pull and reposition. **SUPPORTING** → D1 Back Extra (Ex line, which carries the 15-to-20-inch figure). Digits verified verbatim against mark 4's context, p763: "stop and move back another 15 to 20 inches (38 to 50 cm)" — `numeric: true`, `verified_against: "p763"`, `verified_by: "agent"`. The standalone ~15 in (38 cm) arms-extended figure was left off the card to keep the Ex lean.
- P5 (context, unmarked): avoid situations that involve strenuous effort lasting more than 1 minute. **SKIP** from cards entirely — a separate self-contained rule, not congruent support for the simultaneity card. FLAG: unmarked-but-tempting (see flags).

## Fact pass — mark 5 (_idx 5, p765)

- P6 (highlight): if you must drag a patient across a bed, kneel on the bed. **MUST-TEST** → D2 c1 (decision-point, §12a: situation in the stem, one blank on the action, slot-label hint "your position").
- P7 (highlight): purpose — to avoid reaching beyond the recommended distance. **SUPPORTING** → D2 Back Extra (Why line). Left OFF the front deliberately: with "avoid over-reaching" visible, a non-knower derives "get onto the bed" by plain reasoning (rule 3 decode); the hint "your position" plus the bed situation keeps the blank one-answer without it.
- P8 (context, FIGURE 8-6 caption A, unmarked): kneel to pull a patient who is on the ground. **SUPPORTING** → D2 Back Extra (Cue line: kneeling as the safe-pull posture in both places).
- P9 (context, caption B, unmarked): when pulling, your elbows should extend only just beyond the anterior torso. **SUPPORTING** → D2 Back Extra (Why line) — closes the "recommended distance" prerequisite (rule 11) with the source's own phrasing. FLAG: the reach limit itself is cardable material but unmarked.
- P10 (context, caption C, unmarked): bend your knees to pull a patient at a different height; position feet or knees to balance the force of pull. **SKIP** → flagged as unmarked-but-tempting.
- P11 (context, truncated): "...until the patient is within 15 to 20 inches (38 to..." **SKIP** — fragment; same cycle values as P4.

## Archetypes

- **D1** — rule/polarity card (§8/§10 flavor): "move yourself and the patient {{one at a time, never simultaneously}}" with the mandatory forced-choice hint (a binary blank is unanswerable unhinted). The whys and the drag-cycle Ex live on the back.
- **D2** — decision-point vignette (§12a): discriminating situation (drag across a bed) in the stem, one blank on the action, purpose on the back.

## Design decisions and flags for hand-off

1. **The whys (P2–P3) are Back-Extra-only by design, and this was tested, not defaulted.** Every layout that leaves any why-scaffold visible ("moving both at once causes...") lets a non-knower decode the polarity answer, so whys-visible/rule-clozed leaks; rule-and-whys under one c1 leaks the same way (the scaffold "moving both at once causes ___" still implies the rule); c1-rule/c2-whys on ONE note leaks on the c1 card (c2 text visible). The only leak-free same-note shape is §11 lean-front with the whys as the Why line. A separate sibling note (rule visible, whys clozed) would be legal two-way-across-notes if the editor judges the whys must be produced, not just read — my judgment is the rule is the field-decision worth retrieving and the whys are its retention glue.
2. **Unmarked-but-tempting, not drafted (R40):** the 15-to-20-inch (38-to-50-cm) repositioning cycle and the ~15 in (38 cm) arms-extended distance (P4, used only as Back Extra support); the over-1-minute strenuous-effort rule (P5 — a standalone rule with no card); the elbows-just-beyond-the-torso reach limit (P9, used only as prerequisite closure); the bend-knees / balance-the-pull-force guidance (P10).
3. **D1 carries `numeric: true` for Back-Extra digits only** — the Text has no numbers. Flagged so the verify report reads it correctly.
4. D2's "recommended distance" is never quantified by the source in mark 5's own text; the closure uses caption B's elbow phrasing rather than importing mark 4's 15-inch figure, which belongs to a different mark's context.
