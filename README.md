# EMT Card Maker (Claude skill)

Parker's system for turning yellow Zotero highlights from his EMT textbook into excellent Anki cloze cards. Built 2026-06-29 to replace the old ChatGPT "v60" pipeline.

**Yellow = "make a card." Blue = ignored.** Those are the only two highlight colors in the book (normalized 2026-07-29; the early chapters were originally green).

## How to use it
In Claude Code, say something like **"make my Chapter 1 EMT cards"** (or "I finished highlighting chapter 3"). The skill runs:

1. **Extract** your yellow (`#ffd400`) highlights for that chapter from Zotero, each grounded in its surrounding page paragraph.
2. **Draft → Edit** each highlight into card(s): classify the fact, write it against the rules, then run an adversarial Editor pass that kills vague / tautological / under-clozed / low-yield cards.
3. **Stage** the survivors into that chapter's `all::EMT::Chapter <N>::claude review` deck in Anki (tagged `ch<N>`), where you review, edit, and promote the keepers into the sibling `Book Highlights` deck yourself.

Anki must be **open** for the write step.

## What's where
- `SKILL.md` — the operating instructions Claude follows.
- `reference/card-rules.md` — the card standard (form rules + the editorial judgment rules the old deck lacked).
- `reference/editor-checklist.md` — the 11-point "try to break this card" pass.
- `reference/note-format.md` — exact Anki note type, syntax, deck targets.
- `reference/cloze-mastery.md` — your 2,391-example AnKing field guide (the gold standard cards imitate).
- `reference/chapter_pages.json` — textbook page→chapter map.
- `scripts/extract_highlights.py` — Zotero yellow highlights → grounded JSON (read-only on Zotero).
- `scripts/render_page.py` — render a table/figure page to an image for visual cards.
- `scripts/anki_write.py` — safe, one-at-a-time write into `all::EMT::Chapter <N>::claude review` (per chapter).

## Design notes
- **Greenfield:** the old EMT deck was exported to iCloud and deleted, so there's no dedup step — every card is new.
- **The star piece** is the Editor stage: the old system was a great *formatter* with no *editor*; this adds the editor.
- **Backup:** this skill's source is mirrored to Google Drive, but the *live* skill must stay in `~/.claude/skills/` to work.
- The first chapter is run slowly and interactively to tune the rules to Parker's taste; later chapters run with less hand-holding.
