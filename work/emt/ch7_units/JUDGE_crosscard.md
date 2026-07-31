# Chapter 7 — cross-card judge (whole-batch pass)

Independent read of all 59 shipped notes in `work/emt/chapter_7_cards.json` with the whole
chapter in view. Lens: defects that only exist *between* cards. Nothing was modified.

Also run for corroboration: `check_cards.py … --highlights chapter_7_highlights.json` →
59 cards, 0 hard errors, 3 warnings, **all three already cleared in writing by the unit
editors** (#4 R15 row-label — unit A; #34 husk — unit E; #0/#1 86% similar — unit A). The
mechanical near-duplicate detector surfaces nothing new.

**Tally: 0 SHIP-BLOCKER · 3 SHOULD-FIX · 2 NOTE.**

---

## 1. R6 cross-card give-away — cards **27** and **32** print card **4**'s hidden answers · SHOULD-FIX

Card 4 is the chapter's single hardest recall: nine age bands, **all nine spans under one
`c1`**, so the front is nine simultaneous blanks.

> `[4]` `The nine life-span age groups and the ages each one covers:` …
> `Preschool age — {{c1::3 to 6 years}}` … `School age — {{c1::6 to 12 years}}`

Two of those nine answers sit in plain, un-clozed stem text on other cards:

> `[27]` `By the end of the preschooler stage **(3 to 6 years)**, a child's brain weighs roughly {{c1::90%::percentage}} of its adult weight.`
>
> `[32]` `Each year a school-age child **(6 to 12 years)** gains about {{c1::4 pounds (2 kg)::weight}} and grows about {{c2::2.5 inches (6 cm)::height}}.`

This is visible-stem, not Back Extra, so it is the strong form of the leak: in a shuffled
megadeck two of card 4's nine rows arrive pre-answered, and card 4 feels learned before it is.

The parentheticals are pure scenery on their own cards — card 27's answer is `90%`, card 32's
are `4 pounds` / `2.5 inches`; neither blank needs the band to be forced, and `preschooler
stage` / `school-age child` already name themselves (rule 11 is satisfied by card 4 itself as
the sibling definition card).

That this is a cross-unit blind spot is confirmed by unit F, which hit the *identical* pattern
and reasoned it out correctly: *"If unit A produces a card whose answer is '12 to 18 years',
these are Back Extra lines shown only after answering, so there is no cross-card give-away"*
(`F_adolescent_adult_EDIT.md` §4). Unit F kept its band in the Back Extra; unit E put two in
the stem. Neither editor could see the other.

**Fix (both free):**
- Card **27** — delete `(3 to 6 years)` from `Text`.
- Card **32** — delete `(6 to 12 years)` from `Text`.

If the band is wanted as context, move it to Back Extra on each, per unit F's precedent.

---

## 2. Contradiction — card **41** Text vs card **0** Back Extra: does the older adult's pulse fall or not? · SHOULD-FIX

> `[41]` Text: `Beyond atherosclerosis, aging weakens the older adult's heart in three ways:` `{{c1::the heart rate decreases}}` …
>
> `[0]` Back Extra: `Pitfall: age cuts both ways — a neonate's ceiling of 180 beats/min is baseline rather than distress, while **an older adult gets no allowance at all and is held to the same 60 to 100 as a 20-year-old**.`
>
> `[5]` Text: `As a person gets older, pulse rate and respiratory rate {{c1::decrease::increase or decrease}}…`

Both poles are the book's own: p721 prose (mark 42, verbatim *"Additional cardiovascular
effects of aging include a decrease in heart rate"*) against TABLE 7-1, which gives adolescent,
early, middle and older adult the identical 60–100 band. In one shuffled deck they read as a
flat contradiction, and card 0's *"gets no allowance at all"* sharpens it into an explicit
denial of what card 41 asserts.

**No card reconciles it.** Unit G saw the tension and deliberately avoided *worsening* it —
*"phrased as baseline change rather than 'lower than a young adult's' — TABLE 7-1 gives the
older adult the same 60–100 beats/min band, so the stronger claim would contradict the
chapter's own table"* (`G_older_cardioresp_EDIT.md`) — but the `Distinguish:` line it shipped
on cards 40 and 41 resolves *baseline vs stress response*, a different question. Unit G could
not see card 0's Back Extra; unit A could not see card 41.

Note the contrast with the parallel case one column over: unit A **did** reconcile the same
shape for blood pressure, on card 5's Back Extra — *"systolic pressure stops rising once it
reaches 90 to 130 in early adulthood and is identical in middle and older adults, so a high
reading in a 70-year-old is a finding, not an age effect."* Pulse got no equivalent.

**Fix:** append one digit-free clause to the shared `Distinguish:` line on **both** cards 40
and 41 (unit G requires the line stay word-identical on the pair — *"do not dedupe it; each
card must carry it to survive shuffling"*):

> `Distinguish: the age-related drop in heart rate is a baseline change **that stays inside the adult range — an older adult's normal pulse band is the same one used for a young adult**; in a life-threatening illness the body still raises the heart rate to preserve blood pressure.`

---

## 3. Contradiction — card **9** Back Extra denies the premise card **10** runs on · SHOULD-FIX

> `[9]` Back Extra: `Distinguish: the nose-breathing rule is **stated for the neonate (0 to 1 month)**, while the heightened susceptibility to nasal congestion runs through the first 6 months.`
>
> `[10]` Text: `You are dispatched for a **2-month-old** who is reportedly choking… so you check next for obstruction of {{c1::the nasal passages::anatomic site}}.`
> `[10]` Back Extra: `Why: **neonates and young infants breathe primarily through the nose**, so mucus alone can present as a choking emergency.`

Card 9 draws a hard boundary at 1 month. Card 10 is built on a 2-month-old — past that
boundary — and its answer only works if that patient is a nose breather, which card 10 then
states outright. Same unit, same mark (6), adjacent `from_idx`, so they will sit near each
other in the deck saying opposite things.

Against the source (mark 6, p688, verbatim): *"Neonates are primarily nose breathers. Infants
younger than 6 months are particularly susceptible to nasal congestion… **If you respond to a
call for a baby choking, make sure the nasal passages are clear** of mucus and other
obstructions."* The book never says nose-breathing stops at 1 month, and it explicitly extends
the clinical action to any "baby." So **card 9's boundary is the over-claim**, not card 10's
vignette. `B_neonate_physical_EDIT.md` reworked both cards' Back Extras for a different R6 leak
and did not notice that the new `Distinguish:` invalidates its own sibling.

**Fix:** on card **9**, replace the `Distinguish:` line so it separates the two numbers without
asserting an end to nose-breathing:

> `Distinguish: the 6-month figure is the window of heightened congestion susceptibility, not the age at which nose-breathing stops.`

Leave card 10 alone.

---

## 4. Interference — the geriatric percentage cluster has three separate "50%" and only partial cover · NOTE

Five cards in the older-adult block each hide a percentage, drawn from four pages:

| card | hidden values | topic |
|---|---|---|
| `[40]` | `60%` + `65 years` (both under c1) | atherosclerotic disease prevalence |
| `[46]` | `75` + `50%` (both under c1) | vital capacity vs a young adult |
| `[52]` | `50%` | intestinal blood flow |
| `[53]` | `20%` + `50%` (both under c1) | kidney size / filtration |
| `[55]` | `80` + `10% to 20%` | brain weight |

Every stem names its own organ, so cold-solve holds on all five — this is confidence blur, not
unanswerability, hence NOTE. But the protection is uneven: card 52 carries
*"the 50% belongs to intestinal blood flow, not to the renal figures for kidney size and
filtration"* and card 53 carries *"do not swap the two numbers"* — **card 46 carries nothing**,
and it is a third `50%` that neither existing line mentions.

Unit H set exactly this trigger and could not see across the unit boundary:
*"Three 50%s live within ~15 lines of p723–724… If a later unit adds a fourth percentage from
this region, re-check the Distinguish line on #3"* (`H_older_gi_renal_neuro_EDIT.md` §5). Card
46 is that fourth, and it came from unit G at p722.

Secondary, same cluster: cards **40** and **46** share an unusually specific frame — an
older-adult figure stated as *[percentage] + [age]*, with **both** numbers under a single `c1`,
in the same block. 60/65 against 75/50 is a swap waiting to happen.

**Fix:** add a `Distinguish:` to card **46**'s Back Extra (ahead of the existing `Pitfall:`,
per the label priority order), naming the collision without printing the neighbours' digits —
the technique unit H already used on card 52:

> `Distinguish: this 50% is respiratory reserve measured at 75 against a young adult. The intestinal and renal declines carry their own separate figures — keep each number tied to its organ.`

---

## 5. R6 (Back Extra) — card **48** still recites one of card **47**'s five answers · NOTE

> `[47]` Text: `With age, five protective features of the upper airway weaken:` … `{{c1::sensation within the airway}}`
>
> `[48]` Back Extra: `Pitfall: the risk is a quiet one, because **sensation within the airway also declines** and the older adult may not register material sitting in the airway at all.`

Back Extra is post-answer, so this is the weak form of the leak and on its own it would be
tolerable reinforcement between a fact card and its consequence card. It is reported because
**the unit G editor believed it had removed it and it is still there verbatim**:
*"Back Extra reworked because the old `Why:` ('sensation within the airway also declines') is
now one of card #8's five answers and was doing double duty. Reframed as a `Pitfall:` about the
silence of the risk — the clinical read, not the item."* The label changed; the phrase did not.
Worth knowing, because an EDIT file asserting a fix that did not land is the thing a later pass
will trust.

**Fix (optional):** on card **48**, reword to keep the clinical point without naming the item —
`Pitfall: the risk is a quiet one, because the airway's own warning signals fade too, and the
older adult may not register material sitting in the airway at all.`

---

## Classes checked and clean

- **R2 duplication by meaning — clean.** All 59 recall targets are distinct. Every pair that
  looks like a duplicate is a documented, argued split: vital capacity `[45]`/`[46]`, kidney
  numbers `[53]` / renal consequences `[54]`, reflex roster `[15]` / reflex match `[16]`,
  peristalsis definition `[50]` / consequences `[51]`, five-protections `[47]` / risk `[48]`,
  the four TABLE 7-1 columns `[0]`–`[3]`, and the disjoint milestone halves `[21]`/`[22]`.
  `check_cards.py`'s near-duplicate detector agrees (its one hit, `[0]`&`[1]`, is the
  intentionally identical row skeleton of two different table columns).
