# The source registry

`reference/sources.json` is the list of everything Claude can make cards from, and where
each one's cards go. It is the single file that made this pipeline universal: everything
that used to be hard-coded to one textbook now lives here, per source.

Read it with `python3 scripts/sources.py list | show <id> | segments <id> | deck <id> [n]`.
Write it with `python3 scripts/add_source.py` (never by hand, unless fixing a typo).

---

## Fields

| Field | Required | What it does |
|---|---|---|
| `label` | yes | Human name, shown in listings and at hand-off. |
| `attachment_key` | yes | The Zotero **item key** of the attachment (e.g. `Z98PW7AT`). Stable and unambiguous — this is why resolution is safe. |
| `path_match` | no | Fallback filename substring if the key ever fails. |
| `kind` | no | `textbook` · `lecture` · `article` · `reference`. Descriptive; helps a future session pick sensible defaults. |
| `colors` | no | The hex colors that mean "card me". Defaults to the registry's yellows. Override when a book uses a different scheme. |
| `lexicon_colors` | no | The colors that mean "define this word" — the purple lane (card-rules #28). Defaults to `#a28ae5` (Zotero purple) + `#c885da` (external-annotator purple). Override to `[]` to turn the lane off for a source, or when a book's previous owner used purple for something else. |
| `glossary_pages` | no | `[start, end]` PHYSICAL pages of the book's own glossary. Lets `lexicon.py --find` anchor authored definitions at the strongest tier. Omit for sources without one (lectures, papers). |
| `segments` | no | Path to a segment map (`reference/maps/<id>.json`). Omit for a flat source addressed whole. |
| `segment_noun` | no | `Chapter` · `Unit` · `Lesson` · `Section`. Used in deck names and prose. |
| `deck_root` | yes | The Anki deck this source lives under. |
| `deck` | no | Template for the deck this source's cards go to — the only one. Defaults to `{root}::Book Highlights`. |
| `tags` | no | List of tag templates applied to every card. |
| `profile` | no | Which `reference/profiles/<name>.md` governs emphasis. Defaults to `default`. |
| `model` | no | Anki note type. Defaults to `AnKing Cloze`. |
| `notes` | no | Anything a future session should know about this source. |

### Template variables
`deck` and each `tags` entry expand:

- `{root}` → `deck_root`
- `{segment}` → the segment number (empty for a flat source)
- `{segment_pad}` → the segment number **zero-padded to two digits** (`5` → `05`; a
  non-numeric segment like `3b` passes through). Use this in `deck`, never in `tags`.
  Anki sorts the deck list as TEXT, so an unpadded tree reorders itself to
  `Chapter 1, Chapter 10, Chapter 2, ...` the moment a tenth segment lands — EMT hit
  this on 2026-08-29. Padding is opt-in per source because switching the template
  re-routes writes: a source whose live decks are unpadded would start filling a NEW
  padded deck beside the old one and split the chapter in two. **Only pad a source's
  template in the same change that renames its live decks.**
- `{segment_noun}` → e.g. `Chapter`
- `{segment_name}` → the segment's `name` from the map (empty for a flat source). Use when
  Parker's live decks carry the chapter title, e.g.
  `{root}::Chapter {segment} - {segment_name}::Book Highlights` →
  `…::Chapter 9 - DNA and the Molecular Structure of Chromosomes::Book Highlights`. The map
  name must match the live deck name EXACTLY (dash style, spacing) or anki_write creates a
  sibling deck.
- `{id}` → the source id

---

## One deck per segment

**The pipeline writes a source's cards into its `deck` and stops there.** For a book that
is its `Book Highlights`; every card for that segment lands in it, and that is the deck
Parker studies out of.

There used to be two. Each source had a `claude review` staging deck that the pipeline
wrote to and a sibling the registry called `promote`, and Parker was meant to review
staging and promote the keepers across. **Removed 2026-08-24, because he never did it** —
he judges each card when it comes up in review and edits or deletes it right there, which
is the same first-pass filter promotion was invented to provide, only actually performed.
Eight EMT chapters, an Arabic unit and a genetics chapter later, all 2,440 cards were
still in staging and every `Book Highlights` deck was empty. The split bought nothing and
cost a doubled deck tree. Those cards were moved into `Book Highlights` and the staging
decks deleted.

What guards the collection was never the second deck, and none of it changed:
`check_cards.py` still refuses to let an unstamped or failing file reach Anki, the live
sweep (card-rules #32) still audits notes already in his rotation, and retirement still
handles superseded ones.

```
EMT (segmented textbook, names are case-exact; zero-padded since 2026-08-29):
  deck:  all::EMT::Chapter 06::Book Highlights
  audit: all::EMT::Chapter 06
  tags:  ch6          <- tags stay UNPADDED; 2,440 live cards carry ch1..ch10

A lecture (flat):
  deck:  all::LIBERTY::Genetics::Isaacs 17 Gene Regulation::Book Highlights
  audit: all::LIBERTY::Genetics::Isaacs 17 Gene Regulation
```

`audit` is not a registry field — `sources.audit_deck()` derives it as the container the
write target sits in, and `check_cards.py --live` and `sync_report.py` sweep it so a card
Parker has moved is still audited.

`anki_write.py` also copies the `deck_root`'s deck preset onto any subdeck it creates, so
**bury-siblings stays on** — without it, the two halves of a two-way definition can appear
the same day and inflate his sense of mastery.

---

## Segment maps

`reference/maps/<id>.json`:

```json
{
 "source": "emt",
 "noun": "Chapter",
 "note": "Page numbers are PHYSICAL PDF pages.",
 "segments": [{"n": 1, "name": "EMS Systems", "start": 67, "end": 129}]
}
```

**`start`/`end` are PHYSICAL PDF pages, not printed page numbers.** In the EMT book they
happen to be identical (no front-matter offset); most books have an offset, so measure it
once and pass `--offset` to `--write-map`.

Build a map by reading the book's **printed** table of contents:

```
python3 scripts/add_source.py --toc-pages 7-11 --key <KEY>     # dump the TOC text
# ...read it, then:
echo '[{"n":1,"name":"...","start":12,"end":40}]' | \
  python3 scripts/add_source.py --write-map <id> --noun Chapter --offset 6
```

This deliberately reads the *printed* contents rather than an embedded PDF outline: most of
Parker's textbooks are scanned or exported without a usable outline, but every one of them
prints a contents page. `--write-map` warns on overlapping ranges and refuses inverted ones.

---

## Gotchas worth knowing

- **Zotero's `contentType` lies.** `Isaacs Chapter 16.pptx` is registered as
  `application/pdf` but is a real PowerPoint. The extractor checks magic bytes and stops
  with the fix (export a true PDF, re-attach, re-mark, re-point the key). Don't work around it.
- **Near-duplicate library items.** Several books exist in multiple copies (four `Alif Baa`
  matches, three `sick and injured` files). Always confirm which key is the one Parker
  actually marked up — `add_source.py --search` prints each candidate's marks.
- **Colors are not uniform across his library.** The EMT book is yellow-only; the organic
  chemistry text carries ~1,050 `#facd5a` plus blue and pink from a different annotator.
  Set `colors` per source rather than assuming.
- **A source with zero marks is still worth registering** — it just means he hasn't read it
  yet, or it uses colors you haven't declared.
- **Purple is a LANE, not emphasis.** A book whose previous owner marked in purple (the way
  the orgo text carries a stranger's #facd5a) would flood the lexicon lane with someone
  else's marks — check `add_source.py --search`'s per-color counts when registering, and
  override `lexicon_colors` (or set it `[]`) for that source.
