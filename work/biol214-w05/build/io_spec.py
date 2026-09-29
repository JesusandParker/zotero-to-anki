"""
io_spec.py — the Image Occlusion notes for BIOL 214 W05 (axial skeleton).

Every entry is one IO note on one plate. `masks` lists the labels to occlude, AS PRINTED
on the plate; each item becomes ONE card:
    "Label"                         one occurrence
    ("Label", n)                    n occurrences of the same printed text, one card
    ["Label A", ("Label B", 2)]     different printed texts for the SAME structure, one card
Labels are resolved in the order given and a word can only belong to one mask, so list a
longer label before any shorter label hiding inside it ("temporal process of zygomatic
bone" before "zygomatic bone"). Card order in Anki follows the printed order below, which
is the order the masks are numbered in.

Anything not listed stays visible: view names, panel letters, copyright lines, the
"*ethmoid bone" footnote, orientation words.
"""

BONE = "Bone Basics & Cartilage"
SKULL = "Skull & Hyoid"
FORAMINA = "Skull Foramina & Cranial Floor"
SPINE = "Vertebral Column"
SACRUM = "Sacrum & Coccyx"
CAGE = "Thoracic Cage"

RED = "The lab boxed these in red — know them for the practical."

NOTES = [
    # ============================ BONE BASICS & CARTILAGE ============================
    dict(id="long_bone_slide", deck=BONE, image="s03_long_bone.jpg",
         header="Long bone (humerus), cut lengthwise",
         back="Cue: a long bone is one shaft (diaphysis) with a knobby epiphysis at each end; "
              "the epiphyseal line is the bony scar left where the growth plate used to be.",
         masks=["Proximal epiphysis", "Diaphysis", "Distal epiphysis", "Spongy bone",
                "Articular cartilage", "Epiphyseal line", "Periosteum", "Compact bone",
                "Medullary cavity"]),
    dict(id="long_bone_model", deck=BONE, image="m6_04_long_bone_model.jpg",
         header="Long bone model (humerus), cut lengthwise",
         back="Cue: the hyaline cartilage capping the end is articular cartilage — the smooth "
              "joint surface; the bone marrow cavity of the shaft holds yellow (fatty) marrow.",
         masks=["hyaline cartilage", "spongy bone", "epiphyseal line", "bone marrow cavity",
                "compact bone", "yellow bone marrow", "periosteum", "proximal epiphysis",
                "diaphysis (shaft)", "distal epiphysis"]),
    dict(id="compact_bone", deck=BONE, image="s04_compact_bone.jpg",
         header="Compact bone — (a) a wedge of the shaft, (b) lamellae and osteocytes, "
                "(c) an osteon under the microscope",
         back="Cue: rings of lamellae around one central canal make an osteon; osteocytes "
              "sit in lacunae between the rings, linked to the canal by canaliculi.<br><br>"
              "Distinguish: central (Haversian) canals run LENGTHWISE; perforating "
              "(Volkmann's) canals run SIDEWAYS and connect them.",
         masks=[
             ["Circumferential lamellae"],
             ["Interstitial lamellae"],
             [("Osteon", 2), "(Haversian system)"],
             ["Lamellae", "Lamella"],
             ["Osteocyte"],
             [("Lacuna", 2)],
             ["Canaliculus"],
             [("Central (Haversian) canal", 2), "Central canal"],
             ["Spongy bone"],
             ["Perforating (Sharpey's) fibers"],
             ["Compact bone"],
             ["Periosteum"],
             ["Perforating (Volkmann's) canal"],
             ["Endosteum lining bony canals and covering trabeculae"],
         ]),
    dict(id="marrow_section", deck=BONE, image="s05_marrow_section.jpg",
         header="Fresh bone cut in cross-section",
         back="Cue: red marrow (blood-forming) fills the spongy bone; yellow marrow (fat) "
              "sits in the middle.",
         masks=["Red marrow", "Yellow marrow"]),
    dict(id="intervertebral_disc", deck=BONE, image="s07_disc.jpg",
         header="Intervertebral disc — lateral view (left) and superior view (right)",
         back="Cue: the anulus fibrosus is the tough fibrocartilage ring; the nucleus "
              "pulposus is the soft gel centre it holds in. Spinal nerves leave through the "
              "intervertebral foramen between two vertebrae.",
         masks=["Vertebral body", "Intervertebral foramen", "Anulus fibrosus",
                "Nucleus pulposus"]),

    # ================================= SKULL & HYOID =================================
    dict(id="cranial_bones", deck=SKULL, image="s10_cranial_bones.png",
         header="Cranial bones — skull from the right side (left) and the cranial floor seen "
                "from above (right)",
         back="Mnemonic: PEST OF — Parietal, Ethmoid, Sphenoid, Temporal, Occipital, "
              "Frontal.<br><br>Cue: parietal and temporal come in pairs, so the cranium "
              "has 8 bones.",
         masks=["Frontal", "Ethmoid", "Sphenoid", "Temporal", "Parietal", "Occipital"]),
    dict(id="facial_bones", deck=SKULL, image="s11_facial_bones.png",
         header="Facial bones — skull from the front (left) and from below (right)",
         back="Cue: 14 facial bones — the mandible and vomer are single; the other six come "
              "in pairs.<br><br>Roster: nasal = bridge of the nose · lacrimal = inner wall "
              "of the orbit (tear drainage) · zygomatic = cheekbone · maxilla = upper jaw · "
              "palatine = back of the hard palate · inferior nasal concha = scroll of bone "
              "in the nasal cavity · vomer = lower nasal septum · mandible = lower jaw",
         masks=["Nasal bone", "Lacrimal bone", "Zygomatic bone", "Maxilla", "Mandible",
                "Inferior nasal concha", "Vomer", "Palatine"]),
    dict(id="skull_model_post_lat", deck=SKULL, image="m7_02a_skull_post_lat.jpg",
         header="Skull model — from behind (left) and from the left side (right)",
         back="Cue: the sutures and the bones they join — coronal (frontal and parietals), "
              "sagittal (the two parietals), lambdoid (parietals and occipital), squamous "
              "(parietal and temporal).",
         masks=[
             ["zygomatic process of temporal bone@1353,84"],
             ["temporal process of zygomatic bone@585,527"],
             ["mastoid process (temporal bone)@408,821", "mastoid process of temporal bone@1373,713"],
             ["coronoid process of mandible@619,708"],
             ["condylar process of mandible@1356,863"],
             ["ramus of mandible@602,904"],
             ["angle of mandible@1061,904"],
             ["external occipital protuberance@160,838"],
             ["external acoustic meatus@1373,790"],
             ["parietal bone@464,100", "parietal bone@1458,178"],
             ["sagittal suture@168,168"],
             ["lambdoid suture@97,245", "lambdoid suture@1456,395"],
             ["sutural bone@482,361"],
             ["occipital bone@115,717", "occipital bone@1456,529"],
             ["coronal suture@1062,100"],
             ["frontal bone@735,145"],
             ["sphenoid bone@645,218"],
             ["squamous suture@1454,296"],
             ["supraorbital foramen@572,316"],
             ["zygomatic arch@642,393"],
             ["nasal bone@690,446"],
             ["zygomatic bone@632,483"],
             ["temporal bone@1456,614"],
             ["maxillary bone@642,655"],
             ["mental foramen@640,791"],
             ["mandible@720,846"],
         ]),
    dict(id="skull_model_obl_ant", deck=SKULL, image="m7_02b_skull_obl_ant.jpg",
         header="Skull model — cut-away view into the orbit (left) and from the front (right)",
         back="Cue: the starred parts (perpendicular plate, middle concha) belong to the "
              "ethmoid bone; the lacrimal fossa holds the lacrimal sac, which drains tears into "
              "the nasal cavity.",
         masks=[
             ["mastoid process (temporal bone)@157,719"],
             ["styloid process (temporal bone)@276,829"],
             ["zygomatic process (temporal bone)@502,817"],
             ["temporal process (zygomatic bone)@547,729"],
             ["supraorbital foramen (notch)@1378,169"],
             ["perpendicular plate*@1408,284"],
             ["middle concha*@1409,320"],
             ["infraorbital foramen@1371,528"],
             ["inferior nasal concha@1343,654"],
             ["lacrimal fossa@758,386"],
             ["lacrimal bone@761,350", "lacrimal bone@1401,245"],
             ["zygomatic bone@594,678", "zygomatic bone@1398,445"],
             ["occipital bone@132,122"],
             ["parietal bone@393,86"],
             ["frontal bone@761,190"],
             ["ethmoid bone@761,285", "*ethmoid bone@1454,744"],
             ["nasal bones@761,421"],
             ["temporal bone@107,562"],
             ["maxillary bone@733,614"],
             ["sphenoid bone@1413,373"],
             ["vomer@1243,752"],
         ]),
    dict(id="mandible_model", deck=SKULL, image="m7_05_mandible.jpg",
         header="Mandible (lab model), from the right side",
         back="Cue: the mandibular condyle hinges against the temporal bone; the mandibular "
              "foramen carries nerves and vessels to the lower teeth, the mental foramen to "
              "the chin.",
         masks=["mandibular condyle", "mandibular notch", "coronoid process",
                "mandibular foramen", "alveolar margin", "ramus of mandible",
                "body of mandible", "mental foramen", "mandibular angle"]),
    dict(id="sinuses_model", deck=SKULL, image="m7_07_sinuses.jpg",
         header="Sinuses of the skull (lab model) — front-side view (top) and midline cut "
                "(bottom)",
         back="Cue: four skull bones hold air sinuses — frontal, ethmoid, sphenoid, maxillary; "
              "the sella turcica is the saddle on the sphenoid that seats the pituitary gland, "
              "right above the sphenoid sinus.",
         masks=["frontal sinus", "maxillary sinus", "ethmoid sinuses", "sella turcica",
                "sphenoid sinus"]),
    dict(id="hyoid", deck=SKULL, image="s13_hyoid.jpg",
         header="Hyoid bone — from the front (top) and from the left side (bottom)",
         back="Meaning: cornu = horn — the greater and lesser horns are where muscles and the "
              "stylohyoid ligaments attach.",
         masks=[["Greater cornu@906,121", "Greater cornu@1448,737"], ["Lesser cornu@432,287", "Lesser cornu@911,670"], ["Body@781,511", "Body@1079,970"]]),

    # ========================= SKULL FORAMINA & CRANIAL FLOOR =========================
    dict(id="foramina_red", deck=FORAMINA, image="s12_cranial_foramina.png",
         header="Cranial foramina — floor of the cranial cavity seen from above. " + RED,
         back="Cue: along each side of the sphenoid, rotundum → ovale → spinosum run front "
              "to back (round, oval, spiny).<br><br>"
              "Roster (what passes through): cribriform foramina — smell (olfactory) nerve "
              "fibers · optic canal — optic nerve and ophthalmic artery · foramen rotundum — maxillary nerve (V2) · "
              "foramen ovale — mandibular nerve (V3) · foramen spinosum — middle meningeal "
              "artery · foramen lacerum — plugged with cartilage in life · internal acoustic "
              "meatus — facial and vestibulocochlear nerves (VII, VIII) · jugular foramen — "
              "internal jugular vein + nerves IX–XI · hypoglossal canal — hypoglossal nerve "
              "(XII) · foramen magnum — spinal cord and the vertebral arteries",
         tags=["red-box"],
         masks=[["Cribriform foramina", "Cribriform plate"], "Optic canal", "Foramen rotundum", "Foramen ovale",
                "Foramen lacerum", "Foramen spinosum", "Hypoglossal canal",
                "Internal acoustic meatus", "Jugular foramen", "Foramen magnum"]),
    dict(id="foramina_other", deck=FORAMINA, image="s12_cranial_foramina.png",
         header="Floor of the cranial cavity seen from above — bones, fossae and landmarks",
         back="Cue: the floor steps down in three tiers — anterior, middle and posterior "
              "cranial fossae, front to back.",
         masks=[["Cribriform plate", "Cribriform foramina"], "Crista galli", "Ethmoid bone", "Anterior cranial fossa",
                "Lesser wing", "Greater wing", "Sphenoid", "Hypophyseal fossa of sella turcica",
                "Middle cranial fossa", "Temporal bone (petrous part)", "Posterior cranial fossa",
                "Parietal bone", "Occipital bone", "Frontal bone"]),
    dict(id="cranial_floor_model", deck=FORAMINA, image="m7_04_cranial_floor.jpg",
         header="Floor of the cranial cavity — painted lab model (left) and real skull "
                "(right). Find the highlighted key number on the photos and name it.",
         back="Cue: the lab manual's 'internal acoustic canal' is the same opening as the "
              "internal acoustic meatus.<br><br>Pitfall: the true nuchal lines are ridges on the "
              "OUTER surface of the occipital bone (see the skull from below); key 11 points at "
              "the occipital from inside the skull.",
         masks=["sphenoid bone (greater wing)", "sella turcica (sphenoid)",
                "lesser wing (sphenoid)", "anterior cranial fossa", "middle cranial fossa",
                "posterior cranial fossa", "internal acoustic canal", "ethmoid bone",
                "frontal bone", "temporal bone", "occipital bone", "parietal bone",
                "foramen magnum", "nuchal lines", "foramen rotundum", "foramen lacerum",
                "foramen ovale", "foramen spinosum", "jugular foramen", "hypoglossal canal"]),
    dict(id="skull_inferior", deck=FORAMINA, image="m7_03_skull_inferior.jpg",
         header="Skull from below (real skull)",
         back="Cue: the occipital condyles beside the foramen magnum rest on C1 (the atlas) — "
              "the 'yes' nod; the carotid canal carries the internal carotid artery into the "
              "skull.<br><br>Meaning: the manual's 'medial palatine suture' is usually called the "
              "median palatine suture.",
         masks=["temporal process of zygomatic bone", "zygomatic process of temporal bone",
                "superior nuchal line (occipital bone)", "external occipital protuberance",
                "mastoid process (temporal bone)", "external acoustic meatus",
                "medial palatine suture", "stylomastoid foramen", "incisive fossa",
                "maxillary bone", "palatine bone", "foramen lacerum", "zygomatic arch",
                "foramen ovale", "sphenoid bone", "foramen spinosum", "carotid canal",
                "occipital condyle", "foramen magnum", "occipital bone"]),

    # ================================ VERTEBRAL COLUMN ================================
    dict(id="spine_regions", deck=SPINE, image="s14_spine_regions.jpg",
         header="Vertebral column from the side — name the region",
         back="Mnemonic: breakfast at 7 (7 cervical), lunch at 12 (12 thoracic), dinner at 5 "
              "(5 lumbar), dessert at 5 (5 fused sacral); the coccyx is 3–5 fused.",
         masks=[["cervical", "#box:212,262,305,450"], ["thoracic", "#box:248,450,346,927"],
                ["lumbar", "#box:232,940,282,1180"], ["sacral", "#box:268,1190,380,1352"],
                "coccyx"]),
    dict(id="typical_vertebra_red", deck=SPINE, image="s14_typical_vertebra.png",
         header="Typical vertebra, seen from above. " + RED,
         back="Cue: the body (front) bears weight; the vertebral arch wraps the vertebral "
              "foramen where the spinal cord runs; the spinous and transverse processes are "
              "levers for muscles.",
         tags=["red-box"],
         masks=["Spinous process", "Vertebral arch", "Transverse process",
                "Vertebral foramen", "Body (centrum)"]),
    dict(id="typical_vertebra_other", deck=SPINE, image="s14_typical_vertebra.png",
         header="Typical vertebra, seen from above — the other labeled parts",
         back="Cue: pedicles are the short 'feet' joining the arch to the body, laminae are "
              "the flat plates roofing it behind, and the superior articular processes form "
              "the joints with the vertebra above.",
         masks=["Superior articular process", "Lamina", "Pedicle"]),
    dict(id="atlas_axis", deck=SPINE, image="s15_atlas_axis.jpg",
         header="Atlas (C1) and axis (C2) fitted together, seen from above and behind",
         back="Cue: the dens of C2 pokes up into the front of the atlas's ring, held against "
              "its anterior arch by the transverse ligament — the pivot for turning the head "
              "'no'.",
         masks=["Dens of axis", "Anterior arch", "Transverse ligament", "Atlas (C1)",
                "Posterior arch", "Axis (C2)"]),
    dict(id="cervical_slide", deck=SPINE, image="s15_cervical_labeled.png",
         header="Cervical vertebra, seen from above",
         back="Cue: a hole in each transverse process (transverse foramen) is found ONLY in "
              "cervical vertebrae — it carries the vertebral artery up to the brain.",
         masks=["Bifid Spinous Process", "Transverse Foramen"]),
    dict(id="cervical_model", deck=SPINE, image="m7_10_cervical_model.jpg",
         header="Cervical vertebra (lab model), seen from above at an angle",
         back="Cue: the same parts as any typical vertebra, plus the cervical giveaway — a "
              "transverse foramen in each transverse process.",
         masks=["vertebral foramen", "vertebral arch", "transverse foramen",
                "inferior articular facet", "superior articular facet", "spinous process",
                "pedicle", "lamina", "body"]),
    dict(id="atlas_axis_model", deck=SPINE, image="m7_11_atlas_axis_model.jpg",
         header="Atlas (C1) sitting on the axis (C2), lab model — the renders underneath show "
                "C1 turning on the dens",
         back="Cue: C1 has no body and no spinous process — just an anterior and a posterior "
              "arch joined by the lateral masses; the dens of C2 fills the front of its ring.",
         masks=["superior articular facet (C1)", "dens (odontoid process) (C2)",
                "transverse process (C1)", "anterior tubercle (C1)", "transverse foramen (C1)",
                "anterior arch (C1)", "posterior arch (C1)", "lateral masses (C1)",
                "posterior tubercle (C1)", "spinous process (C2)", "body (C2)"]),
    dict(id="thoracic_vertebra", deck=SPINE, image="s16_thoracic.png",
         header="Thoracic vertebra — seen from above (left) and from the side (right)",
         back="Cue: the costal facets — on the body and on the transverse process — are the "
              "joints for the ribs, found only on thoracic vertebrae; 'corpus' is Latin for "
              "body.",
         masks=[
             ["Superior vertebral notch@1089,160"],
             ["Inferior vertebral notch@1145,614"],
             ["Superior costal facet@836,270", "Superior costal facet@112,619"],
             ["Inferior costal facet@903,617"],
             ["Transverse costal facet@97,383", "Transverse costal facet@1445,456"],
             ["Superior articular facet@293,111", "Superior articular facet@1263,186"],
             ["Inferior articular facet@1067,740"],
             ["Transverse process@64,157"],
             ["Spinous process@404,64", "#box:1395,832,1668,874"],
             ["Vertebral foramen@647,190"],
             ["Corpus@459,780"],
         ]),
    dict(id="lumbar_vertebra", deck=SPINE, image="s17_lumbar_superior.jpg",
         header="Lumbar vertebra, seen from above",
         back="Cue: the massive body is the lumbar giveaway — it carries the whole upper "
              "body's weight; 'spinal canal' here is the vertebral foramen.",
         masks=["Body", "Pedicle", "Transverse Process", "Spinal Canal", "Lamina",
                "Spinous Process"]),

    # ================================= SACRUM & COCCYX =================================
    dict(id="sacrum_red", deck=SACRUM, image="s18_sacrum_coccyx.jpg",
         header="Sacrum and coccyx — front (left) and back (right). " + RED,
         back="Roster: base — broad top surface of S1 · promontory — front lip of S1's body · "
              "ala — the wing on each side of the base · superior articular processes — the "
              "joints with L5 · anterior and posterior sacral foramina — exits for the sacral "
              "nerves · median sacral crest — the fused spinous processes · sacral canal — the "
              "vertebral canal continued · sacral hiatus — the canal's lower opening · apex — "
              "the narrow tip that meets the coccyx",
         tags=["red-box"],
         masks=[["Superior articular process", "Superior articular facet"], "Base of sacrum",
                "Sacral ala", "Anterior sacral promontory", "Anterior sacral foramen",
                "Apex of sacrum", "Sacral canal", "Posterior sacral foramen",
                ["Median sacral crest", "Lateral sacral crest"], "Sacral hiatus"]),
    dict(id="sacrum_other", deck=SACRUM, image="s18_sacrum_coccyx.jpg",
         header="Sacrum and coccyx — front (left) and back (right): the other labeled "
                "landmarks",
         back="Cue: the auricular ('ear-shaped') surface is where the sacrum meets the hip "
              "bone; the transverse lines are the seams where the five sacral vertebrae fused.",
         masks=[["Superior articular facet", "Superior articular process"], "Transverse line",
                ["Lateral sacral crest", "Median sacral crest"], "Sacral tuberosity",
                "Auricular surface", "Sacral cornu", "Coccygeal cornu", "Transverse process"]),

    # ================================== THORACIC CAGE ==================================
    dict(id="sternum", deck=CAGE, image="s20_sternum.jpg",
         header="Sternum, from the front",
         back="Cue: manubrium (handle) + body (blade) + xiphoid process (tip) = a sword; the "
              "sternal angle, where the manubrium meets the body, marks rib 2 — the place to "
              "start counting ribs.",
         masks=["Jugular notch", "Clavicular notch", "Manubrium", "Sternal angle",
                "Facets for attachment of costal cartilages 1-7", "Body", "Xiphoid process"]),
    dict(id="rib", deck=CAGE, image="s20_rib.png",
         header="Typical rib — (A) the whole rib, (B) close-up of its head and neck",
         back="Cue: the head joins the vertebral bodies and the tubercle joins the transverse "
              "process; the costal groove on the lower inner edge shelters the intercostal "
              "nerve and vessels.<br><br>Pitfall: the lab notes say rib markings are NOT "
              "required for the practical — this plate is extra.",
         tags=["optional"],
         masks=["Articular facets@787,1565", "Articular facet@660,1629", "Nonarticular surface@72,1574",
                "Internal surface", "External surface", "Costal cartilage", "Costal groove",
                ["Tubercle@393,103", "Tubercle@459,1265"], ["Neck@320,437", "Neck@733,1240"], "Head", "Angle", "Crest"]),
    dict(id="thoracic_cage_model", deck=CAGE, image="m7_17_thoracic_cage.jpg",
         header="Thoracic cage (lab skeleton), from the front",
         back="Cue: the maroon bars are the costal cartilages — hyaline cartilage joining the "
              "ribs to the sternum; the floating ribs (11–12) end free and never reach the "
              "sternum.",
         masks=["jugular notch", "manubrium", "body of sternum", "costal cartilage (ribs 4-5)",
                "xiphoid process", "floating ribs"]),
]
