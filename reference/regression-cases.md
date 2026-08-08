# Regression Cases — the failure library (tests, not just rules)

Every flaw Parker has caught becomes a permanent test here: a **BAD** card the checks must catch, and (where over-correction is a real risk) a **GOOD** card they must *not* flag. When `card-rules.md`, `check_cards.py`, or the LLM judge changes, re-validate against these so nothing regresses. This is how "I hope it doesn't recur" becomes "it can't — there's a test for it."

**The mechanically-catchable cases are EXECUTABLE:** run `python3 scripts/test_regressions.py` after any change to `check_cards.py` or a rule a detector implements. It runs the real checker over embedded BAD/GOOD exemplars for R2/R3/R7/R10/R10b/R11 and fails loudly on any regression, in either direction (missed catch OR over-flag). Semantic-only classes (R9 open-set) stay with the LLM judge.

---

## R1 — Under-clozing: a must-test fact left as visible scenery
**Rule:** card-rules #7 + editor check #4. **Caught by:** the fact pass + the LLM judge (code can't see this).
- **BAD:** `{{c1::Public health}} examines the needs of {{c2::entire populations}}, with the goal of preventing health problems.` — the GOAL is never tested.
- **GOOD:** `… with the goal of {{c3::preventing health problems}}.` — every must-test fact clozed.
- **Catch test:** list the testable facts in the source; assert each is clozed by some card.

## R2 — Over-clozing / cross-card duplication / over-fragmentation
**Rule:** card-rules #12 (dedupe by meaning) + Stage 2.5 global consolidation. **Caught by:** `check_cards.py` near-duplicate warning + the consolidation stage.
- **BAD:** online medical control split into 9 near-identical cards across 2 units; "licensure is the legal authority to practice" carded verbatim twice; 76 cards from 36 highlights.
- **GOOD:** one definition + at most one feature/vignette per concept; 33 cards from 36 highlights.
- **Catch test:** no two cards test the same fact; no concept fragmented into >2 cards.

## R3 — Leak / crutch: the hidden answer's definition is VISIBLE
**Rule:** card-rules #3. **Caught by:** `check_cards.py` parenthetical-after-cloze + literal-answer-in-stem warnings → the LLM judge's isolation test (editor #15).
- **BAD:** `…{{c1::licensure}} (state authority granted)…` — the parenthetical defines the hidden answer, so Parker decodes instead of recalls.
- **GOOD:** `The pathway… runs in order: {{c1::certification}}, then {{c1::licensure}}, then {{c1::credentialing}}.` + the definitions in the Back Extra.
- **MUST NOT OVER-FLAG (the precision):** `{{c1::Licensure}} is {{c2::the legal authority to practice}}` — a two-way definition (both halves clozed) is NOT a leak. The checker must allow it.
- **Catch test (both ways):** flag a card where the hidden answer's definition sits in visible text; do NOT flag a two-way definition.

## R4 — The collision: a leak-fix that re-creates under-clozing
**Rule:** card-rules #3 precision. **Caught by:** the fact pass re-run after any rewrite.
- **BAD (naive leak-fix):** strip the EMR scope from the stem → dump it in the Back Extra → the scope is now untested.
- **GOOD:** re-test the moved fact as a two-way definition: `The {{c1::emergency medical responder (EMR)}} is trained to {{c2::manage the scene and start lifesaving care before the ambulance arrives}}.`
- **Catch test:** when a rewrite removes a fact from a cloze, assert that fact is still tested somewhere.

## R5 — The AI process failures (the meta-layer Parker named)
- **Overconfidence** — declaring a "full-system rebuild" without running the editor. → Verification is a mandatory harness, not a claim.
- **Shortcuts** — using a rule ("such as → don't card the list") as permission to skip thinking, leaving the AEMT skills untested. → The fact pass forces an explicit must-test / skip tag on every fact.
- **Context-overwhelm** — hand-crafting 27 cards in one context window. → Decompose: one unit per agent + independent editor + global consolidation.

## R6 — Cross-card give-away (a scenario card answered by its sibling)
**Rule:** card-rules #13 + editor check #16. **Caught by:** the LLM judge (needs cross-card view; code can't see intent).
- **BAD:** a "classify this contact route" card whose two scenarios (blood into a cut = direct; contaminated stretcher = indirect) are the *exact* `Ex:` lines on the direct/indirect definition cards in the same batch — the student pattern-matches the neighbor.
- **GOOD:** the same classify card with FRESH exemplars (weeping skin lesion = direct; reused stethoscope = indirect) that don't appear on any sibling.
- **Catch test:** a scenario card's answers must not be spelled out verbatim as examples/definitions on another card in the batch.

