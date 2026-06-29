---
name: emt-card-maker
description: Turn Parker's green Zotero highlights from his EMT textbook into high-quality Anki cloze cards, staged to a review subdeck. Use whenever he's done reading/highlighting an EMT chapter (or names a chapter) and wants cards made, e.g. "make my Chapter 1 cards", "I finished highlighting chapter 3", "build EMT flashcards from my highlights".
---

# EMT Card Maker

Turns the things Parker green-highlights (`#5fb236`) in his EMT textbook (Zotero) into excellent Anki cloze cards, grounded in the real page text, quality-checked, and staged into `EMT::_Review` for him to approve and file.

This replaces his old ChatGPT "v60" system. The old EMT deck was deleted on purpose; this rebuild fixes what that deck got wrong (see `reference/card-rules.md` Layer B for the specific failures). **The green highlight is Parker's "this matters" signal — he has already chosen what's important. Your job is to turn it into the best possible card(s), not to re-decide importance.**

## Three rules that override everything

1. **Always ground in the page paragraph.** Never write a card from the bare highlight sentence. Use the `context` paragraph the extractor provides. Every claim on a card must be supported by that context. (This is what keeps cards correct instead of hallucinated.)
2. **Zero guessing.** If the context is too thin, ambiguous, or the highlight didn't locate (`grounding: NOT_FOUND`), do NOT invent. Flag it for Parker. Especially for any number, dose, or threshold.
3. **Nothing is final.** Everything lands in `EMT::_Review`. Parker reviews, edits, and moves keepers himself. You stage; he commits.

