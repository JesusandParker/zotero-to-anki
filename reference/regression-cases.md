# Regression Cases — the failure library (tests, not just rules)

Every flaw Parker has caught becomes a permanent test here: a **BAD** card the checks must catch, and (where over-correction is a real risk) a **GOOD** card they must *not* flag. When `card-rules.md`, `check_cards.py`, or the LLM judge changes, re-validate against these so nothing regresses. This is how "I hope it doesn't recur" becomes "it can't — there's a test for it."

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

---

*To add a case: when Parker catches something new, record the BAD card, the GOOD fix, the rule it enforces, and the concrete catch test. Then confirm the checker or judge actually catches it before considering it closed.*
