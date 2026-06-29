# Feedback Log — issues Parker caught while studying, and how they were resolved

The running record of the study → catch → fix loop. Newest at the top. Each entry: **what Parker flagged**, the **fix**, and whether it became a permanent **rule + regression test** (systemic) or was a one-off. A fresh Claude session can read this to see the live history of what's been refined.

Parker reports issues two ways: **(a) tell Claude directly** in any session ("I noticed an issue with an EMT card…") — easiest, and Claude logs it here; or **(b) jot a quick line at the top of this file** between sessions, and Claude processes it next time.

---

## Open (jot new issues here)
<!-- Parker: drop a one-liner here anytime, e.g. "- card on X: the hint feels too revealing" -->

## Resolved

- **2026-06-29 — "the pathway card's parentheticals give away the answer."** The `(state authority granted)` after `{{c1::licensure}}` was the term's definition → a crutch. *Systemic (leak/crutch class):* fixed the card (defs → Back Extra), encoded `card-rules.md` #3 + `editor-checklist.md` #15 + regression case **R3**, and added the parenthetical-after-cloze + literal-answer-in-stem warnings to `check_cards.py`. Also caught 2 more leaks (ADA Title I, EMR) in an audit.
- **2026-06-29 — "the public-health card doesn't test the goal."** The goal ("preventing health problems") sat as visible scenery, untested. *Systemic (under-clozing):* fixed to a 3-cloze card, sharpened `card-rules.md` #7 + `editor-checklist.md` #4, regression case **R1**.
- **2026-06-29 — "the AEMT skills are sitting unclozed."** Used the "such as" rule as an excuse to skip a real skill list. *Systemic (shortcut / under-clozing):* added the explicit Fact Pass (must-test / supporting / skip) to the pipeline; regression cases **R1/R5**.
- **2026-06-29 — over-production (76 cards from 36 highlights).** The decomposed per-unit fan-out duplicated facts across units. *Systemic:* added the Stage 2.5 global-consolidation pass + `card-rules.md` #12; regression case **R2**.
