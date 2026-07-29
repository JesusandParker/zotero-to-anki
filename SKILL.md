---
name: emt-card-maker
description: Make and maintain Parker's EMT Anki cloze cards from his yellow Zotero highlights. Use (1) to GENERATE cards when he's done highlighting a chapter ("make my Chapter 1 cards", "I finished highlighting chapter 3"), AND (2) to FIX/REVIEW/IMPROVE existing cards or the card-maker itself when he reports a problem while studying ("I noticed an issue with an EMT card", "this EMT flashcard is wrong / the hint gives it away", "fix the EMT card maker", "the cards keep doing X"), AND (3) to BATCH-PROCESS the complaints Parker types into the hidden "Card Feedback" field during review ("go look at my card feedback", "process my complaints", "go through the cards I ranted about / flagged", "harvest my Anki feedback") — this spans his EMT and Liberty course cards. On any single-card issue follow the "If Parker reports an issue" procedure below; for a batch, follow "Processing card feedback (batch)".
---

# EMT Card Maker

Turns the things Parker yellow-highlights (`#ffd400`) in his EMT textbook (Zotero) into excellent Anki cloze cards, grounded in the real page text, quality-checked, and staged into the chapter's `all::EMT::Chapter <N>::claude review` subdeck for him to approve and promote.

## Highlight colors — yellow is the only input

**Yellow (`#ffd400`) is the ONLY thing that becomes a card.** Every other color is noise to this pipeline, by design.

**Blue (`#2ea8e5`) means "Parker found this interesting, but does not want to memorize it."** It is a personal note to himself, not an omission and not a to-do. Example: the body armor line on p221 — he marked it because *maybe I should get some body armor*, not because he needs to recall that some EMS responders wear it. Treat blue as deliberately, silently out of scope: **never card it, never flag it, never ask about it, never count it as missed coverage.** If Parker asks why some passage has no card, "it's blue, so you told me not to" is the correct answer.

This is a decision he may revisit — someday blue (or another color) may get its own meaning. Until he says so, the mapping is exactly: **yellow = memorize, everything else = his own notes.** These are the only two colors in the book; if you ever see green, something has gone wrong — do not silently skip it, tell him. (History: the early chapters were highlighted green and he switched to yellow around p526; the whole book was normalized to yellow/blue on 2026-07-29.)

This replaces his old ChatGPT "v60" system. The old EMT deck was deleted on purpose; this rebuild fixes what that deck got wrong (see `reference/card-rules.md` Layer B for the specific failures). **The yellow highlight is Parker's "this matters" signal — he has already chosen what's important. Your job is to turn it into the best possible card(s), not to re-decide importance.**

## Three rules that override everything

1. **Always ground in the page paragraph.** Never write a card from the bare highlight sentence. Use the `context` paragraph the extractor provides. Every claim on a card must be supported by that context. (This is what keeps cards correct instead of hallucinated.)
2. **Zero guessing.** If the context is too thin, ambiguous, or the highlight didn't locate (`grounding: NOT_FOUND`), do NOT invent. Flag it for Parker. Especially for any number, dose, or threshold.
3. **Nothing is final.** Everything lands in the chapter's `all::EMT::Chapter <N>::claude review` subdeck. Parker reviews, edits, and PROMOTES keepers into the sibling `...::Book Highlights` deck himself. You stage; he commits.

