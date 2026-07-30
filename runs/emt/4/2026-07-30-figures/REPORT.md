# Chapter 4 figure run — 2026-07-30

A deliberate practice run before Chapter 7, on a chapter whose cards already existed.
Chapter 6 was the easy case: anatomy, labelled diagrams, modern provenance. Chapter 4 was
picked to be *different*, and it was — it broke five things Chapter 6 never touched.

**Outcome:** 31 of 105 live Chapter 4 cards carry a figure (29%), from 16 distinct plates.
Chapter 6 finished at 100 of 202 (49%) from 38 plates. Zero images on any question side.
Zero cards carrying more than one figure. 251 cards across both chapters now have pictures.

---

## What ran, in order

| # | Step | Result |
|---|---|---|
| 1 | Re-extract Ch4 highlights | 81 marks, modern schema, 6 flagged `needs_visual` |
| 2 | Backfill `from_idx` | 104/107 resolved, 3 left null |
| 3 | Build figure index | 21 figures, all native resolution, 2 with publisher description |
| 4 | Match | 6 teaches + 26 context = 32 proposals |
| 5 | Visual audit | 4 figures inspected by eye |
| 6 | Attach | 31 written (1 proposal pointed at a card Parker had deleted) |
| 7 | Verify | leak check clean, gate re-run, both chapters reconciled |

---

## The headline finding: chapter *type* changes everything

Chapter 6 is anatomy — every plate is a labelled diagram, and the publisher supplies an
accessibility long description naming each labelled structure. Chapter 4 is Communications
and Documentation, and its plates are **photographs**: *"Using touch conveys a sense of
caring"*, *"A mobile data terminal"*, *"You will be assigned to a call by the dispatcher."*
There is nothing labelled in them to describe, so the publisher supplied a description for
only **2 of 21** (Ch6: 27 of 45).

That cascades. With no description, a figure's searchable vocabulary comes from its caption
alone, and captions are prose sentences rather than term lists. So **coverage scores collapse**
— Ch4's matches run 0.08–0.50 where Ch6's run 0.29–1.00 — and almost everything lands in the
`context` tier rather than `teaches`.

**The important part: low coverage did not mean bad matches.** The visual audit found the
opposite. The two best matches in the chapter scored near the bottom:

- **FIGURE 4-8** (coverage **0.17**) → *"Managing a patient who has a guide dog"*. The photo
  is a guide dog in harness. Near-perfect.
- **FIGURE 4-7** (coverage **0.12**) → *"Five steps to communicate with a patient who is hard
  of hearing"*. The plate shows the actual signs for Sick / Hurt / Help.

And the strongest genuine wins were equipment cards, where seeing the object *is* the point:
**FIGURE 4-18** → *"a mobile data terminal is a small computer terminal inside the ambulance"*,
**FIGURE 4-15** → *"a mobile radio is installed in a vehicle."*

**Conclusion for Chapter 7:** coverage is a good signal for diagram chapters and a weak one
for photo chapters. Page proximity carries photo chapters, and the generous default already
handles this correctly — but only because `context` accepts on proximity alone. Do not
tighten that threshold without checking a photo-heavy chapter first.

---

## The one bad match, and what it teaches

**FIGURE 4-1** (the Shannon–Weaver communication model) went to card #0, *"therapeutic
communication uses verbal and nonverbal techniques"* — topically adjacent, not illustrative.

Its real home is card #9: *"In communication, **noise** is anything that dampens or obscures
the true meaning of a message."* The diagram has a **Noise** box wired between Encoding and
Decoding. It is the picture for that card.

It missed for two compounding reasons:

1. **Page window.** Card #9 grounds on p361; the figure is on p357. Four pages apart, outside
   the ±2 limit, so it never scored at all.
2. **Blindness to the picture's contents.** With no long description, FIGURE 4-1's terms were
   just `{shannon, weaver, communication, model}`. The words actually drawn inside it —
   *noise, encoding, decoding, feedback* — were invisible.

The second is the deeper one, and it prompted a fix (below). The first exposes a structural
limit still open: **the matcher optimises per-card, never per-figure.** Each card picks its
best figure; no figure ever picks its best card. So a plate can be spent on a mediocre card
while the card it actually illustrates gets nothing.

