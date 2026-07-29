# zotero-to-anki (Claude skill)

Parker's system for turning **anything he marks in yellow in Zotero** into excellent Anki
cloze cards — a textbook chapter, an Arabic unit, a lecture PDF, a paper.

Built 2026-06-29 as an EMT-only card maker to replace an old ChatGPT "v60" pipeline;
generalized to any Zotero source on 2026-07-29 once the card craft had converged.

**Yellow = "make a card."** Every other color is ordinary reading emphasis and is ignored by
design. Color decides, not markup style: highlighting in a textbook and *underlining* on
lecture slides mean the same thing, and an area-selected figure becomes an image card.

## How to use it

Say what you want in plain language:

- *"make cards from chapter 6 of my EMT book"*
- *"I finished highlighting the first Arabic unit"*
- *"I highlighted something in that genetics lecture I want to memorize"*
- *"add my organic chem textbook"* — registers a new source (asks you once where its cards go)
- *"I noticed an issue with a card"* — the fix loop
- *"go look at my card feedback"* — batch-process the complaints you typed while studying

The pipeline: **extract** the marks (grounded in the real page paragraph) → **draft** each
into card(s) using the archetype playbook → **adversarial edit** → **global consolidation** →
**a deterministic gate that cannot be skipped** → **stage** into that source's review deck,
where you promote the keepers yourself.

**Anki must be open** for anything that touches cards.

## Sources

```bash
python3 scripts/sources.py list            # what's registered
python3 scripts/sources.py show emt        # one source, fully resolved
python3 scripts/add_source.py --search "Alif Baa"   # find something new in Zotero
```

Everything source-specific — which PDF, which colors, the page→chapter map, the Anki decks,
the tags, the subject profile — lives in `reference/sources.json`. Adding a book is a
one-time setup; after that you just point at it. See `reference/sources.md`.

## What's where

**Operating instructions**
- `SKILL.md` — what Claude follows, start to finish.
- `CLAUDE.md` — the version-control workflow for this repo.

**The universal card standard** (subject-independent; this is the valuable part)
- `reference/card-rules.md` — Layer A form + Layer B judgment, including the **Cold-Solve Gate**.
- `reference/editor-checklist.md` — the 20-point "try to break this card" adversarial pass.
- `reference/card-recipes.md` — the archetype playbook: which card shape, and the exact template.
- `reference/cloze-mastery.md` — 2,391 annotated AnKing exemplars.
- `reference/note-format.md` — note type, cloze/MathJax/image syntax, write targets.
- `reference/parker-preferences.md` — Parker's living tastes; overrides the rules on conflict.

**The reliability harness** (why quality doesn't regress)
- `reference/regression-cases.md` — R1–R12, every flaw ever caught, with the BAD card it must
  catch *and* the GOOD card it must not over-flag.
- `scripts/test_regressions.py` — makes that library **executable**. Run after any rule or
  checker change.
- `scripts/check_cards.py` — the deterministic gate; writes the `.verified` stamp that
  `anki_write.py` refuses to stage without.
- `reference/feedback-log.md` — the running history of what Parker caught and how it was fixed.

**Per-subject emphasis**
- `reference/profiles/{emt,science,language,default}.md` — what the material is *for*, which
  archetypes dominate, subject traps. A thin overlay, never a second rulebook.

**Scripts**
- `scripts/sources.py` — the registry resolver (source → PDF, colors, segments, decks).
- `scripts/add_source.py` — register a new source; search Zotero, dump a TOC, build a map.
- `scripts/extract_highlights.py` — marks → grounded JSON (read-only on Zotero).
- `scripts/render_page.py` — render a page, or crop exactly to an area selection.
- `scripts/anki_write.py` — safe, one-at-a-time write into the source's staging deck.
- `scripts/feedback_harvest.py` — collect and clear the hidden `Card Feedback` complaints.

## Design notes

- **The star piece is the Editor stage.** The old system was a great *formatter* with no
  *editor*; the adversarial pass is what makes these cards better than a one-shot transform.
- **Reliability is a harness, not a promise.** Every flaw Parker catches gets named as a rule,
  mechanized in the checker, and frozen as a two-directional regression test. That's why the
  honest claim is *monotonic convergence* — nothing found recurs — rather than perfection.
- **The two-deck promotion gate is universal.** The pipeline only ever writes to
  `…::claude review`; Parker promotes keepers himself. Deck *names* are per-source.
- **Card craft is subject-independent; emphasis is not.** Generalizing meant separating those
  two, which is what `reference/profiles/` is.
- **Related skill:** `course-to-anki` is the *scoring* pipeline — it decides what deserves a
  card when nothing is highlighted. This skill is for when Parker has already decided, by
  marking it. They share this repo's card-craft canon.
