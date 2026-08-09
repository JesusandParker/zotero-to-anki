# Arabic unit playbook — how "do Unit N of the Arabic textbook" runs end-to-end

Written 2026-08-08 after the Unit 1 overseer run so any fresh session can execute a unit
without this history in context. The source is registered (`arabic` in `sources.json`); the
canon rules live in `profiles/language.md` §7 and card-rules #30-31; the guards named below
are executable and must all pass before hand-off. **Unit 1's failure pattern was: every
storage gate green, Parker's eyes found five rounds of defects.** The playbook's whole job
is that the guards see what he sees, first.

## 0. Facts you would otherwise rediscover slowly
- **The PDF is a scan with ZERO Arabic in its text layer** (all 251 pages). Prose cards
  ground normally; anything Arabic grounds on page renders + external authority.
- **Publisher Unicode + official audio come from Lingco** (`class.lingco.io`, course 4839
  "Alif Baa: Independent Learners", joined with code `ec098d5`). Per lesson:
  `/api/content/lessons/<id>` (authenticated in-browser fetch) → table HTML carries an
  audio-asset UUID per cell; `/api/assets/<uuid>` 302s to a tokenised URL **fetchable by
  plain curl, no cookies**. Origin filenames (`AB3e_U1VE-…`=Egyptian, `U1VS`=Levantine,
  `U1VSt`=Formal) cross-check the mapping. Snapshot both the vocab JSON and an audio
  manifest into `work/arabic/` (Unit 1 examples: `lingco_unit1_vocab.json`,
  `lingco_audio_manifest.json`).
  **Trial ends 2026-08-22** — harvest remaining units' audio before then, or after Parker
  buys access (he plans to once enrolled in the real section).
- **Letter pronunciation videos** for all 28 letters are already local:
  `~/Anki Media Archive/Arabic - Al-Kitaab pronunciation/` (staged copies:
  `work/arabic/media/arabic_pron_NN_<name>.mp4`, lowercase).
- **Book-name transliteration is canon** (siin, shiin, Saad, DHaa, cayn…) — video filenames
  disagree (seen/sheen/ha); cards follow the BOOK.
- Segment map is physical-page verified (`reference/maps/arabic.json`); the printed→physical
  offset DRIFTS (+14→+17), so never compute pages from printed numbers.
- Deck: `all::LIBERTY::…::ARAB 101 - Elementary Arabic I::Unit {N}::claude review`
  (+ `Book Highlights` promotion sibling). Model `AnKing Cloze`; `Audio` field exists.

## 1. Per-unit sequence
1. **Extract**: `python3 scripts/extract_highlights.py --source arabic --segment N` — then
   PRINT the idx→highlight table and key every card's `from_idx` off it (Unit 1's off-by-N
   came from assigning indices from memory).
2. **Harvest Lingco** for the unit: lesson JSON(s) via the module list
   (`/courses/4839/modules`), audio via curl per asset UUID. Lowercase filenames:
   `arabic_vocab_uN_<row>_<slug>_<dialect>.mp3`. Snapshot JSON + manifest to `work/arabic/`.
3. **Render + measure + crop** evidence pages:
   `render_page.py` → `.venv/bin/python scripts/find_crop_boxes.py <pages>` (measured
   bounds, never eyeballed) → boxes into a `make_crops.py`-pattern build (trim + **no-clip
   assertion**, uniform mat, versioned `_v1` names for the new unit) → **review the contact
   sheet**: zero sliced text, symmetric margins, row counts match the source table.
4. **Generate** with the Unit 1 generator as the template
   (`work/arabic/gen_unit1_cards.py` — copy to `gen_unitN_cards.py`): LRM prefixes, pure
   lines, two-way c1/c2 shapes, MSA-primary vocab with usage frames, membership+property
   lanes for any marked set, `Roster:` on chunked notes, evidence fields on every card.
5. **Gate, all four** (all must pass):
   `verify_report.py` → `check_cards.py` (stamp) → `check_block_spec.py` (cumulative
   requirements — **append a rule for any new preference Parker states, same session**, then
   extend `reference/fixtures/` + run `test_block_spec.py`) → stage.
6. **Stage** `anki_write.py --run …` → **Audio field pass** (AnkiConnect
   `updateNoteFields`; primary clip only — video for letters, Formal mp3 for vocab).
7. **Audit + render review** (the two guards that close Unit 1's blind spot):
   `media_audit.py --deck … --prefix arabic_` (zero broken/uppercase/orphans) and
   `render_check.py --deck … --cards …` → **LOOK at the contact sheet** against its printed
   checklist.
8. **Hand off** per SKILL.md Stage 4 (margin comments answered, exclusions honored,
   needs_human_check list, purple lane status) + remind Parker to sync. Close the run
   (`run_store.finish`, hazards closed per the hazard rule).

## 2. Letters in Units 2-10: EXTEND, never re-mint
Units 2-10 teach the 28 letters properly (positional forms, connection, writing). The 28
letter notes already exist — **do not create new letter notes**. Extend the existing note
(match by its c1 glyph; pipeline-authored, so `updateNoteFields` is licensed):
- Add the unit's new content as NEW same-note lines or new cards only via new cloze numbers
  when it is genuinely a new retrieval (e.g. `Forms: {{c3::ب ﺑ ﺒ ﺐ}}` once Unit N teaches
  them) — keep every line pure-script or pure-Latin, LRM rule unchanged.
- Six letters do not connect forward (ا د ذ ر ز و): two forms, not four.
- Sibling burying already spaces the added cards; check `check_block_spec.py` still passes
  (its letter rules key on structure, so extending is safe — update rules if the shape
  legitimately evolves, in the same commit).
- New-unit vocab/dialogues/drills = new notes as usual.

## 3. The mistakes this playbook exists to prevent (map to guards)
| Failure (all shipped in Unit 1) | Guard that now catches it |
|---|---|
| Whole-card RTL flip (first-strong char) | `U1-lrm` + `render_check.py` (R44) |
| Two play buttons for one clip | `U3` + render review (his screenshot) |
| Boilerplate cue lines | `U4` |
| One-way cards after a "fix" | `check_block_spec.py` C2/V1/L1 — append-only (R50) |
| Set carded as rows only / property stripped | `C1/C4/C5` (R48, R49) |
| Lopsided crop, sliced column | no-clip assertion + `find_crop_boxes.py` + contact sheet (R46, R51) |
| Stale image after "fixing" media in place | versioned filenames + `media_audit.py` (R45) |
| Uppercase media silently broken on iPhone | `U2` + `media_audit.py` (R47) |
| Wrong Arabic read off the scan | external authority (Lingco snapshot) in `verified_against` (R38) |
| `from_idx` keyed from memory | step 1: print the extractor table first |
| Checker that never fails | `test_block_spec.py` fixtures — extend with every new rule |

## 4. Open items Parker owns
- Alphabet-ORDER recitation cards (the membership lane for the letters themselves): his
  call, deliberately not built.
- Buying Lingco access / harvesting Units 2-10 media before 2026-08-22.
- Promotion of Unit 1 keepers from `claude review` into `Book Highlights`.
