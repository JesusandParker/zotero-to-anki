# D2 drafter notes — EMT ch9, blocks D_group_types / E_team_elements / G_team_leader

Assigned marks (0-based indices into `chapter_9_highlights.json`): 4, 5, 6 (p880), 7, 8 (p882), 14 (p885).
Output: 8 card objects in `D2_cards.json` (D-1..D-4, E-1, E-2, G-1, G-2, in file order).

---

## Block D_group_types (idx 4, 5, 6 — p880)

Rule-0 check: three adjacent parallel marks under one heading ("Dependent, Independent, and
Interdependent Groups") = one connected 3-way classification, treated as a set.

### Fact pass

| # | Proposition (from marked span + context paragraph) | Tag | Disposition |
|---|---|---|---|
| 1 | The three group types are dependent, independent, interdependent (section heading names exactly three) | MUST-TEST (membership — rule 30) | D-1, grouped c1 (3 uncued, within rule 23's cap of 4) |
| 2 | Dependent: each member is told what to do — and often how — by the supervisor/group leader | MUST-TEST (idx 4 span) | D-2, two-way c1/c2 |
| 3 | Dependent: members rely on leader for task assignments, troubleshooting, virtually all decisions | SUPPORTING (idx 4 context) | D-2 `Why:` (kept out of visible stems — "rely" visible would leak "dependent", rule 3) |
| 4 | Dependent: that reliance limits ability to adapt/deliver care in an uncontrolled field environment | SUPPORTING | D-2 `Why:`, reused in G-2 `Why:` |
| 5 | Independent: each member responsible for his or her own area (a physical space or a set of tasks) | MUST-TEST (idx 5 span) | D-3, two-way; the gloss moved to `Meaning:` so c2 stays crisp (4 words) and the visible gloss can't paraphrase-leak the hidden answer |
| 6 | Independent: may get support/guidance but do NOT wait for an assignment (unlike dependent) | SUPPORTING (idx 5 context) | D-2 + D-3 `Distinguish:` |
| 7 | Independent: each focused on individual goals (start the IV, splint the arm), not a unified goal | SUPPORTING | D-3 + D-4 `Distinguish:` |
| 8 | Classic independent-group failure: perfectly splinted/packaged trauma patient DOA from unrecognized, poorly managed airway | SUPPORTING (idx 6 context) | D-3 `Pitfall:` — used exactly once (rule 13); no classify vignette built on it |
| 9 | Providers working interdependently are functioning as a TRUE TEAM | MUST-TEST (idx 6 span) | D-4, two-way |
| 10 | Interdependent: still assigned areas/tasks, but shared responsibilities, accountability, common goal | SUPPORTING (idx 6 context) | D-4 `Why:` (trimmed "the best possible patient outcome" tail off this line so E-1's answer doesn't sit verbatim on D-4's back) |

### Archetype choice, and the road not taken

- **Chose: membership card + three per-type two-way definitions** (rule 30 membership-first;
  Parker's two-way default for foundational term↔meaning). The type names are semi-transparent
  English, so the describe→name direction (c1) is the easy half and the name→discriminator
  direction (c2) carries the real load — the two-way gives both from one note each.
- **Rejected: one keyed 3-row classify card** (`description → {{c1::type}}` rows). Legal under
  rules 20/23 (3 uncued, descriptions as cues), but it tests only description→name, leaves the
  name→content direction untested, and the row-label-tautology risk is maximal here because the
  names paraphrase their own descriptions ("relies on the leader" ≈ dependent).
- **Rejected: classify vignette.** Recall-heavy chapter (profile + tasking: do not force
  vignettes); the book's only scenario is spent as D-3's `Pitfall:` and rule 13 forbids reusing
  it as a classify stem; a fresh invented scenario would add nothing the two-ways don't.
- **Leak hygiene:** "rely/reliant" never appears visible on any c1-direction stem (it is a
  near-synonym of "dependent"). Articles sit outside the braces per recipes §4 ("In a/an ...")
  — the a/an vowel tell is the sanctioned house form.
- D-1 `numeric: true`: the stem states the count "three types"; count = 3 clozed rows
  (rule 14 satisfied — the heading + three definition paragraphs are the complete set);
  verified verbatim, so the derived flag will clear.
- D-1 layout: rows with `<br><br>` (rule 19 — the count of owed answers is visible at a glance).

---

## Block E_team_elements (idx 7, 8 — p882)

### Fact pass

| # | Proposition | Tag | Disposition |
|---|---|---|---|
| 1 | There are five essential elements of effective team performance | FRAMING ONLY | visible clause on both cards; roster NOT marked, so no roster/membership card (rule 29; tasking explicit) |
| 2 | Shared goal: every provider (EMT → paramedic → emergency physician) committed to a common goal | MUST-TEST but name-entailed (see below) | E-1 visible scaffold |
| 3 | The common goal is typically the best possible patient outcome | MUST-TEST | E-1 c1 |
| 4 | Alarming phrases ("why splint...", "no point doing good CPR...") = evidence of no shared goal | SUPPORTING | E-1 `Ex:` |
| 5 | Clear roles and responsibilities: each provider must know what needs to be done + what is expected of him or her | MUST-TEST (idx 8 span) | E-2 c1 grouped pair (2 uncued) |
| 6 | The element's name, "clear roles and responsibilities" | MUST-TEST (describe→name) | E-2 c2 |
| 7 | Purpose link: roles exist to achieve a common goal | SUPPORTING | visible in E-2 stem ("to achieve a common goal") |
| 8 | Pit crew CPR = the example of clear roles (interventions defined in advance: compressions, defibrillation, airway, vascular access, medications; providers trained per role) | SUPPORTING | E-2 `Ex:` (per tasking) |
| 9 | "Pit crew" term originated in motor racing | SKIP | trivia beyond the mark's point |

### Why E-1 has no name-cloze while E-2 is two-way (deliberate asymmetry)

"A shared goal" is verbatim-entailed by the scaffold that must stay visible ("must be committed
to a **common goal**") — any cloze on the element name is a freebie (rule 3), and hiding the
scaffold too collapses the card into a husk/open-set ("one of the five elements is ___" — rules
16/17, roster unmarked). So E-1 tests only the non-entailed payoff (best possible patient
outcome), with the element name printed bold as framing. E-2's label is not verbatim-given by
its content clauses; producing "clear roles and responsibilities" from the description is the
NREMT "which element is this" skill, so the two-way is real there (its decodability is the
sanctioned semi-transparency of the define-it/name-it directions, same as block D).

### Rule-0 check for this pair

The two marks are parallel elements under one heading, but the "bigger idea" they'd synthesize
into is the five-element roster, which is unmarked — synthesis at roster level is barred (rule
29). Kept as two cards cross-linked by mirrored `Distinguish:` lines (blessed for confusable
siblings).

Count note: both stems print "five essential elements" (verbatim in idx 7 context: "the five
essential elements that health care providers must share to perform as an effective team");
"one of the five" promises no enumeration, nothing numeric is clozed; `numeric: true` set
anyway because a count is stated, with verification recorded so the derived flag clears.

---

## Block G_team_leader (idx 14 — p885)

### Fact pass

| # | Proposition | Tag | Disposition |
|---|---|---|---|
| 1 | The team leader provides role assignments, coordination, oversight, centralized decision making, and support | MUST-TEST (marked span) | G-1 describe→name: functions VISIBLE as the description, role name hidden |
| 2 | Purpose: so the team accomplishes goals / achieves desired results | SUPPORTING | G-1 visible tail |
| 3 | Leader often defined by policy, procedure, or statute; may be most senior or highest certification | SUPPORTING (context) | G-1 `Cue:` |
| 4 | A leader who simply commands is NOT leading a team — he or she is directing a DEPENDENT GROUP | MUST-TEST (context discriminator; tasking-endorsed) | G-2 c1 |
| 5 | Key differentiation vs a group leader: a team leader HELPS members do their jobs — support + working together + facilitating coordination | MUST-TEST-ish | G-2 `Distinguish:` (full sentence) + lean echo on G-1 |

### Retrieval-load reasoning (rule 23 vs rule 7 — the tasking's caution)

The five provided functions are five uncued, abstract near-synonyms (coordination / oversight /
support overlap heavily) with no spelled mnemonic and no regenerating structure:

- grouped produce-all-five reveal → barred (rule 23: 5–7 needs a handle; none exists);
- sibling numbers → barred outright (rule 24);
- 2-note invented partition (3+2) → legal but would drill verbatim production of near-synonym
  abstractions, the "impossible cold" shape the rules keep calling out; scaffold heavier than
  the knowledge.

Chose the tasking's preferred resolution: **describe→name** (G-1 — the five functions stay
visible as the description; the retrieval is the role name) plus a **separate discriminator
card** (G-2 — commands → dependent group, which also re-activates block D's taxonomy from a
fresh angle). The trade-off, stated plainly: **the five functions are left at recognition
level** (visible on G-1's front, never produced). Flagged as an open concern for the
editor/Parker — if he wants them producible, the follow-up is a 3+2 partition family with
printed (uncloze-able, invented) sub-group names and `Roster:` lines; not drafted now.

G-2 passes rule 21 mechanically and in spirit: the absolute ("is not leading a team") carries a
visible contrast anchor before the blank AND the blank carries a `::group type` slot-label.
G-2 rewards derivation from block D (commanding = telling what to do = dependent) — reasoning,
not recognition; its answer coincides with D-2's ("dependent") but the claims differ (defining
the type vs classifying a leadership failure), so both survive rule 12.

### G-2's c2 that was drafted and cut

A second blank on the positive half ("a true team leader instead {{c2::helps members do their
jobs}}, working together with them...") was cut: the visible tail ("working together with
them") paraphrases the hidden answer, and "helps" is near-given by contrast with the visible
"commands" — a self-answering row is padding (parker-preferences, 2026-07-30). The helping
content lives in G-2's `Distinguish:` instead.

---

## Deliberately not carded (and why)

- **The five-element roster of team performance** — unmarked; rule 29 and the tasking both bar it.
- **The five leader functions as a produce-the-list card** — rule 23 (no handle) + near-synonym
  items; see G block reasoning. Recognition-level by design; flagged.
- **"Shared goal" as a clozed answer** — verbatim-entailed by its own visible scaffold; every
  shape was a freebie or a husk. The element is taught by the visible bold framing on E-1.
- **Leader "defined by policy/procedure/statute" as its own card** — context, not a marked span;
  low-yield trivia; kept as G-1's `Cue:` line.
- **MCI triage/treatment/transport group examples** — live in idx 2's context (another unit's mark).
- **Pit crew racing origin** — trivia; the example itself is E-2's `Ex:`.

## Open concerns for the editor / assembler

1. **E-1 near-synonym interference across units:** idx 1 (p874, another unit) carries "unified
   goal of quality patient care." E-1's answer is "the best possible patient outcome," anchored
   by the "five essential elements... typically" frame. Whoever assembles should check the pair
   for stem discriminability (rule 12 is not violated — different claims — but the answers are
   cousins).
2. **D-4 vs idx 3 (p878 team definition, another unit):** "interdependently = true team" (D-4)
   sits close to "a team = providers with assigned roles working interdependently under a
   designated leader." Different claims; assembler should eyeball for dedupe/cross-leak once
   that unit lands.
3. **D-2 c2 length:** "told what to do — and often how to do it" is 9 words — over the 3–6 crisp
   guideline but one natural clause, within house practice (crepitus card's c2 is 8), and
   "often" is the book's own qualifier; trimming it would misstate the fact.
4. **Describe→name softness in block D:** the c1 directions are decodable-ish because the
   taxonomy's names are self-describing English. Inherent to the material; the c2 directions
   carry the real load. Accepted, not a defect to "fix" (rule 3's precision clause protects
   two-way definitions).
