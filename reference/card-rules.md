# Card Rules

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
4. **Hints are slot-labels, never the answer.** `{{c1::answer::hint}}` where the hint names the *category/form* of the answer ("enzyme", "year", "organ", "T/F", "protective or risk"), never a synonym, definition, or paraphrase. **Hint-leak check:** if the hint could replace the answer and mean the same thing, it's invalid — fix or omit. A direction/binary blank (increase/decrease, indicated/contraindicated, can/cannot) MUST carry a forced-choice `::option/option` hint — an unhinted coin-flip is unanswerable. (Full hint flavors: `card-recipes.md` §2.)
5. **Back Extra is required and must add something new.** 1–3 labeled lines, each opening with one of: `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:` `Roster:` (the last is reference, goes last, and is required on any note from a chunked list — rule 23). **Separate distinct components with a paragraph break `<br><br>`, never a single `<br>`** (Parker's aesthetic, 2026-07-02 — real white space so his eye jumps between parts; `anki_write.py` enforces it at write time). It must teach an edge the Text doesn't already state. For a definition card, Back Extra may NOT re-define the term (use Distinguish / Pitfall / Ex / Cue). Priority when choosing: Distinguish/Pitfall > Mechanism/Why > Ex > Cue > Pathway > Mnemonic.
6. **Length.** Aim 12–35 words; hard max 60. Over that, split. Max 2 sentences, no semicolon run-ons.
7. **Zero guessing.** If the source text is unreadable, ambiguous, or you'd have to invent a fact to finish the card — STOP. Flag it (see Layer B rule 9). Never fabricate. (Especially true for anything clinical.)

---

## Layer B — Judgment (the audit's findings; this is the new work)

Each rule below cites a real failure so the reason is concrete. **Rule 0 gets read first, every time.**

0. **Connected-highlight synthesis — CHECK THIS BEFORE DRAFTING ANYTHING.**
   Before you card a highlight, look at the highlights right around it. Parker often highlights several short spans — consecutive bullet lead-ins, parallel terms, or the pieces of one explanation under a single heading — that together form ONE bigger idea. When highlights are adjacent (same page, consecutive in order, overlapping context) and parallel, **synthesize them into one unified card that captures the whole concept**, not isolated fragment cards. Read the shared context paragraph: if the spans are the skeleton of a single point, make the single point.
   *Failure that created this rule (2026-06-29):* "Scene size-up / Patient assessment / Treatment / Transport" were four highlighted bullet lead-ins under one heading ("EMT Training: Focus and Requirements") — the arc of every call. The system wrongly made two isolated cards and **dropped** the other two, instead of one card on the four core EMT functions. The fix was the single card: "The core work of an EMT on a call follows four steps: scene size-up, patient assessment, treatment, transport."

1. **Yield filter — phrase around the real fact, but NEVER overrule a highlight.**
   Within a highlight, decide *which clause* carries the testable knowledge and build the card around that, not around soft connective filler. But do **not** drop an entire **yellow** span as "trivia" — Parker highlighted it on purpose; the yellow mark *is* the decision that it matters. (This rule covers yellow ONLY. Blue is his personal reading emphasis, deliberately not card material — it never reaches you and is never a "dropped" span. **Purple DOES reach you**, as `kind: "lexicon"` — a different lane with its own contract, rule 28, including the lane's own narrow triage license. See SKILL.md "What counts as card me.") If a span looks thin on its own, that is almost always Rule 0 (it's one leg of a connected set), so zoom out first. If a whole highlight still seems genuinely un-cardable after that, **flag it** (`needs_human_check`) for Parker — never silently discard it.
   *v60 phrasing failure:* "A nicotine-cessation plan should address challenges that may `[trigger product use]`." — build the card around the real fact, don't cloze filler.
   → A yellow highlight is something worth a card; your job is to render it well, not to veto it.

2. **One-answer rule.** With the cloze hidden, the visible stem must point to **exactly one** correct answer. If several answers fit, the stem is too vague — rewrite it (add the constraining detail) or drop it.
   *v60 failure:* "A core goal of CQI is `[minimizing errors]`." (Improving care, quality, safety all fit.)

3. **No tautology / no leakage — context cues the question, never the answer.** The answer must not be stated, echoed, defined, or obviously implied by ANY visible part of the card — stem, `::hint`, OR a parenthetical / appositive / descriptor. The deep version of this rule (the leak-vs-crutch median): because Parker studies one shuffled megadeck, every card needs enough **situational / relational** context (where, when, in what process, related to what) to be answerable in isolation — but that context must NEVER be the hidden answer's own **definition, synonym, or paraphrase**, which lets him *decode* the answer instead of *recall* it (a crutch he stops testing against). Definitional/distinguishing content that would reveal the answer goes in the **Back Extra** (shown after he answers), not the stem; the answer's *form* goes in a slot-label hint (category/form), never its content.
   *Leak via parenthetical (slips past a `::hint`-only check):* "...{{c1::licensure}} (state authority granted)..." — the parenthetical IS the definition of licensure. Fix: strip it, keep the situational framing ("the pathway to practicing as an EMS provider, in order"), move each definition to the Back Extra.
   *Calibration — don't over-correct into uselessness:* the median is ONE test — a student who KNOWS the fact can answer from the stem alone, while one who does NOT cannot decode it from the stem alone. Too vague to answer → add situational (not definitional) context. Decodable without knowing → strip the definitional leak. Target: *maximal situational context, zero definitional content.*
   *Precision (so this never over-fires):* the leak is only the HIDDEN answer's definition sitting VISIBLE. Definitional content is fine when it is hidden inside a cloze, attached to a DIFFERENT shown term, or in the Back Extra — so a **two-way definition card** (`{{c1::TERM}} is {{c2::meaning}}`, both halves clozed) is NOT a leak and must never be "fixed." When stripping a real leak would leave a must-test fact untested, don't just dump it in the Back Extra — re-test it as a two-way definition (which tests it without a visible crutch).
   *v60 failures:* "An organ donor is a person who has expressed a wish to `[donate organs]`." / "Violence prevention includes … `[threats of violence]`."

4. **List rule — test every item, never "cloze one and reveal the rest."**
   When the source lists N parallel items, every item must be tested. Two shapes are legal, and **which one you pick is decided by rule 23 (retrieval load), not by taste**:
   - **One grouped card:** hide the whole set under the *same* cloze number `{{c1::A}}, {{c1::B}}, {{c1::C}}`. The default for a cohesive list that fits in one retrieval.
   - **Separate NOTES:** when the set is too big for one retrieval, chunk it across notes (rule 23). Each note still uses ONE cloze number for its own sub-set.
   Never `{{c1::A}}, B, C, D` — that tests A and gives away B/C/D for free. And never `{{c1::A}}, {{c2::B}}, {{c3::C}}` on one note either — see rule 24, which is the same defect wearing a fix's clothes.
   *v60 failure:* "…frontal, parietal, occipital, and `[temporal]` lobes." (3 of 4 lobes never tested.)

5. **Crisp-cloze rule.** Delete a tight keyword, number, or term — not a long fuzzy phrase you could never recall verbatim.
   *v60 failure:* "Eustress can increase `[focus and short-term energy]`." → cloze the crisp concept, not the phrase.

6. **Cohesive lists stay whole *up to one retrieval's worth*; don't cram unrelated facts.** A genuine cohesive list — parallel members of one set, or the steps of one process — is ONE concept and must never be scattered into unrelated shards. But "one concept" and "one card" are different claims, and **rule 23 sets the ceiling**: past ~4 uncued answers the set is chunked across notes that each keep the whole set in view. The thing to avoid in the other direction is forcing *unrelated/independent* facts into one card just to bundle them. Test before bundling: "are these truly one set, or am I lumping unrelated things together?" — then test again: "can he actually produce all of them in one breath?"
   *Amended 2026-08-02.* This rule previously read "in ONE card no matter how many items," from Parker's 2026-06-29 call on the Star of Life. That instruction was right about *cohesion* and wrong about *capacity*, and it is what generated the 10-element radio-report card he later reported as impossible. See rule 23 for the measurement that settled it.

7. **Under-clozing check.** Within the highlighted passage, every *distinct testable* fact gets tested somewhere (this card or a sibling). Don't leave a clozable fact sitting in plain text.
   *v60 failure (the "didn't cloze cytosine" bug):* 82.5% of long old cards clozed only one thing.

8. **Card-type variety.** Where the content supports it, go beyond fill-in-the-blank: definition, comparison (X vs Y), mechanism/causal chain, ordered steps, classification, **vignette/application**, negation/exception. **Pick the archetype with `card-recipes.md`** (the playbook) and the mix with the source's profile (`reference/profiles/`), then drill into `cloze-mastery.md` for more exemplars. Where the material is assessed by *applying* it rather than reciting it, rehearse reasoning, not just recognition.
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

19. **A list of things to produce must LOOK like a list — one item per line, blank line between.**
    When a card's Text is a list of items Parker must produce (a lead-in, then the members), lay
    the rows out with `<br><br>` between them, not a single `<br>`. Packed rows render as one grey
    block and hide the single most useful piece of information on the front: **how many answers he
    owes.** He answers these by first counting the blanks, then producing them.
    - **BAD:** `The structured handover format <b>SBAR</b> stands for:<br>{{c1::Situation::S}}<br>{{c1::Background::B}}<br>{{c1::Assessment::A}}<br>{{c1::Recap/Rx::R}}`
    - **GOOD:** the same card with `<br><br>` between every row, so four distinct blanks are visible at a glance.
    - **Applies to** any layout where the lines after the lead-in are *rows* — a line carrying a
      cloze and almost no prose of its own (numbering and bullets are layout, not prose). Numbered
      protocols, grouped-reveal sets, mnemonic expansions, and contrast pairs all qualify.
    - **Does NOT apply to prose.** A card that uses `<br>` to separate two flowing sentences is not
      a list; leave it alone. The test is whether the lines are *parallel members of a set*.
    - Mechanically guaranteed by `listify()` in `anki_write.py` (the Text-field twin of
      `paragraphize()` for Back Extra), and warned by `check_cards.py`, so the spacing holds even
      if a card is drafted tight. Regression **R14**.
    *Preference that created this rule (2026-07-30):* Parker showed before/after screenshots of the
    SBAR card — "for me to be able to be prompted to guess these questions and then immediately see
    in a very clear way how many things I need to guess."

---

## The Cold-Solve Gate (rules 16–18, 20–22) — read together, they are the anti-ambiguity core

These came from Parker studying the deck and hitting cards that were **impossible to answer on first sight even though he knew the material** — "I had no chance, it was a set-up for failure." They are all facets of one demand: **a knower must be able to produce the exact answer from the visible side ALONE, the first time, having never seen the card.** That is the *cold-solve test*. It is the strict, load-bearing form of the "cue, not crutch" median (rule 3): rule 3 guards the *crutch* side (too much cue); these guard the *impossible* side (too little cue, or the cue destroyed). Run the cold-solve test on **every** card: cover the answer, and ask "could I have written exactly this, cold?" If no, the card fails — fix it.

> **Run the cold-solve test PER ROW, not per card (2026-07-30).** Rules 16–18 were written and enforced at card granularity, and that is exactly how the next round of failures hid: on a multi-row card, the card as a whole looks answerable while *individual rows* are self-answering or wide open. Parker's two July-30 complaints were both row-level failures on cards that pass a whole-card glance. **Every row of a list card gets its own cold-solve test**, and rules 20–22 below are the three row-level shapes that keep recurring. A card is only as good as its worst row.

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

20. **A row label must CUE its answer, never restate it.** In a row shaped `LABEL → {{answer}}`, the label is the only cue the blank gets. If the label and the answer say the same thing, the row is a freebie dressed up as a hint; if the label says nothing (`Miscellaneous → …`), the row is open-set (rule 16). Both failures live on the same card and both are row-level, which is why a whole-card read misses them.
    - **BAD:** `Arrival at hospital or point of transfer (1) → {{c1::notify dispatch of arrival}}` — the answer is the label with a verb bolted on. Likewise `Return to service (1) → notify dispatch when {{c1::the unit is available for another call}}` (returning to service *means* being available for another call), and `Miscellaneous (1) → notify dispatch anytime the unit is {{c1::not in station}}` (nothing cues it at all).
    - **GOOD:** test what the label does NOT already say. Keep the rows whose message is genuinely not derivable from the phase (`En route → request {{c1::assistance with directions}} or {{c1::additional resources}}`; `On scene → {{c1::check in periodically as a safety measure}}`), and let the derivable ones go — a row that answers itself is not coverage, it is padding.
    - **Litmus:** read the label aloud, then the answer. If the second is a paraphrase of the first, delete the row or re-scope the card.
    - *Caught by:* `check_cards.py row_label_tautology` (a warning, deliberately generous — a shared stem is evidence, not proof; the judge clears the benign ones). It is NOT suppressed on classify/match cards: a real leak can sit inside an otherwise correct match card.
    *Failure that created this rule (2026-07-30):* the EMS-radio card. Parker: "the return to service is the thing I'm supposed to say, so you're giving away the answer while trying to give me a hint." Regression **R15**.

21. **An absolute or prohibition sentence needs an anchor or a slot-label hint.** A stem of the form *never / always / only / must not …* names a rule but does not constrain WHICH thing the rule is about, so a lone unhinted blank at the end of it is open-set (rule 16) in its most common disguise.
    - **BAD:** `You must never attribute a patient's altered mental status to {{c1::old age}}.` Parker: "there are a lot of things I could fit in that blank… since there was no hint, no other cues, nothing else, how am I supposed to know it?" *Sadness*, *skin color*, *being tired* all fit.
    - **GOOD, three ways** — (a) add a slot-label hint that names the answer's FORM: `…to {{c1::old age::a patient characteristic}}`; (b) add a visible contrast that names the rejected alternative: `'right' and 'left' always refer to the {{c1::patient's}} perspective, not the provider's`; (c) best, flip it to the positive fact and let a sibling cloze anchor the negation: `In an older patient with altered mental status, always assume {{c1::an underlying treatable cause}} — never {{c2::normal aging}}.`
    - *Caught by:* `check_cards.py open_set_absolute` — one unhinted, non-numeric blank in a sentence carrying an absolute, with no contrast anchor after the blank. This is the first mechanical proxy for R9, which had been judge-only since July and walked straight back into two later chapters because of it.
    *Failure that created this rule (2026-07-30):* the altered-mental-status card. Regression **R16**.

