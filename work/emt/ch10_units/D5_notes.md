# D5 notes — Skin · capillary refill · bleeding character (idx 50–57, 59–63, 65–72)

21 yellow marks → **21 cards** (ratio 1.0). Purple 58/64 read for adjacency, not carded (DL's lane).
No `user_comment`, no `list_lead_in`, no `needs_visual` on any assigned mark; all grounding EXACT.
`check_cards.py`: 0 hard errors; 1 adjudicated warning (see Q block).

## Verification record (renders read in full)
- **p966** (rendered this run): `98.6°F (37°C)` verbatim ✓; cool-skin causes (early shock / mild
  hypothermia / inadequate perfusion) ✓; jaundice + sclera sentences ✓; high-BP flushed/red ✓;
  hot/cold cause sets in surrounding text ✓.
- **p968** (rendered this run): 2-second threshold, "about the time it takes to say 'capillary
  refill'", "CRT as normal (2 seconds or less)", >2 s / stays blanched → suspect poor peripheral
  circulation ✓; thumb-on-nail technique + FIGURE 10-14 captions ✓; newborn/young-infant sites
  forehead/chin/sternum ✓.
- **p967** (belt-and-suspenders): reporting order color → temperature → moisture ✓; "Skin: pale,
  cool, and clammy" example ✓; clammy/damp/moist vs wet/diaphoretic terminology ✓; early shock →
  slightly moist ✓.
- **p969** (belt-and-suspenders): vein steady / artery spurting ✓; unconscious head-to-toe glove
  sweep ✓.
- p963/964 not rendered: those cards carry no numbers or ordered sequences; contexts are EXACT and
  quote the sentences verbatim (`verified_against: null` on those four cards is intentional).

---

## Block N_skin_color (idx 50–57) — 8 cards

| Proposition | Where | Class | Disposition |
|---|---|---|---|
| Inadequate skin blood flow → pale, cool skin | 50 | MUST | N-1 c1 |
| Pale/cool may signal hypoperfusion of brain, lungs, heart, kidneys | 50 | MUST | N-1 c2 (closed 4-set, grouped, `::4 organs`) |
| Hypoperfusion is usually caused by shock | 50 | MUST | N-1 c3 |
| Perfusion window: skin holds color/temp/moisture; degree+duration → permanent injury | 50 ctx | SUPPORTING | N-1 Back (Why/Pitfall) |
| Skin color = circulating blood + amount/type of pigment | 51 | MUST | N-2 (grouped 2-set, count in stem) |
| Conjunctiva = delicate membrane lining eyelids + eye surface | 52 | MUST | N-3 two-way definition |
| Low-pigment sites in deeply pigmented skin; infant palms/soles | 52 ctx | SUPPORTING | N-3 Cue line |
| Pale/white/ashen/gray, waxy = poor peripheral circulation; cold skin mimics | 52 ctx | SUPPORTING | N-8 stem framing + Pitfall |
| Unsaturated blood appears blue | 53 | MUST | N-4 c2 (merged w/ 54 per Rule 0 — 54 opens "Therefore…") |
| Insufficient air exchange → blue-gray lips/mucosa/nail beds = cyanosis | 54 | MUST | N-4 c1 |
| High BP → abnormally flushed, red skin | 55 | MUST | N-5 |
| Heat-dissipation causes of red skin (fever, heatstroke, sunburn, burns) | 55 ctx | SUPPORTING | N-5 Ex line (see flags) |
| Liver disease/dysfunction → jaundice, skin+sclera yellow | 56 | MUST | N-6 (c1 organ, c2 name) |
| Sclera = normally white portion of eye | 57 | MUST | N-7 c1/c2 two-way |
| Sclera shows color change BEFORE skin | 57 | MUST | N-7 c3 (binary `::before or after`) |

**Archetypes:** N-1 grouped fact chain (§6 within one topic); N-2 grouped 2-list; N-3, N-7 two-way
definitions (§4); N-4 mechanism+name (§7/§4); N-5 buzzword-direction with category hint (§9);
N-6 classification pair; N-8 vignette (§9, the auto-pair).

**Judgment calls:**
- **Auto-pair scope.** The brief floated classify-the-cause vignettes across pale/flushed/jaundice/
  cyanosis. As drafted, the fact cards for cyanosis (N-4 c2), flushed (N-5, hint-forced), and
  jaundice (N-6 c1) already test the color→cause *decision* direction, so a 4-row classify panel
  would have double-tested three of its rows nearly verbatim (rule 12). The one mapping with no
  decision-direction card was pallor→shock — that became the single vignette **N-8** (motorcyclist;
  fresh exemplar, no sibling reuse). Cross-color discrimination is carried by `Distinguish:` lines
  on N-4/N-5/N-6 (pale=flow, blue=oxygenation, red=pressure/heat, yellow=chronic/liver).
- **N-5 direction.** Clozing "flushed and red" (cause→color) felt derivable; instead the answer is
  `high blood pressure` with hint `::cardiovascular cause`, which forces the field-relevant
  direction (red skin → think BP) while the hint walls off the fever/heat answers, which would
  otherwise make the blank open-set. Heat causes live in the Ex line, grounded in 55's context.
- **N-7 cites [56,57]**: the jaundice Cue line is grounded in 56; the definition + before-skin fact
  are 57. N-6 cites [56] alone.
- **Conjunctiva c2 tightened** after a checker length warning: 14 → 8 words ("delicate membrane
  lining the eyelids and eye surface"), article moved outside the brace per §4. "Exposed" was
  dropped as non-discriminating; both defining locations kept.
- Cross-sibling `Distinguish:` lines (conjunctiva↔sclera, pale↔blue↔red↔yellow) draw on facts
  marked elsewhere **within this unit** — the blessed confusable-cross-linking pattern, noted here
  because a strict single-mark grounding read would miss where each line is anchored.

**→ DL fold-in (sclera, purple idx 58):** N-7 is the fold-in target. It is a term↔meaning two-way
whose meaning side reads plainly — `{{c2::the normally white portion of the eye}}` — so the lexicon
card should FOLD INTO note N-7 rather than ship separately: add `Ex:` (the p966 sentence he met the
word in) and optionally `Formal:` (glossary p4122), and extend `from_idx` to [56,57,58]. Nothing
about N-7 needs to change for the fold; the consolidator only adds lines.

## Block O_skin_temp_moisture (idx 59–63, 65) — 6 cards

| Proposition | Where | Class | Disposition |
|---|---|---|---|
| Normal body temperature 98.6°F (37°C); skin normally warm | 59 | MUST (numeric ✓ p966) | O-1 |
| Abnormal temps: hot, cool, cold, clammy | 59 ctx | SUPPORTING | O-1 Ex line |
| Cool skin ← early shock / mild hypothermia / inadequate perfusion | 60 | MUST | O-2 (grouped 3-set, rows) |
| Cold ← profound shock/hypothermia/frostbite; hot ← fever/sunburn/hyperthermia | 60 ctx | SUPPORTING (exam-adjacent) | O-2 Distinguish (see flags) |
| Blood pulled surface→core; cool/pale/clammy = primary-assessment shock sign | 60 ctx | SUPPORTING | O-2 Cue |
| Early shock → slightly moist skin | 61 | MUST | O-3 (c1 early/late binary + c2 finding) |
| Slightly moist, not soaked = clammy/damp/moist | 62 | MUST | O-4 row 1 |
| Bathed in sweat (exercise, shock) = wet/diaphoretic | 63 | MUST | O-4 row 2 (Rule-0 merge: two rungs of one moisture ladder) + O-6 vignette |
| Report order: color → temperature → moisture | 65 | MUST | O-5 (§7 ordered, ordinals printed) |
| "Skin: pale, cool, and clammy"; consider the three together | 65 ctx | SUPPORTING | O-5 Ex/Why |

**Archetypes:** O-1 numeric (§5, unit inside the cloze, no hint needed — "temperature is" announces
the slot per rule 27); O-2 grouped list with rows (§6); O-3 comparison/binary + finding; O-4
two-row match ladder (§8-style, per-row anchors, count hints `::3 terms`/`::2 terms`); O-5 ordered
sequence, ordinals printed, all three under one c1; O-6 vignette (auto-pair on the terminology
discrimination).

**Judgment calls:**
- **O-4 leak repair.** The book's mild descriptors are self-echoing ("slightly *moist* … described
  as *moist*"), so the row labels were rewritten to sweat-quantity language ("only a slight film of
  sweat, not soaked" / "bathed in sweat") — no answer word appears in its own label. Residual: "wet"
  is near-derivable from "bathed in sweat"; the load-bearing recall there is *diaphoretic*, and the
  pair is graded together.
- **No second shock vignette.** Cool+moist→early-shock as a vignette would near-duplicate N-8
  (skin-findings→shock). Instead O-6 forces the *wording* decision (soaked runner → "wet,
  diaphoretic"), which is the fact 62/63 actually teach, with a fresh exemplar. The early-shock
  combination is taught on O-2's Cue and O-4's Pitfall.
- O-3 keeps `early` as its own binary cloze — that moisture is an *early* sign is the high-yield
  half of mark 61.
- O-4/O-6 answers overlap (auto-pair, sanctioned); O-6's Distinguish deliberately re-anchors the
  clammy boundary — discriminability over secrecy for a confusable pair.

## Block P_capillary_refill (idx 66–69) — 4 cards

| Proposition | Where | Class | Disposition |
|---|---|---|---|
| Technique: thumb on nail, fingers under finger, gently compress | 66 | MUST | P-1 c1 (grip, grouped pair) |
| Compress until blanched; released bed re-pinks as capillaries refill | 66 ctx | SUPPORTING | P-1 c2 (confirmation cue) + Why |
| Newborn/young-infant sites: forehead, chin, sternum | 67 | MUST | P-2 c1 (closed 3-set, rows) |
| Which patients use those sites | 67 | MUST | P-2 c2 (`::age group`) |
| Normal: pink within 2 s ("say 'capillary refill'") | 68 | MUST (numeric ✓ p968) | P-3 c1 + Cue |
| Document normal as CRT ≤ 2 s | 68 ctx | SUPPORTING | P-3 Ex (verified on render) |
| >2 s or stays blanched → suspect poor peripheral circulation | 69 | MUST (numeric ✓ p968) | P-3 c2 + P-4 vignette |
| Extremity injury → local (not systemic) hypoperfusion | 66 ctx | SUPPORTING | P-4 Distinguish |

**Archetypes:** P-1 procedure carded as positions + confirmation cue, never narration (§12d —
the motion is visible scaffold, the *values* are clozed); P-2 grouped closed set + population;
P-3 threshold with both sides (normal value c1, abnormal conclusion c2); P-4 decision-point
vignette (§12a) — the stem's three-count forces him to *apply* the 2-second threshold rather than
recite it. P-4 is `numeric: true` conservatively since the decision hangs on the verified threshold.
Vignette exemplar (4-year-old) deliberately matches the source's pediatric emphasis.

## Block Q_bleeding_character (idx 70–72) — 3 cards

| Proposition | Where | Class | Disposition |
|---|---|---|---|
| Large vein → steady flow | 70 | MUST | Q-1 (contrast, same c1, per-side `::steady or spurting` per §8) |
| Artery → spurting flow | 71 | MUST | Q-1 + Q-3 vignette |
| Rapid blood loss → shock or death; signs of blood loss | 70/71 ctx | SUPPORTING | Q-1 Pitfall/Ex |
| Unconscious patient → head-to-toe gloved blood sweep, pause to check gloves | 72 | MUST | Q-2 (c1 trigger binary + c2 grouped operational pair) |

**Archetypes:** Q-1 two-sided grouped contrast exactly as the brief specified; Q-2 procedure →
trigger + decidable specifics; Q-3 identification vignette (spurting chef's-forearm cut →
arterial), kept to identification per the brief — no tourniquet/ch26 action, and no "bright red"
color claim (not in this passage).

**Adjudicated warning (the one the checker still prints):** `#19 possible husk` on Q-2's grouped
c2. Cleared: the visible stem ("sweep for blood … gloved hands quickly and lightly") cues both
spans on its own; each span is answerable with the other hidden, so the pair is a grouped
retrieval, not a mutually-dependent husk. Clearance recorded in that card's `verified_by` per
note-format.md; do not split into c2/c3 (a standalone "pausing periodically to ___" card would be
semi-derivable filler).

---

## Flags for Parker (unmarked but exam-adjacent — one line each, per contract; NO cards made)
1. p963: "Perfusion is assessed by evaluating skin **color, temperature, moisture, and capillary
   refill**" — the four-part skin exam as a set is unmarked (the trio version is carded via O-5).
2. p966: skin-temp field technique — back of a gloved hand on the forehead; thermometer during
   vitals is more accurate. Unmarked.
3. p966: hot/cold cause sets are unmarked; carried only as O-2's Distinguish line.
4. p967: capillary refill is chiefly a *pediatric* perfusion check; in adults it is confounded by
   position, age, smoking, meds, cold — and p969 adds "delayed capillary refill is not always an
   accurate indication of poor perfusion, particularly in adult patients." Strong NREMT nugget,
   fully unmarked.
5. p969: abnormal CRT is documented as "delayed" or "CRT > 2" (just past 69's context window).
6. p969: control major external bleeding **before airway/breathing**; direct pressure → sterile
   bandage; tourniquet if pressure fails or obvious arterial extremity hemorrhage. All unmarked
   here (ch26 territory) — flagging because X-before-ABC is heavily tested.

## Margin comments
None on any assigned mark — nothing to honor.

## Editor pass (independent adversarial, 2026-08-29)

Every check run per row on all 21 cards; renders p963/966/967/968/969 read in full. **16 PASS,
5 REWRITE, 0 DROP** — every mark still covered. Numerics re-verified independently on the renders:
`98.6°F (37°C)` verbatim p966; `within 2 seconds` / "say 'capillary refill'" / "CRT as normal
(2 seconds or less)" / "more than 2 seconds or the nail bed remains blanched" verbatim p968.

| Card | Verdict | Reason |
|---|---|---|
| N-1 | REWRITE | **Real cold-solve failure (checks 1/18):** p966's own triad is "cool, pale, clammy," so two bare c1 slots admitted "cool and clammy" as a knower's true answer. Fixed with axis slot-labels `{{c1::pale::color}}` / `{{c1::cool::temperature}}` — forces exactly the marked pair, leaks nothing. Also recorded `verified_against: p963 / verified_by: editor` (all three claims read verbatim on the render this pass). |
| N-2 | PASS | Count in stem, items lead their rows, 2-set load fine. |
| N-3 | REWRITE | c2 was 8 words — R12 threshold; "delicate" is not the discriminator. Now `{{c2::membrane lining the eyelids and eye surface}}` (7 words, both defining locations kept). |
| N-4 | PASS | Sites left visible are the cue (rule 22's classify exemption), taught as the 4-site set in the Cue line; c1/c2 correctly split, no husk. |
| N-5 | PASS | `::cardiovascular cause` does real work walling off the heat causes; Ex line grounded verbatim. |
| N-6 | PASS | Clean two-direction pair (c1 organ, c2 name), each anchored by the other. |
| N-7 | REWRITE | Article moved outside the brace per §4: `is the {{c2::normally white portion of the eye}}` — c2 now exactly 6 plain words. Fold-in target improved for DL; nothing else changed, consolidator's fold instructions still hold verbatim. |
| N-8 | REWRITE | Cue line said "hypoperfusion **means** shock"; book says "is **caused by** shock" — fidelity fix only. Vignette itself passes (fresh exemplar, forced answer). |
| O-1 | REWRITE | Back-Extra label: abnormal-temperature roster is a `Distinguish:` (the values the clozed normal must not blur into, §5), not an `Ex:`. Numeric verified. |
| O-2 | PASS | Closed 3-set, count in stem, `<br><br>` rows; cold/hot cause sets in Distinguish verified on p966 render. |
| O-3 | PASS | Both hints clean; early/late spelling matches. |
| O-4 | REWRITE (micro) | **Moist-echo fix verified held:** row-1 label words {slight, film, sweat, soaked} share nothing with {clammy, damp, moist}; row-2 {bathed, sweat} share nothing with {wet, diaphoretic}. Only edit: stray comma — "wet, or diaphoretic" → "wet or diaphoretic" (book wording). Residual wet-derivability already documented above; load 3+2 per-row-cued, fine. |
| O-5 | PASS | Ordinals printed, content clozed, order IS the marked fact (§7/§12e shape done right). |
| O-6 | PASS | Fresh exemplar, wording distinct from O-4's labels; auto-pair overlap sanctioned. |
| P-1 | PASS | §12d values (grip positions + blanch confirmation cue), motion visible as scaffold. |
| P-2 | PASS | Closed 3-set + `::age group` reverse direction; matches render exactly. |
| P-3 | PASS | "within ___" + unit-inside-cloze self-announces the number (rule 27 exemptions); both numerics verbatim on p968. |
| P-4 | PASS | Decision vignette applying the threshold; forced-choice spelling matches. Cleared the checker's R13 warning on "too slow" (the applied verdict of the verified >2 s rule, a paraphrase not an addition) — clearance recorded in `verified_by`. |
| Q-1 | PASS | Contrast hints match answer spelling exactly ("steady"/"spurting"); entities bold, axis visible. |
| Q-2 | PASS | Concur with the recorded husk adjudication after independent per-span test: "sweep for blood … gloved hands" cues each c2 span with the other hidden. Not re-split. |
| Q-3 | PASS | Buzzword visible, answer clozed, spelling-matched binary hint; no ch26 overreach, no "bright red" invention — confirmed absent from p969. |

Cross-cutting: no front-side cross-card give-aways in the color family (all pale/blue/red/yellow
cross-links live in Back Extras only); four vignette exemplars unique; no absolutes, no bare
unlabeled counts, no value columns, HTML within `<b>/<i>/<br>`; every Back-Extra line labeled and
`<br><br>`-separated. `check_cards.py` after edits: **0 hard errors, stamped**; 2 warnings remain,
both adjudicated on-card (Q-2 husk, P-4 paraphrase).

**For the consolidator:** N-7's Text changed by one word position (`is the {{c2::…}}`) — the DL
sclera fold-in instructions above are unaffected (fold adds `Ex:`/`Formal:` lines + idx 58 only).
N-1 and P-4 `verified_by` now carry editor clearances — preserve them through any merge.

## Housekeeping
- Load check: no group exceeds 4 uncued answers (max used: N-1 c2's closed 4-organ set). No
  chunked sets → no `Roster:` lines anywhere, correctly.
- Sibling-leak sweep: vignette exemplars (motorcyclist, road-race runner, playground 4-year-old,
  chef's forearm) appear nowhere else in the batch.
- Every binary/direction blank carries a forced-choice hint; the two bare numerics carry their
  units inside the cloze and are slot-announced by the stem, so no `::number` hints were needed.
