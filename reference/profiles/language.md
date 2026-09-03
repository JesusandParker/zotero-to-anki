# Language profile

For Arabic, Spanish, and Mandarin study materials — textbooks, workbooks, graded readers.

Language is the profile that departs most from the rest of the pipeline, because the goal
is **production under time pressure**, not recognition of a fact. Read this before
drafting; the universal rules in `card-rules.md` still bind, but several defaults flip.

---

## 1. What it's for
Reaching working fluency (~B2) — understanding and *producing* the language, not passing a
quiz about it. The test is a conversation, not a multiple-choice item.

## 2. Archetype mix
- ~45% vocabulary (word ↔ meaning, two-way — see below for the direction rule)
- ~20% morphology and patterns (verb forms, plurals, agreement, Arabic root patterns)
- ~15% grammar rules stated as a usable trigger ("when do you use X")
- ~10% fixed phrases / collocations / idioms, kept whole
- ~10% script, orthography, pronunciation

## 3. Direction is the whole game
`parker-preferences.md` makes definitions two-way by default, and for language that
default is **more** important, not less — but the two directions are not equal:

- **Recognition** (see the word → give the meaning) is the easy direction and comes free
  from reading.
- **Production** (see the meaning → produce the word) is the one that actually builds
  fluency and the one he'll fail without.

So: two-way by default, and when only one direction is affordable, **keep production**.
Do NOT two-way a fixed phrase, an example sentence, or a grammar rule.

## 4. Script, diacritics, and RTL
- **Arabic is right-to-left.** Never mix an RTL span and a Latin span inside one cloze — the
  rendering is unpredictable in Anki. Keep the Arabic on its own line; put the English on
  another line.
- **Vowel marks (harakat) are meaningful.** If the textbook prints them, keep them: the
  unvowelled form is a different, harder card and shouldn't be created by accident. If a
  card is specifically *about* vowelling, say so in the stem.
- **Never cloze a bare letter** unless the card is teaching that letter's form. A one-glyph
  blank is unanswerable in a shuffled deck.
- Check any Arabic card renders correctly in Anki the first time — the same one-time visual
  confirmation the MathJax cards got (`note-format.md`).

