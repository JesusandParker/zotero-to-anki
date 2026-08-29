# Editor report — E of D2 (EMT ch9: D_group_types / E_team_elements / G_team_leader)

Adversarial pass, independent of the drafter. Every check in `editor-checklist.md` run on
every card; checks 18-24 run per ROW. Grounding re-verified word-for-word against
`chapter_9_highlights.json` (idx 4, 5, 6, 7, 8, 14, plus adjacent idx 1 and 9 as witnesses).
Post-edit batch: `E_of_D2_cards.json`. **PASS 4 / REWRITE 4 / DROP 0.** No yellow mark
loses coverage.

## Verdict table

| # | Card | Verdict | Failed checks | Exact change made |
|---|------|---------|---------------|-------------------|
| 0 | D-1 membership (3 group types) | **REWRITE** | 1, 18 (open stem) | Stem now opens "Classified by who directs each member's work, …". Bare "three types" of provider groups is answerable-cold with the chapter's OWN other triad — idx 2's context names "triage, treatment, and transport groups" as EMS groups — so a knower could legitimately produce the wrong three. The axis anchor forces the D/I/I taxonomy; it is the Cue line's existing synthesis moved forward (no new claim), and deliberately avoids the root "depend"/"rely" (drafter's own leak-hygiene note) so a non-knower still cannot decode the names. Rows unchanged: 3 uncued under one c1 (load ≤4 ✓), `<br><br>` layout ✓, count "three" = 3 rows = the heading's complete set ✓, no row leaks (all hide together). |
| 1 | D-2 dependent (two-way) | **REWRITE** | 6 (R12: c2 hid 11 tokens) | c2 tightened to `{{c2::told what to do}}` (4 words). The drafter flagged it at "9 words"; actual tokenization is 11, past `LONG_CLOZE_WORDS = 9`, and "— and often how to do it" is a qualifier no one reproduces verbatim, so self-grading fails even when he knows the fact. The qualifier is NOT dropped: folded into the Why: line ("told not only what to do but often how to do it…"), still verbatim-grounded in idx 4. Both faces re-cold-solved after the cut: c1 face ("told what to do by the group leader" → dependent) and c2 face ("In a dependent group, each member is ___ by the group leader" → told what to do) both stay forced. Drafter's worry that trimming "would misstate the fact" is answered by keeping the fact on the back, not by deleting it. |
| 2 | D-3 independent (two-way) | **PASS** | — | c2 "his or her own area" is 5 words, crisp, verbatim. The parenthetical gloss correctly pre-moved to `Meaning:` (kills the paraphrase leak). Pitfall (DOA-from-airway) grounded verbatim in idx 6 context and used exactly once in the batch. The "In a/an" vowel tell (an → not-dependent) is the sanctioned house form per recipes §4 (articles outside the brace); it narrows but never names, and the description does the forcing. `Meaning:` used as a gloss rather than an acronym expansion — matches the blessed-label list in card-rules Layer A #5; left as-is. |
| 3 | D-4 interdependent (two-way) | **PASS** | — | Verbatim idx 6. Both faces forced; c2 "true team" 2 words; `::group type` hint correctly steers the adverb blank to the taxonomy (kills "together/collaboratively" open-set drift). Drafter's trim of "(the best possible patient outcome)" off the Why: line verified — E-1's answer does not sit on this back. Cross-unit overlap with idx 3 noted below for the assembler. |
| 4 | E-1 shared goal | **REWRITE** | 18 (open-set), 15 | Covered the answer and cold-solved: "committed to a common goal — typically, ___" admits several textbook-true fills — above all "quality patient care", which is verbatim in THIS chapter (idx 1 context, p874: "unified goal of quality patient care"). Nothing visible separated process from outcome. Fix per rule 16 + recipes §4's "forced binary when the blank is otherwise open" / §9's confusable-menu license: slot hint `::patient outcome or quality care` (a menu is the licensed leak-on-purpose exception — the recall is WHICH, plus the full phrase), and a third Back-Extra line `Pitfall:` pinning the discrimination (non-negotiable #7: the distinguishing feature in the cue or the Distinguish/Pitfall line). Hint distractor and Pitfall are grounded verbatim in idx 1's context; `from_idx` deliberately NOT extended (idx 1 is another unit's mark — coverage vs grounding-witness kept distinct). Element name left visible/bold — drafter's asymmetry argument sustained (clozing "shared goal" is a freebie against visible "common goal"; hiding the scaffold is a husk). Mechanical note: `open_set_absolute` would NOT have caught this (bare "must" is not in ABSOLUTE) — judge-level catch. |
| 5 | E-2 clear roles (two-way + two spans) | **REWRITE** | 6 (R12), 8-adjacent (R8) | Collapsed to ONE-WAY describe→name: single `{{c1::clear roles and responsibilities}}`, description fully visible. The dropped c1 pair — "what needs to be done" and "what is expected of him or her" — are 5- and 7-word fuzzy spans that are near-synonyms OF EACH OTHER; producing both, verbatim, which-is-which, is noise recall no knower performs cold (the R12 defect in its paired form). §4's one-way license fits exactly ("hide the TERM… when the term is the recognition target"), non-negotiable #6 says untested-direction production was never guaranteed anyway, and rule 22's not-a-violation clause blesses the classify shape (visible description = intended cue). This also mirrors E-1's deliberate asymmetry, so the E-pair is now internally consistent. Idx 8 stays covered (the binding is tested; the meaning text is the cue and lives on the front verbatim). Cold-solve of the kept face: "each provider must know what needs to be done and what is expected of him or her" forces exactly one of the five elements. No hint needed — the "One of the five essential elements…" frame already names the slot's category. |
| 6 | G-1 team leader (describe→name) | **PASS** | — | Drafter's rule-23 reasoning sustained (ruling below). Cold-solve: five functions visible → "team leader" is forced; semi-transparency is the sanctioned describe→name direction of a definition card (rule 3 precision clause). Grounding of the Distinguish tail ("working together with them and facilitating coordination") initially looked invented — idx 14's context truncates at "not only by providing" — but it is VERBATIM in adjacent mark idx 9's context (p884: "…not only by providing support but also by working together with them and facilitating coordination"). Rule 11's adjacent-highlight license applies; grounded, no change. |
| 7 | G-2 commands → dependent group | **PASS** | — | Rule 21 satisfied twice over: visible contrast anchor ("is not leading a team — merely directing…") AND `::group type` slot hint (also mechanically exempt from `open_set_absolute` via the hint). NOT a duplicate of card 1: card 1 defines the dependent group (member is told what to do); card 7 classifies a leadership failure (a merely-commanding "team leader" is really a group leader running a dependent group) — different claims, and the derivation commands→told-what-to-do→dependent is reasoning, not pattern-matching (drafter's argument sustained, distinction recorded). Distinguish tail grounded via idx 9 (same finding as card 6). Clozing "not leading a team" as a c2 was correctly not done — the visible "merely directing a dependent group" would self-answer it. |

## Rulings on the drafter's open concerns

1. **E-1 vs p874 "quality patient care" (cross-unit interference).** Upheld and acted on —
   this was the batch's worst defect, not just a cousin-note. Fixed inside this unit with
   the confusable-menu hint + Pitfall line (card 4). **Assembler must still check the
   reverse direction:** if the unit owning idx 1 cards "unified goal of quality patient
   care", that card's stem needs its own discriminator (e.g. its continuum-of-care /
   whole-system frame), or the pair will interfere from the other side.
2. **D-4 vs idx 3 (p878 team definition).** Noted, no action (cross-unit dedupe is out of
   scope per tasking). The claims differ — D-4: interdependent work = true team; idx 3:
   team = assigned roles + interdependent + designated leader. Flag for the assembler:
   when idx 3's card lands, make sure its front does not display "working interdependently"
   while asking for "team" in a way that duplicates D-4's c1 face by meaning.
3. **D-2 c2 length.** Overruled the "leave it" lean: 11 tokens, mechanically past R12's
   threshold (the drafter's 9-word count was an undercount), and the qualifier is
   preservable on the back without misstating anything. Rewritten as above.
4. **Describe→name softness in block D.** Sustained. The taxonomy's names are
   semi-transparent English; that decodability is inherent to the material, and rule 3's
   precision clause protects the two-way definition shape from being "fixed" into
   obscurity. The c2 directions carry the real load, as designed.

## Rulings on other drafter decisions (verified, not just accepted)

- **G-1 recognition-level five functions (rule-23 reasoning): SUSTAINED.** Independently
  re-derived: 5 uncued abstract near-synonyms (coordination/oversight/support overlap), no
  spelled mnemonic, no regenerating structure → grouped reveal barred by rule 23; sibling
  numbers barred by 24; an invented 3+2 partition would drill verbatim production of
  near-synonym abstractions (the known "impossible cold" family) with scaffold heavier than
  knowledge. Describe→name + the G-2 discriminator is the best legal shape. **Escalated to
  Parker below** (the drafter's flag carried forward): the five functions are never
  produced, only recognized.
- **No membership/roster card for the five team-performance elements: SUSTAINED** — the
  roster lead-in is unmarked; rule 29 bars it. Both E stems correctly print "five" as
  visible framing only.
- **`numeric: true` with `needs_human_check: false`:** verified against the checker —
  `check_cards.py` exempts a numeric-looking card that records `verified_against`
  (and `verify_report.py` derives the same), so the drafter's convention is the pipeline's
  contract, not a dodge. Counts re-verified by me: "three types" = 3 rows = the heading's
  complete enumeration; "five essential elements" stated, none clozed.
- **Membership card + per-type anchors coexisting (card 0 hides names that cards 1-3
  display on their c2 faces):** not a check-16 violation — that is rule 30's mandated
  two-lane design (membership lane + row lane), same-note face reveals are inherent to
  two-way definitions, and bury-siblings spaces them. Check 16 targets scenario cards
  answerable by pattern-matching a sibling's exemplar; no scenario card here reuses one.

## Escalations / hand-off notes

- **For Parker (carried from drafter, endorsed):** the team leader's five functions (role
  assignments, coordination, oversight, centralized decision making, support) are left at
  recognition level — visible on G-1's front, never produced. Every produce-the-list shape
  is barred or bad under rules 23/24. If he wants them producible, the follow-up is a 3+2
  partition family with PRINTED (invented, uncloze-able) sub-group names and `Roster:`
  lines.
- **For the assembler:** the two cross-unit interference pairs in rulings 1-2 above; and
  cards 6/7's Distinguish grounding witness is idx 9's context (p884), not idx 14's own
  truncated context — do not "fix" those lines as ungrounded.
- Editor grounding witnesses beyond the cited marks (all verbatim in
  `chapter_9_highlights.json`, cross-link only, `from_idx` untouched): card 4's hint
  distractor + Pitfall ← idx 1 context; cards 6/7 Distinguish tails ← idx 9 context.
