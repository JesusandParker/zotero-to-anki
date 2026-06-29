# Working in this project (emt-card-maker)

This folder is a **git repository** backed up to a **private GitHub repo**:
`JesusandParker/emt-card-maker` (the Anki card-maker skill: Zotero highlights
to cloze cards).

Parker owns this and is not a heavy coder, so keep version control smooth and
low-friction for him.

## If Parker reports a card issue (the main ongoing loop)
Follow **`SKILL.md` → "If Parker reports an issue with a card"** (read `reference/regression-cases.md` first — the history of every flaw class). Decide one-off vs systemic; if systemic, encode the rule + add a regression test + extend `scripts/check_cards.py`; re-run the checker; log it in `reference/feedback-log.md`; then commit + push. A fresh session needs no prior context — everything is in this repo.

## Version-control workflow
- After meaningful changes here, **commit and push** so the work is saved and
  backed up: `git -C . add -A && git commit -m "<clear message>" && git push`
- **Offer to back up at natural stopping points**, and always do it when Parker
  says "save it" / "back it up." Do not commit half-finished or broken states.
- To undo, **roll back with git** to an earlier commit (Parker can ask in plain
  language, e.g. "go back to before X"); don't hand-edit to "revert."
- Keep credentials out of commits (no API keys/tokens), even though it's private.
