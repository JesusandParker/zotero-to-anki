# Physics ch2 — Describing Motion: Kinematics in One Dimension

Giancoli 7e, physical pp. 42–55 (printed 21–34). **31 marks → 33 notes**, all written to
`…::PHYS 201 - General Physics I::Chapter 2 …::Book Highlights`, tagged `physics-ch2`.

## Scope
Parker asked for "2-1 through 2-7, nothing past that" and thought his marking ran to the
end of 2-8. **His marks actually stop on printed p. 34**, four paragraphs into 2-7 (Freely
Falling Objects, which starts on printed p. 33). Section **2-8 Graphical Analysis** starts
on printed p. 39 and carries **no marks at all**, so nothing from it was carded — his
"nothing past that" and the marks agree; only his page estimate was off. Section 2-6
(Solving Problems) is unmarked too, which is expected for a worked-examples section.

Every one of the 31 marks is cited by at least one card (`from_idx` coverage 31/31).
Nothing unmarked was carded (card-rules #29).

## Margin comments, and what each one did
| Page | Comment | What happened |
|---|---|---|
| p23 | *"…if I highlight these formula numbers to me that's meaning I want to memorize the actual formula"* | **Now a standing rule for this book.** A yellow mark on an equation NUMBER produces its own formula card. Applied to (2-1), (2-3), (2-4), (2-5). |
| p25 | *"this means i want the equ"* (truncated) | Read as the same instruction → Eq. 2-3 card. |
| p29 | *"all of the cinematic \[kinematic\] equations as individual flashcards without any derivations and just the equation… break down every single variable"* | Four separate notes, one per equation, no derivations, every symbol defined in `Meaning:`. |
| p21 | `™™¡™` | Junk keystrokes, not a comment. Surfaced, not acted on. |

Eq. 2-1 has **no symbolic form in the book** — it is written in words. So the "definition"
and "formula" he asked for became the two halves of one two-way note (#9) rather than two
duplicate notes.

## Judgement calls
- **MathJax** for every symbolic equation (`\(v = v_0 + at\)`). Verified safe: no cloze
  answer contains a `}}` sequence, which would truncate Anki's non-greedy cloze parse.
  Confirmed live-safe by his own collection — **246 of 400 sampled notes already put
  MathJax, `\frac` included, inside a cloze deletion.** `render_check.py` shows the raw
  source because the harness runs no JS; that is the documented headless limitation, not
  a defect.
- **The fifth kinematic-equation card (validity) — cut, then added on his say-so.** The
  leak that motivated the cut was real: cards 25–28 opened *"For motion with **constant
  acceleration**, give the kinematic equation for…"*, putting the new card's answer on four
  fronts. Rather than accept it, the four stems were re-cued *"Among the four kinematic
  equations, give the one for…"* — naming the set without stating the condition. The
  condition still sits on all four BACKS, which is an endorsed confusable cross-link, not a
  front-side leak. The four live notes were rewritten in place (authorship: `owned`).
- **Four lexicon cards** (translational motion, particle, magnitude, vectors). Three are
  `external` and reach him in the VERIFY report's Vocabulary block; **magnitude** anchors
  `in_source` to p44 — his own page — after the R61 fix below.

## Cleared warnings (`check_cards.py`, 0 hard / 8 warnings, all adjudicated)
- **5 × long-blank (R8)** on #15/#17/#20/#22/#26 — each blank is a single equation, and
  `card-recipes.md` §5 Template B requires the whole formula inside one cloze.
- **3 × lexicon external-anchor** on #2/#3/#8 — `--find`'s matches are the wrong sense
  (a momentum heading, graph-reading prose, a front-matter notation note). Recorded per
  card in `verified_by`.

## Figures — 22 proposed, 11 kept, 11 rejected
The judge-look **inverted the matcher on its top-scoring pair**: FIGURE 2-2 matched the
reference-frame card at 1.00, but that file is the falling-pinecone art, not the train.
Dropped, and FIGURE 2-1 was force-added to the translational-motion card instead (the
matcher scores cloze answers only and had given it 0.00). FIGURE 2-20, the ball-and-paper
drop, was likewise forced onto the free-fall card. Four "figures" (2-6, 2-11, 2-12, 2-21)
were page-region renders carrying body-text bleed and were rejected on the complete-plate
bar. Post-mortem: **no anomalies**; 11 of 32 live notes carry a plate.

## Evidence storage
`visual_source` originally pointed at `work/physics/page_NN.png` — scratch renders, which
were deleted at commit time and silently hard-blocked card #14 on the next gate run. The 13
affected cards now cite crops filed in this run's `figures/`, the home
`reference/provenance.md` names for exactly this, and `work/*/page_*.png` is gitignored so
no future card can cite a scratch file again.

## Hazards found and closed
- **R61** — `lexicon.py --find` took the first definition-shaped sentence in book order,
  so all four purple words anchored to unrelated pages. Fixed with `_pick_nearest()`
  (prefer the candidate nearest the marked page; stamp `far_from_mark` past 25 pages).
- **R62** — `run_store.record()` wrote an extensionless file for a bare stem, and
  `anki_write.py --run` then refused the write with a misleading error. Fixed with
  `_named()`.
- **R63** — `check_cards.py --live all` interpolated the deck root UNQUOTED, so any deck
  name with a space matched nothing. The card-rules #32 sweep had been answering *"checked
  0 cards, deterministic checks clean"* for physics, genetics and Arabic — **341 live notes**
  — while only EMT (`all::EMT`) was ever really examined. A guard that reports success on an
  empty set is the one failure mode that makes every future remediation believe it finished.
  Fixed; swept properly afterwards with **0 hard errors** across all three.
- **Vector-render bleed** — not new (SKILL.md Stage 2.9 documents it); `mechanizable:
  false`, because the judge-look is the correct guard and it worked.


## Second pass — what a cold re-read found (2026-08-31)

Parker asked whether the cards were really perfect. Re-reading all 33 against the pages,
rather than re-running the gates (which were green, and green by construction cannot see
what they do not model), turned up **seven defects in six cards**. Every gate had passed
all of them: none of these is a shape `check_cards.py` models.

| Card | Defect | Fix |
|---|---|---|
| 25 | **Factual error.** The Cue called \(v = v_0 + at\) "the only one of the four with no position term" — but \(\bar v = (v + v_0)/2\) has no position term either. | Re-cut to the claim that IS unique: the only one carrying both \(a\) and \(t\) with no position. |
| 9 | The Pitfall said averaging 50 and 100 km/h "does not come to 75 km/h". False when the legs take equal **time** — then 75 is exactly right. | Replaced with the book's own equal-**distance** example: 100 km at 50, 100 km at 100 → 67 km/h. |
| 12 | "an average velocity of only 0.57 m/s" — that is the *magnitude*; the card teaching displacement-vs-distance is the last place to drop direction. | "0.57 m/s **east**". |
| 13, 15 | "the equation for average velocity" is ambiguous **inside this batch** — card 28 gives \(\bar v = (v+v_0)/2\), also an equation for average velocity (rule 2). | Both stems now read "the equation **defining** average velocity". |
| 23 | "moving to the left along a decreasing \(x\) axis" — the axis does not decrease, \(x\) does. | Reworded. |
| 26 | Two distinct ideas crammed into one `Pitfall:` line. | The \(x_0 = 0\) point moved into the `Cue:`, where the other \(x_0\) material lives. |

**Still standing, and Parker should judge them in review rather than take my word:**
- Cards 13 and 15 test the same equation in words and in symbols; 12 tests the concept
  behind it. Three cards on average velocity's definition is defensible only because he
  marked those three spans separately and asked for definition-and-formula as separate
  things. If it reads as redundant in review, 13 is the one to delete.
- The motorcycle plate on cards 19 and 21 illustrates *acceleration* generally rather than
  those cards' specific claims — the weakest two of the eleven attachments, kept under his
  stated "overshoot rather than undershoot" preference.
- Card 9 (average **speed**) carries the displacement plate, whose largest label reads
  "Displacement". Its back explains the doubling-back the plate shows, so it holds together
  — but it is the attachment most likely to make him ask why it is there.
