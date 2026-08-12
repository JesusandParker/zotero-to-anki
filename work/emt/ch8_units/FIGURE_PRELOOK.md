# Ch8 figure pre-look (before match/judge) — 2026-08-12

Eyeballed the plates most likely to reach cards, against Parker's bar (complete figure,
no fragments, no page-text bleed — parker-preferences 2026-08-08). Verdicts feed the
judge/repair pass; nothing here is attached yet (fresh segment).

| plate | state | repair needed before it may ship |
|---|---|---|
| TABLE_8_3.png | COMPLETE — all six rows + credit (R32 fix held) | rows 5–6 sit at a narrower indent than 1–4 (page-break seam). Cosmetic; acceptable if judge agrees, else re-composite with aligned margins. |
| SKILL_DRILL_8_7.png | all 8 steps + captions present | MISSING banner strip; trailing numbered list TRUNCATED (items 1–2 of 8) — looks-complete-but-isn't, must be cropped off (or completed). |
| SKILL_DRILL_8_9.png | 3 steps + captions + COMPLETE 5-item list | MISSING banner strip (title). |
| SKILL_DRILL_8_10.png | banner + 4 steps + captions (index metadata says "3 steps" — undercount, plate actually complete) | trailing numbered list TRUNCATED (items 1–3 of 6) — crop off or complete. |
| SKILL_DRILL_8_11.png | banner + 4 steps + captions + complete 4-item list | trailing PAGE-TEXT BLEED: "Other Carries" section + draw-sheet paragraph — crop off after the numbered list. |
| SKILL_DRILL_8_12.png | banner + 4 steps + captions (Step 1 caption displaced above its photo — book's own page layout) | trailing one-sentence bleed ("If a patient is sitting in a chair…") — crop off. |

Repair route: ImageMagick surgery on the archive composites (bottom-crop the bleed;
prepend the banner strip rendered from the drill's caption page), then regenerate the
matted study copies. Not yet in Anki media, so no versioned-rename requirement — but
verify each repaired plate by eye before match/attach.
