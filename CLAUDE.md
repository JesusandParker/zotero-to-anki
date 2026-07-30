# Working in this project (zotero-to-anki)

This folder is a **git repository** backed up to a **private GitHub repo**:
`JesusandParker/zotero-to-anki` (the Anki card-maker skill: yellow Zotero marks
in ANY source -> cloze cards).

Parker owns this and is not a heavy coder, so keep version control smooth and
low-friction for him.

## If Parker reports a card issue (the main ongoing loop)
Follow **`SKILL.md` → "If Parker reports an issue with a card"** (read `reference/regression-cases.md` first — the history of every flaw class). Decide one-off vs systemic; if systemic, encode the rule + add a regression test + extend `scripts/check_cards.py`; re-run the checker AND `scripts/test_regressions.py`; log it in `reference/feedback-log.md`; then commit + push. A fresh session needs no prior context — everything is in this repo.

## Parker's own edits are sacred
He constantly adds his own work to these cards — mnemonics he invented, pasted images, TTS
audio, notes to himself. **Never overwrite a field this system did not write.** Check first
with `python3 scripts/authorship.py check --source <id> --note <noteId>`; `edited` and
`unknown` are protected, and `unknown` covers everything predating the store. Content that
is not in the textbook may be *his*, not a fabrication — verify before "correcting" it.
Run `python3 scripts/authorship.py self-test` after touching that module.

## Version-control workflow
- After meaningful changes here, **commit and push** so the work is saved and
  backed up: `git -C . add -A && git commit -m "<clear message>" && git push`
- **Offer to back up at natural stopping points**, and always do it when Parker
  says "save it" / "back it up." Do not commit half-finished or broken states.
- To undo, **roll back with git** to an earlier commit (Parker can ask in plain
  language, e.g. "go back to before X"); don't hand-edit to "revert."
- Keep credentials out of commits (no API keys/tokens), even though it's private.

## Scope reminder
This skill is **source-agnostic**. Anything specific to one book (its PDF, colors, page map,
Anki decks, tags, subject emphasis) belongs in `reference/sources.json` or
`reference/profiles/`, never hard-coded in a script or written into the universal card rules.
If you find yourself typing "EMT" into `card-rules.md`, `editor-checklist.md`, or a script,
it belongs in a profile or the registry instead.

