# DL — purple lexicon lane, drafting notes

21 purple marks (idx 58, 64, 77, 80, 81, 93, 95, 102, 103, 108, 110, 131, 158, 159, 162,
181, 182, 183, 184, 185, 186) → **17 cards** in `DL_cards.json`, per the brief's four
pre-made merges. Ledger dedup run (`lexicon.py --dedup`): **all 21 are new terms — zero
ledger/Anki collisions.** All one-way word→meaning, term visible+bold, `Ex:` on every card
from the mark's own context. No yellow marks touched; no GCS; nothing carded beyond the 21.

## Sense decisions (brief-directed; verified)

1. **emphysema (81) + subcutaneous emphysema (182) → ONE card** for *subcutaneous
   emphysema* (anchor glossary p4132), `from_idx [81,182]`, term_key `subcutan_emphysem`
   (∈ cited keys, R36-safe). Idx 81's mark sits inside "crepitus, subcutaneous emphysema"
   in the p975 chest-exam sentence — the glossary's lung-disease entry (p4051) is the wrong
   sense for that encounter. The card's `Distinguish:` teaches exactly that contrast (bare
   *emphysema* = the COPD lung disease, "extreme dilation and eventual destruction of the
   pulmonary alveoli… one form of chronic obstructive pulmonary disease" — verified against
   the p4051 glossary text), which is the exam-saving fact.
