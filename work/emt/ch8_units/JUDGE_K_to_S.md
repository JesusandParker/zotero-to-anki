# Independent Judge — Chapter 8, cards #28–#55 (K_rapid_extrication through S_positioning)

Judge: independent LLM judge (fresh context, no prior involvement). Date: 2026-08-12.
Scope: cards #28–#55 of `work/emt/chapter_8_cards.json`, ground-checked against
`work/emt/chapter_8_highlights.json` (marks 18–31) and the SHARED_BRIEF VERIFIED BLOCK.
Cards #0–#27 (A–J) were skimmed for cross-batch interference only, not judged.

## Verdict counts

| Verdict | Count | Cards |
|---|---|---|
| PASS | 27 | #28, #29, #30, #31, #32, #34, #35, #36, #37, #38, #39, #40, #41, #42, #43, #44, #45, #46, #47, #48, #49, #50, #51, #52, #53, #54, #55 |
| REWRITE | 1 | #33 (metadata only: `numeric` false → true) |
| DROP | 0 | — |

## The three check_cards warning adjudications

**1. #35 L_extremity_lift indication card (c1 hides "supine or sitting" + "extremity or spinal") — CLEARED, legitimate grouped indication, not a husk.**
Husk litmus (rule 17): cover c1 and the remainder is substantive, not connective scaffolding —
the move name (anchor), the negation frame "with no suspected ___ injuries", and c2's visible
"a very narrow space". The two spans are NOT mutually dependent (neither is the other's only
context); each carries its own slot-label hint ("two starting positions" / "two injury sites").
They are parallel criteria of ONE indication sentence — the decidable residue rule 26 asks for —
and the load is 2 cued chunks, well under the cap. A knower of the drill cold-solves both
(the lift starts by sitting the patient up → supine or sitting; the lift is BY the limbs with an
unsupported spine → no extremity or spinal injuries). Noted, not a defect: the move's name
half-echoes "extremity" — unavoidable for a self-describing term, and the grouped two-site +
two-position answer is not decodable as a whole by a non-knower.
Clearance string for `verified_by`: `husk_groups cleared: two parallel indication criteria, each
independently hinted, anchor (move name + negation frame) visible; load 2`.

