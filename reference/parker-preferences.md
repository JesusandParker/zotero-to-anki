# Parker's Preferences (living document)

This is where Parker's taste lives. The skill reads it before drafting every card, so anything captured here shapes all future cards. It grows whenever Parker reacts to a card. Every change is a git commit, so we can trace *why* a preference exists and roll back if a change turns out wrong.

How it's used: `card-rules.md` is the hard methodology; this file is Parker's specific tastes layered on top. When they ever conflict, this file wins (it's the more recent, more personal signal).

## Confirmed by Parker
- **Staging:** cards go to `EMT::_Review`; Parker moves keepers into chapter decks himself. Never auto-file into a chapter deck.
- **Never drop a highlighted span.** Connected/adjacent highlights become ONE card (card-rules Rule 0). The green highlight is his decision that it matters.
- **Big lists stay whole.** If the items form a genuine cohesive list (parallel members of one set, or the steps of one process), keep them in ONE card no matter the length — never split a real list into chunks. Guardrail: this applies *only* when the items are genuinely similar/related; never cram *unrelated* facts into one card just to bundle them (that's useless — unrelated facts stay separate cards). Test before bundling: "are these truly one set, or am I lumping unrelated things together?" (Confirmed 2026-06-29 re: Star of Life = 6 functions, EMS Agenda 2050 = 6 principles.)
- **Definitions are two-way by default.** For a term↔meaning fact, write one note as `{{c1::TERM::hint}} is {{c2::tight defining property}}` → Anki makes two cards (name-it from the description, and define-it from the term). Keep the `c2` meaning side CRISP (a few discriminating words, never a long definition). Go single-direction only when just one direction is useful (scenario→name, or word→meaning). Do NOT two-way lists, sequences, numbers, or scenario/application facts. Turn on "bury siblings" for the EMT deck so the two halves space across days. (Decided 2026-06-29, evidence-based: it's AnKing's own §15 "bread-and-butter" pattern, their live decks lean ~73% toward testing the meaning side with crisp answers, and it matches encoding-specificity + minimum-information research. Resolves the directionality gap — the term→meaning direction had been missing.)
- **Tagging:** deferred for now — only the `claude_generated` reversibility marker, not a full taxonomy.
- **Fresh-pass over patching:** when he wants a chapter redone, wipe the deck and rebuild from scratch rather than editing card-by-card.

## Current defaults (working, but not yet explicitly confirmed — flag if wrong)
- Back Extra opens with a labeled line: **Distinguish** for confusable pairs, **Cue** for a memory hook, **Pitfall** for a common trap, **Ex** for an example.
- Confusable terms (certification/licensure/credentialing, primary/secondary prevention, online/off-line) get cross-linking *Distinguish* lines.
- "such as" / open-ended lists are NOT carded as closed memorize-these lists.

## Open questions (need Parker's call — answer once and it becomes a rule)
- **Yield level:** is ~27 cards for Chapter 1 about right, or more granular / fewer cards? — *deferred by Parker for now.*

## Changelog
- 2026-06-29: created during the Chapter 1 calibration; seeded with the tastes established so far.
- 2026-06-29: confirmed big-list handling (keep a cohesive list whole, never split; never lump unrelated items). Card-volume question deferred.
- 2026-06-29: adopted two-way definitions (evidence-based, from the AnKing decks + memory research). Converted Chapter 1's definitional cards to the `{{c1::term}} is {{c2::meaning}}` form.
