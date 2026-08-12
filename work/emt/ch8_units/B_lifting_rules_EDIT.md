# B_lifting_rules — adversarial edit

Editor: independent pass, all checks 1–30 run per card, 18–24 per row. Fact pass re-run
from `B_lifting_rules.json` before editing. Drops: none.

## Verdict table

| Card | Verdict | What changed |
|---|---|---|
| B1 (first key rule) | REWRITE (Back Extra only) | Why line restored to the source's full claim: "muscles **and ligaments** of the lumbar and sacral regions" (draft said "lumbar and sacral muscles" — a silent narrowing of the source). Text untouched. |
| B2 (head higher / tallest at head) | REWRITE (Back Extra + provenance) | Added the reciprocal `Distinguish:` line against the stairs strongest-at-head family; `from_idx` extended to `[2, 10]` so the stairs claim is grounded against the mark that supports it. Text untouched. |

Fact-pass coverage re-verified: P1, P2 (mark 1) clozed on B1; P7, P8 (mark 2) clozed on
B2. Nothing on either card asserts beyond mark context except B2's Distinguish, which is
grounded in mark 10 (now cited).

## Judgement calls

1. **B1 `open_set_absolute` — drafter's benign pre-adjudication CONFIRMED, honestly.**
   Cold-solved with both blanks covered: "The first key rule of lifting is to always keep
   your back in a ___ position and to lift without ___." The anchor is a source-NAMED,
   closed rule ("the first key rule of lifting" is the book's own label), which is rule
   16's closed-taxonomy calibration: hard-but-forced, not open. Each local frame
   constrains form tightly — "back in a ___ position" wants a posture descriptor,
   "lift without ___" wants a forbidden motion. A knower of the named rule produces
   straight/upright + twisting; near-synonyms ("locked-in") are the acceptable 2–3-synonym
   case rule 16 explicitly excludes from open-set. A non-knower has no decode (nothing
   visible implies either answer). No hint added: rule 21's fix menu is for blanks that
   are genuinely unanchored, and this one is anchored by the rule's name.
2. **B1 grouping (two clauses under one c1) — one retrieval, not two glued facts.** The
   source states one rule with two aspects, both spinal-alignment protections, in one
   sentence under one name. Recalling "the first key rule of lifting" should produce the
   whole rule. Load = 2 uncued, well under the ≤4 cap. Not a husk (check 19): the visible
   remainder carries the rule's name, rank, object, and both frames — substantial
   anchoring, and the spans are anchored by the visible name, not by each other (the R10
   failure shape).
3. **B2 grouping (higher + tallest under one c1) — drafter's deliberate design UPHELD.**
   Verified the split-halves-decode claim both ways: with "tallest…to offset" revealed,
   "higher" is derivable (tall people go to the high end); with "head higher" revealed,
   "tallest" is derivable (higher end needs taller EMTs). Split c1/c2 would make two
   decode-leaking cards (rule 3). Grouped, the non-knower's derivation chain is cut (the
   direction it needs is hidden; the binary hint leaves 50/50) while a knower produces
   both. The direction blank carries its mandated forced-choice hint. Load = 2.
4. **B2 vs the stairs family (G unit) — coexistence adjudicated.** B2's own stem carries
   the flat-lift anchoring: "A stretcher is designed so…" + "to offset the difference in
   stretcher height" is the design-offset frame, visibly distinct from G's "on stairs" /
   "flight of stairs" weight-shift frame. That alone is probably enough for a knower, but
   G1's Back Extra already cross-links one-way (it names tallest-at-head), leaving B2 bare
   when B2 is drawn first in the megadeck. Added the reciprocal Distinguish per the
   confirmed confusable-cross-link preference. Phrased "the greater share of the patient's
   weight" deliberately — it does NOT hand over G1's exact `more than half` c1 answer,
   only the entailed paraphrase.
5. **Cross-unit citation `from_idx: [2, 10]`.** The Distinguish line's stairs claim is not
   in mark 2's context; the gate verifies grounding against exactly the cited marks, so
   citing mark 10 (read from `G_stairs.json`, whose context states the strongest-at-head
   rule verbatim) is the honest provenance. B2's TESTED content still comes only from
   mark 2 — mark 10 supports a Back-Extra line, which is support, not a new card (rule 29
   untouched).
6. **"Always" dropped from B2's stem** ("When lifting, position…" for "Always
   position…") — draft choice, kept: the purpose clause anchors the blank, and removing
   the absolute avoids a gratuitous rule-21 shape with no loss of meaning.

## Hand-off flags

1. **G1 grounding gap (not edited — outside my units):** G1's Back Extra Distinguish
   states the tallest-at-head/design-height facts (mark 2 content) but G1 cites
   `from_idx: [10]` only, and mark 10's context contains none of it. If the gate checks
   Back Extra claims against cited marks, G1 will fail R13; fix is citing mark 2 (or
   trimming its Distinguish). Flagging instead of editing per my scope.
2. Drafter flags carried forward unchanged: the power-lift definition (P9) and the
   arms-outstretched / torso-plane mistake (P10) in mark 2's context are unmarked,
   classic test fodder, and NOT drafted (R40). Note: P9 is now used as Back-Extra
   Distinguish support on C3 (unit C) — still no card tests it.
3. The offset MECHANISM stays unexplained on B2 by design (source never states why
   tallest-at-the-higher-end offsets the difference); the Distinguish + Cue lines assert
   pairing, not physics. Do not "improve" with invented mechanics.
