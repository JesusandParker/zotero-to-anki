# Overseer log — Arabic Unit 1 (2026-08-08)

First run of the pipeline on the Arabic source, driven by a single overseer session per
Parker's request, with every deviation and lesson recorded here **for encoding into the
canon (rules / profile / scripts / GitHub) next session**. 90 notes → 146 cards staged to
`…ARAB 101 - Elementary Arabic I::Unit 1::claude review`. Gate HARD-clean, 87/87 regressions pass.

## What shipped
- 28 letter notes (c1 = write the glyph · c2 = name + book's sound gloss together), official
  AB3e mouth video in `Audio` field (autoplays on flip), dot-family `Distinguish:` lines,
  alphabet-chart crop on every back.
- 15 symbol notes (14 chart symbols on carrier `ب` where combining + hamza-not-in-chart
  gotcha), symbols-chart crop on backs; short vowels carry the vowel-chart sound.
- 9 vocab notes, **MSA-primary** (course = Modern Standard per Lingco course description):
  c1 = Arabic (publisher Unicode), c2 = crisp meaning core with the disambiguating qualifier
  visible outside the cloze; Formal audio in `Audio` field; Egyptian/Levantine clips +
  translit in Back Extra; vocab-table crop on backs.
- 11 system + 6 dialect + 1 culture prose cards (English text layer, normally grounded).
- 20 country-capital cards (map-legend per-key pattern, map crop on backs; Kuwait carded as
  "capital shares the country's name" because capital==country made the plain blank self-answering).

## Lessons for next-session encoding (the actual deliverable of overseer mode)
1. **Zero-Arabic text layer** — R38 written. Registry needs `force_visual` per source;
   `check_cards.py` needs an answer-script ∉ context-script check. The extractor's
   SPARSE/CAPTION heuristics are the wrong detector for "dense English, missing script."
2. **RTL discipline** — R39 written. Pure-line rule (never mix scripts on one `<br>` line);
   translit answer-side only; carrier letters for diacritics (`بَ`, never bare, never U+25CC);
   `<div dir>` would be cleaner but `div` HARD-blocks — either extend ALLOWED_TAGS for
   language profiles or keep pure-line. Encode in `profiles/language.md`.
3. **Two-way via c1/c2 on one note** replaces any note-type split (bury-siblings spaces the
   two directions; `anki_write` copies the preset). Letter shape: c1 glyph / c2 name+sound
   joint. Vocab shape: c1 Arabic / c2 meaning-core, qualifier visible. → `card-recipes.md`
   language section.
4. **External authority lane** — publisher Unicode (Lingco lesson JSON) outranks reading the
   scan. Snapshot lives at `work/arabic/lingco_unit1_vocab.json` + `lingco_audio_manifest.json`;
   cite in `verified_against`. My own scan-read of اسمي was wrong (I read إِسمي) — the
   external snapshot caught it. Formalize as a `sources.json` field (`external_authority`).
5. **Audio field exists on AnKing Cloze** (`Text, Back Extra, Audio, …`) — note-format.md
   field list is stale. `anki_write.py` should learn an optional `Audio` key (this run set it
   post-stage via AnkiConnect `updateNoteFields`, safe on pipeline-authored fresh notes only).
6. **Media naming**: everything pipeline-owned is `arabic_*` (authorship-guard compatible);
   crops renamed `src_*.png` pre-write because `anki_write` prefixes `<source>_` itself.
7. **Figure-index stages correctly SKIPPED** for a scan: every page is one JPEG; there are no
   discrete embedded plates to harvest. Direct render→crop is the sanctioned `needs_visual`
   path. A `kind: scan` hint in the registry could make this decision automatic.
8. **Provenance gap**: `anki_write --run` linked 0 noteIds because overseer mode didn't write
   per-card `provenance.jsonl` rows during drafting. Cards still carry `from_idx`. Next
   session: emit provenance rows from the generator, or have `anki_write` synthesize them
   from the cards file.
9. **from_idx off-by-N hazard**: I first assigned indices from memory of the Zotero dump and
   was wrong for p17–p26 (chart-request marks shift everything). Rule: **always print the
   extractor's own idx→highlight table and key assignments off it** (that table caught it).
10. **Autoplay stacking**: vocab backs autoplay Formal (Audio field) and then the dialect
    clips in Back Extra, in order; letter backs autoplay the video. Deliberate — Parker can
    veto; if so, dialect clips become click-to-play via `[anki:play]` links or move to a
    non-autoplay presentation.
11. **Book-name transliteration is canon** (siin not seen, DHaa, cayn, tanwiin aD-Damm…);
    video archive filenames disagree (seen/sheen/ha) — names on cards follow the BOOK.
12. **Unit 1 scope**: isolated letter forms only, by design; Units 2–10 must EXTEND the same
    28 notes (positional forms, writing) rather than mint new ones. Extension workflow TBD.
13. **Trial clock**: Lingco Independent Learners trial ends **2026-08-22**; all 26 vocab
    clips are downloaded locally so cards never depend on the session. Letter videos were
    already local. Units 2–10 media should be pulled while access lasts (one lesson JSON +
    asset sweep per unit, ~30 min total) or after he buys access.
14. **Judge clearances** (recorded here, per note-format's clearance rule): #54 contrast-anchored
    ("unlike Latin…"); #56/#59/#60 same-index pairs each cold-solvable with sibling shown;
    #65 anchors (shaami/maSri) stay visible, only equivalents hidden; #69 examples moved to
    Back Extra then cleared. `<br>`-list warnings are auto-repaired by `anki_write.listify()`.

## Hand-off flags for Parker (also delivered in chat)
- Drill 2 header mark: carded the transliteration-system facts; the 21 translit place-names
  themselves are NOT carded — does he want decode-practice cards for them?
- The `Formal:`-style pronunciation line uses `Cue:`/`Ex:`/`Distinguish:` labels; a dedicated
  `Variants:`/`Pronunciation:` Back-Extra label is worth adding to the house list.
- needs_human_check: 0 cards (all numeric facts verified against context or renders).