## 5. Traps
- **A dictionary gloss is not a definition.** "kataba = to write" is fine; "kataba = to
  write, to compose, to draft, to record, to inscribe" is five cards' worth of fuzz under
  one blank and fails the crisp-cloze rule (card-rules #5, R12). Pick the core sense; put
  the others in `Back Extra` under `Meaning:`.
- **Don't card a paradigm as one giant list.** A full verb conjugation table is a
  grouped-list card only if Parker genuinely memorizes it as one unit; otherwise it's the
  *pattern* that's worth a card, with the table in `Back Extra`.
- **Cognates and false friends need a `Distinguish:` line** — that's exactly what the field
  is for.
- **Don't invent example sentences.** Ground every example in the textbook page like any
  other claim (card-rules #10). If the book didn't give one, don't fabricate one.

## 6. The purple lane in a language source
A purple word here is vocabulary Parker met and couldn't read — which is this profile's
CORE material, so §3's direction rule OVERRIDES §4b's one-way default: **two-way by
default, and when only one direction is affordable, keep PRODUCTION** (meaning → word).
The gloss is still authored-plain (card-rules #28) and still crisp — the §5 trap above
("a dictionary gloss is not a definition") applies with full force. Keep the script rules
(§4) for the term side; the `Ex:` line carries the sentence he met it in, per §4b.

---

## 7. Execution addendum — everything the Arabic Unit 1 run proved (2026-08-08)

The sections above say what language cards should BE; this section says how to BUILD them
without repeating Unit 1's failures. All of it is enforced by running guards, named inline.

### 7a. RTL mechanics (R39, R44)
- **The reviewer decides direction from the card's FIRST STRONG CHARACTER.** A card whose
  Text begins with Arabic renders the ENTIRE card as one RTL paragraph — trailing periods
  jump left, `Distinguish:` colons flip, the AUDIO button swaps sides. Pure-Latin lines with
  no leading/trailing punctuation LOOK fine, which is how it hides.
  **Fix: every Arabic-first Text begins with a literal U+200E LRM** (a character, not a tag
  or entity — gate-legal). Guard: `check_block_spec.py U1-lrm`.
- A line is PURE Arabic or pure Latin, never mixed (bidi scrambles mixed lines around
  neutrals). Keep glyphs out of Back Extra prose; key Distinguish lines on letter NAMES.
- `<div dir="rtl">` would be cleaner but `div` HARD-blocks on ALLOWED_TAGS. Pure lines + LRM
  achieve the same rendering with legal HTML.
- **Transliteration must never be READABLE BESIDE the Arabic it would let you skip reading**
  (R39, refined by R59) — **except while he cannot yet read (R60, 2026-09-01).** In the vocab
  lane the translit rides in `c1` WITH the Arabic: hidden together on the production card (he
  still retrieves the spoken word from the meaning — §3), visible together on the meaning
  card, which is otherwise a bare qualifier beside untaught script. The letter lane is gated
  to the letters class has covered, so vocab may not charge rent on a skill the deck has not
  delivered. `V3-translit-with-arabic` (C_vocab) and `L3-translit-never-beside-glyph`
  (A_letters) say opposite things ON PURPOSE — read R60 before reconciling them. Back Extra
  only was the pre-R60 rule and returns when Parker says he can read. On a two-way LETTER
  note it means the opposite cloze group from the glyph — `{{c1::<glyph>}}` with
  `Transliteration: {{c2::<symbol>}}` — so exactly one of the pair is hidden on either card.
  Translit in `c1` beside the glyph is the defect. Guards: `L2-translit`, `L3-translit-never-beside-glyph`.
- **Diacritics ride a carrier letter** (`بَ`, the book's own convention) — never bare (they
  float and wrap), never on U+25CC (tofu on macOS/iOS).

### 7b. Card shapes that are now the standard (two-way via c1/c2 on ONE note)
- **Letter:** `‎{{c1::ب}}` / `Name: {{c2::baa}}` / `Sound: {{c2::b as in bet}}` — c1 card =
  produce the glyph from name+sound; c2 card = name+sound from the glyph. Family
  `Distinguish:` line name-keyed. Source chart on the back. Official pronunciation video in
  the **Audio field** (autoplays on flip).
- **Symbol:** same shape on a carrier; standalone glyphs (`ء آ ى ة ٱ`) stand alone.
- **Vocab:** `‎{{c1::<Arabic>}}` / `{{c2::<meaning core>}} — <visible qualifier>`.
  Qualifier disambiguates production without bloating the recalled span (crisp-c2).
  **Function words get a blank-style usage frame** that never contains the answer word
  (`fii: the last slot of the intro: "from the city of X, ___ Y"`). Formal/MSA clip in the
  Audio field; dialect clips + translit in Back Extra. Guard: `V1/V2`.
- **A source may EXCLUDE a dialect's audio outright** (`excluded_audio_dialects` in
  `sources.json`). Arabic excludes **maSri (Egyptian)** as of 2026-09-03 (R61): the course
  grades FuSHa and the instructor speaks Levantine, so an Egyptian clip on the back was a
  pronunciation Parker must NOT imitate sitting next to one he should. Do not harvest it, do
  not card it, and do not "restore the full table" in a later unit. The dialect's *forms in
  prose* go with the audio — a `Distinguish:` line teaching Egyptian <i>feen</i> is the same
  defect as the clip. What survives is genuine book knowledge ABOUT the dialect (what maSri
  means, Cairo vs Damascus) when it came from his own highlights. Guard: `V4`.
- **MSA-primary** when the course is MSA (check the course description): Formal is the card,
  dialects are Back Extra enrichment — not three cards per word.

### 7c. Marked SETS (R48, R49 / card-rules #30-31)
Membership lane first (named sub-groups ≤5 + anchor + `Roster:` everywhere), then per-member
cards that (a) NAME THE PROPERTY that defines the set in every stem, (b) quiz BOTH
directions, (c) keep sub-group names as visible scaffolding, never a 20-blank/5-answer
cloze. The one-question test for any derived card: *would it be identical coming from a
different source about a different topic?* Guards: `C1-C5`.

### 7d. Media discipline (R45, R47)
- One home per clip: **the Audio field wins**; Back Extra `[sound:]` only for clips NOT in
  the Audio field. Two play buttons for one clip is a defect. Guard: `U3`.
- **All media filenames lowercase** (case-sensitive on iOS; invisible on the Mac). Guard:
  `U2` + `scripts/media_audit.py`.
- **Never replace a media file's bytes under the same name** — the webview caches by
  filename and serves the stale image through syncs. Version the name (`_v2`, `_v3`),
  repoint the notes, delete the old file. Audit after every write: `media_audit.py`
  (broken refs / uppercase / orphans must all be zero).

### 7e. Source images from a SCAN (R38, R46, R51)
- A scan can be densely OCR'd and contain ZERO target-language text — `grounding: EXACT`
  proves nothing about the script. Arabic-bearing cards need visual/external evidence
  (back-side source crop + `verified_against`), with publisher Unicode (e.g. the course
  platform's lesson JSON) outranking any reading of the page.
- Crops: **measure, don't eyeball** (`scripts/find_crop_boxes.py` — fill-colour band
  segmentation prints each object's true bounds). Build with `make_crops.py`-style
  trim + **no-clip assertion**: after trimming, the ink bbox must not touch any window edge
  — `-trim` can only SHRINK, so a box that cuts the object ships a tidy-looking lopsided
  crop (the alphabet chart lost a whole column this way). Auto-growing the box was tried
  and does NOT work (in-object gutters ≈ object-to-neighbour gaps); it is recorded in R51
  so nobody retries it.
- Review every crop on a CONTACT SHEET before storing. Zero sliced text; symmetric margins.

### 7f. Verification is of the EXPERIENCE, not the artifact (R44's root cause, R50)
- **Render review is mandatory** before hand-off: `scripts/render_check.py` builds real
  rendered cards (model CSS, `dir="auto"`, real media) into one contact sheet — then LOOK.
  Storage checks cannot see direction flips, duplicate buttons, or crop quality.
- **Every requirement Parker states becomes a rule in `check_block_spec.py` the same
  session** — append-only, so a later fix can never silently regress an earlier one (the
  country cards went one-way → two-way → one-way before this existed).
- **A new rule must be tested against a reconstruction of the defect it prevents**
  (`scripts/test_block_spec.py` holds the fixtures). A rule's applies-to predicate must be
  structural, never keyed on the feature under test.
