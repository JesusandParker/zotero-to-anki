#!/usr/bin/env python3
"""test_regressions.py — the executable half of reference/regression-cases.md.

Every MECHANICALLY-catchable regression class gets a behavioral case here: a BAD
exemplar the checker MUST flag, and the neighboring GOOD shape it must NOT
over-flag. Run this after ANY change to scripts/check_cards.py (or to a rule
that a detector implements):

    python3 scripts/test_regressions.py

It runs the real check_cards.py as a subprocess (so refactors are tested, not
imports) and asserts on warning substrings. Exit 0 = suite green. Semantic-only
classes (R9 open-set) have no case here — they live with the LLM judge; see
reference/regression-cases.md for the full library including those.
"""
import json, os, subprocess, sys, tempfile

CHECKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_cards.py")

# Each case: cards (a batch, usually one), the warning substring, and whether it
# must be present (BAD shape) or absent (GOOD shape that must not be over-flagged).

# Shared fixtures for the purple-lane cases (R35–R37). The cards claim source
# "_regression", whose evidence file is a PERMANENT fixture at
# work/_regression/lexicon_evidence.json (diaphor resolves; syncop does not).
LEX_MARKS = [
    {"kind": "lexicon", "page": "612", "highlight": "diaphoretic",
     "term": "diaphoretic", "term_key": "diaphor",
     "context": "The patient was pale and diaphoretic, with a rapid, thready pulse."},
    {"kind": "lexicon", "page": "690", "highlight": "syncope",
     "term": "syncope", "term_key": "syncop",
     "context": "Syncope was reported before the fall."},
    {"kind": "text", "page": "612", "highlight": "Shock produces pale, cool, moist skin.",
     "context": "Shock produces pale, cool, moist skin as blood is shunted to the core."},
]

