# Unit I — editor pass (adversarial, independent)

2 notes → 2 Anki cards. Fact pass re-run from `I_commands.json`; full checklist run,
checks 18–24 per row. The drafter's documented rejections for note 2 were re-derived
from scratch rather than trusted.

## Verdict table

| card | verdict | what was found |
|---|---|---|
| Note 1 (mark 13, two-part command structure) | **PASS** — no edits | Grouped 2-item reveal, printed ordinals, `<br><br>` rows, count visible in stem and matching. No row self-answers. |
| Note 2 (mark 14, countdown clarification) | **PASS** — no edits | Whole-horns cloze re-derived as the correct shape; every alternative is worse (below). |

No drops.

## Note 1 — the task-specified hunts

- **Printed ordinals are legitimate** (rule 26: position is scaffolding, never an
  answer; rule 23: 2 uncued ≤ 4). The rows are all-cloze after the ordinal — the good
  shape, not rule 22's filler-cloze shape.
- **Rule 20 per row: does the stem hand over "preparatory"?** No. The stem's verb
  "initiate" describes the ORDER's function (it starts the move), not either part's
  name; nothing visible paraphrases "preparatory" or "execution." The bare ordinals say
  nothing content-wise, and the set is closed by the lead-in ("given in <b>two
  parts</b>"), so the rows are neither self-answering nor open-set. A knower produces
  the book's two terms; a non-knower can gesture at "a warning and a go" but cannot
  produce the terminology — knower-can / non-knower-can't holds.
- Count integrity (check 17): "two parts" stated, two rows clozed. Count visible per
  recipes §6; a separate numeric card on "two" would be padding (producing both rows
  co-tests it). "two parts" is visible, not clozed, so rule 27 does not fire.
- Back Extra grounded verbatim in mark 13's context (the STOP example's three
  preparatory functions + louder-voice line). Both lines teach edges the Text lacks.

## Note 2 — the whole-horns cloze, re-derived

Front on the only card: `To avoid confusion with a lift countdown, the leader should
<b>always</b> clarify in advance whether "three" is [...] or [...].`

- **Crispness (rule 5/6):** each horn is 4–5 words ("part of the preparatory command" /
  "itself the order to execute") — under the ≥9-word alarm, and both are built from the
  book's own two-part vocabulary, so a knower reproduces their substance cleanly. This
  is not the long-fuzzy-phrase shape; no restructure needed.
- **Re-derived the alternatives, independently reaching the drafter's conclusions:**
  - cloze "clarify" alone → filler-verb blank (rule 22 shape), and open-set even with
    the anchor;
  - cloze "three" → decodable cold (the ambiguous word in a countdown is obviously the
    final count) — a non-knower wins, check 15 fails;
  - classify the two example commands (the task's suggested forced-choice restructure)
    → self-answering by parsing: "We're going to lift on three" *states* that "three"
    executes, and "…One, two, three, LIFT!" states the opposite. It drills reading, not
    recall — the drafter's rejection is correct;
  - two-way (horn A = c1, horn B = c2) → each card shows one pole, and the other is
    complement-decodable ("not the go" = part of the wind-up). Grouping both under c1
    is what forces producing the dichotomy.
  The grouped whole-horns cloze is the best available shape. Load 2, husk check passes
  (covering c1 leaves countdown + "three" + the always-clarify duty — a real anchor).
- **Rule 21 (absolute anchored):** the "always" sentence carries no lone unhinted
  terminal blank — the visible `whether … or …` frame plus the quoted "three" close the
  answer space. Concur with the drafter.
- **Sibling coupling with note 1, adjudicated fine:** note 2's answers reuse note 1's
  taxonomy, but neither FRONT reveals the other's answers (both hide them), and the
  facts differ — structure (n1) vs the countdown's ambiguity between the parts (n2).
  That is prerequisite composition (rule 11 satisfied by the sibling), not a check-16
  scenario leak.
- **The interpretive `Why:` clause kept** ("…an unclarified countdown splits the team's
  timing"). The execution moments are read directly off mark 14's two example commands;
  "splits the team's timing" is the one interpretive step, and it is entailed — a team
  holding two conventions executes at two moments, which is exactly the "confusion" the
  book names. No clinical fact or number is invented (Layer A #7 respected). Logged
  here so the judge sees the call; trim only if Parker wants strict literalism.

## Field verification (both notes)

- `numeric: true` on both — n1 "two parts" verbatim p796; n2 the quoted "three"
  verbatim p796. `verified_against: "p796"` / `verified_by: "agent"` correct on both
  (re-checked word-by-word this pass). n2's numeric flag is conservative (a quoted
  count word, not a threshold) — kept, since it only routes a cheap human glance.
- `needs_human_check: false` left for `verify_report.py` to derive. `visual_source`
  null, `block` correct, allowed HTML only, no image keys.
- **Neither card asserts the unmarked context facts** (staged-briefing overview,
  Words-of-Wisdom alteration-vocalization, multi-stage explanation) — checked Text and
  Back Extra on both. They remain hand-off flags only.

## Hand-off flags

- Drafter's flags stand: (a) staged-briefing pattern and (b) vocalize-any-alteration
  rule — both card-worthy, both unmarked; one sentence to Parker.
- No interference with other ch8 units found (no other unit tests commands); the
  louder-voice detail lives on note 1 only.