22. **Cloze the unit of knowledge, not a word inside it.** When the thing worth knowing is *that the item exists* — one of N questions to ask, one of N functions to name — then the ITEM is the answer. Showing the item and punching a filler word out of it drills recognition of a frame Parker will never be asked to reproduce, while the real recall goes untrained.
    - **BAD:** `run 8 self-check questions:` followed by all 8 questions visible, each missing one obvious word — `Are you {{c1::abandoning}} the patient?`, `Are you neglecting your {{c1::duty}}?`. Parker: "I can pretty much guess most of these… it doesn't actually help me remember this card, it just helps me remember the CONTEXT of the card."
    - **GOOD, in order of preference:** (a) if the items are crisp, cloze the items themselves as a grouped reveal (`{{c1::Signs and symptoms::S}}`, the SAMPLE shape); (b) if the items are too long to reproduce verbatim, **change the archetype** — test the organizing structure that makes the set derivable, and keep the full list in the Back Extra as reference; (c) add 1–2 application vignettes on the highest-yield members. Do NOT settle for clozing a filler word because the real answer is inconvenient.
    - **Not a violation:** a classify/match card (`description = {{c1::category}}`) — there the visible description IS the intended cue; or an item-then-descriptor row (`{{c1::Nasopharynx}} — above the soft palate`) — there the item leads and is already the answer.
    - **How to tell this from rule 18's endorsed 'expose the shared structure' shape**, which looks identical on the page. Rule 18 keeps a shared *scaffold* visible and hides the crisp discriminator (`a {{c1::rules}}-based failure`); rule 22 keeps the *content* visible and hides a filler word (`Are you {{c1::abandoning}} the patient?`). The mechanical line, which until 2026-08-03 existed only inside `fragment_clozed_list` and in no document: a row is the BAD shape when it hides **fewer words than it shows** and does not lead with its cloze. If the blank is the shorter, load-bearing part of the row, you are on rule 18's side; if the blank is the smaller part of a frame he will never be asked to reproduce, you are on rule 22's.
    - *Caught by:* `check_cards.py fragment_clozed_list` (≥3 rows, none leading with its cloze, each hiding fewer words than it shows, no classify lead-in).
    *Failure that created this rule (2026-07-30):* the 8-self-check-questions card. Regression **R17**.

