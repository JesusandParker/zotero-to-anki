# Unit G — older adult: cardiovascular, hematologic, respiratory (marks 40–46)

10 notes. Every mark is covered by at least one card; nothing dropped, nothing flagged
uncardable. `python3 scripts/check_cards.py --require-provenance` on this file: **10 cards,
0 hard errors, 0 warnings**, grounding verified against `chapter_7_highlights.json`.

## Fact pass

**Mark 40 (p720, atherosclerosis)** → card 1
- MUST-TEST: atherosclerosis ↔ buildup of *cholesterol and calcium* on the *inner walls* of
  blood vessels. Built as a two-way definition (`c1` term / `c2` the two substances) with the
  situational anchor "cardiac function declines with age largely because of…", so the c1 card
  is describe→name and the c2 card is name→state the substances. R12 respected: the c2 side is
  3 words, not the whole 15-word clause.
- SUPPORTING (Back Extra): plaque accumulation → flow restricted, eventually blocked entirely.
  Kept off the Text because "restricts or blocks" is a fuzzy near-synonym blank (rule 5/2).
- Deliberately NOT on this card: the 60% statistic (its own card; putting it in this Back
  Extra would give away card 2).

**Mark 41 (p720, 60% over 65)** → card 2
- MUST-TEST: both numbers. Clozed under the same `c1` so the statistic hides as one unit;
  each blank carries a form hint (`::percentage`, `::age`). `numeric` + `needs_human_check`.
- Back Extra carries the compensation chain from mark 42's context (illness raises the heart
  rate → the aged, weakened myocardium can be damaged → combined with severe atherosclerosis
  the damage could prove fatal). That is why this card's `from_idx` is **[41, 42]** — the
  Back Extra is genuinely built from 42. Mark 42 still has its own cards (3 and 4), so this
  is not a coverage double-count.

**Mark 42 (p721, `list_lead_in`)** → cards 3 and 4
- MUST-TEST (card 3): the three additional cardiovascular effects, read off the full context,
  not the truncated highlight: heart rate decreases · cardiac output declines · the heart
  cannot increase cardiac output to meet the body's demands. Grouped reveal, one `c1`,
  `<br><br>` between rows, stated count "three" = 3 clozed items (R7). Each row **leads with
  its cloze**, so the item itself is the answer (R17/R22 exemption) rather than a direction
  word punched out of a visible frame.
- Prereq closure (rule 11): "cardiac output = amount of blood pumped by the heart per minute"
  is the context's own parenthetical, moved to Back Extra so it does not sit visible next to
  its own term.
- MUST-TEST (card 4): vascular stiffening → vessels cannot dilate/contract → **diastolic** BP
  rises and the heart works harder against vascular resistance. Both the *which number* and
  the *direction* are clozed under one `c1` with forced-choice hints
  (`::systolic or diastolic`, `::increases or decreases`), so neither is a coin flip and
  neither row answers the other.
- SUPPORTING, deliberately NOT its own card: the "illness raises the heart rate, which can
  damage a weakened heart" chain. Every draft of it was decodable from its own visible stem
  ("because cardiac muscle weakens with age, the faster rate may ___"), and hinting it would
  have leaked. It teaches better than it tests, so it lives in card 2's Back Extra.

**Mark 43 (p722, marrow → fat)** → card 5
- MUST-TEST: bone marrow is progressively replaced by fatty tissue. Single crisp cloze,
  unhinted (the stem forces it).
- SUPPORTING (Back Extra): reduced ability to manufacture new blood cells, and the field
  consequence — harmless alone, devastating with traumatic rapid large-volume blood loss.
- NOT carded separately: every phrasing of the consequence was decodable from the mechanism
  shown in the same stem (a rule-2/rule-3 tautology). Flagging here in case consolidation
  wants an application card built from a *different* unit's trauma material instead.

