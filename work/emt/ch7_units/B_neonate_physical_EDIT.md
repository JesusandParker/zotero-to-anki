# Unit B — neonate/infant physical — EDITOR verdicts

Adversarial pass over the 8 drafted notes (marks 2–9). Every claim re-verified against the
`context` fields in `B_neonate_physical.json`, plus a direct read of PDF pages 687–689
(`pdftotext -layout`) to settle the p688 list question.

**Result: 2 PASS · 6 REWRITE · 0 DROP.** Note count unchanged (8 notes → 13 Anki cards).
`check_cards.py … --highlights work/emt/chapter_7_highlights.json` → clean, stamped.
Every `from_idx` / `source` / `segment` / `visual_source` / `image` preserved verbatim.

---

## Card 1 — weight timeline (`from_idx [2, 4, 5]`) — **REWRITE**

**Kept the 5-blank grouped reveal.** I stress-tested it against R12, the crisp-cloze rule and
the 60-word cap and it survives all three:

- *Legitimate cohesion, not cramming.* Birth weight → week-1 loss → daily gain → doubling →
  tripling is ONE trajectory stated in one source paragraph. Parker's "big lists stay whole"
  governs; splitting it would be the defect.
- *R12 does not fire.* R12's own MUST-NOT-OVER-FLAG protects a group with several spans; the
  detector targets a group with exactly ONE span ≥9 words. Longest span here is a number.
- *Prose 54 words* (was 52), under the 60 cap.
- *Per-row cold-solve, all five:* each row carries a distinct time label that forces exactly
  one answer ("At birth" → weight · "First week: falls ___ from fluid loss" → a percentage ·
  "Second week onward: gains about ___" → a daily rate · "Doubles birth weight by ___" → a
  time · "Triples birth weight by ___" → a time). Not an R10 husk — cover all of c1 and the
  visible remainder is five substantive labels, not connective scaffolding.

**What changed, and what caught it — check #2 / R3 leak.** The lead-in read *"A neonate's body
weight over the **first year**:"* while the final row's hidden answer is `1 year`. A non-knower
decodes the last blank off the heading. Lead-in → *"A neonate's body weight follows a
predictable course:"* (also fixes a small band error: rows 3–5 are about infants, not neonates).

Numeric flags correct (`numeric` + `needs_human_check` true) for 6–8 lb / 3–3.5 kg / 5–10% /
1 oz / 30 g / 4–6 months / 1 year.

## Card 2 — head = 25% of body weight → lands headfirst (`from_idx [3, 5]`) — **PASS**

Two-cloze, different numbers, so each card anchors the other (no R10). Both facts grounded
verbatim on p687. Back Extra adds the arms-can't-cushion mechanism and the index-of-suspicion
consequence — both in mark 4/5 context, neither restating the Text. `numeric` correct for 25%.

## Card 3 — nose breathers / <6 months (`from_idx [6]`) — **REWRITE**

