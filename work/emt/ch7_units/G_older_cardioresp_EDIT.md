# Unit G — editor verdicts (marks 40–46, older adult: cardiovascular / hematologic / respiratory)

Adversarial pass by an editor who did not draft these. 10 cards in, 10 cards out
(0 dropped, 0 added). Checker after edits: **10 cards, 0 hard errors, 0 warnings**
(`--require-provenance` also clean); `test_regressions.py` 43/43.
`"block": "G_older_cardioresp"` stamped on all 10.

| # | Card (short) | Verdict | What changed / why |
|---|---|---|---|
| 0 | Atherosclerosis two-way definition | **REWRITE (minor)** | Back Extra said plaque "becomes restricted, **and eventually** blocked entirely"; the source says "restricted **or** blocked entirely". The "eventually" asserted an inevitable progression the page does not (Rule 10). Restored the source's disjunction. Structure itself PASSES: it is a licensed two-way definition (c1 term / c2 substances), c2 = 3 words (R12 clean), and R3's precision explicitly protects a two-way def from a "leak" fix. |
| 1 | 60% of over-65s have atherosclerotic disease | **REWRITE** | Back Extra rebuilt. (a) Added the shared `Distinguish:` line resolving the heart-rate interference (see below). (b) Dropped the clause "which the majority of people over 65 already carry" — it restated the card's own answer (check #11 padding). (c) Folded the weakened-myocardium chain into the `Pitfall:`. Numbers/hints/husk-shape all PASS (two spans, 1 multiword → not R10; both hinted `::percentage` / `::age`). `numeric` + `needs_human_check` correct. |
| 2 | Three additional cardiovascular effects | **REWRITE** | Two real defects. (1) **False closure / batch contradiction:** the lead-in said "aging brings **three more cardiovascular changes**", but the source's word is "*include*" (an open list, which parker-preferences says must not be carded as closed) **and** card #3 in this same unit teaches a fourth cardiovascular change of aging (diastolic BP rises). Re-anchored to the heart itself — "aging weakens the older adult's **heart** in three ways" — which is honest, grounded, and cleanly disjoint from the vascular card. (2) Row 3 said "the heart **cannot** increase cardiac output on demand"; the source says "**diminished ability**". Softened to "the ability to increase cardiac output on demand diminishes", also making the three rows parallel. R7 verified: stated three, clozed three, and all three are the source's own ("a decrease in heart rate, a decline in cardiac output, and diminished ability of the heart to increase cardiac output to meet the body's demands"). Added the shared `Distinguish:`. Rows still lead with their clozes → R17/R22 exempt; no direction blank exists, so no legend is owed. |
| 3 | Vascular stiffening → diastolic BP rises | **PASS** | Both binary blanks legended with forced choices whose spelling matches the answers (`::systolic or diastolic` → "diastolic"; `::increases or decreases` → "increases"). Grounded verbatim. Visible remainder is a strong anchor, not a husk. Only `block` added. |
| 4 | Bone marrow → fatty tissue | **REWRITE (minor)** | Dropped the word "progressively" (not in the source; Rule 10). Single unhinted blank is forced by the stem and carries no absolute → no R16 exposure. Back Extra chain (loss of marrow → cannot make new cells → devastating with rapid large-volume blood loss) is grounded verbatim; agreed with the drafter that clozing that consequence would be a tautology against the visible first clause. |
| 5 | Respiratory direction-of-change panel | **REWRITE (minor)** | The panel itself is the best card in the unit and is exactly card-recipes §8's trend template: **every one of the four rows carries `::increases or decreases`, and every hint's spelling matches its own answer**; the classify lead-in is honest (the visible structure names ARE the intended cue for a which-way card), which is the R17/R22 exemption, not a checker dodge. Changes: (a) lead-in now states the count ("the four ways") so Parker can see how many answers he owes — it also switches the mechanical undercount check on (4 stated / 4 clozed); (b) Back Extra dropped the phrase "for gas exchange", which the cited context never says (Rule 10); (c) `Cue:` sharpened to the actual pattern — three down, one up. List completeness verified against the full sentence: airway size, alveolar surface, lung elasticity, intercostal/diaphragm strength = exactly four. |
| 6 | Vital capacity — definition | **REWRITE (minor)** | Label was `Cue:` for what is plainly a clinical trap; changed to `Pitfall:` (and Pitfall outranks Cue in the priority order). **The split does what it was built to do:** card #6 is the two-way definition, where the meaning is *supposed* to face the hidden term; card #7 shows "vital capacity" as a visible anchor and carries **no** parenthetical definition at all. So there is no card in this unit where a bare parenthetical gloss sits beside a hidden "vital capacity" (R3). c2 = 5 words → R12 clean. |
| 7 | Vital capacity — 75 y → ~50% | **PASS** | Verbatim from the page; `numeric` + `needs_human_check` set; both blanks form-hinted; rigid-yet-fragile calcified chest in Back Extra is grounded and is a distinct fact, not a restatement. Only `block` added. |
| 8 | Upper-airway protections that weaken | **REWRITE (substantive)** | **The count was wrong and the card was a coin flip.** It said "three of the upper airway's protective functions fade" and clozed cough reflex / gag reflex / clearing secretions — but the same passage names **five** structures that protect the upper airway and lose function: it also says "the cilia that line the airway dwindle, and sensation within the airway declines". Asking for "three" out of five is unanswerable-cold (which three?), and the card's own old Back Extra admitted the fourth by teaching cilia. This is check #17 / R7 exactly: read the whole list off the page, then state the real count. Now five rows, all verbatim-grounded, count 5 = 5 clozed. New `Why:` line carries the source's own conclusion (harder to maintain an open upper airway) rather than re-listing the answers. |
| 9 | Aspiration + airway obstruction risk | **REWRITE (minor)** | Back Extra reworked because the old `Why:` ("sensation within the airway also declines") is now one of card #8's five answers and was doing double duty. Reframed as a `Pitfall:` about the *silence* of the risk — the clinical read, not the item. Grouped c1 pair is right (a cohesive two-member set, not a husk: only one span is multiword, and the stem anchor is substantial). Grounded verbatim. |