**2. #39 M_direct_carry positions card (c1 two spans, c2 four spans) — CLEARED, legitimate positions matrix at the cap.**
The numbers split by ROLE (c1 = your station + your arms; c2 = the partner's four), so each
generated card shows the other role in full as its anchor — the two-way structure, not a husk
(cover either number and the remainder carries a complete half of the drill). Every blank has a
local frame cue ("you stand at the ___", "facing ___::whom", "hands under the ___", "grasping
the ___"), all grounded verbatim in mark 20's numbered drill text. c2's four blanks sit exactly
at rule 23's ≤4 ceiling and form one coherent spatial picture (where the partner stands, faces,
holds); they are different facts per number, not one enumerated set fanned across numbers, so
rule 24 is not implicated. Borderline by raw count — at the cap, not over it — and the role
split is precisely how rule 23 wants load contained.
Clearance: `husk_groups/overloaded_group cleared: role-split two-way; c2 = 4 frame-cued blanks
at the rule-23 cap, other role visible as anchor`.

**3. #41 N_scoop_stretcher one-side card (c1 hides "one side at a time" + "far hip and upper arm") — CLEARED, legitimate.**
Cover c1: "A scoop stretcher is worked under the patient ___, lifting the patient slightly by
pulling on the ___ (two pull points)" — the device, the action, and the lift mechanism all stay
visible; not scaffolding. The spans are complementary halves of the single insertion technique
(the manner + the pull points), independently cued (manner frame vs "pulling on the ___" with a
two-pull-points hint), grounded verbatim in mark 21's drill text ("Position the stretcher, one
side at a time. Lift the patient's side slightly by pulling on the far hip and upper arm").
Load 2. A knower cold-solves both; a non-knower decodes neither.
Clearance: `husk_groups cleared: complementary halves of one technique fact, each independently
cued; load 2`.

## K-block specific verifications (all four confirmed)

- **Invented sub-group names handled per rule 23.1.** #28/#29 print "environment" / "patient
  factors" VISIBLE and unclozed, both notes carry the full six-item `Roster:` with own members
  bolded, and there is NO anchor note — which is exactly what rule 23.1 prescribes for an
  unordered set, using TABLE 8-3 itself as its worked example ("An UNORDERED set gets NO anchor
  note at all... The sub-group notes plus their Roster: lines are the whole family"). Correct.
- **No self-leak in the sub-group names.** "Environment" and "patient factors" name categories,
  not members — neither hands over "vehicle/scene unsafe", "explosives/hazmat", "fire", nor any
  patient predicate. (#29's visible row scaffold "the patient ___" repeats only what the
  category name already says; the load-bearing predicates are all hidden.) List completeness vs
  the real source: 3 + 3 = the stated six, matching VERIFIED BLOCK #3's count of TABLE 8-3.
- **Timing card #30 carries the license.** The 6-to-8-minutes claim carries the VERIFIED
  BLOCK's `visual_source` verbatim ({pages: ["803"], figures: ["page_803.png"], note: "6-to-8-minute
  vest/short-backboard placement time, read from the p803 render"}); "1 minute or less" grounds
  normally in mark 18's context; `numeric: true`, `verified_against: "p803"`, `verified_by:
  "agent"` all present. Correct.
- **Gasoline vignette (#34) is not pattern-matchable.** "Gasoline" appears in no other card's
  Text, Back Extra, or Ex line in the file; the sibling roster rows name only the abstract
  categories ("explosives or other hazardous materials", "fire or danger of fire"), so the
  student must perform the mapping gasoline → hazmat/fire-danger → rapid extrication, which is
  the tested reasoning. "Your crew is at the vehicle with you" correctly walls off the J-block
  one-person techniques, and "which NAMED technique" + seated-in-vehicle walls off the floor
  drags. Fresh exemplar, real discrimination.

## Per-card rationales

**#28 K — environment sub-group. PASS.** Three items verbatim from mark 18's context; grouped
under one c1 (load 3); `<br><br>` rows; Roster with own members bolded; Why line grounded ("the
delay... is a contraindication"). Membership lane per rule 30, partition derivable by a knower
(the other three all begin "the patient..."). Stated count six = tested six across the pair
(check 17, against VERIFIED BLOCK #3).

**#29 K — patient-factors sub-group. PASS.** Rows lead with the visible scaffold "the patient"
and hide the full predicates (hides more than it shows, leads toward the cloze — rule 18's good
shape, not rule 22's). Closed taxonomy the source enumerates, so cold-solvable. Cue mnemonic
(cannot assess / cannot wait / cannot reach) is an authored hook, back-side, non-distorting.
Roster bolds its own three. Grounded verbatim.

**#30 K — timing contrast. PASS.** c1/c2 are different numbers → two cards, each showing the
other duration as anchor (licensed contrast, not a fanned list). Rule 27 satisfied on both
cards: visible parallel number on the c1 card, unit "minutes" hard against the blank on the c2
card. Both digits verified (p803 + VERIFIED BLOCK #2). Back Extra grounded ("local protocols"
line is in mark 18's context).

**#31 K — risk / do-not-use. PASS.** Two forced-choice binaries under one number, both hinted
(rule 4). Grounded verbatim ("produce a greater risk of spine movement... do not use... if no
urgency exists"). The "so" connective mirrors the book's own causal logic; deriving blank 2 from
blank 1 is mechanism reasoning, not decoding.

**#32 K — stand-and-pivot. PASS.** Grounded verbatim ("If the patient is able to stand and
pivot to the stretcher, it is safer to have them do so"). Decision-framed, forced-choice hinted.

**#33 K — team of three. REWRITE (metadata only).** Text and Back Extra unchanged:
Text: `The rapid extrication technique requires a team of {{c1::three::number of providers}} providers who are knowledgeable and practiced in the procedure.`
Back Extra: `Why: the support is entirely manual — several practiced hands substitute for a device's stabilization, so training, not just a head count, meets the requirement.`
Fix: set `"numeric": true`. The clozed answer is a count, and the brief is categorical ("Every
number, distance, weight, count or time window → numeric: true"); with `numeric: false` the
derived safety overlay (`verify_report.py`) never sees it. The digits themselves check out
(`verified_against: "p803"` verbatim in mark 18's context) and the rule-27 slot-label hint is
already Parker's own pattern, so nothing else changes.

**#34 K — gasoline vignette. PASS.** See adjudication above. Grounded instantiation of two
TABLE 8-3 rows; Pitfall line grounded (device delay = contraindication); pairs the K facts with
the decision framing the brief asks for.

**#35 L — indication. PASS.** See adjudication above. Grounded verbatim in mark 19's context;
c2 (narrow space) independently cold-solvable with a scene-constraint hint; from_idx [19, 20]
correct (the Distinguish line leans on mark 20). Back Extra Why/Distinguish grounded.

**#36 L — positions. PASS.** Decidable residue (positions, grips), not step recitation — no
ordinal is clozed, no row is position-cued. c3 = describe→name (forced); c1 = your two grips
(load 2); c2 = partner's three (load 3, forced-choice hint on the facing blank, which is the
real confusable vs the direct carry). Numbers mark different fact clusters, so no rule-24 fan.
All spans verbatim from mark 19's drill text; Cue line (kneel-facing-each-other opening,
partner moves between legs only after sit-up) grounded in steps 1–4.

**#37 M — definition. PASS.** Two-way-style: c1 name vs c2 (supine + bed, independently
hinted); "lifted and carried in the providers' arms" is the visible discriminator that forces
the name against the draw-sheet method. Back Extra draw-sheet/able-patient/direct-body-carry
content all grounded in marks 20–21 contexts; from_idx [20, 21] correct.

**#38 M — stretcher setup. PASS.** Two forced-choice blanks (parallel/perpendicular,
same/opposite), grounded verbatim in mark 20's step 1. Back Extra prep details and draw-sheet
prep both in mark 20's context. Consistent with card #9's height facts (no cross-batch
contradiction).

