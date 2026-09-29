#!/usr/bin/env python3
"""
apply_review.py — draft (cards_src.NOTES) + independent reviews -> cards_reviewed.json.

Order of authority, most specific wins:
  1. review_craft.json   the adversarial editor's per-card verdicts (fixed Text / Back Extra
                         / image). It already folds in the confirmed items of the anatomy
                         fact-check (review_facts.json card_facts), so applying it cannot
                         bring a corrected error back.
  2. OVERRIDES below     this session's decisions on the reviewers' open questions and the
                         fact-checker's picture suggestions.
  3. NEW                 cards added to close the coverage gaps both reviews found.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cards_src as C  # noqa: E402

W = os.path.dirname(HERE)
FIGDIR = os.path.join(W, "figures")

DROP = {82, 95}          # 82: lettered photo + duplicate of #84's skill; 95: folded into #96

# idx -> field overrides (applied AFTER the craft review)
OVERRIDES = {
    12: dict(img="s11_facial_bones.png"),          # show the bones the card names
    27: dict(img="s06_epiphyseal_plate.jpg"),
    28: dict(img="m6_09_growth_plate.jpg"),        # labels show which side is which
    49: dict(img="s13_hyoid.jpg"),                 # shows it hanging free in the neck
    # a front photo must never reappear on another card: the giraffe/moose plate holds
    # the very photos that #80/#81 ask about, so it moves onto THOSE cards' own backs
    78: dict(img="s16_thoracic.png"),
    79: dict(img="s17_lumbar_superior.jpg"),
    80: dict(back_img="m7_14_giraffe_row.jpg"),
    81: dict(back_img="m7_14_moose_row.jpg"),
    102: dict(img="s20_rib_groups.png"),           # the lab's own table, like #100/#101
}

NEW = [
    dict(deck=C.SKULL, img="s11_facial_bones.png",
         ver="slide 11 speaker notes ('Paired Bones: Nasal, Lacrimal, Zygomatic, Inferior Nasal Conchae, Maxillae, Palatine')",
         text="Three of the PAIRED facial bones sit between and beside the eye sockets:<br><br>"
              "{{c1::nasal bones}}<br><br>{{c1::lacrimal bones}}<br><br>{{c1::zygomatic bones}}",
         back="Why: each sits off the midline with a mirror twin on the other side, so each "
              "counts twice toward the 14 facial bones.<br><br>Roster: paired = <b>nasal</b>, "
              "<b>lacrimal</b>, <b>zygomatic</b>, maxillae, palatine, inferior nasal conchae · "
              "unpaired = mandible, vomer"),
    dict(deck=C.SKULL, img="s11_facial_bones.png",
         ver="slide 11 speaker notes ('Paired Bones: ... Maxillae, Palatine Bones', 'Inferior Nasal Conchae')",
         text="Three of the PAIRED facial bones build the upper jaw, the hard palate, and the "
              "side walls of the airway inside the nose:<br><br>{{c1::maxillae}}<br><br>"
              "{{c1::palatine bones}}<br><br>{{c1::inferior nasal conchae}}",
         back="Why: the right and left maxillae and palatine bones meet at the midline to "
              "build one hard palate, and each side of the airway gets its own concha.<br><br>"
              "Roster: paired = nasal, lacrimal, zygomatic, <b>maxillae</b>, <b>palatine</b>, "
              "<b>inferior nasal conchae</b> · unpaired = mandible, vomer"),
    dict(deck=C.SPINE, img="m7_08_spinal_curves.jpg",
         ver="slide 15 speaker notes ('You can palpate C7 at base of posterior neck'); blue page Q15 + palpation check-off",
         text="The bump you can feel at the base of the back of your neck is the spinous "
              "process of {{c1::C7::vertebra}}.",
         back="Why: C7's spinous process is longer than the ones above it and sticks out under "
              "the skin, which is why C7 is called the vertebra prominens."),
    dict(deck=C.SPINE, img="s15_cervical_labeled.png",
         ver="blue page Q13 ('What is the function of the transverse foramina?'); lab manual p.158 (says carotid — incorrect)",
         text="The transverse foramina carry the {{c1::vertebral arteries::which vessels}} "
              "toward the brain.",
         back="Why: the vertebral arteries climb through the stack of bony rings, which shields "
              "them from the neck's constant bending and turning.<br><br>Pitfall: the lab "
              "manual says the carotid arteries; the carotids run in front of the spine, not "
              "through it."),
    dict(deck=C.SPINE, img="m7_08_spinal_curves.jpg",
         ver="blue page Q14 ('What are the functions of the spinal curves?'); slide 14 curves",
         text="Two functions of the normal spinal curves are to {{c1::absorb shock::what they "
              "do to impact}} and to {{c2::keep the body balanced::what they do for posture}}.",
         back="Why: the thoracic and sacral curves are present at birth, and the cervical and "
              "lumbar curves form as a baby lifts its head and learns to walk; the resulting "
              "S-shape flexes like a spring with each step."),
]


def main():
    review = {v["idx"]: v for v in json.load(open(os.path.join(W, "review_craft.json")))["verdicts"]}
    out = []
    for i, n in enumerate(C.NOTES):
        if i in DROP:
            continue
        n = dict(n)
        v = review.get(i)
        if v and v["verdict"] == "REWRITE":
            if v.get("fixed_text"):
                n["text"] = v["fixed_text"]
            if v.get("fixed_back"):
                n["back"] = v["fixed_back"]
            if v.get("fixed_image"):
                n["img"] = os.path.basename(v["fixed_image"])
        o = OVERRIDES.get(i, {})
        if "img" in o:
            n["img"] = o["img"]
        if "back_img" in o:
            n["back_img"] = o["back_img"]
        n["draft_idx"] = i
        out.append(n)
    for n in NEW:
        n = dict(n)
        n["draft_idx"] = None
        out.append(n)
    for n in out:
        for key in ("img", "back_img"):
            if n.get(key) and not os.path.exists(os.path.join(FIGDIR, n[key])):
                sys.exit(f"missing figure {n[key]}")
    json.dump(out, open(os.path.join(W, "cards_reviewed.json"), "w"), indent=1,
              ensure_ascii=False)
    print(f"{len(C.NOTES)} drafted - {len(DROP)} dropped + {len(NEW)} new = {len(out)} notes")


if __name__ == "__main__":
    main()