## The direction-of-change sweep (the thing this unit is most exposed to)

Every blank in the unit that hides an increase/decrease/rise/fall was enumerated and
checked individually:

- **Card #3** — `diastolic` (`::systolic or diastolic`) and `increases`
  (`::increases or decreases`). Both legended, both spellings match. PASS.
- **Card #5** — four rows, four `::increases or decreases` legends, spellings match
  ("increases" / "decreases" both appear in the legend string). This is the panel the
  brief flagged as highest-risk, and it works *because* it mixes the one INCREASE
  (airway size) with three DECREASES — which is only fair if every row is legended, and
  every row is. PASS.
- **Cards #2 and #8** — the direction words sit *inside* whole clozed items in a grouped
  reveal (the item is the answer), not in a bare directional blank, so card-rules #13
  does not apply and a legend would be noise. Confirmed row by row.
- No other blank in the unit hides a direction word.

## The heart-rate interference — decided: YES, a shared Distinguish line

Card #2 teaches that aging **decreases** heart rate; card #1's Back Extra says the body
**raises** heart rate in a life-threatening illness. Both are the book's own claims, from
the same paragraph, and in a shuffled megadeck they read as a flat contradiction with no
visible reconciliation. Added the **same line, word for word, to both cards** so whichever
one surfaces first resolves the other:

> `Distinguish: the age-related drop in heart rate is a baseline change; in a
> life-threatening illness the body still raises the heart rate to preserve blood pressure.`

Deliberately phrased as *baseline change* rather than "lower than a young adult's" —
TABLE 7-1 gives the older adult the same 60–100 beats/min band as an adult, so the
stronger claim would contradict the chapter's own table.

## For consolidation

1. **Card #2's lead-in was narrowed to the heart on purpose.** If a later unit or the
   consolidator builds another "cardiovascular effects of aging" list card, keep it away
   from that phrasing — the source's list is introduced with "include" and is not closed.
2. **The shared `Distinguish:` line is duplicated by design** across cards #1 and #2.
   Do not dedupe it; each card must carry it to survive shuffling.
3. **Two numeric cards** (#1 and #7) carry `numeric` + `needs_human_check`: *more than
   60% / older than 65 years* and *age 75 / about 50%*. Both are verbatim page text, no
   `visual_source` needed.
4. **Verified but deliberately NOT asserted (the brief forbids asserting outside the
   marks' context).** Mark 46's context ends mid-sentence at "strong inhalation can cause
   the walls of the airway". I read the continuation directly off the source PDF
   (`pdftotext -f 723`, p723 of the Pollak PDF), verbatim: *"…to collapse inward,
   producing inspiratory wheezing, lower flow rates, and air trapping in the alveoli
   (incomplete expiration). Because of these reductions in function, and because the
   white blood cells of the airway are less aggressive toward invading organisms, the
   older patient is more susceptible to lung infections."* That is high-yield geriatric
   respiratory material (lower-airway collapse, inspiratory wheeze, air trapping,
   susceptibility to lung infection) and it is **uncarded**. It belongs to whichever unit
   owns p723 — flagging it here so it is not lost.
5. Other un-highlighted context left uncarded on purpose (available if the chapter comes
   out thin): the "changes are gradual until a crisis" framing is used once, on card #6;
   the rigid-yet-fragile calcified chest is used once, on card #7. Neither is carded as
   its own note.
6. **No figures wanted.** Agreed with the drafter: FIGURE 7-13 is a stock photo of an
   older person with medications and would be incongruent on any card here (R19 /
   Parker's congruence rule). Recommend the figure stage skip unit G.
