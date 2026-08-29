# D4 notes — Circulation: pulse & CPR/AED decisions (idx 41–49, p958–963)

11 notes drafted: 4 in L_pulse_sites, 7 in M_cpr_aed. No margin comments exist in this
range (`user_comment` is null on all nine marks). Boundary check done: idx 40 (TABLE 10-2,
respiratory distress/failure) and idx 50 (skin condition) open the neighboring units'
topics — no Rule-0 adjacency crosses my boundary in either direction.

## Block L_pulse_sites (idx 41, 42, 43, 44)

### Fact pass

| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | Pulse = the pressure wave each heartbeat's surge sends through the arteries | 41 (highlight) | MUST | L1, two-way definition (c1 term / c2 meaning) |
| 2 | Heartbeat = ventricular contraction forcefully ejecting blood | 41 context (unmarked) | SUPPORTING | L1 `Distinguish:` |
| 3 | Pulse point = major artery near surface, pressed gently against bone/solid organ | 41 context (unmarked) | SUPPORTING | L1 `Cue:` |
| 4 | Responsive, >1 yr → radial pulse at wrist | 42 (highlight) | MUST | L2 row 1 |
| 5 | Unresponsive, >1 yr → carotid pulse at neck | 42 (highlight) | MUST | L2 row 2 |
| 6 | <1 yr → brachial pulse, medial (inside) upper arm | 43 (highlight) | MUST | L2 row 3; re-tested in L4 vignette |
| 7 | In infants, radial and carotid pulses are difficult to locate | 43 context (Special Populations box, unmarked) | SUPPORTING | L2 `Why:`, L4 `Why:` |
| 8 | Supine infant: access brachial by elevating arm over the head | 44 (highlight) | MUST | L3 |
| 9 | Chubby arms → press adjacent fingertips firmly along artery (parallel to long axis) | 44 context (unmarked) | SUPPORTING | L3 `Cue:` |
| 10 | Never palpate with your thumb (its own pulse mimics the patient's) | 43/44 context (unmarked) | SUPPORTING | L2 `Pitfall:` |
| 11 | Hold index + long fingers together over the pulse point, press gently | 41/42 context (unmarked) | SKIP | Unmarked technique detail; not carded (see flags) |

### Archetypes & judgment calls
- **L1 — §4 two-way definition.** Both directions are real: the mark's own point is that
  "heartbeat" is the loose word and "pressure wave" the true nature; describe→name and
  name→define both earn a card. Kept the c2 deletion to the crisp discriminator ("the
  pressure wave"), not the whole clause (rule 5). Reworded the visible tail to "sent
  through the arteries by each heartbeat" so the stem's word "surge" does not echo the
  hidden answer "wave" (rule 3 leak trim).
- **L2 — §12(b) decision table, 3 cued rows, one c1 group.** Word answers keyed by
  condition; load = 3 cued answers (≤4, legal). The brief blessed a 4-row version
  including the elevate-arm technique; I split that 4th row out (L3) because it answers a
  different question (how to access, not where), and the 3-row table is the purer
  responsiveness × age decision. Row-level cold-solve run: no row label restates its
  answer (#20); each condition forces exactly one site. **Anatomic locations ride INSIDE
  each cloze** ("radial (at the wrist)") — left visible they would decode the artery name
  (wrist → radial is basic anatomy).
- **L3 — scenario→action, crisp action cloze** with a slot-label hint (`::arm maneuver`)
  guarding the open-action blank (#16/#21). The full maneuver stays in one cloze because
  "elevating the arm" with "over the head" visible would be decodable.
- **L4 — auto-pair vignette** (SHARED mandates the pair for a "which one" fact). Targets
  the trap cell of the table: unresponsive + under 1 yr → brachial, NOT carotid. Fresh
  exemplar (limp 7-month-old handed over by mother) — no sibling carries any exemplar
  (#13 clean). The 7-month age is my scenario construction sitting below the verified
  1-year threshold, not a book value, so `numeric: false` with the threshold's
  verification recorded.
- The 1-year threshold itself is drilled as a visible KEY in L2 and forced in application
  by L4, not clozed anywhere — a table key is cue, not answer (§12b), and a
  "site → which patients" reverse card would drill a direction the field never asks.

## Block M_cpr_aed (idx 45, 46, 47, 48, 49)

### Fact pass

| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | No palpable carotid in unresponsive patient → begin CPR | 45 (highlight) | MUST | M1 fork row 1; applied in M6 vignette |
| 2 | AED available → turn it on, follow voice prompts, per local protocol | 46 (highlight) | MUST | M1b (both spans under one c1) |
| 3 | AED indication = assessed unresponsive AND pulseless | 46 context (unmarked) | SUPPORTING | M1b `Why:`, M5 `Distinguish:`, M6 `Why:`; stem framing on M1b |
| 4 | Pulse present but not breathing → provide ventilations | 47 (highlight) | MUST | M1 fork row 2; visible framing on M2/M3/M4 |
| 5 | Adult rescue-ventilation rate 10–12 breaths/min | 47 (highlight) | MUST | M2 (per-key note) |
| 6 | Infant/child rescue-ventilation rate 12–20 breaths/min | 47 (highlight) | MUST | M3 (per-key note) |
| 7 | Monitor pulse every 2 min to evaluate ventilation effectiveness | 48 (highlight) | MUST | M4 |
| 8 | Patient becomes pulseless → start CPR and apply the AED | 47/48 context (unmarked) | SUPPORTING | M4 `Why:`, M2 `Pitfall:` |
| 9 | Never begin CPR / use AED on a responsive patient; apparent pulselessness there ≠ cardiac arrest | 49 (highlight) | MUST | M5 negation |
| 10 | With practice you can judge slow/fast/irregular without counting | 49 context (unmarked) | SKIP | Unmarked; belongs to the pulse-quality discussion, not carded |

### Archetypes & judgment calls
- **M1 — §12(b) two-row decision fork (Rule-0 synthesis of 45 + 47).** The passage's real
  structure is one fork on the pulse in an unresponsive patient: pulseless → CPR, pulse
  but apneic → ventilations. Carding 45 alone would have left "provide ventilations"
  forever visible-but-untested (#7 under-clozing). Two cued word answers under one c1;
  both rows pass the row-level cold-solve and #20.
- **M1b — the AED handling card (46).** Restructured "turn it on and follow the voice
  prompts" so the crisp nouns are the recall ("follow its ___" / "consistent with your
  ___") instead of hiding a whole action clause (#5, #15). Two independently cued spans,
  one group. The stem's "unresponsive, pulseless" framing comes from 46's own context
  sentence (permitted framing).
- **M2/M3 — the ventilation rates, ONE NOTE PER KEY** per SHARED's #25 clause (a value
  column keyed by age). Two keys → two notes; `numeric: true`; range verified verbatim on
  the p962 render. Rule 27: the visible "breaths/min" immediately after each blank
  announces the numeric slot, so no hint. **`needs_table_back` NOT set:** these rates
  live in running prose on p962 — no TABLE plate exists for the figure stage to attach —
  so the whole-set-in-view duty is carried by a `Roster:` line on each note (own member
  bolded), per rule 25's no-table fallback.
- **M4 — the every-2-minutes recheck (48).** Interval clozed, purpose visible; unit
  follows the blank (#27 satisfied). The becomes-pulseless consequence (unmarked context)
  is its `Why:`.
- **M5 — §10 negation (49).** Negator bold and visible; the unsafe population is the
  cloze, carrying the mandatory forced-choice hint (`::responsive/unresponsive`, rule 4)
  and anchored per #21 by the visible reason-contrast ("apparent pulselessness in that
  patient is not cardiac arrest") plus the `Distinguish:` line naming the licensed
  opposite state (unresponsive AND pulseless).
- **M6 — brief-mandated auto-pair vignette forcing the CPR-start decision.** One stem,
  one cloze; fresh exemplar (58-year-old gym collapse; no sibling uses an exemplar).
- Sanctioned same-fact pairs (profile auto-pair, not rule-12 duplicates): fork row 1 ↔ M6;
  L2 row 3 ↔ L4. Also noted: M2/M3 stems necessarily display fork row 2's answer
  ("ventilations") as framing — inherent to the per-key split; the fork still tests it
  when it comes up shuffled.

## Verification log (every number/threshold read verbatim off a render)

| Value | Card(s) | Render | Verbatim source line |
|---|---|---|---|
| "older than 1 year" ×2, radial/wrist, carotid/neck | L2, L4 | p958 | "In responsive patients who are older than 1 year, palpate the radial pulse at the wrist… In unresponsive patients older than 1 year, palpate the carotid pulse in the neck" |
| "younger than 1 year", brachial, medial (inside) upper arm | L2, L4 | p961 | "Palpate the brachial pulse, located at the medial area (inside) of the upper arm, in children younger than 1 year" |
| elevate arm over infant's head (supine) | L3 | p961 | "With the infant lying supine, you can access the brachial pulse by elevating the arm over the infant's head." |
| 10 to 12 breaths/min (adults) | M2 | p962 | "provide ventilations at a rate of 10 to 12 breaths/min for adults" |
| 12 to 20 breaths/min (infant or child) | M3 | p962 | "and 12 to 20 breaths/min for an infant or a child" |
| every 2 minutes | M4 | p962 | "Continue to monitor the pulse every 2 minutes to evaluate the effectiveness of your ventilations." |
| begin CPR trigger / voice prompts / local protocol | M1, M1b, M6 | p962 | "If you cannot palpate a carotid pulse in an unresponsive patient, begin CPR. If an automated external defibrillator (AED) is available, turn it on and follow the voice prompts, following your local protocol." |
| never CPR/AED on responsive | M5 | p962→p963 | "The apparent absence of a palpable pulse in a responsive patient is not [p963:] caused by cardiac arrest. Therefore, never begin CPR or use an AED on a responsive patient." |

`verified_against`/`verified_by` are recorded on every card whose content I confirmed on a
render (non-numeric ones included, as provenance); `numeric: true` only on L2, M2, M3, M4.
`visual_source` is null throughout — every carded fact lives in the marks' own text-layer
`context`; renders were used to VERIFY wording, not to extract facts.

## Rule-14 check on idx 46 (`list_lead_in: true`)
Read the full p962 passage on the render: the AED sentence is followed by continuous
prose ("An AED is indicated… More information… in Chapter 14"), **no enumerated list**.
The lead-in flag is a false positive (likely tripped by "following your local protocol").
No count committed anywhere on M1b.

## Checker run & warning adjudication
`check_cards.py` on this file: 11 cards, 0 hard errors, 1 warning. The warning
(`open_set_absolute` on M6, the CPR-start vignette) is a false positive: the trigger word
"cannot" sits inside the vignette's clinical findings ("you cannot palpate a carotid
pulse"), not in a prohibition the card states, and the discriminating stem
(unresponsive + pulseless) forces exactly one action — the exact fix #16 prescribes.
Cleared per note-format.md convention: the clearance is recorded in M6's `verified_by`,
naming the detector. No hint added — "What do you do first?" already announces the
answer's form, so a `::next step` hint would be redundant.

## Flags for Parker
- **Unmarked but exam-critical, used only as Back-Extra support (say the word if you want
  any as its own card):** (1) "An AED is indicated for use on patients who have been
  assessed to be unresponsive and pulseless" (p962); (2) "If the patient becomes
  pulseless, start CPR and apply the AED" (p962); (3) the never-use-your-thumb palpation
  warning (p961); (4) "hold index and long fingers together over a pulse point, press
  gently" technique (p958); (5) pulse-quality-without-counting paragraph (p963, top).
- No `flag_for_parker` cards: no yellow span in this range was thin enough to need one —
  all nine marks carded cleanly.
- No margin comments to honor in idx 41–49.

## Editor pass

Independent adversarial pass, full checklist run per row, all four renders re-read
(p958/p961/p962/p963). Every load-bearing value re-verified verbatim on the renders:
10–12 adult / 12–20 infant-or-child breaths/min, the every-2-minutes recheck, both
1-year threshold sentences, the elevate-arm access, and the never-CPR/AED-on-responsive
sentence spanning p962→963. **Verdicts: 7 PASS, 4 REWRITE (all Back-Extra-level; no
cloze structure changed), 0 DROP.** All nine marks still covered; `check_cards.py`
re-run after edits: 11 cards, 0 hard errors, 1 warning (the previously cleared
`open_set_absolute` on M6 — clearance re-affirmed, recorded in its `verified_by`).

| Card | Verdict | Notes |
|---|---|---|
| L1 pulse two-way def | REWRITE | Cue line's dangling "feel it" → "feel the pulse" (Layer A #2). Both directions cold-solve; c2 "the pressure wave" is crisp (3 words); no echo of "wave/pressure" on the c2 front; the c1 front's "often called a heartbeat" cues without stating — sanctioned two-way shape, not a leak. |
| L2 3-row decision table | PASS | Row-level cold-solve clean: each condition forces exactly one site, no label restates its answer (#20/#22 — condition→action is the sanctioned table shape), 3 cued answers ≤4 (#25), word answers so no interpolation (#27). Site+location under one blank verified as the right call — "at the wrist" left visible would decode "radial." Verified p958/p961. |
| L3 supine arm maneuver | PASS | Open-action blank guarded by the `::arm maneuver` slot-label (#18/#23); 6-word cloze is recallable and can't be split without a giveaway tail ("over the infant's ___"). Grounded p961 verbatim. |
| L4 7-month-old vignette | PASS | Fresh exemplar (mother/limp 7-month-old appears nowhere else); #16 interrogated hard: L3's visible stem does pair "infant" with "brachial," but the pairing IS the tested rule itself (age trumps responsiveness), the exemplar is not reused, and the L2-row-3↔L4 pair is the profile-mandated auto-pair. The 1-year threshold is genuinely produced-from-memory here (not visible in the stem), which closes the "threshold never clozed" question. |
| M1 unresponsive fork | PASS | Both rows cold-solve; row 2 ("not breathing → ventilations") probed as a possible #20 freebie — verdict: condition→action relation, not a paraphrase (the load is assigning CPR vs ventilations-only to the right pulse state, and both rows blank together). 2 cued answers. |
| M1b AED voice prompts | REWRITE | The Why line restated the stem's own "unresponsive, pulseless" framing (check 11 fail — padding). Replaced with a real edge: indication requires the patient be already *assessed* — "the pulse check comes before the machine" (grounded in p962's "have been assessed to be" plus the passage's own order). Cloze pair kept: two independent crisp nouns, no husk (#19), "local protocol" is the book's stock collocation — forced for a knower. |
| M2 adult 10–12 | REWRITE | Pitfall opened "these breaths" (Layer A #2 line-initial deixis) → "rescue ventilations." Unit sits directly after the blank (#29 satisfied, no hint needed); no neighbor value anywhere on the front; Roster on the back is rule 25's sanctioned no-table fallback (p962 re-checked: rates are running prose, no plate exists). |
| M3 infant/child 12–20 | REWRITE | Cue's "share this one range" deixis → "share a single range" (Layer A #2). Same per-key hygiene as M2; fronts leak nothing across the pair. |
| M4 2-minute recheck | PASS | "minutes" after the blank announces the numeric slot (#29); purpose clause left visible judged correct — it is the situational anchor, and the actionable consequence (pulseless → CPR + AED) is the Why line. Verified p962. |
| M5 never-CPR/AED negation | PASS | Anchored twice per rule 21: forced-choice `::responsive/unresponsive` hint AND the visible reason-contrast ("apparent pulselessness … is not cardiac arrest" — the endorsed 21(b) shape, an anchor, not a leak). Negator bold and un-clozed (§10). "Not cardiac arrest" deliberately not made a c2: it would re-drill the same discrimination in reverse (rule 8's both-directions bar not met). |
| M6 CPR-start vignette | PASS | Fresh exemplar (58-yo gym), single decision, state forces "Begin CPR." The `open_set_absolute` warning re-adjudicated independently: false positive — "cannot" is a finding in the stem, not a prohibition; clearance already recorded in `verified_by`, kept. Why line states the general rule the stem only instantiates — additive for a vignette (recipes §9's own pattern), not a restatement. |

For the consolidator: (1) the sanctioned same-fact pairs stand — M1-row-1↔M6 and
L2-row-3↔L4 are profile auto-pairs, and M2/M3 stems necessarily display "ventilations"
(fork row 2's answer) as framing — do not "fix" any of these as duplicates or leaks.
(2) M6's checker warning is cleared, twice now; do not add a hint to it. (3) No table
plate exists for the ventilation rates (running prose on p962) — the Roster lines are
the rule-25 fallback, deliberate. (4) `needs_human_check` is derived, not asserted:
all four numeric cards carry `verified_against`/`verified_by`, so `verify_report.py`
will route them to the verified-skim section.
