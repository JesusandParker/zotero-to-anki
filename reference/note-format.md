# Anki Note Format & Write Targets

The exact shape every card must take, and where it goes. Verified live against Parker's collection on 2026-07-01.

## Note type
- **Model:** `AnKing Cloze` (a Cloze type). This replaced `01_Cloze - Parkers Note Type` on 2026-06-29, when Parker restyled his whole collection to the AnKing look and the old type was deleted; all existing EMT cards were migrated.
- **Fields, in order:** `Text`, `Back Extra`, `Lecture Notes`, `Missed Questions`, `Additional Resources`.
- **The pipeline fills only `Text` and `Back Extra`.** The last three are Parker's own study-time fields (his notes, missed exam questions, extra resources) — always leave them empty; never write into them.
- If the model is ever missing/renamed, find whatever cloze type his current `tag:claude_generated` cards use and update `scripts/anki_write.py` MODEL to match.

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

## HTML
- Allowed: `<b>`, `<i>`, `<br>`, `<img>`. Nothing else (no `<u>`, no escaped entities). One note per object. Bold/italics are for *selective* emphasis only — the load-bearing word, not whole phrases (Parker's gold cards use italics for contrast; keep it sparing).

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
- **Staging deck:** `EMT::_Review`. Everything the pipeline generates lands here. Parker reviews/edits in Anki and moves keepers into his real chapter decks himself. Nothing the pipeline writes is "final."
- **Tags (auto-applied):** `claude_generated` + `ch<N>`. This is a reversibility marker, NOT the organizational tagging scheme Parker deferred — it just lets a batch be found and undone in one click. (Full tag taxonomy is a separate, later decision.)
- **Sync:** the pipeline never auto-syncs to AnkiWeb. Parker syncs when he's ready (his cards also live on his phone, so writes propagate on his next sync).

## Operational guards (handled by `anki_write.py`)
- Anki must be **running** (AnkiConnect lives inside the app); the script fails loud if it's closed.
- Each note is written **individually** (not as a batch) and pre-flighted with `canAddNotesWithErrorDetail`, so one bad card can never roll back a whole run.
- Every `Text` is validated to contain cloze markup before sending.
