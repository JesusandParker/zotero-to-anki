# JUDGE — Chapter 8, cards #0–#27 (blocks A_stretcher_strapping … J_emergency_drags)

Independent LLM-judge pass, 2026-08-12. Cold review: full `editor-checklist.md` run on every
card, checks 18–24 per ROW; every claim ground-checked against the cited marks'
highlight+context in `chapter_8_highlights.json` (and the SHARED_BRIEF VERIFIED BLOCK for the
p801-licensed cards #25–#27). Consolidation-edited cards (#4, #9, #12, #26) judged cold, no
editor rationale read. Cards #28–#55 skimmed (Text fields only) for cross-batch interference —
none found that changes a verdict (details at bottom).

**Counts: 27 PASS · 1 REWRITE (#4) · 0 DROP.** Both routed check_cards warnings (#6, #20)
cleared as paraphrases.

## Verdict table

| # | Block | Card (short) | Verdict | Key findings |
|---|-------|--------------|---------|--------------|
| 0 | A | Four belt locations, grouped c1 | **PASS** | 4 uncued ≤4 (rule 23); `<br><br>` rows, count visible; order grounded (book numbers 1–4); Why verbatim from context. |
| 1 | A | Four-point harness | **PASS** | Crisp term cloze; one answer; tightness qualifier correctly carried as Pitfall — clozing "breathing" would self-answer (a chest strap limits breathing; rule 20/22 padding). |
| 2 | B | First key rule of lifting | **PASS** | Two spans one number = one cohesive rule (straight back + no twisting); each blank independently anchored, no husk; Why/Pitfall verbatim from context. |
| 3 | B | Head higher / tallest at head | **PASS** | Coin-flip hinted (higher/lower); "tallest" forced by visible offset-the-height logic *plus* the hidden direction — non-knower can't complete the inference without recalling head-is-higher. Distinguish cross-links stairs/strongest (mark 10) per house pattern. |
| 4 | C | Power grip — palm up | **REWRITE** | Check #4 fail: the term↔purpose binding ("power grip = the max-force grip for lifting") is the highlight's lead sentence, fully visible, untested anywhere in the batch (#5 tests only the 10-in spacing). Add a c2 on the term. Exact replacement below. Everything else sound: coin-flip hinted; the three Back Extra components all grounded (Why: mark 3 context; Cue: mark 3 highlight; power-lift Distinguish: mark 2 context) and each earns its place. |
| 5 | C | Hands ≥10 in (25 cm) apart | **PASS** | Operator+value+unit inside one cloze (§5); "___ apart" self-announces a distance (rule 27 attributive scope doesn't apply); digits verbatim on p761. **Metadata note:** drafter left `numeric: false` — `verify_report.py` derives numeric from Text and will flip it to true; with `verified_against: p761` set it lands in Section B (verified, skim). Confirm the report ran before staging. |
| 6 | D | Move one at a time, never simultaneously | **PASS** | Warning cleared (below). Forced-choice hint per check #13; Ex's 15–20 in (38–50 cm) verbatim in mark 4 context. |
| 7 | D | Drag across a bed → kneel on the bed | **PASS** | Purpose clause ("avoid reaching beyond the recommended distance") correctly moved to Back Extra — visible it would half-decode the answer. Hint is a clean slot-label. Kneel consolidation point for #9's dedup — correct (rule 12). |
| 8 | E | Pull the sheet/blanket, never clothing | **PASS** | Rule 21(b) good shape: the rejected alternative (clothing) visible as the anchor. 6 in (15 cm) in Cue verbatim p766. Bed-vs-emergency contexts keep it discriminable from the clothes drag (#19/#20); optional (not required): a Distinguish naming the emergency clothes drag as the do-pull-clothing case. |
| 9 | E | Bed-transfer setup: height (c1) + increments (c2) | **PASS** | Judged cold. Merge is legitimate: two facts, different numbers, one topic (rule 24 "not a violation"); kneel deduped to #7 and left as visible scenery. c1 anchored by direction (into hospital bed) with the draw-sheet flip taught in Distinguish (grounded via mark 20). c2 "in increments" is the weakest blank in A–J but passes cold-solve: "::pacing" labels the slot and the body-drag reach rules force incremental over continuous — hard but fair. |
| 10 | F | Diamond carry: name (c2) + count/positions (c1) | **PASS** | Endorsed two-way structure (rule 3 precision) — positions visible while term hidden is the name-it direction, not a leak. c1 load = 4 with the name as handle; `::number` satisfies check #29; rows `<br><br>`. One-handed-carry Distinguish grounded in mark 9 context. |
| 11 | F | Carried feetfirst | **PASS** | Forced-choice binary; both Why lines grounded (mark 9 highlight + context). Its Back Extra pre-states #12's facts — cross-teaching via Back Extra is the house Distinguish/Why pattern, not a check-16 sibling leak (that check targets classify cards pattern-matching a neighbor's exemplar). |
| 12 | F | Foot end: lightest load (c1) + back to device (c2) | **PASS** | Judged cold. Merge legitimate: two facts about one subject (the foot-end provider), different numbers. Both binaries carry forced-choice hints. 68–78% in Why is verbatim mark 8 context; correctly NOT its own card (context-only, rule 29). |
| 13 | G | Stairs: >half to head end (c1); head+strongest (c2) | **PASS** | c1 hint "how much" announces the quantity slot. c2's two spans are one decision (heavy end → strong provider), each independently cued — no husk. "Strongest" unhinted but forced by the visible weight rationale. Noted, benign: "68–78%" (#12) and "more than half" are the same distribution fact at different precision, so the near-miss is not a competing answer (check #1 intact). |
| 14 | G | Two strongest at ends; shorter at head | **PASS** | c1 "strongest" anchored by the stairs context (the flat-lift tallest rule is the confusable, and the Distinguish pins it); c2 forced-choice. Grounded verbatim in mark 11 + context. Genuinely counterintuitive fact — good card. |
| 15 | H | Retract undercarriage; not for curb/step/similar | **PASS** | Negation shape done right: carve-out clozed, negator loud, contrast anchor visible both directions. Three c2 items inline in a flowing sentence — R14 does not apply (prose, not rows; the three gaps are visible inline). Distinguish (backboard-down-stairs vs wheeled-stretcher-down-steps, mark 10) earns its place. |
| 16 | I | Orders in two parts: preparatory + execution | **PASS** | Closed 2-item set, grouped c1, count in stem, `<br><br>` rows. Printed ordinals are scaffold, not cues-of-position in the rule-26 sense (the order IS the semantics). Ex and Cue verbatim from mark 13 context. |
| 17 | I | Countdown: clarify what "three" is | **PASS** | The two horns of one ambiguity under one number — splitting c1/c2 would let each card recover the other horn by elimination. Synergy with #16's vocabulary makes it easier, not self-answering: cold, he must produce both roles of "three." Mark 14 is its own yellow span — the card must exist (rule 1), and this is its best shape (hiding "clarify" instead would be rule-22 filler). |
| 18 | J | Four floor/ground drag methods | **PASS** | Membership card first (rule 30), rows `<br><br>`, count visible, load 4. Names ground via FIGURE 8-14 caption in mark 16's context (VERIFIED BLOCK §4). Why grounded in mark 15 context. |
| 19 | J | Clothes drag: neck and shoulder area | **PASS** | Region is the right recall (clozing "clothing" would be tautological with the visible name). Hint is a clean form label. Distinguish (arm-to-arm) grounded. |
| 20 | J | Undo top two buttons / cannot choke | **PASS** | Warning cleared (below). "which buttons" labels the count slot (check #29 satisfied); the choke blank is easy-but-legitimate purpose recall, independently cued — no husk. |
| 21 | J | Classify: coat under patient → blanket drag | **PASS** | Check #16 clean: exemplar (coat) is fresh in the classify sense — it is the book's own non-obvious member ("blanket, coat, or other item"), appears in no sibling's Ex/definition, and the coat≠blanket twist is the real discrimination. One forced answer. |
| 22 | J | Arm drag: name (c1) + technique values (c2) | **PASS** | Two-way name/description structure; c2's three spans are §12(d) decidable residue (end-position, grip point, carriage) recalled as one gestalt, load 3 — not step recitation. Arm vs arm-to-arm Distinguish is the highest-value line and both cards carry it. |
| 23 | J | Arm-to-arm drag: name (c1) + technique (c2) | **PASS** | Same shape as #22; "backward" carries its forced-choice hint. Grounded verbatim in mark 16. |
| 24 | J | Solo vehicle removal: legs first, clear of pedals | **PASS** | Two spans one number = one image (legs clear of pedals), each with independent cues — no husk. The ORDER ("first … before any rotating") is the tested point. Why line is an unstated-but-trivial mechanical gloss of the book's step order (noted; acceptable, same license as #17's Why). |
| 25 | J | Rotate back to door; armpits; head against body | **PASS** | `visual_source` set verbatim per license (answers lean on the p801 render). c1 "back" forced by the visible armpit-drag technique; c2 spans cold-solvable (armpit thread recurs from #23; head support is THE solo detail). |
| 26 | J | Legs don't clear → slowly lower (c1); long-axis body drag (c2) | **PASS** | Judged cold. The c1/c2 split is correct (the old single-number form would have been an R10 husk), and tightening c1 to "slowly lower the patient" obeys rule 15 (crisp verb+object). c1 is soft — the visible result-phrase "onto his or her back beside the vehicle" partially constrains it — but that is the sequence-card license (rule 3 precision: a procedural continuation is not the hidden answer's definition), and no rewording keeps the sequence without implying descent. c2 carries the hard recall; the Distinguish carries the fork's other arm. |
| 27 | J | One-person techniques: only if immediately life-threatening + alone/partner-on-second-patient | **PASS** | Rule 21(a): the "only when" absolute is anchored by the "how severe" slot-label. c2 forced by the or-arm logic. Grounded verbatim in the VERIFIED BLOCK; `visual_source` correct. Constructed Ex instantiates the licensed rule (fresh, no sibling collision — #34's rapid-extrication scenario is cleanly discriminated by "your crew is at the vehicle with you"). |

## Warning adjudications (check_cards → judge)

**#6 (D block) — answer "one at a time, never simultaneously" vs mark 4 — CLEARED, legit paraphrase.**
The mark's highlight is literally *"By not moving yourself and the patient simultaneously…"* — the
"never simultaneously" half IS the mark, re-polarized. The "one at a time" half is the positive
restatement of the alternation procedure the same context prescribes verbatim (*"Alternate between
pulling the patient by flexing your arms and then repositioning yourself"* — patient moves, then you
move, strictly one at a time). No claim exists on the card that the mark+context do not state; the low
word-overlap score is the polarity flip, not an addition.
Record per note-format.md: append to #6 `verified_by` → `"agent; R13 warning cleared: answer re-polarizes mark 4's 'by not moving yourself and the patient simultaneously' + its alternation procedure"`.

**#20 (J block) — answer "choke" vs context's "choking" — CLEARED, legit paraphrase.**
Context: *"the top two should be undone to prevent the patient from choking."* Card: *"so the shirt
cannot choke the patient."* Same verb, inflected (choking → choke), recast from patient-gerund to
shirt-as-agent — and in a clothes drag pulled at the neck/shoulder, the shirt is the only possible
choking agent, so the recast adds zero content. The detector's word-overlap test simply cannot see
inflection.
Record: append to #20 `verified_by` → `"agent; R13 warning cleared: 'choke' is the inflected form of context's 'choking', shirt-as-agent recast, no added claim"`.

## The one REWRITE, in full

**#4 (C_power_grip #0).** Fail: editor check #4 (fully clozed). The highlight's lead sentence — *"You
should use the power grip to get the maximum force from your hands and arms whenever you are lifting a
patient"* — is a distinct testable binding (name ↔ purpose) sitting entirely visible, and no card in
the batch tests it (#5 tests only the hand spacing). Fix: cloze the term under a new number. One-way
(name-it direction) is correct here, NOT a two-way: the reverse direction would leak — "power grip"
visibly contains its own answer's content ("maximum force").

Replacement Text (Back Extra unchanged):

```
You use the {{c2::power grip::grip}} to get the maximum force from your hands and arms whenever lifting a patient. The arm and hand have their greatest lifting strength when facing palm {{c1::up::up or down}}.
```

- c2 card cold-solve: "the ___ (grip) to get the maximum force … palm up" → a knower names the power
  grip; "grip" is the licensed category-suffix hint (recipes §4), not a content leak.
- c1 card unchanged from the shipped version.
- The existing power-lift Distinguish now also disambiguates the c2 answer against its nearest
  confusable — it earns its place twice.

## Notes for the orchestrator

1. **#5 metadata:** `numeric: false` on a card whose answer is "at least 10 inches (25 cm)".
   `verify_report.py` derives numeric from Text and overwrites, so this self-heals — but do not stage
   without running the report. Digits confirmed verbatim against mark 3 (p761). Same pattern is NOT an
   issue on #6/#8/#12 (digits live in Back Extra only, outside the derivation's deliberate scope; I
   verified all three verbatim against their cited contexts: 15–20 in/38–50 cm p763, 6 in/15 cm p766,
   68–78% p771) nor on #10/#16/#20/#13 (spelled counts/proportions, not VALUE matches — consistent
   with #33's convention in K).
2. **Coverage:** all A–J marks (0–17) are covered by at least one card; no yellow span dropped; the
   VERIFIED BLOCK licenses (#25–#27 `visual_source`, exact strings) are used correctly and only where
   needed. Grip-mechanics narration from mark 3 is correctly kept OFF the front (rule 26: values
   carded — palm orientation, spacing; motion narrated only as Back-Extra reference).
3. **Cross-batch skim (#28–#55, not judged):** no interference with A–J. Closest pairs are all
   cleanly discriminated: #34's rapid-extrication scenario carries "your crew is at the vehicle with
   you," which excludes #27's one-person rule; #21's dragged-coat scenario cannot be confused with
   #44/#45's blanket lift-and-carry (clear-danger drag vs to-stretcher carry); #36's "wrists or
   forearms" (extremity lift) vs #22's "wrists" (arm drag) are anchored by different named moves.
   The checker's husk warnings on #35/#39/#41 belong to the K–S judge.
4. **Optional polish (no verdict attached):** a cross-Distinguish on #8 naming the emergency clothes
   drag as the licensed pull-the-clothing case would pre-empt the one plausible interference inside
   this batch.
