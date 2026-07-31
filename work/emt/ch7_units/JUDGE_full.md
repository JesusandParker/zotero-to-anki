# Chapter 7 — independent JUDGE pass (59 notes)

Judge wrote none of these cards and edited none of them. Read-only: **no file in the batch
was modified by this pass.**

Standards applied: all 24 checks of `reference/editor-checklist.md` on every card, checks
18–24 **per row** on every multi-row card, against `card-rules.md`, `parker-preferences.md`
and every MUST-NOT-OVER-FLAG precision in `regression-cases.md`.

Verification actually performed (not assumed):
- **All 36 cells of TABLE 7-1 re-read off the plate** `work/emt/figures/TABLE_7_1.png`
  directly, not off `SHARED_BRIEF.md`. Brief and plate agree in every cell; cards #0–#4
  reproduce them correctly, including all six column collapses.
- Every arithmetic claim in the Back Extra of #0–#6 recomputed against the plate.
- Every card's claims checked against the `context` of the marks its `from_idx` cites.
- `check_cards.py` re-run: 59 cards, 0 hard errors, the 3 warnings ruled on below.
- Mechanical sweeps: mark coverage, banned HTML, source-artifact words, single-`<br>`
  layout (R14), Back Extra label vocabulary, `visual_source` shape, cross-card answer
  collisions, word-count cap.

**Result: 58 PASS · 1 FIX.**

---

## The three gate warnings

### 1. `#4: row label 'Older adult' shares ['older'] with its own answer '61 years and older'` — **CLEAR**

Not an R15 tautology. The tested content of the row is the digit **61**; "Older adult" cues
nothing numeric, so the label does not hand over the blank — it only shares the ordinary
English word *older*, which appears in the answer solely because the band has no upper
bound. This is the documented MUST-NOT-OVER-FLAG side of a detector R15 itself calls
"deliberately generous — a shared word stem is evidence, not proof." Distorting the table's
own wording (e.g. "61+" or "61 years and up") to silence the warning would make the card
worse and would no longer match the plate. Row cold-solves: label = band name, answer =
numeric span, forced. Agreeing with the drafter and unit A's editor.

### 2. `#34: cloze c2 hides 2 multi-word spans in an inline template — possible husk` — **CLEAR**

Card #34 is *verbatim the shape R10 tells the judge to clear*. Compare R10's own licensed
exemplar — `{{c1::cover}} is the tactical use of {{c2::an impenetrable barrier}}, whereas
{{c1::concealment}} only {{c2::hides you from view}}` — with #34. Litmus applied in both
directions:

- **Cover c1:** "___ is our perception of ourselves, whereas ___ is how we feel about
  ourselves and how we fit in with our peers." Both definitions remain visible and force
  both names.
- **Cover c2:** "Self-concept is ___, whereas self-esteem is ___ and how we fit in with our
  peers." Both **entity anchors stay visible**, plus the peer-fit clause, which is the
  discriminator that clinches which side is which.

Neither blank's only cue is the other blank, so this is not a husk; it is a
multi-dimensional contrast. Both c2 spans are 4 and 5 words (R12 crisp). Splitting into
c2/c3 would be the "do not fix a genuine contrast card into split singletons" error, and
would additionally let a *non-knower* decode each blank by contrast with the other.

### 3. `#0 & #1: 86% similar Text — possible duplicate` — **CLEAR**

R12 dedupes **by meaning**, and these two share no claim: #0 is the pulse column of TABLE
7-1, #1 is the respirations column. The 86% is entirely the deliberately identical row
skeleton (`Normal <b>X</b> in <unit>, by age group:` + nine band labels), which is a feature
— it lets Parker learn the table one column at a time, and Parker's list preference wants
exactly this layout. The discriminator is on the front, bolded, with its unit
(`pulse rate` / beats/min vs `respiratory rate` / breaths/min). Merging them would produce
one unanswerable 24-blank card.

---

## Per-card verdicts

`#0 PASS` — pulse ladder. All six ranges match the plate; "Adolescent through older adult —
60 to 100" is a valid 4-row collapse. `Cue:` arithmetic verified: lower bounds walk 100, 100,
90, 80, 70, 60. `numeric` with `verified_against` set, so `needs_human_check: false` is the
correct *derivation*, not a lost flag.

