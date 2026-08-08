# Science profile

For Liberty coursework and science reading — genetics, biochemistry, anatomy, organic
chemistry, general biology — whether the source is a textbook chapter or a lecture deck.

---

## 1. What it's for
A **single professor's exam**, which is the important difference from EMT. What gets tested
is idiosyncratic to that instructor, and a highlight in a lecture PDF carries the strongest
possible signal about it: Parker marked it *while the professor was talking*.

Related but distinct: the `course-to-anki` skill is the *scoring* pipeline that infers what
matters from a whole course's materials when nothing is highlighted. This profile is for
when Parker has already marked what matters. Don't rebuild scoring here.

## 2. Archetype mix
- ~30% mechanism / causal chain / pathway (`card-recipes.md` §7) — the heart of science recall
- ~20% definitions and term↔meaning (two-way) (§4)
- ~15% comparison and direction-of-change (§8) — up/down, more/less, which enzyme
- ~15% classification and enumeration (§6)
- ~10% numbers, ratios, values (§5)
- ~10% application / problem-shaped ("given this cross, what ratio") (§9)

Lecture decks skew further toward mechanism and comparison than textbook chapters do,
because slides carry the professor's framing rather than the book's completeness.

## 3. Lecture sources specifically
- **Margin comments are the highest-value signal in the file.** In a lecture PDF Parker's
  comments are him reacting in real time — *"NOT ON THE EXAM"*, *"this is a lot of
  bioethics"*, *"these are subjective so dont just mem"*. Read every one and obey it:
  - an exclusion ("not on the exam", "not in the slides", "don't just memorize") means
    **do not card it**, or card only the part he indicated — this is the one licensed
    exception to "never drop a marked span," because he is explicitly overriding himself;
  - a question means answer it at hand-off, grounded in the source;
  - an emphasis ("know all of these") means be exhaustive.
- **Slides are terse.** A slide bullet is often not a sentence and won't stand alone. Prereq
  closure (card-rules #11) matters more here than anywhere: fold in the one-clause
  definition or make the sibling card, grounded in the surrounding slide text.
- **A figure Parker area-selected is the card.** Crop it (`render_page.py --crop-from`) and
  author from the image rather than trying to describe it in words.

## 4. Traps
- **Don't card the pathway as one un-recallable blob.** A 7-step pathway is one grouped
  sequence card (§7), not a single blank hiding seven names (R12).
- **Don't turn a mechanism into a definition.** If the highlight explains *why* something
  happens, the card should test the causal link, not the noun.
- **Numbers in science are usually derived, not memorized.** Prefer carding the
  relationship over the value, unless the professor emphasized the value itself.
- **Diagrams beat prose** for anatomy and structure — use the image path, and remember
  image occlusion is the eventual home for these (see the Grant's Atlas work).
- **Purple on a lecture PDF will usually anchor `external`** — slides use jargon without
  defining it and have no glossary, so authored definitions landing in the verify
  report's Vocabulary block is the NORMAL outcome here, not a warning sign. A purple word
  on a slide is also often exactly the prerequisite card-rules #11 wants — one lane
  feeds the other.
