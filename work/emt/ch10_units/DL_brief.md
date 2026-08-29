# DL — The PURPLE lexicon lane (21 marks → authored plain definitions)

Indices: 58, 64, 77, 80, 81, 93, 95, 102, 103, 108, 110, 131, 158, 159, 162, 181, 182,
183, 184, 185, 186

Read `reference/card-rules.md` #28 and `reference/card-recipes.md` §4b FIRST — this lane
has its own template, and editor check #30 hunts blended glosses by name.

Evidence file (ALREADY BUILT — do not re-run --find): `work/emt/lexicon_evidence.json`.
Anchors found (term → method):
- glossary: sclera p4122, diaphoretic p4042, crepitus p4036, emphysema p4051 (WRONG
  SENSE — see below), pertinent negatives p4103, focused assessment p4058, auscultate
  p4014, subcutaneous emphysema p4132, paradoxical motion p4099, flail→'flail chest'
  p4057 (family form, sense OK), pneumothorax p4106, guarding p4064, ecchymoses→
  'ecchymosis' p4048 (plural→singular, sense OK), diaphoresis→'diaphoretic' p4042
  (family form, sense OK), Auscultation→'auscultate' p4014 (family form, sense OK)
- in_source: pallor p2386, fistula p1975
- external (needs Parker's eyes, gate enforces): cookbook medicine, mastectomy
- **distention: the finder matched headword 'distal' — a DIFFERENT WORD. Reject that
  anchor.** Search the glossary yourself for a real 'distention' entry (grep the
  evidence file / use python to search `work/emt/_fulltext` if present, or render a
  glossary page); if the book truly never defines it → method `external` and author
  the definition yourself (plain: "swelling outward / being stretched or inflated").
  Document what you did.

**Sense decisions already made (follow them, verify, and record in notes):**
1. `emphysema` (idx 81, p975) — the mark sits INSIDE the phrase "crepitus, subcutaneous
   emphysema" in the chest-exam sentence. The glossary's lung-disease entry is the WRONG
   sense for this encounter. MERGE idx 81 with idx 182 (`subcutaneous emphysema`, p1064)
   into ONE card for subcutaneous emphysema (anchor: glossary p4132), citing BOTH marks
   in from_idx, with `Distinguish:` against the lung disease emphysema (which the bare
   word usually means — that contrast is exactly what saves him on exams).
2. `crepitus` ×2 (idx 80 p975, idx 108 p1006) — same sense both times (grating of broken
   bone ends; AAOS glossary: "grating or grinding sensation/sound caused by fractured
   bone ends or joints rubbing together"). ONE card, from_idx [80,108]. The repeat is
   DATA — flag in notes for hand-off ("marked twice while reading = the word didn't
   stick on first meeting").
3. `diaphoretic` (64) + `diaphoresis` (103) — same family, same sense (profuse
   sweating). ONE card. Pick the noun (diaphoresis) as headword, mention the adjective
   form in the card or Back Extra (`Parts:`/`Ex:` can carry "diaphoretic"), from_idx
   [64,103].
4. `auscultate` (131) + `Auscultation` (162) — same root/sense (listening with a
   stethoscope; 162's context is the BP-by-auscultation method). ONE card, verb or noun
   headword as reads best, from_idx [131,162], `Ex:` can nod to BP measurement.
So: 21 marks → 17 candidate cards (before cross-lane fold-ins at consolidation).

**Cross-lane fold-in candidates (do NOT draft a lexicon card for these without checking —
note them for the consolidator instead):**
- `sclera` (58): yellow marks 56+57 (unit D5) card "sclera = normally white portion of
  the eye…" from the SAME page. If D5's definition card tests term↔meaning, the lexicon
  card FOLDS INTO it (keep yellow card, add Ex:/Parts: lines, cite both marks). Draft
  your sclera card anyway but mark it `"fold_candidate": "D5 sclera"` in the JSON.
- `guarding` (186): check idx 187's abdomen terms (D13) — 187 does NOT define guarding
  (firm/soft/tender/distended only), so a standalone card is right; but note adjacency.
- `focused assessment` (110): idx 73's context (D6) says the rapid exam "is not a focused
  assessment" — your card should Distinguish rapid exam vs focused assessment using the
  glossary anchor.
- `pertinent negatives` (93): the yellow mark 92/94 neighborhood (OPQRST/SAMPLE, D7);
  standalone lexicon card is right (the book glosses it at p988 — glossary anchor exists).

**Template reminders (§4b):** term VISIBLE and bold, definition hidden, one-way
word→meaning, answer ≤ ~8 plain words with the DISCRIMINATOR, `Ex:` REQUIRED (the
sentence he met the word in, term bolded — pull from the mark's own `context`),
`Parts:` when the word genuinely decomposes (dia-phor-esis, aus-cultare, ec-chym-osis,
pneumo-thorax…), `Distinguish:` when a confusable exists (crepitus vs subcutaneous
emphysema — BOTH are in this batch, cross-link them!; pallor vs cyanosis; hypoxia not
here), `Formal:` quote the glossary wording when it reads differently from your plain
answer. Domain-frame the sense-ambiguous ones (`In EMS documentation, a <b>pertinent
negative</b> is…`).

**Card JSON extras for this lane (see note-format.md):** `"kind": "lexicon"`,
`"lexicon": {"term": "...", "term_key": "<from the highlights item>", "anchor":
{"method": "glossary|in_source|external", "page": "<evidence page>"}}`. from_idx cites
the purple mark(s). For `external` cards leave verification fields null (the gate + report
route them to Parker). Block name: `LEX_<term_key>`.

Output: `DL_cards.json` + `DL_notes.md` (sense decisions, anchor verifications, the
distention hunt, fold candidates, repeat-mark flags).
