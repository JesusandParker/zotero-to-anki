#!/usr/bin/env python3
"""
apply_review.py — draft (cards_src.NOTES) + three independent reviews -> cards_reviewed.json.

Reviews (all written by separate agents that never saw each other's output):
  review_facts_part1.json   anatomy fact-check, idx 0-88
  review_facts_part2.json   anatomy fact-check, idx 89-219 (+ the IO notes, applied in io_spec.py)
  review_craft.json         adversarial card-craft editor, every note

Order of authority, most specific wins:
  1. FACT fixes   every FIX/CHECK the fact-checkers wrote a fix for was read and accepted
                  (listed in FACT_REJECT otherwise), because a craft rewrite must never
                  bring a corrected error back
  2. CRAFT        the editor's REWRITE/DROP verdicts, except CRAFT_REJECT
  3. MERGED       this session's hand-merge where a fact fix and a craft rewrite touch the
                  same note (the fact content wins, the craft shape is kept)
  4. VER_FIX      corrected citations (recording timestamps)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cards_src as C  # noqa: E402

W = os.path.dirname(HERE)
FIGDIR = os.path.join(W, "figures")

FACT_REJECT = set()           # fact-check fixes NOT applied (none: all 30 were right)

# idx -> why the craft verdict was not applied
CRAFT_REJECT = {
    26: "kept; the mirrored picture becomes its own NEW card (each drawing both ways)",
    61: "kept; the mirrored picture becomes its own NEW card",
    84: "kept; the mirrored picture becomes its own NEW card",
}

# idx -> fields, hand-merged where a fact fix and a craft rewrite touch the same note (the
# fact content wins, the craft shape is kept), plus this session's own calls: the Popcorn
# pins now ask for the side too ("the practical wants e.g. 'olecranon process of the
# right'", craft open question), and the scapula/femur siding stems no longer announce the
# view, which is step 1 of the lab's own method (craft open question).
MERGED = {
    0: dict(text="The lab manual counts {{c1::130::number of bones}} appendicular bones out of its "
                 "210 total.",
            back="Why: the manual adds four sesamoid bones (two under each big toe) to the usual "
                 "count of 126 appendicular bones out of 206.<br><br>Pitfall: sources disagree on "
                 "the totals, and on the last home quiz the lab accepted all three bone totals."),
    3: dict(text="Not counting the hip bone or the small sesamoids under the big toe, each lower "
                 "limb has {{c1::30::number of bones}} bones.",
            back="Why: femur + patella + tibia + fibula + 7 tarsals + 5 metatarsals + 14 phalanges = "
                 "30; the patella is a sesamoid too, but every count includes it.<br><br>Pitfall: "
                 "the manual adds the two sesamoids under each big toe, giving 32 per limb (64 for "
                 "both)."),
    9: dict(text="A {{c1::foramen}} is a {{c2::hole::kind of bone marking}} in a bone that nerves "
                 "and blood vessels pass through.",
            back="Why: nerves and vessels have to cross bone to reach what they supply, so bones "
                 "have holes where they pass; the obturator foramen of the hip bone is the largest "
                 "in the body.<br><br>Pitfall: as a bone marking, a foramen is a hole through bone; "
                 "the instructor said openings in muscles are not called foramina."),
    22: dict(text="The clavicle's lateral end articulates with the scapula at the "
                  "{{c1::acromion::part of the scapula}}.",
             back="Why: the acromioclavicular (AC) joint at the top of the shoulder is the "
                  "clavicle's only joint with the scapula; a ligament also ties the clavicle down "
                  "to the coracoid process.<br><br>Cue: the lab also calls the acromion the "
                  "acromial process."),
    39: dict(text="A scapula with all labels removed: is it a right or a left scapula? "
                  "{{c1::right::side}}"),
    40: dict(text="Skeleton seen from the front: name the bone at pin 9, with its side. "
                  "{{c1::left clavicle::side + bone}}",
             back="Why: the clavicle is the S-shaped bone running from the top of the sternum out to the "
                  "shoulder, and seen from the front the skeleton's left side is on your right."),
    41: dict(text="Skeleton seen from behind: name the bone at pin 10, with its side. "
                  "{{c1::left scapula::side + bone}}",
             back="Why: the scapula is the flat, triangular bone over the upper back ribs, and seen from "
                  "behind the skeleton's left side is on your left."),
    60: dict(text="Of the humerus, the {{c1::distal::proximal or distal}} end is the part you can "
                  "easily feel through the skin.",
             back="Why: the proximal end sits inside the shoulder joint, buried under the deltoid "
                  "and rotator cuff, while at the elbow the two epicondyles lie just under the "
                  "skin.<br><br>Pitfall: the manual says ONLY the distal end can be felt; strictly, "
                  "the greater tubercle can also be felt by pressing deep through the deltoid."),
    62: dict(text="Skeleton seen from behind: name the bone at pin 11, with its side. "
                  "{{c1::left humerus::side + bone}}",
             back="Why: the humerus is the only bone of the arm, running from the shoulder to the elbow, "
                  "and seen from behind the skeleton's left side is on your left."),
    76: dict(text="The head of the ulna is at its {{c1::distal}} end, while the head of the radius "
                  "is at its {{c1::proximal}} end.",
             back="Why: each 'head' is the rounded end that fits into the other bone's notch: the "
                  "radius's at the elbow, the ulna's at the wrist.<br><br>Pitfall: the ulna's head "
                  "is its SMALL end; its big end is the olecranon at the elbow."),
    85: dict(text="Skeleton seen from the front: name the bone at pin 17, with its side. "
                  "{{c1::left ulna::side + bone}}",
             back="Why: at the elbow the ulna is the medial forearm bone, the one with the big "
                  "proximal end; seen from the front, the skeleton's left side is on your right."),
    86: dict(text="Skeleton seen from the front: name the bone at pin 18, with its side. "
                  "{{c1::left radius::side + bone}}",
             back="Why: the radius is the lateral (thumb-side) forearm bone, slim at the elbow and wide at "
                  "the wrist; seen from the front, the skeleton's left side is on your right."),
    91: dict(text="The thumb has {{c1::2::number of bones}} phalanges; each other finger has "
                  "{{c2::3::number of bones}}.",
             back="Why: the thumb has only a proximal and a distal phalanx (no middle one), so it "
                  "has one joint between its phalanges (IP), where each other finger has two (PIP "
                  "and DIP)."),
    95: dict(text="Proximal-row carpals, from the thumb side to the pinky side (So Long To "
                  "Pinky):<br><br>{{c1::scaphoid::So}}<br><br>{{c1::lunate::Long}}<br><br>"
                  "{{c1::triquetrum::To}}<br><br>{{c1::pisiform::Pinky}}",
             back="Why: the proximal row is the carpal row next to the forearm, where it "
                  "articulates with the radius (a cartilage disc keeps the ulna off it).<br><br>"
                  "Mnemonic: So Long To Pinky, Here Comes The Thumb."),
    98: dict(text="The {{c1::pisiform}} is the small carpal that sits on the palm side of the "
                  "wrist, on top of the triquetrum.",
             back="Why: pisiform means 'pea-shaped'; it lies inside a wrist flexor tendon, so it "
                  "rides on the front (palm side) of the triquetrum rather than lining up beside "
                  "the other proximal-row carpals.",
             img="s07_hand.png"),
    108: dict(back="Why: the arched metacarpals cup the palm around what you grip, so the hollow "
                   "side is always the palm.<br><br>Cue: hold a loose hand the way your own hangs "
                   "in anatomical position, fingers pointing down and cupped palm facing forward "
                   "(away from you); if its thumb points to your right, it is a right hand."),
    119: dict(back="Why: the sacrum is part of the vertebral column, wedged between the two hip "
                   "bones like a keystone.<br><br>Pitfall: the manual's definition differs from "
                   "the lab's bone list and most textbooks, which count only the two os coxae as "
                   "the pelvic girdle and call the ring they form with the sacrum and coccyx the "
                   "bony pelvis."),
    128: dict(text="The sciatic nerve leaves the pelvis for the lower limb through the "
                   "{{c1::greater::greater or lesser}} sciatic notch.",
              back="Why: the greater sciatic notch is the big gap between the ilium and the "
                   "ischial spine, roomy enough for the sciatic nerve and its vessels; the lesser "
                   "notch below the spine passes smaller nerves and vessels."),
    133: dict(text="The {{c1::inguinal ligament}} stretches from the ASIS to the pubis.",
              back="Why: the inguinal ligament is the rolled lower edge of an abdominal muscle's "
                   "sheet, tacked between two bony points, and it marks the crease of the groin."
                   "<br><br>Pitfall: the manual and the study guide say it ends at the pubic "
                   "crest; most anatomy texts say the pubic tubercle, just beside it."),
    140: dict(text="The lab manual says the gluteal region belongs anatomically to the "
                   "{{c1::trunk}} and physiologically to the {{c1::lower limb}}.",
              back="Why: the gluteal region lies over the pelvis, but its muscles (the glutes) "
                   "move the thigh.<br><br>Pitfall: most anatomy texts count the gluteal region "
                   "as a region of the lower limb, the transition between trunk and thigh."),
    142: dict(text="Skeleton seen from the front: name the bone at pin 19, with its side. "
                   "{{c1::left os coxae (ilium)::side + bone}}",
              back="Why: the pin sits on the broad upper wing of the hip bone, the ilium part of "
                   "the os coxae, on the skeleton's left (your right, seen from the front)."),
    152: dict(text="The femur's sharp ridge (the linea aspera) runs down its "
                   "{{c1::posterior::anterior or posterior}} side, but the tibia's sharp ridge runs "
                   "down its {{c1::anterior::anterior or posterior}} side.",
              back="Why: the femur's ridge runs down the back of the shaft and anchors thigh "
                   "muscles (chiefly the adductors), while the tibia's sharp front border is the "
                   "bare bone of the shin.<br><br>Pitfall: the two long bones are opposite, so a "
                   "sharp ridge tells you front from back only once you know which bone you "
                   "hold."),
    158: dict(text="A femur with all labels removed: is it a right or a left femur? "
                   "{{c1::left::side}}"),
    159: dict(text="Skeleton seen from the front: name the bone at pin 22, with its side. "
                   "{{c1::left femur::side + bone}}",
              back="Why: the femur is the thigh's single bone, running from the hip socket to the knee, "
                   "and seen from the front the skeleton's left side is on your right."),
    198: dict(text="Each foot has {{c1::5::number of bones}} metatarsals, numbered starting from "
                   "the {{c2::big toe::big toe or little toe}}.",
              back="Why: one metatarsal carries each toe, numbered I to V from the big toe (on the "
                   "medial side of the foot), just as the hand is numbered from the thumb; that "
                   "makes 10 in the body."),
    209: dict(text="Per the lab manual, the keystones of the transverse arch are the "
                   "{{c1::medial cuneiform}} and the base of the {{c1::2nd metatarsal}}.",
              back="Why: a keystone marks the top of an arch, and the manual's figure shades the "
                   "medial cuneiform and the wedged-in base of the 2nd metatarsal at the top of "
                   "the dome across the foot.<br><br>Pitfall: most anatomy texts name the "
                   "intermediate (middle) cuneiform, not the medial one, as the transverse arch's "
                   "keystone; the manual and study guide say medial cuneiform."),
}

# notes added after review
NEW = [
    # the craft editor split #33 (borders + angles shared two of three names) into two notes
    dict(deck=C.PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('three angles and three borders: The superior, lateral and inferior angles'); study guide p.1; slide 4 overlays ('superior angle', 'Inferior angle')",
         text="The scapula's three angles (corners) are the {{c1::superior}}, {{c1::inferior}}, "
              "and {{c1::lateral}} angles.",
         back="Why: the scapula is a flat triangle, so its corners are named for where they "
              "point; the lateral angle is the thick corner that carries the glenoid cavity."),
    # mirrored twins of the seven left/right pictures (a mirrored right bone IS a left bone)
    dict(deck=C.PECTORAL, side="front", img="lr_clavicle_superior_mirror.png",
         ver="slide 3 figure (b) 'Right clavicle, superior view' (labels erased), mirrored left-right = a left clavicle; orientation rules slide 3",
         text="A clavicle seen from above, with the front of the body toward the bottom of the "
              "picture: is it a right or a left clavicle? {{c1::left::side}}",
         back="Why: the thick, blunt end at the picture's left is the sternal end (medial), so "
              "the flattened acromial end points to the picture's right. Looking down from above "
              "with the front toward the bottom, the picture's right is the body's left.<br><br>"
              "Cue: sternal end medial, big curve bulging forward, conoid tubercle underneath."),
    dict(deck=C.PECTORAL, side="front", img="lr_scapula_posterior_mirror.jpg",
         ver="slide 4 figure, posterior view of a right scapula (labels erased), mirrored left-right = a left scapula",
         text="A scapula with all labels removed: is it a right or a left scapula? "
              "{{c1::left::side}}",
         back="Why: the spine shows, so you are looking at its back; the glenoid cavity always "
              "points laterally, and it is on the picture's left. Seen from behind, lateral on "
              "your left means the body's left side."),
    dict(deck=C.ARM, side="front", img="lr_humerus_anterior_mirror.png",
         ver="slide 5 figure (a) anterior view of a right humerus (labels erased), mirrored left-right = a left humerus",
         text="A humerus seen from the front (anterior view): is it a right or a left humerus? "
              "{{c1::left::side}}",
         back="Why: the head points medially, and here it points to the picture's left. Seen "
              "from the front, a bone whose medial side is on your left is from the body's left "
              "side.<br><br>Cue: the deltoid tuberosity (lateral) is on the picture's right."),
    dict(deck=C.ARM, side="front", img="lr_forearm_anterior_mirror.png",
         ver="slide 6 figure (a) anterior view of a right radius and ulna (labels erased), mirrored left-right = a left forearm",
         text="A radius and ulna seen from the front (anterior view): is this a right or a left "
              "forearm? {{c1::left::side}}",
         back="Why: the radius (round head at the elbow, wide end at the wrist) is on the "
              "picture's right, and the radius is lateral. Seen from the front, lateral on your "
              "right means the body's left side."),
    dict(deck=C.PELVIS, side="front", img="lr_hip_lateral_mirror.jpg",
         ver="lab manual Fig 8-7 'The Right Hip Bones', lateral view (labels erased), mirrored left-right = a left hip bone; lab recording 9/30 [46:13]-[47:50] (Dr. Blais's orientation recipe)",
         text="A hip bone seen from its outer (lateral) side: is it a right or a left os "
              "coxae? {{c1::left::side}}",
         back="Why: crest up, obturator foramen down, acetabulum facing you (lateral view). The "
              "sciatic notches mark the back and sit on the picture's right, so the front (ASIS) "
              "points to your left: that is a left hip bone seen from outside.<br><br>Cue: Dr. "
              "Blais's recipe: crest superior, obturator foramen inferior, acetabulum lateral, "
              "sciatic notches posterior."),
    dict(deck=C.LEG, side="front", img="lr_femur_posterior_mirror.jpg",
         ver="lab manual Fig 8-9 'Left Femur & Patella', posterior view (labels erased), mirrored left-right = a right femur",
         text="A femur with all labels removed: is it a right or a left femur? "
              "{{c1::right::side}}",
         back="Why: the head points medially, here toward the picture's left. The linea aspera "
              "and intercondylar fossa show this is the back, and seen from behind, a medial side "
              "on your left means the body's right side."),
    dict(deck=C.LEG, side="front", img="lr_tibia_fibula_mirror.png",
         ver="slide 13 figure, anterior view of a right tibia and fibula (labels erased), mirrored left-right = a left leg",
         text="A tibia and fibula seen from the front: is this a right or a left leg? "
              "{{c1::left::side}}",
         back="Why: the thin fibula is on the picture's right, and the fibula is lateral. Seen "
              "from the front, lateral on your right means the body's left leg.<br><br>Cue: the "
              "tibial tuberosity faces you (anterior), and the medial malleolus is on the tibia's "
              "side."),
    # Popcorn pins the first draft skipped (no instructor key; identified at 3x zoom)
    dict(deck=C.PELVIS, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 21 (no instructor key for appendicular pins; the inferolateral part of the hip bone below the obturator foramen)",
         text="Skeleton seen from the front: name the bone at pin 21, with its side. "
              "{{c1::right os coxae (ischium)::side + bone}}",
         back="Why: the pin sits below and lateral to the obturator foramen, on the ischium part "
              "of the hip bone, on the skeleton's right (your left, seen from the front)."),
    dict(deck=C.HAND, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 23 (no instructor key; the thumb is the digit with only three bones: metacarpal + 2 phalanges)",
         text="Skeleton seen from the front: name the bone at pin 23, with its side. "
              "{{c1::left first metacarpal (metacarpal I)::side + bone}}",
         back="Why: the digit standing apart from the curled fingers has only three bones, so it "
              "is the thumb, and pin 23 is the long bone springing from the wrist; seen from the "
              "front, the skeleton's left hand is on your right."),
    dict(deck=C.HAND, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 24 (no instructor key; thumb = metacarpal + proximal + distal phalanx)",
         text="Skeleton seen from the front: name the bone at pin 24, with its side. "
              "{{c1::left first proximal phalanx (of the thumb)::side + bone}}",
         back="Why: the thumb has no middle phalanx, so the segment after its metacarpal is the "
              "proximal phalanx; the hand is the skeleton's left (your right, seen from the "
              "front)."),
    dict(deck=C.HAND, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 25 (no instructor key; thumb tip)",
         text="Skeleton seen from the front: name the bone at pin 25, with its side. "
              "{{c1::left first distal phalanx (thumb tip)::side + bone}}",
         back="Why: the tip of the thumb is its distal phalanx, the last of its two phalanges; "
              "the hand is the skeleton's left (your right, seen from the front)."),
]
VER_FIX = {
    30: "slide 4 notes ('Be able to distinguish between acromial process and coracoid process'); "
        "lab recording 9/30 [16:05] ('this bigger one is called the acromial process'); lab manual Fig 8-2",
    65: "lab recording 9/30 [33:49]-[34:37] ('the ulna ... was the primary articulating bone of the "
        "humerus', 'the radius is the primary articulating bone for the wrist'); study guide p.1; "
        "lab manual p.171",
}


def load(name):
    p = os.path.join(W, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    notes = [dict(n) for n in C.NOTES]
    fact = {}
    for part in ("review_facts_part1.json", "review_facts_part2.json"):
        d = load(part)
        for f in (d or {}).get("card_facts", []):
            if f["idx"] in FACT_REJECT or not (f.get("fix_text") or f.get("fix_back")):
                continue
            fact[f["idx"]] = f
    craft = {v["idx"]: v for v in (load("review_craft.json") or {}).get("verdicts", [])}
    drop, log = set(), []
    for i, n in enumerate(notes):
        f, v = fact.get(i), craft.get(i)
        if i in MERGED:
            if v and v["verdict"] == "DROP":
                sys.exit(f"idx {i}: hand-merged but the editor dropped it — decide")
            n.update(MERGED[i]); log.append(f"{i}: hand-merged")
        else:
            if v and i not in CRAFT_REJECT:
                if v["verdict"] == "DROP":
                    drop.add(i); log.append(f"{i}: DROP ({v['why'][:60]})"); continue
                if f and (v.get("fixed_text") or v.get("fixed_back")):
                    sys.exit(f"idx {i}: fact fix AND craft rewrite — hand-merge it in MERGED")
                if v.get("fixed_text"):
                    n["text"] = v["fixed_text"]
                if v.get("fixed_back"):
                    n["back"] = v["fixed_back"]
                if v.get("fixed_image"):
                    n["img"] = os.path.basename(v["fixed_image"])
                log.append(f"{i}: craft")
            if f:
                if f.get("fix_text"):
                    n["text"] = f["fix_text"]
                if f.get("fix_back"):
                    n["back"] = f["fix_back"]
                log.append(f"{i}: fact")
        if i in VER_FIX:
            n["ver"] = VER_FIX[i]
        n["draft_idx"] = i
    out = [n for i, n in enumerate(notes) if i not in drop]
    for n in NEW:
        n = dict(n)
        n["draft_idx"] = None
        out.append(n)
    for n in out:
        if not os.path.exists(os.path.join(FIGDIR, n["img"])):
            sys.exit(f"missing figure {n['img']}")
    json.dump(out, open(os.path.join(W, "cards_reviewed.json"), "w"), indent=1,
              ensure_ascii=False)
    print(f"{len(C.NOTES)} drafted - {len(drop)} dropped + {len(NEW)} new = {len(out)} notes "
          f"({sum(1 for l in log if 'fact' in l)} fact fixes, "
          f"{sum(1 for l in log if 'craft' in l)} craft rewrites, {len(MERGED)} hand-merged)")


if __name__ == "__main__":
    main()