- **Disputed claim 1 — infant respiratory rate of 60 — clean.** No shipped card contains
  `60 breaths`, `respirations of 60`, or the p683 prose sentence. Card `[1]` teaches infant
  25 to 50 and puts 60 only in the neonate band; card `[6]` was reworded to pulse only. The
  reasoning is recorded in `A_vitals_agebands_EDIT.md` #7 and in `chapter_7_VERIFY.md`.
- **Disputed claim 2 — "walks with minimal assistance at 12 months" — clean.** No card
  contains `minimal assistance`. Card `[22]` uses TABLE 7-2 verbatim (11 months *begins to walk
  without assistance*, 12 months *walks*) and its `Distinguish:` teaches the degree pivot. The
  mark-18 prose is not asserted anywhere.
- **Congenital abnormalities vs "younger than 44 → unintentional injury" — clean in batch.**
  Unit F flagged the possible collision with mark 6's context; unit B did not card the
  congenital fact, so no shipped card contradicts card `[38]`.
- **Age-band ladder cluster `[0]`–`[4]` — separable.** Each carries a bold header naming the
  measure *and* its unit (`pulse rate` / beats/min, `respiratory rate` / breaths/min,
  `systolic blood pressure` / mm Hg, `body temperature`, `age groups`), and the numeric
  magnitudes do not overlap between columns. No `Distinguish:` needed.