---

## Retrieval load (rules 23–24) — a card must be PASSABLE, not just answerable

The Cold-Solve Gate asks whether each blank is *answerable*. These two ask a question it never asked: whether the card as a whole is **passable**. A grouped reveal is graded all-or-nothing — Parker presses one button for the entire set — so a card hiding N items is "Good" only when he produces every one of the N. At a realistic 90% per item that is 0.9^N: **59% at five items, 43% at eight, 35% at ten.** A card can therefore be built entirely from facts he knows cold and still fail essentially forever. Anki then compounds it by rescheduling the *whole card* on its worst item, re-drilling nine known items to chase one unknown — which is why he started skipping the card rather than answering it.

23. **A grouped reveal must be ONE retrieval — chunk the set, don't flatten it.**
    Count the answers under a single cloze number that carry **no per-item cue**. That count, not the list's length, is the load.
    - **≤4 uncued** — ship as one grouped card. This is working memory's honest capacity (Cowan's 4±1, not the folk 7±2).
    - **5–7 uncued** — ship whole ONLY if the set has a genuine **retrieval handle**: a spelled mnemonic the card teaches (SAMPLE, CHART, DCAP-BTLS), or a structure that regenerates the members (an anatomic pathway, a strict causal chain, a schema he already holds). No handle → chunk it.
    - **≥8 uncued** — chunk it. There is no card shape that legitimately demands eight uncued answers at once.
    - **A per-item cue lowers the *difficulty* of each row, but it does NOT make the card passable.** `Transports oxygen → {{c1::red blood cells}}` is a small independently-cued retrieval rather than part of one N-wide recall, so a keyed panel survives much longer than a bare list — but every row still hides and reveals under one number, so the card is still graded all-or-nothing. Converting a bare list into a keyed one is a real improvement; it is not an exemption. **A keyed panel of NUMBERS is the case where this matters most and gets its own rule — see 25.**
    **How to chunk, in preference order:**
    1. **Semantic partition (preferred).** Split into 2–3 *named* sub-groups of ≤4, each its own note. This is what chunking means in the memory literature, and it teaches the set's real structure instead of ten arbitrary slots. The 10-element radio report is 3 + 4 + 3: the dispatch header, the patient picture, care and close.
       **The sub-group names live in the STEM, visible — cloze them only if the source names them too.** A partition you invented is a scaffold for Parker, not content he will ever be asked to produce, and clozing it makes a card whose answer exists in no book: unanswerable cold (rule 16), prerequisite-unclosed (rule 11), and ungrounded (Rule 1). When the names are yours, each sub-group note simply prints its own name and position ("Phase 2 of 3 … the middle four elements of ten") and no anchor is clozed. When the source *does* name the divisions, an anchor note testing them is legitimate and good.
       **What to put on the extra note instead:** the thing the partition risks losing is the ORDER, so test that directly with an application vignette built on the source's own example — *"you have already given X, Y, and Z; what comes next?"* That is grounded, cold-solvable, and the archetype the EMT profile asks for anyway.
       **An UNORDERED set gets NO anchor note at all.** If the members have no order — TABLE 8-3's six situations calling for rapid extrication — then there is no order to test, the sub-group names are yours and may not be clozed, and an anchor note would have nothing legitimate to ask. The sub-group notes plus their `Roster:` lines are the whole family. Do not invent a card to fill the slot.
       *Found by doing it (2026-08-02):* the first draft of the radio-report family clozed "the dispatch header / the patient picture / care and close" — three phrases that appear nowhere in AAOS. Its own Back Extra gave it away: *"the three phases are a memory scaffold, not radio traffic."*
    2. **Convert to cued rows.** If each item has a natural key (an age band, a phase, a function), re-shape the flat list into a keyed panel and keep it whole.
    3. **Change the archetype.** If order is the knowledge, test it as a pathway/sequence; if the set is derivable, test the organizing principle that derives it and keep the full list in the Back Extra as reference (rule 22's option b).
    4. **Role-cued slot notes.** One note per item, each cued by that item's function — only when the members are genuinely independent facts that merely happen to be listed.
    **Every note born from a chunked set carries the FULL set in its Back Extra** under `Roster:`, with that note's own members in `<b>bold</b>`. Parker asked for this by name: he wants "the understanding of seeing the part and the whole in each flash card." It costs nothing, it keeps the set from dissolving into fragments, and it makes any single note traceable back to the list it came from.
    - *Caught by:* `check_cards.py overloaded_group` — ≥6 uncued warns, **≥8 uncued HARD-blocks**, and a verified spelled-mnemonic license exempts the group entirely (the same licensing predicate rule 18 uses, so the two can't disagree).
    *Failure that created this rule (2026-08-02):* the 10-element radio patient report card. Parker: *"it's telling me to in one go guess all of these things… if I forget one thing, I have to do it all again… what I'll find myself doing is just skipping that flash card."* Measured across his live EMT decks, scored on each card's FIRST review so new-card bias can't explain it: ordinary 1–2-blank cards failed 56% at 24.9 s; 3–4-item groups 78% at 33.3 s; 5–6-item groups 89% at 42.7 s; 7+ 80% at 49.3 s. The radio card itself: 5 reviews, 5 "Again," 54 s each — **never once answered correctly.** Regression **R25**.

24. **Chunking means separate NOTES — never sibling cloze numbers on one note.**
    The obvious "fix" for an overloaded list is to renumber it `{{c1::A}} {{c2::B}} {{c3::C}}…`. That is worse than the disease: it generates N cards that each display the other N−1 answers as free context, so the set is recovered by **elimination and recognition** instead of recall, and every card feels learned while nothing is.
    - **BAD:** the radio report renumbered c1…c10 — ten cards, each showing nine answers.
    - **GOOD:** three phase notes + one anchor note, each using a single cloze number for its own sub-set. Nothing on a note reveals another note's answers.
    - **Not a violation:** a two-way definition (`{{c1::TERM}} is {{c2::meaning}}`), a contrast card whose entity anchors stay visible, or any card whose numbers mark *different facts* rather than members of one enumerated set. The defect is specifically an enumerated list fanned across numbers.
    - *Caught by:* `check_cards.py sibling_split_leak` — ≥4 distinct cloze numbers, one span each, laid out as ≥4 parallel list rows → **HARD block**.
    *Preference that created this rule (2026-08-02):* Parker identified this failure mode himself, unprompted, while asking for the fix: *"I don't think that's what we need… if it's a hide-one-but-show-all-the-rest, I can just figure that out."* It is written down as a hard rule precisely because it is the trap a well-meaning future pass would walk into while trying to obey rule 23.

25. **A keyed panel of NUMBERS becomes one note per key, with the source table in Back Extra.**
    When a single cloze group hides a *column of values* keyed by a label — vital signs by age band, milestones by month, thresholds by severity — split it into one note per key. Each note asks for a single value; the **source table goes in Back Extra** so the whole set is visible the moment he answers.
    Two independent reasons, and they compound:
    - **Grading.** Every row hides and reveals together, so the card is all-or-nothing on N values no matter how well each row is cued (rule 23's argument, which the cued-row exemption wrongly excused).
    - **Interpolation.** Ordered keys with values that trend produce a column that gives itself away. Parker: *"if I see infant heart rate, I can guess what the neonate heart rate is… it's already given me half of the solution."* The card that created this rule proved it in its own Back Extra — *"the lower bound walks down in clean tens — 100, then 90, 80, 70, and 60"* — a genuinely good mnemonic that is also an exact recipe for answering without recall.
    - **Scope: numeric answers only.** A match card whose answers are words (`Transports oxygen → red blood cells`) cannot be interpolated and is judged on load alone by rule 23. The defect here is a *value column*.
    - **The split must be separate NOTES** (rule 24). Renumbering the column c1..cN is the worst possible form, because then every card shows the neighbouring values and interpolation becomes trivial rather than merely possible.
    - **Keep the whole set in view on the back.** Attach the real table as an image where one exists (`image` + `image_side: "back"`), otherwise a `Roster:` line. This is Parker's own design: *"the cards are disconnected in the sense of memorizing, but they're connected in the sense of the table, and the fact that I'm able to see the table in the answer."*
    - *Caught by:* `check_cards.py quantitative_panel` — ≥3 keyed numeric rows warns, **≥4 HARD-blocks**. Measured across his whole 4,340-note collection this fires on **9 cards**, every one a genuine value column.
    *Failure that created this rule (2026-08-03):* the normal-pulse-rate-by-age-group card. Parker: *"that was the card where I realized this change needed to be implemented… what is the common heartbeat of a neonate, and then another card saying the heartbeat of an infant is this, with the table in the back extra section — that could've been absolutely fire."* Regression **R28**.

26. **A procedure is carded as DECISIONS and VALUES, never as a narration of its steps.**
    When the source teaches a skill drill, protocol or algorithm, the card asks *"given this state of the world, what now?"* or *"what is the value of this parameter?"* — not *"list the N steps."* Full playbook, with the measured tables: `card-recipes.md` §12.
    - **The shapes, in order:** a **decision-point vignette** (discriminating state in the stem, one blank on the action); a **decision table** (condition → action rows under one cloze number, cued by condition and never by position); a **parameter matrix** for a physical skill (one card per population × parameter cell — this is rule 25's per-key split applied to technique); the **decidable residue** (named end-position, numeric parameter, confirmation cue, indication, contraindication, complication, failure mode); a **step-scaffold** for a causal or mechanistic sequence, where the ordinal is PRINTED and only the content is clozed; and **image occlusion over the flowchart** when the source prints a real algorithm diagram.
    - **Card the values of a technique, not the motion.** The motion is never narrated — no card in Parker's 85,212-note collection says *"then advance the needle while withdrawing the plunger."* But the technique is absolutely carded, through its discrete testable values: CPR, the archetypal psychomotor skill, appears as a **17-card lookup table** keyed by patient population and parameter (`In BLS for infants you check the {{c1::brachial}} pulse`). All 22 cards under AnKing's explicit `Procedures` namespace are indication, device choice, confirmation signal and complication — not one describes how to perform anything.
    - **Never cloze a step NUMBER.** Position is not knowledge and is not what he will be asked for. If ordinals appear at all, they are printed as scaffolding.
    - **Finish what you start.** A `(Step 1)` card with no `(Step 2)` is a broken series; Parker's deck carries two of them, made by this pipeline before the rule existed.
    - **Attach the procedure's own plate to the back**, so the whole sequence stays visible after he answers.
    - *Caught by:* `check_cards.py step_recitation` — a warning, not a block, since a short ordered protocol can be legitimate.
    *Evidence that created this rule (2026-08-03):* Parker asked how to card systematic skill-based material and pointed at his own AnKing decks as the authority. Measured over the whole population, the decision card is a **deliberate constraint rather than house style**: next-step cards beat their own deck's baseline on every axis, in two independently authored decks, and **0 of 419** carry five or more blanks where the baselines predict about five. What predicts a tight card is the chosen archetype, not the deck's polish — AnKing's own flagship MCAT deck is the loosest thing in the collection at 31.6% single-span.
    *Corrected 2026-08-03, same day, by a whole-population re-audit:* the first pass concluded "psychomotor technique is never carded," from keyword searches (`"place your hands"` → 0) that simply were not this vocabulary. Technique IS carded — as values, positions and confirmation cues — and the corrected rule is the more useful one. The first pass also claimed curation predicts tightness, which the MCAT deck refutes, and reported AnKing Step Deck at 89% single-span where the true population figure is **73.0%**.

27. **A bare number must SAY it wants a number — a count in front of its noun needs a slot-label hint.**
    A quantity is only self-constraining once you know the slot wants a quantity, and a bare blank never says so. In the attributive position — a count standing directly in front of the thing it counts — an adjective fits just as comfortably, so the front is genuinely ambiguous: `the {{c1::eight}} bones that form the wrist` and `the {{c1::short}} bones that form the wrist` are the SAME CARD to read.
    - **BAD:** `The {{c2::carpals}} are the {{c1::eight}} bones that form the wrist, and the {{c2::metacarpals}} are the {{c1::five}} bones that form the palm of the hand.` Both counts sit under c1, so on that card neither one cues the other and nothing anywhere says a number is wanted.
    - **GOOD:** `{{c1::eight::number of bones}}` / `{{c1::five::number of bones}}` — Parker's own fix, in his own words.
    - **Any ONE of these already announces the slot, and then a hint is redundant:** a `::hint`; a **unit** immediately after the blank (`___ beats/min`, `___ mg`, `___ months` — nothing but a number fits there); a **content word** immediately before it, which has already named the kind of number (`Type ___ diabetes`, `HPV ___`, `chromosome ___`, `a pKa of ___`, `on day ___`); a quantity word in the stem (`how many`, `the number of`, `the dose of`); or **another number left visible in a parallel slot** (`{{c1::three}} lobes … {{c2::two}} lobes` announces itself on both cards — the same card with both counts under c1 announces nothing on either).
    - **This closes a hole in rule 21's own exemption.** `open_set_absolute` excused numeric answers as *"self-constraining, and already numeric-flagged"*, and regression R16 recorded the same reasoning. Both were wrong in the same way, and this is the exact shape that walked through the gap.
    - **Scope: BARE quantities in an ATTRIBUTIVE slot.** An answer carrying its own unit ("100 to 180 beats/min") has already said what kind of thing it is. Keeping the scope this tight is what makes the rule a fix rather than a war on cards: a first, looser draft fired on **1,454** notes across the collection; the shipped one fires on **4** in the 1,223-card EMT deck, every one genuine.
    - *Caught by:* `check_cards.py unlabeled_quantity_blank` — a WARNING, because ordinary English sometimes forces a count on its own ("there are ___ types of shock") and only the judge can tell. **Repairs are licensed by a verified predicate**, `authorship.is_hint_only_change()`: adding a hint where there was none is allowed even on a protected field, while changing or removing one is not, since a hint may be Parker's.
    *Preference that created this rule (2026-08-03):* Parker, on the carpals card — *"a good hint here would be something like {{c1::five::number of bones}} — that would make it so i can know what im guessing... just say like 'long bones!' or 'short bones!'"* And on the scope: *"rem this is a SYSTEMATIC issue so fix this in the git hub for all the cards and the next ones to come."* Regression **R34**.

28. **The PURPLE lane: a marked word becomes an AUTHORED plain-language definition (2026-08-08).**
    Yellow says *"this matters — card it."* **Purple says *"I did not know this word — define it."*** Purple is `lexicon_colors` in the registry (default `#a28ae5`/`#c885da`), in ANY markup style — Parker's habit is a purple **underline**, which stacks cleanly beneath a yellow highlight over the same span, and a purple highlight means exactly the same thing. The extractor emits these as `kind: "lexicon"` with a cleaned `term` and a dedup `term_key`; the card shape lives in `card-recipes.md` §4b. The lane deliberately differs from yellow in four ways:
    - **The definition is AUTHORED, not extracted.** Parker's requirement, in his own words: a genetics textbook's definition of *chromosome* "may be super complicated and may overcomplicate" the thing worth knowing — *"if you just say something that makes sense and does properly define it… that is so much better."* So the cloze answer is a plain-language definition the drafter writes, held to three bars at once: **plain** (words a layperson knows — §2 #9's Back-Extra doctrine, promoted to the answer itself), **crisp** (≤ ~8 words; R12's bloat detector applies), and **faithful** (it keeps the DISCRIMINATING feature, and the sense the source used — "causes disease" defines *pathogenic*, not *virulent*; blending near-neighbors into one comfortable gloss is this lane's characteristic failure, and editor check #30 hunts it by name).
    - **Grounding is by ANCHOR, not word-overlap.** R13's support test is the wrong instrument here — the source is precisely where the word appears *undefined* — so `lexicon_check` replaces it with a contract that is just as unskippable: every lexicon card carries `lexicon.anchor.method` = `glossary` / `in_source` (lexicon.py `--find` located the book's own definition; quote + page mechanically extracted, never typed by the drafter; the gate verifies the entry exists, **R37**, and the authored answer must AGREE with it — the editor's consistency check) or `external` (the book never defines it → `verify_report.py` derives `needs_human_check`, the gate enforces the flag, **R35**, and the card reaches Parker's eyes in the report's Vocabulary block). The lane itself cannot be self-asserted: a card's `kind` must agree with the extractor-set kind of the marks it cites (**R36**) — the same anti-self-assertion lesson the visual exemption learned (R33).
    - **Triage is INTEGRITY-ONLY.** A purple mark is never vetoed for importance — he marked it because he didn't know it, and that judgment is his (rule 1's spirit, ported whole). The only licensed skips, each one SURFACED at hand-off and never silent: (a) a true duplicate — same `term_key` AND same sense — of a ledger entry still alive in Anki; (b) a hygiene flag (a drag slip or clipped word) that Parker confirms was an accident. A key COLLISION alone decides nothing: it summons a sense check against the two contexts. *Hypoxia/hypoxemia is the canonical pair* — they collide at `hypox`, they are different words, and the right output is TWO cards with `Distinguish:` lines, not a merge. Anatomic vs physiologic *process* likewise: two cards, each with a visible domain cue.
    - **A repeat mark is DATA, not noise.** The same word purpled again means the first card is not doing its job (or was never seen). Report every ledger hit at hand-off — *"you marked these again; they're already carded"* — with the existing card, so Parker can review or re-learn it. Never silently absorb the signal.
    *Origin (2026-08-08):* Parker designed the lane and its doctrine together — unknown words met while reading should land in that chapter's deck as definitions "that make sense." Regressions **R35–R37**; enforced by `check_cards.lexicon_check` + `verify_report.py`; dedup by `scripts/lexicon.py` (term keys, the in-source evidence finder, and the ledger with its Anki liveness check).

29. **Cards come ONLY from Parker's marks — the agent NEVER selects content for him (2026-08-08).**
    Rule 1 already forbade *dropping* a mark; this rule forbids the opposite failure: *adding* beyond the marks. The marks are the entire request. Yellow = "card this," purple = "define this," and unmarked text — however testable, however central, however sparse the chapter's marking — is not card material. A lightly-marked chapter means a small batch of excellent cards, not an invitation to fill the gap.
    - **"Do this for me" refers to the pipeline, not the selection.** He always does the selection; that is what reading is.
    - **Labeling doesn't license it.** The one violation that created this rule tagged every synthetic mark `selected_by: "claude"` and logged everything transparently — and was still 80 retracted cards. Provenance hygiene does not convert unrequested work into requested work.
    - **If unmarked content genuinely seems exam-critical, the whole permitted move is one sentence at hand-off** ("pages X–Y are unmarked; want anything from them?") — and the answer must be his, in his words, before a single extra card exists.
    - *Caught by:* `check_cards.synthetic_marks_check` — a card citing any mark carrying a provenance key the extractor never writes (`selected_by`) is a **HARD block**, and a highlights file containing synthetic marks warns on sight.
    *Failure that created this rule (2026-08-08):* the genetics ch9 "coverage lane" — 99 agent-selected marks, 80 staged cards, retracted in full. Parker: *"never once did I ever instruct you to do that… you could've been spending all that time creating actually really perfect amazing well formatted triple checked high-quality flashcards from those three pages… that was all I asked you to do."* Regression **R40**.

30. **A marked SET is carded for MEMBERSHIP first, then for its rows (2026-08-08).**
    Rules 23–25 tell you how to chunk a set once you have decided to test it. This one says
    what to test. When the source presents an enumerated set — a list of countries, a
    numbered set of characteristics, a roster of categories — **the membership itself is
    normally the primary fact**, and the relations among members are secondary.
    - **Ask the question that decides it:** *after these cards, can Parker PRODUCE the set —
      or only recognize relations among members he was handed?* If the second, the set was
      never carded.
    - **A two-column table is the classic trap.** Carding only `row-key → row-value` puts
      every member on the visible side of some card, so the set can never be produced. The
      pairing lane is fine and worth having; it is not sufficient.
    - **Shape of the membership lane:** named sub-groups of ≤4–5 on separate notes (rule 23's
      semantic partition, rule 24's separate-notes constraint), `Roster:` on every note with
      that note's members bolded, plus an anchor note naming the groups **only when the source
      names them or the partition is a stable public structure** (geography, the book's own
      categories) — never when the grouping is one you invented (rule 23.1).
    - **Make the row-pairing two-way** while you are there: `{{c1::Lebanon}}` /
      `capital: {{c2::Beirut}}` tests both directions from one note, where a stem-visible key
      tested only one.
    - **Check the sub-group names for self-leaks** — a region named "Iraq and the northern
      Gulf" hands over one of its own answers.
    - **Degenerate rows get their own card, not a leaky pairing.** Kuwait's capital *is*
      Kuwait, so the pairing leaks in both directions; the fact worth testing is that the
      names coincide.
    *Failure that created this rule (2026-08-08):* twenty Arabic-country cards that each
    revealed the country and asked for the capital. Parker: *"my goal with those cards was to
    memorize all of the countries that spoke Arabic… you gave me this thing as Arab country
    and then guessing just the capital."* Regression **R48**.

31. **A set defined by a PROPERTY carries that property onto every card it produces (2026-08-08).**
    Rule 30 says test membership before rows. This one governs the row cards themselves.
    When a source groups items *because they share a property* — Arabic-speaking countries,
    Schedule II drugs, essential amino acids — that property is the entire reason the set was
    marked, and a row card that omits it is a generic domain card wearing the set's clothes.
    - **The test:** *would this card be identical if it came from a different source about a
      different topic?* If yes, the property has been stripped and the card is duplicating
      knowledge Parker may already hold in another deck.
    - **Name the property in the stem** of every member card, and prefer the retrieval
      direction his other decks do NOT already drill (capital → country, not country →
      capital).
    - **Sub-group names are scaffolding on a member card, not a blank.** Clozing the group on
      all N members yields N blanks drawing on a handful of answers — a weak retrieval and a
      near-duplicate cluster. Region ↔ members belongs to the roster lane (rule 30).
    - **This is not a licence to bloat the stem.** One clause naming the property is enough;
      the roster on the back carries the rest.
    *Failure that created this rule (2026-08-08):* Arabic-country cards that asked for
    capitals with no mention of Arabic. Parker: *"I don't have a card cementing the fact that
    that is an Arabic speaking country."* Regression **R49**.

32. **A rule reaches the cards already in his decks — a remediation is not done until the superseded note is RETIRED (2026-08-15).**
    Every rule here was written because a live card was bad, so every rule is retroactive in
    intent. The machinery was not: the `.verified` stamp gates the staging FILE at write time,
    and nothing re-examines a note once it ships. A rule written on Tuesday therefore never
    reached the card that caused it, and the remediation run — which knew exactly which notes
    it was replacing — had no operation for taking one out.
    - **Name the superseded notes in the run manifest**, as `supersedes: [{note_id, rule,
      successors, status}]`. Not a count, not a sentence. `"replaced_panels": 8` and a
      `replaces` field reading *"a keyed panel of numbers hidden under one cloze"* are both
      claims that something was replaced, with no way to find it.
    - **Retire, don't delete.** `retire_notes.py` suspends every card of the note and tags it
      `superseded`; his review history, mnemonics and pasted images survive, and the ledger
      keeps the text verbatim so the card is recoverable from the repo alone. Deletion stays
      his call. Suspension is also what he already reached for by hand on the radio-report
      card — the system was just never told about it.
    - **Retirement demands a live successor.** The replacements must exist and be unsuspended
      before the original goes, or the fact silently stops being tested. Retiring with no
      successor requires an explicit `--reason`.
    - **Deferring is allowed; forgetting is not.** "Left in place so he can compare" is a fine
      decision and a terrible record when it lives in a commit message. Status `pending` keeps
      `check_hazards.py` red until someone retires or waives it.
    - **The live deck is a gated surface.** `check_cards.py --live` now exits nonzero on hard
      errors instead of always exiting 0. It skips suspended notes, so a retirement genuinely
      closes the gate rather than leaving a permanent red mark everyone learns to ignore.
    - *Caught by:* `check_hazards.py` (supersession block + a `replaces` that is not note ids)
      and `check_cards.py --live` (exit code), both in `smoke_test.sh`.
    *Failure that created this rule (2026-08-15):* Parker drew the systolic-BP panel in review
    — *"why are these cards like this and not indiviual cards? … dont just change it help me
    fix the system issue in the zotero to anki pipleine"* — and the six individual cards had
    been live for twelve days, three rows down in the same deck. Rules 23 and 25 were both
    authored FROM these very cards; ten of them were still being studied, and this repo's own
    checker had been calling them HARD ERRORS the whole time, in a mode wired to exit 0.
    Regression **R52**.
