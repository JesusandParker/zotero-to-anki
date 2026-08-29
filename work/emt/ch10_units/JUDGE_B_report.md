# JUDGE B — verdict report, chapter 10 cards, indices 85–169

Independent judge pass, 2026-08-29. Every card in the range was run against the full
editor checklist (per row where multi-row); grounding read against
`chapter_10_highlights.json` plus renders p987, p988, p989, p1025, p1027, p1028, p1031,
and pdftotext pulls of p995–997, p1000–1002, p1037–1042, and the glossary (p4040–4050).

**Process note:** per the orchestrator's mid-run change, nothing was edited in
`chapter_10_cards.json`. Both fixes live in `ch10_units/JUDGE_B_patch.json`
(`{"index", "card"}` full-replacement entries) for sequential application after all
judges finish. No re-stamp, no verify_report run.

---

## 1. Checker-warning adjudications (my range)

| # | Warning | Verdict | Reasoning |
|---|---------|---------|-----------|
| 86 | husk pair (c2 ×2, blood sweep) | **OVERTURN — clearance upheld** | The visible scaffold ("sweep for blood… run your gloved hands quickly and lightly ___, pausing periodically to ___") cues each c2 span independently; neither span's only cue is the other hidden span. Not the governmental-immunity shape. Grounded verbatim in idx 72. |
| 90 | husk pair (c2 ×2, pelvis) | **OVERTURN — clearance upheld** | Each c2 blank carries its own frame + slot-label ("palms over the ___ ::bony landmark"; "pressing gently ___ ::two directions"). Independently cold-solvable. Decidable-residue procedure shape (rule 26) done right; c1 no-pain gate is forced-choice. |
| 102 | synonym-equation husk (Golden Hour/Period) | **OVERTURN — clearance upheld** | Correct structure, not a husk: the full definition stays visible as the anchor of the c1 card, and the two c1 spans are ALIASES of one answer — hiding only one would leak the other ("Golden ___"). c2 card (from ___ to ___) is anchored by the visible name; endpoints are one retrieval. |
| 114 | husk pair (c1 ×2, gyn rule) | **OVERTURN — clearance upheld** | Litmus passes: with c1 covered, the remainder ("consider all women of ___ who report ___ to be **pregnant** unless ruled out by history") is substantive, not scaffolding; each c1 span has its own slot-label and the rule's trigger scope is one unit. Verbatim idx 96. |
| 123 | 'oxygenation' not in context (R13) | **OVERTURN — standing clearance verified, not just deferred to** | idx 104: "One of the most common causes of confusion is hypoxia." "Check his oxygenation" is the action-form paraphrase and the profile's auto-pair twin of card 122. Stem excludes the competing causes (glucose reads normal). No addition. |
| 148 | parenthetical after cloze (snoring) | **OVERTURN — clearance verified against the render** | "(or a foreign body)" is not a definition of "tongue"; it is the book's own alternate cause, confirmed verbatim on p1031: "usually caused by the tongue **or a foreign body**." |
| 155 | parenthetical after cloze (sputum) | **OVERTURN — clearance verified** | "(matter from the lungs)" is the **book's own parenthetical** (idx 126 verbatim). On the c2 card it is the licensed describe→name direction (definition cues the hidden term — card-rules #3 precision); on the c1 card the hidden answer is "a respiratory infection," which the parenthetical does not touch. |
| 93 | lexicon anchor external but in-source exists for 'dist' (p4045) | **OVERTURN — false collision; clearance now recorded on the card (PATCHED)** | The p4045 evidence hit is the headword **"distal"** ("Farther from the trunk…") — a different word. Checked the glossary text directly: headwords run `distal:` → `distracting injury:`; **no "distention" entry exists**. External anchor is correct; per the warning's own second branch, the why-it-does-not-fit is now recorded in `verified_by` (patch index 93). `needs_human_check` stays derived-true → Vocabulary block, exactly as the consolidation TODO intends for the DL externals. |