**#39 M — positions matrix. PASS.** See adjudication above. All six spans verbatim from mark
20's steps 2–3; third-provider Ex grounded; Distinguish cross-link to the extremity lift is the
blessed house pattern (back-side).

**#40 N — first thing / length. PASS.** Ordinal printed, never clozed; blanks are a
forced-choice state (separated/locked) and a hinted dimension (length) — decidable residue.
Grounded verbatim in mark 21's step 1. The four-ways-off-the-floor enumeration correctly stays
back-side (it is context, not a mark — rule 29).

**#41 N — one side at a time. PASS.** See adjudication above.

**#42 N — locking. PASS.** Grounded verbatim in mark 21's step 3 + caption ("avoid pinching
both the patient and your fingers"). Two locally-cued blanks under one number, load 2. The
repeat of "one at a time" across #41/#42 is the source's own fact in both places; pattern
transfer yields the correct answer for the correct reason.

**#43 N — straps before transfer. PASS.** c1 action (crisp verb+object, "securing step" hint)
and c2 forced-choice Before/after on separate numbers, each anchoring the other. Grounded
verbatim in mark 21's step 4; Distinguish vs direct-carry strap timing grounded in mark 20
(from_idx [21, 20] correct).

**#44 O — blanket prep / unroll. PASS.** Blanks are values (how much rolled; which direction —
forced-choice), cued by content, not position; narration is scaffold. Grounded verbatim in mark
22 (Steps 1–3); "by half" carries a "how much" slot label; `verified_against: "p836"` present.
("By half" read as extent-of-manner, not one of the brief's five numeric classes — the
verified_against/verified_by protection is set regardless; see metadata notes.)

**#45 O — roll up the ends. PASS.** Scenario-framed, one crisp verb+object blank with a "grip
prep" hint; grounded in mark 22's step 4 caption and mark 21's context ("rolling up the excess
material on each side"); from_idx [22, 21] correct. Distinguish vs the scoop is grounded and
earns its place.

