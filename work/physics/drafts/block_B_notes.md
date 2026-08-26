# Block B — uncertainty & significant figures (drafter notes)

Items: idx 9–19 of `chapter_1_highlights.json` (pp. 27–29). 10 note objects drafted in `block_B.json`, source order.

## Fact-pass tables

### Unit 1 — percent uncertainty (idx 11 yellow + idx 17 purple, FOLD-IN)
| Proposition | Class | Where tested |
|---|---|---|
| percent uncertainty = uncertainty / measured value × 100 | MUST-TEST | card 3, c1 (name it) + c2 (state it), two-way |
| worked example 0.1/8.8 × 100% ≈ 1% | SUPPORTING | card 3 Ex: (mandated) |
| "≈ means approximately equal to" | SKIP | notation gloss in context, unmarked |

**CROSS-LANE FOLD-IN (SKILL.md Stage 2.5), logged as mandated:** purple idx 17 ("Percent Uncertainty", anchor in_source p27 per `lexicon_evidence.json`) marks the exact term yellow idx 11 defines. NO separate lexicon card shipped; ONE regular card cites `from_idx: [11, 17]`. R36-safe: a fold-in must cite at least one yellow mark, and it does. Consolidator: record `perc_uncertaint` in the lexicon ledger as covered-by-fold-in so a re-mark is recognized.

### Unit 2 — lexicon "interpolate" (idx 9, anchor external)
| Proposition | Class | Where |
|---|---|---|
| interpolate = estimate between a scale's smallest divisions (source's sense) | MUST-TEST | card 1, c1 authored plain definition |
| encounter sentence (ruler, smallest divisions) | SUPPORTING | Ex: (required, quoted, term bolded) |
| interpolation difficulty ⇒ reading precise only to ~smallest division (or half) | SUPPORTING | Cue: — cross-links to estimated uncertainty (idx 10) |

Distinguish: vs *extrapolate* — authored dictionary knowledge, lane-licensed (§4b nearest-confusable line). `Parts:` skipped (poly-/-polate decomposition is folk-etymology territory, adds nothing).

### Unit 3 — lexicon "estimated uncertainty" (idx 10, anchor external)
| Proposition | Class | Where |
|---|---|---|
| estimated uncertainty = the stated ± a measurement might be off by | MUST-TEST | card 2, c1 authored plain definition |
| 8.8 ± 0.1 cm ⇒ actual width most likely 8.7–8.9 cm | SUPPORTING | Ex: (required, quoted) |
| relation to percent uncertainty | SUPPORTING | Distinguish: (mutual with card 3) |

### Unit 4 — unstated-uncertainty convention (idx 12)
| Proposition | Class | Where |
|---|---|---|
| unstated uncertainty assumed = one or a few units in the last digit specified | MUST-TEST | card 4, both spans one c1 group (2 uncued answers, ≤4 load; rule 17 litmus passes — visible frame still points at the convention) |
| 8.8 cm ⇒ assumed ±0.1–0.2 cm | SUPPORTING | Ex: |
| do NOT write 8.80 (implies ±0.01, 8.79–8.81) | SUPPORTING | Pitfall: — grounded context, per block guidance NOT separately carded (span not marked, rule 29) |
| stated ± vs the fallback assumption | SUPPORTING | Distinguish: — cross-links idx 10 |

### Unit 5 — significant figures definition (idx 13)
| Proposition | Class | Where |
|---|---|---|
| significant figures = the reliably known digits | MUST-TEST | card 5 two-way: c1 term, c2 discriminator "reliably known" |
| 23.21 → four; 0.062 → two | SUPPORTING | Ex: |
| leading zeros in 0.062 are place holders, not significant | SUPPORTING | Distinguish: |

### Unit 6 — the 80-km family (idx 14 + 15, Rule-0 pair)
| Proposition | Class | Where |
|---|---|---|
| "roughly 80 km" → ONE sig fig | MUST-TEST | card 6, c1 |
| the zero there is merely a place holder | MUST-TEST | card 6, same c1 group |
| unmarked 80 → assumed ±1–2 km → TWO sig figs | TAUGHT-NOT-TESTED (deliberate) | card 6 Distinguish: only, per block guidance — middle case of a one/two/three count column; kept off any blank as interpolation control (rule 25 spirit). Part of idx 14's marked span, so flagging here for the consolidator: coverage is by Distinguish line, not cloze, by design. |
| precisely-±0.1 → written 80.0 km | MUST-TEST | card 7, c2 (production direction: choose the notation) |
| 80.0 km → THREE sig figs | MUST-TEST | card 7, c1 |