---

## Bugs found and fixed

Five, all of which Chapter 6 alone would never have surfaced.

**1. Caption detection assumed `©`.** A caption only counts once a trailing rights line
corroborates it. That regex matched `©` and `(c)` only — fine for `© Jones & Bartlett
Learning` (27 of 42 sampled), but photo chapters credit the photographer:
*"Courtesy of the Guide Dog Foundation for the Blind."* **FIGURE 4-8 and 4-12 were silently
missing.** Widened to accept `Courtesy of` / `Source:` / `Reproduced from` / panel-letter
credits (`A, C: © Photodisc`).

**2. The fix for #1 broke FIGURE 4-4.** The looser patterns needed a length guard so body
prose could not pose as a credit — but applying that guard to *all* patterns dropped a real
figure, because the extractor welds credits onto the following paragraph (p370 returns a
643-character block beginning `© Jones & Bartlett Learning. 7. Always speak slowly...`).
Split into two tiers: a block **opening** with `©` is a credit at any length; the ambiguous
forms are length-capped. Caught only by diffing against the known-good baseline.

**3. The image cache checked itself before checking for art.** `save_art` returned a cached
path whenever a file existed at that name, *even when no art was found*. So a caption whose
art stopped resolving silently adopted whatever a previous run had left there — the count
stayed flat while the index pointed at the wrong picture. This is what produced the phantom
"47 figures" in Chapter 6 (the honest number is 45). Now: no art, no record.

**4. The undo record was not segment-scoped.** Attaching Chapter 4 overwrote Chapter 6's
undo file, stranding 99 writes as unrevertable. Now `figure_attach_undo_seg<N>.json`; Ch6's
was reconstructed from the live deck (99 writes, 0 unresolved labels).

**5. The undo record replaced instead of accumulating.** Because attaching is idempotent, a
re-run only carries the few cards that newly qualified — so the file shrank from 99 entries
to 7. Now merged on `(noteId, media)`.

**6. Re-running after a matcher change added a second figure instead of swapping.** The
idempotency guard was "is *this file* already here", so any card whose best figure *changed*
quietly gained a second picture. Six Chapter 6 cards did this. The guard is now "does this
card already carry a pipeline figure", with `--allow-multiple` / `--replace` as deliberate
opt-ins. The six were reconciled to the matcher's current choice.

---

## Improvement shipped: harvest the book's own cross-references

The FIGURE 4-1 failure showed the matcher was blind to what a picture contains whenever the
publisher supplied no description — which is most of a photo chapter. But the book explains
its own figures in prose: *"…as shown in (FIGURE 4-1)"*. That text is free, deterministic,
and sitting in the text layer.

`crossrefs()` now harvests the sentences citing each figure and folds them into its terms.
**36 of the 37 figures with no publisher description gained vocabulary.** Effect:

| | before | after |
|---|---|---|
| Ch4 cards with a figure | 29 | **32** |
| Ch4 `teaches` tier | 4 | **6** |
| Ch6 cards with a figure | 99 | **100** |
| Ch6 `teaches` tier | 31 | **35** |

Modest in count, but it moves cards from *"a picture is nearby"* into *"the picture shows the
answer"*, which is the tier that matters. It did **not** rescue card #9 — that crossref
sentence is about Bell Labs history and never says "noise" — so the per-figure matching gap
below remains genuinely open.

---

## New tool: `backfill_provenance.py`

Chapter 4's cards predate `from_idx`, and a card with no mark has no page, and a card with no
page cannot be near a figure. Chapters 1, 2, 3 and 5 are in the same state.

Two passes. **Anchor:** score each card against each mark by how much of the marked span it
reproduces; trust only clear winners. **Interpolate:** the generator walks the chapter in
order, so a card between two anchored cards came from a mark between *their* marks — rescoring
inside that window rescues the scenario/application cards, which paraphrase a concept and so
score low against every mark globally.