**#46 P — pull injuries. PASS.** Two one-word blanks, each carrying the class hint
"musculoskeletal injury"; the pull mechanism + class + two slots close the answer space to the
canonical joint/bone pair (rule 16's "hard-but-forced," not open-set). Grounded verbatim in mark
23. Back Extra pull-vs-grip Distinguish, brittleness Why, and RA/pain Pitfall all grounded in
mark 23's context. Cross-linking with #47 is back-side house style.

**#47 P — thin skin. PASS.** c1 forced-choice (thicker/thinner); c2 pair (tears, bruising)
grounded verbatim. The mutual derivability between thinner and tears is the mechanism itself —
the blessed kind of inference (as in the recipes' shock-chain example), not a definitional leak.

**#48 Q — bariatrics. PASS.** Textbook two-way definition: c1 term ("medical specialty" hint),
c2 meaning crisped to 4 words with the source's "(prevention or control)" parenthetical moved to
a back-side Meaning line — exactly the R12 pattern. `Parts:` covers mark 25 (the Greek roots
Parker highlighted) via Rule-0 synthesis instead of a fragment card; note-format licenses
`Parts:` on any decomposable term, which governs over the brief's abbreviated label list. Why
line grounded in mark 24's context. from_idx [24, 25] correct.

**#49 R — flexible stretcher. PASS.** c1 describe→name forced by the paradox cue ("forms a
RIGID stretcher"); c2 = the two defining properties (rigid + conforms-to-sides-no-farther),
name visible as anchor. Noted, within tolerance: the second c2 span is 8 words — at the long
edge of R12 but one coherent, concept-reproducible image whose "no farther" half is the
discriminator vs frame devices, and it sits under the ≥9-word warning bar. Back Extra
(confined-space use, roll-up storage, rope work, basket contrast) all grounded in marks 26/28
contexts; the unmarked confined-space indication correctly stays back-side (rule 29).

**#50 R — vacuum mattress. PASS.** Three numbers = three different facts (alternative-to-what /
device / behavior), each card anchored by the other two — no fan. "Air is removed" partially
echoes the transparent name on the c1 card (unavoidable for a self-describing device; the
mechanism is the identity). Grounded verbatim in mark 27 + its context; Back Extra
(pressure-point tenderness, padding-equivalent, comfort vs long spine board) grounded.

**#51 R — basket stretcher / Stokes. PASS.** Alias two-way (c1 generic name / c2 eponym, each
direction anchored by the other — the sanctioned two-way shape, not a synonym leak) plus the
indication as the situational stem. Grounded verbatim in mark 28. Pitfall (backboard first for
spinal) grounded in mark 28's context; Distinguish vs flexible grounded in mark 26 (from_idx
[26, 28] correct).

**#52 S — position of comfort. PASS.** c1 (comfort position + canonical Fowler/semi-Fowler) and
c2 (hypotensive, "blood-pressure finding" hint) on separate numbers, each anchoring the other.
Grounded verbatim in mark 29. Spinal-injury Distinguish grounded in the same context. Roster
present with own member bolded — the S-block is a keyed condition→position set split one note
per key (rule 23 option 4 / rule 25's spirit, word answers so no interpolation risk), and every
note carries the full roster.

**#53 S — shock supine. PASS.** Grounded verbatim in mark 30. Position universe is closed and
the knower's answer unique; "position" after the blank frames the slot. Roster bolds own member.

**#54 S — pregnancy left side. PASS.** Grounded verbatim in mark 31; recovery-position
Distinguish grounded in mark 31's context. Roster bolds own member.

**#55 S — pregnancy vignette. PASS.** The auto-pair the EMT profile mandates for a
finding→action fact, and the brief names positioning-by-condition as deserving decision
framing — so #54 + #55 are the licensed fact/application pair, not a duplicate discrimination.
Scenario is fresh (en route, on the stretcher); discriminators (late pregnancy, hypotensive,
flat on back) force exactly one action. Pitfall ("hypotension is not required") is a real,
grounded edge.

## Cross-batch interference scan (A–J fronts, not judged)

No A–J card states or spells a K–S answer: the J-block one-person cards never name rapid
extrication; #34's "your crew is at the vehicle with you" cleanly separates it from J's solo
scenarios; #21's blanket-DRAG classify card and O's blanket-CARRY cards test different facts
with explicit context walls; #38's draw-sheet height Cue agrees with #9's (level or slightly
lower onto the stretcher) — no contradiction. No verbatim exemplar reuse found in either
direction.

## Metadata notes for the orchestrator (not card-quality failures)

1. **`visual_source` key omission drift:** #35–#45 omit the key entirely while the rest of the
   file carries `"visual_source": null`. Harmless to consumers; normalize to `null` for
   consistency when convenient.
2. **A–J numeric-flag inconsistency observed in passing (outside my batch):** #5 clozes "at
   least 10 inches (25 cm)" and #10 clozes "four::number" with `numeric: false` — same class of
   issue as #33. Flagging for whoever judged A–J; I did not judge those cards.
3. **Visible structural counts cleared:** #28/#29 state "six situations" (and #37/#39 et al.
   name no counts) — the stated six is scaffolding verified complete against TABLE 8-3
   (`verified_against: "p803-804"`), not a clozed quantity; `numeric: false` is correct there.
4. **`Parts:` label on #48** is licensed by note-format (governing doc) despite being absent
   from the SHARED_BRIEF's abbreviated label list; it is also the coverage vehicle for mark 25.
