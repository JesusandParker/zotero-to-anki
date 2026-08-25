# Anki Note Format & Write Targets

The exact shape every card must take, and where it goes. Verified live against Parker's collection on 2026-07-01.

## Note type
- **Model:** `AnKing Cloze` (a Cloze type). This replaced `01_Cloze - Parkers Note Type` on 2026-06-29, when Parker restyled his whole collection to the AnKing look and the old type was deleted; all existing EMT cards were migrated.
- **Fields, in order (verified live 2026-08-08):** `Text`, `Back Extra`, `Audio`, `Lecture Notes`, `Missed Questions`, `Additional Resources`, `Card Feedback`.
- **`Audio` (added by Parker's HyperTTS setup) autoplays on flip** and is the ONE home for a
  card's primary clip (letter pronunciation video, MSA vocab clip). `anki_write.py` does not
  fill it yet — populate post-stage via AnkiConnect `updateNoteFields` on pipeline-authored
  notes only. A clip in the Audio field must NOT also appear as `[sound:]` in Back Extra
  (two play buttons — Parker-caught defect); Back Extra `[sound:]` is only for secondary
  clips (dialect variants). All media filenames LOWERCASE; corrected assets get a NEW
  versioned filename (see `scripts/media_audit.py`, R45/R47).
- **The pipeline fills only `Text` and `Back Extra`** (plus post-stage `Audio` as above). `Lecture Notes`, `Missed Questions`, `Additional Resources` are Parker's own study-time fields (his notes, missed exam questions, extra resources) — always leave them empty; never write into them.
- **`Card Feedback` (added 2026-07-18) is a HIDDEN, human-only field.** It is not referenced in any card template, so it never renders during review; Parker types card complaints into it via Anki's Edit button while studying, and `scripts/feedback_harvest.py` collects them for the batch feedback loop (see SKILL.md → "Processing card feedback (batch)"). The generator must NEVER write into it. `AnKing Basic` carries the same field (`Front`, `Back`, `Back Extra`, `Card Feedback`).
- The note type is per-source (`model` in the registry, defaulting to `AnKing Cloze`). If it is ever missing or renamed, find whatever cloze type his current cards use (`deck:all::EMT::*`) and update the registry default to match — not the script.

## Cloze syntax
```
{{c1::answer}}                 one blank -> one card
{{c1::answer::hint}}           same blank, hint shown on the front (slot-label only)
{{c1::A}} ... {{c2::B}}        DIFFERENT numbers -> TWO cards
{{c1::A}}, {{c1::B}}, {{c1::C}}  SAME number -> ONE card, all hide/reveal together
```
The number decides how many cards a note makes and which blanks share a card. See `cloze-mastery.md` for 2,391 worked examples of every pattern.

## Math (MathJax)
- Inline: `\( ... \)`   Display: `\[ ... \]`. Renders via Anki's built-in MathJax.
- Example: `Cardiac output is \(CO = HR \times SV\).`
- **One-time check:** the first MathJax card you make, glance at it in Anki to confirm it renders (storage is verified; visual render was never headlessly confirmable).

## Images (tables / figures / anatomy)
- **The book's own plates come from `scripts/build_figure_index.py`, not from rendering pages.** Each figure is already a discrete embedded raster at full publisher resolution; extracting it beats cropping a render by ~2× linear resolution and needs no crop bounds at all. See SKILL.md Stage 2.9. Attach the index's **`study_file`** (1400px, ~150 KB), not the native archive.
- For a mark whose fact lives in a table or figure and you just need to *read* it, `scripts/render_page.py --source <id> <page>` still gives you the page.
- When Parker **area-selected** the figure himself (extractor `kind: "image"`), crop exactly to his box: `scripts/render_page.py --source <id> --crop-from work/<source>/<label>_highlights.json`. His box IS the card — author from the crop rather than describing the figure in words.
- **`image_side` decides which face it lands on, and the default is `back`.** `anki_write.py` stores the file in Anki media and appends `<img src="...">` to **Back Extra**. A labelled plate on the FRONT of a cloze is an answer key — the skull figure labels *frontal / parietal / temporal / occipital*, which are the very answers of the cranium card. Set `"image_side": "front"` only when the picture IS the question (*identify this structure*), where it leaks nothing. Counter-intuitively, **higher answer-coverage is a stronger reason to put the image on the back.**
- Use this for: the hazmat placard diagram (text-impossible), vital-signs-by-age tables, anatomy figures.

## Back Extra vocabulary
Open every Back Extra line with one of: `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:` `Roster:` `Parts:` `Formal:`. (This matches the house style of the old deck and the AnKing Extra field.)

**`Parts:` and `Formal:` (added 2026-08-08) belong to the lexicon lane** (card-rules #28, recipes §4b). `Parts:` is a word-part breakdown (`dia- (through) + phor- (carry)`) — usable on any card whose term genuinely decomposes, typical on lexicon cards. `Formal:` quotes the source's own formal definition from the anchor evidence, and is licensed **on lexicon cards only**: there the plain authored answer is the taught form, so the formal register is new information, not a re-definition (the "never re-define the term" clause in card-rules #5 still governs ordinary definition cards).

**`Roster:` (added 2026-08-02) is required on every note born from a CHUNKED list** (card-rules #23): it carries the full set in order, with that note's own members in `<b>bold</b>`. When a 10-element list becomes four notes, the roster is what keeps the set from dissolving into four unrelated fragments — Parker asked for it directly ("seeing the part and the whole in each flash card"). It goes LAST in the Back Extra, after the teaching lines, since it is reference rather than instruction.

**Separate distinct components with a paragraph break `<br><br>`, not a single `<br>`** (Parker's preference, 2026-07-02) — each labeled line sits in its own block with white space around it so his eye can jump between parts. `anki_write.py` normalizes any run of `<br>` in Back Extra to exactly `<br><br>` at write time, so this is guaranteed even for a card drafted with single breaks. Example: `Distinguish: ...<br><br>Pitfall: ...`.

## HTML
- Allowed on newly generated cards: `<b>`, `<i>`, `<br>`, `<img>`. Nothing else (no `<u>`, no escaped entities). One note per object. Bold/italics are for *selective* emphasis only — the load-bearing word, not whole phrases (Parker's gold cards use italics for contrast; keep it sparing).
- **Rich pre-existing cards are a known exception.** Some cards already in Parker's deck legitimately carry richer HTML he added himself — embedded reference images (`<img>`), a formatted comparison `<table>`, `<div>`-wrapped lists — and the Ch5 medical-terminology cards carry `clinical-ex` `<div>` blocks plus `[sound:…]` TTS audio. Never strip the content itself (the image, the table, the audio). (The one exception: a dead `<a href="google.com/url?…">` tracking wrapper around a pasted image is unwrapped — see the live-deck bullet below — because the `<a>` is inert junk, not content.) When *verifying* existing cards (an audit/refinement pass, not fresh generation), run `python3 scripts/check_cards.py --audit <file>`: `--audit` skips the minimal-HTML gate (so rich cards pass structural verification) while keeping every meaningful check — cloze presence, leaks, husks, first-letter hints, numeric flags. The default (no flag) stays strict so newly generated cards are still held to `<b>/<i>/<br>/<img>`.
- **Auditing the LIVE deck (hand-edit drift).** Parker edits cards inside Anki on Mac and iPhone, and a mobile image paste can drag in an `<a href="google.com/url?…"><img></a>` wrapper — a dead Google-redirect tracking link around the image. **Keep the image; unwrap the dead anchor** (`<a><img></a>` → `<img>`): the image is the content Parker added (never strip it), but the `<a>` is inert junk and a disallowed tag. That is the one sanctioned edit to a pasted reference image — everything else he added (the image itself, `[sound:…]` audio, his own notes) stays untouched. The pre-staging file gate never sees hand-edits, so to sweep the deck as it actually exists, run `python3 scripts/check_cards.py --live <N|all>` — it pulls every card from Anki and runs the checks with the same relaxed HTML as `--audit` (diagnostic only; never stamps). This is how the two Star-of-Life / cyanide reference-image cards were caught and cleaned.

## Recording that a WARNING was cleared

`check_cards.py` warnings are routed to the judge, and several detectors are deliberately
generous (`husk_groups`, `row_label_tautology`, `step_recitation`) precisely so a human or
judge can clear them. **There is currently nowhere on the card to record that clearance** —
a verdict lives only in the run's report, so the next session re-litigates it or "fixes" a
card that was already adjudicated.

Until there is a field for it, put the clearance in the run's `REPORT.md` and in the
card's `verified_by`, naming the detector: `"husk_groups cleared: both blanks are
cold-solvable with the other hidden"`. Do not silence a detector to make a warning go away.

**`image_side` on an image-less card:** omit it. Chapter 7 does both, which is drift; the
key only means something when `image` is set.

## Card object (what the writer produces, what `anki_write.py` consumes)
```json
{
  "Text": "At the carina, the trachea divides into the right and left main stem {{c1::bronchi::airways}}.",
  "Back Extra": "Cue: Main stem bronchi branch into smaller airways inside the lungs.",
  "source": "emt",
  "segment": 1,
  "from_idx": [94, 104],
  "block": "H_nervous_system",
  "numeric": false,
  "verified_against": null,
  "verified_by": null,
  "needs_human_check": false,
  "visual_source": null,
  "image": null
}
```
`from_idx` (the marks this card was built from) is **required for new runs** — it is what
lets the gate verify Rule 1 and what lets any card in Anki be traced back to its source.
`needs_human_check` is **derived, never asserted** (`scripts/verify_report.py`). Full field
reference and the run store: `reference/provenance.md`.

**A lexicon card (the purple lane) adds two fields** — `"kind": "lexicon"` plus its
contract block, both HARD-checked by `check_cards.lexicon_check` (card-rules #28):
```json
{
  "Text": "<b>Diaphoresis</b> is {{c1::heavy, drenching sweating}}.",
  "Back Extra": "Ex: \"The patient was pale and <b>diaphoretic</b>…\"<br><br>Parts: dia- (through) + phor- (carry).",
  "kind": "lexicon",
  "lexicon": {
    "term": "diaphoresis", "term_key": "diaphor",
    "anchor": {"method": "in_source", "page": "612"}
  },
  "source": "emt", "segment": 12, "from_idx": [41]
}
```
`anchor.method` is `glossary` / `in_source` (must resolve in `work/<source>/lexicon_evidence.json`,
written by `lexicon.py --find` — R37) or `external` (must arrive with the derived
`needs_human_check` — R35). The cited marks must themselves be `kind: lexicon` (R36).

## Write target & tags

**All of this comes from the source registry** (`reference/sources.json`) — it is per-source,
not global. See `reference/sources.md` for the field reference.

- **Deck:** the source's `deck` template, which for a book is its `Book Highlights`. Every
  card the pipeline generates lands there — one deck per segment, no staging sibling.
  `anki_write.py` derives it per card from the card's `source` + `segment` fields and
  auto-creates the substructure. Nothing the pipeline writes is "final": Parker judges each
  card when it comes up in review and edits or deletes it in place. (The old `claude review`
  staging deck and its promotion step were removed 2026-08-24 — see `reference/sources.md`.)
- **Tags:** the source's `tags` templates (EMT: `ch<N>` only). Parker had the old
  `claude_generated` marker removed from every card on 2026-07-02 — he found it noise, and
  the deck structure identifies each batch. Add nothing beyond what the registry declares.
- **Deck presets:** `anki_write.py` copies the source root's preset onto any subdeck it
  creates, so **bury-siblings stays on** and the two halves of a two-way definition space
  across days.
- **Sync:** the pipeline never auto-syncs to AnkiWeb. Parker syncs when he's ready (his cards
  also live on his phone, so writes propagate on his next sync).

Example — EMT, whose deck names predate the registry and are **case-exact** (`Chapter <N>`
and `Book Highlights` Title Case; 899 notes live under them, so don't restyle):

```
deck: all::EMT::Chapter 6::Book Highlights
tags: ch6
```

## Operational guards (handled by `anki_write.py`)
- Anki must be **running** (AnkiConnect lives inside the app); the script fails loud if it's closed.
- Each note is written **individually** (not as a batch) and pre-flighted with `canAddNotesWithErrorDetail`, so one bad card can never roll back a whole run.
- Every `Text` is validated to contain cloze markup before sending.
