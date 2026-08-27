# Block E — `E_si_systems_authorized` (physics ch1, p31 / printed p10)

9 notes → 13 Anki cards. Every card carries the authorization contract verbatim; `from_idx` is
empty on all nine, by design.

---

## 0. Why this block is legal at all (card-rules #29)

Rule 29 forbids the agent selecting content Parker did not mark, and names exactly one exit:
ask at hand-off and get his answer in his own words before a single card exists. That happened.

- **Asked:** "Unmarked on p. 10: the SI/MKS/cgs systems paragraph and the seven SI base
  quantities table. Want anything from them?"
- **He answered:** "sure do this"
- **Scope:** p31 (printed p10) — the *Systems of Units* paragraph and TABLE 1-5, and nothing else.

I re-confirmed the marks question myself before drafting. `chapter_1_highlights.json` marks on
page 31 are indices 27–32: the kilogram standard (27), the platinum-iridium cylinder (28), the
amu (29), the multiples-of-10 sentence (30), the lexicon word `base quantity` (31), and TABLE 1-4
Metric (SI) Prefixes (32). **Nothing** in the Systems of Units paragraph and **nothing** in
TABLE 1-5 is marked. So this content genuinely required the authorization, and the block would be
an R40 violation without it.

**Scope discipline — what I deliberately did NOT card**, even though it sat inside the same two
units of text:

