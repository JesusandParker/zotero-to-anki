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
| `segments` | no | Path to a segment map (`reference/maps/<id>.json`). Omit for a flat source addressed whole. |
| `segment_noun` | no | `Chapter` · `Unit` · `Lesson` · `Section`. Used in deck names and prose. |
| `deck_root` | yes | The Anki deck this source lives under. |
| `staging` | no | Template for the deck the pipeline WRITES to. |
| `promote` | no | Template for the deck Parker promotes keepers INTO. |
| `tags` | no | List of tag templates applied to every card. |
| `profile` | no | Which `reference/profiles/<name>.md` governs emphasis. Defaults to `default`. |
| `model` | no | Anki note type. Defaults to `AnKing Cloze`. |
| `notes` | no | Anything a future session should know about this source. |

### Template variables
`staging`, `promote`, and each `tags` entry expand:

- `{root}` → `deck_root`
- `{segment}` → the segment number (empty for a flat source)
- `{segment_noun}` → e.g. `Chapter`
- `{id}` → the source id

---

## The two-deck promotion gate

**Every source keeps it.** The pipeline writes ONLY to `staging`; Parker reviews there and
promotes keepers into `promote` himself. The pipeline never writes to the promotion deck —
it only creates it so his target exists.

The *names* are per-source, which is the point: a textbook chapter reads naturally as
`Book Highlights`, but a lecture doesn't, so it gets `Keepers` (or whatever fits).

```
EMT (segmented textbook, names predate the registry and are case-exact):
  staging: all::EMT::Chapter 6::claude review
  promote: all::EMT::Chapter 6::Book Highlights

A lecture (flat):
  staging: all::LIBERTY::Genetics::Isaacs 17 Gene Regulation::claude review
  promote: all::LIBERTY::Genetics::Isaacs 17 Gene Regulation::Keepers
```

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
