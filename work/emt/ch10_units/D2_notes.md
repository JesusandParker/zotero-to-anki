# D2 notes — Responsiveness (AVPU) · orientation · spinal immobilization (idx 13–25)

18 notes drafted (21 Anki cards; G1 = 3 clozes, G4 = 2). Margin comments: **none** on any
of idx 13–25 (`user_comment` null throughout) — nothing to honor.

Renders read: p945, p946, p948, p949, p950, p951 (945/949 rendered fresh this run at 170
dpi; the other four already existed). Every card's wording was checked against a render,
so `verified_against`/`verified_by` are filled on all 18 even where `numeric` is false.

---

## Block E_avpu (idx 13, 14, 15, 16, 17) → 6 notes

### Fact pass
| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | AVPU = the four LOC grades: Awake and alert / Responsive to verbal stimuli / Responsive to pain / Unresponsive | 13–16 + shared context | MUST | E1 grouped reveal (membership first, rule 30) |
| 2 | A: eyes open spontaneously as you approach | 13 | MUST | E2 (the A-vs-V pivot) |
| 3 | A: aware of/responsive to environment, follows commands, eyes track people/objects | 13 | SUPPORTING | E2 Back Extra `Distinguish:` (descriptive elaboration of "alert," not a discrete exam fact) |
| 4 | V: eyes do not open spontaneously but open to speech | 14 | MUST | E2 (visible contrast half: "not only when spoken to") |
| 5 | V: meaningful response can be moaning, speaking, or moving | 14 | SUPPORTING | E2 Back Extra `Ex:` — a "for example" list, not a closed set (parker-preferences: don't card open-ended lists) |
| 6 | Responds only to LOUD voice → still (loud) verbal stimuli, i.e. V not P | 14 | MUST | E3 vignette (which-one fact → auto-pair) |
| 7 | P: no response to questions, but moves or cries out to painful stimulus | 15 | MUST | E4 (P criterion) |
| 8 | U: no response spontaneously, to verbal, or to painful stimulus | 16 | MUST | E4 (U criterion, via the flaccid/no-sound observable); names also in E1 |
| 9 | Flaccid, no movement or sound after painful stimulus = unresponsive | 18 context (p949) | SUPPORTING→used | folded into E4 as the U-side observable (that's why E4 cites 18) |
| 10 | Unresponsive → usually no cough/gag reflex → cannot protect airway | 17 | MUST (brief calls it high-yield) | E5 fact + E6 auto-pair vignette |
| 11 | In doubt whether truly unresponsive → assume the worst, treat appropriately | 16/17 context start + p949 render completion | SUPPORTING | E5 Back Extra `Pitfall:`; sentence spans the p948→949 break, so E5 carries `visual_source` p949 |

### Load math (the brief asked for it)
- **Membership (E1):** 4 answers under one c1, each with a first-letter hint. AVPU is a
  spelled mnemonic the book itself teaches (the A/V/P/U letters are printed bold-italic
  beside each level on p945/946/948), so first-letter hints are licensed (rule 18) and the
  group is ≤4 anyway — ships whole. No `Roster:` (set not chunked; SHARED forbids Roster
  outside chunked sets).
- **Per-level definitions:** I built the brief's suggested keyed panel (level → feature,
  4 word-answer rows) and ran rule 20 on each row: the V row ("responsive to *verbal*
  stimuli — responds *when spoken to*") and the U row ("*unresponsive* — *no response*")
  are label-restates-answer tautologies; only the A row (spontaneous eye opening) and P row
  (moves/cries out) survive. So the panel collapses to the two real pivots → carded as two
  contrast cards instead: **E2** (A vs V on the eye-opening trigger, one blank, rule 21(b)
  visible-contrast anchor "not only when spoken to") and **E4** (P vs U on the
  painful-stimulus outcome, 2 blanks, both observables hidden — the level names stay
  visible because the OBSERVABLE CRITERIA are the knowledge; answers add specifics beyond
  the labels, so rule 20 passes).
- **E5:** 2 blanks under one c1 (one causal unit: no cough/gag → can't protect airway),
  each independently cued.

### Judgment calls
- Classify-direction cards ("eyes open to speech = {{V}}") were rejected: AVPU level names
  are their own definitions' keywords (verbal↔spoken-to, pain↔painful stimulus), so
  name-the-level cards decode without knowledge (rule 3). The pivots and observables are
  what get hidden instead.
- E6's stimulus is an **ear-lobe pinch** (from FIGURE 10-9's caption, which sits verbatim
  inside idx 17's context) rather than a trapezius/sternum pinch — deliberately NOT one of
  F1's three answer sites, to avoid leaking F1's rows (rule 13).
- "Assume the worst" Pitfall placed on E5 only (not repeated on E6) to avoid duplicate
  back-lines across siblings; E6's back carries the mechanism chain instead.

---

## Block F_painful_stimuli (idx 18) → 1 note

### Fact pass
| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | Pinch/pressure works best at: sternum, posterior edge of mandible (lower jaw), trapezius area (muscle above collar bone) | 18 | MUST | F1 rows 1–3 |
| 2 | Another effective technique: upward pressure along the orbital rim, underside of eyebrow | 18 | MUST (part of the yellow span — never drop) | F1 row 4 |
| 3 | …without applying any pressure to the eyeball | 18 | MUST-adjacent safety caveat | F1 Back Extra `Pitfall:` (kept visible-side-free because printing it near the blank would decode "orbital rim") |
| 4 | Goal is response/withdrawal, not maximal pain | 18 context | SUPPORTING | F1 Back Extra `Why:` |
| 5 | Note type + location of stimulus and how patient responded | 18 context | SUPPORTING | E4 Back Extra `Cue:` (distributed there so F1 and E4 don't carry duplicate back-lines) |

### Load/shape
4 uncued rows under one c1 — at the rule-23 ceiling, ships whole. Rows 1–3 hinted `::site`,
row 4 `::technique` so the solver knows the fourth answer is a different KIND (fair cold-solve
when all four are hidden). The book's own glosses ("lower jaw," "muscle above the collar
bone") ride INSIDE the clozes — visible they would leak the answers.
The brief's warning honored: FIGURE 10-9's methods (ear lobe / bone above eye / neck
muscles) are **not** carded and not listed on F1's back — the mark is the sites sentence.
The count ("three sites… one further technique") verified on p949 → `numeric: true`.
No auto-pair: sites are a technique list, not a sign/finding/threshold.

---

## Block G_orientation (idx 19, 20, 21, 22, 23) → 5 notes

### Fact pass
| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | Orientation is evaluated next, for alert or verbal-responsive patients | 19 | MUST | G1 c3 |
| 2 | Orientation tests mental status via memory and thinking ability | 20 | MUST | G1 c1/c2 two-way definition |
| 3 | The four things: Person (name), Place (location), Time (year, month, day of week), Event (what happened, MOI/NOI) | 21 | MUST | G2 grouped reveal (closed 4-set, ≤4, ships whole) |
| 4 | Tiers: long-term = person+place; intermediate = place + time(year/month); short-term = time(day of week) + event | 22 | MUST | G3 keyed panel (3 cued word-answer rows — not a value column, rule 25 doesn't apply) |
| 5 | Questions not random; paramount to assess all four | 22 context | SUPPORTING | G2 Back Extra `Why:` |
| 6 | Knows all four = "alert and fully oriented" / "A&O × 4" | 22/23 context | SUPPORTING | G2 Back Extra `Cue:` |
| 7 | Deviation from A&O×4 OR from patient's normal baseline = altered mental status | 23 | MUST | G4 (c1 the finding name; c2 the often-missed baseline branch) |
| 8 | Illness, stroke, TBI, developmental delay, Alzheimer → abnormal baselines exist; determine the normal baseline | 23 context | SUPPORTING | G4 Back Extra `Ex:` + `Cue:` |
| 9 | Apply the deviation rule to a live patient | 23 (finding-rule → profile auto-pair) | MUST (profile §3) | G5 vignette |

### Judgment calls
- The exact tier wording (idx 22's highlight is cut in Zotero) was taken from the p950
  render per the brief and matches the extractor context; the overlap structure (place in
  two tiers, time in two tiers) is the confusing part, so it became G3's `Distinguish:`.
- G3 runs tier→items (production) one-way; the reverse (item→tier) would be a weaker
  3-choice classify and two-waying lists is banned.
- G5 was scrubbed of digits (no fabricated year in the stem) so no un-sourced number sits
  on a card; failure is "cannot tell you the year or what happened" (Time + Event), with
  "normally sharp" establishing the baseline branch.
- MOI/NOI appear inside G2's Event cloze exactly as the book glosses them. Both
  abbreviations are established earlier in his EMT deck; flagged here only in case Parker
  wants "(mechanism/nature of illness)" spelled out.

---

## Block H_spinal_immobilization (idx 24, 25) → 6 notes

### Fact pass (table content read from renders p950+p951 — mark 24 is CAPTION_ONLY)
| # | Proposition | Where | Class | Disposition |
|---|---|---|---|---|
| 1 | Group 1: blunt OR penetrating trauma + any of: pain/tenderness on palpation of neck or spine; patient report of neck/back pain; paralysis or neurologic complaint (numbness, tingling, partial paralysis of legs or arms) | TABLE 10-1, p950 | MUST | H1 grouped reveal (3 rows, class named in stem) |
| 2 | Group 2: BLUNT trauma + any of: altered mental status; intoxication (alcohol or drugs); difficulty or inability to communicate | TABLE 10-1, p950 | MUST | H2 grouped reveal (3 rows, "only when blunt" in stem) |
| 3 | Group 3: distracting injury, by itself | TABLE 10-1, p950–951 | MUST | H3 (name-production; definition on back) |
| 4 | Distracting injury = injury that distracts attention from other injuries, e.g. painful femur/tibia fracture masking neck/back pain | TABLE 10-1 body, p951 | MUST(def) | H3 Back Extra `Meaning:`/`Why:` — see the two-way note below |
| 5 | Which finding-class pairs with which trauma-class (the blunt-only nuance) | table structure | MUST (the decision knowledge) | H6 vignette tests it; H2/H6 `Distinguish:` lines + Rosters teach it |
| 6 | ALL long-bone-fracture + significant-MOI patients warrant spinal immobilization | 25 (Words of Wisdom, p951) | MUST | H4 rule + H5 auto-pair vignette |
| 7 | Why: distracting injuries prevent reliable identification of neck/back pain from an unstable fracture | 25 | SUPPORTING | H4/H5 `Why:` lines |

### Structure (rule 30 membership-first + rule 23 partition)
The 7 indications are chunked along the table's OWN 3-group partition, one note per group
(H1/H2/H3), each stem naming its group, each back carrying the full-set `Roster:` with own
members bold. **No separate anchor note:** the two trauma-class group headers are
distinguishable only by their finding lists, so an anchor hiding both headers would leave
its rows distinguishable by position alone (position-as-cue defect) — and rule 23.1's
anchor exists to test ORDER, which this set doesn't have. The group-membership knowledge
lives in the class-cued stems, and the class-discrimination knowledge is TESTED by H6
(blunt + intoxication + clean exam → still indicated) rather than by an abstract card
clozing summary labels the source never names.
Loads: 3 + 3 + 1 uncued — all within rule 23.

### Judgment calls
- **H3 is one-way on purpose.** "Distracting injury" is self-naming: a two-way definition
  leaks in both directions (term ⊃ "distracts…from other injuries"), like the organ-donor
  v60 failure. The non-derivable fact — that it is BY ITSELF an indication — is the stem;
  the definition rides the back as `Meaning:` (allowed: the front never defines it).
- **H4 clozes the rule's two discriminators** ("long bone," "significant") with the shared
  scaffold visible (rule 18's good shape). Clozing the ACTION instead would have made H4
  and H5 near-duplicates; clozing the whole conditions phrase unanchored would be open-set
  (everything in TABLE 10-1 "warrants immobilization"). The masking clause in the stem
  anchors WHICH rule without containing either answer.
- **H6's stem scrubs competing findings**: "admits drinking heavily" (not "slurred
  speech," which would ambiguously match the communication-difficulty row — rule 2), and
  "alert and fully oriented" rules out the AMS row, so `intoxication` is forced.
- Sibling-leak management (rule 13): H4's back uses the book's **tibia** example, H5's
  vignette uses a **femur** + motorcycle (fresh exemplar); H3's back carries no
  femur/tibia example at all.
- `visual_source` set on H1, H2, H3, H6 (table-derived; pages 950/951 per brief). H4/H5
  derive from idx 25's own text layer → null, but still `verified_against: p951`.
- `needs_table_back` NOT set: SHARED scopes it to rule-25 value columns, and these are
  word-answer sets carried by `Roster:`. **Flag for the figure stage / Parker:** if
  attaching the actual TABLE 10-1 plate to H1–H3 backs is cheap, it would suit his
  part-and-whole preference — say the word and I'll mark them.

---

## Cross-block checks
- **Every yellow span carded** (13→E1/E2, 14→E1/E2/E3, 15→E1/E4, 16→E1/E4, 17→E5/E6,
  18→F1(+E4 back), 19→G1, 20→G1, 21→G2(+G5), 22→G3, 23→G4/G5, 24→H1/H2/H3/H6, 25→H4/H5).
  No span was thin enough to need a `flag_for_parker`.
- **Auto-pairs** (profile §3): E3 (loud-voice which-one), E6 (unresponsive→airway,
  brief-mandated), G5 (AMS finding rule), H5 (long-bone threshold, brief-suggested),
  H6 (table which-one). Vignette share 5/18 ≈ 28% — right for a clinical chapter.
- **Unit boundaries:** idx 12 (bleeding, D1) and idx 26 (airway patency, D3) were read for
  Rule-0 adjacency only — no synthesis crosses the boundary; E5/E6 stand on idx 17 alone.
- **Card count vs the 0.6–1.2/mark band:** 18 notes / 13 marks = 1.38. The overshoot is
  the caption-only table mark (idx 24 → 4 notes, exactly the 3-group set the brief
  prescribes plus its decision vignette) and the three brief/profile-mandated auto-pairs.
  Every note maps to a MUST row above; nothing is coverage padding.
- **Dedupe (rule 12):** E5/E6 and H4/H5 are fact+application pairs (sanctioned), not
  duplicates; no two cards test the same claim in the same direction.
- **Detector clearance (pre-cleared for the gate):** F1 contains the word "above" —
  it is ANATOMICAL ("trapezius area (the muscle above the collar bone)", the book's own
  gloss quoted verbatim inside the hidden cloze), not a source-position artifact. Not a
  Layer-A #2 violation.
- **Unmarked exam-critical content noticed, not carded** (rule 29, one line as permitted):
  p949's Words of Wisdom on hard-of-hearing patients (tap them; note "responds to being
  tapped") and p950's "complete the primary assessment before applying a cervical collar"
  are unmarked but look testable — Parker's call if he wants them.

## Verification record
| Render | Verified |
|---|---|
| p945 | AVPU intro wording; A and V definitions verbatim (E1/E2/E3) |
| p946 | P definition verbatim; SPARSE page confirmed — only the P entry (E1/E4) |
| p948 | U definition + cough/gag/airway sentence verbatim; FIGURE 10-9 caption (E1/E4/E5/E6) |
| p949 | "assume the worst" completion; painful-stimulus sites + orbital rim + eyeball caveat; orientation lead-in/definition; the four things incl. Time = year, month, day of week (F1, E5, G1, G2) |
| p950 | memory-tier sentence verbatim; A&O×4 phrasings; AMS definition; TABLE 10-1 header + groups 1–2 all six findings verbatim (G3, G4, G5, H1, H2, H6) |
| p951 | TABLE 10-1 distracting-injury definition + femur/tibia example; Words of Wisdom long-bone sentence verbatim (H3, H4, H5) |

---

## Editor pass

Independent adversarial pass, every check on every card PER ROW, all six renders re-read
(p945/946/948/949/950/951). Every count re-verified against the page: 4 AVPU levels ·
3 sites + 1 technique · 4 orientation things · 3 memory tiers · 3 + 3 + 1 TABLE 10-1
indications. **Verdicts: 16 PASS · 2 REWRITE (H1, H2) · 0 DROP.** All 13 marks remain
covered; no fact was removed.

| Card | Verdict | Notes |
|---|---|---|
| E1 (AVPU grouped) | PASS | Letter hints licensed: AVPU is spelled bold in the stem AND the book prints the letters beside each level (p945/946/948) — checks 20/25 clean. 4 cued answers ≤ ceiling. Level names verbatim. |
| E2 (A-vs-V pivot) | PASS | Cold-solves: "not only when spoken to" is the rule-21(b) visible-contrast anchor, and the answer carries the book's own "as you approach." Leans easy ("awake" nudges toward the answer) but the visible level name is the required entity anchor, and every alternative shape (classify direction, double-blind contrast) decodes worse via the self-defining level names — adjudicated, keep. |
| E3 (loud-voice vignette) | PASS | Forced-choice `::V or P` present; "groans and stirs when you shout" is not a verbatim reuse of E2's Ex (moaning/speaking/moving) and the tested pivot (loud voice = still verbal) appears on no sibling's visible side. Answer matches p945 wording. |
| E4 (P-vs-U outcomes) | PASS | Both blanks share c1 but each is cued by its own VISIBLE level name — not a husk (rule 17 litmus passes). Answers are the book's observables (moves/cries out · flaccid, no movement or sound, p946/p949). Mild decodability from the level names is inherent to self-defining AVPU vocabulary; the drafter's keyed-panel rejection already litigated this. If `husk_groups` warns: cleared — each blank independently anchored by its level name. |
| E5 (cough/gag → airway) | PASS | One causal unit under c1; both blanks hang off the visible "Unresponsive patients" + "reflex"/"ability to" slots. "assume the worst" completion re-verified on p949 render. If `husk_groups` warns: cleared — shared visible subject cues both. |
| E6 (airway vignette) | PASS | Ear-lobe pinch grounded in FIGURE 10-9 caption inside idx 17's context; deliberately none of F1's sites (rule 13). "Assume he cannot ___::ability lost" is forced by the unresponsive setup + taught implication. |
| F1 (painful-stimulus sites) | PASS | 3 + 1 count verbatim on p949; glosses ride inside the clozes (visible they'd leak); `::site`×3/`::technique` distinguish the kinds. Row-4 span is 13 words — cleared: it is the book's own single technique phrase, one retrieval chunk, and any shorter cloze leaks the location. |
| G1 (orientation 2-way + when) | PASS | c1/c2 is the licensed two-way definition (visible meaning on the c1 card is NOT a leak, rule 3 precision); c3 (which grades) independently cued. `::what you evaluate` hint is redundant-but-harmless slot label. |
| G2 (four things) | PASS | All 4 items + glosses verbatim vs p949 render (Time = year, month, day of week; Event = MOI/NOI). 4 uncued = at ceiling, ships whole. Long row spans (item + gloss) cleared — grouped-list rows carry the gloss inside by design. |
| G3 (memory tiers) | PASS | Tier mapping verbatim vs p950; 3 keyed word-answer rows (not a value column, rule 25 N/A); overlaps (place ×2, time ×2) break elimination and are taught in Distinguish. |
| G4 (AMS definition) | PASS | c1 anchored by `::finding`; c2 ("normal baseline") forced by the parallel "deviation from A&O×4 — or from the patient's own ___" frame; on the c2 card the finding name is visible as contrast. If `open_set_absolute` warns on c2: cleared per that structure. |
| G5 (AMS vignette) | PASS | Single decision, forced-choice `::altered or normal`; fails Time + Event with baseline established — fresh exemplar, spelled on no sibling; no fabricated digits. |
| H1 (blunt-or-penetrating 3) | REWRITE | Roster complete (3/3 verbatim vs p950; full 7-item Roster on back). Stem lacked the table's own "with ANY of the following" OR-logic — the decision-critical fact (one finding suffices). Stem now reads "Three findings (any one alone is enough) indicate…". Headers cue disjoint lists: AMS/intox/communication are logically excluded here because they do not indicate after penetrating trauma. |
| H2 (blunt-only 3) | REWRITE | Same fix, same reason: "(any one alone is enough)" added. "Only when blunt" + finding lists keep the two class cards mutually cold-solvable; 3/3 verbatim vs p950. |
| H3 (distracting injury) | PASS | One-way is right (self-naming term; two-way would leak both directions). "By itself" grounded in the table's three-OR-group structure (own unheaded row, p950–951) — the same reading the brief and fact pass reached independently. |
| H4 (long bone + significant MOI) | PASS | Both discriminators hinted (`::fracture type`, `::MOI qualifier`), scaffold visible — rule 18's good shape; WoW sentence verbatim p951. NB the fact-pass note "H4's back uses the book's tibia example" is stale — H4's back carries no tibia, which is fine (less sibling-leak surface). |
| H5 (motorcyclist vignette) | PASS | Fresh exemplar (femur + motorcycle; the book's femur/tibia parenthetical is quoted verbatim nowhere in the batch); one crisp verb+object cloze; denial-of-pain discriminator forces the answer. |
| H6 (intoxication decision) | PASS | Forced-choice `::is / is not`; stem scrubs confounders (drinking ≠ slurred speech; "alert and fully oriented" kills the AMS row; group-1 findings explicitly negated) so intoxication is the only live indication. Table-grounded p950. |

Editor's cross-checks: scrutiny (a) letter-hint license CONFIRMED (AVPU spelled in E1's stem);
(b) H1/H2/H3 rosters complete and identical, 7/7 vs render, own members bolded; (c) all five
vignettes fresh-exemplar and single-decision; (d) E2/E4 pivots cold-solvable with no
tested-blank mutual leak (V's eye-opening criterion and P's precondition appear visible but
are answers nowhere); (e) every count/digit matches the renders. No card states a dose or
threshold; all `numeric: true` cards carry `verified_against`/`verified_by` so the safety
flag derives correctly.

**check_cards.py after edits: 0 HARD errors, stamped OK.** 6 warnings, all adjudicated
false-positive and cleared — clearance recorded in each card's `verified_by`, naming the
detector (note-format.md convention):
- E1 ×2 `first_letter_hint` (::A/::U): AVPU is spelled bold in the stem; the detector
  missed the acronym token. Rule 18 license holds (V/P key the discriminating word, so
  only A/U literally matched).
- E4 + E5 `husk_groups`: each blank independently cued with the other hidden (visible
  P/U level-name anchors; visible "Unresponsive patients" subject + slot frames).
- G3 undercount ("four … clozes only 3"): "four" counts the QUESTIONS (visible anchor);
  the clozed list is the three TIERS, 3/3 vs the p950 render.
- H6 `visible_answer` ('is'): the forced-choice hint displays "is / is not" by design
  (licensed exception); the stem's "is pulled" is an incidental function word.
