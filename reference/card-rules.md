# EMT Card Rules

The standard every generated card must meet. Two layers:

- **Layer A — Form** (the v60 gates that already worked; keep them).
- **Layer B — Judgment** (what v60 lacked; this is where the audit found the real failures).

A card ships only if it passes **both** layers. Layer B is enforced by the Editor stage (`editor-checklist.md`).

---

## Layer A — Form (keep what v60 got right)

The audit of the old deck showed these were already near-perfect (deixis 0.4%, source-artifact words 0.1%, 0% over-length). Hold the line:

1. **One note = one topic.** Every cloze in a note shares a single topic. Two topics = two notes.
2. **Standalone.** The card must make sense with zero access to the textbook.
   - No deixis / anaphora: never "this," "these," "the following," "as shown," "above/below," or a dangling "it/they" whose referent isn't named in the same sentence.
   - Never start a sentence or a Back Extra line with *This / That / These / It / They / Here / There*. Repeat the noun instead.
   - No source artifacts: never reference a source medium — "figure, table, chart, graph, diagram, label, image, picture, slide, chapter, page, recap, summary, review" — or position words "above / below / shown here / as shown / the following." The figure/table is the *source* of a fact, never something Parker must see or recall; anchor on the concept ("IgG antibody functions"), not the medium ("the antibody table").
