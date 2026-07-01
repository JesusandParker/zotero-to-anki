# Feedback Log — issues Parker caught while studying, and how they were resolved

The running record of the study → catch → fix loop. Newest at the top. Each entry: **what Parker flagged**, the **fix**, and whether it became a permanent **rule + regression test** (systemic) or was a one-off. A fresh Claude session can read this to see the live history of what's been refined.

Parker reports issues two ways: **(a) tell Claude directly** in any session ("I noticed an issue with an EMT card…") — easiest, and Claude logs it here; or **(b) jot a quick line at the top of this file** between sessions, and Claude processes it next time.

---

## Open (jot new issues here)
<!-- Parker: drop a one-liner here anytime, e.g. "- card on X: the hint feels too revealing" -->

## Resolved

- **2026-07-01 — the writer targeted a DELETED note type (would hard-fail on the next run).** Two hours after this skill was built (2026-06-29), Parker restyled his whole collection to the AnKing look; his homemade cloze cards migrated to the **`AnKing Cloze`** note type and the old **`01_Cloze - Parkers Note Type`** was deleted. But `anki_write.py` still hard-coded the old model (and `sys.exit`s if it's missing), so the very next `anki_write.py` run would have died before writing a card. *Systemic (silent config drift):* pointed `MODEL` at `AnKing Cloze` (verified live via `notesInfo` on `tag:claude_generated` — his 33 EMT notes are on it), documented the 5-field layout in `note-format.md` (we fill only `Text` + `Back Extra`; the other three are his study fields — never write them), and made the "model missing" error message tell a future session how to re-point it. Dry-run verified against the live collection.
- **2026-07-01 — bury-siblings was never turned on (the two-way-definition freebie).** Two-way definition notes make two sibling cards; without bury-siblings they can appear back-to-back the same day, which inflates the sense of mastery. The 2026-06-29 adoption of two-way defs had flagged this as a to-do and it was never done. *Config fix:* created a dedicated **`EMT` deck preset** (cloned from Default so his other decks are untouched) with new/review/interday bury all ON, and assigned it to `all::EMT` + `all::EMT::_Review`. Verified live.

- **2026-06-29 — "the pathway card's parentheticals give away the answer."** The `(state authority granted)` after `{{c1::licensure}}` was the term's definition → a crutch. *Systemic (leak/crutch class):* fixed the card (defs → Back Extra), encoded `card-rules.md` #3 + `editor-checklist.md` #15 + regression case **R3**, and added the parenthetical-after-cloze + literal-answer-in-stem warnings to `check_cards.py`. Also caught 2 more leaks (ADA Title I, EMR) in an audit.
- **2026-06-29 — "the public-health card doesn't test the goal."** The goal ("preventing health problems") sat as visible scenery, untested. *Systemic (under-clozing):* fixed to a 3-cloze card, sharpened `card-rules.md` #7 + `editor-checklist.md` #4, regression case **R1**.
- **2026-06-29 — "the AEMT skills are sitting unclozed."** Used the "such as" rule as an excuse to skip a real skill list. *Systemic (shortcut / under-clozing):* added the explicit Fact Pass (must-test / supporting / skip) to the pipeline; regression cases **R1/R5**.
- **2026-06-29 — over-production (76 cards from 36 highlights).** The decomposed per-unit fan-out duplicated facts across units. *Systemic:* added the Stage 2.5 global-consolidation pass + `card-rules.md` #12; regression case **R2**.
