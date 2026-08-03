# EMT profile

For the AAOS EMT textbook and anything else feeding NREMT-B preparation.

This is the profile the whole pipeline was originally built around, so most of the worked
examples in `card-recipes.md` and every regression case in `regression-cases.md` come from
here. Universal card craft still lives in those files — this only adds the emphasis.

---

## 1. What it's for
The **NREMT cognitive exam and real field performance**. NREMT is an *application* exam:
it rewards deciding, not reciting. A deck of perfect factoids will underprepare him.

## 2. Archetype mix

**Clinical chapters** (Airway, Shock, Cardiac, Trauma, Patient Assessment, Medical
Emergencies — push application highest here):

- ~30% scenario / application (`card-recipes.md` §9)
- ~20% indication / contraindication / "when do you do X" trigger (§10, §9)
- ~15% sign/symptom → field impression (§9)
- ~15% assessment-sequence & treatment-order (§7)
- ~10% normal ranges + dose/quantity facts (§5)
- ~7% definitions, action-changing only (§4)
- ~3% anatomy / mechanism / "why" (§7, §11)

**Recall-heavy chapters flip toward definitions and rules** — EMS Systems, Medical/Legal,
Communications & Documentation, Lifting & Moving, Ambulance Operations, The Human Body.
Consent types, negligence components, hazmat zones, triage categories, scope-of-practice,
anatomy. Far less scenario; forcing vignettes onto legal definitions produces bad cards.

**Sanity check:** if fewer than ~1 in 4 cards for a *clinical* chapter makes Parker
*decide* something, the batch is too factoid-heavy. This does NOT apply to recall-heavy
chapters.

## 3. The auto-pair rule (what makes the deck feel like NREMT prep)
When a highlight is a **sign, finding, vital threshold, or "which one" discrimination**,
also draft ONE short scenario cloze embedding it in a 1–2 sentence patient stem ending in
a single decision (field impression or next action). One stem, one cloze. The highlight
gives the fact; the vignette forces the decision. This single habit does most of the work
of NREMT-ifying the deck. Heaviest in clinical chapters; light elsewhere.

## 4. EMT-native patterns to build on purpose
The AnKing Step/MCAT decks don't emphasize these, so they won't come from imitation:

1. **Contraindication pairs** — indication AND contraindication together so they don't blur (§10).
2. **"When do you do X" triggers** — one card per intervention, framed as the field trigger (§9).
3. **Age-banded vital ranges** — a tight grouped sub-set (adult / child / infant), anchored to the AAOS numbers (§5, §6).
4. **The finite EMT drug box** — the 5 rights + indication + contraindication + exact dose; skip mechanism of action (§5).
5. **Scope-of-practice boundaries** — EMR vs EMT vs AEMT vs Paramedic; "can an EMT do X" (§9/§10).

## 5. Default flips vs a medical-school deck
- drug → rights / indication / contraindication / **dose** (not MOA)
- condition → field S/S → impression → BLS treatment + transport (not pathophysiology)
- number → the number **plus the action it triggers**
- anatomy → occlude only assessment-relevant figures
- legal/ethical concept → **card it** (med decks skip these; they're easy NREMT points)
- MOI → an index-of-suspicion card

Don't over-card: a finite syllabus plus an application exam means *hundreds* of dense
decision cards, not thousands of trivia.

## 6. Traps
- **Every number, dose, threshold, and time window gets `needs_human_check: true` — **unless it was
verified verbatim against the page**, in which case record `verified_against` /
`verified_by` and let `verify_report.py` derive the flag (it will derive `false`, and the
card still appears in "Section B: verified, skim", so it reaches Parker either way).
The flag is **derived, never asserted** (`note-format.md`); asserting it by hand and
leaving the verification fields empty is what the derivation is there to catch.** A
  wrong digit on a dose is a safety error, not a typo. Verify it verbatim against the
  source page before flagging.
- **Chapter 5 (Medical Terminology) is structurally different** — 587 word-root↔meaning
  notes with clinical-example HTML blocks and TTS audio, built once and correct by design.
  Audit it with `--audit`, never restyle it, and expect its similar-Text warnings (they're
  the shared "The word root X means Y" template, not duplicates).
