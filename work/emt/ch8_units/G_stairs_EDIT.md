# Unit G — editor pass (adversarial, independent)

2 notes → 4 Anki cards. Fact pass re-run from `G_stairs.json`; every check in
`editor-checklist.md` run per card, checks 18–24 per ROW. `B_lifting_rules_cards.json`
read for interference only (not edited).

## Verdict table

| card | verdict | what was found / done |
|---|---|---|
| Note 1 (mark 10, weight-to-head chain) | **REWRITE (metadata only)** | `from_idx` [10] → [10, 2]. The `Distinguish:` line asserts unit B's tallest-at-head fact (mark `_idx 2`, p754) — outside mark 10's context. Verified the claim verbatim against `B_lifting_rules.json` mark 2 ("The stretcher is designed so that the patient's head is slightly higher than the feet. Always position the tallest EMTs at the head…"); kept the line, extended the citation so the R13 gate can audit it. Text untouched — every blank passed cold-solve (below). |
| Note 2 (mark 11, two-strongest + shorter-at-head) | **REWRITE (metadata only)** | Same finding, same fix: `from_idx` [11] → [11, 2] for its `Distinguish:` line's flat-lift/tallest half. Text untouched. |

No drops. All four MUST-TEST facts land in a cloze: >half weight (n1 c1), head end +
strongest provider (n1 c2), two strongest at the ends (n2 c1), shorter at head (n2 c2).
Nothing on either card asserts the unmarked device-indication / anatomic-securing context
facts (correctly left as hand-off flags in `G_stairs_notes.md`).

## Per-row cold-solve, the calls that mattered

- **n1 c1 "more than half" with `::how much` — rule 27 satisfied.** The slot is doubly
  announced: the hint plus the partitive frame "___ of the patient's weight is
  distributed" (nothing but a quantity fits). Answer verified verbatim in the highlight.
  The visible causal tail ("so the strongest provider is positioned at that end") implies
  *more* weight but not the specific quantity — cue, not leak. PASS.
- **n1 c2 "head or foot" forced choice — a knower keeps a real edge.** The stem gives the
  weight-distribution fact as the discriminator; nothing visible states which end. Tested
  against B2 in a shuffled deck: B2's front says "position the ___ EMTs at the head end"
  in the design-offset frame — it never states where weight goes on stairs, so the
  association a non-knower could borrow is a coin-flip guess, while a knower answers from
  the fact. Anchor holds. PASS.
- **n1 c2 "strongest" (unhinted, grouped with "head")** — partially derivable from the
  visible "so" (heavy end → strong provider), but the decode path is the book's own
  causal logic, not a definitional leak; this is the endorsed reasoning-card shape
  (compare rule 21's GOOD example). Grouping head+strongest under one number is one
  causal micro-chain, not a husk: covering c2 leaves the weight fact + stairs anchor
  visible. Load 2. PASS.
- **n2 c1 "the two ___ providers take the head and foot ends"** — open-vocabulary but
  knowledge-closed ("strongest" is verbatim in mark 11's context); the revealed c2
  clause ("…considerably taller… shorter at the head") mildly disfavors "tallest,"
  which is legitimate — height demonstrably varies within the pair. PASS.
- **n2 c2 taller/shorter — adjudicated: keep the why VISIBLE, blank the binary.**
  The task question was whether "Because of the stairway's incline" forces or *decodes*
  the answer. It does neither cheaply: decoding needs the carry convention plus the
  keep-it-level geometry, and a non-knower reasoning cold lands on taller-at-head about
  as often (long arms reach down). The visible why is the situational anchor that
  separates this card from B2's design-height reason; clozing the why instead would be
  an uncrisp phrase blank (rule 5). Forced-choice hint present per rule 13. The book's
  own stated reason is exactly "because of the incline of the stairway" — visible-why is
  faithful, not invented. PASS as drafted.

## Judgement calls

1. **Kept both Distinguish lines** (vs striking them): the batch's central interference
   is three different "who takes the head end?" answers, and parker-preferences
   explicitly wants confusables cross-linked with `Distinguish:` lines. The B2 answers
   they restate ("tallest", "higher") appear only in Back Extra — post-answer — so
   nothing is restated *visibly*; check 16's scenario-sibling leak does not apply.
2. **"on a flat stretcher lift" wording kept.** "Flat" is not in mark 2, but it is the
   contrast-frame (vs stairs) doing situational work, not a new fact claim; the fact core
   (tallest at head; head end higher by design) is verbatim-verified.
3. **n2 leaves "head and foot ends" visible** (only the attribute clozed). Clozing the
   ends too would be half-leaked by the visible c2 clause ("…shorter provider at the
   head") and would husk the row; note 1 already owns head-end recall. One-direction
   testing accepted (facts needed one way are not reversed).
4. **Numeric fields verified:** n1 "more than half" verbatim in mark 10's highlight,
   n2 "the two strongest" verbatim in mark 11's context, both p784 →
   `numeric: true`, `verified_against: "p784"`, `verified_by: "agent"` are correct.
   `needs_human_check: false` left for `verify_report.py` to derive (numerics will
   route to Parker regardless — correct behavior).

## Hand-off flags

- Drafter's flag stands: unmarked-but-tempting device-indication + anatomic-securing
  sentences in mark 10's context (one sentence to Parker, never drafts).
- **For the orchestrator, not for B's file (which I did not edit):** B2's Back Extra
  carries no reciprocal stairs contrast — the family binds one-directionally through
  G's backs. Fine as shipped; a reciprocal `Distinguish:` on B2 would be a strict
  upgrade if B's editor wants it.
- Residual coupling accepted and documented: n2's stem reveals that the strongest pair
  covers both ends, which does not answer n1 (which end is heavy / who mans it).