The spine uses the **longest non-decreasing subsequence**, not a greedy sweep. Greedy lets one
early false anchor evict every later correct one: 67 anchors collapsed to 27, and only 64/107
cards resolved. Solving for the longest consistent run keeps 59 and discards exactly the
handful that break the pattern — which, inspected, are the wrong matches. **104/107 resolved.**

Verified by eye on the cases global matching got wrong:

- card #1 *"Tone, pace, and volume of speech"* — was matched to *"Gather supplementary patient
  documentation"*; now correctly to *"Take note not only of the words being spoken, but how
  they are said."*
- card #11 *"begin with open-ended questions"* — was matched to *"Manage the environment"*; now
  correctly to *"There are two types of questions: Open-ended questions are…"*

Side effect worth noting: **R13 grounding now runs on Chapter 4 for the first time.** It could
not before, with nothing to ground against. It produced warnings, no hard blocks.

---

## The best find came free: backfilling provenance exposed a real grounding hole

Giving Chapter 4 `from_idx` turned R13 on for it for the first time — and it immediately
HARD-blocked six cards. **Every one of them was correct**, with its text sitting verbatim in
the source. The defect was in the extractor's context window, and it had been invisible
because nothing had ever been able to check.

Two compounding causes, both now fixed:

1. **A caption's forward window was never widened.** `wants_next_page()` already treated a
   TABLE/FIGURE caption exactly like a list lead-in and fetched the following page — but
   `locate_context()` did not, so captions got the narrow 450-character window. *The extra
   page was fetched and then immediately thrown away.* TABLE 4-3's context stopped mid-table
   at "Reflection", four rows short of Empathy, Clarification, Confrontation and
   Interpretation — the exact four cards that were blocked.
2. **A caption needs more reach than a list.** Widening it to the list budget (1,700) still
   left TABLE 4-7 blocked: its caption sits at the top of p403, whose own remaining 1,704
   characters consume the whole budget before p404's *"document the name of the facility…
   and the room number"* row is reached. A caption's body is a whole table and routinely
   spans a page boundary, so it now gets **3,800**.

Result: **both chapters gate clean and stamp — 0 hard errors each** (Ch4 was 6, Ch6 was
already 0 and stayed 0).

**And a matching gap in the other direction:** `attach_figures.py` wrote the figure to Anki
but never recorded it in the canon cards file. The gate reads the file, so a card could be
HARD-blocked for lacking exactly the visual evidence now sitting on it in the deck. It now
writes `visual_source` back (132 cards across the two chapters) and clears the stamp so the
gate re-runs.

---

## Still open — for Chapter 7 and after

1. **Per-figure matching.** The real structural gap. Add a reverse pass: for each figure, find
   its best card; where that card has nothing better, attach. This is what would have put
   FIGURE 4-1 on the noise card. Highest-value next change.
2. **Three unresolved cards** (#35, #81, #106) left `null` on purpose. #106 is flagged by the
   gate as ungrounded — correct behaviour, worth a look.
3. **Two Ch6 captions with no locatable art** (FIGURE 6-15, 6-31). Both are prose
   cross-references that open a paragraph, not real captions — arguably right to skip, but
   unconfirmed.
4. **One Ch4 proposal had no live note**: canon holds 107 cards, the deck 105, because Parker
   deleted two. Reported, not forced. `sync_report.py` is the tool for reconciling that drift.
5. **Vector figures are untested.** Both chapters were 100% raster. `render_region` has never
   fired on real content.
6. **Photo chapters may deserve their own profile.** Coverage thresholds tuned on anatomy are
   the wrong instrument for a chapter of photographs; the current generous default absorbs
   this, but it is absorbing it rather than modelling it.

---

## Process note

Four of the six bugs were found by **comparing against a known-good baseline** rather than by
reading code: rebuild Chapter 6, expect 45, get 47, ask why. Chapter 7 will be generated fresh
with no baseline to diff against, so it is worth re-running Chapter 6 after any change to this
code and confirming the numbers still land where they did here:

```
Ch4: 105 notes | 31 with a figure | 16 plates | 0 doubled
Ch6: 202 notes | 100 with a figure | 38 plates | 0 doubled
leak check: 251 cards with figures, 0 images on any question side
```