`#1 PASS` — respiratory ladder. Digits and collapse correct. Back Extra verified: infant
40 breaths/min is inside 25–50 and is 2× the adult ceiling of 20; neonate floor 30 > adult
ceiling 20, so the bands genuinely never overlap.

`#2 PASS` — systolic ladder. The trap is handled correctly: adolescent stays its own row at
90–110 and the 90–130 collapse begins at early adult. Back Extra "ceiling holds at 110 until
age 19, then rises to 130" verified against the plate.

`#3 PASS` — temperature ladder. Three-row collapse valid. Both Back Extra claims verified as
uniquely true: neonate is the only band reaching 100°F, infant/toddler the only bands dipping
below 98°F.

`#4 PASS` — nine age bands. All nine spans match the plate; "birth to 1 month" is grounded in
mark 1's own sentence. Nine rows cold-solved individually. Back Extra's boundary-year
observation verified (12 sits in both school age and adolescent; 18→19 does not overlap).

`#5 PASS` — direction of change. Not an R10 husk: all three entity anchors stay visible, both
blanks carry the mandatory forced-choice legend (check 13), and "whereas" is a visible
contrast anchor. Grounded verbatim in mark 0's context.

`#6 PASS` — 140 beats/min, infant vs adult. Both blanks legended. The editor's removal of the
prose's "60 breaths/min" is the right call and is recorded: TABLE 7-1 caps infant respirations
at 50 and puts 60 only in the neonate band, so keeping it would have put two cards in one
shuffled deck teaching opposite things. Back Extra arithmetic verified (140 − 100 = 40).

`#7 PASS` — neonate weight timeline. Five rows, each with a distinct time label forcing exactly
one answer; not a husk (the visible remainder is five substantive labels). Grounded across
marks 2/4/5. Lead-in correctly avoids the earlier "first year" heading that leaked the last
row. `Ex:` line is disclosed arithmetic on the source's own rule.

`#8 PASS` — head 25% → lands headfirst. c1/c2 on different numbers so each anchors the other.
"total body weight" is the source's own phrase in mark 5's context tail.

`#9 PASS` — nose breathers / under 6 months. Dropping "nasal" from the second clause correctly
removes the visible copy of the hidden c1 answer. `::nose or mouth` is a required forced-choice,
not an R11 letter hint.

`#10 PASS` — choking vignette. The rejected alternative is made visible ("The mouth and throat
are clear"), which is card-rules #21(b)'s licensed fix and turns a former open-set blank
("the airway" also fit) into a forced one.

`#11 PASS` — infant airway/head differences. This is Parker's margin card and it is built the
way he asked. Every row **leads with its cloze**, so the items are the answers (R22 satisfied,
not dodged). Lead-in correctly says "airway and head" — the occiput is not an upper-airway
structure and the earlier "upper airway" framing was ungrounded. No count asserted, correctly:
p688's list is an explicit "such as" list.

`#12 PASS` — hyperextension/hyperflexion. The c1 pair are parallel members of one closed
opposition, not mutually-defining spans; covering c1 still forces the pair. `Meaning:` gloss
closes the prerequisite (rule 11).

`#13 PASS` — rib cage / belly breathing. The former unhinted coin flip is fixed: the shared
scaffold stays visible and only the crisp discriminators are hidden, each legended.

`#14 PASS` — barotrauma. Two-way definition with c2 at 5 words (R12 clean); no parenthetical
anywhere, so R3's "a two-way definition is not a leak" precision applies and it must not be
"fixed." c3 forced by "the cause is ___ with a bag-mask."

`#15 PASS` — four-reflex roster. Grouped reveal of the items themselves (card-rules #22's
preferred shape (a)). Count matches the visible blanks. Back Extra's `Ex:` maps only palmar
grasp and sucking — the two rows deliberately dropped from #16 — so it leaks nothing.
*Watch-item, not a defect:* "four reflexes are present at birth" states a count the source
hedges as "certain reflexes"; the count is what makes the card cold-solvable and it matches
the four the chapter teaches.

`#16 PASS` — name-the-reflex. Only the two **opaque** names survive as rows; *palmar grasp*
and *sucking* were correctly dropped because their cues must contain "palm"/"closes around"
and "lips"/"latch on", which are literal descriptions of the names. The Moro alias was moved
out of the cue, so "caught off guard" no longer hands over *startle*. Neither name is
derivable from its cue.

`#17 PASS` — fontanelle two-way definition. c2 = 6 words (R12 boundary, acceptable), c3
("change shape") is a real untested fact, not filler. Grounding is fine despite mark 14 being
`PARTIAL`: the continuation is verbatim in mark 14's own `highlight` and at the head of mark
15's context. `needs_human_check: true` correctly retained.

`#18 PASS` — fontanelle closure ages. Lead-in correctly avoids asserting "the two fontanelles"
(the skull has six). Rows are parallel members; posterior/anterior anchor each blank. Digits
verbatim from marks 15/16.

`#19 PASS` — depressed vs bulging. Licensed R10 multi-dimensional contrast, verified in both
directions: cover c1 and *dehydration* / *increased ICP* anchor the legended blanks; cover c2
and *depressed* / *bulging* anchor them. Not split.

`#20 PASS` — teething. The load-bearing qualifier (*low-grade*) is clozed, so no R1 failure.
"can be ___" is anchored by its sibling blank in the same group. See TOP FINDINGS #3 for the
Back Extra's flag, which is a reporting gap, not a card defect.

`#21 PASS` — TABLE 7-2, months 2–6. All five rows checked against mark 20's context: 4, 5, 2,
6, 3 all correct. Match card, so R22's classify exemption applies. Row order deliberately
scrambled so position cannot be counted off.

`#22 PASS` — TABLE 7-2, months 7–12. All six rows verified: 9, 12, 7, 11, 8, 10 all correct;
together with #21 the full 11-row table is covered. The one genuinely confusable row (12
months) is kept co-visible with its 10- and 11-month look-alikes so each is the other's
rejected alternative, with the degree pivot italicised. Direction (milestone → age) is right;
the reverse would be a textbook R16 open-set.