Rule 27 on every count answer: card 6 satisfies it in the STEM ("the number of significant figures is ___" — the licensed quantity-word form, hint redundant per rule 27); card 7 carries the mandated slot-label `{{c1::three::number of sig figs}}`. Separate small notes as mandated; neither note's back reveals the other's tested count (card 6's back reveals only the untested middle "two"; card 7's back reveals no counts).

### Unit 7 — multiplication/division rule (idx 16)
| Proposition | Class | Where |
|---|---|---|
| ×/÷ result keeps no more digits than the value with the FEWEST sig figs | MUST-TEST | card 8, crisp 3-word cloze on "fewest significant figures" (fact-pass call: tighter deletion than clozing the whole "which input" phrase; forced cold) |
| 11.3 × 6.8 = 76.84 → quote 77 cm² (6.8 has two) | SUPPORTING | Ex: |
| 77 cm² implies ~1–2 cm² uncertainty; extra digits not significant | SUPPORTING | Why: |
| add/subtract keeps fewest DECIMAL PLACES | TAUGHT-NOT-TESTED (mandated) | Distinguish: line only — context, not marked (rule 29); it is the classic confusable so the line earns its place |
| EXERCISE A answer | SKIP | not in marked spans; zero guessing — never stated anywhere |

### Unit 8 — accuracy vs precision (idx 18 + 19, §8/§4 pair)
| Proposition | Class | Where |
|---|---|---|
| precision (strict sense) = repeatability using a given instrument | MUST-TEST | card 9 two-way |
| accuracy = how close a measurement is to the true value | MUST-TEST | card 10 two-way |
| repeated 8.81/8.85/8.78/8.82 ⇒ precision a bit better than 0.1 cm | SUPPORTING | card 9 Ex: |
| 2%-error ruler ⇒ accuracy ~±0.2 cm on 8.8 cm | SUPPORTING | card 10 Ex: |
| estimated uncertainty covers BOTH accuracy and precision | SUPPORTING | card 10 Cue: (single placement; the mention IS the cross-link to idx 10, per block guidance) |

Mutual Distinguish lines on both cards (Parker's confusables preference; the sanctioned §4 pattern — each back names the sibling's definition on purpose).

## Decisions & flags for the consolidator

1. **Run `verify_report.py` BEFORE `check_cards.py`.** All `needs_human_check` set false per drafting contract (derived, never asserted). Expected derivations: cards 1 & 2 (external lexicon anchors → true, R35 — the gate HARD-fails them until derivation runs); cards 6 & 7 (numeric count answers → true); card 3 cites idx 11 (grounding PARTIAL) — derive per policy.
2. **numeric flags:** true only on cards 6 & 7, whose tested answers are counts stated as fact ("one", "three"). Card 3's "× 100" is structural to the formula, card 4's "one or a few units" is a fuzzy convention, and all other digits (8.8, 0.1, 23.21, 0.062, 11.3, 6.8, 77, 2%) are worked-example values living in Ex/Pitfall/Distinguish lines — per block guidance, unflagged. Overrule if policy reads the formula card as numeric.
3. **OCR repairs in quotes:** source text garbles ± ("8.860.1", "&0.1", "&1 mm", "9261/9761"). Quoted Ex lines render them correctly as 8.8 ± 0.1 cm / ±0.1 cm. Faithful to the printed page, not an invention.
4. **idx 11 PARTIAL grounding:** the definition sentence is complete inside the item's own context field; quoted faithfully (ratio → "divided by", meaning-identical, mandated plain phrasing).
5. **Back-Extra reveal audit:** card 2's Distinguish (extrapolate) is authored external knowledge under the lexicon lane's license, not source-grounded — it is on a lexicon card, where that is the lane's nature. Cards 2↔3, 3↔folded-percent-card, 9↔10 intentionally reveal each other's definitions in Distinguish lines (confusable cross-linking). No card's back reveals a SIBLING'S tested count (checked for the 80-km family).
6. **No unmarked content carded:** add/subtract rule and the 8.80 trap appear only as Distinguish/Pitfall lines grounded in context; EXERCISE A untouched; middle 80-case untested by mandate.
7. **Load audit:** max uncued answers under one number on any note = 2 (cards 4, 6). No grouped list ≥5, no sibling-number fan-out, no keyed numeric panel (the one/two/three column was deliberately split across two notes with the middle taught, not tested).
8. **Cold-solve spot-check (per row):** card 6 was rephrased to "the number of significant figures is ___" so the singular/plural of "figure(s)" cannot leak the count; card 7's c2 ("80.0 km") is derivable only via the trailing-zero convention (hard-but-forced, the intended skill); card 8's stem keeps the ×/÷ discriminator visible and bolded since the rule differs for +/−.
