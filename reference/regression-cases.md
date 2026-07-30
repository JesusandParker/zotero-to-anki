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

---

*To add a case: when Parker catches something new, record the BAD card, the GOOD fix, the rule it enforces, and the concrete catch test. Then confirm the checker or judge actually catches it before considering it closed.*
