# Unit H — older adult digestive, renal, nervous (marks 47–52)

10 notes drafted. `check_cards.py` runs clean (0 hard, 0 warnings) against
`chapter_7_highlights.json`. Recall-heavy chapter, so the mix is definition /
number / mechanism, with exactly ONE application vignette (mark 52), per the
brief and `profiles/emt.md` §2.

## Rule 0 pass (connected marks)

- **47 + 48 + 49** are three consecutive sentences of ONE paragraph under the
  *Digestive System* heading. They are NOT parallel legs of a single point —
  they are three independent mechanisms (flavor perception, motility,
  absorption). Synthesizing them into one card would be the "cram unrelated
  facts" failure guardrail in Rule 6, so they stay separate. The umbrella
  sentence ("age-related changes in gastric and intestinal functions may
  inhibit nutritional intake and utilization") is carried as the `Why:` line on
  the mark-47 card rather than carded on its own.
- **50 + 51 (renal tail)** are one passage split across two context windows.
  Mark 50's context is truncated at "…a decrease in blood supply to the", and
  the rest of the renal paragraph (nephrons, waste, fluids) lives inside mark
  51's context. The renal-consequence card therefore cites `from_idx [50, 51]`
  — that is honest provenance, not padding, and it is what makes the grounding
  check resolvable.
- **51 + 52** are connected (52's mechanism depends on 51's shrinkage) but are
  different card jobs: 51 is the quantitative fact, 52 is the clinical
  mechanism. Kept separate; not cross-linked in Back Extra, deliberately (see
  "leak watch" below).

## Fact pass

### Mark 47 — taste / flavor (1 note, 2 cards)
- MUST-TEST: taste buds less sensitive to **salty and sweet** (arbitrary, must
  be memorized); food bland/flavorless because **smell** fades along with taste
  (the non-obvious half — flavor loss is not taste buds alone).
- SUPPORTING → Back Extra: tooth loss makes chewing harder; decreased saliva
  impairs breakdown of complex carbohydrates; gastric acid secretion diminishes.
  None of these three is inside the yellow span, so they teach on the back
  rather than becoming unhighlighted cards.
- Direction ("**less** sensitive") is left visible, not clozed: "bland and
  flavorless" is right there in the stem, so a direction blank would be a
  freebie (Rule 3 leak). No forced-choice hint is owed on a blank that does not
  exist.
- "taste" could not be co-clozed with "smell" — "taste buds" sits visible in the
  same sentence, which is a literal answer-in-stem leak. Only "smell" is hidden.

### Mark 48 — peristalsis (2 notes, 4 cards)
- Two-way definition + the aging change on one note (`c1` term / `c2` meaning /
  `c3` direction). R3 handled: the parenthetical definition is not left visible
  beside a hidden "peristalsis" — it is `c2`, i.e. the blessed two-way shape
  where the meaning IS the anchor for the name-it card.
- `c3` (`slows`) carries the required forced-choice hint `::speeds up or slows`,
  and it sits on the definition note **on purpose**: consequences are NOT on
  that card, so nothing visible implies the direction. Putting `slows` on the
  consequence card would have been a giveaway (constipation implies slowing).
- Consequences (constipation and/or suppressed feelings of hunger) are their own
  grouped note. Both blanks carry slot-label hints (`::bowel`, `::appetite`) —
  without them the second blank is open-set (bloating / distension / nausea all
  fit "slowed peristalsis can cause ___"). The hints name the category, not the
  content or the direction.

### Mark 49 — intestinal blood flow (1 note, 2 cards)
- MUST-TEST: **50%** drop in intestinal blood flow; **vitamins and minerals**
  are what stops being extracted. Clozed as two paired one-word blanks so the
  pair is forced rather than open ("nutrients", "calories" would otherwise fit).
- `numeric: true` / `needs_human_check: true`.
- **Interference flagged:** three different 50%s live within ~15 lines of this
  chapter (intestinal blood flow 50%, renal filtration up to 50%, and mark 50's
  20%). The Distinguish line names the collision without printing the renal
  digits, so it does not hand mark 50's card its answer.

### Mark 50 — kidneys (2 notes, 2 cards)
- Both numbers (**20%** size, **up to 50%** filtration) are under the **same**
  cloze number so they hide together. Separate numbers would have made each a
  coin flip by elimination — see it is 50, therefore the other is 20.
- The age span "20 to 90 years" is left visible as the frame, NOT clozed. It is
  the range over which the change is measured, not an independently testable
  fact, and clozing it would collide with the *other* age span in the same
  paragraph (nephron count declines between 30 and 80). Recorded here as a
  deliberate call, not an omission.
- Cause (decreased blood supply to nephrons; nephron number falls between ages
  30 and 80) → Back Extra of the numbers card, which is already numeric-flagged
  so the 30/80 digits ride under a `needs_human_check`.
- Consequence (less able to remove waste, less able to conserve fluids) gets its
  own note. Framed as "in two ways" with the two capabilities clozed as the
  units of knowledge, so it is not the R22 filler-word shape.
- **NOT carded, deliberately:** the book's own gloss "Nephrons filter blood
  within the kidney." It is unhighlighted context and no card of mine leans on
  the term in its Text, so Rule 11 prerequisite closure is satisfied by keeping
  it in Back Extra. If the consolidation stage decides Chapter 7 wants a nephron
  definition card, this is where it would come from.

### Mark 51 — brain weight (2 notes, 3 cards)
- **80** years and **10% to 20%** are separate cloze numbers here (unlike mark
  50): they are different *kinds* of number — an age vs a percentage range — so
  there is no elimination shortcut between them.
- `numeric: true` / `needs_human_check: true`.
- The unchanged-despite-shrinkage fact earned its own note, as the brief
  suggested: metabolic rate and oxygen consumption **remain unchanged** while
  the brain shrinks and motor/sensory networks slow. Forced-choice hint
  `::increased, decreased, or unchanged` — the third state is offered because
  "no change" is genuinely possible here and is in fact the answer.
- Motor/sensory slowing is left visible as the contrast that makes "unchanged"
  surprising, rather than clozed as an obvious direction blank.

### Mark 52 — geriatric subdural (2 notes, 3 cards) — highest yield in the unit
- Built from the brief's VERIFIED BLOCK. Mark 52's own `context` field does in
  fact carry the full tail through "may go unnoticed for some time", so the
  verified block and the mark agree and the grounding check resolves against the
  mark itself.
- Mechanism/causal-chain card (recipes §7): `c1` hides **shrinkage** + the
  **meninges** together (each blank is cued by its own frame, not by the other,
  so it is not an R10 husk), `c2` hides **bridging veins** — the payoff blank.
- The "throughout life the cranial vault holds virtually no empty space
  (brain + meningeal layers + CSF)" baseline is the `Distinguish:` line rather
  than a card. It is the contrast that makes the geriatric change meaningful,
  not an independently testable fact, and putting it in the Text pushed the card
  to 47 words for no recall gain.
- The field pearl (**bleeding may go unnoticed for some time**) is tested — it
  is the single cloze on the paired application card, so it is the recall, not
  scenery.
- The application card uses a fresh exemplar (82-year-old, cabinet door) that
  appears nowhere else in the unit (Rule 13).
- **FIGURE 7-14 is wanted on both mark-52 cards.** Both Texts use "brain",
  "shrinkage", "meninges" and "bridging veins" so the matcher finds them.

## Leak watch — one item for the consolidation / judge stage

The mark-52 application card shows "tear bridging veins" in plain text, which is
the hidden `c2` answer of the mark-52 mechanism card. Judged acceptable and left
in: the two cards test different things (name the torn structure vs. recognize
the delayed presentation), the vignette needs that clause to be coherent, and
the brief requires the phrase for the figure matcher. Flagging it rather than
hiding it — if the judge disagrees, the fix is to reword the vignette to
"tear the veins that span that space" and accept a weaker figure match.

## Coverage

Every mark is carded; nothing dropped, nothing flagged as un-cardable.

| mark | notes | Anki cards |
|---|---|---|
| 47 | 1 | 2 |
| 48 | 2 | 4 |
| 49 | 1 | 2 |
| 50 | 2 | 2 |
| 51 | 2 | 3 |
| 52 | 2 | 3 |
| **total** | **10** | **16** |

## For the next stage

- `needs_human_check: true` on 3 notes (marks 49, 50, 51) — every percentage and
  age in the unit. Digits to verify against p723–p724: 50% (intestinal blood
  flow), 20% + up to 50% (kidney size + filtration, ages 20 to 90), ages 30 to
  80 (nephron count, Back Extra only), age 80 + 10% to 20% (brain weight).
- No card in this unit is built on a table or figure, so none carries
  `visual_source`; all six marks are `needs_visual: false`.
- Dedupe check against neighbouring units: unit G (marks 40–46) covers older
  adult cardiovascular, hematologic and respiratory changes. No overlap of claim
  with anything here.
- An etymology hook for peristalsis (*peri-* around + *-stalsis* contraction) was
  considered for that card's Back Extra and left out because it is not in the
  source context. Parker's Chapter 5 deck already teaches *peri-*, so the editor
  may want to add it back as a `Cue:` line.
