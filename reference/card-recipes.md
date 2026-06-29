# Card Recipes — the archetype playbook

The master playbook for picking and executing the right card pattern for any EMT highlight. This is the **fast working reference**; `cloze-mastery.md` is the deep exemplar bank (open only the section you need). Hard form rules live in `card-rules.md`, the adversarial pass in `editor-checklist.md`, Parker's tastes in `parker-preferences.md` (those win on conflict).

Note type is 2-field: **Text** (the cloze) + **Back Extra** (the teaching half, lines open with `Cue:`/`Distinguish:`/`Pitfall:`/`Why:`/`Mechanism:`/`Ex:`/`Pathway:`/`Mnemonic:`/`Meaning:`). HTML allowed: `<b>`, `<i>`, `<br>`, `<img>` only (selective emphasis; no `<u>`).

---

## 1. How to choose an archetype

Do **Rule 0 first** (card-rules): if the highlight is one leg of a connected set, zoom out and treat the set as one unit before classifying. Then classify the *load-bearing fact* and jump to its section:

| If the highlight's point is… | Use | §  |
|---|---|---|
| A named label bound to its meaning (term ↔ definition) | **Definition** (two-way by default) | 4 |
| A single number, cutoff, range, dose, timing, or equation | **Numbers & Equations** | 5 |
| The members of a set / a mnemonic / a head-to-toe checklist | **Lists & Enumerations** | 6 |
| An ordered protocol, pathway, or "what's the next step" sequence | **Sequences & Mechanisms** | 7 |
| "Which of two?" / up-down-normal / X-vs-Y discrimination | **Comparisons & Direction-of-Change** | 8 |
| A hallmark sign/buzzword → one answer, OR a patient scenario → impression/action | **Buzzwords & Vignettes** | 9 |
| "EXCEPT / never / contraindicated / do NOT / cannot" | **Negation & Exception** | 10 |
| A standalone fact whose *value is the teaching context* (mechanism, contrast, mnemonic) | **Teaching-Half & Mnemonics** | 11 |

**Decision shortcuts.** Distinctive short cue → one answer = buzzword. Needs 2-4 clues to be solvable = vignette. Several coordinate members = list. Arrow / "because" / "then" / direction word doing the work = sequence/comparison, not list. Could be answered by a *number* but not a sentence = numeric. A term you'd recognize AND produce = two-way definition.

**EMT default bias:** the NREMT is an *application* exam. Most clinical highlights should become a decision, not a factoid. When a highlight is a sign / threshold / finding, also emit a short **vignette** card that forces the field decision (§9). If fewer than ~1 in 4 cards for a clinical chapter makes Parker *decide* something, the batch is too factoid-heavy.

### Target archetype mix per clinical chapter (Airway, Shock, Cardiac, Trauma, Assessment push application even higher)
- ~30% scenario / application (§9)
- ~20% indication / contraindication / "when do you do X" trigger (§10, §9)
- ~15% sign/symptom → field impression (§9)
- ~15% assessment-sequence & treatment-order (§7)
- ~10% normal ranges + dose/quantity facts (§5)
- ~7% definitions, action-changing only (§4)
- ~3% anatomy / mechanism / "why" (§7, §11)

**Recall-heavy chapters flip toward definitions/rules:** EMS Operations, Medical/Legal, Lifting & Moving, Ambulance Ops (consent types, negligence components, hazmat zones, triage, scope-of-practice). Less scenario there.

**EMT-native patterns the AnKing Step/MCAT decks don't emphasize — build these on purpose:**
1. **Contraindication pairs** — indication AND contraindication together so they don't blur (§10).
2. **"When do you do X" triggers** — one card per intervention, framed as the field trigger (§9).
3. **Age-banded vital ranges** — a tight grouped sub-set (adult / child / infant), anchor to one source (the AAOS/course numbers) (§5, §6).
4. **The finite EMT drug box** — the 5 rights + indication + contraindication + exact dose; skip mechanism of action (§5).
5. **Scope-of-practice boundaries** — EMT-B vs AEMT vs Paramedic; "can an EMT do X" (§9/§10).

