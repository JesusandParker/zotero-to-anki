"""
io_spec.py — the Image Occlusion notes for BIOL 214 W06 (appendicular skeleton).

Every entry is one IO note on one plate. `masks` lists the labels to occlude, AS PRINTED
(as Vision reads them) on the plate; each item becomes ONE card:
    "Label"                         one occurrence
    ("Label", n)                    n occurrences of the same printed text, one card
    ["Label A", ("Label B", 2)]     different printed texts for the SAME structure, one card
    "Label@x,y"                     the occurrence nearest that pixel (first word)
    "#box:x0,y0,x1,y1"              a hand-drawn rectangle, in plate pixels
Labels resolve in the order given and a word belongs to one mask only, so a longer label
goes before any shorter label hiding inside it. Where Vision misreads a word the label is
written as Vision reads it (commented), because the mask is placed from those words.

Scope calls (Parker 2026-09-30: "the maximal set ... exactly what you did before"):
  * every labeled figure on the W06 slides and in lab manual Ch 8 gets a note;
  * slides 6, 9 and 10 mark what the lab wants known with BLUE BOXES (PowerPoint overlays),
    so each of those plates splits into a `boxed` note and an `optional` note for the rest;
  * labels the lab says are not required are kept but tagged `optional`: the slide 8 Netter
    labels ("Do not worry about the labels on this slide"), the femur's intertrochanteric
    line/crest, supracondylar lines and adductor tubercle and the fibular notch (speaker
    notes), the supraspinous/infraspinous fossae (lab instructor, 9/30 recording 16:15),
    the forearm's unboxed labels (slide 6: "identify the boxed labels").
"""

OVERVIEW = "Overview & Fetal Skeleton"
PECTORAL = "Pectoral Girdle"
ARM = "Arm & Forearm"
HAND = "Wrist & Hand"
PELVIS = "Pelvic Girdle"
LEG = "Thigh & Leg"
FOOT = "Ankle & Foot"

BOXED = "The lab boxed these in blue — know them for the practical."
SLIDES, MANUAL = "src::slides", "src::manual"