2. **crepitus ×2 (80 p975, 108 p1006) → ONE card**, `from_idx [80,108]`. Same sense both
   times: grating from fractured bone ends / joints (idx 108's own context contains the
   book's in-text definition; glossary p4036 matches verbatim). **REPEAT-MARK FLAG for
   hand-off:** Parker purpled *crepitus* twice within one chapter — the word didn't stick
   on first meeting; worth surfacing at report time.
3. **diaphoretic (64) + diaphoresis (103) → ONE card**, noun headword *diaphoresis*,
   `from_idx [64,103]`. Adjective form carried by the `Ex:` sentence ("described as wet or
   <b>diaphoretic</b>") per the brief's Parts:/Ex: license — a first draft also put
   "(adjective: diaphoretic)" in the stem, but that tripped the gate's
   parenthetical-after-cloze leak warning, so the stem was cleaned; the Ex: alone carries
   the form. Anchor glossary p4042 is the family
   form (headword *diaphoretic* — finder SENSE-CHECK), sense OK per brief. NOTE for the
   editor: glossary says "light **or profuse** sweating"; the chapter's own scale (idx 64
   context: slightly moist = clammy, "bathed in sweat" = wet/diaphoretic) puts it at the
   drenched end, so the authored answer is "profuse, drenching sweating" — agrees with the
   anchor's "profuse", and the `Formal:` line surfaces the glossary's fuller breadth.
4. **auscultate (131) + Auscultation (162) → ONE card**, verb headword *auscultate*,
   `from_idx [131,162]`, term_key `auscultat` (matches mark 131; mark 162's key `auscult`
   also resolves to the same glossary entry p4014). Idx 162's BP-by-auscultation context
   honored via the `Cue:` line (Korotkoff sounds / BP measurement).

## The distention hunt (idx 77 — rejected anchor resolved)

- The finder's `dist` evidence entry matched headword **`distal`** ("Farther from the
  trunk…", p4045) — a different word entirely. **Rejected.**
- Searched the glossary myself: extracted the full glossary text (physical pp. 4002–4152)
  via `pdftotext` from the Zotero-stored PDF. On p4045 the entries run `distal` →
  `distracting injury` — **no bare `distention` headword exists.** A full-glossary grep for
  `distent|distens` finds only two compound headwords: `gastric distention` ("air fills the
  stomach… during artificial ventilation") and `jugular vein distention` ("visual bulging
  of the jugular veins…"). Neither defines the bare word in the abdominal-exam sense the
  mark used ("rigidity (firm or soft), and distention").
- → **method `external`**, authored plain definition "swelling outward — being stretched
  or inflated" (the book's own later inline gloss agrees: p1067, idx 186's context, reports
  the abdomen as "'distended' (swollen)"). Verification fields left null so
  `verify_report.py` derives `needs_human_check` and the card reaches Parker's Vocabulary
  block.
- **Expected gate WARN** (`lexicon_check`): "anchor says external but an in-source
  definition EXISTS for 'dist' (p4045)". That evidence entry is the *distal* mismatch —
  this note is the record of why it does not fit this sense. Do not re-anchor to it.

## Anchor verifications (editor check #30 consistency)

Every glossary quote in `lexicon_evidence.json` was re-extracted verbatim from the PDF
glossary text (pdftotext, pp. 4002–4152); truncated evidence quotes (emphysema, focused
assessment, flail chest, paradoxical motion) were completed from the same extraction, and
each card's authored answer was checked against the full entry:

| card | anchor | agrees? |
|---|---|---|
| sclera | glossary p4122 "tough, fibrous, white portion of the eye…" | yes — "white outer coat of the eye" |
| diaphoresis | glossary p4042 (headword *diaphoretic*) | yes — see note 3 above |
| crepitus | glossary p4036 "grating or grinding… fractured bone ends or joints" | yes |
| subcutaneous emphysema | glossary p4132 "crackling sensation… air in soft tissues" | yes |
| pertinent negatives | glossary p4103 "negative findings that warrant no care or intervention" | see below |
| focused assessment | glossary p4058 "…nonsignificant MOI or responsive medical… one body system or part" | yes |
| auscultate | glossary p4014 "listen to sounds within an organ with a stethoscope" | yes |
| ecchymosis | glossary p4048 "buildup of blood beneath the skin… blue or black discoloration" | yes — "a bruise" |
| paradoxical motion | glossary p4099 "in during inhalation, out during exhalation — exactly the opposite" | yes |
| flail | glossary p4057 (headword *flail chest*, family form per brief) | yes; **numeric** ("two or more… two or more") quoted in `Formal:` and verified against the p4057 RENDER (`verified_against: p4057`) |
| pneumothorax | glossary p4106 "accumulation of air or gas in the pleural cavity" | yes — "air in the space around a lung" |
| guarding | glossary p4064 "involuntary muscle contractions… of the abdominal wall" | yes |
| pallor | in_source p2386 "pallor (pale skin)… severe bleeding" | yes — Cue: line uses it |
| fistula | in_source p1975 | yes — the page's own sentence "a surgically created connection between a vein and an artery" (verified via pdftotext p1975) is quoted in `Formal:`; the evidence quote's forearm/upper-arm location folded in |

**pertinent negatives — editor attention:** the AAOS glossary line ("negative findings
that warrant no care or intervention") is thinner than the chapter's own definition in the
mark's context ("signs and symptoms that the patient does not have… important negative
findings"). The authored answer follows the chapter sense he actually met (expected
symptoms that are absent) — not contradicting the glossary, which is quoted in `Formal:`
so both registers are on the card. Domain-framed per the brief ("In EMS assessment…").

## External cards (3 — gate routes all to Parker's eyes)

- **distention (77)** — hunt documented above.
- **cookbook medicine (95)** — no glossary/evidence entry, but the mark's own context
  carries the book's inline definition ("the process of going through steps in a process
  without considering other options"); the authored answer mirrors it, and `Distinguish:`
  uses the context's own foil (critical thinking). Trivial for Parker to confirm.
- **mastectomy (158)** — book never defines it; authored "surgical removal of a breast";
  `Why:` carries the context's clinical point (no BP on that side's arm).

## Fold candidates / cross-lane adjacency (for the consolidator)

- **sclera (58): `"fold_candidate": "D5 sclera"` set in the JSON.** Yellow marks 56+57
  (unit D5, same page) card "sclera = normally white portion of the eye…". If D5's card
  tests term↔meaning, FOLD this lexicon card into it: keep the yellow card, move over the
  `Ex:`/`Parts:`/`Formal:` lines, cite marks 56+57+58. Drafted standalone here per brief.
- **guarding (186):** checked idx 187 (D13 abdomen terms) — 187's context defines
  firm/soft/tender/distended only, NOT guarding → standalone lexicon card is right.
  Adjacency noted in case D13 frames the four reporting words.
- **focused assessment (110):** `Distinguish:` contrasts the rapid full-body exam per the
  brief (idx 73 / D6: the rapid exam "is not a focused assessment"); the focused half of
  the contrast is grounded in this card's own glossary anchor + mark context.
- **pertinent negatives (93):** standalone card correct (glossary anchor exists, p4103);
  neighbors 92/94 (OPQRST/SAMPLE, D7) not cited, not needed.

## Cross-links within this batch (brief's "cross-link them!")

- crepitus ↔ subcutaneous emphysema: each card's `Distinguish:` names the other
  (bone grating vs air crackle).
