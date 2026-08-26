# Block D_estimating_dimensions — drafter notes

Items: idx 35 (PURPLE lexicon, p34/label 13), idx 36 (yellow, p37/label 16), idx 37 (yellow, p37/label 16, PARTIAL).
Rule-0 read of the whole chapter file done: idx 35 stands alone (§1-7 estimating); idx 36+37 are one connected unit (§1-8 dimensions — definition + its worked example, same paragraph, consecutive).

## Fact-pass

| # | Proposition | Source | Status | Disposition |
|---|---|---|---|---|
| 1 | An order-of-magnitude estimate is a rough estimate made by rounding all numbers to one significant figure and its power of 10 (keeping one sig fig after calculating) | idx 35 context | MUST-TEST (lexicon lane) | Card 1 c1 (compressed authored answer); full procedure quoted in Formal: |
| 2 | Such an estimate is accurate within a factor of 10, often better | idx 35 context | SUPPORTING | Card 1 Back Extra — carried inside the required Ex: quote |
| 3 | "Order of magnitude" alone is sometimes used to mean simply the power of 10 | idx 35 context | SUPPORTING | Card 1 Back Extra Distinguish: |
| 4 | The dimensions of a quantity = the type of base units or base quantities that make it up | idx 36 highlight | MUST-TEST | Card 2, two-way definition (c1 term / c2 meaning) |
| 5 | The dimensions of area are always length squared | idx 37 highlight | MUST-TEST | Card 3 c1 |
| 6 | Dimension notation uses square brackets: [L²] | idx 37 highlight (garbled "CL2 D") | MUST-TEST | Card 3 c1 (notation inside the same cloze: "length squared — written [L²]") |
| 7 | Units of area can differ (m², ft², cm²) while dimensions stay the same | shared context | SUPPORTING (per caller) | Card 3 stem carries the abstract contrast ("the units vary, not the dimensions"); the concrete units land in Card 3 Distinguish: |
| 8 | Velocity: units km/h, m/s, mi/h differ, dimensions always [L/T] | shared context (in idx 36's context field) | SUPPORTING (per caller) | Card 2 Distinguish: (fresh exemplar — deliberately NOT area, see sibling-leak note) |
| 9 | [L] = a length, [T] = a time (bracket convention) | idx 36 context, brackets intact | SUPPORTING | Card 2 Cue: |
| 10 | The formula for a quantity may differ (triangle vs circle area) but the dimensions remain the same | shared context, beyond the highlights | SUPPORTING | Card 3 Ex: (no formulas restated — see reconstruction notes) |

Every MUST-TEST fact is clozed somewhere: 1 → card 1; 4 → card 2 (both directions); 5+6 → card 3. Both yellow marks covered; the purple mark covered. No unmarked content carded (rule 29): velocity/[L/T] and formula-invariance appear only as Back Extra support, never as tested facts.

## Shape decisions

- **idx 35 — §4b lexicon, one-way, no hint.** Answer authored plain/crisp/faithful at 8 words: "a rough estimate rounded to powers of ten" (discriminator per unit guidance). The exact procedure and the factor-of-10 accuracy go to Back Extra (Formal:/Ex:), per guidance. "Estimate" repeating from the term is the plain genus word, not the root-defining trap (the jargon root is "order-of-magnitude", and the answer renders it in plain words, "powers of ten").
- **idx 36+37 — TWO sibling notes, not one note with c1/c2/c3.** On a single note, the c2 (meaning) card would show "for area, always length squared" as visible scenery — a worked instance from which the definition is partly decodable (rule 3 crutch). Splitting also lets each card use a fresh exemplar (rule 13): card 2's Back Extra uses VELOCITY ([L/T]); card 3 owns AREA ([L²]). Card 2's Back Extra never states [L²], so it cannot pattern-feed card 3.
- **Card 2 is the two-way definition** (Parker default). c2 = "the type of base quantities/units composing it" (7 words) — first draft ("…or units that make it up", 11 words) tripped the long-cloze detector (LONG_CLOZE_WORDS=9); the slash form keeps both of the book's nouns and matches the unit guidance's own phrasing.
- **"In physics," frame on cards 2 and 3**: megadeck isolation — everyday "dimensions" (size of an object) is a live wrong sense in a shuffled all-subject deck; two words pin it. Situational, not definitional; no leak.
- **Card 3 stem carries the invariance as a rule-21(b) contrast**: "…are <i>always</i> {{c1::…}} — the units vary, not the dimensions." First draft's tail ("whatever units are used") left the lone "always"-blank looking open-set to `open_set_absolute`; the named rejected alternative both silences the proxy and is the better card (the contrast IS the concept). The tail does not leak — it never says WHICH dimensions. Concrete units (m², ft², cm²) still stay off the front, since a visible squared unit would let a non-knower decode "length squared" (rule 3); they moved to the Distinguish: line, which now adds the concrete instances rather than restating the front's abstract contrast.

## Grounding / reconstruction notes (for the consolidator)

- **idx 37 PARTIAL is purely a text-layer artifact.** The source's [L²] renders as "CL2 D" in the extraction. Reconstruction to [L²] is safe: the same paragraph (idx 36 context) preserves the bracket convention intact — "a length [L] divided by a time [T]: that is, [L/T]" — and the highlight itself says "length squared, abbreviated … using square brackets" in words. verified_by carries the caller-prescribed string; numeric stays false (notation, no memorized value).
- Other mechanical de-garbles used, same class, none load-bearing on a tested answer: "km兾h" → km/h (CJK slash glyph); the idx 35 context interleaves a margin box ("P R O B L E M S O LV I N G / How to make a rough estimate") into the defining sentence — the Formal: quote is that sentence with the interleave removed, no words added.
- **Card 1 Formal: caveat.** Anchor is `external` (verified: `work/physics/lexicon_evidence.json` has no `order_of_magnitud_estimat` entry), so there is no anchor-evidence quote to cite; the Formal: line instead quotes the mark's own extractor context verbatim (de-interleaved). Caller sanctioned Ex:/Formal: as the vehicles for these nuances. If the gate reads Formal: as licensed only against lexicon_evidence, relabel that line `Mechanism:` — content unchanged.
- **Expected flag, not a defect:** external anchor → verify_report.py will derive needs_human_check true for card 1 and route it to the report's Vocabulary block (R35). Drafted false per instruction (derived, never asserted).
- verified_against uses book page labels ("p13", "p16"), matching provenance.md's "p531" convention.

## from_idx rationale

- Card 1: [35]. Card 2: [36] (its highlight + its own context field carry everything used, incl. the velocity sentence). Card 3: [37, 36] — 37's highlight is the tested fact; 36's context supplies the intact-bracket convention that grounds the [L²] reconstruction, so both were genuinely used. R36 satisfied: the one lexicon card cites only a purple mark; yellow cards cite only yellow marks.

## check_cards.py result (draft stage)

`python3 scripts/check_cards.py work/physics/drafts/block_D.json` → 0 warnings; ONE hard error, which is the expected pre-verify state, not a defect: card #0's external anchor demands the derived needs_human_check, and the message itself says "run verify_report.py before the gate" (R35). Consolidator: run verify_report.py over the merged staging file and the error resolves into the intended Vocabulary-block flag.

## Self-check run (quick gate mirror)

One answer per blank (cold-solve passes on all four fronts) · no leak (definitional content hidden or on the back; two-way def is the endorsed non-leak) · grounded (every claim traced above) · fully clozed (all MUST-TEST tested) · no lists (no listify/roster obligations) · crisp deletions · hints: none (every stem forces its answer; nothing open-set, no bare counts) · standalone (no deixis, no source-medium words; "Formal:" label is the licensed §4b register marker) · Back Extra adds new edges only, labels from the blessed set, components joined with `<br><br>` · HTML used: `<b>`, `<i>` only · numeric false on all three (no memorized value) · needs_human_check false on all three (derived later).
