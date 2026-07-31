# Unit C — newborn reflexes, fontanelles, teething (marks 10–19)

7 notes → **10 Anki cards** (note 3 is a 3-cloze two-way definition; note 5 is a 2-cloze
contrast). `check_cards.py` runs clean: 0 hard, 0 warnings, grounding verified against
`chapter_7_highlights.json`.

## Fact pass (per mark)

| mark | fact | verdict | where it landed |
|---|---|---|---|
| 10 | Moro / startle reflex — caught off guard, arms fly open, fingers spread, appears to grab | **MUST-TEST** | note 1 (match card, row 1) |
| 11 | palmar grasp — object in the palm, hand closes around it | **MUST-TEST** | note 1 (row 2) |
| 12 | rooting — touch the cheek, head turns toward the touch | **MUST-TEST** | note 1 (row 3) + note 2 |
| 13 | sucking — stroking the lips prompts the latch | **MUST-TEST** | note 1 (row 4) + note 2 |
| (context, 10–13) | "in a healthy, full-term infant, certain reflexes are present at birth" | SUPPORTING | note 1 lead-in + Back Extra |
| (context, 12–13) | "Two other reflexes play an important role in feeding" | **MUST-TEST** (grouping fact) | note 2 |
| 14 | cranial bones not yet developed/fused; gaps bridged by flexible fibrous tissue; called fontanelles; let the head change shape through the narrow birth canal | **MUST-TEST** (3 facts) | note 3 (c1 term, c2 meaning, c3 function) |
| 15 | posterior fontanelle closes by the third month | **MUST-TEST** (numeric) | note 4 (row 1) |
| 16 | anterior fontanelle closes between 9 and 18 months | **MUST-TEST** (numeric) | note 4 (row 2) |
| 15/16 context | fontanelles shrink as the cranial bones grow together and fuse into a rigid structure | SUPPORTING | note 3 Back Extra (`Why:`) |
| 17 | depressed fontanelle → dehydration; bulging fontanelle → increased pressure inside the cranium | **MUST-TEST — highest-yield field fact in the unit** | note 5 (two-sided contrast) + note 6 (application) |
| 18 | `FIGURE 7-2 Fontanelles.` — caption only (`content: CAPTION_ONLY`, `needs_visual: true`) | **NOT CARDED — deliberate, see below** | figure request recorded below |
| 19 | teething = baby teeth breaking through the gums; can be painful; sometimes a LOW-GRADE fever | **MUST-TEST** (the qualifier is the point) | note 7 |

No mark was silently dropped. Mark 18 is the only one without a card, and that is the
explicit instruction (a caption is a pointer, not a fact — carding it alone would be R13).

## Merges and archetype decisions

- **Marks 10–13 → ONE classify/match card, not four definition cards.** The four reflexes
  are a natural description → name set. Per `regression-cases.md` R17 a classify/match card
  (`description = {{c1::category}}`) is an explicitly licensed neighbour of the
  fragment-clozed-list defect, not an instance of it, and the lead-in carries the required
  imperative ("Name each one…"). I deliberately did **not** also emit four one-fact cards —
  that is the R2 over-fragmentation the consolidation stage exists to kill.
- **Reverse direction (name → describe) was considered and rejected.** `parker-preferences`
  licenses single-direction precisely for the **scenario→name** case, and these four are
  vivid behavioural descriptions, i.e. scenario→name. Two-waying them would have produced
  a card hiding four long descriptions at once. Row craft follows card-rules #18: the shared
  scaffold ("… = the ___ reflex") stays visible and only the discriminator is clozed.
  Moro's alias sits *inside* the blank (`Moro (startle)`) and the word "startled" is kept
  out of the visible row, so the row cannot leak its own answer and either name counts.
- **Note 2 (rooting + sucking = the feeding pair)** is a separate claim from note 1
  (which behaviour = which name), so it is not a dedupe target — but it is the one card in
  this unit I would drop first if consolidation finds Chapter 7 heavy. Its Back Extra was
  written *not* to restate note 1's row descriptions verbatim, to avoid an R6 sibling leak.
