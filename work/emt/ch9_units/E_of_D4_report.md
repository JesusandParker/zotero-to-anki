# Editor report — E of D4 (EMT ch9, blocks J / K / L / M)

Independent adversarial pass. Every checklist item run on every card; checks 18-24 run on every ROW. Grounding re-verified word-for-word against `chapter_9_highlights.json` marks 17-24 (highlight + context), not against the drafter's notes. Profile consulted: `profiles/emt.md` (ch9 = recall-heavy chapter, so check 12 scenario-forcing does not apply; §6 says the numeric flag is derived by `verify_report.py` from `verified_against`/`verified_by`, never asserted by hand).

## Verdict table

| # | Block | Verdict | Failed checks (by number) | Change made |
|---|-------|---------|---------------------------|-------------|
| 1 | J_prearrival (idx 17) | **PASS** | none | none |
| 2 | K_rows (idx 18) | **PASS** | none | none |
| 3 | L_decision_process (idx 19-23) | **PASS** | none | none (rule-23 license upheld — ruling below) |
| 4 | M_decision_traps (idx 24) | **PASS** | none | none |

`E_of_D4_cards.json` is therefore the D4 batch unchanged (verified byte-equal, valid JSON, 4 cards). No `verified_by` strings were amended because nothing was rewritten.

---

## Ruling 1 — the L rule-23 call (5 uncued contents under one c1): UPHELD

The question: does gather → interpret → plan → communicate/implement → evaluate carry a genuine retrieval handle, or is the drafter's "causal chain" claim the kind of feels-right license the parker-preferences probation note ("5-7-item cards are on probation, not exonerated") exists to catch?

**For overturning:** the probation evidence is brutal — 5-6-item groups failed 89% on first review; CHART (5 items, acronym-anchored, the card Parker himself called good) is 3/4 Again. "Feels derivable" and "is passable" came apart once already. Grading is still all-or-nothing on 5 (0.9^5 ≈ 59%).

**For upholding:** rule 23's 5-7 license names, in its own text, "a structure that regenerates the members (… a strict causal chain, a schema he already holds)" — and that clause survived the 2026-08-02 revision that CREATED the probation note, so the two coexist deliberately. This set is the strongest possible instance of the clause: each step's output is literally the next step's input (data → meaning → plan → executed plan → observed effect), so asking "what must exist before the next thing can happen?" regenerates every member in order — unlike CHART or the radio report, whose members are conventional slots no logic derives (an acronym cues but does not regenerate). It is also the universal assess-decide-act-check loop (the nursing-process shape), a schema Parker already holds. The recipes actively model this exact shape at this exact size: §7's own BLS example is 5 steps under one c1; §12e (step-scaffold, ordinals printed, cognitive sequence — not psychomotor, so rule 26 is satisfied) is the drafter's cited archetype and the licensed one. If THIS set fails the causal-chain clause, the clause licenses nothing and is dead letter — that repeal is Parker's call, not an editor's.

**The chunked alternative is worse here**, not just unnecessary: any 2/3-way partition of a 5-step loop uses invented sub-group names (unclozeable per rule 23.1, so they'd be scaffolding boilerplate), and the order-vignette anchor that 23.1 wants for a chunked ORDERED set would need the book's chest-discomfort example — already spent as this card's `Ex:` (a rule-13 self-leak) — or an invented scenario (rule 10).

**Probation honored concretely:** this card is the batch's designated probation case. If the review log shows it failing like CHART, the rule-32 remediation lane (retire + chunk into steps 1-3 / 4-5 with `Roster:` lines) is the pre-agreed fix — record that in the run manifest rather than relitigating. Per-row cold-solve passes (closed printed-count set, rule 16's closed-taxonomy exemption; rows lead with their cloze, hide more than they show, ordinals printed never clozed; `<br><br>` layout shows the count owed).

## Ruling 2 — J's open-set guard: the frame does force the answer

Covered "mentally rehearse" and hunted for surviving true fills. The blank's object — "the steps in the care that may be needed" — is what closes it: the crew-level en-route alternatives the source lists (designate a leader, discuss roles / additional help / equipment / destination) do not take that object, and the source never says anyone "discusses the steps in the care." What survives ("review," "think through," "rehearse") is the same answer in other words, which rule 16 explicitly does not count as an open set. Considered a slot-label hint and rejected it: "::mental action" leaks half the answer ("mentally"), "::verb" adds nothing — recipes' default is no hint. The un-clozed "prearrival" stage name is correctly left as scenery: "en route to the call" in the same sentence decodes it, so a c2 there would be padding (2026-07-30 corollary). No change.

## Ruling 3 — K's licensed-acronym shape, both directions, and the sibling-mark Distinguish

