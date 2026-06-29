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

1. **Classify the fact type.** Definition · vocabulary · numeric value/dose · formula · classification list · ordered sequence · anatomy/spatial · comparison · mechanism/causal chain · indications/contraindications · clinical-application · table/figure · ambiguous fragment.
   - If it's a **table/figure** fact (or `grounding` is `PARTIAL`/`NOT_FOUND`), render the page and read it visually:
     ```
     python3 ~/.claude/skills/emt-card-maker/scripts/render_page.py <page>
     ```
     Then author from the image and attach it via the card's `image` field.
2. **Draft 1–N cards** using the recipe for that type. Open the matching archetype section of `reference/cloze-mastery.md` (Part III for lists/equations/tables/numerics; Part V for definitions, comparisons, mechanisms, sequences, classifications, vignettes) and follow `reference/card-rules.md`. Apply the **under-clozing check**: every distinct testable fact in the passage must be tested by some card. A `user_comment` like "Know all of these!!" is a signal to be thorough.
3. **Edit each candidate** through `reference/editor-checklist.md` as an adversary. Rewrite or drop. Set `needs_human_check: true` for any number/dose/threshold or weak grounding.
4. Keep the survivors as card objects in the shape from `reference/note-format.md`.

**For the first chapter (calibration): go slowly and show Parker.** Draft a handful, show him the before/after thinking, let his reactions sharpen the rules. Don't silently generate 36 cards on the first run — the point of chapter one is to tune your taste to his. Once he's happy, later chapters can run with less hand-holding.

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
- `reference/editor-checklist.md` — the 11-point adversarial Editor pass. Read before editing.
- `reference/note-format.md` — exact note type, cloze/MathJax/image syntax, Back Extra vocabulary, write targets.
- `reference/cloze-mastery.md` — 2,391 annotated AnKing exemplars across 23 sections. **Large file — open only the section for the card type you're writing**, not the whole thing.
- `reference/chapter_pages.json` — page→chapter map (used by the extractor).

## Improving over time
When Parker rejects or rewrites a card, that's signal. Capture the lesson as a new line in `reference/card-rules.md` (or a `reference/parker-preferences.md` you create) so the system gets better instead of repeating the mistake. This is the feedback loop the old static prompt never had.