CASES = [
    # --- R35: an external-anchored authored definition must arrive FLAGGED -----------
    {
        "id": "r35_bad_external_definition_unflagged",
        "warn": "external-anchored definition without needs_human_check",
        "present": True, "scope": "hard",
        "highlights": LEX_MARKS,
        "cards": [{"Text": "<b>Syncope</b> is {{c1::a brief fainting spell}}.",
                   "Back Extra": "Ex: \"<b>Syncope</b> was reported before the fall.\"",
                   "kind": "lexicon", "source": "_regression", "segment": 1,
                   "from_idx": [1], "needs_human_check": False,
                   "lexicon": {"term": "syncope", "term_key": "syncop",
                               "anchor": {"method": "external"}}}],
        "note": "the authored definition the book can't confirm must reach Parker's eyes",
    },
    {
        "id": "r35_good_external_definition_flagged",
        "warn": "external-anchored definition without needs_human_check",
        "present": False,
        "highlights": LEX_MARKS,
        "cards": [{"Text": "<b>Syncope</b> is {{c1::a brief fainting spell}}.",
                   "Back Extra": "Ex: \"<b>Syncope</b> was reported before the fall.\"",
                   "kind": "lexicon", "source": "_regression", "segment": 1,
                   "from_idx": [1], "needs_human_check": True,
                   "lexicon": {"term": "syncope", "term_key": "syncop",
                               "anchor": {"method": "external"}}}],
    },
    # --- R36: the lane cannot be self-asserted (kind must match the marks' kind) -----
    {
        "id": "r36_bad_text_card_from_purple_marks_only",
        "warn": "cites ONLY purple lexicon mark",
        "present": True, "scope": "hard",
        "highlights": LEX_MARKS,
        "cards": [{"Text": "A diaphoretic patient shows {{c1::pale, sweaty skin}}.",
                   "Back Extra": "Cue: classic early-shock skin signs.",
                   "kind": "text", "source": "_regression", "segment": 1,
                   "from_idx": [0]}],
        "note": "a yellow-lane card built purely from purple marks dodges the lexicon contract",
    },
    {
        "id": "r36_bad_lexicon_card_citing_yellow_mark",
        "warn": "cites non-purple mark",
        "present": True, "scope": "hard",
        "highlights": LEX_MARKS,
        "cards": [{"Text": "<b>Diaphoresis</b> is {{c1::heavy, drenching sweating}}.",
                   "Back Extra": "Ex: \"The patient was pale and <b>diaphoretic</b>…\"",
                   "kind": "lexicon", "source": "_regression", "segment": 1,
                   "from_idx": [2],
                   "lexicon": {"term": "diaphoresis", "term_key": "diaphor",
                               "anchor": {"method": "in_source"}}}],
        "note": "kind: lexicon citing a yellow mark would dodge R13's word-overlap block",
    },
    {
        "id": "r36_good_foldin_cites_purple_plus_yellow",
        "warn": "purple",
        "present": False, "scope": "hard",
        "highlights": LEX_MARKS,
        "cards": [{"Text": "In early shock the skin turns {{c1::pale, cool, and moist}}.",
                   "Back Extra": "Ex: \"The patient was pale and <b>diaphoretic</b>…\"",
                   "kind": "text", "source": "_regression", "segment": 1,
                   "from_idx": [0, 2]}],
        "note": "a Stage-2.5 fold-in legitimately cites both lanes; must not block",
    },
    # --- R37: a claimed in-source anchor must RESOLVE to mechanical evidence ---------
    {
        "id": "r37_bad_claimed_anchor_without_evidence",
        "warn": "no resolving entry",
        "present": True, "scope": "hard",
        "highlights": LEX_MARKS,
        "cards": [{"Text": "<b>Syncope</b> is {{c1::a brief fainting spell}}.",
                   "Back Extra": "Ex: \"<b>Syncope</b> was reported before the fall.\"",
                   "kind": "lexicon", "source": "_regression", "segment": 1,
                   "from_idx": [1],
                   "lexicon": {"term": "syncope", "term_key": "syncop",
                               "anchor": {"method": "in_source"}}}],
        "note": "the R33 lesson: an exemption the drafter can assert is no exemption at all",
    },
    {
        "id": "r37_good_resolving_anchor_passes",
        "warn": "no resolving entry",
        "present": False,
        "highlights": LEX_MARKS,
        "cards": [{"Text": "<b>Diaphoresis</b> is {{c1::heavy, drenching sweating}}.",
                   "Back Extra": "Ex: \"The patient was pale and <b>diaphoretic</b>…\"",
                   "kind": "lexicon", "source": "_regression", "segment": 1,
                   "from_idx": [0],
                   "lexicon": {"term": "diaphoresis", "term_key": "diaphor",
                               "anchor": {"method": "in_source"}}}],
    },
    # --- R25/R26: retrieval load (Parker 2026-08-02, the 10-element radio report) ---
    # The thresholds here are CALIBRATION, not taste: each of these four cases is a card
    # Parker himself graded in the report that created the rule, and the detector has to
    # reproduce his verdict. If a future change breaks one of these, the rule has drifted
    # away from the person it exists to serve.
    {
        "id": "r25_bad_ten_uncued_items_is_unpassable",
        "warn": "card-rules #23", "present": True, "scope": "hard",
        "cards": [{"Text": "An EMT's <b>radio patient report</b> commonly includes 10 elements, in order:<br><br>1. {{c1::Unit ID and service level}}<br><br>2. {{c1::Any special alert}}<br><br>3. {{c1::Receiving hospital and ETA}}<br><br>4. {{c1::Patient's age and sex}}<br><br>5. {{c1::Chief complaint and severity}}<br><br>6. {{c1::Brief history of current problem}}<br><br>7. {{c1::Brief report of physical findings}}<br><br>8. {{c1::Summary of care given}}<br><br>9. {{c1::Patient's response to treatment}}<br><br>10. {{c1::Any additional questions or orders}}",
                   "Back Extra": "Cue: the report tells the call's story in order.", "chapter": 4}],
        "note": "Parker's prime example: 5 reviews, 5 Again, 54s each, never answered — must HARD block",
    },
    {
        "id": "r25_bad_eight_uncued_items",
        "warn": "card-rules #23", "present": True, "scope": "hard",
        "cards": [{"Text": "The eight presumptive signs of death are:<br><br>{{c1::Unresponsiveness to painful stimuli}}<br><br>{{c1::Lack of a carotid pulse}}<br><br>{{c1::Absence of chest rise and fall}}<br><br>{{c1::No deep tendon reflexes}}<br><br>{{c1::No pupillary reactivity}}<br><br>{{c1::No systolic blood pressure}}<br><br>{{c1::Profound cyanosis}}<br><br>{{c1::Lowered or decreased body temperature}}",
                   "Back Extra": "Pitfall: presumptive signs alone do not establish death.", "chapter": 3}],
    },
    {
        "id": "r25_good_chart_acronym_is_one_chunk",
        "warn": "card-rules #23", "present": False,
        "cards": [{"Text": "The 5 sections of a <b>CHART</b> narrative are:<br><br>{{c1::Chief complaint::C}}<br><br>{{c1::History and physical examination::H}}<br><br>{{c1::Assessment::A}}<br><br>{{c1::Treatment (Rx)::R}}<br><br>{{c1::Transport::T}}",
                   "Back Extra": "Mnemonic: C-H-A-R-T, with the R coming from Rx.", "chapter": 4}],
        "note": "Parker named this one GOOD: the acronym IS the anchor and splitting it destroys that",
    },
    {
        "id": "r25_good_five_step_protocol_under_cap",
        "warn": "card-rules #23", "present": False,
        "cards": [{"Text": "<b>Giving</b> a handover report follows a five-point method, in order:<br><br>1. {{c1::Initiate eye contact}}<br><br>2. {{c1::Manage the environment}}<br><br>3. {{c1::Ensure the ABCs}}<br><br>4. {{c1::Provide a structured report}}<br><br>5. {{c1::Provide documentation}}",
                   "Back Extra": "Why: eye contact marks that the handover is beginning.", "chapter": 4}],
        "note": "Parker named this one GOOD — 5 uncued sits under the warn threshold",
    },
    {
        "id": "r25_good_dcap_btls_mnemonic_licenses_eight",
        "warn": "card-rules #23", "present": False,
        "cards": [{"Text": "The components of <b>DCAP-BTLS</b> (rapid trauma assessment) are:<br><br>{{c1::Deformities::D}}<br><br>{{c1::Contusions::C}}<br><br>{{c1::Abrasions::A}}<br><br>{{c1::Punctures/penetrations::P}}<br><br>{{c1::Burns::B}}<br><br>{{c1::Tenderness::T}}<br><br>{{c1::Lacerations::L}}<br><br>{{c1::Swelling::S}}",
                   "Back Extra": "Mnemonic: DCAP-BTLS at every body region.", "chapter": 10}],
        "note": "8 items but ONE chunk — the letters regenerate the set; must not warn OR block",
    },
    {
        "id": "r25_good_cued_rows_are_not_one_wide_recall",
        "warn": "card-rules #23", "present": False,
        "cards": [{"Text": "Normal <b>pulse rate</b> in beats/min, by age group:<br><br>Neonate — {{c1::100 to 180}}<br><br>Infant — {{c1::100 to 160}}<br><br>Toddler — {{c1::90 to 150}}<br><br>Preschool age — {{c1::80 to 140}}<br><br>School age — {{c1::70 to 120}}<br><br>Adolescent — {{c1::60 to 100}}",
                   "Back Extra": "Pitfall: rate alone is not enough — judge depth and effort too.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "each row carries its own key, so this is 6 cued retrievals, not a 6-wide one",
    },
    {
        "id": "r25_good_classify_card_rows_are_cued",
        "warn": "card-rules #23", "present": False,
        "cards": [{"Text": "Match each function of the blood to the component that carries it out:<br><br>Fights infection → {{c1::white blood cells}}<br><br>Transports oxygen → {{c1::red blood cells}}<br><br>Forms clots → {{c1::platelets}}<br><br>Carries the cells and nutrients → {{c1::plasma}}<br><br>Neutralizes toxins → {{c1::antibodies}}<br><br>Maintains fluid balance → {{c1::plasma proteins}}",
                   "Back Extra": "Distinguish: plasma is the fluid; the cells ride in it.", "chapter": 6}],
    },
    {
        "id": "r25_good_lead_in_colon_is_not_a_per_item_cue",
        "warn": "card-rules #23", "present": True, "scope": "hard",
        "cards": [{"Text": "The <b>digestive system</b> is composed of 10 structures: {{c1::the gastrointestinal tract}}, {{c1::mouth}}, {{c1::salivary glands}}, {{c1::esophagus}}, {{c1::stomach}}, {{c1::liver}}, {{c1::gallbladder}}, {{c1::pancreas}}, {{c1::small intestine}}, and {{c1::large intestine}}.",
                   "Back Extra": "Pathway: mouth to anus, with accessory organs feeding in.", "chapter": 6}],
        "note": "the card's own colon lead-in must NOT be read as a label for the first inline item",
    },
    {
        "id": "r25_good_chunk_note_may_state_the_full_sets_count",
        "warn": "may be missing", "present": False,
        "cards": [{"Text": "<b>Phase 3 of 3</b> of an EMT's radio patient report is <b>care and close</b>, the last of its 10 elements, in order:<br><br>8. {{c1::a brief summary of the care you gave}}<br><br>9. {{c1::the patient's response to that care}}<br><br>10. {{c1::any additional questions or orders the hospital has}}",
                   "Back Extra": "Distinguish: element 8 is what you <i>did</i>, element 9 is what it <i>changed</i>.<br><br>Roster: 1 unit identification and level of service, 2 any special alert, 3 receiving hospital and ETA, 4 patient age and sex, 5 chief complaint and its severity, 6 brief history of the current problem, 7 brief report of physical findings, 8 <b>summary of the care given</b>, 9 <b>the patient's response to that care</b>, 10 <b>any additional questions or orders</b>.",
                   "chapter": 4}],
        "note": "rules 14 and 23 must not fight: a chunk note states the FULL set's count "
                "while clozing only its own members, and its Roster: line proves it is a chunk. "
                "Without this the drafter is pushed into checker-shaped phrasing to dodge the regex.",
    },
    {
        "id": "r7_bad_undercount_still_caught_without_a_roster",
        "warn": "may be missing", "present": True,
        "cards": [{"Text": "When determining decision-making capacity, consider 8 factors:<br><br>{{c1::Impaired intellect}}<br><br>{{c1::Legal age}}<br><br>{{c1::Intoxication}}<br><br>{{c1::Significant pain}}",
                   "Back Extra": "Why: capacity is the foundation of consent.", "chapter": 3}],
        "note": "the Roster exemption must not blanket-disable R7 — a genuine undercount with "
                "no Roster line still flags",
    },
    {
        "id": "r26_bad_list_split_across_sibling_numbers",
        "warn": "card-rules #24", "present": True, "scope": "hard",
        "cards": [{"Text": "An EMT's <b>radio patient report</b> opens with, in order:<br><br>1. {{c1::Unit ID and service level}}<br><br>2. {{c2::Any special alert}}<br><br>3. {{c3::Receiving hospital and ETA}}<br><br>4. {{c4::Patient's age and sex}}<br><br>5. {{c5::Chief complaint and severity}}",
                   "Back Extra": "Cue: who we are, what alert, where we're headed.", "chapter": 4}],
        "note": "the naive 'fix' for R25 — 5 cards each revealing the other 4 answers",
    },
    {
        "id": "r26_good_two_way_definition_is_not_a_split_list",
        "warn": "card-rules #24", "present": False,
        "cards": [{"Text": "{{c1::Hypoxia::condition}} is {{c2::inadequate oxygen at the cellular level}}.",
                   "Back Extra": "Distinguish: hypoxemia is low oxygen in the blood.", "chapter": 6}],
    },
    {
        "id": "r26_good_multi_fact_card_with_three_numbers",
        "warn": "card-rules #24", "present": False,
        "cards": [{"Text": "{{c1::Public health}} examines the needs of {{c2::entire populations}}, with the goal of {{c3::preventing health problems}}.",
                   "Back Extra": "Distinguish: clinical medicine treats the individual patient.", "chapter": 1}],
        "note": "three numbers marking three distinct facts — not an enumerated list",
    },

    # --- R28: quantitative keyed panels (Parker 2026-08-03, the pulse-rate-by-age card) ---
    {
        "id": "r28_bad_vitals_by_age_is_a_value_column",
        "warn": "card-rules #25", "present": True, "scope": "hard",
        "cards": [{"Text": "Normal <b>pulse rate</b> in beats/min, by age group:<br><br>Neonate — {{c1::100 to 180}}<br><br>Infant — {{c1::100 to 160}}<br><br>Toddler — {{c1::90 to 150}}<br><br>Preschool age — {{c1::80 to 140}}<br><br>School age — {{c1::70 to 120}}<br><br>Adolescent through older adult — {{c1::60 to 100}}",
                   "Back Extra": "Cue: the lower bound walks down in clean tens.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "the card Parker named: all six hide together AND the column interpolates",
    },
    {
        "id": "r28_bad_milestones_are_a_consecutive_run",
        "warn": "card-rules #25", "present": True, "scope": "hard",
        "cards": [{"Text": "Match each infant characteristic to the age at which it typically appears:<br><br>Afraid of strangers → {{c1::7 months}}<br><br>Responds to \"no\" → {{c1::8 months}}<br><br>Pulls self up to stand → {{c1::9 months}}<br><br>Crawls efficiently → {{c1::10 months}}<br><br>Begins to walk → {{c1::11 months}}<br><br>Knows his or her name → {{c1::12 months}}",
                   "Back Extra": "Cue: the second half-year is a mobility ladder.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "a complete consecutive run of months is solvable by elimination",
    },
    {
        "id": "r28_good_one_note_per_key",
        "warn": "card-rules #25", "present": False,
        "cards": [{"Text": "What is the normal <b>pulse rate</b> for a <b>toddler</b>, in beats/min? {{c1::90 to 150::range}}",
                   "Back Extra": "Distinguish: a toddler's floor of 90 is still above an adult's ceiling of 100 only barely — age decides what counts as fast.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "the fix: one value, one note, table on the back",
    },
    {
        "id": "r28_good_word_answers_cannot_interpolate",
        "warn": "card-rules #25", "present": False,
        "cards": [{"Text": "Match each function of the blood to the component that carries it out:<br><br>Fights infection → {{c1::white blood cells}}<br><br>Transports oxygen → {{c1::red blood cells}}<br><br>Forms clots → {{c1::platelets}}<br><br>Carries the cells and nutrients → {{c1::plasma}}<br><br>Neutralizes toxins → {{c1::antibodies}}",
                   "Back Extra": "Distinguish: plasma is the fluid; the cells ride in it.", "chapter": 6}],
        "note": "a word-answer match card is judged on LOAD (rule 23), not as a value column",
    },
    {
        "id": "r28_good_three_independent_values_only_warn",
        "warn": "card-rules #25", "present": False, "scope": "hard",
        "cards": [{"Text": "The adult <b>heart rate</b> depends on the situation:<br><br>at rest, {{c1::60 to 100 beats/min}}<br><br>at rest in a well-conditioned athlete, {{c1::45 to 60 beats/min}}<br><br>during vigorous physical activity, {{c1::as fast as 180 beats/min}}",
                   "Back Extra": "Why: a trained heart moves more blood per beat, so it needs fewer beats.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "3 rows is the warn band, never a block — the situations do not interpolate",
    },
    {
        "id": "r28_good_a_lone_numeric_row_is_not_a_panel",
        "warn": "card-rules #25", "present": False,
        "cards": [{"Text": "In <b>compensated shock</b>:<br><br>Heart rate: {{c1::increased::increased/decreased/normal}}<br><br>Systolic BP: {{c1::normal::increased/decreased/normal}}<br><br>Skin: {{c1::pale, cool, clammy}}<br><br>Cap refill: {{c1::delayed (>2 s)::delayed or normal}}",
                   "Back Extra": "Pitfall: a normal BP does NOT rule out shock.", "chapter": 8}],
        "note": "a direction-of-change panel is mostly word answers — one numeric row must not "
                "turn it into a value column",
    },

    # --- R33: R13's visual exemption must be VERIFIED, not self-asserted ---
    {
        "id": "r33_bad_self_asserted_visual_evidence_does_not_exempt",
        "warn": "needs_visual", "present": True, "scope": "hard",
        "cards": [{"Text": "The answer is {{c1::zygomaticomaxillary buttress}}.",
                   "Back Extra": "Cue: a facial buttress.", "source": "emt", "segment": 9,
                   "from_idx": [0],
                   "visual_source": {"pages": ["1"], "figures": [],
                                     "note": "I read it off the rendered page"}}],
        "highlights": [{"page": "1", "highlight": "x", "context": "the quick brown fox",
                        "needs_visual": True}],
        "note": "visual_source is free text the drafter writes itself; asserting evidence "
                "must not switch off the only mechanical enforcement of Rule 1",
    },
    {
        "id": "r33_good_a_real_attached_plate_does_exempt",
        "warn": "needs_visual", "present": False, "scope": "hard",
        "cards": [{"Text": "The answer is {{c1::zygomaticomaxillary buttress}}.",
                   "Back Extra": "Cue: a facial buttress.", "source": "emt", "segment": 9,
                   "from_idx": [0],
                   "image": "/Users/parkerregner/.claude/skills/zotero-to-anki/work/emt/"
                            "figures/study/TABLE_7_1.jpg"}],
        "highlights": [{"page": "1", "highlight": "x", "context": "the quick brown fox",
                        "needs_visual": True}],
        "note": "a plate that actually exists on disk is real evidence and still exempts",
    },

    # --- R30: procedures are carded as decisions (evidence: 85,212 AnKing notes) ---
    {
        "id": "r30_bad_recites_steps_by_number",
        "warn": "card-rules #26", "present": True,
        "cards": [{"Text": "Perform the extremity lift with the following steps:<br><br>1. {{c1::Kneel behind the patient's head as your partner kneels at the feet}}<br><br>2. {{c1::Cross the patient's hands over the chest}}<br><br>3. {{c1::Grasp the wrists and pull the upper torso to sitting}}<br><br>4. {{c1::Your partner slips both hands under the knees}}",
                   "Back Extra": "Pitfall: never use it on a suspected spinal injury.", "chapter": 8}],
        "note": "every row cued only by its position — the shape 85k professional cards never use",
    },
    {
        "id": "r30_good_decision_table_rows_cued_by_condition",
        "warn": "card-rules #26", "present": False,
        "cards": [{"Text": "Choosing a move for a patient still in the vehicle:<br><br>Scene is unsafe or there is a fire → {{c1::rapid extrication}}<br><br>Patient cannot be assessed in place → {{c1::rapid extrication}}<br><br>Stable, no spinal concern → {{c1::an ordinary non-urgent move}}<br><br>Stable with suspected spinal injury → {{c1::a vest-type extrication device}}",
                   "Back Extra": "Why: rapid extrication takes under a minute where a vest device takes 6 to 8, and buys that time at the cost of some spinal protection.", "chapter": 8}],
        "note": "the AnKing decision-table shape: each row cued by its CONDITION, not its position",
    },
    {
        "id": "r30_good_decision_point_vignette",
        "warn": "card-rules #26", "present": False,
        "cards": [{"Text": "A patient is seated in a wrecked car that has begun to smoke, and you cannot assess him where he sits. What move do you use? {{c1::Rapid extrication}}",
                   "Back Extra": "Pitfall: the speed is bought at the cost of spinal protection, so it needs a reason this specific.", "chapter": 8}],
        "note": "the workhorse: discriminating state visible, one blank on the action",
    },
    {
        "id": "r30_good_short_ordered_protocol_is_licensed",
        "warn": "card-rules #26", "present": True,
        "cards": [{"Text": "<b>Giving</b> a handover report follows a five-point method, in order:<br><br>1. {{c1::Initiate eye contact}}<br><br>2. {{c1::Manage the environment}}<br><br>3. {{c1::Ensure the ABCs}}<br><br>4. {{c1::Provide a structured report}}<br><br>5. {{c1::Provide documentation}}",
                   "Back Extra": "Why: eye contact marks that the handover is beginning.", "chapter": 4}],
        "note": "DELIBERATELY still flagged — Parker likes this card and rule 26 licenses a short "
                "ordered protocol, but the detector cannot tell it from a recitation, so it warns "
                "and the judge clears it. Asserted so the warn-not-block contract stays explicit.",
    },
    {
        "id": "r30_good_prose_card_is_untouched",
        "warn": "card-rules #26", "present": False,
        "cards": [{"Text": "The <b>rapid extrication technique</b> moves a seated patient onto a backboard in {{c1::1 minute or less}}, where proper placement of a vest-type device takes {{c1::6 to 8 minutes}}.",
                   "Back Extra": "Pitfall: the speed costs spinal protection, so it needs a specific indication.",
                   "chapter": 8, "needs_human_check": True}],
    },

    # --- R34: a bare count in a slot that never says it wants a count (Parker 2026-08-03) ---
    {
        "id": "r34_bad_bare_count_before_the_noun_it_counts",
        "warn": "card-rules #27", "present": True,
        "cards": [{"Text": "The {{c2::carpals}} are the {{c1::eight}} bones that form the wrist, and the {{c2::metacarpals}} are the {{c1::five}} bones that form the palm of the hand.",
                   "Back Extra": "Cue: wrist to fingertip runs carpals, then metacarpals, then phalanges.", "chapter": 6}],
        "note": "Parker's card. 'the ___ bones that form the wrist' takes short/long/carpal as "
                "readily as eight, and BOTH numbers are under c1 so neither cues the other.",
    },
    {
        "id": "r34_good_the_slot_label_hint_he_asked_for",
        "warn": "card-rules #27", "present": False,
        "cards": [{"Text": "The {{c2::carpals}} are the {{c1::eight::number of bones}} bones that form the wrist, and the {{c2::metacarpals}} are the {{c1::five::number of bones}} bones that form the palm of the hand.",
                   "Back Extra": "Cue: wrist to fingertip runs carpals, then metacarpals, then phalanges.", "chapter": 6}],
        "note": "the fix, in his own words: 'a good hint here would be something like "
                "{{c1::five::number of bones}}'",
    },
    {
        "id": "r34_good_a_unit_after_the_blank_labels_the_slot",
        "warn": "card-rules #27", "present": False,
        "cards": [{"Text": "The normal <b>pulse rate</b> for a <b>toddler</b> is {{c1::90 to 150}} beats/min.",
                   "Back Extra": "Pitfall: a toddler's rate overlaps an infant's at the top of the range.",
                   "chapter": 7, "needs_human_check": True}],
        "note": "nothing but a number fits before 'beats/min' — the slot is already labelled",
    },
    {
        "id": "r34_good_a_content_word_before_the_blank_labels_it",
        "warn": "card-rules #27", "present": False,
        "cards": [{"Text": "Type {{c1::1}} diabetes mellitus is characterized by {{c2::insulin deficiency}}.",
                   "Back Extra": "Distinguish: type 2 is insulin resistance, not deficiency.", "chapter": 6}],
        "note": "an IDENTIFIER, not a count — 'Type' has already named what kind of number this is. "
                "This is the class that made a first, looser draft fire 1,454 times across the "
                "collection instead of 4 times in the deck this pipeline owns.",
    },
    {
        "id": "r34_good_a_visible_parallel_number_shows_the_pattern",
        "warn": "card-rules #27", "present": False,
        "cards": [{"Text": "The right lung has {{c1::three}} lobes, while the left lung has {{c2::two}} lobes.",
                   "Back Extra": "Mnemonic: only the right lung has a middle lobe.", "chapter": 6}],
        "note": "c1 blanked still shows 'two', so the slot announces itself. The SAME card with "
                "both counts under c1 announces nothing on either card, and does flag.",
    },
    {
        "id": "r34_good_the_stem_asks_in_words",
        "warn": "card-rules #27", "present": False,
        "cards": [{"Text": "How many bones form the wrist? {{c1::Eight}}, together called the carpals.",
                   "Back Extra": "Cue: wrist to fingertip runs carpals, then metacarpals, then phalanges.", "chapter": 6}],
        "note": "'How many' is the announcement; a hint would be redundant",
    },

    # --- R11: first-letter hints (Parker 2026-07-19, the ::r/::k/::s rant) ---
    {
        "id": "r11_bad_letters_original",
        "warn": "first-letter", "present": True,
        "cards": [{"Text": "Medical errors are examined as coming from three possible sources (alone or combined):<br>{{c1::rules-based failure::r}}<br>{{c1::knowledge-based failure::k}}<br>{{c1::skills-based failure::s}}",
                   "Back Extra": "Cue: authority, information, execution.", "chapter": 1}],
    },
    {
        "id": "r11_bad_unrelated_acronym_no_license",
        "warn": "first-letter", "present": True,
        "cards": [{"Text": "An EMT is liable for negligence only when four elements are all present: {{c1::duty::D}}, {{c1::breach of duty::B}}, {{c1::damages::D}}, and {{c1::causation::C}}.",
                   "Back Extra": "Pitfall: all four must be present at once.", "chapter": 3}],
        "note": "'EMT' in the stem licenses NOTHING — D/B/D/C does not spell into it",
    },
    {
        "id": "r11_good_sample_mnemonic",
        "warn": "first-letter", "present": False,
        "cards": [{"Text": "To take a <b>SAMPLE</b> history, gather: {{c1::Signs and symptoms::S}}<br>{{c1::Allergies::A}}<br>{{c1::Medications::M}}<br>{{c1::Pertinent past medical history::P}}<br>{{c1::Last oral intake::L}}<br>{{c1::Events leading up to the illness or injury::E}}",
                   "Back Extra": "Cue: the letters spell SAMPLE.", "chapter": 10}],
    },
    {
        "id": "r11_good_partial_mnemonic_run",
        "warn": "first-letter", "present": False,
        "cards": [{"Text": "The first three items of a <b>SAMPLE</b> history are {{c1::Signs and symptoms::S}}, {{c1::Allergies::A}}, and {{c1::Medications::M}}.",
                   "Back Extra": "Cue: S-A-M opens SAMPLE.", "chapter": 10}],
        "note": "a partial run of a spelled mnemonic is still licensed (substring)",
    },
    {
        "id": "r11_good_mnemonic_with_rx_gap",
        "warn": "first-letter", "present": False,
        "cards": [{"Text": "The 5 sections of a <b>CHART</b> narrative are:<br>{{c1::Chief complaint::C}}<br>{{c1::History and physical examination::H}}<br>{{c1::Assessment::A}}<br>{{c1::Treatment (Rx)::R}}<br>{{c1::Transport::T}}",
                   "Back Extra": "Why: the R comes from Rx.", "chapter": 4}],
        "note": "C-H-A-T skips CHART's R (an Rx-mapped item) — in-order subsequence still licenses",
    },
    {
        "id": "r11_bad_letter_hint_on_co_clozed_acronym",
        "warn": "first-letter", "present": True,
        "cards": [{"Text": "In the EMS-modified version of SBAR ({{c1::SBAT::acronym}}), the final component becomes {{c1::Treatment::T}} rather than recap/Rx.",
                   "Back Extra": "Meaning: T = Treatment.", "chapter": 4}],
        "note": "the acronym is HIDDEN on the same card, so ::T leaks its final letter — hidden answers never license",
    },
    # --- R10: all-blanks-at-once husk (the governmental-immunity rant) ---
    {
        "id": "r10_bad_husk_original",
        "warn": "husk", "present": True,
        "cards": [{"Text": "The lawsuit defense of {{c1::governmental immunity::defense}} generally applies only to EMS systems operated by {{c1::municipalities or other governmental entities::operator type}}.",
                   "Back Extra": "Pitfall: state laws vary.", "chapter": 3}],
    },
    {
        "id": "r10_good_renumbered",
        "warn": "husk", "present": False,
        "cards": [{"Text": "The lawsuit defense of {{c2::governmental immunity::defense}} generally applies only to EMS systems operated by {{c1::municipalities or other governmental entities::operator type}}.",
                   "Back Extra": "Pitfall: state laws vary.", "chapter": 3}],
    },
    {
        "id": "r10_good_coordinate_pair",
        "warn": "husk", "present": False,
        "cards": [{"Text": "{{c1::Therapeutic communication::approach}} uses both {{c2::verbal}} and {{c2::nonverbal}} techniques to encourage patients to {{c3::express how they are feeling}} and to achieve a {{c3::positive relationship}} with the patient.",
                   "Back Extra": "Ex: eye contact is a nonverbal channel.", "chapter": 4}],
    },
    {
        "id": "r10_good_counted_set",
        "warn": "husk", "present": False,
        "cards": [{"Text": "The Star of Life's six functions are {{c1::detection}}, {{c1::reporting}}, {{c1::response}}, {{c1::on-scene care}}, {{c1::care in transit}}, and {{c1::transfer to definitive care}}.",
                   "Back Extra": "Cue: the six points of the star.", "chapter": 1}],
    },
    # --- R10b: synonym-equation husk (the off-line/online + Expressed-consent shape) ---
    {
        "id": "r10b_bad_equation_husk",
        "warn": "synonym/equation", "present": True,
        "cards": [{"Text": "{{c1::Expressed consent}}, also called {{c1::actual consent}}, must be obtained from every conscious, mentally competent adult before treatment.",
                   "Back Extra": "Distinguish: implied consent covers the unconscious patient.", "chapter": 3}],
    },
    {
        "id": "r10b_good_equation_renumbered",
        "warn": "synonym/equation", "present": False,
        "cards": [{"Text": "{{c1::Expressed consent}}, also called {{c2::actual consent}}, must be obtained from every conscious, mentally competent adult before treatment.",
                   "Back Extra": "Distinguish: implied consent covers the unconscious patient.", "chapter": 3}],
    },
    # --- R3: leak / crutch ---
    {
        "id": "r3_bad_parenthetical_after_cloze",
        "warn": "parenthetical", "present": True,
        "cards": [{"Text": "The EMS provider pathway runs in order: certification, then {{c1::licensure}} (state authority granted), then credentialing.",
                   "Back Extra": "Pathway: certify, license, credential.", "chapter": 1}],
    },
    {
        "id": "r3_good_two_way_definition",
        "warn": "leak", "present": False,
        "cards": [{"Text": "{{c1::Licensure}} is {{c2::the legal authority to practice}} granted by a state.",
                   "Back Extra": "Distinguish: certification attests skill; licensure grants the legal right.", "chapter": 1}],
    },
    # --- R7: list undercount (the 7-vs-8-factors bug) ---
    {
        "id": "r7_bad_undercount",
        "warn": "may be missing", "present": True,
        "cards": [{"Text": "Consider seven factors when evaluating decision-making capacity: {{c1::alertness}}, {{c1::orientation}}, {{c1::coherent speech}}, {{c1::judgment intact}}, {{c1::no intoxication}}.",
                   "Back Extra": "Pitfall: verify against the full source page.", "chapter": 3}],
    },
    {
        "id": "r7_good_overcount_branch",
        "warn": "may be missing", "present": False,
        "cards": [{"Text": "The general adaptation syndrome has three stages: {{c1::alarm}}, {{c1::reaction and resistance}}, and {{c1::recovery}} or {{c1::exhaustion}}.",
                   "Back Extra": "Cue: the third stage branches by outcome.", "chapter": 2}],
    },
    # --- R2: in-batch near-duplicate ---
    {
        "id": "r2_bad_duplicate_pair",
        "warn": "similar", "present": True,
        "cards": [{"Text": "{{c1::Licensure}} is the legal authority granted by a state to practice as an EMS provider.",
                   "Back Extra": "Distinguish: not certification.", "chapter": 1},
                  {"Text": "{{c1::Licensure}} is the legal authority granted by the state to practice as an EMS provider.",
                   "Back Extra": "Distinguish: not certification.", "chapter": 1}],
    },
    # --- R12: bloated single blank — a fuzzy scenario clause (R8) or a two-way-def c2
    #         side too long to recall verbatim (crisp-c2, card-recipes §4). Added
    #         2026-07-19 after the ch1-5 audit found ~30 two-way defs with 8-21-word c2. ---
    {
        "id": "r12_bad_bloated_c2",
        "warn": "in ONE blank", "present": True,
        "cards": [{"Text": "{{c1::Continuous quality improvement (CQI)}} is {{c2::a quality-management process in which team members continuously review responses to find and fix system weaknesses over time}}.",
                   "Back Extra": "Distinguish: not a one-time review.", "chapter": 1}],
    },
    {
        "id": "r12_good_crisp_c2",
        "warn": "in ONE blank", "present": False,
        "cards": [{"Text": "{{c1::Licensure::authority}} is {{c2::the legal authority to practice}}.",
                   "Back Extra": "Distinguish: certification attests skill; licensure grants the legal right.", "chapter": 1}],
    },
    {
        "id": "r12_good_grouped_list_long_items",
        "warn": "in ONE blank", "present": False,
        "cards": [{"Text": "Medical necessity for ambulance transport is established when the patient is {{c1::unconscious or in shock}}, {{c1::in acute respiratory or cardiac distress}}, or {{c1::bed-confined before and after the trip}}.",
                   "Back Extra": "Cue: transport must be the only safe option.", "chapter": 4}],
        "note": "long items under the SAME number are a grouped list, not a single fuzzy blank — must not flag",
    },

    # --- R13: grounding — the first mechanical enforcement of Rule 1 (2026-07-29) ---
    {
        "id": "r13_bad_caption_claim_no_evidence",
        "warn": "R13", "present": True, "scope": "hard",
        "highlights": json.loads('''[{"page": "548", "highlight": "TABLE 6-3 Muscles: Locations and Functions",
      "context": "There are more than 600 muscles in the musculoskeletal system. FIGURE 6-15 and TABLE 6-3 show the major muscles, their locations, and their functions.",
      "grounding": "EXACT", "content": "CAPTION_ONLY", "needs_visual": true}]'''),
        "cards": [{"Text": "On the anterior thorax the {{c1::pectoralis}} flexes and rotates the arm.",
                   "Back Extra": "Cue: it pulls the arm across the chest.",
                   "source": "emt", "segment": 6, "from_idx": [0]}],
        "note": "the mark is a TABLE caption flagged needs_visual; 'pectoralis' is in the table BODY, not the cited context, and no crop is attached",
    },
    {
        "id": "r13_good_caption_claim_with_visual_evidence",
        "warn": "R13", "present": False, "scope": "hard",
        "highlights": json.loads('''[{"page": "548", "highlight": "TABLE 6-3 Muscles: Locations and Functions",
      "context": "There are more than 600 muscles in the musculoskeletal system. FIGURE 6-15 and TABLE 6-3 show the major muscles, their locations, and their functions.",
      "grounding": "EXACT", "content": "CAPTION_ONLY", "needs_visual": true}]'''),
        "cards": [{"Text": "On the anterior thorax the {{c1::pectoralis}} flexes and rotates the arm.",
                   "Back Extra": "Cue: it pulls the arm across the chest.",
                   "source": "emt", "segment": 6, "from_idx": [0],
                   "visual_source": {"pages": ["549"],
                                     "figures": ["figures/study/TABLE_7_1.jpg"],
                                     "labels": ["TABLE 6-3"],
                                     "note": "read off the extracted plate"}}],
        "note": "same claim, but the crop proving it was read is REAL and resolves on disk -> "
                "legitimately grounded. The path must exist: R33 made this exemption a "
                "verified predicate, and this fixture previously named a file that never "
                "existed, which is precisely the self-assertion R33 closes.",
    },
    {
        "id": "r13_good_morphology_not_a_false_positive",
        "warn": "R13", "present": False, "scope": "hard",
        "highlights": json.loads('''[{"page": "527", "highlight": "In other joints, called symphyses, only slight motion is possible.",
      "context": "The fibrous tissues that connect bone to bone are called ligaments. In other joints, called symphyses, only slight motion is possible.",
      "grounding": "EXACT", "content": "FULL", "needs_visual": false}]'''),
        "cards": [{"Text": "A joint that permits only slight motion is a {{c1::symphysis}}.",
                   "Back Extra": "Ex: the pubic symphysis joins the left and right pubic bones.",
                   "source": "emt", "segment": 6, "from_idx": [0]}],
        "note": "source says 'symphyses', card answers 'symphysis' — naive stemming called this ungrounded",
    },
    {
        "id": "r13_good_legacy_batch_not_blocked",
        "warn": "R13", "present": False, "scope": "hard",
        "highlights": json.loads('''[{"page": "527", "highlight": "In other joints, called symphyses, only slight motion is possible.",
      "context": "The fibrous tissues that connect bone to bone are called ligaments. In other joints, called symphyses, only slight motion is possible.",
      "grounding": "EXACT", "content": "FULL", "needs_visual": false}]'''),
        "cards": [{"Text": "A joint that permits only slight motion is a {{c1::symphysis}}.",
                   "Back Extra": "Ex: the pubic symphysis.", "source": "emt", "segment": 6}],
        "note": "no from_idx anywhere = a pre-provenance batch; warn, never block",
    },

    # --- R14: list layout — the count of answers must be visible (Parker 2026-07-30) ---
    {
        "id": "r14_bad_packed_sbar_list",
        "warn": "LIST of things to produce", "present": True,
        "cards": [{"Text": "The structured handover format <b>SBAR</b> stands for:<br>{{c1::Situation::S}}<br>{{c1::Background::B}}<br>{{c1::Assessment::A}}<br>{{c1::Recap/Rx::R}}",
                   "Back Extra": "Meaning: S = a concise statement of the problem.", "chapter": 4}],
        "note": "the exact card Parker screenshotted; four blanks packed into one grey block",
    },
    {
        "id": "r14_good_spaced_sbar_list",
        "warn": "LIST of things to produce", "present": False,
        "cards": [{"Text": "The structured handover format <b>SBAR</b> stands for:<br><br>{{c1::Situation::S}}<br><br>{{c1::Background::B}}<br><br>{{c1::Assessment::A}}<br><br>{{c1::Recap/Rx::R}}",
                   "Back Extra": "Meaning: S = a concise statement of the problem.", "chapter": 4}],
    },
    {
        "id": "r14_good_numbered_rows_spaced",
        "warn": "LIST of things to produce", "present": False,
        "cards": [{"Text": "The six EMS functions on the <b>Star of Life</b>, in order:<br><br>1. {{c1::Detection}}<br><br>2. {{c1::Reporting}}<br><br>3. {{c1::Response}}",
                   "Back Extra": "Mnemonic: the six bars run in call order.", "chapter": 1}],
        "note": "ordinals are layout, not prose — a numbered list is still a list",
    },
    {
        "id": "r14_good_prose_is_not_a_list",
        "warn": "LIST of things to produce", "present": False,
        "cards": [{"Text": "At a vehicle crash, the first risk to consider is {{c1::traffic::hazard}}.<br>Ideally, park the ambulance so you can easily {{c2::leave::action}} the scene without reversing.",
                   "Back Extra": "Why: reversing on a live roadway is the highest-risk manoeuvre.", "chapter": 2}],
        "note": "two flowing sentences separated by <br> — must stay untouched",
    },
    # --- R14 (2026-07-30 hole): one long row must not veto the whole list ---
    {
        "id": "r14_bad_one_long_row_does_not_veto",
        "warn": "LIST of things to produce", "present": True,
        "cards": [{"Text": "Before a tough ethical call, an EMT can run the six-question checklist:<br>Would you agree if you were the {{c1::patient}}?<br>Is it in the patient's {{c1::best interest}}?<br>Is it based on {{c1::logic and reason}} rather than emotion?<br>Would you make the same decision {{c1::again}} in similar circumstances?<br>Can you {{c1::defend}} the decision to others?",
                   "Back Extra": "Mnemonic: ETHICS.", "chapter": 3}],
        "note": "row 4 carries 9 residual words; the old all()-veto let it silence the whole card",
    },
    {
        "id": "r14_bad_mixed_spacing_is_still_packed",
        "warn": "LIST of things to produce", "present": True,
        "cards": [{"Text": "The upper airway ends at the {{c2::larynx}}:<br><br>{{c1::Nasopharynx}} — above the soft palate<br>{{c1::Oropharynx}} — down to the hyoid bone<br>{{c1::Laryngopharynx}} — the lowest section",
                   "Back Extra": "Cue: nose, mouth, voice box.", "chapter": 6}],
        "note": "one spaced gap + two packed ones — the old 'contains <br><br>' test called this fine",
    },
    {
        "id": "r14_good_colon_lead_in_with_one_row_only",
        "warn": "LIST of things to produce", "present": False,
        "cards": [{"Text": "The EMT's first duty at any scene is simple:<br>confirm the scene is {{c1::safe}} before you approach.",
                   "Back Extra": "Why: a second patient helps no one.", "chapter": 2}],
        "note": "a colon lead-in heading ONE line is not a list — signal 1 needs >=2 rows",
    },
    # --- R15: a row label that restates its own answer (Parker 2026-07-30, radio card) ---
    {
        "id": "r15_bad_label_restates_answer",
        "warn": "row label", "present": True,
        "cards": [{"Text": "Across the phases of an EMS call, a unit radios <b>dispatch</b> to:<br><br>Arrival at hospital or point of transfer → {{c1::notify dispatch of arrival}}<br><br>En route → request {{c1::assistance with directions}}",
                   "Back Extra": "Why: keep the channel clear.", "chapter": 4}],
        "note": "the label IS the answer — 'you're giving away the answer while trying to give me a hint'",
    },
    {
        "id": "r15_good_match_row_label_is_a_real_cue",
        "warn": "row label", "present": False,
        "cards": [{"Text": "Name the negligence element each description matches:<br><br>An obligation to provide care per the standard set by training = {{c1::duty}}<br><br>Noticeable physical or psychological harm to the patient = {{c1::damages}}",
                   "Back Extra": "Pitfall: all four elements must be present at once.", "chapter": 3}],
        "note": "a classify row's description legitimately CUES the answer without restating it",
    },
    {
        "id": "r15_good_two_way_definition_has_no_row_label",
        "warn": "row label", "present": False,
        "cards": [{"Text": "{{c1::Licensure::term}} is {{c2::the legal authority to practice}}.",
                   "Back Extra": "Distinguish: certification attests to training.", "chapter": 1}],
    },
    # --- R16: absolute statement + lone unhinted blank (Parker 2026-07-30, 'old age') ---
    {
        "id": "r16_bad_absolute_open_blank",
        "warn": "absolute/prohibition", "present": True,
        "cards": [{"Text": "You must <b>never</b> attribute a patient's altered mental status to {{c1::old age}}.",
                   "Back Extra": "Why: altered mental status has treatable causes that must be found.", "chapter": 4}],
        "note": "'sad', 'skin color', 'being tired' all fit the blank — nothing visible forces old age",
    },
    {
        "id": "r16_good_contrast_tail_forces_the_answer",
        "warn": "absolute/prohibition", "present": False,
        "cards": [{"Text": "In medical directional terms, 'right' and 'left' always refer to the {{c1::patient's}} perspective, not the provider's.",
                   "Back Extra": "Pitfall: the patient's right is on your left.", "chapter": 5}],
        "note": "'not the provider's' names the rejected alternative — the blank is forced, not open",
    },
    {
        "id": "r16_good_slot_label_hint_constrains_it",
        "warn": "absolute/prohibition", "present": False,
        "cards": [{"Text": "You must <b>never</b> attribute a patient's altered mental status to {{c1::old age::a patient characteristic}}.",
                   "Back Extra": "Why: altered mental status has treatable causes that must be found.", "chapter": 4}],
        "note": "the fix Parker asked for himself — a hint that labels the slot without leaking it",
    },
    {
        "id": "r16_good_absolute_only_inside_quoted_speech",
        "warn": "absolute/prohibition", "present": False,
        "cards": [{"Text": "A patient says, \"I am afraid I will never see my kids again,\" and the EMT replies, \"You are afraid you will not see your kids again.\" Which therapeutic communication technique is the EMT using? {{c1::Reflection}}",
                   "Back Extra": "Cue: the EMT hands the patient's own statement back nearly word for word.", "chapter": 4}],
        "note": "the 'never' is dialogue in a vignette, not a rule — and 'which technique?' forces one answer",
    },
    {
        "id": "r16_good_sibling_cloze_anchors_it",
        "warn": "absolute/prohibition", "present": False,
        "cards": [{"Text": "In an older patient with altered mental status, always assume {{c1::an underlying treatable cause}} — never {{c2::normal aging}}.",
                   "Back Extra": "Pitfall: dismissing new confusion as aging misses a reversible problem.", "chapter": 4}],
    },
    # --- R17: an announced list whose items are visible, with a filler word clozed ---
    {
        "id": "r17_bad_visible_frames_fragment_clozed",
        "warn": "rows of this list are VISIBLE", "present": True,
        "cards": [{"Text": "Before you transfer care or leave a patient, run <b>8</b> self-check questions:<br><br>What {{c1::problems}} may develop from your actions?<br><br>How might the patient's condition {{c1::worsen}} if you leave?<br><br>Does the patient {{c1::need care}}?<br><br>Are you neglecting your {{c1::duty}}?<br><br>Is the person assuming care {{c1::capable}}?<br><br>Are you {{c1::abandoning}} the patient?<br><br>Are you violating a {{c1::standard of care}}?<br><br>Are you acting {{c1::prudently}}?",
                   "Back Extra": "Why: each question tests whether leaving would breach your duty.", "chapter": 3}],
        "note": "all 8 questions visible; one obvious word punched out of each — recognition, not recall",
    },
    {
        "id": "r17_good_mnemonic_rows_are_the_answers",
        "warn": "rows of this list are VISIBLE", "present": False,
        "cards": [{"Text": "To take a <b>SAMPLE</b> history, gather:<br><br>{{c1::Signs and symptoms::S}}<br><br>{{c1::Allergies::A}}<br><br>{{c1::Medications::M}}<br><br>{{c1::Pertinent past medical history::P}}",
                   "Back Extra": "Cue: the letters spell SAMPLE.", "chapter": 10}],
        "note": "each row LEADS with its cloze — the item itself is the answer",
    },
    {
        "id": "r17_good_classify_card_visible_side_is_the_cue",
        "warn": "rows of this list are VISIBLE", "present": False,
        "cards": [{"Text": "In a <b>SOAP</b> narrative, classify where each item is documented:<br><br>The patient describes his pain as sharp and burning = {{c1::Subjective::S/O/A/P}}<br><br>The respiratory rate you counted during your exam = {{c1::Objective::S/O/A/P}}<br><br>Your impression that he is having an allergic reaction = {{c1::Assessment::S/O/A/P}}",
                   "Back Extra": "Pitfall: your impression is Assessment, not Objective.", "chapter": 4}],
        "note": "a classify lead-in — the visible description IS the intended cue",
    },
    {
        "id": "r17_good_item_and_descriptor_rows",
        "warn": "rows of this list are VISIBLE", "present": False,
        "cards": [{"Text": "The upper airway runs, in descending order:<br><br>{{c1::Nasopharynx}} — above the soft palate<br><br>{{c1::Oropharynx}} — from the soft palate to the hyoid bone<br><br>{{c1::Laryngopharynx}} — where food and air part ways",
                   "Back Extra": "Cue: nose, mouth, then the split.", "chapter": 6}],
        "note": "item-then-descriptor rows: the structure names ARE the recall target",
    },
    # --- R24: values the numeric safety flag used to walk straight past (ch7, 2026-07-31) ---
    {
        "id": "r24_bad_percentage_escapes_numeric_flag",
        "warn": "looks numeric", "present": True,
        "cards": [{"Text": "At birth the head accounts for about {{c1::25%}} of a neonate's total body weight.",
                   "Back Extra": "Why: the head leads in a fall, so neonates land headfirst.", "chapter": 7}],
        "note": "'%' is not a word char, so the old trailing \\b made the percentage branch dead",
    },
    {
        "id": "r24_bad_age_in_months_escapes_numeric_flag",
        "warn": "looks numeric", "present": True,
        "cards": [{"Text": "The average age at which toddlers complete toilet training is {{c1::28 months}}.",
                   "Back Extra": "Distinguish: bladder control is possible far earlier, at 12 to 15 months.", "chapter": 7}],
        "note": "this book states developmental facts as ages in months/years, not as ranges",
    },
    {
        "id": "r24_bad_rate_with_inline_noun_escapes_numeric_flag",
        "warn": "looks numeric", "present": True,
        "cards": [{"Text": "A resting pulse of {{c1::140 beats/min}} is a normal finding in an infant.",
                   "Back Extra": "Pitfall: the same rate in an adult is far above the 60 to 100 range.", "chapter": 7}],
        "note": "'140 beats/min' — the counted noun sits between the digits and '/min'",
    },
    {
        "id": "r24_good_list_ordinal_is_not_a_value",
        "warn": "looks numeric", "present": False,
        "cards": [{"Text": "The stages of grief begin with {{c1::denial}} and end with {{c1::acceptance}}.",
                   "Back Extra": "Cue: the order is not fixed; people move back and forth.", "chapter": 7}],
        "note": "no digit at all — widening VALUE must not start flagging ordinary prose",
    },
    {
        "id": "r24_good_verified_card_is_exempt",
        "warn": "looks numeric", "present": False,
        "cards": [{"Text": "Normal <b>pulse rate</b> in beats/min, by age group:<br><br>Neonate — {{c1::100 to 180}}<br><br>Infant — {{c1::100 to 160}}",
                   "Back Extra": "Cue: the lower bound walks down in tens.", "chapter": 7,
                   "verified_against": "TABLE 7-1 (p683-684)",
                   "verified_by": "rendered plate figures/TABLE_7_1.png"}],
        "note": "a card that RECORDS what it was checked against is exempt — the same "
                "exemption verify_report.py derives, so the two scripts cannot disagree",
    },
]


def run_case(case, tmpdir):
    path = os.path.join(tmpdir, case["id"] + ".json")
    with open(path, "w") as f:
        json.dump(case["cards"], f)
    cmd = [sys.executable, CHECKER, path]
    # R13 needs the extractor output the cards claim to come from, so a case may ship
    # its own highlights fixture.
    if case.get("highlights") is not None:
        hp = os.path.join(tmpdir, case["id"] + "_highlights.json")
        with open(hp, "w") as f:
            json.dump(case["highlights"], f)
        cmd += ["--highlights", hp]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    # scope="hard" asserts only on BLOCKING errors, so a case can require "this must not
    # be blocked" while still allowing an advisory warning (the paraphrase contract).
    scope = out
    if case.get("scope") == "hard":
        scope = "\n".join(l for l in out.splitlines() if l.strip().startswith("x "))
    hit = case["warn"].lower() in scope.lower()
    return hit == case["present"], hit, out


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for case in CASES:
            ok, hit, out = run_case(case, tmpdir)
            want = "must flag" if case["present"] else "must NOT flag"
            print(f"{'PASS' if ok else 'FAIL'}  {case['id']}  ({want} '{case['warn']}'; flagged={hit})")
            if not ok:
                failures.append((case["id"], out))
    print(f"\n{len(CASES) - len(failures)}/{len(CASES)} regression cases pass")
    for cid, out in failures:
        print(f"\n--- checker output for FAILED {cid} ---\n{out}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()