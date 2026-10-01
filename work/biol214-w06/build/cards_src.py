"""
cards_src.py — every cloze note for BIOL 214 W06 (appendicular skeleton), one dict per note.

  deck  : subdeck under ...::Practical 2::Appendicular Skeleton
  text  : the Text field (cloze)
  back  : Back Extra (a 1-2 sentence Why first — Parker's explicit ask — then at most one
          more labeled line)
  img   : figure file under ../figures (attached to the BACK unless side="front")
  side  : "front" only when the picture IS the question (which bone / which side is this)
  ver   : where the fact was read (slide / speaker notes / lab recording timestamp / study
          guide / lab manual PRINTED page / blue page / Popcorn render)
  num   : True when the answer is a number/range (routes to needs_human_check)
  tags  : extra tags ("optional" = the lab says it is not required)

Parker's scope (2026-09-30): "the maximal set ... exactly what you did before ... you do have
the additional recording from lab" — so every fact on the W06 slides + speaker notes, in the
9/30 lab recording, in the Ch 8 study guide (Canvas, posted during lab 9/30), in lab manual
Ch 8 (printed pp. 169-182) and its blue pages (185-188), plus the Popcorn Points pins.
Source tags (src::slides, src::recording, ...) are derived from `ver` by make_cards.py so the
deck can be trimmed to one source later (the W05 quiz trim needed exactly that).
The IO plates live in io_spec.py.
"""

OVERVIEW = "Overview & Fetal Skeleton"
PECTORAL = "Pectoral Girdle"
ARM = "Arm & Forearm"
HAND = "Wrist & Hand"
PELVIS = "Pelvic Girdle"
LEG = "Thigh & Leg"
FOOT = "Ankle & Foot"

