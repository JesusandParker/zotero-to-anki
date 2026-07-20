# Anki Note Format & Write Targets

The exact shape every card must take, and where it goes. Verified live against Parker's collection on 2026-07-01.

## Note type
- **Model:** `AnKing Cloze` (a Cloze type). This replaced `01_Cloze - Parkers Note Type` on 2026-06-29, when Parker restyled his whole collection to the AnKing look and the old type was deleted; all existing EMT cards were migrated.
- **Fields, in order:** `Text`, `Back Extra`, `Lecture Notes`, `Missed Questions`, `Additional Resources`, `Card Feedback`.
- **The pipeline fills only `Text` and `Back Extra`.** `Lecture Notes`, `Missed Questions`, `Additional Resources` are Parker's own study-time fields (his notes, missed exam questions, extra resources) — always leave them empty; never write into them.
- **`Card Feedback` (added 2026-07-18) is a HIDDEN, human-only field.** It is not referenced in any card template, so it never renders during review; Parker types card complaints into it via Anki's Edit button while studying, and `scripts/feedback_harvest.py` collects them for the batch feedback loop (see SKILL.md → "Processing card feedback (batch)"). The generator must NEVER write into it. `AnKing Basic` carries the same field (`Front`, `Back`, `Back Extra`, `Card Feedback`).
- If the model is ever missing/renamed, find whatever cloze type his current EMT cards use (`deck:all::EMT::*`) and update `scripts/anki_write.py` MODEL to match.

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
- For a highlight whose fact lives in a table or figure, run `scripts/render_page.py <page>` to get a PNG, then pass its path as the card's `image` field. `anki_write.py` stores it in Anki media and appends `<img src="...">` to the Text.
- Use this for: the hazmat placard diagram (text-impossible), vital-signs-by-age tables, anatomy figures.

## Back Extra vocabulary
Open every Back Extra line with one of: `Meaning:` `Why:` `Mechanism:` `Distinguish:` `Pitfall:` `Ex:` `Cue:` `Pathway:` `Mnemonic:`. (This matches the house style of the old deck and the AnKing Extra field.)

**Separate distinct components with a paragraph break `<br><br>`, not a single `<br>`** (Parker's preference, 2026-07-02) — each labeled line sits in its own block with white space around it so his eye can jump between parts. `anki_write.py` normalizes any run of `<br>` in Back Extra to exactly `<br><br>` at write time, so this is guaranteed even for a card drafted with single breaks. Example: `Distinguish: ...<br><br>Pitfall: ...`.

## HTML
- Allowed on newly generated cards: `<b>`, `<i>`, `<br>`, `<img>`. Nothing else (no `<u>`, no escaped entities). One note per object. Bold/italics are for *selective* emphasis only — the load-bearing word, not whole phrases (Parker's gold cards use italics for contrast; keep it sparing).
- **Rich pre-existing cards are a known exception.** Some cards already in Parker's deck legitimately carry richer HTML he added himself — embedded reference images/links (`<a><img></a>`), a formatted comparison `<table>`, `<div>`-wrapped lists — and the Ch5 medical-terminology cards carry `clinical-ex` `<div>` blocks plus `[sound:…]` TTS audio. Never strip these. When *verifying* existing cards (an audit/refinement pass, not fresh generation), run `python3 scripts/check_cards.py --audit <file>`: `--audit` skips the minimal-HTML gate (so rich cards pass structural verification) while keeping every meaningful check — cloze presence, leaks, husks, first-letter hints, numeric flags. The default (no flag) stays strict so newly generated cards are still held to `<b>/<i>/<br>/<img>`.

## Card object (what the writer produces, what `anki_write.py` consumes)
```json
{
  "Text": "At the carina, the trachea divides into the right and left main stem {{c1::bronchi::airways}}.",
  "Back Extra": "Cue: Main stem bronchi branch into smaller airways inside the lungs.",
  "chapter": 1,
  "needs_human_check": false,
  "image": null
}
```

## Write target & tags
- **Staging deck (per chapter):** `all::EMT::Chapter <N>::claude review`. Every card the pipeline generates for a chapter lands in THAT chapter's `claude review` subdeck. `anki_write.py` derives the deck per card from its `chapter` field and auto-creates the substructure. Nothing the pipeline writes is "final."
  - **Exact deck names (case matters — match Parker's):** `Chapter <N>` and `Book Highlights` are Title Case; `claude review` is lowercase.
- **Promotion (Parker's manual first-pass gate):** Parker reviews the `claude review` deck and PROMOTES keepers into the sibling `all::EMT::Chapter <N>::Book Highlights` deck himself. The pipeline NEVER writes to Book Highlights — it only creates the empty deck so his promotion target exists.
- **Tags (auto-applied):** `ch<N>` only. Parker had the old `claude_generated` marker removed from every card and from the skill on 2026-07-02 (he found it noise); the per-chapter deck structure now identifies each batch. Keep the chapter tag; add nothing else.
- **Sync:** the pipeline never auto-syncs to AnkiWeb. Parker syncs when he's ready (his cards also live on his phone, so writes propagate on his next sync).

## Operational guards (handled by `anki_write.py`)
- Anki must be **running** (AnkiConnect lives inside the app); the script fails loud if it's closed.
- Each note is written **individually** (not as a batch) and pre-flighted with `canAddNotesWithErrorDetail`, so one bad card can never roll back a whole run.
- Every `Text` is validated to contain cloze markup before sending.
