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
   - No source artifacts: never reference "the figure / table / chapter / page / slide / recap / summary."
3. **Human-flow sentences.** Write like a tutor speaking, not note-shorthand. First line is a complete sentence with a real verb. Prefer "X is/does…" over "X: …". Colons only in the sequence format "Process Name (Step N): …".
4. **Hints are slot-labels, never the answer.** `{{c1::answer::hint}}` where the hint names the *category/form* of the answer ("enzyme", "year", "organ", "T/F", "protective or risk"), never a synonym, definition, or paraphrase. **Hint-leak check:** if the hint could replace the answer and mean the same thing, it's invalid — fix or omit.
5. **Back Extra is required and must add something new.** 1–3 `<br>` lines, each opening with one of: `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:`. It must teach an edge the Text doesn't already state. For a definition card, Back Extra may NOT re-define the term (use Distinguish / Pitfall / Ex / Cue). Priority when choosing: Distinguish/Pitfall > Mechanism/Why > Ex > Cue > Pathway > Mnemonic.
6. **Length.** Aim 12–35 words; hard max 60. Over that, split. Max 2 sentences, no semicolon run-ons.
7. **Zero guessing.** If the source text is unreadable, ambiguous, or you'd have to invent a fact to finish the card — STOP. Flag it (see Layer B rule 9). Never fabricate. (Especially true for anything clinical.)

---

## Layer B — Judgment (the audit's findings; this is the new work)

Each rule below cites a real failure from the deleted v60 deck so the reason is concrete.

1. **Yield filter — card knowledge, not sentences.**
   Only make a card if the fact is worth long-term memory for an EMT / the NREMT exam. Drop soft, throwaway, or edge-case clauses even if they were highlighted.
   *v60 failure:* "A nicotine-cessation plan should address challenges that may `[trigger product use]`." (Not testable knowledge.) Also low-yield guide-dog handling trivia.
   → A green highlight marks the *territory*; the yield filter picks the *cards* inside it. One highlight may yield several cards, one card, or — occasionally — none.

2. **One-answer rule.** With the cloze hidden, the visible stem must point to **exactly one** correct answer. If several answers fit, the stem is too vague — rewrite it (add the constraining detail) or drop it.
   *v60 failure:* "A core goal of CQI is `[minimizing errors]`." (Improving care, quality, safety all fit.)

3. **No tautology / no leakage.** The answer must not be stated, echoed, or obviously implied by the visible stem.
   *v60 failures:* "An organ donor is a person who has expressed a wish to `[donate organs]`." / "Violence prevention includes … `[threats of violence]`."

4. **List rule — test every item, never "cloze one and reveal the rest."**
   When the source lists N parallel items, every item must be tested. Choose deliberately:
   - **Sibling cards:** N cards, each hiding a *different* item with the others shown as context (best when each item is independently high-yield), or
   - **One grouped card:** hide the whole set under the *same* cloze number `{{c1::A}}, {{c1::B}}, {{c1::C}}` (best for a short set learned as a unit).
   Never `{{c1::A}}, B, C, D` — that tests A and gives away B/C/D for free.
   *v60 failure:* "…frontal, parietal, occipital, and `[temporal]` lobes." (3 of 4 lobes never tested.)

5. **Crisp-cloze rule.** Delete a tight keyword, number, or term — not a long fuzzy phrase you could never recall verbatim.
   *v60 failure:* "Eustress can increase `[focus and short-term energy]`." → cloze the crisp concept, not the phrase.

6. **List-size cap.** No single card hides more than ~3–4 items. Bigger sets become sibling cards.
   *v60 failure:* one de-escalation card hid a 5-item list under one cloze.

7. **Under-clozing check.** Within the highlighted passage, every *distinct testable* fact gets tested somewhere (this card or a sibling). Don't leave a clozable fact sitting in plain text.
   *v60 failure (the "didn't cloze cytosine" bug):* 82.5% of long old cards clozed only one thing.

8. **Card-type variety.** Where the content supports it, go beyond fill-in-the-blank: definition, comparison (X vs Y), mechanism/causal chain, ordered steps, classification, **clinical vignette/application**, negation/exception. EMT is an *application* exam; rehearse reasoning, not just recognition. See `cloze-mastery.md` Part V for the archetypes and worked examples.
   *v60 failure:* 88% were single-cloze factoids; zero vignette/compare/reasoning cards.

9. **Confidence & safety flag.** If grounding is weak (the extractor marked it `PARTIAL`/`NOT_FOUND`) or the fact is a **number/dose/threshold**, mark the card `needs_human_check: true` and surface it to Parker rather than trusting it silently. A wrong digit on a dose is dangerous.

10. **Ground every claim.** Every fact on the card must be supported by the highlight's `context` paragraph from the extractor. Do not add outside facts the source doesn't support. If the context is too thin to make a correct card, that's rule 7-of-Layer-A (flag, don't guess).