NOTES = [
    # ============================ OVERVIEW & FETAL SKELETON ============================
    dict(deck=OVERVIEW, num=True, img="m8_01_appendicular.jpg",
         ver="lab manual p.170 + Fig 8-1 ('Of the 210 bones ... 130'); study guide p.1 ('130 appendicular bones of 210'); slide 2 ('Appendicular Skeleton (126)'); lab recording 9/30 [01:05]",
         text="The lab manual counts {{c1::130::number}} appendicular bones out of 210, not the "
              "slides' 126 out of 206.",
         back="Why: the manual adds four sesamoid bones (two under each big toe) to the "
              "appendicular count.<br><br>Pitfall: sources disagree on the totals; on the last "
              "home quiz the lab gave credit for every published count (9/30 recording)."),
    dict(deck=OVERVIEW, img="m8_01_appendicular.jpg",
         ver="lab manual p.170 ('Most of those bones are found in the hands and feet'); study guide p.1",
         text="Most of the appendicular skeleton's bones are in the {{c1::hands and feet}}.",
         back="Why: each hand and wrist holds 27 bones and each foot 26, so 106 of the 126 "
              "appendicular bones are in the hands and feet."),
    dict(deck=OVERVIEW, num=True, img="m8_01_appendicular.jpg",
         ver="lab manual p.170 ('Sixty bones are found in the upper limbs') + Fig 8-1; slide 2; blue page Q2",
         text="Each upper limb has {{c1::30::number}} bones: the humerus, radius, ulna, 8 "
              "carpals, 5 metacarpals, and 14 phalanges.",
         back="Why: 1 + 1 + 1 + 8 + 5 + 14 = 30, so the two upper limbs hold 60 bones, most of "
              "them in the hands."),
    dict(deck=OVERVIEW, num=True, img="m8_01_appendicular.jpg",
         ver="slide 2 (Femur, Patella, Tibia, Fibula (2 each), Tarsals (14), Metatarsals (10), Phalanges (28)); lab manual Fig 8-1 (+ '4 sesamoids'); study guide p.1 ('lower limbs 64'); blue page Q2",
         text="Each lower limb has {{c1::30::number}} bones, not counting sesamoids: the femur, "
              "patella, tibia, fibula, 7 tarsals, 5 metatarsals, and 14 phalanges.",
         back="Why: 1 + 1 + 1 + 1 + 7 + 5 + 14 = 30.<br><br>Pitfall: the manual adds the two "
              "sesamoids under each big toe, giving 32 per limb (64 for both)."),
    dict(deck=OVERVIEW, num=True, img="m8_01_appendicular.jpg",
         ver="slide 2 (Scapula (2), Clavicles (2), Os coxae (2)); lab manual Fig 8-1; study guide p.1 ('pectoral girdle 4 · ... · os coxae 2'); blue page Q2",
         text="The pectoral girdles contribute {{c1::4::number}} bones to the appendicular "
              "skeleton, and the pelvic girdle contributes {{c2::2::number}}.",
         back="Why: each pectoral girdle is a clavicle plus a scapula (2 × 2 = 4), while the "
              "pelvic girdle's appendicular part is just the two os coxae."),
    dict(deck=OVERVIEW, img="s02_overview.jpg",
         ver="lab recording 9/30 [06:39] ('first identify the anterior posterior side and then ... the left and right') + [47:50] (Dr. Blais: 'I got to pick it up'); slides 3 + 16 ('Be able to differentiate Left vs Right')",
         text="The lab's method for telling whether a loose bone is from the left or right side: "
              "first work out {{c1::anterior vs posterior}}, then use a medial or lateral "
              "landmark.",
         back="Why: many bones look right either way until you know which face is the front "
              "and which end is up; after that, one medial or lateral landmark settles the "
              "side.<br><br>Cue: on the practical the bone lies loose in any orientation, so "
              "pick it up and turn it into anatomical position first."),
    dict(deck=OVERVIEW, img="s02_overview.jpg",
         ver="lab recording 9/30 [28:11] ('all of this stuff is going to be in anatomical position, what we taught you in the first week')",
         text="The lab names every bone's orientation as if the body were in {{c1::anatomical "
              "position}} (standing, palms facing forward).",
         back="Why: in anatomical position the thumbs point outward, so the radius and its "
              "styloid process count as lateral even when your own forearm is turned.<br><br>"
              "Pitfall: a relaxed arm hangs palm-in, which makes the radius look anterior; "
              "always name sides as if the palms faced forward."),
    dict(deck=OVERVIEW, img="s05_humerus.png",
         ver="lab recording 9/30 [24:20] ('A fossa is something like a divot within a bone where something else sits') + [54:22] ('a divot within a bone, or a basin, or a concavity')",
         text="A {{c1::fossa}} is a shallow depression (a divot or basin) in a bone where "
              "another structure sits.",
         back="Why: the olecranon fossa, for example, is the pit on the back of the humerus "
              "that the ulna's olecranon drops into when you straighten your elbow."),
    dict(deck=OVERVIEW, img="s13_tibia_fibula.png",
         ver="lab recording 9/30 [24:20] ('tuberosity, tubercle, process ... bulging out from a bone') + [42:55] ('A spine is something that sticks out') + [61:26]",
         text="Tuberosities, tubercles, processes, and spines are all bone markings that "
              "{{c1::stick out (projections)::stick out or dip in}}.",
         back="Why: bone builds up where a muscle, tendon, or ligament pulls on it, raising "
              "bumps like the tibial tuberosity or the deltoid tuberosity."),
    dict(deck=OVERVIEW, img="s10_hip_medial.png",
         ver="slide 9 notes ('Foramen = hole'); lab recording 9/30 [50:18]-[51:05] ('There's a lot of important structures that flow through foramens')",
         text="A {{c1::foramen}} is a hole through a bone that lets structures such as nerves "
              "and blood vessels pass.",
         back="Why: the obturator foramen of the hip bone, the largest foramen in the body, "
              "is a good example.<br><br>Pitfall: foramina are holes in BONES; openings in "
              "muscles are not called foramina (9/30 recording)."),
    dict(deck=OVERVIEW, num=True, img="s02_overview.jpg",
         ver="lab recording 9/30 [00:51] (home-quiz correction: 'the percent of calcium in the bones. It was supposed to be 99%')",
         text="About {{c1::99::percent}}% of the body's calcium is stored in the bones.",
         back="Why: bone mineral is calcium phosphate (hydroxyapatite), so the skeleton doubles "
              "as the body's calcium bank and releases calcium into the blood when levels "
              "drop."),
    dict(deck=OVERVIEW, num=True, img="m8_17_fetal.jpg",
         ver="lab manual p.182 ('a newborn baby has closer to 275 bones'); study guide p.2 ('Newborn ≈ 275 bones')",
         text="A newborn has about {{c1::275::number}} bones.",
         back="Why: many adult bones, such as the sternum and the phalanges, start out as "
              "several pieces that fuse later in life.<br><br>Pitfall: estimates vary (roughly "
              "270 to 300); 275 is the lab manual's figure."),
    dict(deck=OVERVIEW, img="m8_17_fetal.jpg",
         ver="lab manual p.182 ('The skull of the fetus is disproportionately large, as is the ribcage. The limbs ... disproportionately short'); study guide p.2",
         text="In a fetus, the {{c1::skull}} and ribcage are disproportionately large, while "
              "the {{c2::limbs}} are disproportionately short.",
         back="Why: growth runs head-first, so the brain and chest develop early and the "
              "limbs do most of their lengthening after birth."),
    dict(deck=OVERVIEW, img="m8_17_fetal.jpg",
         ver="lab manual p.182 ('The wrist and ankle bones are small and mostly cartilage'); study guide p.2",
         text="In a fetus, the wrist and ankle bones are small and mostly {{c1::cartilage}}.",
         back="Why: bones form by replacing a cartilage model, and the carpals and tarsals are "
              "among the last to ossify; most carpals don't start until after birth."),
    dict(deck=OVERVIEW, img="m8_18_fetal_skull.jpg",
         ver="lab manual p.182 ('The mandible is almost straight ... makes nursing easier for the mother'); study guide p.2",
         text="The fetal mandible is almost {{c1::straight}}, which reduces the jaw's leverage "
              "and makes nursing easier for the mother.",
         back="Why: an angled adult jaw gives the chewing muscles a strong lever; the nearly "
              "straight newborn jaw produces far less bite force."),
    dict(deck=OVERVIEW, img="m8_18_fetal_skull.jpg",
         ver="lab manual p.182 ('held loosely together by connective tissues called fontanels'); study guide p.2 ('Fontanels (\"soft spots\")')",
         text="The fetal skull bones are not fused; they are joined by areas of connective "
              "tissue called {{c1::fontanels}}.",
         back="Why: the bones ossify from separate centers and don't meet and fuse until after "
              "birth.<br><br>Cue: the fontanels are the baby's 'soft spots' and last for "
              "months after birth."),
    dict(deck=OVERVIEW, img="m8_18_fetal_skull.jpg",
         ver="lab manual p.182 ('allows the skull (the widest part of the fetus) to be compressed and distorted during the birthing process'); study guide p.2",
         text="Fontanels let the fetal skull {{c1::compress and change shape}} as it passes "
              "through the birth canal.",
         back="Why: the skull is the widest part of the baby, and bones held by flexible "
              "tissue can shift and overlap slightly instead of cracking."),

    # ================================= PECTORAL GIRDLE =================================
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="slide 2 (Pectoral Girdle: Scapula, Clavicles); slide 3 notes ('Made of scapula and clavicle'); lab manual p.170",
         text="Each pectoral girdle is made of two bones: the {{c1::clavicle}} and the "
              "{{c1::scapula}}.",
         back="Why: together they hang each arm from the trunk; the clavicle braces the "
              "shoulder out to the side and the scapula provides the socket."),
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="slide 3 notes ('Attaches upper limb to axial skeleton'); lab recording 9/30 [07:31]; lab manual p.170",
         text="The pectoral girdle attaches the {{c1::upper limb}} to the {{c2::axial "
              "skeleton}}.",
         back="Why: the limbs are appendicular, so each needs a girdle to anchor it to the "
              "body's central axis."),
    dict(deck=PECTORAL, img="m8_03_clavicles.jpg",
         ver="lab manual p.170 ('the only articulation of the upper limbs with the axial skeleton occurs between the clavicles ... and the manubrium'); study guide p.1",
         text="The only bony joint between the upper limb and the axial skeleton is between "
              "the {{c1::clavicle}} and the {{c2::manubrium of the sternum}}.",
         back="Why: the scapula has no joint with the ribs or spine, so every force from the "
              "arm reaches the trunk through the clavicle.<br><br>Cue: the clavicle-manubrium "
              "joint is the sternoclavicular joint, beside the jugular notch at the base of "
              "the neck."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('These \"floating\" bones have no direct attachment to the axial skeleton ... held in place by muscles'); study guide p.1",
         text="The scapulae have no direct attachment to the axial skeleton; they are held "
              "over the posterior ribs by {{c1::muscles}}.",
         back="Why: held by muscle alone, each scapula can slide up and down and side to side "
              "over the ribs, which greatly widens the arm's range of motion."),
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="slide 3 figure ('Sternal (medial) end', 'Acromial (lateral) end') + notes (landmarks: Acromial end, Sternal End)",
         text="The clavicle's medial end is the {{c1::sternal}} end and its lateral end is the "
              "{{c1::acromial}} end.",
         back="Why: each end is named for what it meets: the sternum (manubrium) medially and "
              "the acromion of the scapula laterally."),
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="slide 3 figure ('Acromioclavicular joint'); lab recording 9/30 [11:30] ('the acromial end, articulates with the acromial process'); study guide p.1",
         text="The acromial end of the clavicle articulates with the {{c1::acromion (acromial "
              "process) of the scapula::which part of which bone}}.",
         back="Why: the acromioclavicular (AC) joint at the top of the shoulder is the "
              "clavicle's only link to the scapula."),
    dict(deck=PECTORAL, img="m8_03_clavicles.jpg",
         ver="lab manual p.170 + Fig 8-3 ('acromial end (flat)', 'sternal end (triangular)'); study guide p.1; slide 3 ('The flat sternal end points medially'); lab recording 9/30 [08:20]-[09:08] (sternal end 'looks kind of like a nail'; acromial end 'the round part')",
         text="On a loose clavicle, the thick, blunt end with a triangular outline is the "
              "{{c1::sternal}} end; the broad, flattened end is the {{c1::acromial}} end.",
         back="Why: the sternal end is built up to bear against the manubrium, while the "
              "acromial end flattens out to meet the small acromion.<br><br>Pitfall: 'flat' "
              "is used both ways. The slide and the instructor mean the sternal end's flat tip "
              "(like a nail head); the manual means the acromial end's flattened shape. Go by "
              "thickness: the thick end is sternal."),
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="lab recording 9/30 [10:44] ('this bigger curvature ... is going to be facing anterior'); lab manual p.170 (S-shaped); slide 3 figure (superior view)",
         text="The clavicle is S-shaped, and its larger (medial) curve bulges "
              "{{c1::anteriorly::which direction}}.",
         back="Why: the medial two-thirds curves forward and the lateral third curves back, so "
              "the bone arcs around the front of the ribcage to reach the shoulder.<br><br>"
              "Cue: the big bow you feel along your collarbone near the sternum is the forward "
              "curve."),
    dict(deck=PECTORAL, img="s03_clavicle.png",
         ver="slide 3 ('the conoid tubercle points inferiorly'); lab recording 9/30 [09:55] ('closer to the acromial end, this is going to be inferior'); lab manual Fig 8-3 (inferior view)",
         text="The conoid tubercle is on the {{c1::inferior::which surface}} side of the "
              "clavicle, near the {{c2::acromial::which}} end.",
         back="Why: the conoid tubercle anchors the conoid ligament, which ties the clavicle down to the "
              "coracoid process below, so finding it tells you which surface faces down."),
    dict(deck=PECTORAL, side="front", img="lr_clavicle_superior.png",
         ver="slide 3 figure (b) 'Right clavicle, superior view' (labels erased); orientation rules slide 3; lab recording 9/30 [11:30] ('It's the right clavicle')",
         text="A clavicle seen from above, with the front of the body toward the bottom of the "
              "picture: is it a right or a left clavicle? {{c1::right::side}}",
         back="Why: the thick, blunt end at the picture's right is the sternal end (medial), "
              "so the flattened acromial end points to the picture's left. Looking down from "
              "above with the front toward the bottom, the picture's left is the body's right."
              "<br><br>Cue: sternal end medial, big curve bulging forward, conoid tubercle "
              "underneath."),
    dict(deck=PECTORAL, img="s04_scapula.png",
         ver="slide 4 ('The glenoid cavity faces laterally') + notes ('Glenoid cavity is always lateral'); lab recording 9/30 [14:40]",
         text="The glenoid cavity of the scapula always faces {{c1::laterally::direction}}.",
         back="Why: the glenoid cavity is the socket for the head of the humerus, and the arm hangs off the "
              "side of the body.<br><br>Pitfall: beginners often take the scapula's long "
              "curved edge for the lateral side; find the glenoid cavity instead, since "
              "wherever it points is lateral."),
    dict(deck=PECTORAL, img="s04_scapula.png",
         ver="slide 4 ('the spine projects posteriorly') + notes ('Spine of scapula is always posterior'); lab recording 9/30 [13:06]; study guide p.1",
         text="The spine of the scapula is always on its {{c1::posterior::which surface}} surface.",
         back="Why: the spine is a ridge that anchors back and shoulder muscles, while the "
              "front of the scapula lies against the ribs as a smooth hollow (the subscapular "
              "fossa)."),
    dict(deck=PECTORAL, img="s04_scapula.png",
         ver="slide 4 ('Coracoid process is more anterior than the acromial process'); lab recording 9/30 [13:52]",
         text="On the scapula, the {{c1::coracoid process}} is anterior to the acromion.",
         back="Why: the coracoid hooks forward under the clavicle toward the chest, while the "
              "acromion extends from the spine over the top of the shoulder."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="slide 4 notes ('Be able to distinguish between acromial process and coracoid process'); lab recording 9/30 [20:15] ('this bigger one is called the acromial process'); lab manual Fig 8-2",
         text="Of the two processes above the glenoid cavity, the larger, flat one that "
              "continues from the spine is the {{c1::acromion}}, and the smaller, finger-like "
              "hook that curls forward is the {{c1::coracoid process}}.",
         back="Why: the acromion is the outer end of the scapula's spine, forming the tip of "
              "the shoulder; the coracoid ('like a crow's beak') projects forward below the "
              "clavicle."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab recording 9/30 [13:52]-[14:40] ('the glenoid cavity, which is where the humerus attaches'); lab manual p.170; study guide p.1 ('Glenoid cavity = shallow socket for the humeral head')",
         text="The glenoid cavity is the socket where the {{c1::head of the humerus}} "
              "articulates, forming the shoulder joint.",
         back="Why: the socket is shallow, which trades stability for the shoulder's huge "
              "range of motion.<br><br>Cue: glenohumeral joint = glenoid + humerus."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('The acromion and coracoid process wrap around the head of the humerus superiorly'); study guide p.1",
         text="The acromion and the coracoid process wrap around the head of the humerus from "
              "{{c1::above (superiorly)}}.",
         back="Why: together they form a bony roof over the shoulder joint, shielding it and "
              "anchoring muscles and ligaments."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('three angles and three borders: The superior, lateral and inferior angles and the lateral, medial and superior borders'); study guide p.1; lab recording 9/30 [16:15] ('I want you guys to know the borders'); slide 4 overlays ('superior angle', 'Inferior angle')",
         text="The scapula has three borders ({{c1::superior, medial, and lateral}}) and "
              "three angles ({{c2::superior, inferior, and lateral}}).",
         back="Why: the scapula is a flat triangle, so its edges are named by where they face "
              "(up, toward the spine, toward the armpit) and its corners likewise; the lateral "
              "angle is the thick corner that carries the glenoid cavity."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="study guide p.1 ('Suprascapular notch sits on the superior border'); lab manual Fig 8-2; slide 4 figure ('Scapula notch')",
         text="The suprascapular notch (the slide's 'scapula notch') is on the scapula's "
              "{{c1::superior border}}.",
         back="Why: the suprascapular nerve passes through it on its way to the muscles on "
              "the back of the scapula."),
    dict(deck=PECTORAL, tags=["optional"], img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('The flattened area above the spine is the supraspinous fossa and the larger ... beneath the spine is the infraspinous fossa'); study guide p.1; slide 4 figure; lab recording 9/30 [16:15] (won't be asked)",
         text="The spine divides the back of the scapula into the {{c1::supraspinous}} fossa "
              "above it and the larger {{c2::infraspinous}} fossa below it.",
         back="Why: supra- means above and infra- means below the spine; each fossa holds the "
              "rotator-cuff muscle named for it.<br><br>Pitfall: the lab instructor said "
              "(9/30) they won't ask about these two fossae."),
    dict(deck=PECTORAL, img="s04_scapula.png",
         ver="slide 4 (overlay 'Subscapular fossa'); lab manual Fig 8-2; study guide p.1 ('Anterior face = subscapular fossa')",
         text="The anterior (rib-facing) surface of the scapula is the {{c1::subscapular "
              "fossa}}.",
         back="Why: sub- means under; it is the underside of the scapula, a smooth hollow "
              "pressed against the ribs with no spine on it."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('the acromion can be easily seen and felt as a bump on the superior aspect of the shoulder') + p.179; study guide p.1",
         text="The bony bump at the top of the shoulder is the {{c1::acromion}}.",
         back="Why: the acromion is the end of the scapula's spine and lies just under the skin where it "
              "meets the clavicle.<br><br>Cue: raise your arm and you can also find it in the "
              "dip the deltoid makes at the top of the shoulder."),
    dict(deck=PECTORAL, img="m8_02_scapula.jpg",
         ver="lab manual p.170 ('the coracoid process can sometimes be seen on the anterior aspect of the shoulder ... just below the clavicle'); study guide p.1",
         text="The {{c1::coracoid process}} can sometimes be felt on the upper chest just "
              "below the clavicle.",
         back="Why: the coracoid is the only part of the scapula that reaches the front of the body, "
              "curling forward under the clavicle."),
    dict(deck=PECTORAL, side="front", img="lr_scapula_posterior.jpg",
         ver="slide 4 figure, posterior view of a right scapula (labels erased); slide 4 notes ('Be able to differentiate right vs left scapula')",
         text="A scapula seen from behind (posterior view): is it a right or a left scapula? "
              "{{c1::right::side}}",
         back="Why: the spine shows, so you are looking at its back; the glenoid cavity always "
              "points laterally, and it is on the picture's right. Seen from behind, lateral on "
              "your right means the body's right side."),
    dict(deck=PECTORAL, side="front", img="pp2_front_pins.png",
         ver="Popcorn Points slide 2, pin 9 (the instructor key lists only the axial pins: 'The other bones are appendicular')",
         text="Skeleton seen from the front: name the bone at pin 9. {{c1::clavicle::bone}}",
         back="Why: the clavicle is the S-shaped bone running from the top of the sternum (the "
              "manubrium, pin 12) out to the shoulder."),
    dict(deck=PECTORAL, side="front", img="pp2_back_pins.png",
         ver="Popcorn Points slide 2, pin 10 (no instructor key for appendicular pins)",
         text="Skeleton seen from behind: name the bone at pin 10. {{c1::scapula::bone}}",
         back="Why: the scapula is the flat, triangular bone lying over the upper back ribs, with the "
              "ridge of its spine running across it."),

    # ================================== ARM & FOREARM ==================================
    dict(deck=ARM, img="s05_humerus.png",
         ver="lab manual p.170 ('The arm contains only one bone - the humerus'); slide 5 title",
         text="Anatomically, the arm is only the segment from the shoulder to the elbow; its "
              "one bone is the {{c1::humerus::bone}}.",
         back="Why: anatomists call the elbow-to-wrist segment the forearm, so 'arm' means "
              "only the upper segment."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="lab recording 9/30 [17:01] ('This attaches to the glenoid cavity of the scapula and articulates with the radius and ulna'); lab manual p.170",
         text="The humerus articulates proximally with the {{c1::scapula (glenoid cavity)}} "
              "and distally with the {{c2::radius and ulna}}.",
         back="Why: the humerus's rounded head fits the glenoid cavity at the shoulder, and its "
              "capitulum and trochlea meet the forearm bones at the elbow.<br><br>Pitfall: the "
              "manual says the humerus also articulates with the clavicle; it doesn't. The "
              "clavicle meets only the acromion and the sternum."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 ('Head is directed medially') + notes ('Humoral head is medial'); lab recording 9/30 [17:49]",
         text="The head of the humerus points {{c1::medially}}.",
         back="Why: the head has to face the glenoid cavity, which sits medial to the arm."
              "<br><br>Pitfall: the head points 'inward' whichever way you turn the bone, so it "
              "can't tell front from back; pair it with the deltoid tuberosity or the olecranon "
              "fossa."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 ('deltoid tuberosity is angled laterally') + notes ('Deltoid tuberosity is lateral'); lab recording 9/30 [17:49]; lab manual p.170-171 ('Approximately midway down the length of the diaphysis')",
         text="The deltoid tuberosity is on the {{c1::lateral}} side of the humeral shaft, "
              "about halfway down.",
         back="Why: the deltoid tuberosity is the roughened spot where the deltoid muscle, the cap of the "
              "shoulder, inserts, and the deltoid wraps the outside of the arm."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 ('Olecranon fossa is located posteriorly'); lab recording 9/30 [18:44]; lab manual p.171 ('Between the epicondyles posteriorly is a deep cleft called the olecranon fossa')",
         text="The olecranon fossa is on the {{c1::posterior}} surface of the distal humerus.",
         back="Why: the olecranon fossa is the deep pit that takes the ulna's olecranon when the elbow "
              "straightens, and the olecranon is the back point of the elbow."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.171 ('Between the epicondyles anteriorly are two clefts: The coronoid fossa and the radial fossa'); study guide p.1",
         text="The coronoid fossa and the radial fossa are on the {{c1::anterior}} surface of "
              "the distal humerus.",
         back="Why: the two fossae take the ulna's coronoid process and the head of the radius when the "
              "elbow bends fully, and bending brings those parts forward against the "
              "humerus."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 notes ('Capitulum of Humerus articulates with Head of Radius'); lab manual p.171; study guide p.1 ('capitulum is the “little head” for the radius')",
         text="The capitulum of the humerus articulates with the {{c1::head of the radius}}.",
         back="Why: capitulum means 'little head': a rounded knob on the lateral side of the "
              "distal humerus that the radial head spins against.<br><br>Cue: capitulum "
              "(lateral) = radius; trochlea (medial) = ulna."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 notes ('Trochlea of Humerus articulates with Trochlear Notch of Ulna'); lab manual p.171; study guide p.1; lab recording 9/30 [25:06]",
         text="The trochlea of the humerus articulates with the trochlear notch of the "
              "{{c1::ulna::which bone}}.",
         back="Why: trochlea means 'pulley': a spool-shaped surface that the ulna's C-shaped "
              "notch wraps around, making the elbow a hinge."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="slide 5 notes ('Olecranon Fossa of Humerus articulates with Olecranon Process of Ulna'); lab manual p.171 ('receives the olecranon of the ulna when the arm is fully extended'); study guide p.1",
         text="The olecranon fossa takes the ulna's olecranon when the elbow is fully "
              "{{c1::extended::flexed or extended}}.",
         back="Why: straightening swings the olecranon back and up into the pit on the back of "
              "the humerus, which stops the elbow from bending backward."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="slide 5 notes ('Coronoid Fossa of Humerus articulates with Coronoid Process of Ulna'); lab manual p.171 ('when the arm is fully flexed'); study guide p.1",
         text="The coronoid fossa takes the ulna's coronoid process when the elbow is fully "
              "{{c1::flexed::flexed or extended}}.",
         back="Why: bending brings the front lip of the ulna's C-shaped notch up against the "
              "front of the humerus."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.171 ('the coronoid fossa and the radial fossa, which accept coronoid process of the ulna and the head of the radius, respectively, when the arm is fully flexed'); study guide p.1; lab recording 9/30 [21:04]",
         text="The radial fossa takes the {{c1::head of the radius}} when the elbow is fully "
              "flexed.",
         back="Why: the radial fossa sits just above the capitulum on the front of the humerus, lateral to "
              "the coronoid fossa, and gives the radial head room as the elbow bends."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 notes ('Greater tubercle is more lateral'); lab recording 9/30 [20:16] ('the greater tubercle is more superior lateral to the lesser tubercle')",
         text="The greater tubercle is {{c1::lateral}} to the lesser tubercle on the proximal "
              "humerus.",
         back="Why: the lesser tubercle faces forward (anterior), while the greater tubercle "
              "forms the outer edge of the shoulder.<br><br>Cue: both tubercles show from the "
              "anterior view."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="study guide p.1 ('Greater and lesser tubercles = proximal rotator-cuff attachments'); lab recording 9/30 [20:16] ('places for muscle attachments')",
         text="The greater and lesser tubercles of the humerus are attachment points for the "
              "{{c1::rotator cuff}} muscles.",
         back="Why: the rotator cuff holds the humeral head in the shallow glenoid cavity, so "
              "it attaches right beside the head."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="slide 5 figure ('Intertubercular groove')",
         text="The groove between the greater and lesser tubercles is the "
              "{{c1::intertubercular groove (sulcus)}}.",
         back="Why: inter- means between; the groove carries the tendon of the biceps' long "
              "head up over the front of the humerus to the shoulder."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.170 ('The anatomical neck marks the boundary of the glenohumeral joint as defined by the synovial cavity'); study guide p.1",
         text="The {{c1::anatomical neck}} of the humerus is the rim just below the head that "
              "marks the edge of the shoulder joint.",
         back="Why: the joint capsule attaches there, so it outlines the joint surface itself."
              "<br><br>Distinguish: the surgical neck is the narrower shaft just below the "
              "tubercles, the common fracture site."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.170 ('the surgical neck is a narrowing region of the bone distal to the joint'); study guide p.1 ('common fracture site')",
         text="The {{c1::surgical neck}} of the humerus, the narrowing just below the "
              "tubercles, is a common fracture site.",
         back="Why: the bone narrows where the wide head and tubercles meet the slimmer shaft, "
              "so falls on the arm often break it there."),
    dict(deck=ARM, img="s05_humerus.png",
         ver="lab recording 9/30 [21:04] ('the medial epicondyle is going to be that bigger spot ... what you're going to feel right here on the medial side of your elbow')",
         text="The larger, more prominent epicondyle, the one you feel on the inner side of the "
              "elbow, is the {{c1::medial}} epicondyle.",
         back="Why: the medial epicondyle anchors many forearm flexor muscles, and the ulnar nerve runs just "
              "behind it (the 'funny bone')."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.171 ('The lateral epicondyle and medial epicondyle are projections that stabilize the elbow joint. Both epicondyles can be easily palpated'); study guide p.1",
         text="The medial and lateral epicondyles of the humerus are projections that "
              "{{c1::stabilize the elbow joint}}.",
         back="Why: ligaments and forearm muscles anchor on them on both sides of the elbow, "
              "and both can be felt easily."),
    dict(deck=ARM, img="m8_04b_humerus.jpg",
         ver="lab manual p.179 ('The humerus of the arm can only be felt at the distal end because the proximal end is within the shoulder joint and surrounded by large muscles')",
         text="Of the humerus, only the {{c1::distal::proximal or distal}} end can be felt, because the proximal "
              "end sits inside the shoulder joint under large muscles.",
         back="Why: the deltoid and rotator cuff bury the head, while at the elbow the two "
              "epicondyles lie just under the skin."),
    dict(deck=ARM, side="front", img="lr_humerus_anterior.png",
         ver="slide 5 figure (a) anterior view of a right humerus (labels erased); lab recording 9/30 [20:16] ('So is this right or left? Right, awesome')",
         text="A humerus seen from the front (anterior view): is it a right or a left humerus? "
              "{{c1::right::side}}",
         back="Why: the head points medially, and here it points to the picture's right. Seen "
              "from the front, a bone whose medial side is on your right is from the body's "
              "right side.<br><br>Cue: the deltoid tuberosity (lateral) is on the picture's "
              "left."),
    dict(deck=ARM, side="front", img="pp2_back_pins.png",
         ver="Popcorn Points slide 2, pin 11 (no instructor key for appendicular pins)",
         text="Skeleton seen from behind: name the bone at pin 11. {{c1::humerus::bone}}",
         back="Why: the humerus is the only bone of the arm, running from the shoulder to the elbow."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('The ulna is medial while the radius is lateral'); slide 7 ('Radius leads to the thumb while the ulna leads to the pinky')",
         text="In anatomical position, the forearm bone on the lateral (thumb) side is the "
              "{{c1::radius}}, and the one on the medial (pinky) side is the {{c1::ulna}}.",
         back="Why: in anatomical position the palms face forward and the thumbs point "
              "outward.<br><br>Mnemonic: the radius leads to the thumb, the ulna to the "
              "pinky."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab recording 9/30 [26:40] ('the ulna is very large in the superior portion ... in the radius we have a smaller proximal end and a larger distal end'); lab manual p.171 ('The ulna is large proximally and tapers off distally'); study guide p.1",
         text="The ulna is large at its {{c1::proximal}} end, and the radius is large at its "
              "{{c2::distal}} end.",
         back="Why: each bone is biggest where it carries its main joint: the ulna at the "
              "elbow, the radius at the wrist."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab recording 9/30 [43:49]-[44:37] ('the ulna ... was the primary articulating bone of the humerus', 'the radius is the primary articulating bone for the wrist'); study guide p.1; lab manual p.171",
         text="At the elbow, the humerus articulates mainly with the {{c1::ulna}}; at the "
              "wrist, the carpals articulate mainly with the {{c1::radius}}.",
         back="Why: the ulna's C-shaped notch grips the humerus to make the elbow's hinge, "
              "and the radius's wide distal end carries the wrist."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 notes ('Ulna has a “claw” at proximal end'); lab recording 9/30 [23:34] ('big, nice C-shaped claw') + [71:00] (Dr. Blais: 'looks like a wrench')",
         text="The forearm bone with a C-shaped 'claw' (a wrench shape) at its proximal end is "
              "the {{c1::ulna}}.",
         back="Why: the claw is the trochlear notch, framed by the olecranon behind and the "
              "coronoid process in front, and it grips the humerus's trochlea like a wrench "
              "on a bolt."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 notes ('Radius has a circular structure at proximal end'); lab recording 9/30 [71:49] (Dr. Blais: 'that little circular rotating area on the head of the radius')",
         text="The forearm bone with a round, disc-shaped head at its proximal end is the "
              "{{c1::radius}}.",
         back="Why: the disc spins against the capitulum and the ulna's radial notch, which "
              "lets the forearm rotate (pronate and supinate)."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab manual p.171 ('The olecranon forms the bony point of the elbow'); study guide p.1 ('Point of the elbow')",
         text="The olecranon of the ulna forms the bony point of the {{c1::elbow}}.",
         back="Why: the olecranon is the top of the ulna's C, sticking out behind the joint; it's what "
              "you lean on when you rest on your elbows."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab manual p.171 ('locks the forearm in position during full extension ... also prevents overextension of the elbow joint'); study guide p.1",
         text="In full extension, the olecranon locks into the olecranon fossa, which keeps the "
              "elbow from {{c1::overextending (hyperextending)}}.",
         back="Why: once the olecranon hits bone at the back of the humerus, the elbow cannot "
              "straighten any further."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="lab recording 9/30 [25:53] ('the coronoid process is more anterior, whereas the olecranon process is more posterior')",
         text="On the ulna's C-shaped proximal end, the {{c1::coronoid process}} is the front "
              "lip and the {{c1::olecranon}} is the back one.",
         back="Why: the C opens forward to hold the trochlea, so its lower lip juts forward "
              "(coronoid) and its upper hook rises behind (olecranon)."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('Trochlear notch faces anteriorly') + notes",
         text="The trochlear notch of the ulna faces {{c1::anteriorly}}.",
         back="Why: the notch opens forward to cradle the trochlea, with the olecranon rising "
              "behind it, so the open side of the 'C' is the front."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('The radial tuberosity is directed medially'); lab recording 9/30 [25:53]",
         text="The radial tuberosity is directed {{c1::medially::direction}}.",
         back="Why: the radial tuberosity sits on the inner (ulnar) side of the radius just below the head, where "
              "the biceps tendon pulls on the bone."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('rough surface on distal end is posterior') + notes ('Smooth surface of distal radius is anterior'); lab recording 9/30 [30:41]",
         text="The smooth, flat surface of the distal radius faces {{c1::anteriorly}}; its "
              "rough, ridged surface faces posteriorly.",
         back="Why: the back of the distal radius is ridged by grooves for the extensor "
              "tendons, while the palm side is smooth and flat."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('The ulnar styloid process is medial while the radial styloid is lateral') + notes ('Styloid process of radius is lateral'); lab recording 9/30 [27:26]; study guide p.1 ('Radial styloid = bump on the thumb side')",
         text="The styloid process of the radius is on the {{c1::lateral::medial or lateral}} "
              "side of the wrist.",
         back="Why: the radius is the thumb-side forearm bone, so its pointed tip is the bump "
              "you feel on the thumb side of your wrist.<br><br>Cue: the radial styloid is the key landmark "
              "for siding a loose radius."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 ('The ulnar styloid process is medial'); lab recording 9/30 [28:11] ('It is on the head of the ulna'); study guide p.1 ('Ulnar styloid = bump on the pinky side')",
         text="The styloid process of the ulna is on the {{c1::medial::medial or lateral}} side "
              "of the wrist, projecting from the {{c2::head of the ulna}}.",
         back="Why: the ulna ends at the wrist on the pinky side, and its small pointed "
              "styloid juts down from its head."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab recording 9/30 [27:26] ('the head of the ulna right down here, that is the smaller portion, whereas the head of the radius is going to be up here'); slide 6 figure; lab manual p.173",
         text="The head of the ulna is at its {{c1::distal}} end, while the head of the "
              "radius is at its {{c2::proximal}} end.",
         back="Why: each 'head' is the rounded end that turns in the other bone's notch: the "
              "radius's at the elbow, the ulna's at the wrist.<br><br>Pitfall: the ulna's "
              "head is its SMALL end; its big end is the olecranon at the elbow."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab manual p.173 ('the head of the ulna articulates with the ulnar notch of the radius'); study guide p.1; slide 6 figure",
         text="At the distal radioulnar joint, the {{c1::head of the ulna}} fits into the "
              "{{c2::ulnar notch}} of the radius.",
         back="Why: the radius swings around the fixed head of the ulna here when you turn "
              "your palm up or down."),
    dict(deck=ARM, img="s06_forearm.png",
         ver="slide 6 figure ('Radial notch', 'Proximal radioulnar joint'); study guide p.1 ('Head spins on the capitulum and in the radial notch of the ulna')",
         text="At the proximal radioulnar joint, the {{c1::head of the radius}} turns in the "
              "{{c2::radial notch}} of the ulna.",
         back="Why: the radial head spins in place in this notch while the forearm rotates."),
    dict(deck=ARM, img="m8_04a_joints.jpg",
         ver="lab manual p.173 ('The radius rotates around the head of the ulna when the hand undergoes pronation & supination') + Fig 8-4; lab recording 9/30 [71:49] (Dr. Blais)",
         text="During pronation and supination, the {{c1::radius}} rotates around the ulna.",
         back="Why: the ulna is locked to the humerus in a hinge that only bends, so turning "
              "the palm up or down has to come from the radius swinging around it."),
    dict(deck=ARM, img="m8_04a_joints.jpg",
         ver="lab manual Fig 8-4 ('hinge joint (flexion / extension)', 'rotational joint (supination / pronation)')",
         text="At the elbow, the humerus-ulna joint is a {{c1::hinge}} joint (flexion and "
              "extension), and the radius-ulna joint is a {{c2::rotational (pivot)}} joint "
              "(supination and pronation).",
         back="Why: the trochlear notch can only swing around the trochlea like a door on a "
              "hinge, while the round radial head spins in place like a wheel on an axle."),
    dict(deck=ARM, num=True, img="m8_11_q_carrying.jpg",
         ver="study guide p.1 ('About 10–15° of valgus at the extended elbow. It lets the forearms clear the hips'); lab manual Fig 8-11 ('carrying angle 10-15°')",
         text="With the elbow straight, the forearm angles outward about {{c1::10–15::degrees}}° "
              "from the arm (the carrying angle).",
         back="Why: the angle lets the forearms swing clear of the hips when the arms hang at "
              "the sides."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab manual p.179 ('The ulna can be felt from one end of the bone to the other', 'the radius cannot be felt from end-to-end'); study guide p.1",
         text="The {{c1::ulna::bone}} can be traced end to end on your forearm; the radius cannot.",
         back="Why: the ulna's back border lies just under the skin from the olecranon to the "
              "wrist, while the radius's shaft is buried under forearm muscles."),
    dict(deck=ARM, img="m8_04c_forearm.jpg",
         ver="lab manual p.179 ('the head of the radius ... a small bump immediately distal to the lateral epicondyle of the humerus. Try to feel the head of the radius rotate'); study guide p.1",
         text="The head of the radius can be felt just distal to the {{c1::lateral "
              "epicondyle}} of the humerus, turning as you rotate your palm up and down.",
         back="Why: the radial head sits right below the capitulum on the outer side of the "
              "elbow and rotates during pronation and supination."),
    dict(deck=ARM, side="front", img="lr_forearm_anterior.png",
         ver="slide 6 figure (a) anterior view of a right radius and ulna (labels erased)",
         text="A radius and ulna seen from the front (anterior view): is this a right or a left "
              "forearm? {{c1::right::side}}",
         back="Why: the radius (round head at the elbow, wide end at the wrist) is on the "
              "picture's left, and the radius is lateral. Seen from the front, lateral on your "
              "left means the body's right side."),
    dict(deck=ARM, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 17 (no instructor key for appendicular pins)",
         text="Skeleton seen from the front: name the bone at pin 17. {{c1::ulna::bone}}",
         back="Why: at the elbow the ulna is the medial forearm bone, the one with the big "
              "proximal end; the radius (pin 18) runs down the thumb side."),
    dict(deck=ARM, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 18 (no instructor key for appendicular pins)",
         text="Skeleton seen from the front: name the bone at pin 18. {{c1::radius::bone}}",
         back="Why: the radius is the lateral (thumb-side) forearm bone, slim at the elbow and wide at "
              "the wrist."),
    dict(deck=ARM, tags=["optional"], img="s06_forearm.png",
         ver="slide 6 figure ('Interosseous membrane', not boxed); lab recording 9/30 [21:04]-[22:00] ('I won't ask you about this in the actual practical')",
         text="The sheet of connective tissue joining the shafts of the radius and ulna is the "
              "{{c1::interosseous membrane}}.",
         back="Why: the membrane ties the two bones together along their length and passes force from "
              "the radius to the ulna.<br><br>Pitfall: the lab instructor said this won't be "
              "asked on the practical."),

    # =================================== WRIST & HAND ===================================
    dict(deck=HAND, num=True, img="s07_hand.png",
         ver="slide 2 ('Carpals (16)'); lab manual p.173 ('8 bones in two rows of four'); lab recording 9/30 [64:38]-[65:25] (Dr. Blais: 'Eight in each wrist ... 16 carpal bones')",
         text="Each wrist has {{c1::8::number}} carpal bones (16 in the whole body).",
         back="Why: the carpals sit in two rows of four, a proximal row against the radius and a "
              "distal row against the metacarpals.<br><br>Pitfall: if a question says 'in the "
              "body', count both wrists (16)."),
    dict(deck=HAND, num=True, img="s07_hand.png",
         ver="slide 2 ('Metacarpals (10)'); lab recording 9/30 [44:37] ('There are five metacarpals') + [69:27] ('There are 10 metacarpals')",
         text="Each hand has {{c1::5::number}} metacarpals (10 in the body).",
         back="Why: one metacarpal carries each digit, and together they form the palm."),
    dict(deck=HAND, img="s07_hand.png",
         ver="lab recording 9/30 [44:37]-[45:29] ('we want to start always with the big thumb or the big toe ... It would be the fifth metacarpal'); slide 7 figure (1-5); lab manual Fig 8-6",
         text="Metacarpals and fingers are numbered 1 to 5 starting from the {{c1::thumb}}.",
         back="Why: numbering always starts from the thumb (or the big toe), so the pinky's "
              "metacarpal is metacarpal V.<br><br>Cue: give the full name on the practical, "
              "e.g. 'fifth metacarpal of the right hand.'"),
    dict(deck=HAND, num=True, img="s07_hand.png",
         ver="lab recording 9/30 [36:17] ('for the thumb ... we have the proximal bone, and then we have the distal bone'); study guide p.1 ('Thumb has 2 phalanges; fingers have 3')",
         text="The thumb has {{c1::2::number}} phalanges (proximal and distal); each other "
              "finger has {{c2::3::number}}.",
         back="Why: the thumb lacks a middle phalanx, so beyond the palm it bends at only one "
              "joint instead of two."),
    dict(deck=HAND, num=True, img="s07_hand.png",
         ver="slide 2 ('Phalanges (28)'); lab manual p.179 ('Each of the 14 phalanges can be felt'); study guide p.1 ('All 14 phalanges can be felt')",
         text="Each hand has {{c1::14::number}} phalanges (28 in both hands).",
         back="Why: 4 fingers × 3 phalanges + the thumb's 2 = 14."),
    dict(deck=HAND, num=True, img="s07_hand.png",
         ver="lab recording 9/30 [36:17]-[37:03] (the instructor's own question: 'How many middle phalange bones are there? Four')",
         text="A hand has 5 proximal, {{c1::4::number}} middle, and 5 distal phalanges.",
         back="Why: every digit has a proximal and a distal phalanx, but the thumb has no "
              "middle one."),
    dict(deck=HAND, img="m8_06a_hand_palmar.jpg",
         ver="slide 7 notes ('Especially the terminology of naming the bones in the phalanges (ex. 4th Proximal Phalange of the Right Hand)'); lab recording 9/30 [45:29] + [92:06] ('So specific, it would be a[n] olecranon process of the right')",
         text="Name a finger bone with three pieces of information: its {{c1::digit number "
              "(thumb = 1)}}, its {{c2::row (proximal, middle, or distal)}}, and the "
              "{{c3::side (right or left hand)}}.",
         back="Why: the practical asks for the specific bone, e.g. '4th proximal phalanx of "
              "the right hand'; 'phalanx' alone is only half right."),
    dict(deck=HAND, img="s07_hand.png",
         ver="slide 7 (Carpals list + 'Mnemonic: So Long To Pinky, Here Comes The Thumb') + notes; lab manual p.173 + Fig 8-6",
         text="Proximal-row carpals, thumb side to pinky side: So = {{c1::scaphoid}}, Long = "
              "{{c2::lunate}}, To = {{c3::triquetrum}}, Pinky = {{c4::pisiform}}.",
         back="Why: the proximal row sits against the radius and ulna, running from the "
              "thumb side to the pinky side.<br><br>Mnemonic: So Long To Pinky, Here Comes The "
              "Thumb."),
    dict(deck=HAND, img="s07_hand.png",
         ver="slide 7 (Carpals list + mnemonic) + notes ('Loop up and back around towards thumb'); lab manual p.173 + Fig 8-6",
         text="Distal-row carpals, pinky side back to the thumb: Here = {{c1::hamate}}, Comes = "
              "{{c2::capitate}}, The = {{c3::trapezoid}}, Thumb = {{c4::trapezium}}.",
         back="Why: after crossing the proximal row, the mnemonic loops up to the distal row "
              "and comes back toward the thumb.<br><br>Mnemonic: So Long To Pinky, Here Comes "
              "The Thumb."),
    dict(deck=HAND, img="s07_hand.png",
         ver="slide 7 notes ('Mnemonic works only if you start at scaphoid', 'Find proximal carpal on thumb side (near the radius on the thumb side)'); lab recording 9/30 [33:03]",
         text="The carpal mnemonic only works if you start at the {{c1::scaphoid::carpal}}, the "
              "proximal carpal on the thumb side, next to the radius.",
         back="Why: the order runs across the proximal row from thumb to pinky and then loops "
              "back along the distal row, so it has to start in that corner."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="slide 7 notes ('The pisiform is on the anterior (palm side) of the hand'); lab recording 9/30 [31:27]-[32:18] ('it's going to kind of sit on top of the triquetrum')",
         text="The {{c1::pisiform}} is the pea-shaped carpal that sits on the palm side of the "
              "wrist, on top of the triquetrum.",
         back="Why: pisiform means 'pea-shaped'; it lies inside a wrist flexor tendon, so it "
              "rides on the front of the triquetrum instead of sitting in the row."),
    dict(deck=HAND, img="s07_hand.png",
         ver="slide 7 notes ('The pisiform is on the anterior (palm side) of the hand--> how to determine left versus right'); lab recording 9/30 [37:57]-[38:43] ('actually that's medial, why did I say lateral? The PISI form is going to be medial')",
         text="On a loose hand, the pisiform marks both the {{c1::anterior (palm)}} side and "
              "the {{c2::medial (pinky)}} side.",
         back="Why: once you know which face is the palm and which edge is the pinky side, "
              "the thumb (lateral) is on the other edge and the side follows.<br><br>Pitfall: "
              "in lab the instructor first said 'lateral', then corrected herself; the "
              "pisiform is MEDIAL."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="lab manual p.173 ('the trapezium (which articulates with the thumb)'); study guide p.1 ('Trapezium → thumb')",
         text="The {{c1::trapezium}} is the distal carpal at the base of the thumb.",
         back="Why: the trapezium forms the saddle-shaped joint that lets the thumb swing across the palm."
              "<br><br>Mnemonic: trapeziUM sits under the thUMb."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="lab manual p.173 ('the trapezoid (which articulates with the index finger)'); study guide p.1; lab recording 9/30 [33:03]-[33:49] ('if we switch those up, that is technically wrong')",
         text="The {{c1::trapezoid}} is the distal carpal at the base of the index finger.",
         back="Why: the trapezoid sits between the trapezium (thumb) and the capitate (middle finger)."
              "<br><br>Pitfall: trapezoid and trapezium are spelled alike but are different "
              "bones, and the lab counts a swap as wrong."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="lab manual p.173 ('the capitate (which articulates with the middle finger)'); study guide p.1",
         text="The {{c1::capitate}} is the distal carpal at the base of the middle finger.",
         back="Why: capitate means 'head-shaped'; it is the largest carpal and sits in the "
              "center of the wrist."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="lab manual p.173 ('the hamate which articulates with the pinky and ring fingers'); study guide p.1",
         text="The {{c1::hamate}} is the distal carpal at the base of the ring and pinky "
              "fingers.",
         back="Why: hamate means 'hooked'; it has a hook on its palm side and carries the two "
              "metacarpals on the pinky side of the hand."),
    dict(deck=HAND, img="m8_06b_hand_dorsum.jpg",
         ver="lab manual p.179 ('at the base of the hypothenar eminence the pisiform bone can be palpated'; the triquetrum is 'distal to the head of the ulna'); conflicts: lab manual p.173 + study guide p.1 swap the two",
         text="The bump at the base of the hypothenar eminence (the fleshy heel of the palm on "
              "the pinky side) is the {{c1::pisiform}}.",
         back="Why: the pisiform sits on the palm side of the wrist, on top of the triquetrum, "
              "right where the heel of the hand meets the wrist crease.<br><br>Pitfall: manual "
              "p.173 and the study guide swap these two; p.179 has it right. The triquetrum is "
              "the smaller bump on the back of the wrist just past the head of the ulna."),
    dict(deck=HAND, num=True, img="m8_06a_hand_palmar.jpg",
         ver="lab manual p.173 ('There are 27 bones in each hand and wrist'); study guide p.1 ('27 bones each side')",
         text="Each hand and wrist together contain {{c1::27::number}} bones.",
         back="Why: 8 carpals + 5 metacarpals + 14 phalanges = 27."),
    dict(deck=HAND, img="m8_06a_hand_palmar.jpg",
         ver="lab manual p.179 ('the head of each bone is readily seen and felt at the distal ends (also known as the \"knuckles\")'); study guide p.1 ('Metacarpal heads = knuckles')",
         text="The knuckles are the {{c1::heads of the metacarpals}}.",
         back="Why: each metacarpal ends in a rounded head that pushes up under the skin when "
              "you make a fist."),
    dict(deck=HAND, img="m8_06a_hand_palmar.jpg",
         ver="lab manual p.179 ('The lines you might see on the dorsum side of the hand are not the metacarpal bones but are tendons of the extensor muscles'); study guide p.1",
         text="The lines you see on the back of your hand are {{c1::extensor tendons}}, not "
              "metacarpals.",
         back="Why: the metacarpals lie deeper and are felt rather than seen; the tendons that "
              "straighten the fingers ride just under the skin."),
    dict(deck=HAND, img="m8_06a_hand_palmar.jpg",
         ver="lab recording 9/30 [38:43]-[39:34] (Dr. Blais: 'These metacarpals are curved. They form the palm ... the curvature is always going to be concave in the front')",
         text="The metacarpals arch so that the palm is {{c1::concave (cupped)}} on its "
              "anterior (palm) side.",
         back="Why: the arched metacarpals cup the palm around what you grip, so the hollow "
              "side is always the palm.<br><br>Cue: hold a loose hand like your own, cupped "
              "palm facing forward and away from you; if its thumb points to your right, it "
              "is a right hand."),

    # =================================== PELVIC GIRDLE ===================================
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="lab recording 9/30 [40:27] ('This is where the lower extremities attach to the axial skeleton'); lab manual p.173",
         text="The pelvic girdle attaches the {{c1::lower limbs}} to the axial skeleton.",
         back="Why: each os coxae meets the sacrum in back and holds the femur's head in the "
              "acetabulum, so body weight passes from the spine to the legs through it."),
    dict(deck=PELVIS, img="s08_coxal_netter.png",
         ver="slide 8 ('The os coxae is formed by the fusion of three bones: the ilium, ischium, and pubis'); lab recording 9/30 [40:27]; lab manual p.173",
         text="Each os coxae (hip bone) forms from the fusion of three bones: the "
              "{{c1::ilium}}, {{c1::ischium}}, and {{c1::pubis}}.",
         back="Why: the three are separate bones in a child and fuse around the acetabulum by "
              "adulthood, which is why all three share the hip socket."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab manual p.173 ('The iliac bones are the largest of the 3 bones that form the os coxae'); lab recording 9/30 [41:17] ('the ilium is going to be the superior portion'); study guide p.2",
         text="The {{c1::ilium}} is the largest of the three hip bones and forms the superior "
              "part of the os coxae.",
         back="Why: the ilium's broad, flared wing (ala) supports the abdominal organs and anchors "
              "the large hip and abdominal muscles."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab manual p.173 ('The ischial bones form the posteroinferior portion of the pelvis'); study guide p.2; lab recording 9/30 [41:17] ('The ischium is going to be posterior')",
         text="The {{c1::ischium}} forms the posteroinferior part of the os coxae.",
         back="Why: the ischium is the part you sit on, behind and below the hip socket."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab recording 9/30 [41:17] ('we know that the pubis is going to be anterior'); lab manual p.173",
         text="The {{c1::pubis}} forms the anterior part of the os coxae.",
         back="Why: the two pubic bones curve forward and meet each other at the midline in "
              "front, at the pubic symphysis."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab manual p.173 ('All three bones of the os coxae contribute to the formation of the acetabulum'); study guide p.2",
         text="All three bones of the os coxae (ilium, ischium, pubis) contribute to the "
              "{{c1::acetabulum}}.",
         back="Why: the three bones meet and fuse at the hip socket, so the cup is part ilium, "
              "part ischium, and part pubis."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="slide 8 ('Acetabulum is directed laterally') + notes ('Acetabulum is always facing laterally'); lab recording 9/30 [42:55] + [45:24] (Dr. Blais: 'it is lateral but it's also external')",
         text="The acetabulum always faces {{c1::laterally::direction}}.",
         back="Why: the acetabulum is the socket for the head of the femur, and the thigh hangs from the "
              "outside of the pelvis.<br><br>Cue: Dr. Blais prefers 'external'; the inner face "
              "of the hip bone is smooth, with no acetabulum."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="slide 8 notes ('articulates with the head of the femur'); lab recording 9/30 [42:55] ('That is where the femur will articulate'); lab manual p.173 ('accommodates the head of the femur and forms the hip joint')",
         text="The acetabulum is the socket for the {{c1::head of the femur}}, forming the hip "
              "joint.",
         back="Why: a deep cup around a ball makes a ball-and-socket joint that is far more "
              "stable than the shallow shoulder."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="slide 8 notes ('Pubic Symphysis is the articulation between left and right pubic bones'); lab recording 9/30 [44:34] ('a little bit of a cartilaginous bit'); lab manual p.173 ('articulate directly with each other only in the front')",
         text="The two os coxae articulate directly with each other only in front, at the "
              "{{c1::pubic symphysis::joint}}.",
         back="Why: a pad of fibrocartilage joins the two pubic bones at the midline, allowing "
              "only slight movement.<br><br>Cue: in back, each os coxae meets the sacrum "
              "instead of the other hip bone."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual Fig 8-8 ('auricular surface*' — '*articulating surfaces for sacrum'); study guide p.2 ('Auricular surface meets the sacrum')",
         text="Each os coxae articulates with the {{c1::sacrum}} at the ilium's "
              "{{c2::auricular surface}}.",
         back="Why: auricular means 'ear-shaped'; this ear-shaped rough patch on the inner "
              "ilium forms the sacroiliac joint."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.173 ('The posterior wall of the pelvic girdle is formed by the sacrum and coccyx of the axial skeleton; the lateral and anterior portions are formed by the coxal bones'); study guide p.2",
         text="The pelvic girdle mixes axial and appendicular bones: its posterior wall is the "
              "{{c1::sacrum and coccyx}} (axial), and its sides and front are the {{c2::two os "
              "coxae}} (appendicular).",
         back="Why: the sacrum is part of the vertebral column, wedged between the two hip "
              "bones like a keystone."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="slide 8 notes ('The \"hip bone\" that you can feel is the anterior superior iliac spine'); lab recording 9/30 [42:04]; lab manual p.175; study guide p.2 ('ASIS is a visible anterior bump')",
         text="The bony 'hip bone' you feel at the front of your hips is the {{c1::anterior "
              "superior iliac spine (ASIS)}}.",
         back="Why: the ASIS is the front end of the iliac crest and lies right under the skin, "
              "which also makes it the landmark for measuring the Q angle."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="lab manual p.179 ('The crest terminates anteriorly with the anterior superior iliac spine ... with the posterior superior iliac spines'); study guide p.2",
         text="The iliac crest ends anteriorly at the {{c1::ASIS}} and posteriorly at the "
              "{{c2::PSIS}}.",
         back="Why: 'spine' marks each pointed end of the crest, and just below each superior "
              "spine sits an inferior one (AIIS, PIIS)."),
    dict(deck=PELVIS, img="s10_hip_medial.png",
         ver="study guide p.2 ('Four spines: ASIS, AIIS, PSIS, PIIS'); slides 9-10 (all four boxed); lab recording 9/30 [49:31]",
         text="The ilium has four spines: the {{c1::anterior superior}}, {{c1::anterior "
              "inferior}}, {{c1::posterior superior}}, and {{c1::posterior inferior}} iliac "
              "spines.",
         back="Why: the crest ends in a superior spine at each end, with an inferior spine "
              "just below it: two in front, two behind.<br><br>Cue: ASIS, AIIS, PSIS, PIIS."),
    dict(deck=PELVIS, img="m8_10_gluteal.jpg",
         ver="lab manual p.175 ('the posterior superior iliac spines are seen as dimples on either side of the sacrum'); study guide p.2 ('PSIS = dimples beside the sacrum'); lab manual Fig 8-10",
         text="The PSIS shows on the lower back as {{c1::dimples}} on either side of the "
              "sacrum.",
         back="Why: the skin is anchored down to the bone over the posterior superior iliac "
              "spines, so it dimples inward there."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="lab manual p.173 ('the long ridge - the iliac crest - that extends along the superior border') + p.179 ('where you commonly place your hands'); study guide p.2 ('Crest = hands-on-hips ridge'); lab recording 9/30 [44:34] (Dr. Blais)",
         text="The long ridge along the top of the ilium, where you rest your hands on your "
              "hips, is the {{c1::iliac crest}}.",
         back="Why: the crest is the thick upper border of the ilium, running from the ASIS in front "
              "to the PSIS behind."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="lab recording 9/30 [45:24] (Dr. Blais: 'it's rough and bone anytime you have rough and bone that means something's going to attach and all your abdominal muscles they attach in that area')",
         text="The iliac crest feels rough because the {{c1::abdominal muscles}} attach along "
              "it.",
         back="Why: tendons pull on bone where they anchor, and the bone responds by building "
              "a roughened ridge; rough bone always means an attachment."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="slide 8 ('ischial spine points posteriorly'); lab recording 9/30 [42:04]",
         text="The ischial spine points {{c1::posteriorly}}.",
         back="Why: the ischial spine juts backward between the greater and lesser sciatic notches, on the "
              "back edge of the hip bone.<br><br>Cue: a 'spine' is a sharp, slender "
              "projection."),
    dict(deck=PELVIS, img="s09_hip_lateral.png",
         ver="lab recording 9/30 [46:13]-[47:02] (Dr. Blais: 'there's a big groove right here and there's a little one here. That's always facing posterior'); slides 9-10",
         text="The greater and lesser sciatic notches are on the {{c1::posterior}} edge of "
              "the hip bone.",
         back="Why: the two notches cut into the back edge of the bone above and below the ischial spine, "
              "which is how Dr. Blais finds 'posterior' on a loose hip bone."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab manual p.175 ('The greater sciatic notch provides a route for the sciatic nerve and blood vessels to pass into the leg'); study guide p.2",
         text="The greater sciatic notch lets the {{c1::sciatic nerve}} (and blood vessels) "
              "pass into the leg.",
         back="Why: the greater sciatic notch is the big gap between the ilium and the ischial spine; the lesser "
              "notch below the spine passes smaller nerves and vessels."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="lab manual p.173 ('The ischial and pubis bones form a large opening called the obturator foramen'); study guide p.2",
         text="The obturator foramen is the large hole in the os coxae, enclosed by the "
              "{{c1::ischium and pubis}}.",
         back="Why: the ischium and pubis loop around it; in life a membrane covers most of "
              "it, leaving a small canal for a nerve and vessels."),
    dict(deck=PELVIS, side="front", img="lr_hip_lateral.jpg",
         ver="lab manual Fig 8-7 'The Right Hip Bones', lateral view (labels erased); lab recording 9/30 [46:13]-[47:50] (Dr. Blais's orientation recipe)",
         text="A hip bone seen from its outer (lateral) side: is it a right or a left os "
              "coxae? {{c1::right::side}}",
         back="Why: crest up, obturator foramen down, acetabulum facing you (lateral view). "
              "The sciatic notches mark the back and sit on the picture's left, so the front "
              "(ASIS) points to your right: that is a right hip bone seen from outside."
              "<br><br>Cue: Dr. Blais's recipe: crest superior, obturator foramen inferior, "
              "acetabulum lateral, sciatic notches posterior."),
    dict(deck=PELVIS, img="s10_hip_medial.png",
         ver="lab recording 9/30 [43:42] ('if we look on the medial side, it's just a smooth surface, we don't see an acetabulum there') + [47:02] (Dr. Blais); slide 10 (Iliac fossa boxed)",
         text="The inner (medial) face of the hip bone is smooth, with the shallow "
              "{{c1::iliac fossa}} above and no acetabulum.",
         back="Why: the iliac fossa is the smooth hollow on the inside of the ilium's wing "
              "that cradles the abdominal organs and anchors the iliacus muscle."),
    dict(deck=PELVIS, img="s10_hip_medial.png",
         ver="slide 8 notes ('Pubic tubercle faces anteriorly')",
         text="The pubic tubercle faces {{c1::anteriorly}}.",
         back="Why: the pubic tubercle is the small knob on the front of the pubis near the midline, where the "
              "inguinal ligament anchors."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.175 ('The inguinal ligament, which connects the anterior superior iliac spine to the pubic crest'); study guide p.2; lab manual Fig 8-8",
         text="The {{c1::inguinal ligament}} stretches from the ASIS to the pubis, marking the "
              "crease of the groin.",
         back="Why: the inguinal ligament is the rolled lower edge of an abdominal muscle's sheet, tacked between "
              "two bony points.<br><br>Pitfall: the manual says it ends at the pubic crest; most "
              "anatomy texts say the pubic tubercle, just beside it."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.173 ('The pubic crest above this joint is easily felt on men but is usually more difficult to feel on women because of a fat pad (the mons pubis)'); study guide p.2",
         text="The {{c1::pubic crest}} is the ridge you can feel just above the pubic "
              "symphysis.",
         back="Why: the pubic crest is the upper border of the pubic bones and is harder to feel on women "
              "because of the fat pad (mons pubis) over it."),
    dict(deck=PELVIS, img="m8_07_hip_lateral.jpg",
         ver="study guide p.2 ('Ischial tuberosity takes sitting weight'); lab manual p.173 ('The rami of the ischial bones support your body weight while you sit and have thus been nick-named the \"sitz bones\"')",
         text="When you sit, your weight rests on the {{c1::ischial tuberosities}}.",
         back="Why: the ischial tuberosities are the thick, rough lower ends of the ischium, padded by the "
              "buttocks.<br><br>Pitfall: the manual credits the ischial RAMI and calls them "
              "the 'sitz bones'; most texts say the weight rests on the tuberosities."),
    dict(deck=PELVIS, img="m8_10_gluteal.jpg",
         ver="lab manual p.175 ('The ischial rami is best felt by pressing hard against the buttocks at the level of the gluteal fold') + p.179",
         text="The ischial ramus can be felt by pressing on the buttocks at the level of the "
              "{{c1::gluteal fold}}.",
         back="Why: the gluteus muscles thin out at the fold under the buttock, so the bone "
              "lies close enough to feel, especially with the muscles relaxed."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.173 ('The pelvic brim (or pelvic inlet) is formed by the sacral promontory posteriorly and the arcuate lines of the ilia anterolaterally'); study guide p.2",
         text="The pelvic brim (pelvic inlet) is formed by the {{c1::sacral promontory}} "
              "behind and the {{c2::arcuate lines}} of the ilia at the sides.",
         back="Why: the pelvic brim is the doorway into the true pelvis below, the opening a baby's "
              "head must pass through."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.173-175 ('The pelvic brim is considerably wider in women ... the entire pelvis is wider and shorter in women'); study guide p.2",
         text="The pelvic brim is much {{c1::wider}} in women than in men.",
         back="Why: a wider inlet eases the passage of the baby during childbirth; the whole "
              "female pelvis is also wider and shorter, which makes the hips the widest part "
              "of the female body."),
    dict(deck=PELVIS, img="m8_08_hip_medial.jpg",
         ver="lab manual p.173 ('The pelvis surrounds and protects the organs of the pelvic cavity and supports the organs of the abdominal cavity')",
         text="The pelvis surrounds and protects the organs of the {{c1::pelvic cavity}} and "
              "supports those of the abdominal cavity.",
         back="Why: the bony basin wraps the bladder and reproductive organs, and its flared "
              "iliac wings hold up the intestines above them."),
    dict(deck=PELVIS, img="m8_10_gluteal.jpg",
         ver="lab manual p.175 ('Anatomically, the gluteal region belongs to the body trunk; physiologically, the gluteal region belongs to the lower limbs')",
         text="Anatomically the gluteal region belongs to the {{c1::trunk}}; physiologically "
              "it belongs to the {{c2::lower limb}}.",
         back="Why: the gluteal region lies over the pelvis, but its muscles (the glutes) move the thigh."),
    dict(deck=PELVIS, img="m8_10_gluteal.jpg",
         ver="lab manual p.175 ('The coccyx can be felt immediately superior to the anus'); study guide p.2",
         text="The coccyx can be felt just {{c1::above (superior to) the anus}}.",
         back="Why: the tailbone curves forward at the bottom of the sacrum, in the cleft "
              "between the buttocks."),
    dict(deck=PELVIS, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 19 (no instructor key for appendicular pins)",
         text="Skeleton seen from the front: name the bone at pin 19. {{c1::os coxae "
              "(ilium)::bone}}",
         back="Why: the pin sits on the broad upper wing of the hip bone, the ilium part of "
              "the os coxae."),

    # =================================== THIGH & LEG ===================================
    dict(deck=LEG, img="s11_femur.png",
         ver="lab recording 9/30 [51:54] ('it is a very big bone the biggest bone in our body it is what makes up our thigh'); lab manual p.175 ('the largest and heaviest bone of the body'); study guide p.2",
         text="The femur, the thigh's only bone, is the {{c1::largest (and heaviest)::size}} bone in "
              "the body.",
         back="Why: the femur carries the body's weight from the hip to the knee and anchors the "
              "powerful thigh muscles."),
    dict(deck=LEG, img="s11_femur.png",
         ver="slide 11 ('Head is directed medially') + notes ('Head of the femur articulates with the acetabulum'); lab recording 9/30 [51:54]-[52:41]",
         text="The head of the femur points {{c1::medially}}, into the acetabulum.",
         back="Why: the ball has to reach the hip socket, which lies medial to the thigh; it "
              "is the same rule as the humerus's head at the shoulder."),
    dict(deck=LEG, img="m8_09_femur_patella.jpg",
         ver="slide 11 figure ('Fovea capitis'); study guide p.2 ('fovea capitis on the head is a ligament attachment'); lab manual Fig 8-9",
         text="The small pit on the head of the femur, the {{c1::fovea capitis}}, is where a "
              "ligament attaches.",
         back="Why: fovea means small pit; the ligament of the head of the femur runs from "
              "here to the acetabulum and carries a small artery to the head."),
    dict(deck=LEG, num=True, img="m8_09_femur_patella.jpg",
         ver="lab manual p.175 ('The rather long neck of the femur angles medially about 125 degrees (the angle of inclination)'); study guide p.2",
         text="The femur's neck angles medially about {{c1::125::degrees}}° from the shaft (the "
              "angle of inclination).",
         back="Why: the angle brings the knees in under the body even though the hip sockets "
              "are far apart, and it is why the femur isn't parallel to the tibia (the Q "
              "angle)."),
    dict(deck=LEG, img="s11_femur.png",
         ver="slide 11 ('greater trochanter is directed laterally'); lab recording 9/30 [56:42]",
         text="The greater trochanter is on the {{c1::lateral}} side of the proximal femur.",
         back="Why: the greater trochanter is the big bump at the side of the hip, where the thigh's abductor "
              "muscles pull."),
    dict(deck=LEG, img="m8_09_femur_patella.jpg",
         ver="lab manual p.176 ('The greater trochanter ... serves as an attachment site for powerful muscles that abduct the thigh'); study guide p.2 ('Greater = abductors')",
         text="The greater trochanter anchors muscles that {{c1::abduct}} the thigh.",
         back="Why: muscles pulling on the outside of the femur swing the thigh out to the "
              "side (abduction)."),
    dict(deck=LEG, img="s11_femur.png",
         ver="lab recording 9/30 [52:41] ('the lesser trochanter is going to be ... more on the posterior medial side'); slide 11 figure",
         text="The lesser trochanter is on the {{c1::posteromedial}} side of the proximal "
              "femur.",
         back="Why: the lesser trochanter faces back and in, just below the neck, where the main hip flexor "
              "(iliopsoas) pulls."),
    dict(deck=LEG, img="m8_09_femur_patella.jpg",
         ver="lab manual p.176 ('Muscles that adduct and flex the thigh attach to the lesser trochanter'); study guide p.2 ('Lesser = adductors and flexors')",
         text="The lesser trochanter anchors muscles that {{c1::flex and adduct}} the thigh.",
         back="Why: on the inner side of the femur, a pull there draws the thigh forward (flex) "
              "and inward (adduct)."),
    dict(deck=LEG, img="s11_femur.png",
         ver="slide 11 notes ('Linea aspera is on posterior surface of femur'); lab recording 9/30 [52:41]-[53:32]; study guide p.2",
         text="The linea aspera is a rough ridge running down the {{c1::posterior}} shaft of "
              "the femur.",
         back="Why: linea aspera means 'rough line'; the thigh's adductor muscles attach along "
              "it, building the ridge up the back of the shaft."),
    dict(deck=LEG, img="s11_femur.png",
         ver="lab recording 9/30 [53:32] ('the anterior portion of the femur is going to be a rounded edge, whereas the posterior shaft of the femur is going to be pointed') + [63:04] ('it's a little opposite than that, than the femur')",
         text="The femur's pointed ridge (the linea aspera) faces {{c1::posteriorly::direction}}, "
              "but the tibia's sharp ridge (the shin) faces {{c2::anteriorly::direction}}.",
         back="Why: the femur's ridge anchors muscles on the back of the thigh, while the "
              "tibia's sharp anterior border is the bare bone of the shin."),
    dict(deck=LEG, img="s11_femur.png",
         ver="slide 11 ('The intercondylar fossa is located posteriorly') + notes ('Intercondylar fossa is on distal portion of posterior femur'); lab recording 9/30 [53:32]-[54:22]",
         text="The intercondylar fossa is on the {{c1::posterior}} distal femur, between the "
              "medial and lateral condyles.",
         back="Why: the deep notch between the condyles houses the knee's cruciate ligaments "
              "and opens toward the back."),
    dict(deck=LEG, img="s11_femur.png",
         ver="slide 11 ('patellar surface is anterior') + notes ('Patellar surface is on distal anterior surface'); lab recording 9/30 [55:07]",
         text="The patellar surface is on the {{c1::anterior}} distal femur.",
         back="Why: the patellar surface is the shallow groove the kneecap glides in, at the front of the knee."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('the large medial and lateral condyles articulate with the tibia bone'); study guide p.2 ('Distal condyles meet the tibia')",
         text="The femur's medial and lateral {{c1::condyles}} articulate with the tibia.",
         back="Why: the two rounded knuckles at the bottom of the femur roll on the flat tops "
              "of the tibia's condyles to form the knee."),
    dict(deck=LEG, img="m8_09_femur_patella.jpg",
         ver="lab manual p.176 ('The lateral and medial epicondyles can be felt high on either side of the knee') + p.180 ('best felt with the knee fully flexed'); study guide p.2",
         text="The femur's epicondyles can be felt high on each side of the knee, best with "
              "the knee {{c1::flexed}}.",
         back="Why: bending the knee pulls the kneecap and tendons out of the way and stretches "
              "the skin over the bony sides of the knee."),
    dict(deck=LEG, img="m8_09_femur_patella.jpg",
         ver="lab manual p.179-180 ('Only the ends of the femur can be palpated. Proximally, the greater trochanter ... Distally, the two condyles'); study guide p.2 ('easier if you swing the leg')",
         text="Only the {{c1::ends::which part}} of the femur can be felt: the greater trochanter at the "
              "hip and the condyles and epicondyles at the knee.",
         back="Why: the thick thigh muscles bury the shaft.<br><br>Cue: to find the greater "
              "trochanter, press on the side of the hip while swinging the leg front to "
              "back."),
    dict(deck=LEG, side="front", img="lr_femur_posterior.jpg",
         ver="lab manual Fig 8-9 'Left Femur & Patella', posterior view (labels erased)",
         text="A femur seen from behind (posterior view): is it a right or a left femur? "
              "{{c1::left::side}}",
         back="Why: the head points medially, here toward the picture's right. Seen from "
              "behind, a medial side on your right means the body's left side.<br><br>Cue: the "
              "linea aspera and intercondylar fossa show only from the back."),
    dict(deck=LEG, side="front", img="pp3_lower_pins.png",
         ver="Popcorn Points slide 3, pin 22 (no instructor key for appendicular pins)",
         text="Skeleton seen from the front: name the bone at pin 22. {{c1::femur::bone}}",
         back="Why: the femur is the thigh's single bone, running from the hip socket to the knee."),
    dict(deck=LEG, tags=["optional"], img="s11_femur.png",
         ver="study guide p.2 ('Intertrochanteric line/crest connect them'); slide 11 notes ('You do NOT need to know the intertrochanteric line, intertrochanteric crest')",
         text="The intertrochanteric {{c1::line}} runs across the front of the femur and the "
              "intertrochanteric {{c1::crest}} across the back, both between the two "
              "trochanters.",
         back="Why: inter- means between; both mark where hip ligaments and muscles attach "
              "between the greater and lesser trochanters.<br><br>Pitfall: the slide 11 notes "
              "say you do NOT need these two."),
    dict(deck=LEG, img="m8_11_q_carrying.jpg",
         ver="study guide p.2 ('Angle between ASIS → mid-patella and tibial tuberosity → mid-patella'); lab manual p.181 (Activity 5)",
         text="The Q angle is the angle between a line from the {{c1::ASIS}} to the middle of "
              "the patella and a line from the {{c2::tibial tuberosity}} to the middle of the "
              "patella.",
         back="Why: the Q angle measures how far the thigh slants inward from hip to knee compared "
              "with the straight line of the lower leg."),
    dict(deck=LEG, num=True, img="m8_11_q_carrying.jpg",
         ver="lab manual p.181 ('It should be about 8-10 degrees on males and 10-15 degrees on females') + p.175 ('usually larger on women due to the wider hip bones'); study guide p.2",
         text="A normal Q angle is about {{c1::8–10::degrees}}° in males and "
              "{{c2::10–15::degrees}}° in females.",
         back="Why: wider hips set a woman's femurs at a steeper inward slant, which widens "
              "the angle at the knee."),
    dict(deck=LEG, img="m8_11_q_carrying.jpg",
         ver="lab manual p.175 ('The point of the Q angle is to bring the knees closer together to return the center of body mass directly under the trunk'); study guide p.2",
         text="The Q angle's purpose is to bring the knees {{c1::closer together}}, putting "
              "the body's center of mass under the trunk.",
         back="Why: the hip sockets are wide apart, so slanting the femurs inward sets the "
              "knees and feet under the body's midline for balance."),
    dict(deck=LEG, img="m8_16_q_measure.jpg",
         ver="lab manual p.181 (Activity 5 steps 1-5: 'lying down is preferred', 'Place the fulcrum of the goniometer on the patella and align the stationary arm with the tibial tuberosity', 'Align the rotating arm with the ASIS'); study guide p.2",
         text="To measure the Q angle, set the goniometer's fulcrum on the {{c1::patella}}, "
              "its stationary arm along the {{c2::tibial tuberosity}}, and its moving arm "
              "toward the {{c3::ASIS}}.",
         back="Why: the angle sits at the knee, between the lower leg's line (to the tibial "
              "tuberosity) and the thigh's line (up to the hip).<br><br>Cue: lying supine is "
              "preferred, with the subject keeping a finger on the ASIS."),
    dict(deck=LEG, img="m8_16_q_measure.jpg",
         ver="lab manual p.175 ('The Q angle can be measured using a goniometer, which is more commonly used to measure joint range-of-motion'); slide 15 ('Use a goniometer to measure Q angle')",
         text="The Q angle is measured with a {{c1::goniometer}}, a tool usually used for "
              "joint range of motion.",
         back="Why: a goniometer is a protractor with two arms hinged at a fulcrum, so it "
              "reads the angle between two body segments."),
    dict(deck=LEG, img="s12_patella.png",
         ver="slide 12 ('The apex is the inferior most feature') + notes ('Apex points inferiorly'); lab recording 9/30 [58:20]-[59:07] ('like an upside down pyramid')",
         text="The patella's pointed {{c1::apex}} is its inferior end, and its broad "
              "{{c1::base}} is superior.",
         back="Why: the patella is an upside-down triangle: wide at the top where the "
              "quadriceps tendon attaches, narrowing to the point the patellar ligament hangs "
              "from.<br><br>Pitfall: 'base' sounds like the bottom, but on the patella the "
              "base is the TOP."),
    dict(deck=LEG, img="s12_patella.png",
         ver="slide 12 figure ('Articular surface', posterior view); lab recording 9/30 [59:07]-[59:52] ('The posterior view is going to be a little bit more smoother ... This is where it sits on the patellar surface of the femur')",
         text="The patella's smooth {{c1::articular surface}} is on its {{c2::posterior}} "
              "side, gliding on the femur's patellar surface.",
         back="Why: the back of the kneecap is smooth and flatter where it faces the femur; "
              "the front, which you feel through the skin, is rounded and rough."),
    dict(deck=LEG, img="s12_patella.png",
         ver="slide 12 ('Posterior medial facet is smaller than lateral facet')",
         text="On the back of the patella, the {{c1::lateral}} facet is larger than the medial "
              "facet.",
         back="Why: the lateral side of the femur's patellar groove is broader and higher, so "
              "the patella's matching lateral facet is bigger too."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('One function of the patella is to increase the leverage arm of the quadriceps'; 'tracks up-and-down'); study guide p.2 ('lengthens the quads’ lever arm')",
         text="The patella increases the leverage of the {{c1::quadriceps}} muscle.",
         back="Why: set inside the tendon in front of the knee, it holds the tendon away from "
              "the joint's pivot, lengthening the lever arm; it also tracks up and down as the "
              "knee bends and straightens."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="lab manual p.176 ('The leg, defined anatomically as the region between the knee and the ankle, contains two bones'); slide 13",
         text="Anatomically, the leg is only the segment between the knee and the ankle; its "
              "two bones are the {{c1::tibia}} and the {{c1::fibula}}.",
         back="Why: the thigh (femur) and the leg are separate segments in anatomy, just as "
              "the arm and the forearm are."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="slide 13 ('Fibula is lateral while the tibia is medial') + notes ('the ”la” in fibula can remind you that it is lateral'); lab recording 9/30 [61:26]-[62:15]",
         text="In the leg, the {{c1::tibia}} is medial and the {{c1::fibula}} is lateral.",
         back="Why: the big tibia sits under the femur in line with the knee, and the slim "
              "fibula runs along its outer side.<br><br>Mnemonic: the 'la' in fibula = "
              "LAteral."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('The tibia is the larger of the two bones and transfers body weight from the femur to the ankle and foot. The smaller fibula serves as an anchor for muscles'); study guide p.2",
         text="The {{c1::tibia}} carries the body's weight from the femur to the ankle; the "
              "fibula mainly anchors muscles.",
         back="Why: the thick tibia sits right under the femur, while the slim fibula runs "
              "alongside as an anchor for the muscles that move the foot and toes."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab recording 9/30 [62:15] ('the tibia is the primary articulating bone for the femur'); lab manual p.176",
         text="At the knee, the femur articulates with the {{c1::tibia}}; the fibula is not "
              "part of the knee joint.",
         back="Why: the fibula's head sits against the side of the tibia below its lateral "
              "condyle, out of the femur's reach."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="slide 13 ('Tibial tuberosity is anterior') + notes; lab recording 9/30 [60:38]-[61:26] ('You can kind of feel that at almost near the top of your shins')",
         text="The tibial tuberosity is on the {{c1::anterior}} tibia, just below the knee.",
         back="Why: the tibial tuberosity is the bump you can feel at the top of your shin, below the kneecap."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('the large tibial tuberosity serves as an attachment site for powerful thigh muscles that extend the leg (e.g., when kicking a football)'); study guide p.2 ('Tibial tuberosity = patellar tendon (kicking)')",
         text="The tibial tuberosity anchors the {{c1::quadriceps}} (through the patellar "
              "ligament), the muscles that straighten the knee when you kick a ball.",
         back="Why: the quadriceps tendon wraps the patella and continues as the patellar "
              "ligament to the tuberosity, so the pull that straightens the knee lands "
              "there."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.177 ('The anterior margin of the tibia (i.e., the \"shin bone\") can be felt all the way down the front of the leg'); study guide p.2 ('Anterior margin = shin'); lab recording 9/30 [63:04]",
         text="The shin is the {{c1::anterior margin (border)}} of the tibia.",
         back="Why: the tibia's front edge lies just under the skin for the whole length of the "
              "leg, which is why a knock to the shin hurts so much."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="slide 13 ('Fibular malleolus is lateral while Tibial malleolus is medial') + notes; lab recording 9/30 [63:52]-[64:38]; lab manual p.176",
         text="The medial malleolus is the lower end of the {{c1::tibia}}; the lateral "
              "malleolus is the lower end of the {{c1::fibula}}.",
         back="Why: the two ankle bumps are the ends of the leg bones hugging the talus from "
              "each side.<br><br>Pitfall: people call them 'ankle bones', but they belong to "
              "the leg; the true ankle bones are the tarsals."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="lab manual p.176 ('The lateral malleolus is lower than the medial malleolus'); study guide p.2; lab recording 9/30 [63:52] ('it's going to extend actually further than the tibia')",
         text="The lateral malleolus sits {{c1::lower (more inferior)}} than the medial "
              "malleolus.",
         back="Why: the fibula reaches farther down than the tibia, so the outer ankle bump is "
              "the lower one, a quick way to side a leg."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('The head of the fibula articulates with the tibia laterally just beneath the lateral condyle of the tibia at the proximal tibiofibular joint'); study guide p.2",
         text="The head of the fibula articulates with the tibia just below the tibia's "
              "{{c1::lateral condyle}} (the proximal tibiofibular joint).",
         back="Why: the fibula's upper end tucks against the outside of the tibia, below the "
              "knee joint itself."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.177 ('The head of the fibula can be felt (and seen) as a small bump on the lateral side of the leg in the same plane as the tibial tuberosity') + p.180; study guide p.2",
         text="The head of the fibula can be felt as a small bump on the {{c1::lateral}} side "
              "of the leg, level with the tibial tuberosity.",
         back="Why: find the tibial tuberosity, then slide your hand around to the outside of "
              "the leg at the same height."),
    dict(deck=LEG, img="m8_12_leg_foot.jpg",
         ver="lab manual p.176 ('Between the malleoli, the two bones articulate again at the distal tibiofibular joint')",
         text="Just above the ankle, the tibia and fibula articulate again at the {{c1::distal "
              "tibiofibular}} joint.",
         back="Why: the fibula meets the tibia twice, once below the knee (proximal "
              "tibiofibular joint) and once above the ankle."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="lab recording 9/30 [62:15] ('the lateral condyle is not the most lateral structure within the distal leg, but it is the most lateral structure of the tibia')",
         text="The tibia's lateral condyle is not the most lateral part of the leg; the "
              "{{c1::head of the fibula}} lies farther out.",
         back="Why: the fibula runs along the outside of the tibia, with its head tucked under "
              "the lateral condyle."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="slide 13 notes ('“Sharp” surface of Fibula faces anteriorly')",
         text="The sharp edge of the fibula's shaft faces {{c1::anteriorly}}.",
         back="Why: like the tibia, the fibula's shaft is roughly triangular in cross-section, "
              "with its sharpest border pointing forward."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="lab recording 9/30 [60:38] ('The fibula looks almost like a pencil') + [71:00] (Dr. Blais: 'I try to think of it like an arrow')",
         text="The long, thin leg bone that looks like a pencil (or an arrow) is the "
              "{{c1::fibula}}.",
         back="Why: the fibula is the slimmest of the long bones, a thin shaft with a small knob at "
              "each end, easy to confuse with the radius and ulna until you check the ends."),
    dict(deck=LEG, side="front", img="lr_tibia_fibula.png",
         ver="slide 13 figure, anterior view of a right tibia and fibula (labels erased); slide 13 notes ('How to distinguish right vs left?')",
         text="A tibia and fibula seen from the front: is this a right or a left leg? "
              "{{c1::right::side}}",
         back="Why: the thin fibula is on the picture's left, and the fibula is lateral. Seen "
              "from the front, lateral on your left means the body's right leg.<br><br>Cue: the "
              "tibial tuberosity faces you (anterior), and the medial malleolus is on the "
              "tibia's side."),
    dict(deck=LEG, img="s13_tibia_fibula.png",
         ver="lab manual p.176-177 ('your legs appear to make a triangle (apex up), but the bones actually form a rectangle ... With the legs closed, however, both the flesh of the legs and the bones make a triangle with the apex down'); study guide p.2",
         text="Standing with feet apart, your legs look like an apex-up triangle but the bones "
              "form a {{c1::rectangle}}; with feet together, flesh and bones both make an "
              "apex-{{c2::down::up or down}} triangle.",
         back="Why: the femurs slant inward toward the knees, so with the feet apart the leg "
              "bones stand nearly vertical and stable; with the feet together they meet "
              "below, which is harder to balance on."),

    # =================================== ANKLE & FOOT ===================================
    dict(deck=FOOT, num=True, img="s14_foot.png",
         ver="slide 2 ('Tarsals (14)'); lab manual p.177 ('There are seven ankle (or tarsal) bones')",
         text="Each ankle has {{c1::7::number}} tarsal bones (14 in the body).",
         back="Why: 2 in the hindfoot (talus, calcaneus) + 5 in the midfoot (navicular, 3 "
              "cuneiforms, cuboid) = 7."),
    dict(deck=FOOT, img="s14_foot.png",
         ver="slide 14 (Tarsals list + 'Mnemonic: The Circus Needs More Interesting Little Clowns') + notes ('Start on proximal portion of foot at talus ... Move laterally towards little toe'); lab recording 9/30 [66:11]-[67:00]",
         text="Tarsals in mnemonic order: The = {{c1::talus}}, Circus = {{c2::calcaneus}}, "
              "Needs = {{c3::navicular}}, More Interesting Little = {{c4::medial, intermediate, "
              "and lateral cuneiforms}}, Clowns = {{c5::cuboid}}.",
         back="Why: start at the talus on top, drop to the calcaneus, run forward and "
              "medially to the navicular and the three cuneiforms (toward the big toe), then "
              "finish laterally at the cuboid (toward the little toe)."),
    dict(deck=FOOT, img="m8_12_leg_foot.jpg",
         ver="lab manual p.177 ('The tibia in the leg rests upon the talus, which in turn rests upon the calcaneus'); lab recording 9/30 [66:11] ('The one here at the top that goes into the ankle is called the talus')",
         text="The tibia rests on the {{c1::talus}}, which rests on the {{c2::calcaneus}}.",
         back="Why: the talus, clamped between the two malleoli, forms the ankle joint and "
              "hands the body's weight down to the heel bone."),
    dict(deck=FOOT, img="m8_12_leg_foot.jpg",
         ver="lab recording 9/30 [66:11] ('The one that is our heel bone is called the calcaneus'); lab manual p.178 ('The calcaneus forms the bulk of your heel'); study guide p.2",
         text="The heel bone, the largest tarsal, is the {{c1::calcaneus}}.",
         back="Why: the calcaneus takes the full impact of each heel strike and anchors the Achilles "
              "tendon."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('The talus and calcaneus constitute the hindfoot') + Fig 8-13; lab recording 9/30 [66:11] ('they make up the rear foot'); study guide p.2",
         text="The hindfoot is made of the {{c1::talus}} and the {{c1::calcaneus}}.",
         back="Why: the talus and calcaneus carry the leg's weight down to the heel, at the back of the "
              "foot."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('These five tarsal bones constitute the midfoot') + Fig 8-13; study guide p.2",
         text="The midfoot is made of the {{c1::navicular}}, the {{c1::three cuneiforms}}, "
              "and the {{c1::cuboid}}.",
         back="Why: the five midfoot tarsals sit in front of the hindfoot and link the talus and "
              "calcaneus to the metatarsals."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual Fig 8-13 (forefoot / midfoot / hindfoot); study guide p.2 ('Forefoot: 5 metatarsals + 14 phalanges')",
         text="The forefoot is made of the {{c1::metatarsals}} and the {{c1::phalanges}}.",
         back="Why: the long bones at the front of the foot spread the load across the ball "
              "of the foot and the toes."),
    dict(deck=FOOT, img="s14_foot.png",
         ver="lab manual p.177 ('The navicular bone bridges the talus and the three cuneiform bones'); study guide p.2 ('Navicular (talus → three cuneiforms)')",
         text="The {{c1::navicular}} bridges the talus and the three cuneiforms.",
         back="Why: the navicular sits in front of the talus on the inner side of the foot and passes the "
              "talus's load forward to the cuneiforms."),
    dict(deck=FOOT, img="m8_15_arch_height.jpg",
         ver="lab manual p.178 ('The navicular bone can often be felt and seen as a large bump on the medial side of your foot, high on the arch'); study guide p.2",
         text="The navicular can be felt as a large bump on the {{c1::medial}} side of the "
              "foot, high on the arch.",
         back="Why: the navicular sits near the top of the inner (medial longitudinal) arch, which is why "
              "its height from the floor is one of the lab's arch measurements."),
    dict(deck=FOOT, img="s14_foot.png",
         ver="lab manual p.177 ('Laterally, the cuboid bone is found between the calcaneus and 5th metatarsal'); study guide p.2",
         text="The {{c1::cuboid}} sits on the lateral side of the foot, between the calcaneus "
              "and the 5th metatarsal.",
         back="Why: cuboid means 'cube-shaped'; it carries the outer column of the foot from "
              "the heel to the little toe's metatarsal."),
    dict(deck=FOOT, img="s14_foot.png",
         ver="slide 14 (Medial / Intermediate / Lateral Cuneiform); lab manual Fig 8-13 (1C, 2C, 3C); study guide p.2",
         text="The three cuneiforms are named {{c1::medial, intermediate, and lateral}}, from "
              "the big-toe side outward.",
         back="Why: cuneiform means 'wedge-shaped'; the three wedges sit in a row in front of "
              "the navicular, each carrying one of the first three metatarsals."),
    dict(deck=FOOT, num=True, img="s14_foot.png",
         ver="slide 2 ('Metatarsals (10)'); slide 14 notes ('I-V (beginning with hallux)'); lab recording 9/30 [67:50] ('The big toes, number one, first metatarsal')",
         text="Each foot has {{c1::5::number}} metatarsals (10 in the body), numbered I to V "
              "starting from the {{c2::big toe}}.",
         back="Why: one metatarsal carries each toe, numbered like the hand from the medial "
              "side (big toe = I)."),
    dict(deck=FOOT, num=True, img="m8_13_foot.jpg",
         ver="slide 14 notes ('I-V, proximal, middle & distal (except hallux has no middle phalanx)'); lab recording 9/30 [67:50]-[68:42]; lab manual p.177 ('The toes, or digits, contain 14 bones'); study guide p.2",
         text="Each foot has {{c1::14::number}} phalanges: {{c2::2::number}} in the big toe "
              "and 3 in each of the other toes.",
         back="Why: exactly like the hand; the big toe (hallux), like the thumb, has no middle "
              "phalanx."),
    dict(deck=FOOT, num=True, img="s02_overview.jpg",
         ver="lab recording 9/30 [68:42] (Dr. Blais: '28 in the hand, 28 in the feet, 56 all together ... I'm giving you the tricky questions now so you don't mess it up on a test'); slide 2 ('Phalanges (28)' under both limbs)",
         text="The body has {{c1::56::number}} phalanges in all: 28 in the hands and 28 in the "
              "feet.",
         back="Why: 14 per hand or foot × 4 = 56; a question asking for the phalanges 'in the "
              "body' means all four limbs.<br><br>Pitfall: slide 2 lists 'Phalanges (28)' "
              "twice, once for the hands and once for the feet."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('The hallux, i.e., the first toe, or great toe'); slide 14 notes ('beginning with hallux')",
         text="The big toe is called the {{c1::hallux}}.",
         back="Why: 'hallux' is the anatomical name, just as the thumb is the pollex; the big toe's bones are "
              "number 1 (first metatarsal, first proximal phalanx)."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('The joint between the proximal and distal first phalanges is the interphalangeal (IP) joint. The two joints in the other toes are the distal interphalangeal joints (DIP) and proximal interphalangeal joints (PIP)'); study guide p.2; lab manual Fig 8-13",
         text="The big toe has one joint between its phalanges, the {{c1::IP}} joint; each "
              "other toe has two, the {{c2::PIP and DIP}} joints.",
         back="Why: joints sit between phalanges, so two phalanges make one interphalangeal "
              "(IP) joint and three make a proximal and a distal one."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('The base of each metatarsal articulates with the ankle bones; the head of each metatarsal articulates with a proximal phalanx')",
         text="The base of each metatarsal meets the {{c1::tarsals}}; its head meets a "
              "{{c2::proximal phalanx}}.",
         back="Why: for metacarpals and metatarsals alike, the base is the proximal end and "
              "the head is the distal end."),
    dict(deck=FOOT, img="m8_12_leg_foot.jpg",
         ver="lab manual p.178 ('The large tuberosity of the 5th metatarsal can be felt as a bump on the lateral side of your foot, exactly halfway between your heel and \"pinky\" toe'); study guide p.2; slide 14 notes; blue page 185 (palpation check-off)",
         text="The bump on the lateral side of the foot, halfway between the heel and the "
              "little toe, is the tuberosity of the {{c1::5th metatarsal}}.",
         back="Why: the tuberosity juts from the base of the little toe's metatarsal on the outer edge of "
              "the foot, where a calf muscle's tendon (fibularis brevis) attaches."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="lab manual p.178 ('The highest point of the foot is the base of the 2nd metatarsal'); study guide p.2",
         text="The highest point of the foot is the base of the {{c1::2nd metatarsal}}.",
         back="Why: the 2nd metatarsal's base is wedged in among the cuneiforms at the top of the foot's transverse "
              "dome."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="lab manual p.177 ('the metatarsals form three arches: The medial longitudinal arch ... the lateral longitudinal arch ... and the transverse arch'); study guide p.2; lab manual Fig 8-14",
         text="The foot has three arches: the {{c1::medial longitudinal}}, the "
              "{{c1::lateral longitudinal}}, and the {{c1::transverse}} arch.",
         back="Why: two run heel to toe along the inner and outer edges, and one arcs across "
              "the width of the foot."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="study guide p.2 ('Medial longitudinal (keystone ≈ talus)'); lab manual Fig 8-14 + p.177 ('Each arch has a keystone bone that marks the top of the arch')",
         text="The keystone of the medial longitudinal arch is the {{c1::talus}}.",
         back="Why: a keystone is the top stone of an arch, and the talus sits highest on the "
              "inner arch, taking the tibia's load."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="study guide p.2 ('Lateral longitudinal (keystone ≈ cuboid)'); lab manual Fig 8-14",
         text="The keystone of the lateral longitudinal arch is the {{c1::cuboid}}.",
         back="Why: the cuboid sits at the top of the outer arch, between the calcaneus and "
              "the 5th metatarsal."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="study guide p.2 ('Transverse (keystone ≈ medial cuneiform / 2nd metatarsal base)'); lab manual Fig 8-14",
         text="The keystones of the transverse arch are the {{c1::medial cuneiform}} and the "
              "base of the {{c2::2nd metatarsal}}.",
         back="Why: the transverse arch is a dome across the foot, and its high point is "
              "where the medial cuneiform and the wedged-in base of the 2nd metatarsal "
              "sit."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="lab manual p.177 ('These arches are dynamic structures that act as shock absorbers and springs when walking. The arches are held in place largely by supporting ligaments'); study guide p.2",
         text="The arches of the foot act as {{c1::shock absorbers and springs}}, held up "
              "mainly by {{c2::ligaments}}.",
         back="Why: the arched bones flatten slightly under each step and spring back, "
              "cushioning impact, while ligaments tie the arch's ends like a bowstring."),
    dict(deck=FOOT, img="m8_14_arches.jpg",
         ver="lab manual p.177-178 ('elongated ligaments resulting in a \"fallen arch\", or \"flat feet.\" There is mounting evidence that shoes are the cause of most fallen arches'); study guide p.2",
         text="Stretched (elongated) ligaments let the arch drop, giving a {{c1::fallen arch "
              "(flat feet)}}.",
         back="Why: once the ligaments stop holding the arch's ends together, the arch sags "
              "under body weight.<br><br>Cue: the manual cites evidence that shoes cause most "
              "fallen arches and that walking barefoot can strengthen weak ones."),
    dict(deck=FOOT, img="m8_12_leg_foot.jpg",
         ver="lab manual p.177 ('body weight is transferred from the femur to the tibia to the talus to the calcaneus'); blue page 186 Q3 ('Which bones of the lower limb support the body when standing?')",
         text="Standing, body weight passes from the femur to the {{c1::tibia}}, then the "
              "{{c2::talus}}, then the {{c3::calcaneus}}.",
         back="Why: the thick tibia sits on top of the talus, the talus on the heel bone, and "
              "the heel on the ground; the fibula is not part of this column."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab manual p.177 ('When walking, your body weight is transferred from the femur to the tibia to the talus to the calcaneus, then along the lateral edge of the foot through the 5th metatarsal, across the heads of the metatarsals and finally to the phalanges of the great toe'); study guide p.2",
         text="When walking, weight rolls from the heel along the {{c1::lateral edge of the "
              "foot (5th metatarsal)}}, across the {{c2::heads of the metatarsals}}, and "
              "finally to the {{c3::great toe}}, which lifts you into the next step.",
         back="Why: the heel strikes first, weight rolls along the outer edge, crosses the "
              "ball of the foot, and the big toe pushes off."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab recording 9/30 [68:42] (Dr. Blais: 'Right under that first metatarsal ... you're going to have two little sesamoid bones. They're medial and lateral sesamoids'); study guide p.2 ('Each foot has two sesamoid bones under the hallux'); lab manual Fig 8-1 ('4 sesamoids')",
         text="Each foot's two sesamoid bones sit under the head of the {{c1::first metatarsal "
              "(big toe)::which bone}}.",
         back="Why: the sesamoids sit in the tendons under the ball of the big toe and take the "
              "pressure as you push off.<br><br>Cue: the four foot sesamoids are why the "
              "manual counts 210 bones instead of 206."),
    dict(deck=FOOT, img="m8_13_foot.jpg",
         ver="lab recording 9/30 [68:42]-[69:27] (Dr. Blais: 'What are sesamoid bones? They are bones within tendons')",
         text="Sesamoid bones are bones that form inside {{c1::tendons}}.",
         back="Why: a bone embedded in a tendon protects it and improves its leverage; the "
              "patella and the two under each big toe are the main ones, and some people have "
              "extras in the hands or feet."),
    dict(deck=FOOT, num=True, img="m8_15_arch_height.jpg",
         ver="lab manual p.181 (arch-type table: High arch <0.74, Normal 0.75 - 1.25, Low 1.26 - 2, Flat >2); study guide p.2 ('Arch TAI')",
         text="A normal transverse arch index (TAI) is {{c1::0.75–1.25::range}}.",
         back="Why: the lab's footprint table: below 0.74 is a high arch, 1.26 to 2 a low "
              "arch, and above 2 a flat foot."),
    dict(deck=FOOT, img="m8_15_arch_height.jpg",
         ver="lab manual p.181 (arch-type table) + Fig 8-15 (High TAI=0.545, Normal 0.750, Low 1.94)",
         text="The higher the TAI, the {{c1::lower (flatter)::higher or lower}} the arch.",
         back="Why: the TAI rises as more of the midfoot prints on the paper, pushing the "
              "print's inner edge toward the medial line."),
    dict(deck=FOOT, img="m8_15_arch_height.jpg",
         ver="lab manual p.180 (Activity 4 step 7: 'The transverse arch index (TAI) is the ratio of MC/MA')",
         text="The transverse arch index (TAI) from a charcoal footprint is the ratio "
              "{{c1::MC / MA}}, measured across the middle of the print.",
         back="Why: both distances are measured from the medial line along the line through "
              "the middle of the footprint, so the ratio shows how much of the arch touches "
              "the floor."),
    dict(deck=FOOT, img="m8_15_arch_height.jpg",
         ver="lab manual p.181 (Activity 4 step 9: 'measure the height of the navicular bone from the floor (in mm) while standing'); study guide p.2 ('Also record navicular height from the floor')",
         text="Besides the TAI, the arch activity records the height of the "
              "{{c1::navicular}} bone from the floor while standing.",
         back="Why: the navicular sits near the top of the medial arch, so its height is a "
              "direct measure of how high the arch is."),
]