No warning in my range was upheld as a defect; every one was either a deliberately-generous
detector correctly cleared by the editor (verified independently, not rubber-stamped) or a
key-prefix false positive (#93).

## 2. Special-attention verifications

- **OPQRST (108, 109) vs p987/p988 renders:** all six elements and their question wording
  match the book exactly (O/P/Q/R on p987; S with the 0-to-10 scale and T on p988).
  First-letter hints licensed — "OPQRST" is spelled in the stem. Card 109's P-scenario
  verified against the render ("How are you most comfortable?" belongs to P) — **patched**
  to record `verified_against: p987` + a `visual_source` note, so verify_report can derive
  `needs_human_check` false instead of leaving an unverified-looking card in Section A.
- **SAMPLE (111, 112) vs p988/p989 renders:** all six expansions exact (P = "Pertinent past
  medical history"); the 12-hour medication window and "No known allergies" charting rule
  are on the render; the childbearing-age L card matches p989 verbatim ("the 'L' in SAMPLE
  also represents last menstrual period").
- **Gyn / male history chunks (114–118):** six gyn questions confirmed across the p994/p995
  break (3+3 chunk, invented sub-group names printed and NOT clozed, rosters with own
  members bolded, per rule 23.1); male urinary set is idx 99 verbatim (4 items); the
  frequency-vs-voiding Distinguish is accurate; the STD/judgmental/confidential lines
  verified on p995 via pdftotext.
- **TABLE 10-4 six-band family (137, 140–144) vs p1027/p1028 renders:** every value exact —
  adults 12–20, adolescents 12–16, school-age 18–30, preschoolers 22–34, toddlers 24–40,
  infants 30–60. One note per key (rule 25), `needs_table_back: TABLE 10-4` on all six
  (figure stage attaches the plate — flagged load-bearing in CONSOLIDATION_TODO), stems
  announce the number ("in breaths/min" + `::range`), and **no card's Back Extra restates a
  neighbor band's values** — scenario twins 138/145 cite only their own key's range. The
  NHTSA/PALS provenance lines match the table's note.
- **Breath-sound buzzword family (147–154, 158, 164) vs p1031 render:** every description
  verbatim-faithful. One-answer discipline holds: each name-the-sound card keeps its unique
  buzzword visible (crowing→stridor, whistling→wheezing, Rice-Krispies→crackles,
  bubbles-under-water→rhonchi, snoring named, bubbling/gurgling named) and phase/level
  blanks are forced-choice hinted. The editor's root-echo fix on 152 (moving "crackling" to
  the back) checks out. The stridor framing across 132 (D8, p1025 foreign-body crowing) and
  149/150 (D9, "foreign body or swelling") mirrors the book's own two sentences on p1025 —
  complementary, not contradictory, per the TODO's alignment instruction. Membership card
  deliberately absent (recognition taxonomy, no handle) — hand-off item stands.
- **Lexicon cards (93, 96, 97, 110, 113, 121, 130, 159), checklist #30:** all eight are
  plain (no jargon-by-jargon, no recycled roots), crisp (3–8 words), and faithful
  (discriminating feature kept; Distinguish lines separate crepitus/subcutaneous emphysema,
  pallor/cyanosis, rigidity/distention, focused/rapid). Every glossary/in_source anchor
  resolves in `lexicon_evidence.json` and the authored answer agrees with the quoted
  definition; every cited mark is `kind: lexicon` (R36 checked for all, incl. multi-mark
  cards 96 [80+108], 97 [81+182], 159 [131+162]). Interleaving follows document order
  (110 sits between OPQRST and SAMPLE; 159 right after the auscultate sentence; etc.).
  159's Korotkoff cue verified on p1039 via pdftotext.

## 3. Cross-batch leak sweep (whole file, both directions)

Scripted sweep of all 254 cards for my range's answer words (and reverse). Findings:

- **No check-#16 violations found.** Every hit inspected traced to (a) a clozed occurrence
  (hidden, e.g. card 38's noisy-breathing list, card 84's steady/spurting), (b) a
  sanctioned auto-pair or mirror (84↔85 arterial vignette; 174's pulse-30s×2 Distinguish ↔
  136's respiration twin — the exact mirror the consolidator ordered), (c) within-family
  `Roster:` lines (part-and-whole design), or (d) ordinary topical vocabulary in a
  different fact's context.
- **Interference note for hand-off (not a defect):** cards 61/62 (rescue-ventilation
  rates, another judge's range) legitimately contain "12 to 20 breaths/min" for
  infant/child ventilations — the same numerals as my card 137's adult resting range.
  Different fact, both book-true; worth one line at hand-off so Parker expects the
  collision, mirroring the TODO's cross-family interference concern.
- **Minor, benign:** 227's Back-Extra cue "rate, quality, and rhythm" overlaps 167's
  answer triple — the book itself repeats this schema (idx 138), it is a core doctrine
  drilled from two exams, and 167 is not a scenario/classify card; left as-is.
- 102's "Golden Hour/Period" names, 87's "90 seconds," 128's "Battle sign," and the
  auscultation landmarks appear nowhere else in the file — clean.

## 4. Per-card issues found and fixed

- **[93] distention (lexicon):** warning #93 adjudicated as a key-prefix false positive;
  clearance recorded in `verified_by` naming the detector (note-format.md's clearance
  rule) so no future session re-litigates or "fixes" the anchor to the wrong headword.
  → `JUDGE_B_patch.json` entry 1.
- **[109] OPQRST-P scenario:** content correct but unverified (`verified_against: null`,
  `needs_human_check: true` by derivation). Verified against the p987 render; recorded
  `verified_against`/`verified_by`/`visual_source`. `needs_human_check` left untouched —
  it is derived, never asserted; the orchestrator's verify_report will re-derive it.
  → `JUDGE_B_patch.json` entry 2.

## 5. Verified-clean notes (spot-checks beyond the warnings)

- 122's dementia/delirium/Alzheimer Pitfall confirmed on p1001 ("Confused behavior is not
  a normal response… verify the normal mental status"); 120's "no such thing as too much
  information" + refocus/stick-to-the-facts cue confirmed on the overly-talkative
  paragraph; 156's urgent-oxygenation/ventilation Pitfall is idx 129's context verbatim.
- DCAP-BTLS (88): 8 items under the spelled-mnemonic license (the checker's exemption
  applied correctly); high-priority 8 (99/100) correctly chunked 4+4 with printed (not
  clozed) invented sub-group names, full rosters, and no anchor note for an unordered set.
- Rapid-exam family (87–98): all region extras grounded verbatim; rosters consistent
  across all six notes; pelvis pain-gate scenario (91) ties to TABLE 10-3's T correctly.
- Auscultation landmark trio (160–162): values verbatim off the p1030 render;
  `needs_table_back: FIGURE 10-23` present on all three (TODO calls it load-bearing).
- 110 (pertinent negatives): authored answer follows the chapter's in-text sense
  ("expected findings the patient does NOT have"); the glossary's odd formal wording
  ("warrant no care or intervention") is carried transparently in the `Formal:` line.
  Judged consistent; flagging here only so the choice is on record.

## 6. Cards I could NOT fix / items for the orchestrator

- **None unfixable in my range.** Zero DROPs, zero REWRITEs beyond the two patch entries.
- Orchestrator to-dos already tracked elsewhere but load-bearing for my range: figure
  stage must attach TABLE 10-4 (137/140–144), TABLE 10-5 (165), and FIGURE 10-23
  (160–162) plates; DL externals (incl. 93 distention, 113 cookbook medicine) must
  surface in the verify_report Vocabulary block; purple repeat flags (crepitus ×2,
  auscultate family) go in the hand-off.
- Hand-off line suggested: the 12–20 breaths/min collision between adult resting rate
  (137) and infant/child rescue ventilations (62) — same numerals, different facts.

**Tally:** 85 cards reviewed (indices 85–169) · 8 warnings adjudicated (8 overturned /
0 upheld, two with new evidence: the glossary probe and the p1031 render) · 2 cards
patched · 0 cross-batch leaks requiring fixes · 0 unresolved.