**Check #2 / R3 leak, on the c1 card.** The stem said *"…especially susceptible to **nasal**
congestion…"* while `{{c1::nose}}` was hidden. The answer's own word sat visible three words
after the blank. Fixed by dropping "nasal" from the second clause ("susceptible to congestion
that can lead to viral upper respiratory infections") — still grounded, and "nasal congestion"
is restored in the Back Extra where it is shown *after* the answer.

**Check #16 / R6, secondary.** The Back Extra `Why:` line ("a blocked nose is a breathing
problem…") pre-answered card 4's vignette. Re-scoped to pure physiology ("no easy second
route, so even mucus can compromise ventilation") so card 4 requires the inference rather than
recognition of a neighbour.

The `::nose or mouth` hint is correct and stays — nose-vs-mouth is a genuine binary, so
check #13 *requires* the forced-choice form. It is not an R11 first-letter hint.

## Card 4 — choking-infant vignette (`from_idx [6]`) — **REWRITE**

**Check #18 / R9 open-set.** *"Parents hand you a 2-month-old… What do you make sure is
clear? `{{c1::the nasal passages}}`"* — "the airway", "the mouth and throat", "the airway of
foreign bodies" all fit that hole, and the classic reflex answer is "the airway". Nothing
visible forced the nose. Rewritten with the rejected alternative made visible, which is
card-rules #21(b)'s licensed fix: *"The mouth and throat are clear, yet the infant is still
struggling to breathe, so you check next for obstruction of `{{c1::the nasal passages}}`."*
Now forced cold; the discriminating knowledge (infant = nose breather) is still what gets him
there. Also fixed the sentence-fragment stem into human-flow prose (rule 3).

Kept as the ONE application card the brief licenses for infant airway. `numeric` true is
right per the brief's blanket rule (the "2-month-old" must sit inside the <6-month band).

## Card 5 — infant airway differences, Parker's margin card (`from_idx [7]`) — **REWRITE**

**The drafter's no-count call is CORRECT and I upheld it.** p688 reads *"Due to factors **such
as** the proportionally oversized occiput, the increased flexibility of the trachea, and the
infant's limited or absent ability to reposition…"* — an explicitly open list, and
`parker-preferences.md` forbids carding a "such as" list as a closed memorize-these set. No
count is stated or implied numerically; the four `<br><br>`-separated blank rows give him the
count on the front (R14) without the card asserting the source closed the list. **R7 does not
apply** (no stated count), and I read the whole of p688 to confirm nothing spills past the
context window — the passage is fully captured in marks 7 and 8.

**Check #3 grounding — the frame was mis-attributed.** p688 has TWO separate sentences:

1. *"An infant's **upper airway** is quite different from that of an adult. The infant's
   tongue is larger… and the airway is proportionally shorter and narrower."* → 2 items.
2. *"Due to factors such as the proportionally oversized occiput, the increased flexibility of
   the trachea…"* → a different, open list about why **positioning** is crucial.

The draft asked *"How does an infant's **upper airway** differ from an adult's?"* and answered
with all four. The occiput is not an airway structure at all and the trachea is lower airway —
the source never calls either an upper-airway difference. Lead-in re-scoped to what is
actually true and grounded: *"Compared with an adult, what is anatomically different about an
infant's **airway and head**?"* All four items kept (Parker asked for the whole set; both
extras are in mark 7's own context).

**Check #17 completeness.** The third member of the "such as" list ("limited or absent ability
to reposition") is deliberately NOT a row — it is a capability, not an anatomic difference, so
including it in an "anatomically different" set is a category error. It is now named in this
card's Back Extra `Why:` line (the draft omitted it there) and is the `Why:` line of card 6.

**R17/#24 clear:** every row LEADS with its cloze, so the items are the answers — not items
visible with filler punched out. This is exactly the shape Parker's margin comment asked for.

## Card 6 — positioning / hyperextend-hyperflex (`from_idx [7, 8]`) — **REWRITE**

Text unchanged and passes: the c1 pair (hyperextending / hyperflexing) are parallel members of
ONE set, not mutually-defining spans, so R10's MUST-NOT-OVER-FLAG applies — cover c1 and
"because both ___ and ___ the head and neck can easily produce an airway obstruction" still
forces the pair of opposite malpositions.

**Check #11 — Back Extra restated the Text.** The `Pitfall:` line ("the error runs both ways")
is literally what "both hyperextending and hyperflexing" already says. Replaced with a
`Meaning:` gloss that closes the prerequisite instead (rule 11): *"hyperextension tips the head
too far back, and hyperflexion lets the chin drop toward the chest."* Component order
normalised (`Meaning:` then `Why:`), semicolon removed.

## Card 7 — rib cage / belly breathing (`from_idx [8]`) — **REWRITE**

**Check #13 — unhinted coin-flip.** *"An infant's rib cage is `{{c1::less rigid}}`"* is a bare
direction blank: more-rigid and less-rigid both fit the visible stem, and card-rules #13 calls
an unhinted coin-flip unanswerable. Restructured per rule 18's GOOD pattern — keep the shared
scaffold visible, cloze only the crisp discriminator, and carry a forced-choice hint:
`{{c1::less::more or less}} rigid` and `the ribs sit {{c1::horizontally::orientation}}`.
c2 (diaphragmatic/belly breathing) was already forced and is unchanged.

## Card 8 — barotrauma (`from_idx [9]`) — **PASS**

Verified exactly what the brief asked me to scrutinise:

- **c2 is crisp.** "pressure-induced trauma to the lungs" = 5 words, inside R12's 3–6-word
  target for a two-way definition's meaning side. No tightening needed.
- **No parenthetical leaks the hidden term.** The card carries no parentheticals at all; the
  c1 card shows only the meaning and the cause, the c2 card shows only the term and the cause.
  Per R3's precision, a two-way definition is not a leak and must not be "fixed."
- c3 (forceful ventilations and overinflation) is forced by "the cause is ___ with a bag-mask".
- Back Extra teaches the fragility mechanism and the compensation trap — neither re-defines
  the term (required for a definition card). All grounded in mark 9's context.

---

## Coverage audit (no yellow mark dropped)

| Mark | Fact | Where tested |
|---|---|---|
| 2 | birth weight 6–8 lb (3–3.5 kg) | card 1 row 1 |
| 3 | head ≈25% of body weight | card 2 c1 |
| 4 | week-1 loss 5–10% from fluid loss | card 1 row 2 |
| 5 | regain wk 2, ~1 oz/30 g per day, ×2 by 4–6 mo, ×3 by 1 y | card 1 rows 3–5 |
| 5 | headfirst landing (context tail) | card 2 c2 |
| 6 | nose breathers · <6 mo congestion · clear the nose | cards 3 + 4 |
| 7 | tongue · airway calibre · occiput · trachea | card 5 (4 rows) |
| 7/8 | hyperextend/hyperflex obstructs | card 6 |
| 8 | rib cage less rigid, ribs horizontal → belly breathing | card 7 |
| 9 | barotrauma + cause | card 8 |

## Things consolidation must know

1. **FIGURE 7-2 is NOT wanted on any card in this unit** — the fontanelle marks (14+) belong to
   unit C. No card here is `needs_visual`; none needs `visual_source`.
2. **Two facts are intentionally visible-but-untested**, both as situational framing, not
   oversight: *"airway obstruction is more common in infants than in older children and
   adults"* (card 5 lead-in — alone it is a one-word coin flip) and *"which can lead to viral
   upper respiratory infections"* (card 3 — clozing it would create an R9 open-set blank).
3. **Three Back Extra lines are grounded inferences, not verbatim source.** Recording them so
   nobody later mistakes them for fabrication or "corrects" them:
   - card 1 `Ex:` — arithmetic on the source's own doubling/tripling rule (card is already
     `needs_human_check`);
   - card 6 `Meaning:` — plain-English gloss of hyperextension/hyperflexion (word meaning, not
     a clinical claim; closes the prereq per rule 11);
   - card 7 `Pitfall:` — corollary of "typically seen in infants". **Independently confirmed on
     p689**, which carries a Special Populations box: *"When you are counting respirations in
     an infant, count the number of times the abdomen rises instead of concentrating solely on
     the chest rise."* That box is not itself highlighted, so it is not carded, but it settles
     that the inference is sound.
4. **Dedupe watch (unchanged from the drafter's note):** card 2 owns head-size-as-proportion.
   If unit C also cards "the infant head is proportionally large", keep card 2 — it carries the
   headfirst-fall consequence — and drop the duplicate.
5. **Numeric/human-check flags:** cards 1–4 true, cards 5–8 false. Verified against every digit
   in the unit (6–8 lb, 3–3.5 kg, 25%, 5–10%, 1 oz, 30 g, 4–6 months, 1 year, 6 months,
   2-month-old).
6. The `.verified` stamp on this file is from the post-edit run and will be invalidated by the
   merge into the chapter file.
