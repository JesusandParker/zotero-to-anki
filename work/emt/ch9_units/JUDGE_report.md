# JUDGE report — EMT Chapter 9 final batch (21 cards)

Independent whole-batch judge pass (Stage 2.75 step 2), 2026-08-29. Full editor checklist run
on every card; checks 18–24 run on every ROW (card 3's three name rows, card 8's four element
rows, card 13's four letter rows + pre-step, card 19's five step rows). Grounding spot-checked
word-for-word against the cited marks' highlight/context on cards 0, 1, 2, 4, 5, 6, 8, 12, 13,
18, 19, 20 (12 cards — every cloze answer verbatim or verbatim-close in its cited mark; no
fabrication found anywhere). Cross-checked the final file against the four `E_of_D*_cards.json`
editor outputs field-by-field and against `dropped.jsonl` / `decisions.jsonl`.

**Verdicts: 17 PASS · 4 FIX · 0 KILL.**

---

## Per-card verdict table (0-based file order)

| # | Block | Verdict | Detail |
|---|-------|---------|--------|
| 0 | A_just_culture | **PASS** | Fresh cold-solve of c3 ("encourages people to ___"): **forced, not open-set**. The entity is named ("Just culture" visible on the c3 face) — this is the definitional completion of a named concept, R9's own "name the entity that makes the answer inevitable" fix built in; error/near-miss reporting is the concept's signature feature, and nothing visible states or echoes it (knower-can / non-knower-can't holds). Independent concurrence with the D1 editor's logged ruling. All Back Extra lines verbatim-grounded in idx 0's context. |
| 1 | B_continuum_of_care | **PASS** | Fresh cold-solve of c3 ("…improving performance, safety, and ultimately ___"): **forced**. The rising ladder + "ultimately" + the chapter's own drumbeat (best possible patient outcome) converge on exactly "patient outcomes"; the "improving ___" frame rejects the shared-goal card's fuller phrase, so no interference. I independently raised the check-4 question (performance/safety visible-untested) and then found the D1 editor's SUSTAINED ruling; on the merits I concur — clozing all three benefits trades one forced blank for three semi-open ones (R9 precision: the defect is an *open* answer-space, not a *hard* one; rule 5: fuzzy multi-word phrases; `list_lead_in: false` — rhetorical prose, not the v60 lobes closed set). Spared, see batch section. |
| 2 | C_group_vs_team | **FIX** (metadata; Text untouched) | `"needs_human_check": false` → `"needs_human_check": true`. The D1 editor OVERTURNED this flag to true (safety overlay: idx 3 is extractor-marked `grounding: PARTIAL` — mechanical, "regardless of the verdict") and `E_of_D1_cards.json` carries `true`; **the consolidated file reverted it to `false` while keeping the verified_by sentence that documents the flip**. Restore the editor's value and append to verified_by: "judge: restored needs_human_check=true — the consolidation had silently reverted the editor's logged safety-overlay flip (PARTIAL-grounded idx 3)." Craft itself all passes: R10 contrast shape cleared per cloze number (entity anchors visible, uncued load 2 ≤ 4 on the c2 face), c1 menus match answer spelling exactly. |
| 3 | D_group_types (anchor) | **PASS** | 3 uncued ≤ 4; closed taxonomy (R9 must-not-over-flag); stated count 3 = 3 rows = the source's full set (check 17); rows `<br><br>`; editor's classifying-axis anchor resolves the three-types collision with the MCI functional groups. Back-side Cue/Pitfall exposure of sibling answers is the adjudicated part-and-whole class (decisions #4's logic; rule 25's back-restatement ban is numeric-columns only). Pitfall's fold of the dropped card's teaching verified verbatim against idx 6. |
| 4 | D_group_types (dependent) | **FIX** (minor, article leak) | Old: `In a {{c1::dependent::group type}} group, each member is {{c2::told what to do}} by the group leader.` → New: `In {{c1::dependent::group type}} groups, each member is {{c2::told what to do}} by the group leader.` Why: on the c1 face, the visible article "a" admits only the consonant-initial member of the three-type roster — a roster-knower decodes "dependent" by grammar alone, without the description (rule 3's crutch side / non-knower-can-decode). The plural is the **book's own syntax** ("In dependent groups, each individual is told…"), so the fix is zero-cost and restores source wording. c2 face unaffected. |
| 5 | D_group_types (independent) | **FIX** (minor, same class as #4) | Old: `In an {{c1::independent::group type}} group, each member is responsible for {{c2::his or her own area}}.` → New: `In {{c1::independent::group type}} groups, each member is responsible for {{c2::his or her own area}}.` The "an" eliminates "dependent" from the roster for free (weaker than #4's leak but the same shape); book's own syntax again ("In independent groups, each individual is responsible for…"). |
| 6 | E_team_elements (shared goal) | **PASS** | Confusable-menu hint adjudicated (decisions #2 + logged verified_by) — no new evidence; fresh check confirms the menu does real work (p874's "quality patient care" genuinely fits the frame cold) and the Pitfall pins the discrimination post-answer. "One of the five" is scene-setting, not an enumeration promise (no R7 undercount). Hint distractor and Pitfall grounded verbatim in idx 1's context. |
| 7 | E_team_elements (clear roles) | **PASS** | Editor's one-way collapse sustained on fresh read: the dropped c1 pair were near-synonyms *of each other* (R12 in paired form); kept face cold-solves (description = cue, rule 22's not-a-violation classify shape); "one of the five essential elements" frame names the slot's category, no hint needed. |
| 8 | F_team_communication (four elements) | **PASS** | 4 uncued = at rule-23 cap; stated count = rows = the source's full list (check 17); rows `<br><br>`; all four answers verbatim from idx 9–13. The Meaning gloss spelling sibling card 9's c2 answer on the back is the explicitly adjudicated exposure (decisions #4 names this exact card). No letter hints despite all four starting with C — correctly resisted. |
| 9 | F_team_communication (constructive intervention) | **PASS** | Two-way def; c2 "respectfully question or correct" 4 words crisp, forced by the mistake-situation + "even the team leader"; c1 face is the licensed describe→name direction. Roster + definition family with card 8 is R2-legal (membership vs meaning). |
| 10 | G_team_leader (definition) | **PASS** | Describe→name one-way; five functions visible as the cue — recognition-level by deliberate, logged choice (D2 editor: every produce-the-list shape is barred or bad under rules 23/24; hand-off note to Parker already recorded — carry it forward, see hazards). Distinguish tail's grounding via adjacent idx 9's context (rule 11 license) verified by the D2 editor; concur. |
| 11 | G_team_leader (commands) | **FIX** (minor, article leak — same class as #4/#5) | Old: `…he or she is merely directing a {{c1::dependent group::group type}}.` → New: `…he or she is merely directing {{c1::a dependent group::group type}}.` Folding the article into the cloze kills the a/an elimination cue at zero wording cost (the answer simply picks up its own article). Not a duplicate of card 4: definition vs leadership-failure classification — distinct claims, fresh wording, reasoning not pattern-match (D2 editor's distinction sustained; decisions #6 covers the Why-line overlap). |
| 12 | H_closed_loop | **PASS** | Two-way def; c2 = 6 words, defining action, forced. Ex dialogue re-verified word-for-word against idx 15's highlight (the editor's restoration held through consolidation). Membership-vs-definition split with card 8's row is legal. `numeric: true` for the Ex's liter digits is the asserted-flag lane (R51), correctly left to verify_report derivation. |
| 13 | I_pace (expansion + pre-step) | **PASS** | **Fresh honest cold-solve of c2 "get the attention of the crew member":** solvable. On the c2 face the four PACE contents sit visible, closing off every competing candidate action (probe/alert/challenge/emergency are all *taken*); the slot is specifically "the pre-mnemonic step," and the protocol teaches exactly one; "First ___, then use the mnemonic" is the book's own sequencing frame; the tested discrimination (crew member's attention first, though the *problem* is bound for the team leader) is real knowledge, and a paraphrase ("get their attention") is the same answer. 7 words but load-bearing verb+object (rule 15). Concurs independently with the D3 editor's ruling. c1 letter hints licensed — PACE spelled and bolded in the stem (R11's one license). Rows `<br><br>`; count stated = 4 = rows. |
| 14 | I_pace (Alert vs Emergency) | **PASS** | R10 judge-cleared contrast: entity anchors visible, both blanks menu-forced with exactly-matching spelling. The answer-by-elimination property once one side is known is inherent to any 2×2 contrast (the endorsed cover/concealment exemplar has it) — spared. |
| 15 | I_pace (Challenge) | **PASS** | Row-label check (20/22): the *blank* ("suggest an alternative plan") is what the visible "challenge…" scaffold does NOT say; the restated scaffold is visible anchor, not the answer — rule 18's exposed-shared-structure side. Ex verbatim. Card 13's back gloss spelling this answer = adjudicated exposure class. |
| 16 | I_pace (leader broadcasts) | **PASS** | `::role` slot; anchored; the genuine competing answer (the challenging crew member) is exactly what the card discriminates against — knower-certain, non-knower-not. "to everyone on the team" left visible-untested is a deliberate spare: the Distinguish line carries that edge, and a third "entire team"-shaped blank would compound interference with card 14. Distinct from L step 4 (decisions #5). |
| 17 | J_prearrival | **PASS** | "mentally rehearse" 2-word crisp; the object "the steps in the care that may be needed" + singular-EMT subject force a rehearse-verb (crew-level alternatives don't take that object) — D4's open-set guard verified. Prearrival deliberately not clozed (en-route would decode it — freebie). Back Extra invents no ratio. |
| 18 | K_rows | **PASS** | Licensed mnemonic direction (acronym visible, expansion hidden — the SAMPLE shape); expansion simultaneously the marked first-priority behavior. Reverse direction correctly skipped (first-letters derivable = freebie). Sparse-page grounding handled by orchestrator render, logged; grounding EXACT so no overlay flag. Anchoring cross-link on the back grounded in sibling mark 24 (decisions #3). |
| 19 | L_decision_process | **PASS** — **step_recitation CLEARED** (ruling below) | 5-item group under rule 23's causal-chain license: adjudicated (D4_notes.md + verified_by), not re-litigated — and on fresh row-level cold-solves the license holds (cover row 3: "1. Gather data, 2. Interpret that data, 3. ___" regenerates "Develop a plan" from the chain, not from position). Stated count 5 = rows = the source's printed 1–5 (check 17). Ordinals printed, never clozed. Rows `<br><br>`. All five answers verbatim from idx 19–23. Back Extra Ex faithfully compresses the book's chest-discomfort example. |
| 20 | M_decision_traps | **PASS** | Two-way def; `::decision trap` is the book's own category word; c2's two crisp spans reveal together with the term as anchor (no husk); "sometimes before the call" correctly exiled to the back (would decode "early"). Overconfidence held to Distinguish-only (rule 29). The classify-vignette skip is right — the only grounded exemplar is already spent as the Ex, and reuse would be the exact R6 failure. |

---

## Ruling on the step_recitation warning (card 19) — **CLEARED**

Sentence to record in `verified_by`:

> judge: step_recitation CLEARED — §12e step-scaffold on a cognitive decision sequence, not a
> psychomotor narration: the ordinals are printed and never clozed, each blank is cued by the
> chain's input→output logic (data → interpreted meaning → plan → communicated/implemented plan
> → observed effect) rather than by bare position, the sequence itself is the marked knowledge
> (Parker highlighted all five lead-ins, Rule 0 connected set), and R30's preferred vignette
> shape is already served by the Ex's evaluate-step rehearsal; rule 23's causal-chain license
> for the 5-item group stands as adjudicated in D4_notes.md.

Reasoning: R30 is a deliberate warning-not-block because "a short ordered protocol whose order
genuinely is the knowledge is legitimate" and only the judge can tell it from a recitation. This
card is the licensed case on every axis R30 measures: (1) it is a *thinking* loop, not a motion
— nothing here narrates a psychomotor step (the class the AnKing evidence shows is never
narrated); (2) no blank's only cue is its ordinal — the chain regenerates each member (the exact
"structure that regenerates the members" handle rule 23 names); (3) the decision-table shape is
inapplicable (no conditions) and a fresh order-vignette would require an invented scenario (the
book's sole example is spent, grounded, as the Ex — reusing it in a vignette would be an R6
self-leak); (4) the D4 drafter surfaced the judgment call honestly rather than burying it —
R25c's behaviour-to-reinforce. Uphold would require evidence the card is unpassable or
position-cued; fresh row-level cold-solves show the opposite.

---

## Batch-level findings

### Cross-card checks (the whole-batch work the per-batch editors could not do)

- **Check 16 across all 21:** no scenario/classify card's stem reuses a sibling's Ex line or
  definition wording verbatim. Card 11's "simply commands others" appears on no sibling's back;
  card 9's mistake-situation is the definition's own trigger, not a borrowed exemplar. Clean.
- **Dedupe by meaning across units:** the two near-collisions flagged at unit level were both
  resolved correctly downstream — (a) B's "patient outcomes" vs E's "the best possible patient
  outcome" (decisions #2: distinct facts, menu-discriminated; the "improving ___" frame also
  grammatically rejects E's phrase); (b) C's team content vs the D trio — resolved by the
  consolidation's drop+fold of the redundant interdependent card (dropped.jsonl), with mark 6
  still cited by cards 3 and 5, so no mark lost coverage. Closed-loop and constructive
  intervention each get exactly one membership row + one definition card (R2-legal families).
- **Interference between similar answers (watch, no action):** "team leader" answers three cards
  (10 definition, 14 Alert-audience, 16 broadcast-role) and "dependent (group)" answers two (4,
  11). Claims are distinct and the stems are not mutually confusable; if any shows up in Card
  Feedback, the first lever is a Distinguish cross-link, not a merge.
- **Mark coverage:** union of `from_idx` across the batch = 0–24 complete. Every one of Parker's
  25 marks is cited by at least one shipped card. No authorization-lane cards; no synthetic marks.
- **Consolidation reconciliation (R27a-class check):** field-level diff of the final file against
  the four editor outputs shows exactly two divergences — card 3's documented Back-Extra fold
  (logged in verified_by + decisions.jsonl; legitimate) and **card 2's `needs_human_check`
  reversion (the defect fixed above)**. 22 editor cards − 1 logged drop = 21 shipped. Nothing
  else drifted.

### Over-flag candidates deliberately spared (with the precision that spares each)

1. **Card 1's visible benefits ladder** ("performance, safety" untested) — spared by R9's
   MUST-NOT-OVER-FLAG (the defect is an *open* answer-space, not a hard one: clozing the trio
   makes three semi-open blanks) + rule 5 (fuzzy multi-word spans) + the D1 editor's logged
   SUSTAINED ruling. Raised independently before reading that ruling; concur on the merits.
2. **Card 2's "interdependently in a coordinated manner" vs its two-word menu** — head-word
   matches the menu exactly; the trailing qualifier hides *with* its answer because visible it
   decoded the binary (the editor's leak fix). Spared per the endorsed option-plus-trailing-bonus
   precedent (`{{c1::Delayed (>2 s)::Delayed or Normal}}`) named in E_of_D1_report.md.
3. **Back-side part-and-whole exposure** (card 3's Cue naming all three types, card 8's and card
   13's Meaning glosses spelling sibling answers, Distinguish cross-links restating neighbor
   answers) — spared per decisions #3/#4: the leak surface is Text + hints; Back Extra renders
   after answering; rule 25's back-restatement ban is scoped to numeric columns; R6 governs
   visible-side scenario exemplar reuse, of which there is none.
4. **Card 14's shared-menu elimination** (know one audience → infer the other) — spared per
   R10's judge-cleared multi-dimensional contrast (the endorsed cover/concealment shape has the
   same property; the 2×2 IS the knowledge).
5. **Card 19's five uncued answers** — spared per rule 23's explicit causal-chain handle license,
   adjudicated in D4_notes.md; the warning adjudication above is the licensed judge action, not a
   re-litigation.
6. **Cards 7/10 one-way definitions** (meaning visible, only the name hidden) — spared per rule
   22's not-a-violation classify clause + §4's one-way license + the logged R12 reasoning (the
   dropped meaning-spans were near-synonyms of each other, unrecallable verbatim).
7. **PACE letter hints and ROWS whole-expansion** — spared per R11's mnemonic license (the
   spelled acronym is visible in each stem and IS the memory hook).
8. **Husk-proxy candidates** (cards 0 c2-pair, 2 c2-face, 14 c1-pair, 20 c2-pair) — each cleared
   per R10's judge procedure: a visible entity/term anchor makes every blank answerable; none is
   mutually-dependent-spans-under-one-number.

### Hazards for the run manifest

1. **The consolidation stage dropped an editor-set safety flag** (card 2: `needs_human_check`
   true → false) while carrying the verified_by prose documenting the flip — a stamped file
   contradicting its own verification note. This is the R27a stale-read/reconcile class one step
   later: prose survived, the field didn't. Record in the manifest; after the orchestrator
   applies fixes, re-diff the final file against the `E_of_D*` outputs (the diff that caught
   this), and consider a mechanical consolidation check — any card whose text matches an editor
   output must not carry a *weaker* `needs_human_check` than the editor set.
2. **Figure attachments owed by the downstream figure stage:** card 19 must receive FIGURE 9-4
   (the decision-strategies plate) on its back — check 28's "attach the procedure's plate" was
   deliberately deferred (D4_notes), not waived. Card 7 is the natural home for FIGURE 9-2 (pit
   crew CPR) if the matcher proposes it. Neither card should ship to Anki without the figure
   pass running.
3. **Hand-off sentences owed to Parker** (rule 29's one-sentence lane, both carried from unit
   reports — do not lose at hand-off): (a) the five-essential-elements roster on p882 is unmarked
   and therefore uncarded — cards 6/7 name "one of the five" but only shared-goal and clear-roles
   are marked; does he want the other three elements or a roster card? (b) the team leader's five
   functions (card 10) are left at recognition level; if he wants them producible, the follow-up
   is a chunked 3+2 family.
4. **needs_human_check summary for the verify report:** with the card-2 fix applied, exactly one
   card in the batch carries the flag (card 2, PARTIAL-grounded idx 3, answers verified verbatim
   against the mark's own highlight — documentation for a glance, not a suspected error). The
   numeric:true cards (3, 6, 7, 8, 12, 13, 19) correctly leave flag derivation to
   verify_report.py per the batch convention.
