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

## 3b. Physics and any equation-carrying source
- **A yellow mark on an EQUATION NUMBER means "card the formula itself."** Parker stated
  this in the margin of Giancoli p23 (2026-08-31): *"if I highlight these formula numbers
  to me that's meaning I want to memorize the actual formula."* So `(2-1)`, `[average
  acceleration]`, an equation label — any of them marked yellow — is a request for a
  `card-recipes.md` §5 Template B card, separate from whatever prose definition the
  neighbouring highlight produces. When the book's equation exists only in WORDS (Giancoli's
  Eq. 2-1 is literally *average speed = distance traveled / time elapsed*), the definition
  and the formula are the two halves of one two-way note rather than two duplicate notes.
- **Break down every symbol on the back.** His standing request: *"tell me what each of the
  letters are, right, \(x\) with the subscript of zero, like what that means — break down
  every single variable in the equations."* A `Meaning:` line naming each symbol, spelling
  out subscript-zero as "initial", is required on every equation card, and *"without any
  derivations"* — the equation, not how it was obtained.
- **Cue each equation by what it relates, never by its number.** Four kinematic equations
  cannot share the stem "give the kinematic equation" (rule 16, open-set). Distinguish them
  the way the book's own worked examples do: which variables each connects, and which one is
  missing (*"the one with no time term in it"*).
- **MathJax is the right register for symbols, and it has one hard trap:** Anki's cloze
  parse is non-greedy, so **any `}}` inside a cloze answer truncates it.** `\frac{\Delta
  x}{\Delta t}` is safe; `\frac{\text{distance}}{\text{time}}` is NOT (the inner `}`
  meets the group's `}`). Write word-formulas as plain text with `/`, keep MathJax for
  symbols, and assert no cloze answer contains `}}` before staging.

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