NOTES = [
    # ================================ OVERVIEW ================================
    dict(id="fetal_skull", deck=OVERVIEW, image="m8_18_fetal_skull.jpg", tags=[MANUAL],
         header="Fetal skull (lab model) — from the front (left) and from the left side (right)",
         back="Cue: fontanels are the soft, unossified gaps between the skull bones; they let "
              "the skull squeeze through the birth canal and close during infancy, the large "
              "anterior fontanel last (by about 18–24 months).",
         masks=["anterior fontanel", "frontal bone", "zygomatic arch", "maxilla", "mandible",
                "parietal bone", "temporal bone", "occipital bone", "mastoid fontanel",
                "sphenoidal fontanel"]),

    # ============================= PECTORAL GIRDLE =============================
    dict(id="clavicle_slide", deck=PECTORAL, image="s03_clavicle.png", tags=[SLIDES],
         header="Clavicle — (a) in place on the skeleton, (b) right clavicle from above, "
                "(c) right clavicle from below",
         back="Cue: the conoid tubercle is a bump on the UNDERSIDE near the acromial end; the "
              "sternal end is the thick end that meets the manubrium.",
         masks=["Acromio- clavicular joint", "Clavicle@434,342", "Scapula@67,1086",
                ["Sternal (medial) end", "Sternal end@1346,856"],
                ["Acromial (lateral) end", "Acromial end@871,759"],
                "Trapezoid line", "Conoid tubercle"]),
    dict(id="clavicle_model", deck=PECTORAL, image="m8_03_clavicles.jpg", tags=[MANUAL],
         header="Clavicles on the lab skeleton, with one clavicle seen from below (inset)",
         back="Cue: the manual sides a loose clavicle by its ends — thick, triangular sternal "
              "end vs flattened acromial end — plus the S-curve.",
         masks=["acromial end (flat)", "body",
                ["sternal end (triangular)", "sternal end@816,1089"], "conoid tubercle"]),
    dict(id="scapula_slide", deck=PECTORAL, image="s04_scapula.png", tags=[SLIDES],
         header="Right scapula — anterior view (left), lateral view (middle), posterior view "
                "(right)",
         back="Cue: the spine is only on the back; the glenoid cavity always faces laterally; "
              "the coracoid process is the smaller hook that sits in FRONT of the acromion.",
         masks=[("Acromial process", 3),        # Vision reads two of them as "Aeromial"
                ("Coracoid process", 3), ("Superior border", 2), "Scapula notch",
                ("Glenoid cavity", 3), "Neck", ("Lateral border", 3),
                ("Medial border", 2),           # one printed "Medail border" (slide typo)
                ("Spine", 2), "Body", "superior angle", "Subscapular fossa",
                "Inferior angle"]),
    dict(id="scapula_slide_fossae", deck=PECTORAL, image="s04_scapula.png",
         tags=[SLIDES, "optional"],
         header="Right scapula — the two fossae on the posterior surface",
         back="Pitfall: the lab instructor said (9/30) they won't ask about the supraspinous "
              "or infraspinous fossa, so this card is extra.<br><br>Cue: the spine divides "
              "the back of the scapula — supraspinous fossa ABOVE it, the larger "
              "infraspinous fossa BELOW it.",
         masks=["Supraspinous fossa", "Infraspinous fossa"]),
    dict(id="scapula_model", deck=PECTORAL, image="m8_02_scapula.jpg", tags=[MANUAL],
         header="Scapula (lab model) — lateral view, anterior view (inset), posterior view",
         back="Cue: three borders (superior, medial, lateral) and three angles (superior, "
              "inferior, lateral); the suprascapular notch sits on the superior border.",
         masks=[("acromion", 2), ("coracoid process", 2), "superior border", "superior angle",
                ("glenoid cavity", 2), "lateral angle", ("spine", 2), "suprascapular notch",
                ("lateral border", 2), "medial border", "subscapular fossa",
                ("inferior angle", 2)]),         # one read as "interior angle"
    dict(id="scapula_model_fossae", deck=PECTORAL, image="m8_02_scapula.jpg",
         tags=[MANUAL, "optional"],
         header="Scapula (lab model) — the two fossae on the posterior surface",
         back="Pitfall: the lab instructor said (9/30) they won't ask about the supraspinous "
              "or infraspinous fossa, so this card is extra.",
         masks=["supraspinous fossa", "infraspinous fossa"]),

    # ============================== ARM & FOREARM ==============================
    dict(id="humerus_slide", deck=ARM, image="s05_humerus.png", tags=[SLIDES],
         header="Right humerus — (a) anterior view, (b) posterior view",
         back="Cue: head points medially, deltoid tuberosity laterally; capitulum and "
              "trochlea show from the front, the deep olecranon fossa from the back.",
         masks=["Greater tubercle", "Lesser tubercle", "Inter- tubercular groove",
                "Head of humerus", "Anatomical neck", "Surgical neck", "Radial groove",
                ("Deltoid tuberosity", 2), "Medial supracondylar ridge",
                "Lateral supracondylar ridge", "Coronoid fossa", "Olecranon fossa",
                "Radial fossa", "Medial epicondyle", "Lateral epicondyle", "Capitulum",
                "Trochlea"]),
    dict(id="humerus_model", deck=ARM, image="m8_04b_humerus.jpg", tags=[MANUAL],
         header="Humerus (lab model) — posterior view (left), anterior view (right)",
         back="Distinguish: anatomical neck = the rim of the joint surface right under the "
              "head; surgical neck = the narrower shaft just below it, where the bone "
              "usually breaks.",
         masks=["head of humerus", "anatomical neck", "surgical neck", "lesser tubercle",
                "greater tubercle", ("deltoid tuberosity", 2), "medial supracondylar ridge",
                "coronoid fossa", "radial fossa", "olecranon fossa", "medial epicondyle",
                "lateral epicondyle", "trochlea", "capitulum"]),
    dict(id="forearm_slide_boxed", deck=ARM, image="s06_forearm.png", tags=[SLIDES, "boxed"],
         header="Right radius and ulna — (a) anterior view, (b) posterior view. " + BOXED,
         back="Cue: the ulna's proximal end is the C-shaped 'claw' (olecranon + trochlear "
              "notch + coronoid process); the radius has the round head. Radial styloid = "
              "thumb side, ulnar styloid = pinky side.",
         masks=["Olecranon process", "Trochlear notch",
                ["Head@138,219", "Head of radius@1351,216"], "Radial tuberosity",
                "Coronoid process", "Ulna@677,720", ["Radius@111,910", "Radius@1346,956"],
                "Head of ulna", "Styloid process of ulna", ("Styloid process of radius", 2)]),
    dict(id="forearm_slide_other", deck=ARM, image="s06_forearm.png",
         tags=[SLIDES, "optional"],
         header="Right radius and ulna — the labels the lab did NOT box",
         back="Pitfall: slide 6 says to know the BOXED labels, and the lab instructor said the "
              "interosseous membrane won't be asked, so these cards are extra.<br><br>Cue: "
              "each radioulnar joint pairs a head with a notch — radial head in the ulna's "
              "radial notch (proximal), ulnar head in the radius's ulnar notch (distal).",
         masks=["Radial notch", ["Neck@138,291", "Neck of radius"],
                "Proximal radioulnar joint", "Interosseous membrane", "Ulnar notch",
                "Distal radioulnar joint"]),
    dict(id="forearm_model", deck=ARM, image="m8_04c_forearm.jpg", tags=[MANUAL],
         header="Ulna (left bone) and radius (right bone), lab model — the upper 'styloid "
                "process' label is the ulna's, the lower one the radius's",
         back="Cue: the ulna is big at the elbow and small at the wrist; the radius is the "
              "reverse. Its head is at the elbow; the ulna's head is at the wrist.",
         masks=["olecranon", "trochlear notch", "coronoid process",
                "proximal radioulnar joint", "head of radius", "radial tuberosity",
                "ulna@319,666", "radius@904,770", "styloid process@799,1027",
                "head of uina",                  # Vision reads "ulna" as "uina"
                "distal radioulnar joint", "styloid process@791,1436"]),

    # =============================== WRIST & HAND ===============================
    dict(id="hand_slide", deck=HAND, image="s07_hand.png", tags=[SLIDES],
         header="Bones of the hand and wrist, palm side (the numbers 1–5 name the "
                "metacarpals)",
         back="Mnemonic: So Long To Pinky, Here Comes The Thumb — scaphoid, lunate, "
              "triquetrum, pisiform (proximal row, thumb side to pinky side), then hamate, "
              "capitate, trapezoid, trapezium (distal row, back to the thumb).<br><br>"
              "Cue: metacarpals and fingers are numbered from the THUMB (1) to the pinky (5).",
         masks=["Distal", "Middle", "Proximal", "Phalanges (fingers)", "Metacarpals (palm)",
                "Carpals (wrist)", "Hamate", "Pisiform", "Triquetrum", "Lunate", "Ulna",
                "Trapezium", "Trapezoid", "Scaphoid", "Capitate", "Radius",
                "1", "2", "3", "4", "5"]),
    dict(id="hand_palmar_key", deck=HAND, image="m8_06a_hand_palmar.jpg", tags=[MANUAL],
         header="Bones of the right hand, palm side — name the bone at each numbered pin",
         back="Cue: name a finger bone by row (proximal / middle / distal) and digit number "
              "(thumb = 1st); the thumb has no middle phalanx.",
         masks=["distal 1st phalanx", "proximal 1st phalanx", "distal 2nd phalanx",
                "middle 2nd phalanx", "proximal 2nd phalanx", "metacarpal I",
                "metacarpal II", "metacarpal III", "metacarpal IV", "metacarpal V"]),
    dict(id="hand_dorsum_key", deck=HAND, image="m8_06b_hand_dorsum.jpg", tags=[MANUAL],
         header="Carpal bones of the right wrist, back of the hand — name the carpal at each "
                "numbered pin (the word in brackets is its word in the mnemonic)",
         back="Mnemonic: So Long To Pinky, Here Comes The Thumb.",
         masks=["scaphoid (so)", "lunate (long)", "triquetrum (to)", "pisiform (pinky)",
                "hamate (here)", "capitate (comes)", "trapezoid (the)",
                "trapezium (thumb)"]),

    # =============================== PELVIC GIRDLE ===============================
    dict(id="hip_lateral_boxed", deck=PELVIS, image="s09_hip_lateral.png",
         tags=[SLIDES, "boxed"],
         header="Right hip bone (os coxae), lateral view. " + BOXED,
         back="Cue: orient it first — iliac crest up, obturator foramen down, acetabulum "
              "facing out (lateral), sciatic notches and ischial spine at the back.",
         masks=["Mum@1299,155",                 # "Ilium" (Vision reads "Mum")
                "Iliac crest", "Anterior superior iliac spine",
                "Posterior superior iliac spine", "Posterior inferior iliac spine",
                "Anterior inferior iliac spine", "Greater sciatic notch", "Acetabulum",
                "Ischial spine@217,793", "Lesser sciatic notch", "Ischium@217,955", "Pubis@1235,919",
                "Ischial tuberosity", "Ischial ramus", "Obturator foramen"]),
    dict(id="hip_lateral_other", deck=PELVIS, image="s09_hip_lateral.png",
         tags=[SLIDES, "optional"],
         header="Right hip bone, lateral view — the labels the lab did NOT box",
         back="Pitfall: the lab said the blue-boxed labels are what to know, so these cards "
              "are extra.<br><br>Cue: ala means wing — the broad, flared upper part of the "
              "ilium; the gluteal lines on it mark where the gluteal muscles attach.",
         masks=["Anterior gluteal line", "Posterior gluteal line", "Inferior gluteal line",
                "Ischial body", "Pubic body", "Inferior ramus of pubis", "Ala"]),
    dict(id="hip_medial_boxed", deck=PELVIS, image="s10_hip_medial.png",
         tags=[SLIDES, "boxed"],
         header="Right hip bone (os coxae), medial (inside) view. " + BOXED,
         back="Cue: the inside face has NO acetabulum — just the smooth, hollow iliac fossa "
              "above and the obturator foramen below.",
         masks=["Num@236,151",                  # "Ilium" (Vision reads "Num")
                "Iliac crest", "Iliac fossa", "Posterior superior iliac spine",
                "Posterior inferior iliac spine", "Anterior superior iliac spine",
                "Anterior inferior iliac spine", "Greater sciatic notch", "Ischial spine",
                "Lesser sciatic notch", "Obturator foramen", "Ischium@1183,1037",
                "Ischial ramus", "Pubic tubercle"]),
    dict(id="hip_medial_other", deck=PELVIS, image="s10_hip_medial.png",
         tags=[SLIDES, "optional"],
         header="Right hip bone, medial view — the labels the lab did NOT box",
         back="Pitfall: the lab said the blue-boxed labels are what to know, so these cards "
              "are extra.<br><br>Cue: the ear-shaped auricular surface is where the ilium "
              "joins the sacrum (sacroiliac joint).",
         masks=["Auricular surface", "Body of the ilium", "Arcuate line",
                "Superior ramus of pubis", "Articular surface of pubis (at pubic symphysis)",
                "Inferior ramus of pubis"]),
    dict(id="coxal_netter_bones", deck=PELVIS, image="s08_coxal_netter.png", tags=[SLIDES],
         header="Hip bone (coxal bone), lateral view, colour-coded by the three bones that "
                "fuse to form it — name each colour",
         back="Cue: all three meet in the acetabulum — ilium on top, ischium at the back and "
              "bottom, pubis in front.",
         masks=["Miur@182,1302",                # legend "Ilium" (Vision reads "Miur")
                "Ischium@183,1353",             # printed "Ischiun"
                "Pubis@183,1394"]),
    dict(id="coxal_netter_labels", deck=PELVIS, image="s08_coxal_netter.png",
         tags=[SLIDES, "optional"],
         header="Hip bone, lateral view (Netter) — slide 8 says: do not worry about the "
                "labels on this slide",
         back="Pitfall: the slide itself says not to worry about these labels; the blue-boxed "
              "slides (9 and 10) are the ones to know. Kept here only as extra practice on a "
              "different drawing.",
         masks=["Interediate line of iliac crest",   # printed "Intermediate"
                "Tubercle of iliac crest", "Anterior gluteal line", "Inferior gluteal line",
                "External lip of iliac crest", "Posterior gluteal line",
                "Anterior superior iliac spine", "Posterior superior iliac spine",
                "Wing (ala) of ilium (gluteal surface)", "Anterior inferior iliac spine",
                "Posterior inferior iliac spine", "Lunate surface of acetabulum",
                "Acetabulum", "Greater sciatic notch",
                "Intargin (limbus) of acetabulum",   # "Margin (limbus)" misread
                "Body of ilium", "Notch of acetabulum", "Ischial spine",
                "Superior pubic ramus", "Lesser sciatic notch", "Pubic tubercle",
                "Body of ischium", "Obturator crest", "Inferior pubic ramus",
                "Obturator foramen", "Ischial tuberosity", "Ramus of ischium"]),
    dict(id="hip_lateral_model", deck=PELVIS, image="m8_07_hip_lateral.jpg", tags=[MANUAL],
         header="Right hip bone (lab model), lateral view colour-coded by bone, with a view "
                "from above (right)",
         back="Cue: ASIS/AIIS on the front edge of the ilium, PSIS/PIIS on the back edge; "
              "below the PIIS come the greater sciatic notch, ischial spine and lesser "
              "sciatic notch.",
         masks=["ilium@236,196", "ischium@233,236", "pubis@235,280", "wing (ala) of ilium",
                "iliac crest", "anterior superior iliac spine (ASIS)",
                "anterior inferior iliac spine (AllS)",   # "(AIIS)" read as "(AllS)"
                "posterior superior iliac spine (PSIS)",
                "posterior inferior iliac spine (PIIS)", "acetabulum",
                "greater sciatic notch", "superior pubic ramus", "ischial spine",
                "pubic tubercle", "lesser sciatic notch", "obturator foramen",
                "ischial tuberosity", "inferior pubic ramus", "ischial ramus"]),
    dict(id="hip_medial_model", deck=PELVIS, image="m8_08_hip_medial.jpg", tags=[MANUAL],
         header="Right hip bone (lab model) seen from the inside (left, numbered), and the "
                "whole pelvis from the front (right)",
         back="Cue: the starred iliac tuberosity and auricular surface are the rough areas "
              "where the ilium joins the sacrum; the pelvic inlet (red ring) is the pelvic "
              "brim.",
         masks=["iliac fossa", "ASIS", "iliac tuberosity*", "auricular surface*",
                "arcuate line", "ischial spine", "pubic tubercle",
                ["pubic symphysis (articulation site)", "pubic symphysis@922,643"],
                "iliac crest", "greater sciatic notch", "lesser sciatic notch",
                "inguinal ligament", "pelvic inlet", "pubic crest"]),
    dict(id="gluteal_region", deck=PELVIS, image="m8_10_gluteal.jpg",
         tags=[MANUAL, "surface-anatomy"],
         header="Gluteal region from behind — surface landmarks",
         back="Cue: the two dimples over the PSIS sit on either side of the sacrum; the "
              "greater trochanter lies at the side of the hip.",
         masks=["dorsum", "level of iliac crest", "PSIS", "lateral gluteal depression",
                "intergluteal cleft", "hip", "buttock", "gluteal fold",
                "site of greater trochanter", "thigh"]),

    # ================================ THIGH & LEG ================================
    dict(id="femur_slide", deck=LEG, image="s11_femur.png", tags=[SLIDES],
         header="Right femur — anterior view (left) and posterior view (right)",
         back="Cue: head medial, greater trochanter lateral; linea aspera and intercondylar "
              "fossa on the back, patellar surface on the front.",
         masks=["Neck", "Fovea capitis", "Head@838,224", "Greater trochanter",
                "Lesser trochanter", "Gluteal tuberosity", "Linea aspera",
                "Intercondylar fossa", "Medial epicondyle@796,1332",
                "Medial condyle@742,1147",
                ["Lateral epicondyle@63,1324", "Lateral epicondyle@1319,1036"],
                "Patellar surface", "Lateral condyle@1309,881"]),
    dict(id="femur_slide_extra", deck=LEG, image="s11_femur.png", tags=[SLIDES, "optional"],
         header="Right femur — the labels the lab says you do NOT need",
         back="Pitfall: the slide 11 notes say you do NOT need the intertrochanteric line, "
              "intertrochanteric crest, supracondylar lines, or adductor tubercle — these "
              "cards are extra.",
         masks=["Intertrochanteric line", "Inter- trochanteric crest",
                "Medial and lateral supra- condylar lines", "Adductor tubercle"]),
    dict(id="femur_model", deck=LEG, image="m8_09_femur_patella.jpg", tags=[MANUAL],
         header="Left femur (lab model) — posterior view (left), anterior view with the "
                "patella (right)",
         back="Cue: the neck angles about 125 degrees off the shaft (angle of inclination); "
              "the fovea capitis is the pit on the head where a ligament attaches.",
         masks=["site of fovea capitis", "head@610,180", "neck@419,231",
                "greater trochanter", "lesser trochanter", "angle of inclination",
                "pectineal line", "gluteal tuberosity", "linea aspera",
                "lateral epicondyle", "medial epicondyle", "patella", "lateral condyle",
                "intercondylar fossa", "medial condyle"]),
    dict(id="femur_model_extra", deck=LEG, image="m8_09_femur_patella.jpg",
         tags=[MANUAL, "optional"],
         header="Left femur (lab model) — labels the lab says you do NOT need",
         back="Pitfall: the slide 11 notes say the intertrochanteric line and the "
              "supracondylar lines are not required — these cards are extra.",
         masks=["intertrochanteric line", "lateral supracondylar line",
                "medial supracondylar line"]),
    dict(id="patella_slide", deck=LEG, image="s12_patella.png", tags=[SLIDES],
         header="Patella — anterior view (left), posterior view (right)",
         back="Cue: the patella is an upside-down triangle — broad base on top, pointed apex "
              "at the bottom; the smooth articular surface faces the femur.",
         masks=["Base", "Apex", "Articular surface"]),
    dict(id="tibia_fibula_slide", deck=LEG, image="s13_tibia_fibula.png", tags=[SLIDES],
         header="Right tibia and fibula, anterior view",
         back="Mnemonic: the 'la' in fibula = LAteral.<br><br>Cue: medial malleolus = end "
              "of the tibia (inner ankle); lateral malleolus = end of the fibula (outer "
              "ankle).",
         masks=["lateral condyle", "medial condyle", "head of fibula", "tibial tuberosity",
                "tibia (shinbone)", "fibula@383,762", "medial malleolus",
                "lateral malleolus"]),
    dict(id="tibia_fibula_slide_extra", deck=LEG, image="s13_tibia_fibula.png",
         tags=[SLIDES, "optional"],
         header="Right tibia and fibula, anterior view — the one label the lab excludes",
         back="Pitfall: the slide 13 notes say to know the labels EXCEPT the fibular notch — "
              "this card is extra.<br><br>Cue: the fibular notch is the groove on the "
              "distal tibia where the fibula fits (distal tibiofibular joint).",
         masks=["fibular notch"]),
    dict(id="leg_foot_model", deck=LEG, image="m8_12_leg_foot.jpg", tags=[MANUAL],
         header="Tibia, fibula and foot (lab model), with the front of the knee (inset, "
                "patella removed)",
         back="Cue: the femur's condyles rest on the flat articular surfaces of the tibia's "
              "condyles; the head of the fibula sits just under the lateral condyle.",
         masks=["intercondylar eminence", "articular surface of lateral condyle",
                "articular surface of medial condyle", "lateral condyle@113,329",
                "medial condyle@668,422", "head of fibula", "popliteal line",
                "fibula@168,806", "tibia@196,919", "patellar surface (femur)",
                "tibial tuberosity", "talus", "calcaneus", "tuberosity of 5th metatarsal",
                "lateral malleolus"]),

    # ================================ ANKLE & FOOT ================================
    dict(id="foot_slide", deck=FOOT, image="s14_foot.png", tags=[SLIDES],
         header="Bones of the right foot, from above",
         back="Mnemonic: The Circus Needs More Interesting Little Clowns — talus, calcaneus, "
              "navicular, medial / intermediate / lateral cuneiform, cuboid.",
         masks=["Distal", "Middle", "Proximal", "Phalanges", "Metatarsals", "Tarsals",
                "Medial cuneiform", "Intermediate cuneiform", "Lateral cuneiform",
                "Navicular", "Cuboid", "Talus", "Calcaneus"]),
    dict(id="foot_regions_model", deck=FOOT, image="m8_13_foot.jpg", tags=[MANUAL],
         header="Bones of the foot and ankle (lab model), from above — colour-coded forefoot, "
                "midfoot, hindfoot; letters on the bones match the key",
         back="Cue: hindfoot = talus + calcaneus; midfoot = navicular, three cuneiforms, "
              "cuboid; forefoot = metatarsals + phalanges. Between its phalanges the big toe "
              "has one joint (IP); the other toes have two (PIP, DIP).",
         masks=["calcaneus", "talus", "cuboid", "navicular", "medial cuneiform",
                "intermediate cuneiform", "lateral cuneiform", "metatarsals 1-5",
                "forefoot", "midfoot", "hindfoot", "distal", "middle", "proximal",
                "IP", "DIP", "PIP", "tuberosity of 5th metatarsal"]),
    dict(id="foot_arches", deck=FOOT, image="m8_14_arches.jpg", tags=[MANUAL],
         header="The three arches of the foot and the keystone bone at the top of each",
         back="Cue: like the top stone of a stone arch, each keystone sits at the highest "
              "point of its arch — talus (medial longitudinal), cuboid (lateral "
              "longitudinal), medial cuneiform / 2nd metatarsal (transverse).<br><br>"
              "Pitfall: most anatomy texts name the intermediate (middle) cuneiform, not the "
              "medial one, as the transverse arch's keystone; the manual's figure and the "
              "study guide say medial cuneiform.",
         masks=["medial cuneiform", "2nd metatarsal", ("transverse arch", 2), "cuboid",
                "Lateral longitudinal arch", "talus", ("medial longitudinal arch", 2)]),
]
