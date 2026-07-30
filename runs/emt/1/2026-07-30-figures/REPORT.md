# Chapter 1 figure run — 2026-07-30

The third figure pass, run to keep finding kinks before Chapter 7. Chapter 6 was anatomy
with modern provenance; Chapter 4 was photographs with none; Chapter 1 turned out to break
something neither of them touched.

**Outcome:** 2 of 32 cards carry a figure. That is the correct answer, not a failure — see
below. Running total across the three chapters: 69 cards with figures, 0 doubled, 0 images
on any question side, all three gate clean and stamp.

| | Ch1 | Ch4 | Ch6 |
|---|---|---|---|
| cards | 32 | 105 | 202 |
| figures in chapter | 9 | 21 | 45 |
| with a figure, after judging | **2 (6%)** | 16 (15%) | 51 (25%) |

---

## The bug this chapter found: card order is not universal

`backfill_provenance.py` recovers which mark a card came from in two passes — anchor on
strong text overlap, then interpolate between anchors on the assumption that **card order
tracks mark order**, because the generator walks the chapter in order. That held for
Chapter 4 (67 anchors, 59 forming one consistent run, 104/107 resolved).

Chapter 1 collapsed to **6 spine anchors and 12 of 32 resolved.**

The anchors were not wrong. I checked them by hand: card #0 → the rules/knowledge/skills
failure mark, card #1 → the licensure-levels mark, and three separate cards correctly
sharing the one off-line/online medical-control mark. What was wrong was the *assumption*.
Chapter 1's sequence runs `0→30, 1→3, 2→20, 4→8, 5→31` — no monotone structure at all,
because Chapter 1 went through the heaviest consolidation of any chapter (33 notes from 36
highlights, after many rounds of Parker-caught rewrites). Generation order did not survive.

### The fix: stop needing card order at all

The matcher never actually wanted the *mark*. It wanted the **page**. That can be read
straight off the source — score each page of the chapter against the card's own text and
take the best — with no ordering assumption, and it works identically on a legacy chapter
and a fresh one. Added as pass 3, writing `source_page` on every card it can place.

**Chapter 1: 29 of 32 located, against 12 via marks.**

The two methods are independent, so where both speak they are a genuine cross-check, and
the run now prints it:

| | agree | disagree |
|---|---|---|
| Ch4 | 91 | 4 |
| Ch6 | 174 | 5 |
| Ch1 | 6 | 5 |

96–97% agreement on the two chapters with sound provenance is what validates the new pass.
Chapter 1's poor agreement is the mark side failing, not the page side: every remaining
disagreement there is a card scoring **0.05–0.29** against its mark's page and **0.45–0.77**
against the located one. Three separate cards had latched onto one false anchor on p77.

### A second bug inside the fix: the chapter restates itself

The first version of page-location put card #1 on p88 instead of p73, #8 on p125 instead of
p97, #13 on p90 instead of p74 — all **exact ties**, 0.73 vs 0.73.

p125 is the **chapter glossary**: *"credentialing — An established process to determine the
qualifications necessary to be allowed to practice…"*. A chapter condenses itself at the
end, in the glossary and the "Ready for Review" recap, so a definition card matches the
summary exactly as well as the prose that taught it.

Fixed by breaking ties toward the **earliest** page: the body always precedes the recap,
and it is the body that has a figure beside it. All three ties then resolve to the correct
page, and Ch4/Ch6 agreement was unaffected.

---

## Why 2 of 32 is right

Chapter 1 is EMS Systems — licensure levels, medical direction, quality improvement, scope
of practice. Almost nothing in it is picture-shaped, and its 9 plates are mostly generic
scene photography. The judge kept 2 of 6 proposals:

**KEPT**
- FIGURE 1-3 (a Venn diagram of Medical direction / State EMS offices / National Scope of
  Practice Model) on *"because licensure is a **state** function…"* — coverage 1.00, and the
  diagram labels "State EMS offices — regulatory role" outright. The best match in the
  chapter.
- FIGURE 1-2 (a training classroom) on the **certification** card — congruent, not strictly
  needed. Exactly the class Parker wants kept.

**DROPPED**
- FIGURE 1-4 (a law-enforcement officer giving care) on the **AEMT** card. The plate shows an
  *EMR*. Wrong certification level — misleading rather than merely unrelated, and the same
  species as Chapter 6's sensory-nerve-on-a-motor-nerve-card.
- FIGURE 1-4 on a **medical director's authority** card — a responder giving care does not
  depict who may limit a scope of practice.
- FIGURE 1-2 (classroom) on the **four licensure levels** card and on the **EMR definition**
  card — one classroom depicts no hierarchy of levels, and FIGURE 1-4 is the EMR plate.

A chapter of abstractions should get few pictures. The pipeline reporting 6% here and 25%
for anatomy is the signal working, not failing.

---

## The other thing this run caught: the figure writers were unguarded

While starting this chapter, `SKILL.md` and `CLAUDE.md` had gained an **authorship guard**
from a concurrent session, added after a real incident: a pass decided a card's ETHICS
mnemonic was fabricated because it was not in the textbook, replaced it, and reported the
catch. The mnemonic was Parker's own.

`attach_figures.py` and `judge_figures.py --strip-live` both write `Back Extra` on live
notes and **consulted none of it.** Every card predating the store is `unknown`, which the
guard protects — so a strict reading would have blocked the figure stages entirely on the
existing deck.

The answer was not a bypass but a **second verified predicate**, `is_figure_only_change()`:
strip every pipeline-owned `<img src="emt_…">` from both sides, normalise the break runs
they sat in, and require the residue to be identical. Attaching and stripping a figure pass;
anything else does not. Parker's own pasted images never carry the `emt_` prefix, so they
survive into the residue — which means **removing his screenshot still fails the guard**,
which is the case that matters most. Both writers now guard before writing and record after,
and the self-test grew 8 → 13 cases covering exactly that.

Deliberately **not** done: back-filling authorship records for the 67 figures attached to
Chapters 4 and 6 before the guard existed. The module's own rule is that recording a field
we did not author is worse than recording nothing, because it converts one of Parker's edits
into something a future pass believes it owns. Those fields stay `unknown`; the `figure_only`
predicate is what lets the pipeline still manage its own figures there.

---

## Still open

1. **Per-figure reverse matching** — still the top item. The matcher optimises per-card only.
2. **Chapters 2, 3 and 5** have not had provenance backfilled or figures attached.
3. **Vector figures remain untested** — all three chapters were 100% raster. Ch1's TABLE 1-5
   was skipped for having no locatable art and is a candidate.
4. **Chapter 1's three unresolved cards** (`from_idx` null, no `source_page` above threshold).
5. The cross-check is **printed, not enforced.** A large disagreement rate is a real signal
   that one method is broken for that chapter; right now a human has to read it.
