# Arabic Unit 2 — alif section, pp. 40-42 physical (printed 20-22) — night unit 20260904-0840-1

Alif Baa 3e (600 dpi scan, attachment SPRRWAP7). Night-shift unit scoped to **6 marks**
(5 yellow, 1 purple) on the alif pages of Unit 2. **3 new notes** →
`…::ARAB 101 - Elementary Arabic I::Unit 2::Book Highlights` (tag `arabic-u2` + night tags
`night::2026-09-04`, `night-unit::20260904-0840-1`), **1 existing Unit 1 letter note extended
in place** (alif, 1786229797674 — NO night tag, so a block-delete by tag leaves it alone),
**1 mark deferred** (Drill 1 audio — see below). Nothing dropped, nothing invented.

## Marks → cards
| idx | key | mark (page) | outcome |
|---|---|---|---|
| 0 | XLD9U2BZ | purple "wel quality" (p40) — midword drag slip, term fixed to **vowel quality** | lexicon card 1788528744775 (external anchor, flagged for the Vocabulary block) |
| 1 | YKTUQ9YB | "Arabic also distinguishes vowel length" — stored on p40, sentence is on p41 (NOT_FOUND) | grouped with idx 3 → card 1788528745451 |
| 2 | NSNM2FEZ | "Drill 1. Hearing frontal and deep alif" + margin comment asking for Lingco audio cards | **deferred** — Lingco unreachable unattended (permission classifier blocked the Chrome route); generator + recipe prepared: `work/arabic/gen_unit2_drill1_cards.py` |
| 3 | Y7TW6BPR | "Long vowels attract word stress in Arabic." (p41) | card 1788528745769 |
| 4 | PRLWHU2C | "In both cases the alif does not connect to what follows it. Always pick your pen up…" (p42) | alif note extension (c1: connects? no) |
| 5 | H34SH2F2 | "Writing" (the word inside idx 4's sentence) + margin comment: flashcards for each position "like all the positions of BAA" | alif note extension (c1: four positional shapes as cued rows) |

## The cards
1. `<b>Vowel quality</b> is {{c1::which particular sound a vowel has}}.` — one-way (English phonetics
   term, not target-language vocab); Ex (p40 verbatim) / Distinguish (quality vs length, bet-bat-but) /
   Why (dialect east-west, surrounding consonants). `needs_human_check: true` (R35).
2. `Besides vowel <i>quality</i>, Arabic also distinguishes vowel {{c1::length}}, and this too can change a word's meaning.`
   Ex (DHaalim) / Distinguish / Cue. Cites idx 1 + 3; grounded on the p41 render (crop in figures/).
3. `In Arabic, word stress is attracted to the syllable with a {{c1::long::long or short}} vowel.` Ex (DHaalim) / Distinguish (length vs stress).

## The alif extension (playbook §2: EXTEND, never re-mint)
Text only (authorship: `owned`); Back Extra (`edited`) and Audio (`unknown`) untouched, asserted
unchanged before and after the write. Appended, all in **c1** with the glyph:
`Connects to the letter after it? {{c1::no — always pick the pen up after it::yes/no}}` and
`Shapes — independent, initial, medial, final:` + four LRM-prefixed pure-Arabic rows
`{{c1::ا::independent}} {{c1::ا::initial}} {{c1::ـا::medial}} {{c1::ـا::final}}`. No new cards
spawned (still c1/c2); both cards stay in Unit 1::Book Highlights. Block-spec L1/L2/L3/U1 hold.
Canon synced: `work/arabic/unit_1_cards.json` alif Text updated to match live (stamp stale by design).
Why not one card per position: sibling clozes on one note reveal the other shapes (card-rules #24),
separate notes would be near-duplicates for alif (two distinct shapes) and violate the no-new-letter-notes
rule, and the playbook's `Forms: {{c3::…}}` idea fails block-spec L1 (letters = exactly c1/c2) — a
daytime rule change if Parker wants it.

## Anchor judgement
`lexicon.py --find` hit only p122 (*"vowel quality is the easiest way to distinguish between س and ص"*),
82 pages away (R61 `far_from_mark`), a usage sentence. The book defines the term on the marked page in a
frame the finder cannot match (*"we refer to these differences in pronunciation as vowel quality"*).
Anchor kept **external + derived flag**; the gate's one warning was cleared by both the editor and the
judge, recorded on the card's `verified_by`.

## Editor & judge (both independent subagents)
- Editor: 4 REWRITEs — lexicon answer carries the which-sound discriminator (check 30); the `{{c1::meaning}}`
  blank was open-set (stress/pronunciation/meaning) and is now visible context (1/18/19); `DHAA-lim` →
  the book's `DHaalim`, restating Cue → grounded Distinguish (3/11); the alif connection fact moved from
  c2 to c1 because in opposite groups each derived the other (2/15/6).
- Judge: PASS on all three cards and on both alif cards separately; warning CLEARED; one bookkeeping
  nit (a grounding attribution) fixed.

## Figures
No captioned plates exist on pp.40-42 (scan; the only art is the alif shapes strip and handwriting
samples). `build_figure_index.py` **crashed** on the empty segment (hazard, deferred). No proposals, no
attachments. Evidence crops (not attached to cards): `figures/night_20260904-0840-1_ev_p41_alif_shapes.png`,
`figures/night_20260904-0840-1_ev_p41_vowel_length.png`.

## Render review / media / live sweep
- `figures/render_review.png` (local HP tool `work/arabic/night_render_check_hp.py`; the shared
  render_check.py needs the Mac's ImageMagick, which is absent): all 10 sides LTR, pure lines, hints
  render Latin on the front and pure Arabic on the back, one audio button — **clean**.
- `media_audit.py` on the whole Arabic tree: 120 notes, 121 refs, all clear.
- `check_cards.py --live 2`: 17 cards clean. `--live 1`: 5 pre-existing warnings on older Unit 1 notes
  (not tonight's; the alif note is clean).

## Deferred: Drill 1 (Parker's margin comment)
Not built — no guessing. Daytime recipe (playbook §0): module 27015 → Drill 1 lesson JSON → per item the
audio asset UUID + correct answer (F/D) → `curl -L /api/assets/<uuid>` → lowercase clips
`arabic_u2_drill1_NN.mp3` → snapshot `work/arabic/lingco_unit2_drill1.json` →
`python3 work/arabic/gen_unit2_drill1_cards.py --highlights <file carrying NSNM2FEZ>` → gates → write.
**The night ledger marks NSNM2FEZ processed with the unit, so it will not re-queue on its own.**

## Hazards
Five entries in `manifest.json`; four deliberately left RED (daytime gate-code work), one
`mechanizable: false` (permission policy). See `new_hazards_found`.
