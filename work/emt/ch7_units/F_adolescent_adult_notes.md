# Unit F — Adolescent & Middle Adult (marks 37, 38, 39)

**Output:** 5 notes → 8 Anki cards. `check_cards.py` passes clean (stamped).

---

## Fact pass

### Mark 37 — p708, adolescent growth spurt

| Fact | Verdict | Where it went |
|---|---|---|
| Growth order: hands and feet → long bones of the extremities → torso | **MUST-TEST** (the highlight) | Note 1, `c1` grouped sequence (recipes §7, arrows outside the clozes, one cloze number) |
| The spurt lasts 2 to 3 years | **MUST-TEST** | Note 1, `c2` — it sat in the visible stem of the sequence card, so leaving it unclozed would have been visible scenery (checklist #4) |
| Girls finish by about 16 y; boys peak by 18 y; boys generally end up taller | **MUST-TEST** | Note 2, grouped contrast (recipes §8) |
| Girls start earlier than boys | SUPPORTING | Note 2 Back Extra `Why:` — it is the reason behind the 16-vs-18 split, and clozing it too would have been redundant with the numbers |
| At the end of the spurt, muscle mass and bone density have nearly reached adult levels | SUPPORTING | Note 1 Back Extra `Why:` — a genuine endpoint fact, but not action-changing for EMT and not highlighted; it earns the Back Extra rather than a third blank |
| "Growth spurt = an increase in muscle and bone growth" (the book's parenthetical gloss) | **SKIP** as a card | Near-tautological (a *growth* spurt is an increase in growth); carding it would fail checklist #8 |
| Adolescent = 12 to 18 years (FIGURE 7-8 caption) | **SKIP here** — belongs to the age-band/vitals unit | Used only as Back Extra reference on notes 2 and 4 |

**Why the sex-difference facts got their own card rather than riding along visibly on the sequence card:** the brief's warning cuts both ways. Folding 16/18/taller into note 1 would have bloated a clean ordered-sequence card with facts that are not part of the sequence (Layer B #6, "don't cram unrelated facts"); leaving them visible there would have been the under-clozing trap. A separate comparison card is the only shape that respects both.

### Mark 38 — p708, menarche

| Fact | Verdict | Where it went |
|---|---|---|
| Menarche = the first menstrual bleeding | **MUST-TEST** | Note 3, two-way definition, `c2` side is 4 words |
| Some girls begin menstruating **before** adolescence, and this is *not uncommon* | **MUST-TEST** (brief: the qualifier is testable) | Note 4, its own note |
| By mid-adolescence the female body produces eggs (oocytes) | SUPPORTING | Note 3 Back Extra `Why:` |
| Other secondary sexual developments: enlargement of external reproductive organs, pubic + axillary hair, vocal changes, adipose deposit in breasts and thighs | **SUPPORTING, not carded as a list** | Note 3 Back Extra `Cue:`, kept intact as reference |

**Decision on the secondary-sex-characteristic list (the brief asked me to state this):** not carded.
Three reasons. (1) Parker highlighted only the menstruation sentence — the yellow mark is the filter, and Rule 1 governs *yellow spans*, not the surrounding prose. (2) For NREMT/field purposes it is not action-changing, and `profiles/emt.md` §5 says definitions get carded only when they change what you do. (3) Turning four items of running prose into a closed "name all four" grouped card would be a low-yield card built on an un-highlighted run. Per recipes §22(b) the list is preserved verbatim in the Back Extra as reference, so nothing is lost and consolidation can promote it to a card cheaply if it disagrees.

**Why the qualifier is a separate note instead of a `c3` on the definition note.** I drafted it as `c3` first (recipes §4 explicitly blesses a `c3` qualifier on a definition). It leaked: with `c3` present the visible tail read "…yet it is not uncommon for a girl to begin menstruating earlier," which on the **`c2` card** ("Menarche is `___`") hands over "the start of menstruation" to someone who does not know the term. Splitting the qualifier off keeps the definition note leak-free (card-rules #3).

### Mark 39 — p717, leading cause of death

| Fact | Verdict | Where it went |
|---|---|---|
| Younger than 44 y → unintentional injury (visible half of the sentence) | **MUST-TEST** — it is what makes the highlighted half answerable | Note 5, `c1` |
| Ages 45 to 64 → cancer (the highlight) | **MUST-TEST** | Note 5, `c2` |
| Middle adults: rising cholesterol, decreased cardiac efficiency, weight-control difficulty, often-undiagnosed diabetes and hypertension | SUPPORTING | Note 5 Back Extra `Cue:` |

**The cold-solve fix the brief asked for, and why it is `c1`/`c2` and not one shared number.** Recipes §8 defaults to putting both contrast values under the *same* cloze number. That default fails here: if both halves hide together, each row's only cue is its bare age band, and "the leading cause of death in persons 45 to 64 is `___`" is close to open-set — *heart disease* is a perfectly reasonable wrong answer for a knowledgeable person. Under `c1`/`c2` each generated card shows the other half as the anchor, so the question becomes "what takes over from unintentional injury in the mid-40s" (forced → cancer) and "what does cancer displace below 44" (forced → unintentional injury). That is card-rules #17's GOOD pattern, and the cold-solve gate outranks a recipe default.

---

## Merges, layout and flags

- **No marks merged.** Rule 0 was run: 37 and 38 are adjacent on p708 and share a paragraph run, but they are two different ideas (skeletal growth order vs. reproductive milestone), not one idea in two spans. 39 is nine pages later. Merging any of them would have been the "cram unrelated facts" failure.
- **Every mark is covered by a card.** 37 → notes 1–2, 38 → notes 3–4, 39 → note 5. Nothing flagged as uncardable.
- **R14 layout:** notes 1 and 5 are row-shaped and use `<br><br>` between rows. Note 1's arrow chain is a single line per recipes §7 (arrows visible, outside the clozes, all steps on `c1`).
- **Numeric flags:** notes 1, 2, 5 carry ages/durations in the Text → `numeric: true`, `needs_human_check: true`. Note 4 is flagged too even though its *Text* holds no digits — its Back Extra asserts the 12-to-18 age band and the claim itself is age-relative, so it deserves the same human glance. Note 3 (pure definition) is the only unflagged card.
- **No figure is needed or wanted for this unit.** None of marks 37–39 is `needs_visual`; there is no `visual_source` on any card. (The p708 FIGURE 7-8 adolescent photo is a stock portrait, not information — if the figure matcher offers it, it is a "congruent but empty" case and I would let the judge decide; nothing here depends on it.)

---

## For the consolidation stage

1. **Potential contradiction with unit B, worth one deliberate decision.** Mark 6's context (p688, unit B) states that *"the leading cause of death for the neonate and infant age group is congenital abnormalities (ie, birth defects)."* My note 5 says the leading cause below 44 is unintentional injury. Both are the book's own words from different pages, and read side by side in one shuffled deck they look like a conflict. That fact is **not** in my marks' context, so per the brief I did not assert it anywhere. If unit B cards it, consolidation should add a cross-linking `Distinguish:` line to one or both cards (neonates/infants are the carve-out to the under-44 rule). Flagging rather than fixing, because fixing it would require asserting a fact outside my grounding.
2. **Age band 12–18 appears in the Back Extra of notes 2 and 4** as reference. If the age-band/vitals unit (A) produces a card whose *answer* is "12 to 18 years," check for a cross-card give-away (checklist #16) — I believe there is none, since these are Back Extra lines shown only after answering, but it is the one place my unit touches another's answer space.
3. **Word "milestone" appears in notes 3 and 4** as the shared framing. Deliberate (they are the same topic seen from two sides), but if the similar-Text warning fires in the merged batch, that is why.
4. No scenario/vignette card was drafted. This is a recall-heavy chapter and the brief plus `profiles/emt.md` §2 both say not to force vignettes onto developmental facts; none of these three facts changes field management in a way a vignette would sharpen.
5. A `.verified` stamp exists next to this unit's cards file from the unit-level gate run. It is keyed to this file's hash and will not carry over to the merged file — re-run `check_cards.py` after consolidation as normal.