## Priority order when rules collide
When two goals trade off, resolve in this order (Parker's explicit ranking from his ChatGPT-era notes): **(1)** correct cloze formatting + reliable write to Anki, **(2)** completeness/coverage of testable facts, **(3)** standalone atomicity, **(4)** a teachable Back Extra, **(5)** readability/aesthetics, **(6)** speed — dead last. Parker will gladly wait for better cards; never trade 1–5 for speed.

## If Parker reports an issue with a card (his main ongoing loop — START HERE)

Once a chapter's cards exist, this is the primary use. A fresh Claude session with NO memory of past work can do this end-to-end from this skill alone. When Parker says something like *"I noticed an issue with an EMT card,"* *"the hint gives it away,"* *"this card is wrong":*

1. **Read the standards first** — `reference/regression-cases.md` (every flaw caught before + how it's caught; his issue is usually a known class), then `reference/card-rules.md` and `reference/parker-preferences.md`.
2. **Find the card** — it's in Anki under `all::EMT::Chapter <N>::claude review` (or `...::Book Highlights` if Parker already promoted it) via AnkiConnect at `localhost:8765` (Anki must be running; search by a distinctive phrase) and in `work/chapter_<N>_cards.json`.
   - **To sweep for the whole class mechanically, audit the LIVE deck:** `python3 scripts/check_cards.py --live <N>` (one chapter) or `--live all`. This runs the deterministic gate against the cards as they actually exist in Anki — the only way to catch defects that entered by hand-editing in Anki (Parker edits on Mac + iPhone), which never pass back through the file gate. Diagnostic only; it never writes or stamps.
3. **Diagnose honestly — one-off or systemic?** If it's a *kind* of mistake (not a typo), assume systemic: the rules would let it recur, so fix the rules, not just the card.
4. **Fix the card(s)** in Anki and in the JSON.
5. **If systemic:** encode the rule (`card-rules.md` / `editor-checklist.md` / `parker-preferences.md`), AND add a case to `reference/regression-cases.md` (a BAD card the checks must catch + a GOOD card they must NOT over-flag), AND extend `scripts/check_cards.py` if it can be mechanized.
6. **Re-verify:** run `python3 scripts/check_cards.py work/chapter_<N>_cards.json` and confirm the regression cases still pass (catch the bad, spare the good).
7. **Log it** in `reference/feedback-log.md` (date, what he flagged, the fix, the rule/test added).
8. **Commit + push** per `CLAUDE.md`.

Be honest about one-off vs systemic, and never over-correct — the regression suite's "don't over-flag" cases are the guard against swinging too far.

## Processing card feedback (batch) — "go look at my complaints"

Parker leaves complaints on cards *while studying* by typing into a hidden **`Card Feedback`** field (on his `AnKing Cloze` / `AnKing Basic` note types) via Anki's **Edit** button — it never shows during review but stays attached to the exact card, on Mac and iPhone. This is the batch front-door to the single-card loop above; it spans his EMT **and** Liberty course cards. When he says *"go look at my card feedback,"* *"process my complaints,"* *"go through the cards I ranted about"*:

1. **Harvest** (Anki must be running):
   ```
   python3 ~/.claude/skills/emt-card-maker/scripts/feedback_harvest.py
   ```
   Lists every note with a non-empty `Card Feedback` and writes `work/feedback_inbox_<date>.json` (per card: noteId, deck, front, Back Extra, the rant). Read it. Non-empty = unprocessed; an empty inbox means nothing to do.
2. **Process each item** with the **"If Parker reports an issue with a card"** procedure above (read `reference/regression-cases.md` first; diagnose one-off vs systemic; fix the card; if systemic, encode the rule + add a regression test + extend `check_cards.py`). Route by the card's deck:
   - *Card-craft* issues (leaky hint, under-clozing, phrasing, formatting) → the shared `reference/` canon here, whatever the subject. This is the home of card craft; `course-to-anki` reuses it.
   - A card from a **Liberty course deck** (`all::LIBERTY::…`) whose complaint is about *selection/scoring* ("this shouldn't exist", "you missed the real testable fact") → also route to `course-to-anki` per its feedback loop (adjust `scripts/score.py` weights or the pass prompts, and log why).
3. **Write back** with the same script — one small JSON batch does fixes and clears together:
   ```
   python3 ~/.claude/skills/emt-card-maker/scripts/feedback_harvest.py --apply fixes.json
   ```
   where `fixes.json` is a list of `{"noteId": …, "fields": {"Text": "…", "Back Extra": "…"}, "clear_feedback": true}`. Applies the approved fix and clears the feedback in one step. (Or `--clear <noteId> …` when the card just needed logging, no edit.)
4. **Log every item** in `reference/feedback-log.md` (date, deck, the complaint, the fix, any rule/test added) — the permanent history. The field is only the transient inbox.
5. **Clear a card's feedback ONLY after it's logged** — a non-empty `Card Feedback` must always mean "still unprocessed," so nothing is ever lost.
6. Re-run `python3 scripts/check_cards.py …` if you touched any rule/regression file, then **commit + push** per `CLAUDE.md`, and remind Parker to **sync** (his cards live on his phone too).

The `Card Feedback` field is **hidden + human-only**: the card generator must never write into it (see `reference/note-format.md`).

## The pipeline

Work **one chapter at a time**, and within a chapter, **one highlight at a time** (Parker explicitly wants this blocked, focused approach — it's also what fixes the old deck's under-clozing).

### Stage 1 — Extract (once per chapter)
```
python3 ~/.claude/skills/emt-card-maker/scripts/extract_highlights.py --chapter <N>
```
This writes `work/chapter_<N>_highlights.json` (green highlights + grounded `context` + page + any margin `user_comment` + a `list_lead_in` flag). Read it.
- **`list_lead_in: true`** marks a highlight that introduces an enumerated list. The extractor widens its context and pulls the next page for these, but you MUST still read the whole list off the source page and test EVERY item — lists that span a page break are where items get dropped (card-rules #14).
- **`user_comment`** is Parker talking directly to you. Obey it: "Know all of these!!" → test every item exhaustively; a *question* → answer it (grounded only in the source) and surface the answer at hand-off; "look more into this" → flag `needs_human_check` and tell him what to look into. Never silently ignore a margin comment.

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

### Stage 2.75 — Verify (a mandatory gate, never skip)
Reliability is a harness, not a promise to be careful. Before staging, the set MUST pass verification:
1. `python3 scripts/check_cards.py work/chapter_<N>_cards.json` — the deterministic gate (legal HTML + cloze-present = HARD block; literal-answer-in-stem, parenthetical-after-cloze, numeric-without-flag, in-batch duplicates = warnings). Fix HARD errors; route every warning to the judge. On a HARD-clean pass it writes a `<file>.verified` stamp (a hash of the exact file).
2. The independent LLM judge runs the FULL `reference/editor-checklist.md` on every card (run, never eyeballed).
3. Both are calibrated against `reference/regression-cases.md` — the library of every flaw ever caught (bad cards the checks MUST flag, good cards they must NOT). Whenever a rule, the checker, or the judge changes, re-validate against it so nothing regresses. Every new flaw Parker catches gets added there as a permanent test.

**This gate is physically unskippable, not just a rule:** `anki_write.py` refuses to stage any file that lacks a current `.verified` stamp (and editing the JSON after the check invalidates the stamp — re-run `check_cards.py` to re-stamp). So Stage 3 cannot run until Stage 2.75 has passed on the exact bytes being staged. `--force` exists as a deliberate escape hatch only.

### Stage 3 — Stage into Anki (once per chapter)
Write the collected card objects to a JSON, then:
```
python3 ~/.claude/skills/emt-card-maker/scripts/anki_write.py work/chapter_<N>_cards.json
```
(Add `--dry-run` first to validate without writing — dry-run skips the stamp gate.) This adds each card to `all::EMT::Chapter <N>::claude review` (derived per card from its `chapter` field; the writer also creates the `Book Highlights` sibling for Parker to promote into) on the `AnKing Cloze` note type (fields `Text` + `Back Extra`; the other three AnKing fields stay empty — they're Parker's own), tagged `ch<N>` only, one at a time, with pre-flight validation. Anki must be open.

### Stage 4 — Hand off
Tell Parker:
- how many cards landed in `Chapter <N>::claude review` (and remind him to promote keepers into the sibling `Book Highlights` deck after his first pass);
- the `needs_human_check` ones (doses/numbers/weak grounding) for him to verify before he moves anything into his real chapter decks;
- **answers to any margin questions** he wrote (`user_comment` that is a question) — answered from the source, with what he should double-check;
- anything he flagged with "look more into this," and the specific thing to look into.
Margin comments are Parker's voice on the page; a hand-off that ignores one has failed even if the cards are perfect.

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