- "it is very important to use a consistent set of units" — an exhortation, not a discriminator
  (it is already the page's own PROBLEM SOLVING margin note). No card; it earns no back line either.
- "Several systems of units have been in use over the years." — filler.
- "In SI units, the standard of length is the meter / time the second / mass the kilogram."
  — already carded three times (live #20 meter, #21 second, #22 kilogram). Rule 12. It survives
  only as *visible anchor scaffolding* in T2's stem, never as an answer.
- "We use SI units almost exclusively in this book." — book navigation, and a source artifact.
- **cgs → centimeter, gram, second** as its own card — this is acronym-decoding, and rule 20 calls
  a row that answers itself padding. The plan said not to write one; I agree and did not. cgs
  earns its place only as the *mass* half of S3's contrast and as a back line on S2.
- **length / time / mass pairing notes** for TABLE 1-5 — excluded per plan; the meter, second and
  kilogram cards already own that ground (rule 12).

---

## 1. Grounding — verified this run, first-hand

I did not take the supplied verbatim on trust. I re-read `work/physics/page_31.png` and zoomed
TABLE 1-5 and the Systems of Units paragraph to 2× before drafting.

- The *Systems of Units* paragraph matches the supplied verbatim **exactly**, word for word.
- TABLE 1-5 confirmed at 7 rows, in this order, with these abbreviations:
  Length/meter/m · Time/second/s · Mass/kilogram/kg · Electric current/ampere/A ·
  Temperature/kelvin/K · Amount of substance/mole/mol · Luminous intensity/candela/cd.
- **One correction to the briefing:** the supplied "(b)" paragraph omitted a sentence that is on
  the page — *"The corresponding units for these quantities are called base units and derived
  units."* It sits between "…base quantities and derived quantities" and "A base quantity must be
  defined in terms of a standard." Nothing in this block depends on it, but it is why "base unit"
  is legitimate vocabulary on T4's back rather than an import.

---

## 2. Fact-pass

### Unit A — the *Systems of Units* paragraph

| # | Fact | Verdict | Where it went |
|---|---|---|---|
| A1 | Use a consistent set of units | SKIP | exhortation, not testable |
| A2 | Several systems have been in use over the years | SKIP | filler |
| A3 | **The most important today is the Système International, abbreviated SI** | **MUST-TEST** | **S1** |
| A4 | "French for International System" | SUPPORTING | S1 `Meaning:` |
| A5 | SI standards: length = meter, time = second, mass = kilogram | SKIP (already carded) | T2 stem anchor only |
| A6 | **SI used to be called the MKS system** | **MUST-TEST** | **S2** |
| A7 | MKS = meter-kilogram-second | SUPPORTING | S2 `Meaning:` (back only — see §4) |
| A8 | cgs: centimeter, gram, second = length, mass, time | SUPPORTING | S2 + S3 `Distinguish:` |
| A9 | **British engineering system: foot = length, pound = FORCE, second = time** | **MUST-TEST** (the force part) | **S3** |
| A10 | "more used in the U.S. than Britain" | SUPPORTING | S3 `Cue:` |
| A11 | "We use SI almost exclusively in this book" | SKIP | source artifact |

### Unit B — Base vs. Derived intro + TABLE 1-5

| # | Fact | Verdict | Where it went |
|---|---|---|---|
| B1 | A base quantity must be defined in terms of a standard | SKIP (already carded) | live #50 |
| B2 | Scientists want the smallest number consistent with a full description of the world | SUPPORTING | T1 stem framing |
| B3 | **That number is seven** | **MUST-TEST** | **T1** |
| B4 | **The membership of TABLE 1-5** | **MUST-TEST (rule 30 — membership first)** | **T2** |
| B5 | electric current ↔ ampere (A) | MUST-TEST | T3 (two-way) |
| B6 | temperature ↔ kelvin (K) | MUST-TEST | T4 (two-way) |
| B7 | amount of substance ↔ mole (mol) | MUST-TEST | T5 (two-way) |
| B8 | luminous intensity ↔ candela (cd) | MUST-TEST | T6 (two-way) |
| B9 | length/time/mass ↔ meter/second/kilogram | SKIP | rule 12, live #20–22 |

---

## 3. The cards

| | Note | Cards | Archetype |
|---|---|---|---|
| S1 | SI stands for Système International | 1 | definition, **one-way** (see §4) |
| S2 | SI used to be called the MKS system | 1 | naming fact, `::acronym` slot-label |
| S3 | the pound is a standard of **force** | 1 | comparison / discriminator (§8) |
| T1 | the SI is built on **seven** base quantities | 1 | number (§5), rule-27 slot-label |
| T2 | the four non-mechanical base quantities | 1 | **membership** (rule 30), grouped reveal |
| T3–T6 | quantity ↔ unit, one per non-mechanical quantity | 8 | two-way definition (§4) |

**Retrieval load.** The only grouped reveal is T2: four uncued answers under one `c1`, which is
exactly the rule-23 ceiling (≤4). Everything else hides one span per card. Nothing in this block
approaches the `overloaded_group` warn threshold.

---

## 4. Where I departed from the plan, and why

### S1 is ONE-WAY, not two-way. (The one real disagreement.)

The plan asked for "SI ↔ Système International (two-way per Parker's default)". I drafted it
one-way and I think two-way is wrong here, for a specific reason: **the reverse card is a freebie.**

A two-way would produce a card whose front reads *"___ stands for Système International"* (or
*"Système International is abbreviated ___"*). The answer is the initials of two words sitting
visible on the same line. That is card-rules #20 verbatim — *"read the label aloud, then the
answer; if the second is a paraphrase of the first, delete the row"* — and it is rule 18's
first-letter leak wearing a different hat. Parker's own words on that shape: *"literally giving
away the answer, an easy copout."*

Parker's two-way default explicitly carries its own exit: *"Go single-direction only when just one
direction is useful."* Term↔meaning two-ways work because the meaning is not recoverable from the
term's letters. An **abbreviation↔expansion** pair is different: one direction is memory, the other
is spelling. So S1 tests the memory direction only.

I also kept *"French for International System"* **off the front** for the same reason. With "SI"
plus the English gloss visible, a non-knower can construct "Système International" from cognates —
a rule-3 crutch. It is a `Meaning:` line on the back instead, which is where card-rules #5 puts an
acronym expansion anyway.

### S2's stem was rephrased to kill a cataphoric pronoun

First draft opened *"Before it was called the SI…"*, where "it" points forward. Layer A #2 bans a
sentence opening on a pronoun. Now: *"The system of units now known as the SI used to be called the
{{c1::MKS::acronym}} system."*

### S3's hint is a forced-choice pair, not a bare slot-label

The plan said "cloze the quantity word (force) with a slot-label hint." A plain `::physical
quantity` leaves the blank open to **force / mass / weight**, which fails rule 2 (one answer). A
`::force or mass` forced-choice closes it to the exact axis the card exists to teach, and
card-recipes §2 licenses forced-choice option lists by name (*"the point there is which, not the
word"*). The hint names the axis, never the answer.

**And the metric contrast stayed off the front.** An earlier draft had *"…the pound as its standard
of {{c1::force}} — not of mass"* and *"…whereas the metric systems make theirs a mass."* Both are
leaks by elimination: with a binary hint plus a visible "the other one is mass," the answer is
derivable without knowing anything. The whole contrast is now the `Distinguish:` line, which is
where card-rules #3 says definitional content belongs.

### S3 leaves "foot for length" and "second for time" visible on purpose

Editor check #4 (fully clozed) asks whether a testable fact is riding along as scenery. These two
are, and I left them anyway: *foot → length* and *second → time* are self-answering rows (rule 20 —
a foot is obviously a length), so clozing them would be padding, and grouping three answers under
one number would make an all-or-nothing card out of one real fact and two freebies. Visible, they
are the parallel scaffold that makes the third slot surprising. Parker's own corollary applies:
*"a row that answers itself is padding, not coverage — drop it."*

### T2 shows length/time/mass rather than testing all seven

Per plan, and I agree. Seven uncued answers is 0.9⁷ ≈ 48% — a card built entirely from facts he
knows and graded as one, which is the exact failure mode of the radio-report card (rule 23, R25).
The three mechanical quantities are the three he can already produce (three live cards each own
one), so handing them over costs nothing and buys a card that sits precisely at the ≤4 ceiling.
Rule 30's membership test — *can he PRODUCE the set?* — is satisfied by T1 (the count) + T2 (the
four he cannot derive) + the three standing meter/second/kilogram cards.

### `Roster:` rides on T3–T6 too, not just T1/T2

Rule 23 requires it on chunked-list notes; T3–T6 are the pairing lane, so it is optional there.
I included it because rule 31 says *"the roster on the back carries the rest"* on member cards, and
because Parker asked for it by name: *"the understanding of seeing the part and the whole in each
flash card."* The roster lists the **quantities only** — never the other three units, which would
hand over T3–T6's own sibling answers.

---

## 5. Dedupe against the 56 live chapter-1 cards (rule 12)

Searched `work/physics/chapter_1_cards.json` for every load-bearing term in this block:

| Term | Live hits | Verdict |
|---|---|---|
| `ampere`, `kelvin`, `candela`, `luminous`, `MKS`, `cgs`, `British`, `foot`, `temperature`, `amount of substance` | **none** | clear |
| `Syst` | #24 ("system"), #54 ("measuring system") | not Système International — clear |
| `mole` | #23 ("molecules") | not the unit — clear |
| `pound` | #22 (`Ex:` "1 kg weighs about 2.2 pounds on Earth") | a conversion aside, not the British system's standards — clear, and it mildly *reinforces* S3 |
| `International` | #18 (French Academy), #22 (Int'l Bureau of Weights and Measures) | different entities — clear |
| `electric current` | #3 ("Galvani … battery and electric current") | history of electricity, unrelated — clear |
| `base quantit` | #50 (lexicon def), #51 (derived quantities), #54 (dimensions) | none tests the count or the membership — clear |

**Sibling-leak check (editor #16).** The three already-live cards that touch this ground are #50
(base quantity), #51 (derived quantities) and #22 (kilogram). None of them puts a Block-E answer on
its **front**. Two of them state "seven" on their **backs** (#50 `Why:` — *"in the SI it turns out
to be seven"*; #51 `Ex:` — *"in terms of these seven base quantities"*).

**⚠ Flag for the editor / Parker:** the count *seven* is therefore already broadcast on two live
card backs, and T1 is the first card that actually **tests** it. I judged this acceptable — a fact
stated on a sibling's back is reinforcement, not a front-side give-away, and rule 12 is about not
carding the same fact twice, which is not happening (#50/#51 mention it, T1 tests it). But it is
the closest thing in this block to a sibling leak and someone should agree with me rather than
discover it later. I did **not** touch #50 or #51 — they are live and not mine to edit
(card-rules #32 / authorship).

I also scrubbed my own block for the same problem: three of T3–T6's backs originally said *"the
SI's seven"*, which would have added three more broadcasts of T1's answer. All rewritten to "the
SI's base quantities" / "an SI base unit". Only T1's own back names the number now.

---

## 6. Editor self-check (checklist run per row)

Every card, every check. Only the non-obvious verdicts are written out.

- **#1 one answer / #18 cold-solve.** All 13 fronts read cleanly with the answer covered. The two
  I stress-tested hardest: S3 (closed by the `::force or mass` pair) and T5's c1 (*"the base
  quantity ___ is measured in moles (mol)"* — "amount of substance" is the only fill; a knower may
  say "amount of a substance", which is the same answer and he self-grades).
- **#2 / #15 leak vs crutch.** T3–T6 are two-way definitions with both halves clozed, which
  card-rules #3's precision clause names explicitly as **not** a leak. S1's front carries no gloss
  and no language cue. T1's "smallest number consistent with a full description of the physical
  world" is situational, not definitional — it does not imply seven.
- **#4 fully clozed.** S3's two visible pairs are a deliberate call — see §4. T1's rationale clause
  is left visible because clozing it would hide a long fuzzy phrase (rule 5).
- **#5 / #25 / #26 list + load.** T2 is one grouped reveal, one cloze number, four members, laid out
  with `<br><br>` per rule 19 so the count of blanks is visible. Not fanned across numbers
  (rule 24). `Roster:` present with its own four bolded.
- **#6 crisp.** Longest hidden span is "amount of substance" (3 words) and "the smallest…" is not
  hidden. No blank hides ≥9 words.
- **#9 / #20 hints.** Three hints total. `::acronym` (form label), `::number of base quantities`
  (rule 27's canonical shape), `::force or mass` (licensed forced choice). None is a first-letter
  hint; none could replace its answer.
- **#10 standalone.** Swept mechanically for all 19 banned source-artifact words and for
  sentence-initial `This/That/These/It/They/Here/There`: clean. One catch during drafting — T2's
  back said "a mechanics-only **picture** of nature"; harmless metaphor, but "picture" is on the
  banned list, so it is now "description" (which also echoes the source's own phrasing).
- **#11 Back Extra earns its place.** No back line restates its own Text. Every line is either a
  contrast the front does not carry (S1, S2, S3, T2, T3, T4, T5), a memorable grounded aside
  (S3's `Cue:`), or reference (`Roster:`).
- **#12 application-fit.** N/A — `profiles/science.md`, not EMT; no scenario quota.
- **#13 coin-flip hinted.** S3 is the only binary and it carries its forced-choice pair.
- **#14 prereq-closed.** Every stem names the system or the property it belongs to (rule 31), so no
  card leans on unstated context.
- **#17 list complete vs the real source.** T1 says seven; TABLE 1-5 has exactly seven rows,
  re-counted off the render. T2 says "four" and clozes four. No undercount.
- **#19 husk.** T3–T6 use `c1`/`c2` on different numbers, so each card reveals one half as the
  anchor. No same-number mutual dependence anywhere.
- **#21 list reads as a list.** T2 only; `<br><br>` between all four rows.
- **#22 row label cues.** No `LABEL → answer` rows in this block. T2's rows are bare items.
- **#23 absolutes anchored.** Two negative claims live on backs, not fronts (T3 "not among the SI's
  base quantities", T4 "the degree Celsius is not an SI base unit"), so no unhinted absolute blank.
- **#24 cloze is the unit of knowledge.** T2 hides the items themselves, not filler inside them —
  rule 22's endorsed shape.
- **#27 value column.** N/A — no numeric panel; T1 is a single scalar.
- **#29 bare number.** T1 is the only bare quantity and carries `::number of base quantities`.
- **#30 lexicon.** N/A — no `kind: lexicon` cards in this block.
- **Safety overlay.** T1 states a count → `"numeric": true`. `needs_human_check` left `false` on all
  nine, since `verify_report.py` derives it.

---

## 7. Grounding notes on the back lines (the only places I reasoned past a literal sentence)

Each of these is a **negative reading of a closed table** — TABLE 1-5 states its own
exhaustiveness ("This number turns out to be seven, and those used in the SI are given in
TABLE 1-5"), so "X is not on the list" is licensed by the source rather than imported:

- T3: *charge, voltage, and resistance are not among the SI's base quantities* — true and
  table-supported; the three nouns are named only to be excluded, nothing is asserted about them.
- T4: *the degree Celsius is not an SI base unit* — same shape. *"its abbreviation carries no
  degree sign"* is a direct reading of the table's `K` cell.
- T5: *the mole does not measure how heavy something is* — follows from mass and amount of
  substance being listed as two distinct base quantities with two distinct units.
- T6: *luminous intensity is the only SI base quantity that concerns light* — a direct reading of
  the seven rows.
- T1/T2: "the mechanical three" is my label for length/time/mass, used only as visible scaffolding
  on the **back**; it is never clozed, so rule 23.1's ban on clozing an invented partition name is
  not in play.

Everything else on every card traces to a literal clause of the two verified passages.

---

## 8. Gate result

```
python3 scripts/check_cards.py work/physics/drafts/block_E.json \
    --highlights work/physics/chapter_1_highlights.json --require-provenance
checked 9 cards
  (grounding checked against chapter_1_highlights.json)
  deterministic checks clean
  stamped OK -> block_E.json.verified
```

**`authorized_lane_check` has already landed** in `scripts/check_cards.py` (line 1102), and the
predicted missing-provenance noise did **not** materialise: `grounding_check` now skips a card that
has an `authorization` block instead of reporting it, and it flips unmarked cards to HARD whenever
the authorized lane is in play at all (`lane_in_play`). So the nine cards pass clean in both the
default mode and under `--require-provenance` — zero hard errors, zero warnings.

I checked the enforcement against the contract I was given: it requires `by`/`asked`/`quote`/`date`/
`scope` all non-empty, `by == "parker"`, a quote of ≥3 characters, and — for a card with no
`from_idx` — a non-empty `verified_against`. All nine satisfy every clause.
