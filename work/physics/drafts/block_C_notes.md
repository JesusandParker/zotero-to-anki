# Block C — Units, Standards, and the SI System (drafter notes)

Source: physics (Giancoli 7e), segment 1, chapter 1, pp. 29-32 (labels 8-11).
Items drafted: idx 20-34 of `work/physics/chapter_1_highlights.json`. **35 cards** in `block_C.json`.
Read for Rule-0 context: the whole highlights file; drafted ONLY from idx 20-34.

Card index map (0-based positions in block_C.json):
- #0 M1 first international standard (idx 22) · #1 M2 meter original definition (idx 23) · #2 M3 meter current definition (idx 24)
- #3 S1 second + cesium (idx 25+26) · #4 K1 kilogram + cylinder (idx 27+28) · #5 K2 amu (idx 29) · #6 U1 multiples of 10 (idx 30)
- #7-#26 P1-P20 prefix rows, table order yotta→yocto (idx 32) · #27 micro symbol · #28 deka symbol · #29 case pattern (all idx 32)
- #30-#34 lexicon: unit (20), standard (21), base quantity (31), derived quantities (33), operational definition (34)

---

## Fact-pass tables

### Unit 1 — THE METER (idx 22 + 23 + 24, one Rule-0 cluster → 3 notes)
| # | Proposition | Class | Where tested |
|---|---|---|---|
| 1 | The meter was the FIRST truly international standard | MUST | M1 c1 |
| 2 | Established by the French Academy of Sciences | MUST | M1 c2 |
| 3 | Established in the 1790s | MUST | M1 c3 (::decade, rule 27) |
| 4 | Original def: one ten-millionth of equator→either-pole distance | MUST | M2 c1 (fraction) + c2 (span) |
| 5 | Current def: length light travels in vacuum in 1/299,792,458 s | MUST | M3 c1 (light in vacuum) + c2 (fraction) |
| 6 | Abbreviated m | SKIP | first-letter-derivable padding; not clozed |
| 7 | Platinum rod made to represent it (context) | SUPPORTING | M1 Back Extra Why |
| 8 | 1889 platinum-iridium bar marks; 1960 krypton-86 wavelengths; 1983 redefinition (context) | SUPPORTING | M3 Back Extra Pathway |
| 9 | 1 m ≈ nose-to-outstretched-fingertip (context) | SUPPORTING | M1 Back Extra Cue |
| 10 | Original survey off by ~1/50 of 1% (footnote) | SUPPORTING | M2 Back Extra Ex — see flag 6 |
| 11 | c's best measured value 299,792,458 m/s ± 1 (context) | SUPPORTING | M3 Back Extra Cue (reciprocal hook) |

