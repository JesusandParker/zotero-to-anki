# Unit H — editor pass (adversarial, independent)

1 note → 2 Anki cards. Fact pass re-run from `H_stretcher_steps.json`; full checklist
run, checks 18–24 per row.

## Verdict table

| card | verdict | what was found |
|---|---|---|
| Note 1 (mark 12, undercarriage rule + carve-out) | **PASS** — no edits | Both MUST-TEST facts clozed (c1 the preparation, c2 the 3-item exception set); nothing beyond mark context asserted; all fields verified. |

No drops.

## The task-specified hunts, run

- **Carve-out count: exactly THREE c2 spans** ("a curb" / "a single step" / "an obstacle
  of similar height") — matches the book's closed set (mark 12 highlight; the FIGURE 8-13
  caption repeat is the same set, correctly deduped by the drafter). Stated-count
  integrity: no count is stated, three blanks are shown — consistent.
- **Inline layout renders the owed count visible.** The three spans sit inline in the
  sentence, so the c2 card's front reads "…over [...], [...], or [...]" — three discrete
  brackets with the "or" before the last. Rule 19 / check 21 does NOT demand `<br><br>`
  here: these are not rows under a lead-in, they are a flowing negation sentence, and
  the recipe's alternative (one span + `::3` count hint) is strictly worse — the three
  separate spans self-display the count AND keep each answer atomic. Leave inline.
- **"The same preparation…" opener cannot leak c1.** On the c1 card the exception
  sentence is fully visible but names the preparation only as "the same preparation" —
  the undercarriage is never mentioned outside the cloze. Verified word-by-word. It also
  reads cold ("the same preparation" = whatever fills the blank in the same Text), and
  it does not open with a banned pronoun.
- **`::stretcher adjustment` is a slot-label, not a leak.** It names the category
  (equipment adjustment), not the content; it cannot replace the answer. It earns its
  place twice over: kills the open-action-blank shape (rule 16 — "before steps,
  first ___" admits many EMT actions) and steers away from unit-G interference
  ("position the strongest at the head end" is a plausible wrong fill in an unhinted
  steps stem).

## Other checks worth recording

- **Cold-solve, both directions:** c1 — knower produces retract/raise-the-undercarriage
  from stem + hint; non-knower can't decode it (nothing visible defines it). c2 — the
  exemption is a closed taxonomy the source names; visible "short flight of steps"
  frames the boundary dimension without handing over the three members. PASS.
- **Husk check:** covering c1 leaves the full situation + the entire exception sentence;
  covering c2 leaves the full rule sentence. Neither blank depends on the other. Load:
  c2 group = 3 uncued ≤ 4.
- **Negation form per recipes §10:** negator loud and visible (`is <b>not</b>
  necessary`), the carve-out clozed, contrast fully visible. `<b>` correctly used
  (no `<u>`).
- **Grounding:** every clozed word verbatim in mark 12's highlight ("of similar height"
  vs the book's "of a similar height" — trivial smoothing, meaning identical). No `Why:`
  invented for a mechanism the book never states — correct restraint.
- **Cross-unit citation `from_idx: [10, 12]` verified and kept:** mark 12 grounds every
  cloze; mark 10 grounds the `Distinguish:` line's backboard-stairway half ("secure the
  patient onto a … backboard … Carry the patient on the backboard down the stairs to the
  prepared stretcher"). Same multi-mark pattern applied to unit G this pass. The
  `Distinguish:` naming "the retract-the-undercarriage rule" restates the c1 answer only
  in Back Extra (post-answer), in service of the G-vs-H family contrast — legitimate.
- **Numeric fields:** "a single step" + the 3-member set verified verbatim p789 →
  `numeric: true`, `verified_against: "p789"`, `verified_by: "agent"` correct;
  `needs_human_check` left false for the report to derive.
- **The unmarked safety-hook fact is asserted NOWHERE on the card** (checked Text and
  Back Extra) — it stays a hand-off flag only.

## Hand-off flags

- Drafter's flag stands: the ambulance-loading detail (advance until the **safety hook**
  catches) is unmarked and its context sentence is truncated — one sentence to Parker if
  he wants it.
