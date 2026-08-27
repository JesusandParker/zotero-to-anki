# Block E — editor log

**File:** `work/physics/drafts/block_E_edited.json` — 9 notes → 13 Anki cards, all 9 survive.
**Verdicts:** 3 PASS · 6 REWRITE · 0 DROP.
**Gate:** `check_cards.py` clean in both default and `--require-provenance` mode; zero HARD, zero warnings.

Grounding was re-established first-hand this run: `work/physics/page_31.png` re-read, and
TABLE 1-5 plus both paragraphs cropped and upscaled (3× / 2.2×) before any verdict.
I did **not** trust the supplied transcription. Two notes on it:

- The paragraph transcription (a) matches the page **word for word**.
- Transcription (b) **omits a sentence that is on the page**: *"The corresponding units for
  these quantities are called base units and derived units."* (The drafter caught this too.)
- TABLE 1-5 re-counted: exactly **7** rows, in order —
  Length/meter/**m** · Time/second/**s** · Mass/kilogram/**kg** · Electric current/ampere/**A** ·
  Temperature/kelvin/**K** · Amount of substance/mole/**mol** · Luminous intensity/candela/**cd**.
  **All four abbreviations in this block (A, K, mol, cd) are correct and correctly cased.**

---

## Per-card verdicts

| | Verdict | What changed, and why |
|---|---|---|
| **S1** SI → Système International | **REWRITE** | Added the slot-label hint `::its French name`. **Check 1 / check 18:** with the answer covered, *"SI … stands for ___"* admits **two** defensible fills — the book's *Système International* and the ordinary English *International System (of Units)*, which is what most English sources say SI stands for. A knower could produce the wrong one and self-grade himself down. The hint names the answer's **form** (rule 4), cannot replace the answer (check 9), and is not a letter hint (check 20). `Meaning:` reworded to *"in English, Système International is 'International System.'"* so it delivers the translation instead of half-restating the new stem (check 11) and does not open on a pronoun (Layer A #2). |
| **S2** SI used to be the MKS system | **REWRITE** | Back Extra only. The old `Meaning:` called meter-kilogram-second *"the three standards the system is built on"* — which **contradicts T1** (the SI rests on **seven** base quantities) in the exact place he looks after answering, and T1's own Pitfall exists to kill that misconception. Replaced with the acronym's order mapping: *"the SI's standards of length, mass, and time, in that order"* — grounded, scoped, new information (M→length, K→mass, S→time is the non-obvious bit), no tension. Text untouched: `::acronym` is a genuine form label and is what closes the blank against *"metric"* (check 1). The expansion stays **back-only** on purpose — on the front it would spell out its own initials (rule 18). |
| **S3** the pound is a standard of force | **REWRITE** | Hint normalized `::force or mass` → `::force/mass`, matching rule 13's prescribed `::option/option` notation and the live deck's house style (#1 `classical/modern`, #48 `uppercase/lowercase`). Substance upheld — see ruling 3. |
| **T1** the SI has seven base quantities | **REWRITE** | **Two independent faults, both in the trailing clause** *"— the smallest number consistent with a full description of the physical world"*: (a) **out of scope (rule 29).** That claim lives in the ***Base vs. Derived Quantities*** section, a different section from the one Parker was asked about; the ask named *the SI/MKS/cgs systems paragraph and the seven SI base quantities table*, and rule 29 is explicit that *"sure do this"* about one paragraph and one table authorizes **that paragraph and that table — not the page.** (b) It duplicates **live #51's `Why:` line** in substance (rule 12) while riding along **untested as visible scenery** (check 4) — the drafter's own fact-pass classed it "SUPPORTING … T1 stem framing", i.e. never tested. **Clause cut, card kept:** *seven* itself is squarely in scope (the table has exactly seven rows and the ask literally says *"the seven SI base quantities table"*). Also fixed a category slip in the Pitfall: it called the meter/second/kilogram *"those three [base quantities]"* — those are **units**, not quantities. |
| **T2** the other four base quantities | **REWRITE** | Back Extra only. The `Distinguish:` line — *"length, time, and mass are the mechanical three; the other four are what a mechanics-only description of nature leaves out"* — is **ungrounded (check 3 / rule 10).** Neither *"the mechanical three"* nor the mechanics-only claim appears anywhere on p31. The drafter's §7 defends *"the mechanical three"* as a labelling scaffold under rule 23.1, and that half is fair — but it never addresses the **second half**, which is a substantive interpretive physics claim imported from outside the page (and a shaky one: temperature is not obviously outside a mechanical description). Replaced with the grounded edge the front does **not** already state: *"the meter, the second, and the kilogram already cover length, time, and mass — these other four are the base quantities those familiar standards leave out."* Text untouched — see the verification below. |
| **T3** electric current ↔ ampere (A) | **PASS** | Abbreviation re-read at 3×: **A**, capital. Two-way via c1/c2, no husk (rule 17). |
| **T4** temperature ↔ kelvin (K) | **REWRITE** | **Factual fix.** The Pitfall read *"the degree Celsius is not an SI base unit — **only the kelvin is**"* — which states that the kelvin is the SI's **only** base unit. That is false: the meter, second, kilogram, ampere, mole and candela are base units too. Rescoped to *"not the SI base unit **for temperature** — the kelvin is."* Abbreviation **K** confirmed; *"carries no degree sign"* is a direct read of the table's `K` cell. |
| **T5** amount of substance ↔ mole (mol) | **PASS** | Abbreviation **mol** confirmed, lowercase. |
| **T6** luminous intensity ↔ candela (cd) | **PASS** | Abbreviation **cd** confirmed, lowercase. |

Nothing was dropped. **No card strays outside the authorized scope** once T1's clause is cut —
S1/S2/S3 come from the Systems-of-Units paragraph, T1–T6 from TABLE 1-5, and every Back-Extra
line traces to one of those two units of text (the negative readings — *charge/voltage/resistance
are not base quantities*, *luminous intensity is the only one concerning light* — are readings of a
table the source states is exhaustive, not imports).

---

## The three flagged items

**1. S1 one-way vs. Parker's two-way default — the drafter is RIGHT. Upheld.**
Parker's two-way rule carries its own exit in its own text: *"go single-direction only when just
one direction is useful."* A term↔meaning pair two-ways because the meaning is not recoverable
from the term's letters; an **abbreviation↔expansion** pair is not that shape. The reverse card
would read *"Système International is abbreviated ___"* with both initials sitting visible on the
same line — rule 18's first-letter leak in its purest form, and Parker's own verdict on that shape
is *"literally giving away the answer, an easy copout."* One-way kept. (I added the form hint
above for a different reason — the forward direction was the one that had two answers.)

**2. "Seven" on live #51/#52 backs — the drafter is RIGHT. It holds, and it is now cleaner than it was.**
Check 16's defect is a card answerable by pattern-matching a neighbour **at answer time**. A
statement on a *back* is only visible **after** that card has been answered, so it functions as
prior exposure — the same prior exposure the textbook itself provides — not as an available crib.
Rule 12 is likewise not engaged: #51 and #52 *mention* seven while defining base/derived
quantities; neither **tests** it. Two additions from me: (a) the number is now stated on exactly
**one visible side** in the whole deck, because I cut it from T1's own front-side scenery, so T1 is
unambiguously the single testing site; (b) I did **not** touch #51/#52 — correct call under rule 32
/ `authorship.py` (they are live and not this pass's to edit).

**3. S3's forced-choice pair — the drafter is RIGHT on substance, and the form is now house-style.**
It is **not** answerable by elimination, and the reason is worth stating precisely: the stem's two
parallel rows (foot→length, second→time) leave *mass* as the missing member of the familiar
length/mass/time trio, so **elimination produces MASS — the wrong answer**. The pair therefore sets
the trap the card exists to spring rather than solving it. A bare slot-label like `::physical
quantity` would leave *force / mass / weight* all open and fail rule 2. Checks 9 and 13 both pass:
the hint cannot replace the answer, and the blank is a genuine binary that would be unanswerable
unhinted. Only the notation changed, to rule 13's `::option/option`.

---

## Also verified (not assumed)

- **T2 hides exactly 4 uncued answers** under a single `c1` — **at** rule 23's ceiling, not over it
  (`overloaded_group` warns at ≥6, hard-blocks at ≥8). Laid out with `<br><br>` between all four
  rows, so the count of answers owed is visible at a glance (check 21 / rule 19). Not fanned across
  cloze numbers (check 26 / rule 24). Its `Roster:` lists **all seven in TABLE 1-5 row order** with
  its own four bolded — confirmed against the render.
- **T2 must exist** — rule 30: the quantity↔unit notes alone would put every member on some card's
  visible side, so the set could never be *produced*. Membership first, rows second. Its partition
  (*apart from length, time, and mass*) is the source's own grouping, not an invented one (rule
  23.1), and it leaks none of its own four answers (rule 30's self-leak check).
- **Every abbreviation**: A / K / mol / cd — all four correct and correctly cased against the 3×
  crop of TABLE 1-5.
- **The `authorization` block** is present, complete (`by`/`date`/`asked`/`quote`/`scope`) and
  **byte-identical across all 9 cards**, with `verified_against: "p31"` on every one. Machine-diffed
  against the draft: **zero drift** on `authorization`, `from_idx`, `numeric`, `visual_source`,
  `image`, `block`, `verified_against`. Nothing weakened, nothing removed.
- **`needs_human_check` left untouched** (`false` on all nine) — derived downstream by
  `verify_report.py`; T1 carries `numeric: true`, which is what drives that derivation.
- **All 13 fronts rendered and cold-solved** individually (per cloze number), including per row on
  T2. Every one resolves to exactly one producible answer.
- **HTML** limited to `<b>` and `<br>`; Back Extra components separated by `<br><br>`; every line
  opens with a blessed label; `Roster:` last on every note that carries one.

## Cross-card findings against the 56 live chapter-1 cards

- **No duplicate claim.** Nothing live tests SI's expansion, MKS, the British engineering system,
  the count seven, the membership of TABLE 1-5, or any of the four quantity↔unit pairs. The one
  overlap by substance was T1's imported rationale clause vs **#51's `Why:`** — cut.
- **No sibling leak into the block.** No live card puts a Block-E answer on a **visible side**.
  #51/#52 state *seven* on their backs (adjudicated above); #23's `Ex:` mentions pounds as a weight
  conversion, which mildly *reinforces* S3 rather than leaking it.
- **No leak out of the block.** Deliberately excluded: length/time/mass ↔ meter/second/kilogram
  pairing notes, which would duplicate live **#21/#22/#23** (rule 12). Those three live cards are
  also what makes T2's 3-visible/4-hidden split legitimate — he can already produce the three
  handed to him.
- **The `Roster:` on T3–T6 was checked against rule 25's leak clause** (*never restate the other
  keys' values in Back Extra prose*) and **clears**: it carries the other **quantities** — the set
  rule 30 wants visible on every member note, and what Parker asked for by name ("the part and the
  whole in each flash card") — and **never** the other rows' **units**, so no sibling's answer is
  restated.
- **No cgs card, and that is correct.** The source itself says the cgs standards are *"as
  abbreviated in the title"* — the name self-documents, so a card would be acronym-decoding, which
  rule 20 calls padding. cgs earns its place on S2's and S3's `Distinguish:` lines instead.
- **Internal contradiction found and fixed:** S2's back said the system is built on three standards
  while T1 says seven. That is the kind of thing only a same-deck read catches.

## For Parker

Nothing blocks staging. One judgment call worth a glance: **T1's front is now a bare
seven-word question** (*"The SI is built on ___ base quantities."*) because the textbook's
"why seven" sentence turned out to sit in a section he did not authorize. If he wants that
reasoning on the card, it needs its own one-sentence ask covering the **Base vs. Derived
Quantities** paragraph — the current authorization does not reach it.