## R7 — List undercount (tested items < the real source list)
**Rule:** card-rules #14 + editor check #17. **Caught by:** `check_cards.py` count-vs-clozed-items undercount warning + the fact pass re-read against the full page.
- **BAD:** "consider 7 factors" clozing 7, when the textbook lists 8 (the 8th sat on the next page, past the extractor's context window). On a card Parker marked "Know all of these!!".
- **GOOD:** all 8 factors clozed; the extractor now appends the next page for any `list_lead_in` highlight so the whole list is in context.
- **MUST NOT OVER-FLAG:** a genuine branch — "the 3 stages: alarm, resistance, recovery **or** exhaustion" clozes 4 spans for 3 stages. An *overcount* is a safe branch, not a bug; the checker only warns on *undercount*.
- **Catch test:** stated count == number of clozed list items, verified against the full source page(s), not just the context paragraph.

## R8 — Scenario→action fuzzy cloze (a whole sentence hidden)
**Rule:** card-rules #15 (+ rule 5 crisp-cloze) + editor check #6. **Caught by:** the LLM judge (semantic; a long cloze span isn't always wrong, e.g. a real list).
- **BAD:** `you should {{c1::Park a heavy vehicle, such as a fire engine, so it blocks traffic in that lane}}` — an un-recallable sentence-length blank.
- **GOOD:** `physically shield the scene by parking a {{c1::heavy vehicle::what}} upstream to block the lane` — crisp keyword, situational stem visible, the fire-engine example moved to Back Extra.
- **Catch test:** in a scenario/next-action card, the hidden span is 1–3 load-bearing words, not the whole action clause.

## R9 — Open-set cloze (answer is one of an unbounded universe)
**Rule:** card-rules #16 + editor check #18. **Caught by:** the LLM judge + the cold-solve test (code can flag a proxy, not the concept).
- **BAD:** `A patient tells you her religious convictions strongly oppose {{c1::medications, blood, and blood products::3 items}}. Beyond respecting her wishes, you must {{c2::report the objection to the next level of care::action}}.` — a religion could oppose countless things and many EMT actions fit the second hole; nothing visible forces *these* answers. Parker: "there are so many things that could fit in that hole… impossible to answer without having first seen the answer."
- **GOOD:** anchor the entity so the answer is forced — `A {{c1::Jehovah's Witness::faith}} patient will typically refuse {{c2::blood and blood products}}, so you honor the refusal and ensure the objection is documented and handed off with care.` (name the faith → the refused items are forced; put the situation in view → the action is forced).
- **MUST NOT OVER-FLAG:** a genuinely closed taxonomy the source names — "the three types of shock are…" — is answerable-cold and stays. The defect is an *open* answer-space, not a *hard* one.
- **Catch test:** cover the answer; a knower must be able to produce exactly it from the visible stem. If the blank is "one of many true things," fail.

## R10 — All-blanks-at-once husk (mutually-dependent co-cloze under one number)
**Rule:** card-rules #17 + editor check #19. **Caught by:** `check_cards.py` husk warning (blanked words ≥ visible words in a single multi-deletion group) + the judge.
- **BAD:** `The lawsuit defense of {{c1::governmental immunity}} generally applies only to EMS systems operated by {{c1::municipalities or other governmental entities}}.` — both halves are c1, so the front is "the ___ of ___ applies only to systems operated by ___"; each blank's only cue is the other, also hidden. Parker: "how am I supposed to guess both at the same time… I had no chance."
- **GOOD:** number them c1 and c2 → two cards; each shows one span as the anchor and tests the other. Card A: "governmental immunity … operated by {{c2::municipalities or other governmental entities}}." Card B: "{{c1::governmental immunity}} … operated by municipalities or other governmental entities."
- **MUST NOT OVER-FLAG:** a genuine cohesive *list* under one number (SAMPLE's 6 items, the 8 medical-necessity scenarios) is correct grouped-reveal — those items are parallel members of ONE set, not two spans that define each other. The husk is specifically *mutually-dependent* spans whose removal guts the stem.
- **THE JUDGE (not the checker) clears multi-dimensional contrast (added 2026-07-19):** a two-sided contrast card that hides the differing VALUES under one number while the ENTITY anchors stay visible — `When you need protection, {{c1::cover::term}} is the tactical use of {{c2::an impenetrable barrier}}, whereas {{c1::concealment::term}} only {{c2::hides you from view}}` — is answerable (blank c2 → cover/concealment anchor it; blank c1 → the definitions anchor it), so it is NOT a husk. But `check_cards.py husk_groups` is deliberately GENEROUS and MAY flag it: suppressing every multi-number card would risk a false negative (a real husk that merely coexists with an unrelated cloze — the costly error on the class Parker rants about). So the checker over-flags and **editor check #19 (the LLM judge) is what clears the benign ones** — cover the group, and if a sibling cloze number or a visible entity anchor makes each blank answerable, PASS it. Do not "fix" a genuine contrast card into split singletons.
- **Catch test:** cover everything under each single number; if the visible remainder is mostly connective scaffolding AND no sibling cloze/anchor helps, it's a husk — re-number. Otherwise PASS.
- **R10b — synonym-equation husk (the shape the word-count proxy misses).** `{{c1::Off-line}} = also called {{c1::indirect}}<br>{{c1::Online}} = also called {{c1::direct}}` — every term of both synonym pairs is under c1, so the c1 card reads "___ = also called ___ / ___ = also called ___": both sides of each identity are hidden at once. The spans are *short* (one word each) so the multi-word husk proxy skips it; the giveaway is that a synonym/identity connective (`=`, `also called`, `also known as`, `aka`, `stands for`) ends up flanked by two blanks. **GOOD:** renumber to c1/c2 and c3/c4 so each card shows one side as the anchor and tests its synonym. **MUST NOT OVER-FLAG:** an acronym card (`SBAR stands for {{c1::Situation}}…`) keeps the acronym VISIBLE, so only one blank flanks "stands for" — not a husk; a two-way def (`{{c1::X}} is {{c2::Y}}`, different numbers) shows one side per card — not a husk. *Caught by:* `check_cards.py` `equation_husk_groups` (a synonym connective flanked by two same-number blanks) — added 2026-07-19 after the Chapter 1 audit found the off-line/online card the word-count proxy had missed.

## R11 — First-letter hint on a non-mnemonic list (giveaway copout)
**Rule:** card-rules #18 + editor check #20. **Caught by:** `check_cards.py` first-letter-hint warning (hint == answer's leading letters, no spelled acronym in stem) + the judge.
- **BAD:** `Medical errors come from three sources: {{c1::rules-based failure::r}} {{c1::knowledge-based failure::k}} {{c1::skills-based failure::s}}` — `::r/::k/::s` hand over each answer; there is no acronym being taught. Parker: "your hint is a letter… that's literally giving away the answer, an easy copout."
- **GOOD:** drop the letter hints and expose the shared structure — `medical errors come from three sources: a {{c1::rules}}-based, a {{c1::knowledge}}-based, or a {{c1::skills}}-based failure.` The "-based failure" scaffold stays visible; recall is the three crisp discriminators, no letter leak.
- **MUST NOT OVER-FLAG:** first-letter hints on a real spelled mnemonic the card teaches — `<b>SAMPLE</b> history: {{c1::Signs/Symptoms::S}}…` — are licensed (the letters ARE the memory hook, and SAMPLE is visible in the stem). Only flag a first-letter hint when the stem contains no acronym those letters build.
- **Catch test:** hint equals its answer's first letter(s) AND no spelled acronym in the stem → leak.
- **Precision round (2026-07-19, independent verification pass).** Three refinements after adversarial testing of the detector itself:
  - **An unrelated acronym licenses NOTHING.** "EMT/EMS/CPR" sit in half this book's stems; `duty::D / breach::B / damages::D / causation::C` with "EMT" visible must STILL flag — the group's hint letters, joined in document order, have to actually spell INTO a stem token. (The first detector draft licensed on mere acronym presence — a false-negative hole across most of the deck.)
  - **MUST NOT OVER-FLAG — the Rx-gap:** CHART's `Treatment (Rx)::R` item breaks the contiguous letter run (C-H-A-...-T), so licensing accepts an in-order SUBSEQUENCE (≥3 letters) of the token, not just a contiguous run (≥2).
  - **BAD — co-clozed acronym:** `...version of SBAR ({{c1::SBAT::acronym}}), the final component becomes {{c1::Treatment::T}}` — the acronym is HIDDEN on the same card, so `::T` leaks its final letter (SBAR visible + "final letter T" → SBAT derivable without recall). Hidden answers are never license tokens; a lone letter never self-licenses. Fixed live: hint → `::component`.

## R12 — Bloated single blank: a fuzzy clause or an un-crisp two-way-definition c2 side
**Rule:** card-rules #5 (crisp cloze) + the definition recipe (card-recipes §4: c2 meaning side ~3-6 words) + parker-preferences ("keep the c2 meaning side CRISP"). **Caught by:** `check_cards.py` long-single-blank warning (a cloze group with exactly ONE span hiding ≥9 words) + the LLM judge. Surfaced 2026-07-19 when the full ch1-5 live audit found ~30 two-way definition cards whose c2 (name → state the meaning) side ran 8-21 words — impossible to reproduce verbatim, so the define-it direction was a guaranteed "fail cold." This is the definition-card face of R8 (fuzzy scenario cloze).
- **BAD:** `{{c1::Continuous quality improvement (CQI)}} is {{c2::a quality-management process in which team members continuously review responses to find and fix system weaknesses over time}}.` — the c2 answer is 21 words; no one recalls that string.
- **GOOD:** tighten c2 to the discriminating core and move the rest to Back Extra — `{{c1::Continuous quality improvement (CQI)}} is a {{c2::system to review and improve care over time}}.` + `Distinguish:`/`Why:` lines carrying the fuller explanation. The two-way structure is preserved; only the c2 span is crisped.
- **MUST NOT OVER-FLAG:** a genuine grouped list keeps its long items under the SAME cloze number (several spans in one group), which is NOT a single fuzzy blank — the medical-necessity scenarios (`{{c1::unconscious or in shock}}, {{c1::in acute respiratory or cardiac distress}}, …`) must stay whole (Parker's "big lists stay whole"). The checker only flags a group with exactly ONE span, so grouped lists are safe.
- **Catch test:** a single-span cloze answer is a crisp term/number/short phrase, not a whole clause; a two-way def's c2 side is a few discriminating words, not a sentence.

## R13 — Ungrounded claim: a fact that is in no source the card cites
**Rule:** card-rules Rule 1 (always ground in the page paragraph) + SKILL.md's "zero guessing". **Caught by:** `check_cards.py` grounding check (needs `from_idx` provenance) + the LLM judge. Surfaced 2026-07-29 by a post-mortem of the EMT Chapter 6 run.

This is the first MECHANICAL enforcement of the system's #1 rule. For its entire life, Rule 1 was honor-system: `grounding: EXACT` only ever answered *"did I locate your marked text?"*, never *"are this card's claims supported?"* — and nothing compared the two. The gap became visible on table captions but is general: it covers figures, image-only pages, multi-page lists, and anything a caption merely points at.

- **BAD:** a card whose highlight is `TABLE 6-3 Muscles: Locations and Functions` (a caption; the body is on the NEXT page and, for some tables, is a rendered image with no text layer at all) and which asserts `the {{c1::pectoralis}} {{c2::flexes}} and rotates the arm`. The word "pectoralis" appears nowhere in the context the card cites. The fact happened to be correct — an agent went and read the page — but **nothing in the artifacts recorded that**, so it was indistinguishable from a fabrication after the fact. 23 Chapter 6 cards were in this state.
- **GOOD (two valid shapes):**
  1. The extractor now widens a caption's context onto the next page, so the body arrives as text and the claim is grounded normally. (EMT TABLE 6-3's context went 271 → 716 characters and gained the real muscle rows.)
  2. When the material genuinely only exists as an image, the card carries **visual evidence** — `image` or `visual_source` — which both satisfies the check and makes the grounding auditable forever.
- **MUST NOT OVER-FLAG (three precisions, all found by testing the detector against real cards):**
  - **Morphology.** The source says "symphyses", the card answers "symphysis". Naive suffix-stripping called a correctly-grounded card ungrounded. Matching allows a ≥5-character prefix, which absorbs the whole class.
  - **Paraphrase is not fabrication.** House style rewrites source prose into human-flow sentences, so partial overlap is normal and healthy. Only a *zero-overlap* answer on a mark the extractor has already flagged `needs_visual` is HARD-blocked; every other shortfall is a warning routed to the judge. Measured on Chapter 6: 47 hard blocks, 94% of them citing a `needs_visual` mark.
  - **Legacy batches.** A cards file where NO card carries `from_idx` is pre-provenance; it emits one explanatory warning and is not blocked. Only files that already carry provenance are held to it.
- **Catch test (both ways):** a card asserting a fact absent from its cited context, on a `needs_visual` mark, with no `image`/`visual_source` → HARD. The same card with visual evidence attached → PASS. A paraphrase with partial overlap → warning, never a block.


## R14 — Packed list layout: a list of things to produce, crammed into one block
**Rule:** card-rules #19 + editor check #21. **Caught by:** `check_cards.py` packed-list warning; **repaired mechanically** by `listify()` in `anki_write.py`. Surfaced 2026-07-30 by Parker, with before/after screenshots of the SBAR card.

Parker answers a list card by first seeing **how many things he owes**, then producing them. Rows separated by a single `<br>` render as one grey block, which hides the count — the single most useful piece of information on the front. This is the Text-field twin of the 2026-07-02 Back Extra paragraph-break preference, and gets the same treatment: a rule, a warning, and a mechanical guarantee at write time.

- **BAD:** `The structured handover format <b>SBAR</b> stands for:<br>{{c1::Situation::S}}<br>{{c1::Background::B}}<br>{{c1::Assessment::A}}<br>{{c1::Recap/Rx::R}}` — four blanks packed into a block.
- **GOOD:** the same card with `<br><br>` between every row, so four distinct answers are visible at a glance.
- **MUST NOT OVER-FLAG — prose is not a list.** `At a vehicle crash, the first risk to consider is {{c1::traffic::hazard}}.<br>Ideally, park the ambulance so you can easily {{c2::leave::action}} the scene.` uses `<br>` to separate two flowing sentences. The discriminator is whether the lines after the lead-in are *rows*: a line carrying a cloze and almost no prose of its own (≤8 residual words; numbering and bullets count as layout, not prose). Measured across the live EMT deck: 43 cards restructured, 41 cards containing `<br>` correctly left alone.
- **Catch test (both ways):** a lead-in plus ≥2 cloze-rows joined by single `<br>` → flag and repair; the same card already spaced → silent; multi-sentence prose using `<br>` → silent.
- **R14b — the all()-veto hole (found 2026-07-30, hours after R14 shipped).** The first implementation asked `all(_is_list_row(s) for s in segs[1:])`, where a row is ≤8 residual words. **One long row therefore vetoed the entire card**, and because `listify()` and `packed_list_layout()` each held their own copy of the predicate, the repairer AND the warning went silent together — the defect was invisible from both directions. Twelve genuinely list-shaped live cards stayed packed, including the EMS-radio card Parker complained about the same day (3 of its 6 rows were "too wordy") and the ETHICS checklist (5 of 6 rows qualified; one 9-word row killed it). Reported as "43 restructured, 41 correctly left alone" — but some of that 41 were lists, not prose.
  **Fix, three parts:** (1) a second, independent signal — a **colon-terminated lead-in heading ≥2 cloze-bearing lines** is a list, because the author literally announced one, and that beats any word count; (2) `_has_single_br_separator` replaces "contains no `<br><br>` anywhere", which had let a MIXED card (one spaced gap, two packed) pass as already-spaced; (3) `anki_write.listify()` now **imports `list_shaped` from `check_cards`** so the repairer and the warning can never drift apart again. **MUST NOT OVER-FLAG:** a colon lead-in heading only ONE row is not a list; prose with `<br>` between sentences still has no colon header and too much residue.
  *Lesson:* a duplicated predicate is a single point of failure that reports itself as two independent confirmations. When code repairs something AND warns about it, both must read from one definition.

---

# Figure pipeline (R15–R17)

These do not describe a bad *card* — they describe a way the figure pipeline can quietly
produce the wrong picture, or none. They are executable in **`scripts/test_figures.py`**
(run it alongside `test_regressions.py`; `smoke_test.sh` runs both). All three were found
during the Chapter 4 figure run, 2026-07-30 — see `runs/emt/4/2026-07-30-figures/REPORT.md`.

## R15 — Caption detection assumed a © credit line
**Rule:** a caption only counts once a trailing rights line corroborates it, otherwise body prose opening *"FIGURE 4-9 shows…"* is indexed as a figure. **Caught by:** `build_figure_index.is_credit()`.

Chapter 6 is illustrations, credited `© Jones & Bartlett Learning.` Chapter 4 is **photographs**, credited *"Courtesy of the Guide Dog Foundation for the Blind."* Matching only on `©` silently lost FIGURE 4-8 and 4-12 — and would lose more of any photo-heavy chapter.

The obvious fix then caused a second regression. The looser wordings need a length guard so a sentence of prose cannot pose as a credit — but applying that guard to the `©` tier **dropped FIGURE 4-4**, because the extractor welds the credit onto the following paragraph (EMT p370 returns a 643-character block beginning `© Jones & Bartlett Learning. 7. Always speak slowly…`). Hence two tiers: a block **opening** with `©` is a credit at any length; the ambiguous forms are capped at 200 characters.

- **MUST CATCH:** `© Jones & Bartlett Learning.` · the same welded to 600+ characters of body text · `Courtesy of…` · `Source:…` · `Modified from…` · panel-letter credits (`A, C: © Photodisc; B: …`).
- **MUST NOT OVER-FLAG:** ordinary body prose · a long sentence that merely begins with the word *"Courtesy"* · a caption line itself.
- **Catch test (both ways):** in `test_figures.py`, 7 credit forms must match and 4 non-credits must not.

## R16 — A cached image adopted by a caption that has no art
**Rule:** no art located means no index record — never fall back to whatever file already sits at that name. **Caught by:** `build_figure_index.save_art()` checking art *before* the cache.

`save_art` returned a cached path whenever a file existed at that path, **even when no art was found**. So after any change that altered which captions resolve, a caption whose art stopped resolving silently inherited a stale image from the previous run: the figure count stayed flat while the index pointed at the wrong picture. This produced a phantom "47 figures" for Chapter 6 (the honest number is 45) and is the most dangerous class here, because it is invisible in every summary.

- **MUST CATCH:** `save_art(art=None)` with a file already present at the target path → must return `None`, not the stale file.
- **MUST NOT OVER-FLAG:** `save_art` with real art and a valid cached file → must still reuse the cache (rebuilding 45 plates per chapter is expensive).
- **Catch test (both ways):** both directions asserted in `test_figures.py` against a temp file.

## R17 — A re-run stacks a second figure instead of swapping
**Rule:** a card carries ONE pipeline figure; improving the matcher and re-running must swap, never accumulate. **Caught by:** the "already carries a pipeline figure" guard in `attach_figures.py` (`--allow-multiple` / `--replace` opt in).

Attaching is idempotent on *"is this exact file already here"*, which is too weak. After the crossref improvement changed which figure scored best, **six Chapter 6 cards silently gained a second picture** rather than exchanging one for the other. The outcome is only clutter — Parker's standing preference is to overshoot — but it was arrived at by accident rather than by decision, and that is the defect.

- **MUST CATCH:** a Back Extra already containing `<img src="emt_…">` → do not append a different figure.
- **MUST NOT OVER-FLAG:** a Back Extra containing only **Parker's own** pasted screenshot is *not* an existing pipeline figure — his image is never stripped, and it must not block the pipeline from adding its own (this is exactly the cranium card). A Back Extra with no image at all is untouched.
- **Catch test (both ways):** all three states asserted in `test_figures.py`.

## R15 — Row label restates its own answer (the label that leaks the blank it should cue)
**Rule:** card-rules #20 + editor check #22. **Caught by:** `check_cards.py row_label_tautology` + the judge. Surfaced 2026-07-30 by Parker, studying EMT Chapter 4.

In a `LABEL → {{answer}}` row the label is the blank's ONLY cue. When the label and the answer say the same thing, the row is a freebie wearing a hint's clothes.

- **BAD:** `Arrival at hospital or point of transfer (1) → {{c1::notify dispatch of arrival}}` — the answer is the label with a verb bolted on. Same card, same defect: `Return to service (1) → notify dispatch when {{c1::the unit is available for another call}}` (returning to service *means* being available). Parker: "the return to service is the thing I'm supposed to say, so you're giving away the answer while trying to give me a hint."
- **The mirror failure on the same card:** `Miscellaneous (1) → notify dispatch anytime the unit is {{c1::not in station}}` — a label that cues NOTHING is R9 open-set. Both live on one card, which is why the row is the right unit of review.
- **GOOD:** keep only the rows whose message is not derivable from the label — `En route → request {{c1::assistance with directions}} or {{c1::additional resources}}`; `On scene → {{c1::check in periodically as a safety measure}}` — and drop the self-answering ones.
- **MUST NOT OVER-FLAG:** a classify/match row whose visible description legitimately CUES the answer without restating it (`An obligation to provide care per the standard set by training = {{c1::duty}}`); and a two-way definition, which has no row label at all.
- **Deliberately generous, and NOT suppressed on classify cards.** A shared word stem is evidence, not proof (`Initial receipt of call → acknowledge the call` shares "call" but still tests "acknowledge"), so this is a warning the judge clears. It stays live on match cards because a real leak can sit inside a correct one — EMT's blood-components card is a good match card with one bad row: `Clotting (coagulation) → {{c1::platelets and clotting factors in the plasma}}`.
- **Catch test (both ways):** a row whose label shares a content-word stem with its own answer → flag; a classify row whose description merely points at the answer → silent.

## R16 — Absolute statement with a lone unhinted blank (the first mechanical proxy for R9)
**Rule:** card-rules #21 + editor check #23. **Caught by:** `check_cards.py open_set_absolute` + the judge. Surfaced 2026-07-30 by Parker, studying EMT Chapter 4.

**Why this case exists at all:** R9 (open-set) was ruled mechanically undetectable in July — "no reliable mechanical proxy… enforced by the LLM judge + the cold-solve test" — and was therefore the ONE Cold-Solve rule with no code behind it. Chapters 4 and 6 were generated after that decision and the class walked straight back in. A rule that only a judge enforces is a rule that recurs. This does not decide R9 in general; it closes its highest-frequency disguise.

- **BAD:** `You must never attribute a patient's altered mental status to {{c1::old age}}.` A *never / always / only* stem names a rule without constraining what the rule is about. Parker: "there are a lot of things I could fit in that blank… since there was no hint, no other cues, nothing else, how am I supposed to know it?" — *sadness*, *skin color*, *being tired* all fit.
- **GOOD (three shapes, weakest to strongest):** a slot-label hint — `{{c1::old age::a patient characteristic}}` (the fix Parker proposed himself); a visible contrast naming the rejected alternative — `'right' and 'left' always refer to the {{c1::patient's}} perspective, not the provider's`; or the positive flip with the negation as a sibling cloze — `always assume {{c1::an underlying treatable cause}} — never {{c2::normal aging}}`.
- **MUST NOT OVER-FLAG:** a hinted blank (the drafter constrained the slot), a numeric answer (self-constraining, and numeric-flagged separately), a sibling cloze that anchors the blank, and a contrast anchor AFTER the blank.
- **The numeric exemption above was half wrong, and R34 (2026-08-03) is the correction.** A number is self-constraining only *once you know the slot wants a number*; a bare blank never says so, and `the {{c1::eight}} bones` reads exactly like `the {{c1::short}} bones`. This detector keeps the exemption — an absolute sentence is not the shape that fails — but the class it was waving through is now caught by `unlabeled_quantity_blank` under card-rules #27. Recorded here because the exemption was stated as settled reasoning in two places, and a future pass reading only this line would re-derive the hole.
- **Catch test (both ways):** one unhinted non-numeric blank in a sentence carrying an absolute, with no post-blank contrast → flag; any of the four anchors present → silent.

## R17 — Fragment-clozed list (the items are visible; only filler is hidden)
**Rule:** card-rules #22 + editor check #24. **Caught by:** `check_cards.py fragment_clozed_list` + the judge. Surfaced 2026-07-30 by Parker, studying EMT Chapter 3.

The inverse of under-clozing (R1). R1 is a must-test fact left visible by oversight; this is the card **inverting** cue and answer on purpose — the knowledge is *which items are on the list*, all items are shown, and one guessable word is punched out of each. It trains recognition of frames Parker will never be asked to reproduce.

- **BAD:** `run 8 self-check questions:` + all 8 questions visible, each missing a word — `Are you {{c1::abandoning}} the patient?`, `Are you neglecting your {{c1::duty}}?`, `Is the person assuming care {{c1::capable}}?`. Parker: "I can pretty much guess most of these and get it right… it doesn't actually help me remember this card, it just helps me remember the CONTEXT of the card." Its twin is the ETHICS six-question checklist.
- **GOOD, in order:** cloze the items themselves if they are crisp (the SAMPLE shape); if they are too long to reproduce verbatim, **change the archetype** — test the organizing structure that makes the set derivable and keep the full list in the Back Extra; add 1–2 application vignettes on the highest-yield members.
- **MUST NOT OVER-FLAG (two real neighbours):** a **classify/match** card (`description = {{c1::category}}`) — there the visible description IS the intended cue, and the lead-in says so in the imperative; and an **item-then-descriptor** row (`{{c1::Nasopharynx}} — above the soft palate`, every SAMPLE/SBAR mnemonic row) — there the row leads with its cloze, so the item already is the answer.
- **Catch test (both ways):** ≥3 rows, none leading with its cloze, each hiding fewer words than it shows, no classify lead-in → flag; a mnemonic list, a classify card, or an item-then-descriptor list → silent.

---

*To add a case: when Parker catches something new, record the BAD card, the GOOD fix, the rule it enforces, and the concrete catch test. Then confirm the checker or judge actually catches it before considering it closed.*

## R18 — A caption's body is out of reach, so correct cards read as ungrounded
**Rule:** Rule 1 (always ground in the page paragraph) + R13. **Caught by:** `check_cards.py` R13 grounding, once the context actually contains the body. Found 2026-07-30 when backfilled provenance turned R13 on for Chapter 4 for the first time.

A highlighted TABLE/FIGURE caption is a *pointer*; the material is the body below it. Two separate cuts kept that body out of the mark's context, and both produced the same symptom: a **correct** card, whose text sits verbatim in the source, HARD-blocked as ungrounded.

1. **The forward window was never widened for a caption.** `wants_next_page()` already treated a caption exactly like a list lead-in and fetched the following page — but `locate_context()` did not, so the extra page was fetched and then discarded by the 450-character default. EMT TABLE 4-3's context stopped mid-table at "Reflection", four rows short of the Empathy / Clarification / Confrontation / Interpretation rows that four blocked cards were built from.
2. **A caption needs MORE reach than a list.** Raising it to the list budget (1,700) still blocked TABLE 4-7, whose caption sits at the top of p403: that page's own remaining 1,704 characters consume the whole budget before p404's "document the name of the facility… and the room number" row is reached. Captions now get `CAPTION_FWD_CHARS = 3800` — a caption's body is a whole table and routinely crosses a page break.

The mirror-image failure, fixed with it: **`attach_figures.py` wrote the figure to Anki but not to the canon cards file.** The gate reads the file, so a card could be HARD-blocked for lacking precisely the visual evidence already sitting on it in the deck. It now writes `visual_source` back and clears the `.verified` stamp so the gate re-runs.

- **MUST CATCH:** a card asserting a fact that is absent from its cited caption-mark's context and carries no visual evidence.
- **MUST NOT OVER-FLAG:** a card whose fact *is* in the widened context (the six Chapter 4 cards) → clean; a card carrying an attached figure as `visual_source` → clean.
- **Catch test (both ways):** re-extract Chapters 4 and 6 and gate them — both must reach **0 hard errors** and stamp. Before the fix Ch4 had 6. `smoke_test.sh` asserts the ch4 gate.

## R19 — A figure that is merely NEARBY, not about the card
**Rule:** a plate must depict the card's SUBJECT, not merely share its topic or its page. **Caught by:** the zero-coverage block in `match_figures.py` + the mandatory judge pass (`scripts/judge_figures.py`, SKILL.md Stage 2.95). Found 2026-07-30 by Parker while studying Chapter 4 — the first defect this feature produced in his actual review.

Word overlap can tell you a figure and a card share vocabulary. It cannot tell you the figure *depicts* what the card is about, and that is the only question that matters. Parker's test is the standard: *"if I see a picture and my first thought is 'why in the world is that picture there?' it leads me to a root of confusion instead of a root of actually succeeding."*

Two distinct causes, and only one of them is mechanically catchable:

1. **Pure page adjacency.** FIGURE 4-2 (*"the effectiveness of body language. A. Happy. B. Angry. C. Sad."* — three faces including a crying baby) attached to *"Facing a hostile patient, stand with your {{c1::palms facing out}}"*. **Coverage 0.00, matched terms `[]`.** It qualified only because it sat on the same page. The rule that allowed this — "the book put the plate beside the sentence" — was wrong reasoning: a page holds many paragraphs and the figure illustrates ONE. **Now blocked outright: zero shared vocabulary never qualifies.**
2. **Domain wallpaper.** FIGURE 4-17 (control centre → tower → ambulance) attached to *"A cellular telephone is effectively a {{c1::low-power portable radio}}…"* on the strength of `radio` and `repeater`. Both are genuinely *distinctive* terms (each in ≤4 of 66 figures), so **no frequency/IDF weighting catches this** — it was measured and rejected. The plate shows a base station; the card is about a phone. **Only looking at the picture catches it.** Hence the judge stage.

- **MUST CATCH:** a proposal with zero shared vocabulary (mechanical); a proposal whose plate depicts a different subject from the card (judge).
- **MUST NOT OVER-FLAG:** **low coverage is not the defect.** Chapter 4's two BEST matches scored near the bottom — the guide dog at 0.17, the sign-language panel at 0.12 — and both were kept. Congruent-but-unnecessary is fine and wanted (the developmental age-group photos). The defect is *incongruent*, at any score.
- **Catch test (both ways):** on EMT ch4, FIGURE 4-2 → palms card and FIGURE 4-17 → cellular card must both be absent from the proposals; FIGURE 4-8 → guide-dog card and FIGURE 4-7 → hard-of-hearing card must both survive. Verified live: after the fix both flagged cards carry no figure, and ch4 went 31 → 17 attached.

## R20 — Provenance recovery assumed card order, and the chapter restates itself
**Rule:** a card's page must be recoverable without assuming generation order, and the page it is recovered to must be where the material was TAUGHT, not where the chapter recapped it. **Caught by:** `backfill_provenance.py` pass 3 (direct page location) + the earliest-among-ties rule, cross-checked against pass 1/2. Found 2026-07-30 on EMT Chapter 1.

Passes 1–2 anchor a card to a mark by text overlap and then interpolate between anchors, which needs card order to track mark order. That is true of a freshly generated chapter and of Chapter 4 (67 anchors, 59 in one consistent run, 104/107 resolved). **Chapter 1 collapsed to a 6-anchor spine and 12 of 32 resolved** — not because its anchors were wrong (they verify by hand) but because its cards were reordered by heavy consolidation: `0→30, 1→3, 2→20, 4→8`. The assumption, not the matching, was the defect.

The matcher never wanted the mark; it wanted the **page**. Pass 3 scores each page of the chapter against the card's own text — no ordering assumption, identical behaviour on legacy and fresh chapters. Ch1: **29/32 located vs 12/32 via marks.**

That introduced its own failure. A chapter **restates itself at the end** — the glossary and the "Ready for Review" recap condense every definition — so a definition card ties exactly with the summary. Three Ch1 cards landed on the p125 glossary (*"credentialing — An established process to determine the qualifications…"*) instead of the body page that taught them, at 0.73 vs 0.73. **Ties break toward the EARLIEST page:** the body always precedes the recap, and it is the body that has a figure beside it.

- **MUST CATCH:** a chapter whose card order is scrambled must still resolve its pages (Ch1 ≥ 25/32); a definition card must not resolve to the glossary.
- **MUST NOT OVER-FLAG:** the earliest-among-ties rule must not disturb chapters that were already correct — Ch4 and Ch6 agreement between the two methods stayed at 91/4 and 174/5.
- **Catch test (both ways):** run the backfill on ch1, ch4 and ch6 and read the printed cross-check. 96–97% agreement on ch4/ch6 is the corroboration; Ch1's disagreements must each be a card scoring far higher against the located page than against its mark's page (0.45–0.77 vs 0.05–0.29), i.e. the mark is the wrong one.

## R21 — The figure writers could clobber Parker's own work
**Rule:** nothing writes a field this system did not author. **Caught by:** `authorship.guard(..., figure_only=True)` in `attach_figures.py` and `judge_figures.py --strip-live`; `authorship.py self-test`.

The authorship store treats every card predating it as `unknown` and protects it — deliberately, since the incident it exists for was a pass confidently overwriting Parker's own ETHICS mnemonic. But `attach_figures.py` and the `--strip-live` reconciliation both write `Back Extra` on live notes and **consulted none of it**, so they had been running unguarded over the whole existing deck.

A strict guard would have blocked the figure stages entirely, since no card predating the store is `owned`. The answer is a **second verified predicate, not a bypass**: `is_figure_only_change()` strips every pipeline-owned `<img src="<source>_…">` from both sides, normalises the break runs they sat in, and requires the residue to be identical. Attaching or stripping a pipeline figure passes; anything else does not.

- **MUST CATCH:** removing an image **Parker** pasted (his files never carry the `<source>_` prefix); any text change riding along with an image change; an ordinary field rewrite that merely sets `figure_only=True`.
- **MUST NOT OVER-FLAG:** attaching a pipeline figure to a field carrying his own screenshot and his own prose; stripping a pipeline figure back off it.
- **Catch test (both ways):** five cases in `authorship.self_test()` (8 → 13 total), including the one that matters most — stripping his own pasted screenshot must be REFUSED.

## R22 — The fresh-segment route must refuse unjudged proposals
**Rule:** no figure reaches a card without a judge verdict. **Caught by:** the `judged` check in `attach_figures.py --to-cards`.

There are two ways to attach, and they are not interchangeable. A chapter already staged gets its LIVE notes updated; a fresh chapter (7 onward) gets figures written into the **cards file**, which `anki_write.py` then embeds as it creates the notes. Re-running `anki_write.py` on an already-staged chapter would ADD 202 duplicate notes instead of 202 pictures.

The fresh route is the dangerous one, because nothing stands between it and a brand-new deck. If it accepted unjudged proposals, every merely-nearby figure — the whole R19 class the judge exists to catch — would ship straight into the chapter with no human ever looking at a picture.

- **MUST CATCH:** `--to-cards` against a proposals file with no `judged: true`.
- **MUST NOT OVER-FLAG:** a judged file must pass, including one whose kept list is empty (a chapter can legitimately earn no figures).
- **Catch test (both ways):** both asserted in `test_figures.py` by invoking the real script.

## R23 — A table split across a page break, and provenance too weak to assert
**Rule:** a TABLE title with no body under it has its body on the next page; and provenance is only recorded when it can be trusted. **Caught by:** `find_captions(page, next_page)` + the `pair_art` table fallback; the `from_idx` decision is a judgement recorded per segment. Found 2026-07-30 on EMT Chapter 5.

**The split table.** House style titles a table ABOVE its body, so a title near the foot of a page leaves the body — and the credit line that corroborates it — on the page after. Two independent checks each blocked it: `find_captions` looked for corroboration only on the caption's own page, and `pair_art`'s next-page fallback required the title to sit in the bottom 140pt, which is wrong for a reflowed PDF (TABLE 5-1's title lands at y=324 on a 792pt page with nothing beneath it but white space). Together they lost **all twelve of Chapter 5's terminology tables** — the entire source of a 587-card chapter. Fixed: corroboration may come from the top of the next page when the caption is among the last blocks, and a table with no body on its own page always looks to the next. Book-wide effect: 127 → 135 figures, every chapter gaining.

**Provenance too weak to assert.** Chapter 5 is 587 cards from 27 marks — 21.7 cards per mark — and the mark-vs-page cross-check agreed only **57%** (against 96–97% on ch4/ch6). Backfilling `from_idx` anyway turned R13 on and HARD-blocked ~166 **correct** cards whose word roots genuinely live in image-only tables. The backfill's own rule is that *a wrong `from_idx` is worse than a missing one*, so ch5 keeps `source_page` (located directly, order-independent, and what the matcher actually uses) and asserts no mark-level provenance.

- **MUST CATCH:** a table whose title ends a page and whose body begins the next; a segment whose cross-check agreement is far below the ~95% the sound chapters show.
- **MUST NOT OVER-FLAG:** tables that pair on their own page (EMT TABLE 6-9/6-10) must still pair there — the next-page branch is only reached after the same-page search comes up empty.
- **Catch test (both ways):** rebuild all six chapter indexes; ch5 must index TABLE 5-1…5-6 with art on the FOLLOWING page, and ch6 must still index 47 with TABLE 6-9/6-10 paired on their own page.

## R25 — Retrieval overload: a grouped reveal that cannot be passed even when known
**Rule:** card-rules #23 + editor check #25. **Caught by:** `check_cards.py overloaded_group` (≥6 uncued warns, ≥8 uncued HARD) + the judge. Surfaced 2026-08-02 by Parker, studying EMT Chapter 4.

Every earlier Cold-Solve case asks whether a blank is **answerable**. This one asks whether the card is **passable**. A grouped reveal is graded all-or-nothing — one button for the whole set — so a card hiding N items is "Good" only if every one of the N is produced. At a realistic 90% per item that is 0.9^N: 59% at five, 43% at eight, **35% at ten**. The card can therefore be built entirely from facts Parker knows cold and still fail forever, and Anki compounds it by rescheduling the whole card on its worst item. His response was not to fail it but to stop answering it: *"what I'll find myself doing is just skipping that flash card as I'm reviewing, because I know that I can't get it right — 10 things all at once."*

**The measurement** (live collection, EMT decks only so generation run and maturity match, scored on each card's FIRST review so new-card bias cannot explain the gap):

| group | notes | failed first review | again rate | sec/review |
|---|---|---|---|---|
| ordinary (1–2 blanks) | 1027 | 56% | 41% | 24.9 |
| 3–4 items | 90 | 78% | 46% | 33.3 |
| 5–6 items | 34 | 89% | 61% | 42.7 |
| 7+ items | 7 | 80% | 63% | 49.3 |

- **BAD:** the 10-element radio patient report under one `{{c1::}}` group. Live stats: **5 reviews, 5 "Again", 54 s each — never once answered correctly.**
- **GOOD:** chunked into an anchor note (the three phases) plus three phase notes of 3/4/3, each with one cloze number and a `Roster:` line carrying all ten with its own members bolded.
- **MUST NOT OVER-FLAG, three real neighbours** — and all three are what keep this from becoming a war on lists:
  - **A spelled mnemonic the card teaches.** DCAP-BTLS is 8 items and is ONE chunk, because the letters regenerate the set. Licensing reuses R11's exact predicate (the group's hint letters must spell into a token *visible* in the stem), so the two detectors cannot disagree — and a licensed group is silent, not re-flagged for a human to confirm what the code already proved (the R14b duplicated-predicate lesson).
  - **Cued rows.** `Neonate — {{c1::100 to 180}}` and `Transports oxygen → {{c1::red blood cells}}` are N independently-cued retrievals, not one N-wide recall. A keyed panel or match card is exempt at any length. The trap inside this exemption, found while calibrating: a card's own colon-terminated LEAD-IN ("…is composed of 10 structures:") would otherwise be read as a per-item label for the first inline item, so a label only counts inside a row of its own — never in the segment the card opens with.
  - **Anything at or under the cap.** The defect is load, not list length as such; 4 uncued answers ship untouched.
- **Calibration is the test.** The thresholds were set by checking the detector against Parker's OWN verdicts in the report that created the rule, all four of which it reproduces: the 10-element radio report → HARD; CHART (5, acronym) → clean; the five-point handover method → clean; the six-cause hostility card → warn, which is exactly the "you could argue it either way" he described. Live blast radius across 1158 EMT notes: **5 HARD, 8 warn.**
- **Catch test (both ways):** a group hiding ≥8 uncued answers with no mnemonic license → HARD; the same count under a spelled mnemonic, or with per-row cues, or at ≤4 → silent.
- **R25b — rules 14 and 23 fight over the stated count, and the drafter loses.** A chunked note legitimately states the FULL set's count while clozing only its own members ("the report's 10 elements … 8. …, 9. …, 10. …"), which is exactly the shape R7's undercount warning exists to catch. The first draft of the radio family dodged it by writing "10-element" instead of "10 elements" — a **checker-shaped word choice**, which is the smell that says two rules are in conflict and the human is absorbing it. Fixed by exempting any card carrying a `Roster:` line, since rule 23 requires one on every note born from a chunk. **MUST NOT OVER-FLAG in the other direction:** the exemption must not blanket-disable R7 — a genuine undercount with no `Roster:` line still flags. Both directions asserted in `test_regressions.py`.
- **R25c — an anchor note must not cloze invented vocabulary.** The first draft's anchor hid "the dispatch header / the patient picture / care and close," three phrases that exist in no book; its own Back Extra admitted *"the three phases are a memory scaffold, not radio traffic."* A partition the pipeline invented is a scaffold, not content Parker will be asked to produce, so clozing it is simultaneously ungrounded (Rule 1), open-set (R9) and prerequisite-unclosed (rule 11). **The names stay visible in each sub-group note's stem; the extra note becomes a grounded order vignette instead** (*"you have already given X, Y and Z — what comes next?"*, built on the source's own running example). Caught by the human review pass, not by code — the drafter surfaced it honestly as a judgment call rather than burying it, which is the behaviour to reinforce.

## R26 — The fix that recreates the disease: a list split across sibling cloze numbers
**Rule:** card-rules #24 + editor check #26. **Caught by:** `check_cards.py sibling_split_leak` (HARD). Written the same day as R25, pre-emptively.

This case exists because the obvious way to obey R25 is wrong, and a future pass would find it by reasoning rather than by malice. Renumbering an overloaded list `{{c1::A}} {{c2::B}} {{c3::C}}…` generates N cards that each display the other N−1 answers as free context, so the set is recovered by **elimination and recognition** instead of recall — every card feels learned while nothing is. Parker identified this himself, unprompted, in the same message that reported R25: *"I don't think that's what we need… if it's a hide-one-but-show-all-the-rest, I can just figure that out."*

R25 and R26 are a matched pair and must be read together: R25 says *split it*, R26 says *split it the right way*. Fixing one by committing the other is the whole hazard.

- **BAD:** the radio report renumbered c1…c10 — ten cards, each revealing nine answers.
- **GOOD:** separate NOTES, each using a single cloze number for its own sub-set, so nothing on one note reveals another note's answers.
- **MUST NOT OVER-FLAG:** a two-way definition (`{{c1::TERM}} is {{c2::meaning}}`); a contrast card whose entity anchors stay visible while the values hide (the R10 precision); any card whose numbers mark *different facts* rather than members of one enumerated set. The detector requires all four signals at once — ≥4 distinct numbers, exactly one span each, ≥4 parallel list ROWS — so ordinary c1/c2/c3 cards are untouched. Measured: **0 hits across 1158 live EMT notes**, i.e. no false positives on a deck built entirely under the old rules.
- **Catch test (both ways):** an enumerated list fanned across ≥4 numbers on one note → HARD; a two-way definition, a contrast card, or a 3-number multi-fact card → silent.

## R28 — A keyed panel of NUMBERS: all-or-nothing grading plus an interpolable column
**Rule:** card-rules #25 + editor check #27. **Caught by:** `check_cards.py quantitative_panel` (≥3 keyed numeric rows warns, ≥4 HARD). Surfaced 2026-08-03 by Parker — the card that gave him the idea behind R25 in the first place.

**This case narrows R25, written the day before.** R25 *exempted* keyed panels at any length, reasoning that a per-item cue turns one N-wide recall into N independently-cued ones. That is true about **difficulty** and false about **grading**: every row still hides and reveals under one cloze number, so the card is graded all-or-nothing however well each row is cued. And for a *value column* it is doubly false, because the numbers give each other away. Parker: *"if I see infant heart rate, I can guess what the neonate heart rate is… it's already given me half of the solution."*

The card proved the leak in its own Back Extra, which taught the shortcut as a mnemonic: *"the lower bound walks down in clean tens — 100, then 90, 80, 70, and 60."* A genuinely good memory hook and an exact recipe for answering without recall.

- **BAD:** `Normal <b>pulse rate</b> in beats/min, by age group:<br><br>Neonate — {{c1::100 to 180}}<br><br>Infant — {{c1::100 to 160}}<br><br>Toddler — {{c1::90 to 150}}…` — six values, one grading event, monotonic column.
- **Also BAD, and worse:** a match card whose answers are a *complete consecutive run* — the infant-milestone tables, answers 2–6 and 7–12 months. Once two rows are confident, the rest fall out by elimination and developmental ordering, so the card is solvable without recalling any single month.
- **GOOD:** `What is the normal <b>pulse rate</b> for a <b>toddler</b>, in beats/min? {{c1::90 to 150::range}}` on its own note, with TABLE 7-1 attached (`image_side: "back"`). Parker's framing: *"the cards are disconnected in the sense of memorizing, but they're connected in the sense of the table."*
- **MUST NOT OVER-FLAG, three neighbours:**
  - **Word answers cannot interpolate.** `Transports oxygen → {{c1::red blood cells}}` is judged on load alone by rule 23. Scoping this rule to numeric answers is what keeps it from becoming a war on match cards.
  - **A lone numeric row does not make a value column.** A direction-of-change panel (`Heart rate: increased · Systolic BP: normal · Cap refill: delayed (>2 s)`) is mostly words; the detector requires ≥80% of rows to be *both* keyed and quantitative.
  - **Three rows is a warning, never a block.** The adult-heart-rate-by-situation card (at rest / athlete at rest / vigorous activity) has three values that do *not* trend with an ordered key, and is fine as it stands.
- **Do not restate the other rows' values in Back Extra prose.** The table image carries them; prose restatement rebuilds the leak in the one place he looks after answering.
- **Measured scope:** across his whole 4,340-note collection this fires on **9 cards**, every one a genuine value column — 7 hard (all in Chapter 7) and 2 warns. Chapters 1–5 are untouched.
- **Catch test (both ways):** ≥4 keyed rows whose answers are values → HARD; a word-answer match card, a mostly-word direction panel, a 3-row non-trending set, or a single-value note → silent.

## R34 — A bare count in a slot that never says it wants a count
**Rule:** card-rules #27 + editor check #29. **Caught by:** `check_cards.py unlabeled_quantity_blank` (a WARNING) + the judge. Surfaced 2026-08-03 by Parker, studying EMT Chapter 6.

**This case exists because an earlier case's exemption was wrong.** R16 (`open_set_absolute`) excused numeric answers in writing — *"a numeric answer (self-constraining, and numeric-flagged separately)"* — and the checker's own docstring said the same. The reasoning has a hole: a number is self-constraining **only once you know the slot wants a number**, and a bare blank never says so. In the attributive position, where a count stands directly in front of the thing it counts, an adjective fits just as comfortably. `the {{c1::eight}} bones that form the wrist` and `the {{c1::short}} bones that form the wrist` are the same front.

Parker named both the defect and the fix: *"a good hint here would be something like {{c1::five::number of bones}} — that would make it so i can know what im guessing... just say like 'long bones!' or 'short bones!'"*

- **BAD:** `The {{c2::carpals}} are the {{c1::eight}} bones that form the wrist, and the {{c2::metacarpals}} are the {{c1::five}} bones that form the palm of the hand.` — both counts under c1, so on that card neither cues the other.
- **GOOD:** the same card with `{{c1::eight::number of bones}}` and `{{c1::five::number of bones}}`.
- **MUST NOT OVER-FLAG — four real neighbours, and finding them is what made the rule shippable:**
  - **A unit after the blank** (`{{c1::90 to 150}} beats/min`) — nothing but a number fits there.
  - **A content word before it** (`Type {{c1::1}} diabetes`, `HPV {{c1::6}}`, `chromosome {{c1::11}}`, `a pKa of {{c1::6.5}}`) — that word has already named the kind of number, and the answer is an IDENTIFIER rather than a count. This is the single biggest class: a first, looser draft that checked only "is the answer a bare number, is it unhinted" fired on **1,454** notes across the collection, most of them this.
  - **A quantity word in the stem** (`How many bones form the wrist?`).
  - **Another number left visible in a parallel slot** — `{{c1::three}} lobes … {{c2::two}} lobes` announces itself on both cards; the same card with both counts under c1 announces nothing on either, and does flag.
- **Measured scope:** the shipped detector fires on **4 of the 1,223 notes** in the deck this pipeline owns — all four genuine, all four fixed. It also fires **44 times** across the 85,212 imported AnKing notes (`There are ___ pairs of spinal nerves`, `The right lung has ___ lobes`), which is corroboration that the shape is a real and recurring one rather than a quirk of this generator — not a license, and those decks are not ours to edit.
- **The repair needed a third verified predicate.** Every card predating the authorship store is `unknown` and therefore protected, so "fix this for all the cards" could not have been applied to any of them. `authorship.is_hint_only_change()` licenses **adding** a hint where there was none — the prose, every cloze number and every answer must be byte-identical — and deliberately refuses to change or remove an existing hint, since a hint may be Parker's own and there is no prefix to tell his from ours (the trick that lets `is_figure_only_change` protect his pasted images). Six cases in `authorship.self_test()` (13 → 19).
- **Catch test (both ways):** six cases in `test_regressions.py` (`r34_*`) — the carpals card must warn; the hinted version, a unit-after blank, an identifier, a visible parallel number, and a "how many" stem must all stay silent.

## R33 — The grounding gate's visual exemption was self-asserted
**Rule:** Rule 1, enforced by R13. **Caught by:** `check_cards.py _visual_evidence_exists`. Found 2026-08-03 by a drafting agent that read the checker while following the docs — the best kind of find, because it came from someone trying to *use* the system correctly.

R13's HARD block is the only mechanical enforcement of Rule 1. It is skipped for a card carrying visual evidence, which is right: when the material genuinely lives in a picture, an unsupported answer is fine *provided the picture is attached*. But the test was `bool(card.get("image") or card.get("visual_source"))` — and `visual_source` is a **free-text field the drafter writes itself**. Any card could switch off the check on every one of its answers by asserting that it had looked. The one gate protecting the system's first rule could be disabled by the thing it was checking.

The exemption is now a **verified predicate**: an `image` path that resolves on disk, or a `visual_source.figures` entry that resolves under the source's work directory. A `visual_source` carrying only prose proves nothing and exempts nothing.

- **MUST CATCH:** a card whose answer is absent from a `needs_visual` mark's text and which asserts `visual_source` with no resolvable file.
- **MUST NOT OVER-FLAG:** the same card with a real attached plate — that is genuine evidence and still exempts.
- **This immediately invalidated an existing GOOD fixture**, which had named `figures/p549_table_6-3.png` — a file that never existed. The test had been asserting the hole rather than the behaviour. Repointed at a real plate.
- **Catch test (both ways):** two cases in `test_regressions.py` (`r33_*`).

## R32 — A rendered table can be cut by a page break; an extracted one cannot
**Rule:** SKILL.md Stage 2.9's "extracting returns it whole — splitting is a property of pagination, not of the picture." **Caught by:** `test_figures.py` R32. Found 2026-08-03, the same day the render path was written.

That guarantee is true for **embedded rasters** and false for **`text-table-render`**, which re-renders the page. EMT TABLE 8-3's last two situations and its credit line sit at the top of p804, *above* the Skill Drill 8-7 banner — and the render loop broke on "a caption appears on this page" before taking them. The plate showed **four of six situations**, which is worse than no plate at all, because it looks complete. A card built from it would have taught two-thirds of a list and told Parker it was the whole set.

A new caption bounds a table's body from **below**, not from before: the continuation page is now clipped to the caption rather than abandoned.

- **MUST CATCH:** a table whose remaining rows sit above a caption on the following page.
- **MUST NOT OVER-FLAG:** a continuation page whose caption sits at the very top has nothing left of the table on it and is still skipped.
- **The same error had reached the brief in prose:** the Chapter 8 run brief said TABLE 8-3 had "four situations," written from a render of p803 alone. It has six. Corrected, with a note to count the list against the mark's context rather than a single page render (card-rules #14, one content type further on).

## R30 — Reciting a procedure by step number (the shape professional decks never use)
**Rule:** card-rules #26 + editor check #28 + recipes §12. **Caught by:** `check_cards.py step_recitation` (a WARNING the judge clears). Established 2026-08-03 by measuring Parker's own collection rather than by reasoning.

He asked how to card systematic, skill-based material without producing junk, and pointed at his AnKing decks as the authority: *"let's use the evidence-based system that I already have built into my Anki."* So the rule was derived from **85,212 professionally-made notes** — the AnKing Step Deck, Ankisthesia, USMLE-Rx/First Aid and Dermki.

**What the measurement found:**
- **"next step in management" cards (n=194): 93% hide exactly ONE span, 99% use one cloze number, 0% hide five or more, 95% are question-form.** The procedural workhorse of medicine is a rich situational vignette with a single blank on the action.
- **The flagship AnKing Step Deck is 89% single-span; 1% carry ≥5.** The older USMLE-Rx deck is 49% single-span — tightness is what curation converges on.
- **Psychomotor technique is not carded at all.** Across all 85,212 notes, including 10,907 anesthesia cards: `"place your hands"` → 0, `"position your"` → 0, `"how do you perform"` → 0, `"steps to perform"` → 0, `"insert the needle"` → 1. What they card instead is the *decidable residue*: `The ideal site for a femoral nerve block is in the {{c1::inguinal crease}} at the lateral border of the femoral artery`.
- **A whole algorithm becomes a DECISION TABLE**, cued by conditions rather than positions — the exemplar being AnKing's blunt-abdominal-trauma card, six blanks under one cloze number where every row is cued by its own condition (`FAST (+) and unstable? → Ex-lap`). Not one blank is guessable from its neighbours, because position carries no information and the condition carries all of it.

- **BAD:** `Perform the extremity lift with the following steps:` + rows cued only by `1.`, `2.`, `3.`, `4.` Position is not knowledge, and it is not what he will be asked for on a call.
- **GOOD (three shapes):** a decision-point vignette (state in the stem, one blank on the action); a decision table (rows cued by conditions); the decidable residue of a physical skill (indication, landmark, contraindication, complication, the step people get wrong).
- **MUST NOT OVER-FLAG:** a decision table whose rows carry conditions; a single-blank vignette; ordinary prose comparing two procedures. The detector requires EVERY row's only cue to be an ordinal, so one condition-cued row exempts the card.
- **Deliberately a WARNING, never a block.** A short ordered protocol whose order genuinely is the knowledge is legitimate, and Parker likes one of them (the five-point handover method). The detector cannot tell it from a recitation, so it warns and the judge clears it — and `test_regressions.py` asserts that the handover card *is* flagged, so the warn-not-block contract stays explicit rather than drifting into a block.
- **Catch test (both ways):** five cases in `test_regressions.py` (`r30_*`). Live blast radius on the EMT deck: **5 of 1,223 notes**, all genuine short protocols.

- **R30b — the first evidence pass was WRONG about psychomotor technique, and the correction matters more than the original claim (2026-08-03, same day).** A whole-population re-audit (all 85,212 notes dumped and analysed locally, rather than sampled) overturned two of the four findings:
  - **"Psychomotor technique is never carded" was a VOCABULARY failure, not a fact.** `"place your hands"` → 0 because these decks do not write that way. They write `In BLS for infants the compression method is {{c1::2-3 fingers}}` — and there are **17 such cards**, a full parameter matrix covering six parameters across three patient populations. CPR, the archetypal psychomotor skill, is carded as a lookup table keyed by (population × parameter). Technique vocabulary the first pass never tried: `sniffing position` 5, `jaw thrust` 5, `cricoid` 30, `gauge` 44, `Tuohy` 5. **The corrected claim is narrower and more useful: the MOTION is never narrated, but the technique's discrete testable VALUES always are** — named end-position, numeric parameter, confirmation cue, failure mode.
  - **"The more curated the deck, the tighter the cards" is false.** AnKing's own flagship *MCAT* deck is the loosest thing in the collection (31.6% single-span), looser than the "old" USMLE-Rx deck used as the negative example. What predicts tightness is the deliberately chosen **archetype** — `Card_Features::Rapid_Diagnosis` is 98.3% single-span against a 73.0% deck baseline.
  - **A reported figure was also wrong:** AnKing Step Deck is **73.0%** single-span over the whole population, not the 89% the sample reported.
  - **What survived, and got stronger:** the decision card is a *deliberate constraint*, not house style — next-step cards beat their own deck's baseline on every axis in two independently authored decks, and **0 of 419** carry ≥5 spans where the baselines predict ~5. And the decision table is not just a pattern but a *mechanized* one: AnKing's `Card_Features::Shuffle` tag (152 notes) randomizes row order at review so position can never become the cue.
  - **Three shapes the first pass missed entirely**, now in recipes §12: the **parameter matrix** (above); the **step-scaffold**, where the ordinal is printed and only the content is clozed (120 notes, used for mechanisms and lab protocols and *never* for a clinical psychomotor procedure); and **image occlusion over a printed flowchart** — AnKing's `IO-one by one` note type has 5 notes, 1 template and **4 real uses, all four tagged `Card_Features::Algorithm`**. That note type was invisible to the first pass because its `Text` field is empty.
  - *Lesson, and the reason this is recorded as a case rather than quietly patched:* **a keyword search proves a phrasing absent, never a concept absent.** The first pass drew a strong negative conclusion from zero hits on five phrases it chose itself. A negative claim needs a search designed by someone trying to *refute* it — which is exactly what the re-audit was, and what any future "X is never done" claim must get before it enters the canon.

## R29 — A SKILL DRILL is a multi-page procedure, and three things treated it as a plate
**Rule:** a drill's banner is a title above its body, its corroboration is a `Step N` heading, and its steps run one per page. **Caught by:** `test_figures.py` R29 + the `skill-drill-composite(N steps)` extraction label in the index. Found 2026-08-03 while preparing EMT Chapter 8, which is mostly drills — **four of the five marks Parker made in that chapter are Skill Drills.**

Chapters 1–7 contain almost no drills, so this whole content type reached Chapter 8 untested. Three independent defects stacked, and together they indexed **1 of 12** drills:

1. **`find_captions` demanded a credit line.** A drill banner has none — its body is a run of step panels and the credit lands pages later — so 10 of 12 were rejected before `pair_art` ever ran. A drill's own corroboration is that a `Step N` heading follows, which is exactly as strong: body prose that merely name-drops a drill is never followed by one.
2. **`pair_art` classed a drill with FIGURE**, i.e. caption-BELOW-art, so the search ran upward into the preceding prose. A drill banner is a title ABOVE its body, like a TABLE.
3. **A drill is not one plate.** Its steps run **one per page**, so pairing a single art object returned Step 1 and silently dropped the rest of the procedure — a card about a four-step carry would carry a picture of its first move. Now composited into one plate showing the whole procedure, which is the artifact that belongs on the back of a procedure card.
   - **And Step 1 sits on the banner's OWN page as often as on the next.** Starting the walk at `cap+1` lost the first step of **three of the four drills Parker marked**. The caption page is included when it carries a step heading, and its render is clipped to the banner so the section's body prose above it is not dragged in.

**The extractor had the mirror bug.** `wants_next_page` appends exactly ONE page, which covers every other caption but not a drill: Skill Drill 8-11's context came back as **172 characters covering Steps 1–2 of 4**. A card built from that would state a procedure missing its last step — the R7 undercount class, one content type further on. A drill now walks forward while pages keep carrying step headings, stopping at the procedure's end. Measured: marks 19–22 went from 172–628 characters to 1,125–3,132, and all four now carry their complete step sequence.

- **MUST CATCH:** a banner followed by `Step 1` is a caption; a drill is title-above-body; the walk includes the banner page when it carries a step, and follows the steps to their end.
- **MUST NOT OVER-FLAG:** body prose merely naming a drill (`"As described in SKILL DRILL 8-9…"`) is not a caption; the walk stops at the next caption rather than swallowing the following section; FIGURE keeps caption-below orientation.
- **Catch test (both ways):** four assertions in `test_figures.py` R29, plus the live check that EMT Chapter 8 indexes 11 drills with plausible step counts (was 1).

## R27 — Two process failures from the same run, both about STALE READS
Not card defects — ways the *pipeline around* the cards went wrong on 2026-08-02. Recorded because both are cheap to repeat and neither is visible in any card.

**a) A fan-out's output file was read, edited, and then re-read after the agent rewrote it.** Three drafting agents ran in parallel; the main loop reviewed each output, edited it (dropping anchor notes), and later re-read the same paths to stage. Two agents rewrote their files *after* that review, so the staging step silently picked up the pre-edit content and **three rejected cards were written into the live deck**. Caught only by comparing the staged files against canon afterward.
- **The rule:** after a fan-out, treat every agent output as immutable input — copy it, or re-verify at the moment of use. **Reconcile what you staged against canon before declaring success**, since the staged file and the canon file are two reads of the same intent and they must agree.
- **Catch test:** for each `retrieval_load_ch<N>_cards.json`, every note's Text must exist in `chapter_<N>_cards.json` AND in the live `claude review` deck. Run it after any staging.

**b) A smoke-test assertion encoded a card COUNT, so staging cards broke the suite.** `live ch3 = 84 cards` went stale the moment six notes were staged. A green suite must mean *"the path works"*, never *"nobody has staged anything since this was written."* Rewritten to assert the live audit reaches the deck and reads a plausible chapter.
- **MUST NOT OVER-CORRECT:** parity assertions that pin a genuinely fixed quantity (ch1 still extracts 36 marks; ch5 canon loads 587 notes) are correct as exact numbers — those describe the SOURCE, which does not change. Only counts of things the pipeline itself adds should be ranges.

## R24 — The numeric safety flag walked past percentages, ages, and inline-noun rates
**Rule:** `profiles/emt.md` §6 — *every* number, dose, threshold and time window gets `needs_human_check: true`, because a wrong digit is a safety error, not a typo. **Caught by:** `check_cards.py VALUE` + `verify_report.py` (which derives the flag from it). Found 2026-07-31 during the Chapter 7 run, independently by two unit editors.

`needs_human_check` is *derived*, never asserted (`reference/provenance.md`), and the whole derivation rests on one regex. Three holes in it meant a card could hand-assert `numeric: true` and have `verify_report.py` silently derive it back to `false` — the card then landed in "Section B: verified, skim" instead of "Section A: needs your eyes." The flag was reporting safety it was not delivering.

1. **Every percentage in the book.** The branch was `\d+\s*(?:…|%|…)\b`. `%` is not a word character, so the trailing `\b` can never match after it — the alternative was dead code from the day it was written. `25%`, `5% to 10%`, `90%`, `60%`, `50%`, `10% to 20%` all escaped. (Ranges like `5% to 10%` were rescued by the unrelated range branch; bare percentages were not.)
2. **Ages stated in months or years** — how a life-span chapter states nearly every fact. `28 months`, `2 months`, `61 years and older` carried no recognised unit. Chapter 7 is age bands end to end, so this was most of the chapter.
3. **Rates with the counted noun inline.** The unit list had `/min`, which requires the digits to sit against it; this book writes `140 beats/min` and `60 breaths/min`.

- **MUST CATCH:** a bare percentage · a **stated** age or duration in months/years/weeks/days (`28 months`, `61 years and older`) · a rate written `N <noun>/min` · a measured decimal (`98.6`) · weights (`6 to 8 pounds`, `30 g`).
- **MUST NOT OVER-FLAG:** a bare list ordinal (`1. Detection`, `Step 3`), a word ordinal with no digit (`the third month`), a cross-reference (`Chapter 29`), or prose carrying no digit at all. Widening the unit list must not turn ordinary text numeric.
- **Deliberately NOT caught: the hyphenated patient descriptor** (`a 2-month-old`, `a 30-year-old adult`, `an 82-year-old`). The separator is a hyphen rather than whitespace, so the age branch does not reach it — and that is the wanted behaviour, not a residual hole. This form is how a **vignette names its patient**, and a vignette age is invented scene-setting, not a value Parker must check against the book. Flagging it would push every scenario card into "Section A: needs your eyes" and dilute the section that exists to concentrate his attention on real digits. The genuinely dangerous numbers — ranges, doses, percentages, and *stated* thresholds like `by age 75` — are all caught by other branches even when a descriptor sits on the same card. (Raised by the Chapter 7 judge as an R24 shortfall; resolved as a scope decision rather than a widening.)
- **Catch test (both ways):** four cases in `test_regressions.py` (`r24_*`) — three values that must now flag, one ordinal-only card that must stay silent.
- **Known, pre-existing, and harmless:** the range branch `\d+\s*(?:to|-|–)\s*\d+` also matches a figure label like `FIGURE 7-2`. Card text may never contain a source-artifact word (card-rules Layer A #2), so a legal card cannot trip it. Not introduced by this fix and deliberately left alone.

## R35 — An authored definition the source can't confirm must arrive FLAGGED
**Rule:** card-rules #28 (the purple lane). **Caught by:** `check_cards.lexicon_check` (HARD) + `verify_report.py` (which derives the flag — the gate enforces the two scripts agree).
The purple lane is the first place the pipeline is LICENSED to author content the source never states (a plain-language definition). The license is conditional: an `external`-anchored definition must carry `needs_human_check` so it lands in the verify report's Vocabulary block under Parker's eyes. A card that authors a definition AND declares itself clean has stepped outside the license.
- **BAD:** `kind: lexicon`, `anchor.method: "external"`, `needs_human_check: false` → must HARD-block.
- **GOOD (must not over-flag):** the same card with the derived flag true → passes.
- **Catch test:** executable — `r35_*` in `test_regressions.py`.

## R36 — The lexicon lane cannot be SELF-asserted (kind must match the marks' kind)
**Rule:** card-rules #28. **Caught by:** `check_cards.lexicon_check` (HARD, both directions).
`kind` decides which grounding contract a card answers to — word-overlap (R13) or anchor (R35/R37) — so if the drafter could choose it freely, either contract could be dodged: a yellow-built card claiming `lexicon` escapes R13's support test; a purple-built card claiming `text` smuggles an authored definition past the anchor contract. The extractor sets each MARK's kind from its color, and the gate requires the card's claim to agree with the marks it cites. Same anti-self-assertion lesson as R33's visual exemption.
- **BAD:** `kind: text` citing ONLY `kind: lexicon` marks → HARD. **BAD:** `kind: lexicon` citing a yellow mark → HARD.
- **GOOD (must not over-flag):** a Stage-2.5 fold-in — `kind: text` citing purple AND yellow marks together — is the legitimate mixed case and must pass.
- **Catch test:** executable — `r36_*` in `test_regressions.py`.

## R37 — A claimed in-source anchor must RESOLVE to mechanically-extracted evidence
**Rule:** card-rules #28. **Caught by:** `check_cards.lexicon_check` (HARD).
A `glossary`/`in_source` anchor exempts a lexicon card from the external-tier flag, so the anchor is an exemption surface — and R33 taught that an exemption the drafter can assert by typing a sentence is no exemption at all. The evidence must exist in `work/<source>/lexicon_evidence.json` with a non-empty quote and page, and that file is written only by `lexicon.py --find`, which QUOTES the PDF itself.
- **BAD:** `anchor.method: "in_source"` for a term_key with no evidence entry → must HARD-block.
- **GOOD (must not over-flag):** the same claim for a term_key whose entry resolves (permanent fixture: `work/_regression/lexicon_evidence.json`) → passes.
- **Catch test:** executable — `r37_*` in `test_regressions.py`.

## R38 — A page can be densely OCR'd and still be missing the TARGET LANGUAGE entirely
The Arabic textbook (source `arabic`, 2026-08-08) is a scan whose OCR captured only the
English: all 251 pages together contain ZERO Arabic codepoints, yet every Unit 1 mark came
back `grounding: EXACT` / `content: FULL` because the English prose around each mark is
dense. The `needs_visual` heuristic (CAPTION_ONLY / SPARSE_PAGE) never fired — the pages
are not sparse, they are missing one script. Every Arabic-bearing card had to be grounded
by page-render transcription + external authority (Lingco publisher JSON) instead.
- BAD (must catch): a card whose cloze answer contains codepoints from a script that appears
  NOWHERE in the cited context, shipped with no `visual_source`/`image`/external evidence.
- GOOD (don't over-flag): the same card carrying a back-side source crop (`image`) or a
  `verified_against` naming an external authority snapshot in `work/<source>/`.
- Mechanization direction (next session): per-source `force_visual` flag in the registry +
  a script-mismatch check in `check_cards.py` (answer-script ∉ context-script ⇒ require evidence).

## R39 — RTL text: a MIXED line scrambles; a PURE line is safe (and `<div dir>` is not the fix)
Verified in-browser 2026-08-08 (Alif Baa run): Arabic and Latin on ONE line reorder
unpredictably around neutrals (parens, `=`, digits); a line that is 100% one script renders
correctly inside Anki's LTR field with gate-legal HTML only. `<div dir="rtl">` also fixes it
but `div` is outside ALLOWED_TAGS and HARD-blocks.
- BAD (must catch): a Text or Back Extra LINE (between `<br>`s) mixing Arabic codepoints with
  Latin words/digits — except single bare glyphs in a name-keyed Distinguish list, whose
  visual reversal is harmless because the explanation keys on letter NAMES, not positions.
- GOOD (don't over-flag): pure-Arabic line followed by pure-Latin line; `{{c1::أَهلاً}}` alone
  on its line; transliteration lines that contain no Arabic script.
- Also record: translit is ANSWER-SIDE ONLY (it gives pronunciation away on both card
  directions); diacritics ride a carrier letter (بَ), never bare, never on U+25CC (tofu).
