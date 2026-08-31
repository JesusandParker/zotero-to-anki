# Physics ch2 — Describing Motion: Kinematics in One Dimension

Giancoli 7e, physical pp. 42–55 (printed 21–34). **31 marks → 32 notes**, all written to
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
- **No fifth kinematic-equation card** for the constant-acceleration validity condition.
  It would have to name or show the four equations to be answerable, leaking them. The
  condition is on all four backs instead. Offered to Parker.
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

## Hazards found and closed
- **R61** — `lexicon.py --find` took the first definition-shaped sentence in book order,
  so all four purple words anchored to unrelated pages. Fixed with `_pick_nearest()`
  (prefer the candidate nearest the marked page; stamp `far_from_mark` past 25 pages).
- **R62** — `run_store.record()` wrote an extensionless file for a bare stem, and
  `anki_write.py --run` then refused the write with a misleading error. Fixed with
  `_named()`.
- **Vector-render bleed** — not new (SKILL.md Stage 2.9 documents it); `mechanizable:
  false`, because the judge-look is the correct guard and it worked.