`#23 PASS` — separation anxiety. **Grounding specifically re-checked and it holds:** the term
*anxious-avoidant attachment* in the Back Extra is not invented — it sits at offset 2196 of
**mark 20's** context, which is why `from_idx` is `[20, 21, 28]`. Mark 28 is recorded here, so
it is provably covered rather than silently dropped.

`#24 PASS` — trust versus mistrust. c1 forced (only one stage runs birth → ~18 months); c2's
two spans are anchored by the visible term. The `Meaning:` line is not a banned re-definition
— the Text gives only the time span, so the meaning is genuinely new. `Pitfall:` grounded
across marks 21/22, which `from_idx` cites.

`#25 PASS` — lung musculature. The unclozed bronchioles/alveoli clause is *unhighlighted*
context serving as the contrast anchor that forces c1, not a yellow fact left as scenery.

`#26 PASS` — passive → acquired immunity. c1 anchored by the visible *acquired immunity*
counterpart (a paired term, not a definition, so not an R3 leak). c2's pair is the source's
own closed pair.

`#27 PASS` — preschool brain 90%. Single forced number, `::percentage` is a form-label. The
"(3 to 6 years)" band is grounded in mark 23's own context (FIGURE 7-5 caption), which
`from_idx` cites.

`#28 PASS` — toilet training. All three numbers tested, each under its own cloze number so the
other two stay visible as anchors. Prose, not rows, so correctly no `<br><br>` (R14
must-not-over-flag).

`#29 PASS` — language milestones. Two numbers on separate clozes, each anchored by the other.
Verbatim from mark 29.

`#30 PASS` — cause and effect at 18–24 months. Both Back Extra lines grounded inside mark 30's
own context.