3. **Human-flow sentences.** Write like a tutor speaking, not note-shorthand. First line is a complete sentence with a real verb. Prefer "X is/does…" over "X: …". Colons only in the sequence format "Process Name (Step N): …".
4. **Hints are slot-labels, never the answer.** `{{c1::answer::hint}}` where the hint names the *category/form* of the answer ("enzyme", "year", "organ", "T/F", "protective or risk"), never a synonym, definition, or paraphrase. **Hint-leak check:** if the hint could replace the answer and mean the same thing, it's invalid — fix or omit. A direction/binary blank (increase/decrease, indicated/contraindicated, can/cannot) MUST carry a forced-choice `::option/option` hint — an unhinted coin-flip is unanswerable. (Full EMT hint flavors: `card-recipes.md` §2.)
5. **Back Extra is required and must add something new.** 1–3 labeled lines, each opening with one of: `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:`. **Separate distinct components with a paragraph break `<br><br>`, never a single `<br>`** (Parker's aesthetic, 2026-07-02 — real white space so his eye jumps between parts; `anki_write.py` enforces it at write time). It must teach an edge the Text doesn't already state. For a definition card, Back Extra may NOT re-define the term (use Distinguish / Pitfall / Ex / Cue). Priority when choosing: Distinguish/Pitfall > Mechanism/Why > Ex > Cue > Pathway > Mnemonic.
6. **Length.** Aim 12–35 words; hard max 60. Over that, split. Max 2 sentences, no semicolon run-ons.
7. **Zero guessing.** If the source text is unreadable, ambiguous, or you'd have to invent a fact to finish the card — STOP. Flag it (see Layer B rule 9). Never fabricate. (Especially true for anything clinical.)

---

## Layer B — Judgment (the audit's findings; this is the new work)

Each rule below cites a real failure so the reason is concrete. **Rule 0 gets read first, every time.**

0. **Connected-highlight synthesis — CHECK THIS BEFORE DRAFTING ANYTHING.**
   Before you card a highlight, look at the highlights right around it. Parker often highlights several short spans — consecutive bullet lead-ins, parallel terms, or the pieces of one explanation under a single heading — that together form ONE bigger idea. When highlights are adjacent (same page, consecutive in order, overlapping context) and parallel, **synthesize them into one unified card that captures the whole concept**, not isolated fragment cards. Read the shared context paragraph: if the spans are the skeleton of a single point, make the single point.
   *Failure that created this rule (2026-06-29):* "Scene size-up / Patient assessment / Treatment / Transport" were four highlighted bullet lead-ins under one heading ("EMT Training: Focus and Requirements") — the arc of every call. The system wrongly made two isolated cards and **dropped** the other two, instead of one card on the four core EMT functions. The fix was the single card: "The core work of an EMT on a call follows four steps: scene size-up, patient assessment, treatment, transport."

1. **Yield filter — phrase around the real fact, but NEVER overrule a highlight.**
   Within a highlight, decide *which clause* carries the testable knowledge and build the card around that, not around soft connective filler. But do **not** drop an entire highlighted span as "trivia" — Parker highlighted it on purpose; the green mark *is* the decision that it matters. If a span looks thin on its own, that is almost always Rule 0 (it's one leg of a connected set), so zoom out first. If a whole highlight still seems genuinely un-cardable after that, **flag it** (`needs_human_check`) for Parker — never silently discard it.
   *v60 phrasing failure:* "A nicotine-cessation plan should address challenges that may `[trigger product use]`." — build the card around the real fact, don't cloze filler.
   → A green highlight is something worth a card; your job is to render it well, not to veto it.

2. **One-answer rule.** With the cloze hidden, the visible stem must point to **exactly one** correct answer. If several answers fit, the stem is too vague — rewrite it (add the constraining detail) or drop it.
   *v60 failure:* "A core goal of CQI is `[minimizing errors]`." (Improving care, quality, safety all fit.)

3. **No tautology / no leakage — context cues the question, never the answer.** The answer must not be stated, echoed, defined, or obviously implied by ANY visible part of the card — stem, `::hint`, OR a parenthetical / appositive / descriptor. The deep version of this rule (the leak-vs-crutch median): because Parker studies one shuffled megadeck, every card needs enough **situational / relational** context (where, when, in what process, related to what) to be answerable in isolation — but that context must NEVER be the hidden answer's own **definition, synonym, or paraphrase**, which lets him *decode* the answer instead of *recall* it (a crutch he stops testing against). Definitional/distinguishing content that would reveal the answer goes in the **Back Extra** (shown after he answers), not the stem; the answer's *form* goes in a slot-label hint (category/form), never its content.
   *Leak via parenthetical (slips past a `::hint`-only check):* "...{{c1::licensure}} (state authority granted)..." — the parenthetical IS the definition of licensure. Fix: strip it, keep the situational framing ("the pathway to practicing as an EMS provider, in order"), move each definition to the Back Extra.
   *Calibration — don't over-correct into uselessness:* the median is ONE test — a student who KNOWS the fact can answer from the stem alone, while one who does NOT cannot decode it from the stem alone. Too vague to answer → add situational (not definitional) context. Decodable without knowing → strip the definitional leak. Target: *maximal situational context, zero definitional content.*
   *Precision (so this never over-fires):* the leak is only the HIDDEN answer's definition sitting VISIBLE. Definitional content is fine when it is hidden inside a cloze, attached to a DIFFERENT shown term, or in the Back Extra — so a **two-way definition card** (`{{c1::TERM}} is {{c2::meaning}}`, both halves clozed) is NOT a leak and must never be "fixed." When stripping a real leak would leave a must-test fact untested, don't just dump it in the Back Extra — re-test it as a two-way definition (which tests it without a visible crutch).
   *v60 failures:* "An organ donor is a person who has expressed a wish to `[donate organs]`." / "Violence prevention includes … `[threats of violence]`."

4. **List rule — test every item, never "cloze one and reveal the rest."**
   When the source lists N parallel items, every item must be tested. Choose deliberately:
   - **Sibling cards:** N cards, each hiding a *different* item with the others shown as context (best when each item is independently high-yield), or
   - **One grouped card (the default for a cohesive list):** hide the whole set under the *same* cloze number `{{c1::A}}, {{c1::B}}, {{c1::C}}`. Use this for any list whose items belong together as a unit, regardless of length (Parker's preference — see rule 6). Reach for sibling cards only when the items are really independent facts that merely happen to be listed.
   Never `{{c1::A}}, B, C, D` — that tests A and gives away B/C/D for free.
   *v60 failure:* "…frontal, parietal, occipital, and `[temporal]` lobes." (3 of 4 lobes never tested.)

5. **Crisp-cloze rule.** Delete a tight keyword, number, or term — not a long fuzzy phrase you could never recall verbatim.
   *v60 failure:* "Eustress can increase `[focus and short-term energy]`." → cloze the crisp concept, not the phrase.

6. **Cohesive lists stay whole; don't cram unrelated facts.** A genuine cohesive list — parallel members of one set, or the steps of one process — goes in ONE card no matter how many items (Parker confirmed 2026-06-29: keep a real list together, don't split it; e.g. the Star of Life's 6 functions, the EMS Agenda 2050's 6 principles). The only thing to avoid is forcing *unrelated/independent* facts into one card just to bundle them — those stay separate cards. Test before bundling: "are these truly one set, or am I lumping unrelated things together?"

7. **Under-clozing check.** Within the highlighted passage, every *distinct testable* fact gets tested somewhere (this card or a sibling). Don't leave a clozable fact sitting in plain text.
   *v60 failure (the "didn't cloze cytosine" bug):* 82.5% of long old cards clozed only one thing.

8. **Card-type variety.** Where the content supports it, go beyond fill-in-the-blank: definition, comparison (X vs Y), mechanism/causal chain, ordered steps, classification, **clinical vignette/application**, negation/exception. EMT is an *application* exam; rehearse reasoning, not just recognition. **Pick the archetype with `card-recipes.md`** (the playbook), then drill into `cloze-mastery.md` for more exemplars.
   *v60 failure:* 88% were single-cloze factoids; zero vignette/compare/reasoning cards.
   Note (encoding specificity): retrieval practice does NOT reliably train the *untested* direction, so if both directions are real goals, make both — this is why definitions are two-way (parker-preferences.md), while facts needed only one way (scenarios, numbers, lists) are not reversed.

9. **Confidence & safety flag.** If grounding is weak (the extractor marked it `PARTIAL`/`NOT_FOUND`) or the fact is a **number/dose/threshold**, mark the card `needs_human_check: true` and surface it to Parker rather than trusting it silently. A wrong digit on a dose is dangerous.

10. **Ground every claim.** Every fact on the card must be supported by the highlight's `context` paragraph from the extractor. Do not add outside facts the source doesn't support. If the context is too thin to make a correct card, that's rule 7-of-Layer-A (flag, don't guess).

11. **Prerequisite closure — no card that only makes sense in source/lecture context.** If a card's stem or answer leans on a term not defined within its own visible text (and not already its own card), either fold a one-clause definition into the card so it stands alone, or make a short sibling definition card for that term. This is the fix for Parker's "wonky cards that only make sense in slide context." Stay grounded: only add a definition the `context` paragraph (or an adjacent highlight) supports — if the prerequisite isn't in the source, flag `needs_human_check` rather than inventing it.

12. **Dedupe by meaning (recaps are coverage checks, not a card factory).** Before staging, compare each new card's *claim* against the others in this chapter's batch. If two highlights test the same fact (e.g. one in the body, one in an end-of-chapter recap), make ONE card and keep the clearer phrasing. This is *not* dropping a highlight (Rule 0 / rule 1) — the fact is still carded once and both highlights are covered; it's the same-fact consolidation Rule 0 already does for adjacent duplicates. Only make a second card if the recap adds a genuinely new qualifier. Dedupe by meaning, not wording.

13. **No cross-card give-away (the sibling-leak).** A scenario/classify card must not be answerable by pattern-matching a *neighbor* card. If the exact example you use in a "classify this" card also appears as an `Ex:` line (or a definition) on a sibling card in the same batch, a student answers by recognition, not reasoning — the interference makes both cards feel learned before they are. Use a **fresh exemplar** for each scenario card, distinct from the examples on its definition siblings.
    *Failure that created this rule (2026-07-01):* Ch2 "classify the contact route" reused the *identical* blood-into-a-cut / stethoscope examples that its direct/indirect definition cards already gave in their `Ex:` lines. Fixed with fresh scenarios (weeping skin lesion; reused stethoscope).

14. **List completeness against the FULL source — not just the context window.** When a highlight introduces an enumerated list (the extractor marks it `list_lead_in: true`), the 450-char context can cut the list off — and a list that spills across a page break is invisible to a one-page read. Before you commit a count or a list card, read the WHOLE list off the source page(s) and test every item. A stated count that doesn't match the number of clozed items is the alarm (`check_cards.py` flags an undercount).
    *Failure that created this rule (2026-07-01):* the decision-making-capacity card said "7 factors" and clozed 7, but the textbook lists **8** — the 8th ("significant distracting injury") was on the next page, past the context window, and Parker had written "Know all of these!!" beside it. Fixed the extractor to pull the next page for lead-ins, and the card to all 8.

15. **Scenario→action cards: cloze the load-bearing words, not the whole clause.** A "what do you do next" vignette tends to hide an entire sentence (`{{c1::Park a heavy vehicle so it blocks traffic in that lane}}`) — an answer no one can recall verbatim (violates rule 5, crisp-cloze). Keep the situational stem visible and delete only the 1–3 words that carry the decision (`park a {{c1::heavy vehicle}}`).
    *Failure that created this rule (2026-07-01):* several Ch2 scenario cards (highway blocker, orient-the-patient, let-parents-hold-the-child) hid whole sentences. Fixed to crisp keyword clozes.

---

## The Cold-Solve Gate (rules 16–18) — read together, they are the anti-ambiguity core

These three came from Parker studying the deck and hitting cards that were **impossible to answer on first sight even though he knew the material** — "I had no chance, it was a set-up for failure." They are all facets of one demand: **a knower must be able to produce the exact answer from the visible side ALONE, the first time, having never seen the card.** That is the *cold-solve test*. It is the strict, load-bearing form of the "cue, not crutch" median (rule 3): rule 3 guards the *crutch* side (too much cue); these guard the *impossible* side (too little cue, or the cue destroyed). Run the cold-solve test on **every** card: cover the answer, and ask "could I have written exactly this, cold?" If no, the card fails — fix it.

16. **No open-set cloze — the answer must be forced, not one of many plausible fills.** With the cloze hidden, the visible stem must constrain the answer to **essentially one** producible response. If the blank could be filled by many different true things and nothing visible singles out the intended one, the card is unanswerable-cold and must be rewritten. This is rule 2 (one-answer) sharpened for the *open universe* case: not "are there 2–3 near-synonyms" but "is the answer space wide open?"
    - **The two open-set shapes to kill:**
      - *"List N things that [broad category]"* with no anchor — "her religious convictions strongly oppose `{{c1::medications, blood, and blood products}}`." A religion can oppose countless things; nothing points to *these three*. **Fix by anchoring:** name the entity that makes the answer inevitable ("A **Jehovah's Witness** patient refuses `{{c1::blood and blood products}}`"), or flip to the constrained direction (give the refused items, recall the implication), or if it is genuinely a memorize-this list, ensure the *parent* is specific enough that the set is closed and derivable.
      - *"You must [do what]"* / open action blank — "Beyond respecting her wishes, you must `{{c2::report the objection to the next level of care}}`." Many EMT actions fit that hole. **Fix:** put the discriminating situation in the visible stem so exactly one action is right, and cloze only the load-bearing verb+object, or name the protocol/step so the action is forced.
    - **Do NOT over-correct:** a genuinely closed taxonomy the source names ("the three types of X are…") is answerable-cold by a knower and is fine — the test is whether the answer universe is *open*, not whether recall is *hard*. Hard-but-forced is the target; open-ended is the defect.
    *Failure that created this rule (2026-07-19):* the Jehovah's-Witness religious-objection card (both the "3 items" blank and the "you must…" blank were open-set). Regression **R9**.

17. **No all-blanks-at-once husk — never co-cloze mutually-dependent spans under the SAME number.** If two substantial spans each supply the *other's* only context, hiding both under one cloze number guts the stem into an unanswerable husk. Put them under **different** numbers (c1, c2) so each resulting card reveals one span as the anchor and tests the other — the two-way pattern (rule 3 precision; parker-preferences two-way defs). A single cloze group should not hide so much that the visible remainder no longer points to anything.
    - **BAD:** `The lawsuit defense of {{c1::governmental immunity}} generally applies only to EMS systems operated by {{c1::municipalities or other governmental entities}}.` — both halves are c1, so the front reads "the lawsuit defense of ___ applies only to systems operated by ___"; each blank's only cue is the *other* blank, which is also gone. Impossible cold.
    - **GOOD:** make them c1 and c2 → two cards. Card A shows "governmental immunity," asks the operator type; Card B shows "operated by municipalities/governmental entities," asks the defense name. Each is forced.
    - **Litmus:** cover everything hidden under one number. If what remains visible is mostly connective scaffolding ("the ___ of ___ applies to ___"), the cloze is a husk — re-number or re-scope.
    *Failure that created this rule (2026-07-19):* the governmental-immunity card. Regression **R10**.

18. **Hints label the answer's FORM; a first-letter hint is licensed ONLY for a spelled mnemonic.** A hint may name the answer's category, count, unit, or forced-choice options — never leak its content (rule 4). The specific trap: a **first-letter hint** (`::r`, `::k`) is legitimate ONLY when the item set is a *named/spelled acronym the card is teaching* (SAMPLE, DCAP-BTLS) — there the letters ARE the memory hook and the acronym is visible in the stem. On an **ordinary categorical list**, a first-letter hint collapses recall to "the obvious word starting with that letter" — a giveaway copout, not a form-label.
    - **BAD:** `three sources of medical error: {{c1::rules-based failure::r}} / {{c1::knowledge-based failure::k}} / {{c1::skills-based failure::s}}` — no spelled acronym; `::r` just hands over "rules-based."
    - **GOOD:** drop the letter hints. Better still, expose the shared structure and cloze only the distinguishing word: `medical errors come from three sources: a {{c1::rules}}-based, a {{c1::knowledge}}-based, or a {{c1::skills}}-based failure.` The "-based failure" scaffold stays visible; the recall is the three crisp discriminators, with no letter leak.
    - **Test:** if the hint equals the first letter(s) of its own answer AND the stem contains no spelled acronym those letters build, the hint is a leak — remove it.
    *Failure that created this rule (2026-07-19):* the three-sources-of-medical-error card. Regression **R11**.