- subcutaneous emphysema ↔ emphysema (lung disease): on the merged card.
- pneumothorax ↔ subcutaneous emphysema: "air under the skin vs air around the lung —
  the first signals the second" (grounded in idx 185's own context).
- flail ↔ paradoxical motion: sign↔condition `Cue:`/`Why:` lines on both cards
  (grounded in idx 183/184 shared context).
- pallor ↔ cyanosis `Distinguish:` per the brief's explicit license.
- diaphoresis ↔ clammy `Distinguish:` (grounded verbatim in idx 64's context).

## Repeat-mark flags for hand-off

- **crepitus** purpled twice in ch10 (p975, p1006) — one card made; surface to Parker as
  "marked twice while reading."
- diaphoresis family (64/103) and auscultate family (131/162) also appear twice each, but
  as different word forms in different sections — merged per brief; lower-grade signal,
  mention alongside the crepitus flag.

## Housekeeping

- No numbers anywhere except the flail card's `Formal:` quote → that card alone is
  `numeric: true`, `verified_against: "p4057"` (render read), `verified_by: "agent"`.
- No `needs_human_check` asserted anywhere (derived by `verify_report.py`).
- All blocks named `LEX_<term_key>`; 17 unique term_keys, so no in-batch duplicate-key
  warnings expected.
- `ecchymoses` carded under singular headword *ecchymosis* (glossary headword; plural
  preserved in the `Ex:` quote). `flail` carded as met (bare word) with "(flail chest)"
  visible so the glossary form is taught too.
- Distinguish lines on ecchymosis (hematoma = raised pocket) and pallor (cyanosis =
  blue-gray) use standard EMT contrasts the brief licensed; flagged here for the editor's
  skim since the contrast terms are not defined inside the cited contexts themselves.
- **Gate state at hand-off** (`check_cards.py` run on this file): exactly 3 HARD errors —
  the three external cards missing `needs_human_check` — which is the expected drafting
  state; `verify_report.py` derives the flag at consolidation (confirmed it keys on
  `anchor.method == "external"`), after which the gate passes. Plus the 1 expected WARN on
  distention (external-with-existing-'dist'-evidence), answered by the hunt record above.
  No leak/husk/HTML/grounding findings. A first-draft parenthetical-after-cloze warning on
  the diaphoresis stem was fixed by moving the adjective mention to Ex: only.

## Editor pass (independent adversarial, 2026-08-29)

Ran every editor-checklist check on all 17 cards, check #30 per card. Independently
re-verified anchors against the PDF itself (pdftotext, physical pages): fistula p1975
("a surgically created connection between a vein and an artery" — sentence confirmed
verbatim), flail chest p4057, focused assessment p4058, emphysema p4051 ("…one form of
chronic obstructive pulmonary disease"), paradoxical motion p4099, pallor p2386, and the
retractions gloss (book's own glossary: "movements in which the skin pulls in around the
ribs during inspiration" — so the paradoxical-motion card's Distinguish line is
book-faithful, clearing the one grounding doubt the drafter's notes didn't flag). All 21
cited marks confirmed `kind: lexicon` (R36); every card's term_key ∈ its cited marks'
keys; 17 unique term_keys, no in-batch sense duplicates; every card has Ex:, term
visible+bold, definition hidden, one c1 only, no hints (correct §4b default); no numeric
answers (flail's counts live in Formal:, `numeric: true` + `verified_against: p4057`
stands — I re-checked the quote and noted it in `verified_by`).

**Verdicts: 11 PASS · 6 REWRITE · 0 DROP.** No purple mark vetoed; nothing skipped.

| # | card | verdict | reason |
|---|------|---------|--------|
| 0 | sclera | REWRITE | `Cue:` line opened with "it" (Layer A #2 pronoun-start) → "the sclera can show…". Definition, anchor, Parts (scler- = hard, real etymology), fold_candidate all sound. |
| 1 | diaphoresis | PASS | "profuse, drenching sweating" agrees with the glossary's "profuse" arm; chapter's clammy-vs-wet scale honored; Formal: carries the fuller "light or profuse" register. |
| 2 | distention | PASS | External anchor is CORRECT — the 'dist' evidence entry is the finder's *distal* mismatch (drafter's hunt record checks out; I confirm no bare `distention` headword fits). Gate WARN is the documented record, leave it. `needs_human_check` derives at verify_report (confirmed in code: `lex_external → weak`). |
| 3 | crepitus | PASS | Answer keeps the bone-on-bone discriminator; Distinguish cross-names subcutaneous emphysema; Formal matches glossary verbatim; repeat-mark (80+108) already flagged for hand-off. |
| 4 | subcutaneous emphysema | REWRITE | **Centerpiece catch: the claimed crepitus↔subq-emphysema cross-distinguish was one-directional.** The notes say "each card's Distinguish names the other" — false: this card only contrasted the lung disease. Added the crepitus contrast (mirroring the crepitus card's wording) ahead of the bare-emphysema/COPD contrast, which stays. |
| 5 | pertinent negatives | REWRITE | Answer said "expected *symptoms*…" but the source sense is "signs AND symptoms" / "negative findings" — symptoms-only wrongly narrows to patient-reported. → "expected findings the patient does NOT have" (7 words; matches both the chapter's and the glossary's register). Chapter-sense-over-thin-glossary call reviewed and endorsed: not contradictory, both registers on card. |
| 6 | cookbook medicine | REWRITE | Ex: quote opened mid-reference — "When providers do this…" with no referent on the card (deixis, Layer A #2). Prepended the source's own preceding clause with a bracketed gloss: "it is important that [assessment] is not done robotically by the book. When providers do this…". Also "Distinguish: its opposite…" → "the opposite of cookbook medicine…" (pronoun-start). External anchor correct: the finder wrote no evidence entry, so in_source may not be self-asserted (R37) even though the context carries the inline definition — routed to Parker's eyes as designed. |
| 7 | pallor | PASS | in_source p2386 verified; answer agrees ("pale skin"); cyanosis Distinguish is the brief-licensed contrast; Parts: rightly omitted (pallere = "be pale" would recycle the root). |
| 8 | focused assessment | REWRITE | Answer said "the complaint's body *area*" — the glossary discriminator is "one body **system or part**" (a focused cardiovascular exam is not an "area"). → "an exam limited to the complaint's body part/system" (8 words). Formal completion re-verified verbatim at p4058. |
| 9 | auscultate | PASS | Crisp 4-word answer agrees with glossary; idx 162's BP/Korotkoff context honored in Cue:; auscultare etymology real. |
| 10 | mastectomy | PASS | External correct (book never defines it — confirmed no glossary entry expected, none claimed); mast-/-ectomy real; Why: carries the clinical point (no BP that side). No fabricated authority. |
| 11 | fistula | REWRITE | Two fixes: (a) answer tail "…for dialysis access" echoed the visible frame "In dialysis patients" (stem-echo padding) → trimmed to "a surgically made vein-to-artery connection" (5 words, crisper, discriminator intact); (b) Formal:'s meta-commentary ("the book's own wording where it teaches dialysis") replaced with the evidence quote's own location fact ("usually located in the forearm or upper arm"). p1975 sentence independently confirmed. |
| 12 | ecchymosis | PASS | "a bruise — blood pooled under the skin" is the lane's ideal plain form; hematoma Distinguish keeps raised-vs-flat discriminator; glossary agrees. |
| 13 | paradoxical motion | PASS | Retractions Distinguish confirmed book-faithful (see above); Why: grounded in the glossary's "detached in a flail chest"; Formal verified. |
| 14 | flail | REWRITE | `Cue:` opened with "its" (pronoun-start) → "the telltale sign of a flail is…". Numeric Formal re-verified against p4057 text; recorded in verified_by. |
| 15 | pneumothorax | PASS | "air in the space around a lung" = pleural cavity in plain words; subq-emphysema Distinguish keeps skin-vs-chest discriminator + the suspect-the-second clinical link (grounded idx 185). |
| 16 | guarding | PASS | Involuntary + abdominal-wall + pain-protective all kept; rigidity Distinguish; domain frame licensed (generic English word). |

Gate after edits: identical to hand-off state (3 expected external HARDs that
verify_report.py clears by deriving the flag — confirmed the derivation keys on
`anchor.method == "external"`; 1 expected distention WARN answered by the hunt record).
No new findings introduced. Cross-links now genuinely bidirectional: crepitus↔subq
emphysema, subq↔bare emphysema, pneumothorax↔subq, flail↔paradoxical motion,
pallor↔cyanosis, diaphoresis↔clammy. Repeat-mark hand-off flags (crepitus ×2;
diaphoresis and auscultate families) stand — surface them.