`#31 PASS` — parent as secondary patient. Real decision card; cloze is two load-bearing words
(R8/#15 satisfied) with a `::role on scene` slot-label. The invented panic behaviour was
correctly pulled back to the source's own wording.

`#32 PASS` — school-age annual growth. Both numbers clozed with their units inside the
deletion. Teeth/hemispheres correctly in Back Extra (unhighlighted).

`#33 PASS` — three levels of moral reasoning. Verified in both directions: c1 hidden → the
three drivers force the three names; c2 hidden → the three names force the drivers. Licensed
contrast, not a husk. Count 3 = 3 clozed and the source names the third level explicitly. Row
1 correctly tests mark 33's own yellow clause rather than the unhighlighted neighbour sentence.

`#34 PASS` — self-concept vs self-esteem. See gate ruling 2.

`#35 PASS` — adolescent growth spurt. Arrows sit outside the clozes; the c2 duration card keeps
the sequence visible as its anchor and the c1 card shows three blanks at a glance. "2 to 3
years" correctly clozed rather than left as scenery.

`#36 PASS` — girls 16 / boys 18 / taller. Not a husk: the entity anchors (*girls*, *boys*) stay
visible and only the differing values hide. The binary carries its mandatory
`::taller or shorter`. Back Extra's 12–18 band is grounded in mark 37's context.

`#37 PASS` — menarche. Two-way definition (c2 = 4 words) plus the frequency fact as c3. The
former standalone freebie is fixed correctly: the telegraphing *but* is gone, the tail no
longer contains any form of *menstruate* (which would have leaked c2), and c3 carries a true
forced-choice legend. The card now runs against intuition, which is what makes it worth
reviewing.

`#38 FIX` — leading cause of death. **Defect:** the card teaches "All age groups younger than 44
years → unintentional injury" as an unqualified rule, but this same chapter contradicts it at
p688 (mark 6's context, verbatim): *"the leading cause of death for the neonate and infant age
group is congenital abnormalities (ie, birth defects)."* Both unit B's and unit F's editors saw
the collision, each correctly declined to assert it from their own marks, each explicitly asked
consolidation to add a cross-linking `Distinguish:` line — and consolidation did not. The card
ships teaching the broader claim with no caveat, and *congenital abnormalities* is the standard
answer for the infant age group. The claim is grounded in this chapter's own highlight set, so
the fix requires no outside fact. **Replace the `Back Extra` with:**

> `Distinguish: the under-44 figure is the combined-population rule, and this chapter names its own exception — for the neonate and infant age group the leading cause of death is congenital abnormalities (birth defects).<br><br>Pitfall: middle adults may already have diabetes or hypertension without knowing it, so a denied medical history does not rule them out.<br><br>Cue: rising cholesterol, decreasing cardiac efficiency, and harder weight control mark these years, though proper exercise and a healthy diet blunt much of the effect.`

> and widen `from_idx` from `[39]` to `[6, 39]` so the added claim is provably grounded.
> The `Text` is correct as written and must not change — it is verbatim from mark 39.

`#39 PASS` — atherosclerosis two-way definition. c2 = 3 words. R3's precision protects it from a
"leak" fix. Back Extra restores the source's disjunction ("restricted **or** blocked"), removing
the earlier ungrounded "and eventually".

`#40 PASS` — 60% of over-65s. Two spans, both form-hinted, not mutually defining. Verbatim from
mark 41. The shared `Distinguish:` line sets up the `Pitfall:` chain (illness raises rate →
weakened myocardium → plus atherosclerosis → fatal), so it is congruent here, not a non sequitur.

`#41 PASS` — three ways aging weakens the heart. Rows lead with their clozes. The closure claim
is honest as re-scoped: narrowing from "cardiovascular" to "the heart" makes the three
exhaustive for this passage's cardiac list, with the fourth (vascular) change owned by #42.
Row 3 correctly softened from "cannot" to "diminishes" to match the source.

`#42 PASS` — vascular stiffening → diastolic rises. Both binaries legended, and both legends'
spellings match their answers. Grounded verbatim.

`#43 PASS` — marrow → fatty tissue. Single blank forced by the stem; no absolute, so no R16
exposure. "progressively" correctly removed as ungrounded.

`#44 PASS` — respiratory direction panel. The best-built card in the batch. Every one of the
four rows carries `::increases or decreases`; the classify lead-in is honest, which is R22's
exemption rather than a dodge. Count 4 = 4 clozed, and the list is verified complete against
mark 44's full sentence. The one INCREASE (airway size) mixed with three decreases is exactly
the yield, and it is fair only because every row is legended — and every row is.

`#45 PASS` — vital capacity definition. c2 = 5 words. Deliberately split from #46 so no card in
the batch shows a bare parenthetical gloss beside a hidden "vital capacity" (R3).

`#46 PASS` — age 75 → 50% vital capacity. Verbatim; both blanks form-hinted; `numeric` +
`needs_human_check` correctly set.

`#47 PASS` — five upper-airway protections. The count correction from three to five is the
single best catch of the unit edits: the same passage names cilia and airway sensation, and
"which three of the five?" was unanswerable-cold. Now 5 stated = 5 clozed, all verbatim.

`#48 PASS` — aspiration + airway obstruction. Cohesive two-member set; the stem anchor is
substantial. Its stem names the category, not the five members, so it does not leak #47.

`#49 PASS` — taste and smell. c1 groups *salty* + *sweet* so neither is free, and the answer
universe (taste qualities) is closed — R9's must-not-over-flag. "less sensitive" correctly left
visible: clozing a direction whose consequence is printed beside it would be a freebie.

`#50 PASS` — peristalsis two-way definition. c2 tightened to 6 words with "intestinal
contractions" left visible as the anchor. c3 carries its mandatory forced-choice.

`#51 PASS` — peristalsis consequences. Re-anchored opener ("Age-related change in peristalsis")
correctly refuses to print #50's c3 answer on an adjacent front. Slot-label hints `::bowel` /
`::appetite` are form-labels, not leaks, and without them the blank is genuinely open.

`#52 PASS` — intestinal blood flow 50%. Verbatim. The Back Extra names the renal collision
*without printing the renal digits*, so it does not hand #53 its answer.

`#53 PASS` — kidney 20% / up-to-50%. Both under c1 is correct: separate numbers would let
elimination solve each, and with one-word spans each blank is cued by its own frame (size vs
filtration), not by the other. `from_idx` correctly widened to `[50, 51]` for the nephron
material in the Back Extra.

`#54 PASS` — renal consequences. Count 2 = 2 clozed; each blank cued by its own tail. The
`Mechanism:` line closes the *nephron* prerequisite used on #53's back.

`#55 PASS` — brain weight at 80. Age and percentage on **separate** numbers is right here (an
age and a percentage cannot solve each other by elimination), so the asymmetry with #53 is
principled, not sloppy.

`#56 PASS` — metabolic rate unchanged. The concessive frame was correctly stripped: *although X
declines, Y remains ___* resolved to "unchanged" by grammar alone. Now a clean three-way forced
choice that preserves the valuable trap of guessing "decreased".

`#57 PASS` — subdural mechanism. Un-clozing *meninges* is right: it converts a near-given blank
into the anchor that makes `c2::bridging veins` genuinely forced. Fully grounded in mark 52's
context, which runs past the highlight to "may go unnoticed for some time."

`#58 PASS` — geriatric subdural vignette. The overturned leak is properly fixed: the front no
longer prints *shrinkage* or *bridging veins*, which are #57's two answers, and the reasoning
is no longer done for him in the stem. The 6-word span is a deliberate R22 call (the unit of
knowledge is the whole idea, not the word "unnoticed") and sits well under the 9-word alarm.
Vignette exemplar is fresh across all eight units.

---

## Sweeps that came back clean (recorded so they are not re-run)

- **Mark coverage:** 52 of 53 marks carded. The one uncarded mark is **18** (`FIGURE 7-2
  Fontanelles.`) — a caption pointer whose margin comment asks for a *picture*, not a card.
  Correctly a deliberate non-card, but see TOP FINDINGS #2.
- **R14 layout:** zero single-`<br>` separators anywhere in the batch.
- **HTML:** only `<b>`, `<i>`, `<br>`. No `<img>` yet (figure stage has not run).
- **Source-artifact words:** none. (Two Back Extras use "below" comparatively — "dips below
  98°F", "20 mm Hg below the adult floor" — which is ordinary English, not a source-position
  reference.)
- **Back Extra vocabulary:** every labelled line uses a blessed label; every card has at least
  one; all components separated by `<br><br>`.
- **Word cap:** #4 (71), #21 (70), #22 (80) exceed 60 words but are all list cards, which
  card-rules #6 and Parker's "big lists stay whole" exempt. No prose card is over.
- **`visual_source` shape:** all seven carriers are canonical **dicts**. Unit A's warning about
  bare strings crashing `attach_figures.py:307` does not apply — nothing to normalise.
- **Cross-unit R2/R6:** no duplicate claim across blocks, and no card's answer is spelled out as
  a definition or `Ex:` on a sibling's front. The apparent hits are all benign: a term visible on
  a sibling *without* its definition (fontanelles, vital capacity, peristalsis, atherosclerosis),
  coincidental identical strings ("6 months" as a congestion window vs a TABLE 7-2 milestone), and
  Back Extra lines that are shown only after answering.
- **`needs_human_check` derivations:** every `numeric: true` card with the flag off carries a
  `verified_against`, which is exactly the documented derivation `(numeric or weak grounding) and
  not verified_against`. The unit-file → chapter-file changes are the derivation working, not
  drift.

---

## TOP FINDINGS

**1. `#38` teaches an unqualified mortality rule that this same chapter contradicts, and two
editors flagged it for consolidation, which then dropped it.**
The card says "All age groups younger than 44 years → unintentional injury"; p688 (mark 6's
context) says the leading cause of death for the neonate and infant age group is congenital
abnormalities. Unit B's editor and unit F's editor each recorded the collision and each
correctly declined to assert it from their own marks, both asking for a cross-linking
`Distinguish:` line. It was never added. The fix is grounded entirely in this chapter's
existing highlight set — exact replacement text and the `from_idx` widening are in the `#38`
entry above. **The only card-level change this batch needs.**

**2. Parker's own margin request on mark 18 is about to be half-delivered, silently.**
He wrote: *"I want to see if you can add a high-quality screenshot … into the flashcards
relating to the fontanelles"* — plural. Unit C's editor verified against the real matcher code
that **only card #17 can ever be proposed**: `match_figures.score()` computes coverage from
cloze *answers* only, so #17 scores 0.375 against FIGURE 7-2 while **#18 and #19 both score
0.00** and are blocked outright by the R19 zero-coverage rule. They cannot be reached by
lowering a threshold; they must be **force-attached**. Nothing at chapter level carries this
forward — it lives only inside a unit EDIT file — so the default outcome is one fontanelle card
with the picture and two without. `parker-preferences.md` requires margin comments to be honored
end to end. Decide it explicitly at the figure stage, and say so at hand-off. (Related, same
stage: unit H verified FIGURE 7-14 → card #57 sits at page distance 2, *exactly* at
`--max-page-dist`; any tightening makes that match vanish without a message.)

**3. `check_cards.VALUE` still misses hyphenated ages, so R24 does not deliver what R24 says it
delivers.** R24 was written **today**, during this run, by two unit editors, and its stated
MUST-CATCH includes "an age in months/years/weeks/days." Verified against the live regex:
`2-month-old` → False, `30-year-old` → False, `82-year-old` → False, because the unit branch
requires `\d+\s*` immediately before the unit word and a hyphen breaks it. Batch impact is nil
— the three instances (#10, #6, #58) are invented vignette ages with no source digit to verify,
and #6 is flagged anyway via `140 beats/min` — but the hole is live for any future card stating
a real threshold in the form the book uses constantly ("a 65-year-old patient"). One-character
class fix to the separator, plus an `r24_hyphenated_age` case in `test_regressions.py`.

**4. The one disclosed inference in the batch reached Parker with its flag stripped, exactly as
its editor predicted.** Card #20's Back Extra asserts *"teething accounts only for a low-grade
fever, so a higher fever in an infant is not explained by teething"* — an entailment, not source
text. Unit C's editor set `needs_human_check: true`, foresaw that `verify_report.py` would
re-derive it to false (EXACT grounding, no digits), and wrote: *"if the orchestrator wants
Parker's eyes on it, it needs surfacing another way."* It was cleared, and `chapter_7_VERIFY.md`
Section A does not list it. The inference is clinically sound and standard, so this is a
reporting gap rather than a content error — but it is the same shape as R24 ("the flag was
reporting safety it was not delivering"), and the derivation `(numeric or weak grounding) and
not verified_against` has no channel for *disclosed inference*. Add card #20 to Section A by
hand for this chapter; consider a `disclosed_inference` input to the derivation before Chapter 8.

**5. Worth telling Parker at hand-off (not a defect):** the textbook contradicts itself on p683,
saying a respiratory rate of **60 breaths/min** is "usually normal for an infant" while TABLE
7-1 caps infant respirations at 50 and puts 60 only in the neonate band. The editor removed the
digit from card #6 rather than teaching it, which is right — but Parker will read that sentence
himself, and he should know the grid governs.