- **Milestone cards `[21]`/`[22]` — not re-raised.** `D_infant_psychosocial_EDIT.md` verified
  per-row forcing on all 11 rows, resolved the three confusable pairs (*sits upright*/*can sit
  alone*, *responds to "no"*/*responds to name*, *responds to*/*knows* + *begins to walk*/
  *walks*), and confirmed the row order is neither ascending nor descending. Its cross-card
  fix landed: card 21's `Distinguish:` says `months later` rather than naming card 22's
  9-month answer.
- **Considered and dismissed as ordinary vocabulary overlap, not leaks:** `Fontanelles` `[17]`
  visible on `[18]`/`[19]` (unit C weighed this explicitly and kept the cloze to preserve the
  FIGURE 7-2 match; the definition→term mapping is not handed over anywhere);
  `atherosclerosis` `[39]` visible on `[40]`/`[41]` (licensed two-way definition — its full
  definition is visible on its own card by design); `airway obstruction` `[48]` visible on
  `[11]`/`[12]` (different age group, generic clinical noun, and the paired answer
  *aspiration* appears nowhere else); `Peristalsis` `[50]` visible on `[51]` and
  `Vital capacity` `[45]` visible on `[46]` (both the designed anchor-card halves, argued in
  their EDIT files); `smell` `[49]` echoed in `[51]`'s Back Extra (that line is a deliberate
  interference fix and the blank is near-forced by *"fades along with taste"* regardless).
