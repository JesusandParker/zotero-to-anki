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
CASES = [
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
                   "visual_source": {"page": 549, "figure": "figures/p549_table_6-3.png"}}],
        "note": "same claim, but the crop proving it was read is attached -> legitimately grounded",
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