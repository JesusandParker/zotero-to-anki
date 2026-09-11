# Arabic — Unit 2 (alif baa taa thaa waaw yaa), 2026-09-11

**35 new notes** into `…::ARAB 101 - Elementary Arabic I::Unit 2::Book Highlights`
(which now holds 38 notes / 56 cards), plus **1 live letter note extended** (waaw).

## Scope
The extractor found **37 marks** in Unit 2 (33 yellow, 4 purple) and **8 margin comments**.

| | |
|---|---|
| carded this run | 32 marks |
| already carded by the 2026-09-04 night run | 4 marks ([0] vowel quality, [1] vowel length, [3] word stress, [4] alif does not connect) |
| blocked, escalated to Parker | 1 mark ([2], the Drill 1 audio request) |

Unit 2 teaches **six** letters, not the four its segment label names: alif, baa, taa, thaa
(printed pp. 21-29) and then, skipping ahead, the other two long vowels **waaw** and **yaa**
(pp. 30-31), followed by the three short vowels.

## What was built
- **15 concept cards** (`D_system`) — the three long vowels and their short partners, vowel
  length, fatHa / Damma / kasra: quality range, frontal consonants, name meanings, and how a
  short vowel is written.
- **13 letter-form notes** (`A_letter_forms`) — one note per (letter x position), for the
  *connected* forms of baa, taa, thaa, yaa plus waaw's joined shape. Each carries the book's
  own printed Writing row on the back. This is Parker's most-repeated margin request.
- **3 culture cards** (`E_culture`) — the Shaking hands box.
- **3 lexicon cards** (`L_lexicon`) — consonant, short vowel, syllable.
- **1 vocab card** (`C_vocab`) — برافو *braafoo*, "Bravo!", per his margin ask on p47.
- **waaw letter note extended** with the connector fact from mark [13], append-only, mirroring
  the line the alif note already carries.

## Consolidation — 7 drafted notes dropped
An independent duplicate audit against all 131 live ARAB 101 notes found that the
**independent** form of each letter is not new work: every letter's Unit 1 note already prompts
Name/Transliteration/Sound and asks for exactly that isolated glyph, and the reverse card would
have asked a position a lone glyph answers by itself. Dropped the independent-form notes for
baa, taa, thaa and yaa, both alif notes (the 9/4 night run already put all four alif shapes on
the live alif note), and waaw's independent/initial note. What Unit 2 genuinely adds is the
**connected** forms, and those are what shipped.

## Verification
- `check_cards.py` — 0 hard errors; 3 warnings, each with a recorded clearance in `verified_by`.
- `check_block_spec.py` — 21 accumulated requirements, all satisfied (4 of them new, below).
- `test_regressions.py` 110/110 · `test_block_spec.py` green.
- `media_audit.py` — 166 notes, 154 refs, 0 broken / 0 uppercase / 0 orphans.
- `render_check.py` — contact sheet reviewed: no RTL flips, no duplicate play buttons, plates
  complete with even margins, both cloze directions present.
- Two independent adversarial editors ran the full editor checklist; both independently
  confirmed the positional Unicode letter-by-letter against the book's plates.

## New executable requirements (append-only, this session)
`F1-position-cued`, `F2-two-way`, `F3-one-shape-per-note`, `F4-plate` in
`check_block_spec.py`, with a bad fixture reconstructing the defect they prevent (all four
positional shapes crammed under one cloze number). Parker asked for a card per position four
times in the margins; these keep a later rebuild from collapsing that shape.

## Figures
Six plates, one per letter, cropped from the book's own printed Writing row. Boxes were
**measured** (a red-ink band segmenter written for this, since `find_crop_boxes.py` masks a
pale table fill these rows do not have), proved by a **no-clip assertion**, and matted in the
page's own paper colour. The assertion caught two real clips during the build. The first
contact sheet showed **reverse-side bleed-through** on every plate — which Parker's figure bar
forbids outright — so the plates now composite the red ink over flat paper, removing the ghost
without touching a glyph.