## Priority order when rules collide
When two goals trade off, resolve in this order (Parker's explicit ranking from his ChatGPT-era notes): **(1)** correct cloze formatting + reliable write to Anki, **(2)** completeness/coverage of testable facts, **(3)** standalone atomicity, **(4)** a teachable Back Extra, **(5)** readability/aesthetics, **(6)** speed — dead last. Parker will gladly wait for better cards; never trade 1–5 for speed.

## The pipeline

Work **one chapter at a time**, and within a chapter, **one highlight at a time** (Parker explicitly wants this blocked, focused approach — it's also what fixes the old deck's under-clozing).

### Stage 1 — Extract (once per chapter)
```
python3 ~/.claude/skills/emt-card-maker/scripts/extract_highlights.py --chapter <N>
```
This writes `work/chapter_<N>_highlights.json` (green highlights + grounded `context` + page + any margin `user_comment`). Read it.

### Stage 2 — For each highlight: classify → draft → edit
For every highlight in the file:

0. **Group first (Rule 0 — do this before anything else).** Scan the highlights around this one (same page, consecutive, overlapping `context`). If several are parallel pieces of one idea — the bullet lead-ins under a single heading, a set of related terms, the steps of one process — treat them as ONE unit and make a single unified card. Never fragment a connected set into isolated cards, and never drop a highlighted span as "thin." See `reference/card-rules.md` Rule 0.

1. **Classify the fact type, then open its recipe.** Definition · numeric value/dose/cutoff · classification list · ordered sequence/protocol · comparison/direction-of-change · mechanism/causal chain · indication/contraindication · trigger ("when do you do X") · scope-of-practice · MOI → index of suspicion · age-banded vitals · buzzword/clinical-vignette · anatomy/figure · ambiguous fragment. Then open the matching section of **`reference/card-recipes.md`** — the archetype playbook (when-to-use, exact template, hint + Back-Extra conventions, do's/don'ts, EMT examples). Drill into `reference/cloze-mastery.md` only for more exemplars.
   - If it's a **table/figure** fact (or `grounding` is `PARTIAL`/`NOT_FOUND`), render the page and read it visually:
     ```
     python3 ~/.claude/skills/emt-card-maker/scripts/render_page.py <page>
     ```
     Then author from the image and attach it via the card's `image` field.
2. **Fact pass, THEN draft.** First list every atomic proposition in the highlighted span + its `context`, and tag each: **MUST-TEST** (a competent EMT must *produce* it from memory — a definition, a goal/purpose/function, scope/what-a-level-does, a number/range/dose, a discriminating feature, an indication/contraindication, an ordered step, a sign/symptom), **SUPPORTING** (only cues the answer — leave it as visible context), or **SKIP** (incidental filler). THEN draft card(s) — using the chosen recipe in `reference/card-recipes.md` and the gates in `reference/card-rules.md` — so that EVERY must-test fact is clozed somewhere. Leaving a must-test fact unclozed as scenery is the under-clozing bug (the public-health *goal*, the AEMT *skills*). A `user_comment` like "Know all of these!!" means be extra exhaustive.
   **Auto-pair rule (what makes the deck feel like NREMT prep):** if the fact is a sign, finding, vital threshold, or "which one" discrimination, also draft ONE short scenario cloze embedding it in a 1–2 sentence patient stem ending in a single decision (field impression or next action) — one stem, one cloze. Heaviest in clinical chapters; recall-heavy chapters (EMS Systems, Medical/Legal) need it far less. See `card-recipes.md` §1 and §9.
3. **Edit each candidate** through `reference/editor-checklist.md` as an adversary — mandatory, and best run by fresh, *independent* eyes (a writer defends its own work; a reviewer hunts the miss). Its #1 job: re-run the fact pass — is every MUST-TEST fact actually clozed, or is one sitting as scenery? Rewrite or add cards to cover it; set `needs_human_check: true` for any number/dose/threshold or weak grounding.
4. Keep the survivors as card objects in the shape from `reference/note-format.md`.

**Generate DECOMPOSED, never hand-crafted in one pass.** Work one unit at a time (a single highlight, or a Rule-0 group), each unit getting its own focused fact-pass → draft → *independent* adversarial edit. Do NOT draft a whole chapter inside one context window: that is how an AI gets overwhelmed, takes shortcuts, and skips the checks — exactly how the public-health goal and the AEMT skills were left untested. For a full chapter, FAN OUT — and the fan-out has THREE stages, not two: (1) **group aggressively** so a connected cluster (certification/licensure/credentialing, or online/off-line medical control) is ONE unit, not several that duplicate each other; (2) per-unit draft + *independent* edit (coverage); (3) **global consolidation** (Stage 2.5). Then show Parker the cards *and* the per-card fact-coverage, and let his reactions sharpen the rules.

### Stage 2.5 — Global consolidation (REQUIRED after any fan-out)
A per-unit fan-out has no global view, so it duplicates the same fact across neighboring units and over-fragments one concept into many micro-cards (it once turned 36 highlights into 76 cards — online medical control alone got 9). After all units are drafted and edited, run ONE consolidation pass with the WHOLE chapter's cards in view: **dedupe** the same fact carded in multiple units (keep the best one), **collapse** a concept split into many micro-cards down to the 1–2 high-yield cards, and **trim** genuine low-yield/trivia — all WITHOUT dropping any must-test fact (never re-introduce under-clozing). Emit a transparent merge/collapse/cut log so Parker can audit the balance. The per-unit agents structurally cannot do this; it's what turns an exhaustive dump into a tight, high-yield set.

### Stage 3 — Stage into Anki (once per chapter)
Write the collected card objects to a JSON, then:
```
python3 ~/.claude/skills/emt-card-maker/scripts/anki_write.py work/chapter_<N>_cards.json
```
(Add `--dry-run` first to validate without writing.) This adds each card to `EMT::_Review`, tagged `claude_generated` + `ch<N>`, one at a time, with pre-flight validation. Anki must be open.

### Stage 4 — Hand off
Tell Parker: how many cards landed in `EMT::_Review`, and specifically list the `needs_human_check` ones (doses/numbers/weak grounding) for him to verify before he moves anything into his real chapter decks.

## Reference files (load on demand)
- `reference/card-rules.md` — the full standard (Layer A form + Layer B judgment). Read before drafting.
- `reference/parker-preferences.md` — Parker's living tastes. Read before drafting; when it conflicts with card-rules, this wins.
- `reference/card-recipes.md` — **the archetype playbook**: for any highlight, which card shape to use plus the exact template and conventions. The primary drafting reference; consult it every time.
- `reference/editor-checklist.md` — the 13-point adversarial Editor pass. Read before editing.
- `reference/note-format.md` — exact note type, cloze/MathJax/image syntax, Back Extra vocabulary, write targets.
- `reference/cloze-mastery.md` — 2,391 annotated AnKing exemplars across 23 sections. **Large file — open only the section for the card type you're writing**, not the whole thing.
- `reference/chapter_pages.json` — page→chapter map (used by the extractor).

## Improving over time (the feedback loop)
When Parker reacts to a card, that's the signal that makes this system grow. Route it to the right layer, then commit + push (per `CLAUDE.md`):
- **One bad card** → fix that card in Anki. No rule change.
- **A recurring pattern** ("cards keep doing X") → add/edit a rule in `reference/card-rules.md` or `reference/editor-checklist.md`.
- **A taste/preference** ("I like it phrased like Y", "split big lists") → add it to `reference/parker-preferences.md`, and resolve any matching "Open question" there.
- **An extraction/code issue** → fix the script.
Always generalize: turn "this card is wrong" into the rule that prevents the whole class of mistake. That's how Chapter N+1 inherits everything learned in Chapter N.
