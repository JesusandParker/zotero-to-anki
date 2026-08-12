# Unit G — moving a patient on stairs (marks 10–11)

2 notes → **4 Anki cards**. Gate not run by this drafter (per SHARED_BRIEF the orchestrator
runs `check_cards.py` after the editor pass); all cloze answers were hand-checked word-by-word
against the cited marks' highlight/context text.

## Fact pass

| mark | proposition | verdict | where it landed |
|---|---|---|---|
| 10 | (highlight lead fragment) "…patient on the backboard down the stairs to the prepared stretcher" — the stair carry uses the backboard; the wheeled stretcher waits, prepared, at the bottom | SUPPORTING | note 1 `Cue:` (fragment is the tail of the preceding procedural sentence; carding it alone would be step narration, rule 26) |
| 10 | when moving on stairs, MORE THAN HALF of the patient's weight is distributed to the HEAD end of the device | **MUST-TEST** (quantity + end) | note 1, c1 (quantity) + c2 (end) |
| 10 | therefore the STRONGEST provider is positioned at the head end | **MUST-TEST** | note 1, c2 (grouped with "head" — one causal micro-chain, one retrieval) |
| 10 context | unresponsive / must-be-supine / must-be-immobilized patients are secured onto a soft stretcher, backboard, or vacuum mattress; anatomically secured so they cannot slide | SKIP — unmarked | flagged below (tempting) |
| 10 context | even with FOUR OR MORE providers, head-end strain still increases on a NARROW flight of stairs | SUPPORTING | note 1 `Pitfall:` |
| 10/11 context | carrying up or down stairs, proportionally greater weight is ALSO distributed to the foot-end provider when the device angles because of the incline/decline | SUPPORTING | note 2 `Why:` (it is the book's stated reason for the two-strongest rule) |
| 11 context | "make sure the two strongest providers are positioned at the head and foot ends of the device" | **MUST-TEST** (named in my assignment as unit content; verbatim in mark 11's context, presupposed by the highlight's "one of the two strongest providers") | note 2, c1 |
| 11 | because of the stairway's incline, if one of the two strongest is CONSIDERABLY TALLER, it is easier with the SHORTER provider at the head | **MUST-TEST** (the trap — inverts unit B's tallest-at-head) | note 2, c2 (forced binary `::taller or shorter`) |
| 11 | stated reason = the incline of the stairway | SUPPORTING | note 2 stem (visible, "Because of the stairway's incline") |

No mark dropped; the mark-10 lead fragment is covered in note 1's Back Extra rather than
as a step-recitation card.

## Archetypes

- **Note 1 (mark 10):** causal-link fact card (§7 single link, §5 quantity direction).
  c1 = the quantity ("more than half", hint `::how much`, numeric-verified), c2 = the
  head-end + strongest-provider pair under ONE number — a single causal micro-chain
  (weight loads the head → strongest mans it), not two independent facts. "head" carries
  the forced-choice `::head or foot` hint.
- **Note 2 (mark 11):** procedures-as-decisions residue (§12d, position assignment) +
  §8 forced-binary contrast. c1 = "strongest" (the pair rule), c2 = "shorter" (binary
  `::taller or shorter`). Deliberate decision: "head" is NOT re-clozed in note 2 — note 1
  owns head-end recall; re-drilling it here would double-card the answer and add
  cross-leak between siblings.

## Interference engineering (the batch's biggest risk, per the drafting brief)

Three different "who takes the head end?" answers coexist in one shuffled deck:

| situation | answer | where |
|---|---|---|
| ordinary FLAT stretcher lift | TALLEST EMTs (stretcher's head end designed slightly higher) | unit B, mark _idx 2, p754 |
| on STAIRS | STRONGEST provider (>half the weight is at the head end) | this unit, note 1 |
| on stairs, between the TWO STRONGEST with a big height gap | the SHORTER of the two (the incline) | this unit, note 2 |

- Every G stem opens with the stairs situation, **bolded** (`<b>on stairs</b>`, `<b>up or
  down a flight of stairs</b>`) — situational anchors, per the brief, with neither fact
  weakened.
- Both notes carry a `Distinguish:` line naming the flat-lift/tallest contrast so the
  families bind instead of colliding.
- **Grounding flag for the editor:** the Distinguish lines assert the unit-B fact
  ("tallest at head on a flat lift; the stretcher's head end sits slightly higher by
  design"). That fact is NOT in marks 10–11's context and not in the VERIFIED BLOCK — it
  was supplied by the orchestrator's brief, and I verified it verbatim against
  `B_lifting_rules.json` mark `_idx 2` (p754) before asserting it. `from_idx` on the G
  cards cites only this unit's marks ([10] / [11]), which ground every CLOZE answer; the
  cross-unit claim lives only in Back Extra. If the judge wants it mechanically
  auditable, extend note 1/note 2 `from_idx` with `2` or record the clearance per
  `note-format.md`.
- Notes 1 and 2 compose without contradiction: strongest at the head (note 1); the pair
  of strongest at head AND foot, shorter of them at the head (note 2). Note 2's stem
  reveals that the strongest pair covers both ends, which does not answer note 1 (which
  end is heavy, who specifically mans it) — residual coupling accepted as family
  coherence.

## Flags for hand-off

1. **Unmarked-but-tempting (context of mark 10):** the device indication ("when a patient
   is unresponsive, must be moved in a supine position, or must be immobilized, secure the
   patient onto a soft stretcher, backboard, or vacuum mattress") and the anatomic-securing
   requirement ("so that he or she cannot slide significantly"). Both card-worthy, both
   unmarked — want anything from them?
2. **Numeric verification:** "more than half" (note 1) and "the two strongest" (note 2)
   checked verbatim against mark 10's highlight and mark 11's context respectively, both
   p784 → `verified_against: "p784"`, `verified_by: "agent"`, `numeric: true` on both
   notes. `needs_human_check` left `false` for the report to derive.
3. No figure request: marks 10–11 are pure text (`needs_visual: false`), and no Skill
   Drill plate belongs to this unit.