- **Shape:** ROWS visible, expansion clozed — this is rule 18's licensed direction exactly ("the letters ARE the memory hook and the acronym is visible in the stem"); the letters partially deriving the expansion is the designed mechanism of a spelled mnemonic, not a leak. The italicized printed "first" is right not to cloze: a c2 on it would be near-self-answering with any priority hint, i.e. padding.
- **The reverse freebie:** the drafter's skip of the expansion-visible → "name the acronym" direction is correct and important — R-O-W-S is mechanically first-letter-derivable from a visible "rule out worst-case scenario," so that card would test nothing. Verified skipped.
- **Distinguish from sibling mark 24:** acceptable, kept. Grounding by a cited-in-batch sibling mark is disclosed in D4_notes and the line is verbatim-faithful to mark 24. Cross-linking Distinguish lines on confusables are explicitly endorsed (parker-preferences; §4 calls Distinguish the highest-value line, and its own hypoxia example states the neighbor's full definition). Check 16 does not fire: it targets scenario/classify cards pattern-matching a sibling's exemplar; M is a definition note and back-side teaching of a confusable is how Distinguish is supposed to work. One soft spot noted, below the rewrite bar: "the opposite failure" is slightly loose (ROWS is a strategy, not a failure), but the teaching contrast is clear and grounded.
- Mark 18 is `page_sparse`/`needs_visual` with grounding EXACT; the orchestrator's page-897 render is recorded in `verified_by`. The safety overlay keys on PARTIAL/NOT_FOUND, so `needs_human_check: false` stands.

## Ruling 4 — M's two-way, the Pitfall move, and the overconfidence line

- **Shape confirmed:** c1 term (hint "::decision trap" = the book's own category word, a clean form label) / c2 meaning as two crisp spans (6 + 5 words) revealing together — 2 uncued answers, well under load. The c2 card shows "Anchoring" as the visible anchor, so no husk; the c1 card's visible definition is the intended describe → name cue. A two-way definition is NOT a husk/leak (R3/R10 precision) — nothing "fixed."
- **"Sometimes before the call" → Pitfall: correct, and nothing must-test went untested.** Visible in the Text it would decode "early" on the c2 card (a real rule-3 leak); as its own cloze it is an open-set-ish qualifier with no independent retrieval value ("early, sometimes even before the call" intensifies "early," it is not a separate fact). Taught every review in `Pitfall:` is its doctrinally correct home.
- **Distinguish: overconfidence is teaching, not a card in disguise.** Overconfidence is unmarked (idx 24's highlight covers only anchoring), so a standalone card would violate rule 29; pinning it on the back with its discriminator ("overestimates his or her own ability … instead of fixating on one cause") is the licensed use of adjacent context, grounded verbatim in mark 24's own context paragraph.
- The asthma/anaphylaxis `Ex:` is verbatim-close and is NOT reused on any classify sibling (none exists — the drafter's rule-13 skip of a classify-vignette is correct; the profile's recall-heavy stance agrees).

## Cross-checks run batch-wide (all clean)

- **Cold-solve per row (18-24):** every blank forced; no open sets, no husks, no self-answering rows, no absolutes with bare blanks, no filler-word clozes (L's rows lead with their cloze and hide more than they show — rule 22's good side).
- **Leaks (2/9/15):** none visible; the only definitional content on a front is M-c1's describe → name cue, which is the definition archetype, not a leak.
- **Grounding (3/R13):** every Text claim and Back-Extra line matched against the cited marks' highlight+context. Two synthesis points verified as faithful, not invented: K's `Why:` second clause (gloss of two grounded sentences) and L's `Ex:` "prompts the plan to be adjusted" (the book prints the example to illustrate the "continues or adjusts" branch; new shortness of breath → adjust is the only reading).
- **Under-clozing (4/7):** J's stage name and object phrase, K's "first," M's timing parenthetical all adjudicated above — deliberate scenery/back-side, each for a stated rule reason.
- **Lists (5/17/19/21):** L is the only list: complete (5/5 vs source's numbered 1-5), stated count printed and matching, `<br><br>` between every row. M's mark has `list_lead_in: true` but the flag points at the following unmarked "Avoiding Decision Traps" material (rule-29 out of scope); the card states no count, so check 17 does not bite.
- **Formatting:** only `<b>/<i>/<br>` used; Back-Extra components separated by `<br><br>`; all labels blessed (Why/Cue/Ex/Distinguish/Pitfall); c2 spans crisp; lengths 20-35 words.
- **Numbers (27/29 + safety overlay):** no clozed quantities anywhere. L's "five" is printed scaffolding, verified verbatim, `numeric: true` with `verified_against`/`verified_by` recorded — per profile §6 the flag is derived downstream, so hand-asserting `needs_human_check` would itself be the anti-pattern. M's "24-year-old" appears only inside a verbatim illustrative `Ex:`; not a dose/threshold/time window.
- **Provenance:** all `from_idx` cite real yellow marks; no unmarked content tested; no marks in this range left uncovered (17, 18, 19-23, 24 = full coverage of the D4 slice).

## Suspected cross-unit overlaps (noted only — no dedupe performed, per instructions)

1. **L step 4 vs D3's I_pace card "When a PACE challenge leads the team to alter the original plan… the {{c1::team leader}} communicates the change to everyone."** Nearest neighbor in the chapter: both concern the leader communicating a plan to the team. Different tested claims (a step's content vs the role who communicates a CHANGE) and different marks (22 vs 16) — I judge them distinct, but the cross-unit dedupe pass should eyeball the pair.
2. **L step 4 vs D3's F_team_communication four-elements card:** checked; no overlap ("communicate the plan" is not one of the four elements).
3. **J's Back-Extra `Cue:` (leader designated en route) vs D2's G_team_leader cards:** back-side teaching only on J, no tested-claim overlap.

## Escalations / notes for the orchestrator

- **L is a probation-zone card by design** (5 uncued, licensed by the causal-chain handle). Watch its first reviews; the pre-agreed fallback is in Ruling 1. No action now.
- Cosmetic only, below the rewrite bar: J's `Cue:` line has a mild modal mismatch ("should be clearly designated and the crew discusses"), and K's "the opposite failure" phrasing is slightly loose. Neither affects any tested content; flagged in case a later pass touches these cards anyway.