- **Marks 15 + 16 merged into ONE two-row contrast card** (card-recipes §8): both entities
  visible, both closure ages under the same cloze number so they reveal together. Rows use
  `→` rather than `=` on purpose — with `=` the two short rows sit close enough to trip
  `equation_husk_groups`' 40-character window (a known false positive on grouped rows).
- **Mark 17 got two cards** — the two-sided contrast (note 5) plus one application card
  (note 6), per `profiles/emt.md` §3 auto-pair and the brief's carve-out that a finding
  which changes field management earns one application card. Note 6 runs the **reverse**
  direction (dehydration scenario → expected finding), so it is a genuine complement to
  note 5's finding → meaning, not a duplicate. Fresh scenario, not reused from any sibling.

## Things the next stage must know

1. **FIGURE 7-2 is wanted on the fontanelle cards — Parker asked for it by name** on mark
   18: *"I want to see if you can add a high-quality screenshot like a high definition
   screenshot of this into the flashcards relating to the fontanelles."* I did not attach
   anything (the figure pipeline runs later). The matcher targets, strongest first:
   **note 5** (contrast, "fontanelle" ×3 + Back Extra), **note 4** (closure, ×3),
   **note 6** (vignette, ×2), **note 3** (definition, ×2). Note 3's occurrence of
   "Fontanelles" is inside the c1 cloze, so if the matcher reads only the *visible* stem it
   may score note 3 low — notes 4 and 5 are the safe carriers. Per `note-format.md` the
   plate belongs on the **back** here (a labelled anterior/posterior fontanelle diagram on
   the front of note 4 would be an answer key).
2. **Note 5 will look like a husk to a fast reader — it is not.** It is the licensed
   multi-dimensional contrast of R10 ("cover c2 → the depressed/bulging anchors remain;
   cover c1 → the dehydration/ICP anchors remain"), and both c1 blanks carry the
   forced-choice hint. `check_cards.py` did not flag it. Do not "fix" it into singletons.
3. **Note 3 carries `needs_human_check: true` for grounding, not for a number.** Mark 14 is
   `grounding: PARTIAL` only because the 450-char context window cuts at "These areas,
   called" — the continuation ("fontanelles, allow the newborn's head to change shape
   slightly as it passes through the narrow birth canal") is verbatim at the head of marks
   15/16/17's context, so the claim is fully verifiable. Human glance should be quick.
4. **Note 4 is the numeric card** (`numeric: true`, `needs_human_check: true`): posterior
   **by the third month**, anterior **between 9 and 18 months**. Read verbatim off mark
   15/16 highlights; nothing was imported from another chapter. Note that `check_cards.py`'s
   `VALUE` regex does not treat "months" as a unit, so this card is **not** caught
   automatically — the flag is asserted by hand and must survive `verify_report.py`.
5. **One inference beyond the literal source, disclosed:** note 7's Back Extra says a high
   fever "should not be written off as teething." The source states only that teething is
   "sometimes accompanied by a low-grade fever" — the do-not-dismiss corollary is a
   one-step clinical inference, and it is what makes the qualifier worth carding. It was
   drafted at the orchestrator's explicit direction. If the gate wants strict literalism,
   soften to "the fever the source attaches to teething is low-grade only."
6. **Note 1 runs ~80 words**, over Layer A rule 6's 60-word prose cap. That cap targets
   prose; a genuine cohesive list stays whole at any length (Parker's rule, card-rules #6,
   and the 8-row DCAP-BTLS exemplar). Do not split it into two match cards.
7. Nothing in this unit overlaps units B or D: mark 9 (infant bag-mask/airway) is B's,
   TABLE 7-2 and separation anxiety (marks 20–22) are D's. Teething appears in the body of
   mark 18/20's context window as well — if unit D also cards teething off TABLE 7-2's
   "6 months: begins teething" row, that is a **different** fact (age of onset) and both
   should survive; only a verbatim second "low-grade fever" card would be a dedupe target.