Decisions: three notes, not one — each definition era is one topic (Layer A #1); "as the standard of length"
dropped from M1's visible stem because "standard of length" + French + 1790s lets a NON-knower decode
"meter" (rule 3 median); the superlative claim is the tested direction instead. M2 hides the fraction and
the geographic span under different numbers (each card keeps the other as anchor — no husk). M3's c2 has
no hint: "of a second" immediately after the blank is the unit-frame rule-27 exemption. M3's c1 ("light in
vacuum") is strongly cued by the visible reciprocal-of-c fraction for anyone who knows c — accepted:
that is knowledge, not decoding, and hiding both spans would be an R10 husk.

### Unit 2 — THE SECOND (idx 25 + 26, Rule-0 pair → 1 note, S1)
| # | Proposition | Class | Where tested |
|---|---|---|---|
| 1 | Standard unit of time = second | MUST | S1 c1 |
| 2 | Now defined via frequency of radiation from cesium atoms between two particular states | MUST | S1 c2 (crisp discriminator = cesium; mechanism phrase stays as visible scaffold) |
| 3 | 9,192,631,770 oscillations (bracketed context, NOT highlighted) | SUPPORTING | Back Extra Ex only — per block guidance, never a cloze |
| 4 | Old def 1/86,400 of a mean solar day (context) | SUPPORTING | Back Extra Distinguish |
| 5 | Abbreviated s; 60 s/min, 60 min/h | SKIP | padding / trivial context |

Decision: clozing just "cesium" (::element) rather than the whole mechanism phrase — rule 5 crisp-cloze;
"frequency of radiation emitted by" is scaffold. "when THEY pass" keeps its referent ("atoms") visible on
both cards. numeric=false: no clozed number; the big numbers live in Back Extra, verbatim from context.

### Unit 3 — THE KILOGRAM (idx 27 + 28 + 29 → 2 notes, K1 + K2)
| # | Proposition | Class | Where tested |
|---|---|---|---|
| 1 | Standard unit of mass = kilogram | MUST | K1 c1 |
| 2 | Standard mass = platinum-iridium cylinder | MUST | K1 c2 (::alloy) |
| 3 | Kept at International Bureau of Weights and Measures near Paris | MUST | K1 c3 (::institution) |
| 4 | Its mass is defined as exactly 1 kg | MUST | K1 stem ("defined as exactly the mass of…") — phrased so no visible "kg" leaks c1; the exactly-by-definition relation is the sentence itself |
| 5 | Atoms/molecules → unified atomic mass unit (u or amu) | MUST | K2 c1 (term + abbreviations in ONE blank — either visible would decode the other) |
| 6 | 1 u = 1.6605 × 10^-27 kg | SUPPORTING | K2 Back Extra Ex only (science profile: relationship over value); VERIFIED on p31 render |
| 7 | 1 kg ≈ 2.2 lb on Earth (bracketed context) | SUPPORTING | K1 Back Extra Ex |
| 8 | Proton ≈ 10^-27 kg (Table 1-3 context) | SUPPORTING | K2 Back Extra Why |

Decisions: K1's Distinguish breaks the platinum-iridium interference (1889 meter BAR vs kilogram CYLINDER)
— the bar fact is grounded in idx 23's context, cited on M3's Pathway too. K2 numeric=false because the
1 u value is Back-Extra-only (the block guidance's "if you cloze the value" condition not met); it still
carries verified_against p31 — consolidator: if the gate wants numeric=true for back-side constants, flip it.

### Unit 4 — METRIC = MULTIPLES OF 10 (idx 30 → 1 note, U1)
| # | Proposition | Class | Where tested |
|---|---|---|---|
| 1 | Larger/smaller metric units = multiples of 10 from the standard unit | MUST | U1 c1 (::number, rule 27) |
| 2 | This makes calculation easy | SUPPORTING | visible in stem |
| 3 | kilo=1000 m, centi=1/100 m, milli=1/1000 m examples (context) | SUPPORTING | Back Extra Ex |
| 4 | Prefixes apply to ANY unit (cL, kg examples) (context) | SUPPORTING | Back Extra Why |

### Unit 5 — TABLE 1-4 METRIC (SI) PREFIXES (idx 32, CAPTION_ONLY/needs_visual → 23 notes)
All 20 rows read visually from the p31 render this run (VERIFIED); text layer carries them garbled
(carets lost: "yotta Y 1024"). Every table card cites verified_against "p31", verified_by "agent, read
from page render this run", and visual_source with a RESOLVABLE figures path (`work/physics/page_31.png`)
— the checker's R13 visual exemption requires the evidence to exist on disk, prose alone exempts nothing.

| Fact | Class | Where tested |
|---|---|---|
| 20 × (prefix → power of ten) | MUST | P1-P20, one note per key (rule 25, Parker's own design) — value alone in c1, abbreviation VISIBLE, no hint ("multiplies a unit by" + 10^ shape announces the slot) |
| micro → μ (Greek mu) | MUST | #27 (::symbol) — not first-letter-derivable; footnote "μ is the Greek letter mu" verified |
| deka → da | MUST | #28 (::symbol) — own small note (guidance's option b) so "da" is actually TESTED, not a freebie Distinguish line; cross-linked to deci, no values stated |
| Case pattern: uppercase mega-and-larger, lowercase kilo-and-smaller | MUST | #29, both case words under one c1 with forced-choice ::uppercase/lowercase hints |
| All other abbreviations (Y Z E P T G M k h d c m n p f a z y) | SKIP | first-letter-derivable = self-answering padding (Parker's word); stay VISIBLE on their row cards |

Back Extra discipline on P1-P20: ONE line each, a knowledge-free arithmetic Ex restating the prefix
itself (1 GHz = 10^9 Hz; the mega card uses the book's own 8.2-megapixel camera, grounded in idx 30's
context). NO neighboring row's value appears in any Back Extra prose (rule 25 interpolation leak).
The micro/deka symbol cards' Distinguish lines name the colliding prefix (milli, deci) with NO values.

**Case-pattern card verified claims:** mega-and-larger all uppercase (M G T P E Z Y), kilo-and-smaller all
lowercase (k h da d c m μ n p f a z y) — checked row by row on the render. "Only two-letter abbreviation"
claim on the deka card: also verified against all 20 rows (μ is a single letter).

### Unit 6 — LEXICON (idx 20, 21, 31, 33, 34 → 5 §4b cards, all anchor external)
| Term | term_key | Answer authored (plain · crisp · faithful) | Discriminator kept |
|---|---|---|---|
| unit | unit | "the named amount a measurement is expressed in" (8 w) | vs standard: what you express IN |
| standard | standard | "the agreed physical reference defining a unit exactly" (8 w) | the defining reference; "exactly" kept |
| base quantity | base_quant | "one defined by its own standard, not other quantities" (9 w) | own standard, not from other quantities |
| derived quantities | deriv_quant | "quantities defined in terms of the base quantities" (8 w) | built FROM base quantities |
| operational definition | oper_defin | "a definition that specifies a rule or procedure" (8 w) | rule/procedure; NOT blended with "standard" |

All five: one-way (word → meaning), Ex quotes the met-sentence with the term bolded, term_keys copied
exactly from the highlights JSON. unit ↔ standard cross-linked with mirrored Distinguish lines (purpled in
the same sentence); base ↔ derived cross-linked likewise (speed = distance ÷ time example from idx 33's
own context). "operational definition" gets Parts: instead of a Distinguish — a contrast line against
"standard" risked exactly the blending the block guidance forbids.

---

## Expected gate noise (do not re-fix)

1. **5 HARD R35 errors on #30-#34 (external anchor without needs_human_check) are EXPECTED at draft
   stage.** needs_human_check is derived, never asserted (note-format.md); run `verify_report.py` before
   the write gate and they clear into the report's Vocabulary block — the normal outcome for this book
   per the science profile.
2. **Warning "#30 anchor external but in-source definition EXISTS for 'unit' (p31)"** — cleared, recorded
   in that card's verified_by: the lexicon_evidence quote is "unit (u or amu)", the ATOMIC-MASS-UNIT
   sense, not the generic p29 sense Parker marked. §4b SENSE-CHECK downgrade to external; the amu sense
   got its own yellow-lane card (K2). Do not re-anchor.
3. **Warning "#32 hides 9 words"** — cleared, recorded in verified_by: 9 plain words is the floor that
   keeps the task-mandated discriminator for "base quantity".

## Flags for the consolidator / hand-off

1. **MIDWORD hygiene flags on idx 20 ("unit") and idx 21 ("standard")** — extractor flagged both; the
   extracted terms read as complete words, so I proceeded as-is. Surface at hand-off per rule 28 triage
   (Parker confirms accident vs intent; both look deliberate — they sit in the sentence that defines the
   section's topic).
2. **Force-attach the TABLE 1-4 plate** to the back of all 20 prefix notes (#7-#26) downstream — image is
   null on all of them by instruction; visual_source already points at `work/physics/page_31.png` (the
   full-page render; a tighter table crop from the figure index would be better if one exists). Parker's
   design: "disconnected in the sense of memorizing, connected in the sense of the table."
3. **OPEN QUESTION for Parker:** prefix cards are prefix → value ONLY. The reverse direction
   (10^9 → "giga") is not drafted; reflex two-way is banned for numbers, but if he wants production of
   the prefix names, that is a second 20-card lane he must ask for.
4. **PARTIAL-grounding items handled:** idx 24 (the fraction lives in context with the CJK slash 兾 —
   normalized to "1/299,792,458"); idx 28 and the idx 29 value completion both verified against the p31
   render this run. M3 is numeric=true with verified_against=null (text-layer grounded) — if the gate
   wants render verification for it, p30 would need a render pass; the digits match the context verbatim.
5. **M1's dates (1790s) numeric=true, text-grounded (EXACT highlight), not render-verified** — same
   convention block A used for p23 dates it DID render; flag only if the gate demands render proof.
6. **M2's Back Extra Ex (survey off by one-fiftieth of 1%)** is the † footnote attached to idx 23's own
   sentence; the footnote TEXT was captured in idx 26's context window (same page 30). Grounded, but the
   from_idx trace is [23] — noting the cross-context read here so R13 review does not mistake it for an
   outside fact.
7. **K1's Distinguish line** (meter BAR vs kilogram CYLINDER) draws the bar fact from idx 23's context;
   from_idx stays [27, 28] for coverage accounting.
8. **Case-pattern card (#29) shows mega=10^6 and kilo=10^3 visible in its stem** (per block guidance —
   they anchor the boundary). Mild reveal of those two row-card answers; those are the two most
   universally known rows, accepted trade-off.
9. **U1's Back Extra restates kilo/centi/milli values** — they are the book's own examples inside idx 30's
   highlight context (the anchor card's teaching material, not a row card's back). The full-table
   attachment on row backs makes all values post-answer-visible anyway; rule 25's interpolation concern
   is about deriving answers pre-answer, which none of this enables.
10. **Unmarked-but-central p31 prose NOT carded (rule 29):** the SI name (Système International, ex-MKS),
    the cgs and British systems, and Table 1-5's enumeration of the seven SI base quantities (explicitly
    excluded by the block guidance — the COUNT seven is used, grounded in idx 31's context, on the
    base-quantity card's Why line only). One permitted hand-off sentence: "p31's SI/MKS/cgs naming prose
    and Table 1-5's seven base quantities are unmarked — want anything from them?"
11. **Abbreviations m / s / kg never clozed** — first-letter-derivable padding; left visible or omitted.
12. **No ledger info was provided for the five lexicon terms** — dedup against the term ledger + live-Anki
    liveness (lexicon.py) is assumed to run at consolidation; term_keys are exact copies for that purpose.