**Default flips vs a med deck:** drug → rights/indication/contra/**dose** (not MOA); condition → field S/S → impression → BLS treatment + transport (not pathophys); number → number **+ the action it triggers**; anatomy → occlude only assessment-relevant figures; legal/ethical concept → **card it** (med decks skip these, they're easy NREMT points); MOI → index-of-suspicion card. Don't over-card: a finite syllabus + application exam means *hundreds* of dense decision-cards, not tens of thousands of trivia.

---

## 2. The non-negotiables (research-backed; every card must pass all)

1. **Tests recall, not recognition.** The answer is hidden and produced from memory. *(Testing effect; generation effect.)*
2. **Atomic — one fact, one schedulable unit.** No compound answers, no "and." A genuine cohesive *set* may share one cloze number (§6), but two *independent* facts = two cards. *(Minimum-information; cognitive load; spacing.)*
3. **Exactly one correct answer.** Hide the cloze: a knowledgeable EMT cannot legitimately give a different right answer. If several fit, constrain the stem. *(Cue discriminability; interference.)*
4. **The front carries enough context to make the answer unique** and to match the test situation — the cue Parker studies with is the cue at the exam. *(Encoding specificity.)*
5. **Answer is short** — a word, phrase, or number that fits in working memory in one chunk; never a paragraph. *(Cognitive load.)*
6. **Both directions become separate cards only when both are real goals** — never assume one direction trains the reverse. *(Recall is directional; backward transfer is real but unreliable.)*
7. **Confusable siblings are made mutually discriminable** — the distinguishing feature appears in the cue or the `Distinguish:` line. *(Interference; the defensible core of interleaving.)*
8. **Visual/spatial facts use images** (image-occlusion ideally), not words alone — but only *relevant* images, never decorative. *(Dual coding.)*
9. **Emphasis is signal, not decoration; explanations use plain language.** Bold or italicize only the genuinely load-bearing word(s) — the negator, the contrast pivot, the one term the eye must land on. Styling several words, or styling "to look formatted," destroys the signal. When a Back Extra explains or defines, use plain words a layperson knows; never define a hard term with more jargon — gloss it in the same line. *(Parker: "don't make me look up six more words.")*

**Hint hard rule (all archetypes):** a hint constrains the answer's *form* (category, count, binary options, first letter) and NEVER leaks its content. The two licensed leak-on-purpose exceptions are first-letter mnemonic cues and forced-choice option lists (the point there is *which*, not the word). Default is **no hint** — only ~16-21% of live AnKing clozes carry one.

---

## 4. Definition (one-way & two-way)

**When:** the highlight is a clean "X is Y" — a vocabulary term, equipment, structure, condition, drug class, legal/operational concept whose value is the term↔meaning binding. Not for enumerations, sequences, bare numbers, or "what do you do for X" (that's a vignette).

**Template — two-way (Parker's default for foundational vocab):**
```
{{c1::TERM::hint}} is {{c2::tight defining property}}.
```
Different numbers → 2 cards: c1 hides the term (describe → name), c2 hides the meaning (name → state it). Keep the c2 side CRISP (a few discriminating words, never a long definition). Articles go OUTSIDE the brace: `A/an {{c1::free radical}} is…`. Term span ~1-2 words, definition ~3-6.

**One-way** when only one direction is useful: hide the TERM for sign/condition recognition (the NREMT scenario direction — vivid description → name it); hide the DEFINITION when the term is familiar and only its precise meaning matters. Do NOT two-way lists, sequences, numbers, or scenario facts.

**Hint:** category-suffix for named entities (`::... reflex`, `::... position`, `::... Scale`); a one-word class label (`::vital sign`, `::airway maneuver`); forced binary when the blank is otherwise open (`::male/female`). Skip if the stem already forces the answer.

**Back Extra:** `Distinguish:` is the highest-value line (pin against the nearest confusable — hypoxia vs hypoxemia, crepitus vs subcutaneous emphysema). Then `Cue:`/`Pitfall:`/`Why:`. Never re-define the term.

**Do:** write the full "X is Y" sentence first, then decide which half to hide; make the definition specific enough that exactly one term fits. **If the sentence also carries a goal, function, cause, or key qualifier, that is a SECOND testable fact — give it its own cloze (`c3`), don't leave it as visible scenery.** (The under-clozing trap for definitions: "public health examines the needs of {{c2::populations}}, with the goal of {{c3::preventing health problems}}" — the *goal* gets clozed too, not just the term and the "who.") **Don't:** put term + meaning under the *same* number (all-blanks, unanswerable); cloze a word so generic the rest gives it away ("hypoxia is low {{c1::oxygen}}" — hide the discriminator instead).

**Examples:**
```
Text: {{c1::Hypoxia::condition}} is {{c2::inadequate oxygen at the cellular (tissue) level}}.
Back Extra: Distinguish: hypoxemia = low O2 in the blood; hypoxia = O2 not reaching the tissues.
Cue: earliest reliable sign is altered mental status, NOT cyanosis (a late sign).
```
```
Text: {{c1::Crepitus}} is the {{c2::grating sound of broken bone ends rubbing together}}.
Back Extra: Distinguish: subcutaneous emphysema also crackles, but that is air under the skin, not bone-on-bone.
Pitfall: never intentionally re-elicit it; it causes pain and further injury.
```

---

## 5. Numbers, values, cutoffs & equations

**When:** the load-bearing fact is quantitative/notational — a cutoff with an operator (SpO2 < 94%), a normal range (RR 12-20/min), a dose (aspirin 324 mg), a timing/interval, a count/percentage, or an equation (minute volume = Vt × RR). Test: if the best answer is "126 mg/dL" not a sentence, it's this archetype.

**Template A — numeric value/cutoff/range:** the WHOLE expression (operator + value + unit) lives in ONE cloze.
```
What is the systolic BP cutoff that defines hypotension in an adult? {{c1::< 90 mmHg}}
What is the normal adult respiratory rate range? {{c1::12-20/min::rate}}
```
Strip the unit out only when the stem already prints the operator and unit: `SpO2 falls below {{c1::94}}%`.

**Template B — equation:** stem says "Give the equation for X", whole formula in one cloze, DEFINE every variable in Back Extra.
```
Give the equation for minute volume: {{c1::tidal volume (Vt) × respiratory rate (RR)}}
```

**Hint:** sparingly, to signal FORM only — `::range`, `::rate`, `::dose`, `::Duration`, `::%`, `::age group`. Never put a number in the hint.

**Back Extra:** `Distinguish:` is the workhorse — anchor the clozed value against the value it must not be confused with (cloze the abnormal cutoff → give the normal range; cloze the adult rate → give the pediatric rates). Then `Why:` (the physiology of the number), `Ex:` (a worked plug-in for equations), `Pitfall:` (unit confusion, 1:1,000 vs 1:10,000 epi).

**Do:** pin the number with a single-target stem; keep operator and range inside the deletion. **Don't:** strand the unit outside a standalone cloze ("{{c1::126}} mg/dL" — a bare number is untestable and a wrong unit is a safety error); split value and unit into two blanks; leave the operator outside ("< {{c1::90 mmHg}}"); split a MathJax `\( \)` across the cloze boundary. **Safety:** every number/dose/threshold card → `needs_human_check: true`.

**Examples:**
```
Text: What aspirin dose is given for suspected cardiac chest pain (no contraindications)? {{c1::324 mg (4 x 81 mg chewable)::dose}}
Back Extra: Why: chewing non-enteric-coated aspirin speeds antiplatelet action.
Distinguish: nitroglycerin is 0.4 mg SL — a different drug and number; do not swap them.
```
```
Text: What is the normal respiratory rate range for an adult at rest? {{c1::12-20/min::rate}}
Back Extra: Distinguish: child 15-30/min; infant 25-50/min.
Pitfall: rate alone is not enough — also judge depth and effort.
```

---

## 6. Lists, enumerations & classifications

**When:** the highlight teaches the *members of a set* — a mnemonic (SAMPLE, OPQRST, DCAP-BTLS, AVPU), a head-to-toe checklist, the layers/types/components of something, or a sort-into-category fact. If you could shuffle the items with no loss of meaning it's a flat list; if order matters it's a sequence (§7).

**Template — grouped reveal (default):** every member shares ONE cloze number so the whole set blanks together and Parker must produce all of it.
```
The components of <b>SAMPLE</b> history are:<br>
{{c1::Signs/Symptoms::S}}<br>{{c1::Allergies::A}}<br>{{c1::Medications::M}}<br>{{c1::Past history::P}}<br>{{c1::Last oral intake::L}}<br>{{c1::Events leading up::E}}
```
Name the parent AND its count in the stem. Keep each blank atomic (1-3 words). For a 2-way contrast list, give BOTH sides the same option-pair hint (`::arterial/venous`). For a sort-into-category list, the binary hint repeats on every line (`::basic/advanced`).

**This is Parker's "big lists stay whole" rule:** a genuine cohesive list goes in ONE grouped card no matter the length (Star of Life = 6 functions, EMS Agenda 2050 = 6 principles). Only split into *sibling cards* (one per item, different numbers) when the items are genuinely independent facts that merely happen to be listed. Never `{{c1::A}}, B, C` (tests A, gives away the rest).

**Hint:** first-letter for acronyms (`::S`, `::Ca`); count when several items hide behind one blank (`::3`); category label when the answer class isn't obvious (`::treatment`). Direction legend for trend panels (`::↑↓`).

**Back Extra:** `Mnemonic:` (the acronym expansion in order) is the single most useful line; then `Distinguish:` for contrast lists, `Pitfall:` for the trap (OPA needs NO gag reflex; NPA tolerates one).

**Do:** name the set + count in the stem; preserve fixed mnemonic order even in a "flat" list (don't shuffle DCAP-BTLS); keep flat grouped lists to ~5-7 members. **Don't:** give list items separate numbers hoping for sequence; cloze the category label; dump a 12-item list into one note (split by logical subset); turn an open-ended "such as" list into a closed memorize-these card.

**Examples:**
```
Text: The components of <b>DCAP-BTLS</b> (rapid trauma assessment) are:<br>{{c1::Deformities::D}}<br>{{c1::Contusions::C}}<br>{{c1::Abrasions::A}}<br>{{c1::Punctures/penetrations::P}}<br>{{c1::Burns::B}}<br>{{c1::Tenderness::T}}<br>{{c1::Lacerations::L}}<br>{{c1::Swelling::S}}
Back Extra: Mnemonic: DCAP-BTLS — inspect and palpate for each at every body region.
Why: a systematic head-to-toe sweep so no soft-tissue injury is missed.
```
```
Text: Classify each airway adjunct as basic or advanced:<br>OPA = {{c1::basic::basic/advanced}}<br>NPA = {{c1::basic::basic/advanced}}<br>Endotracheal tube = {{c1::advanced::basic/advanced}}<br>Supraglottic (King LT / i-gel) = {{c1::advanced::basic/advanced}}
Back Extra: Distinguish: basic adjuncts only position the tongue; advanced airways pass the glottis (AEMT/paramedic scope).
Pitfall: an OPA needs NO gag reflex; an NPA is tolerated with a gag reflex.
```

---

## 7. Sequences, pathways & mechanisms

**When:** the fact IS a relationship or an order — an ordered protocol/algorithm, an anatomic/flow pathway, a cause→effect chain, or a "what's the next step" decision. The tell: an arrow, "because/due to/leads to", "first→then→next", or a branching mild→A / severe→B. If order doesn't matter it's a list (§6).

**Template — ordered chain (default grouped):** write every step in true order, arrows OUTSIDE the cloze, all steps share c1.
```
Trace the path of air from the mouth to the alveoli:<br><br>
{{c1::pharynx}} → {{c1::larynx}} → {{c1::trachea}} → {{c1::bronchi}} → {{c1::bronchioles}} → {{c1::alveoli}}
```
Numbered protocol (order is the answer; never shuffle):
```
1. {{c1::step one}}<br>2. {{c1::step two}}<br>3. {{c1::step three}}
```
**Single causal link:** hide the one load-bearing node — `{{c1::Hypoxia}} causes altered mental status`. Use sequential c1→c2→c3 ONLY when each transition is independently worth drilling (rare; don't fragment a 7-item flow path). **Branching ladder:** both arms in one group with role hints — `Mild → {{c1::do A::Initial}}<br>Severe → {{c1::do B::Severe}}`.

**Hint:** binary direction is mandatory on any direction-of-change blank (`::increases or decreases`); role/severity on branch rungs (`::Initial`, `::if worse`); count when a blank hides several items.

**Back Extra:** `Mechanism:` (the arrow chain behind the link), `Why:` (why this order — compressions before breaths because circulating oxygenated blood matters more), `Pathway:` (restate the full route), `Pitfall:`.

**Do:** keep arrows and connectives ("leads to", "then") visible as the scaffold; state direction in the stem ("nose → alveoli"). **Don't:** cloze the arrows or connectives; reorder or shuffle an ordered note; split one inseparable memorized sequence into c1…c7.

**Examples:**
```
Text: Cardiac arrest — adult BLS sequence:<br><br>1. {{c1::Check responsiveness and breathing}}<br>2. {{c1::Activate EMS and get the AED}}<br>3. {{c1::Start chest compressions (30:2)}}<br>4. {{c1::Attach AED and analyze rhythm}}<br>5. {{c1::Shock if advised, then resume CPR}}
Back Extra: Why: compressions first (C-A-B) — circulating already-oxygenated blood matters more than a first breath.
Pitfall: minimize interruptions; resume compressions immediately after a shock.
```
```
Text: In <b>hypovolemic shock</b>, blood loss causes {{c1::decreased::increased or decreased}} preload, which {{c1::decreases::increases or decreases}} cardiac output and {{c1::decreases::increases or decreased}} blood pressure.
Back Extra: Mechanism: blood loss → ↓ venous return → ↓ stroke volume → ↓ cardiac output → ↓ BP.
Pitfall: a normal BP does NOT rule out shock (compensated); a falling BP is a late, decompensated sign.
```

---

## 8. Comparisons & direction-of-change (X-vs-Y / up-down-normal)

**When:** the point is "which way / which one," not "what is it." Signals: "compared to / versus / whereas / unlike", or a vital/level that goes UP / DOWN / stays NORMAL under a condition. Both sides must share a real axis — if there's no genuine second entity on one axis, it's a plain definition.

**Template — two-sided grouped contrast:** name both entities and the shared axis in the stem; cloze ONLY the differing values, both under the SAME number so they reveal together.
```
Compared to <b>arterial</b> bleeding, <b>venous</b> bleeding is {{c1::lower::higher or lower}} pressure and {{c1::darker::darker or brighter}} red.
```
**Direction-of-change panel (the NREMT vital-trend template):** one condition, several vitals, all c1, every line legended.
```
In <b>compensated shock</b>:<br>Heart rate: {{c1::Increased::Increased/Decreased/Normal}}<br>Systolic BP: {{c1::Normal::Increased/Decreased/Normal}}<br>Skin: {{c1::Pale, cool, clammy}}<br>Cap refill: {{c1::Delayed (>2 s)::Delayed or Normal}}
```

**Hint:** legend EVERY bare directional answer (match the answer's spelling: answer "higher" → `::higher or lower`; answer "Decreased" → `::Increased/Decreased`). Offer the third state (`Normal`/`No change`) whenever unchanged is genuinely possible.

**Back Extra:** `Distinguish:` carries the OTHER side / the value you didn't cloze (cross-link the pair); `Why:`/`Mechanism:` for why a value moves; `Pitfall:` for the trap (a normal/rising BP in a child is dangerously late).

**Do:** keep the comparator word visible; use strictly parallel phrasing so the only variable is the answer; build mirror cards for symmetric pairs if both directions are real goals. **Don't:** cloze the entity names or the shared axis; cloze the analyte and leave the direction showing; leave a bare directional blank with no legend; force a comparison between things with no shared axis.

**Example:**
```
Text: A <b>tension pneumothorax</b> makes breath sounds {{c1::decreased/absent::increased or decreased}} on the affected side, whereas <b>JVD</b> is {{c1::increased::increased or decreased}}.
Back Extra: Mechanism: trapped air collapses the lung (no breath sounds) and squeezes the great vessels → blood backs up into the neck veins.
Distinguish: simple pneumothorax has absent breath sounds but NO JVD and no hemodynamic collapse.
```

---

## 9. Buzzwords & clinical vignettes (recognition → application)

**The NREMT workhorse.** Two siblings:

**Buzzword** — a single distinctive cue → ONE high-yield answer (a hallmark sign-in-words, a named triad/rule, a "X is associated with Y"). **Vignette** — a short patient/scene where the payoff is the field impression, the cause, or the next action. Short distinctive token → buzzword; needs a 2-4 clue constellation → vignette.

**Template — buzzword:** keep the cue 100% VISIBLE, cloze only the payoff.
```
What is the most likely cause of cherry-red skin, headache, and confusion in two patients found in a running car in a closed garage? {{c1::Carbon monoxide poisoning}}
```
**Template — vignette (next-action is the NREMT favorite verb):** self-contained stem packing the 2-4 discriminators, ONE blank on the conclusion.
```
<scenario with the discriminating clues left visible>. What is the best next step? {{c1::action}}
```
Pair the diagnosis and the action with the same number to reveal together, labeling each: `{{c1::tension pneumothorax::diagnosis}}` … `{{c1::needle decompression::next step}}`.

**Auto-pair rule:** for any highlight that is a *sign / finding / threshold*, also emit one short vignette that embeds the fact in a 1-2 sentence patient stem. The highlight gives the fact; the vignette forces the decision. This single habit does most of the work of "NREMT-ifying" the deck.

**Hint:** sparing — a confusable menu (`::osmotic / secretory`), an answer-type label in multi-part stems (`::diagnosis`, `::next step`, `::volume`), or a direction (`::rises / falls`). Don't hint when the stem already forces one answer.

**Back Extra:** `Cue:` (name the buzzword and why it points here), `Distinguish:` (the mimic and the one separating feature), `Why:`/`Mechanism:`, `Pitfall:` (the field trap / can't-miss action).

**Do:** quote vivid descriptors verbatim ("coffee-ground emesis", "fruity breath"); keep vignette stems single-decision; write ACTION vignettes as often as diagnosis ones; spawn age variants (peds/geriatric modifier on a known fact). **Don't:** cloze the buzzword/clue/lab value (destroys the association); scatter blanks across the discriminators (blank the endpoint only); write a stem that admits two diagnoses; depend on an image the text-only card lacks; make an exhaustive "name all 5" set (that's §6).

**Examples:**
```
Text: A driver with chest trauma has JVD, tracheal deviation away from the injured side, and absent breath sounds on that side with worsening dyspnea. Field impression? {{c1::Tension pneumothorax::diagnosis}}<br><br>Immediate intervention? {{c1::Needle chest decompression (beyond EMT scope — request ALS)::next step}}
Back Extra: Cue: JVD + tracheal deviation + unilateral absent breath sounds = tension pneumothorax until proven otherwise.
Distinguish: simple pneumothorax has absent breath sounds but no JVD/deviation or shock.
```
```
Text: Adult trauma patient breathing 8/min and shallow. Your action? {{c1::Assist ventilations with a BVM at ~10/min plus high-flow oxygen::next step}}
Back Extra: Why: RR < 12 with poor tidal volume means inadequate minute volume — ventilate, don't just give oxygen.
Pitfall: a present respiratory rate is not the same as adequate breathing.
```

---

## 10. Negation & exception (EXCEPT / never / contraindicated / cannot)

**When:** the fact is memorable because it BREAKS an expected pattern or is a safety carve-out — "except", "all … but", "never", "contraindicated", "do not give", "cannot", "least likely". Litmus: delete the negator; if the sentence flips to FALSE, it's a true negation card.

**Template — keep the negator LOUD and in plain text; cloze the carve-out, the unsafe population, or the polarity word:**
```
<b>Nitroglycerin</b> is <u>contraindicated</u> if the patient took {{c1::an erectile-dysfunction medication (e.g. sildenafil)}} within the last {{c2::24 to 48 hours}}.
```
*(Note: `<u>` is not in Parker's allowed HTML — use `<b>` to emphasize the negator: `is <b>contraindicated</b>`.)*
Polarity fact → cloze the direction word with a binary hint: `{{c1::cannot::can/cannot}}`. Multi-item exclusion set → group every excluded item under ONE number + a count hint so they hide together (`{{c1::I and II::2}}`), never separate numbers.

**Hint:** binary polarity (`::can/cannot`, `::indicated/contraindicated`) on polarity cards; count (`::2`) on exclusion sets. Don't first-letter-hint the exception itself.

**Back Extra:** `Distinguish:` the contrasting sibling that breaks the other way (the drug that IS safe, the test that DOES apply); `Why:`/`Mechanism:` the reason for the carve-out; `Pitfall:` the trap this card defuses.

**Do:** capitalize/bold the negator so it can't be skimmed; cloze the exception/population/polarity, never the negator alone; pair indication with contraindication. **Don't:** cloze the bare negator with nothing else hidden (a guessable coin-flip); leave the negator in skim-past lowercase; give exclusion items separate numbers; invent a "never" the AAOS text states as only relative.

**Examples:**
```
Text: <b>Oral glucose</b> is <b>contraindicated</b> if the patient is {{c1::unconscious}} or {{c1::unable to swallow}}.
Back Extra: Why: an unprotected airway plus glucose gel risks aspiration.
Distinguish: for a conscious diabetic who can swallow, oral glucose is indicated for suspected hypoglycemia.
```
```
Text: You should control all external bleeding with direct pressure, <b>except</b> {{c1::an impaled object}}, which you {{c1::leave in place and stabilize}}.
Back Extra: Why: removing it can trigger uncontrolled internal hemorrhage.
Pitfall: bulky-dress AROUND the object; do not apply pressure on top of it.
```

---

## 11. Teaching-half & mnemonics (lean front, rich back)

**When:** the highlight is testable in one breath but would be rote, confusing, or dangerous-to-confuse without context — a term whose value is the contrast, a protocol step where the WHY is the high-yield part, a one-fact mechanism, OR any *arbitrary* list with no internal logic (the mnemonic trigger). If you catch yourself writing "because…", "unlike…", "but NOT when…" on the front, that clause is Back-Extra material.

**Template — teaching front (lean cloze, back teaches):**
```
What should you rule out FIRST in any patient with altered mental status? {{c1::Hypoglycemia (check a blood glucose)}}
```
Back Extra carries the mechanism / discriminator / caveat the front deliberately omits.

**Template — acronym IS the answer (the dominant mnemonic form):**
```
The components of a focused trauma history are recalled with the mnemonic {{c1::SAMPLE}}.
```
Put the ordered expansion in Back Extra under `Mnemonic:`. (If Parker wants each item drilled instead, use the §6 first-letter-hinted grouped list.)

**Hint:** disambiguation only — a category noun (`::status`, `::drug`), a binary frame, or a first letter inside a spelled mnemonic. The hint never explains.

**Back Extra:** `Why:`/`Mechanism:` (ideally an arrow chain), `Distinguish:` (name the OTHER entity and the one separating feature), `Pitfall:`, `Cue:`, `Mnemonic:` (letter-by-letter, in order). A teaching card should almost never have an empty Back Extra.

**Do:** keep the front one recallable fact; reserve mnemonics for genuinely arbitrary lists (don't force one onto reason-able anatomy or derivable doses); cloze the acronym when "name the mnemonic" is the skill. **Don't:** cram the explanation onto the front; put the real teaching in a `::hint`; cloze both the acronym AND every item on the same card.

**Examples:**
```
Text: What is the most likely cause of altered mental status that a blood glucose check should rule out before anything else? {{c1::Hypoglycemia}}
Back Extra: Why: it is rapidly reversible and rapidly fatal, and it mimics stroke, intoxication, and postictal states.
Pitfall: treating the "obvious" diagnosis while a low sugar goes uncorrected can cause permanent brain injury in minutes.
```
```
Text: The components of a focused trauma history are recalled with the mnemonic {{c1::SAMPLE}}.
Back Extra: Mnemonic: Signs/Symptoms, Allergies, Medications, Past pertinent history, Last oral intake, Events leading up.
Cue: "Last oral intake" and "Events" are the two most often forgotten under stress.
```

---

## Quick self-check before staging (mirrors editor-checklist.md)
One answer · no leak · grounded in context · fully clozed (no testable fact left in plain text) · lists handled (grouped or sibling, never cloze-one-reveal-rest) · crisp deletion · cohesive not crammed · built on real knowledge not filler · hint is a clean slot-label · standalone (no deixis/source words) · Back Extra earns its place. Number/dose/threshold or weak grounding → `needs_human_check: true`.
