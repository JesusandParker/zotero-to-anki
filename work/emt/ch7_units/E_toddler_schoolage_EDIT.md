# Unit E — editor verdicts (marks 23–36)

Adversarial pass over `E_toddler_schoolage_cards.json`. 10 notes → 19 cards (unchanged count).
**5 PASS · 5 REWRITE · 0 DROP.** Checker: 0 hard, 1 warning (card 9, cleared below).

| # | Fact | Verdict | What I did |
|---|---|---|---|
| 0 | lung musculature limit | REWRITE (cosmetic) | Text untouched — c1 "musculature" is forced by the *but*-contrast with structural growth plus "cannot sustain … for long"; c2 is one concept, not an open set. Back Extra was a single 38-word block holding two distinct ideas → split into `Why:` (the oxygen-demand purpose, grounded, new) + `Pitfall:` (power vs surface). |
| 1 | passive → acquired immunity | REWRITE (Back Extra) | Text passes: c1 anchored by the visible "acquired immunity" counterpart (a paired term, not a definition — not an R3 leak); c2's two spans are parallel members of one set (R10 must-not-over-flag), GI distress is the yield. Old `Pitfall:` restated c3's own answer → replaced with a real `Distinguish:` between the two confusable immunities. |
| 2 | brain 90% of adult weight | PASS | Single forced number, `::percentage` is a form-label, numeric+HC set, age band grounded in mark 23's context and the brief's verified band list. |
| 3 | toilet training (3 numbers) | PASS | Verified against marks 26+27: all three numbers tested, none scenery — 12–15 mo (c1), 18–30 mo (c2), 28 mo (c3), each under its OWN number so the other two stay visible as anchors. Physiologic-vs-psychological IS the axis (the italicised *psychologically* carries it). Prose, not rows → correctly no `<br><br>` (R14 must-not-over-flag). |
| 4 | language milestones | PASS | Two numbers, separate clozes, each anchored by the other. |
| 5 | cause and effect at 18–24 mo | REWRITE (cosmetic) | Text untouched. Back Extra was one 38-word run holding two unrelated facts → split into `Cue:` (social gains) + `Ex:` (role models → gender differences). |
| 6 | parent as secondary patient | REWRITE | Real decision card, not a definition in costume — it asks what the parent *has become on scene*, and the source gives no management action to invent. Cloze is 2 load-bearing words (R8/#15 OK) but the article was inside the brace → moved out. Invented panic behaviours ("shouts, shakes") pulled back to the source's own "overwhelmed … causing panic". Back Extra `Why:` had become a restatement of the new stem → replaced with `Cue:` carrying the *general* rule (look for the second patient on any peds call), which is the edge the Text doesn't state. |
| 7 | school-age annual growth | PASS | Both numbers clozed with their units inside the deletion, numeric+HC set. Teeth/hemispheres correctly in Back Extra (not yellow). |
| 8 | three levels of moral reasoning | REWRITE | R10 verified **per direction**: c1 hidden → the three drivers are visible and force the three names; c2 hidden → the three names are visible and force the drivers. Both directions answerable ⇒ licensed contrast, NOT a husk. Kohlberg independently re-confirmed absent (0 hits in `chapter_7_highlights.json`) — correctly unnamed. **The real defect:** row 1's driver was "consequences — punishment or incentive", which is the *unhighlighted neighbour sentence*, leaving mark 33's own yellow clause untested (Rule 1). Swapped in "external forces such as parental discipline"; the consequences criterion moved into `Distinguish:`. Bonus: all three rows now share one axis (outside authority → the group → the self), and the lead-in says "answering to a different influence" so the c2 card knows what form it owes. |
| 9 | self-concept vs self-esteem | REWRITE — **the flagged failure, fixed** | See below. |

## Card 9 — how the self-concept card was fixed

The drafter's own flag was right, and the card was worse than flagged. Under one `c2` it hid
three generic single words: `perception`, `feel`, `peers`. Two are wide-open (R16) —
*view / image / opinion / sense* all fill "our ___ of ourselves", and "how we fit in with our
___" admits *friends / classmates / others / social group*. The `c1` direction was fine.

**Fix: re-scope the deletions so each `c2` span is a whole discriminating definition anchored by
its own VISIBLE term** — the blessed two-way shape (R3 precision), rather than a bare noun with
nothing forcing it:

`{{c1::Self-concept}} is {{c2::our perception of ourselves}}, whereas {{c1::self-esteem}} is {{c2::how we feel about ourselves}} and how we fit in with our peers.`

- **c1 card** (unchanged in force): both definitions visible → both names forced.
- **c2 card**: both terms visible as anchors, and the peer-fit clause stays visible — it is the
  discriminator that clinches which side is which, and it is exactly the span that could not be
  guessed, so it must not be a blank. Each answer is now 4–5 words (R12 crisp) and the recall is
  the *contrast* (perception vs feeling), which is the actual teaching point of the pair.
- No hint added anywhere. The parent agent was right that no hint can force "perception" without
  leaking it — the answer to that is to stop asking for the bare noun, not to bolt on a hint.
- Back Extra: old `Distinguish:` re-defined the terms the card defines (card-rules #5). Now a
  picture-vs-verdict hook + the school-age timing (the one genuinely new fact in the context).
  Digits deliberately kept out of Back Extra so the card stays honestly non-numeric.

**Checker warning on card 9 is CLEARED, do not "fix" it.** `husk_groups` fires ("c2 hides 2
multi-word spans"), which R10 documents as deliberately generous. Litmus applied: cover both c2
spans and the visible remainder still carries **both entity anchors** plus the peer clause —
this is verbatim R10's licensed multi-dimensional contrast ("do not fix a genuine contrast card
into split singletons"). Splitting to c2/c3 would also let a *non-knower* decode each blank by
contrast with the other, which fails rule 3's median in the opposite direction.

## For consolidation

1. **Mark 28 is genuinely covered — verified, not assumed.** Unit D's third card
   (`D_infant_psychosocial_cards.json`, `from_idx [21]`) carries "peaking between
   `{{c3::10 and 18 months}}` of age". Same fact, same digits as mark 28. Unit E owes no card.
   **Action: add `28` to that card's `from_idx`** so the mark is provably covered rather than
   silently dropped.
2. **Every mark 23–36 is covered.** 23→c0/c1/c2 · 24→c1 · 25→c2 · 26+27→c3 · 28→unit D ·
   29→c4 · 30→c5 · 31→c6 · 32→c7 · 33+34+35→c8 · 36→c9. Nothing flagged uncardable.
3. **Checker-precision note worth logging.** The ORIGINAL card 9 passed silently and the FIXED
   one warns. `husk_groups` uses a multi-word-span proxy, so blanks that are too *small* — the
   generic single words that make a card R16-open-set — slip under it, while the correct crisp
   phrasing trips it. The silence was the defect and the warning is benign. R16 still has no
   mechanical proxy outside `open_set_absolute` (absolute sentences only), and this unit's worst
   card was exactly the shape that gap leaves uncovered.
4. **Overlaps to reconcile:** "autonomy versus shame and doubt" sits in card 3's Back Extra only
   (not clozed) — if unit D cards Erikson's stages, keep it one card. Card 9's Back Extra notes
   moral reasoning continuing through adolescence; unit F may own that fact.
5. **Numeric/HC flags:** cards 2, 3, 4, 5, 7 are `numeric: true` + `needs_human_check: true`
   (every age, month range, percentage, weight and height). Cards 0, 1, 6, 8, 9 carry no digits
   in either field and are correctly unflagged.
6. **Figures:** nothing required. Marks 31 and 32 are `needs_visual` + `page_sparse`, but both
   answers sit verbatim in their own context, so R13 does not fire and `visual_source` stays
   `null` — re-confirmed by the clean grounding run. FIGURE 7-5/7-6/7-7 are age-group photos and
   would be congruent-but-unnecessary on cards 0–5/7 if the matcher wants them.