**Mark 44 (p722, respiratory changes)** → card 6
- MUST-TEST: all four directions, including the airway-increases half, which lives in the
  **context** and not the highlight — included because it is the one counterintuitive item
  and it turns a flat list of decreases into a genuine which-way card. Grounded verbatim
  ("In older adults, the airway increases in size").
- Built as a classify panel (card-recipes §8/§6) with a `::increases or decreases` hint on
  every row, per the coin-flip rule. The classify lead-in is honest, not a checker dodge:
  the visible structure names ARE the intended cue for a direction-of-change card, which is
  the exemption card-rules #22 spells out.
- Rows use `:` rather than `=` on purpose — `=` rows trip `equation_husk_groups` spuriously
  when four blanks share one cloze number.

**Mark 45 (p722, vital capacity)** → cards 7 and 8
- Split into a two-way definition (card 7) and the numeric fact (card 8), exactly to dodge
  R3: the parenthetical definition never sits visible beside a hidden "vital capacity."
  On card 7 both halves are clozed (licensed two-way, not a leak); card 8 carries no
  definition at all, only the term as the anchor.
- Card 8 clozes both 75 and 50% under one `c1` with form hints. `numeric` +
  `needs_human_check`.
- SUPPORTING (card 8 Back Extra): the chest becomes rigid yet fragile and the calcified rib
  cage fractures rather than flexing. **Candidate for its own card** — high-yield geriatric
  trauma — but it is un-highlighted context and outside this unit's brief. Flagging for
  consolidation.

**Mark 46 (p722, upper-airway protection)** → cards 9 and 10
- MUST-TEST (card 9): the three protective functions that fade — cough reflex, gag reflex,
  ability to clear secretions. Grouped reveal, rows lead with their clozes.
- MUST-TEST (card 10): the field payoff — greater risk of **aspiration and airway
  obstruction**. This is the one application-flavored card in the unit, justified by the
  brief's carve-out for findings that change field management (airway).
- Scoped to the three highlighted items rather than five: I first drafted card 9 with the
  cilia and the declining airway sensation as two more clozed rows, then pulled them out,
  because any Back Extra that explains the mechanism would then have named card 10's answer
  or card 9's own answers (rule 13, cross-card give-away). Final split: **cilia** teaches on
  card 9, **sensation** teaches on card 10, and card 10's stem never names card 9's items.

## Merges
None — no two marks were folded into one card. Marks 41 and 42 are *cross-cited* (card 2's
`from_idx` is [41, 42]) but not merged; 42 has its own two cards.

## For the consolidation stage
1. **`block` field omitted.** The brief's card shape does not include it; `note-format.md`
   and the ch6 canon do. If the consolidator wants per-unit provenance, stamp
   `"block": "G_older_cardioresp"` on all 10 — `from_idx` 40–46 identifies them unambiguously.
2. **Adjacent-fact interference to eye once the whole chapter is merged.** Card 3 teaches
   "the heart rate *decreases* with age"; card 2's Back Extra says the body *raises* the heart
   rate in a life-threatening illness. Both are the book's own claims and each states its
   context, but they are the two facts in this unit most likely to feel contradictory in a
   shuffled deck. Worth a Distinguish line if the chapter-level editor wants one.
3. **Two numeric cards** (2 and 8) carry `needs_human_check: true`: *60% / older than 65
   years* and *age 75 / about 50%*. Both are verbatim from the page text, not from a figure —
   no `visual_source` needed.
4. **No figures wanted for this unit.** Nothing here is a table or plate; FIGURE 7-13 is only
   a stock photo of an older person with medications, so a match against these cards would be
   incongruent (Parker's congruence rule). Recommend the figure stage skip unit G.
5. **Un-highlighted context left uncarded, on purpose** (available if the chapter comes out
   thin): the rigid-yet-fragile calcified chest wall (mark 45 context) and the lower-airway
   smooth-muscle weakening that lets airway walls collapse on strong inhalation (mark 46
   context, sentence cut off mid-clause).
