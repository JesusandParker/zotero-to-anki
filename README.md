# zotero-to-anki (Claude skill)

Parker's system for turning **anything he marks in yellow in Zotero** into excellent Anki
cloze cards — a textbook chapter, an Arabic unit, a lecture PDF, a paper.

Built 2026-06-29 as an EMT-only card maker to replace an old ChatGPT "v60" pipeline;
generalized to any Zotero source on 2026-07-29 once the card craft had converged.

**Yellow = "make a card." Purple = "define this word"** (2026-08-08: the lexicon lane —
an unknown word met while reading becomes ONE plain-language definition card in that
chapter's deck, deduped across the whole collection by a term-key ledger; card-rules #28,
recipes §4b). Every other color is ordinary reading emphasis and is ignored by design.
Color decides, not markup style: highlighting in a textbook and *underlining* on lecture
slides mean the same thing (Parker's purple habit is the underline), and an area-selected
figure becomes an image card.

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
**a deterministic gate that cannot be skipped** → **write** into that source's deck, which
for a book is its `Book Highlights`.

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
- `reference/editor-checklist.md` — the 28-point "try to break this card" adversarial pass.
- `reference/card-recipes.md` — the archetype playbook: which card shape, and the exact template.
- `reference/cloze-mastery.md` — 2,391 annotated AnKing exemplars.
- `reference/note-format.md` — note type, cloze/MathJax/image syntax, write targets.
- `reference/parker-preferences.md` — Parker's living tastes; overrides the rules on conflict.

**The reliability harness** (why quality doesn't regress)
- `reference/regression-cases.md` — R1–R37, every flaw ever caught, with the BAD card it must
  catch *and* the GOOD card it must not over-flag.
- `scripts/test_regressions.py` — makes that library **executable**. Run after any rule or
  checker change.
- `scripts/check_cards.py` — the deterministic gate; writes the `.verified` stamp that
  `anki_write.py` refuses to stage without.
- `reference/feedback-log.md` — the running history of what Parker caught and how it was fixed.
- `reference/provenance.md` — how every card stays traceable, and the run store.
- `scripts/check_hazards.py` — a run may not discover a problem and only write prose about it.

**Per-subject emphasis**
- `reference/profiles/{emt,science,language,default}.md` — what the material is *for*, which
  archetypes dominate, subject traps. A thin overlay, never a second rulebook.

**Scripts**
- `scripts/sources.py` — the registry resolver (source → PDF, colors, segments, decks).
- `scripts/add_source.py` — register a new source; search Zotero, dump a TOC, build a map.
- `scripts/extract_highlights.py` — marks → grounded JSON (read-only on Zotero).
- `scripts/lexicon.py` — the purple lane's toolbox: term keys, the in-source definition
  finder (`--find`, writes the gate's evidence file), and the dedup ledger with its
  live-Anki liveness check (`--dedup`).
- `scripts/render_page.py` — render a page, or crop exactly to an area selection.
- `scripts/anki_write.py` — safe, one-at-a-time write into the source's deck.
- `scripts/feedback_harvest.py` — collect and clear the hidden `Card Feedback` complaints.
- `scripts/run_store.py` — the permanent record of every run; `trace <noteId>` for one card's whole story.
- `scripts/verify_report.py` — derives `needs_human_check`; splits verification into must-check vs may-skim.
- `scripts/sync_report.py` — what Parker changed after a write: rejections and edits as feedback.
- `scripts/smoke_test.sh` — 31 end-to-end checks; run after any structural change.

## Design notes

- **The star piece is the Editor stage.** The old system was a great *formatter* with no
  *editor*; the adversarial pass is what makes these cards better than a one-shot transform.
- **Reliability is a harness, not a promise.** Every flaw Parker catches gets named as a rule,
  mechanized in the checker, and frozen as a two-directional regression test. That's why the
  honest claim is *monotonic convergence* — nothing found recurs — rather than perfection.
- **Grounding is now machine-checked (R13).** Rule 1 — "always ground in the page paragraph" —
  was honor-system for the system's entire life, because `grounding: EXACT` only ever meant
  "I found your marked text." Cards now carry provenance, so every claim can be tested against
  the source it cites; material that only exists as an image passes by carrying the crop.
- **Every run is kept.** `runs/` holds the inputs, outputs, decisions, and dropped cards of
  each run, so you can work backwards from any card and ask why it exists.
- **One deck per segment.** Cards go straight into the source's `deck` (`…::Book Highlights`
  for a book). The old `…::claude review` staging deck and its promotion step were removed
  2026-08-24: Parker filters by editing and deleting cards as they come up in review, so
  nothing was ever promoted and every promotion deck sat empty. What actually guards the
  collection — the gate, the live sweep, retirement — is unchanged. Deck *names* stay
  per-source.
- **Card craft is subject-independent; emphasis is not.** Generalizing meant separating those
  two, which is what `reference/profiles/` is.
- **Related skill:** `course-to-anki` is the *scoring* pipeline — it decides what deserves a
  card when nothing is highlighted. This skill is for when Parker has already decided, by
  marking it. They share this repo's card-craft canon.
