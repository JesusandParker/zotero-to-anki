"""
cards_src.py — every cloze note for BIOL 214 W05 (axial skeleton), one dict per note.

  deck  : subdeck under ...::Practical 2::Axial Skeleton
  text  : the Text field (cloze)
  back  : Back Extra (a 1-2 sentence Why first — Parker's explicit ask — then at most one
          more labeled line)
  img   : figure file under ../figures (attached to the BACK unless side="front")
  side  : "front" only when the picture IS the question (identify this vertebra/pin)
  ver   : where the fact was read (slide / speaker notes / lab manual page / Popcorn key)
  num   : True when the answer is a number/range (routes to needs_human_check)

Parker's scope (2026-09-29): every fact on the W05 slides + speaker notes, and "all of the
bones ... all of the parts" — so the lab manual Ch 7 model photos, the blue-page review
questions and the Popcorn Points key are in scope too. The IO plates live in io_spec.py.
"""

BONE = "Bone Basics & Cartilage"
SKULL = "Skull & Hyoid"
FORAMINA = "Skull Foramina & Cranial Floor"
SPINE = "Vertebral Column"
SACRUM = "Sacrum & Coccyx"
CAGE = "Thoracic Cage"

NOTES = [
    # ======================= BONE BASICS & CARTILAGE (slides 2-9) =======================
    dict(deck=BONE, num=True, img="s08_axial_appendicular.jpg",
         ver="slide 2 + speaker notes ('Remember the number of bones'); lab manual p.130 footnote",
         text="An adult human skeleton has {{c1::206::number of bones}} bones.",
         back="Why: a newborn has around 270 separate bony pieces, and many fuse as you grow "
              "(the skull plates, sacrum, and coccyx), which is how the adult count settles at "
              "206.<br><br>Pitfall: the lab manual counts 210 because it adds two sesamoid "
              "bones in each foot. The lab slides use 206."),
    dict(deck=BONE, num=True, img="s08_axial_appendicular.jpg",
         ver="slide 2 ('Axial (80) vs. Appendicular (126)'); slide 8",
         text="Of the adult skeleton's 206 bones, {{c1::80::number of bones}} are axial and "
              "{{c1::126::number of bones}} are appendicular.",
         back="Why: the axial skeleton is only the central pole (skull, ribcage, spine), while "
              "the limbs hold most of the bones — each hand alone has 27."),
    dict(deck=BONE, img="s08_axial_appendicular.jpg",
         ver="slide 8 speaker notes (axis vs appendages)",
         text="Bones that form the body's central axis make up the {{c1::axial::which "
              "division}} skeleton, and the bones of the limbs and the girdles that attach "
              "them make up the {{c1::appendicular::which division}} skeleton.",
         back="Why: 'axial' comes from axis, the midline pole of the body; 'appendicular' "
              "comes from appendage, the parts that hang off it."),
    dict(deck=BONE, img="s08_axial_appendicular.jpg",
         ver="slide 9 review question 4 (True)",
         text="The ribs belong to the {{c1::axial::axial or appendicular}} skeleton.",
         back="Why: the ribs and sternum form the thoracic cage around the body's central "
              "axis; they are not part of a limb.<br><br>Pitfall: the clavicle and scapula "
              "sit on the trunk but are appendicular, because they exist to hang the arm."),
    dict(deck=BONE, img="m7_01_axial_skeleton.jpg",
         ver="slide 8 (Cephalic / Thoracic Cage / Vertebral Column); lab manual p.152",
         text="The axial skeleton has three divisions: the {{c1::skull (cephalic bones)}}, "
              "the {{c1::thoracic cage}}, and the {{c1::vertebral column}}.",
         back="Why: each division wraps bone around something soft and vital, which is the "
              "axial skeleton's main job."),
    dict(deck=BONE, img="m7_01_axial_skeleton.jpg",
         ver="slide 20 ('protects vital thoracic organs'); lab manual p.152; blue page Q2",
         text="Within the axial skeleton, the skull protects the {{c1::brain}}, the thoracic "
              "cage protects the {{c2::heart and lungs}}, and the vertebral column protects the "
              "{{c3::spinal cord}}.",
         back="Why: the axial skeleton is built mainly for protection, while the appendicular "
              "skeleton is built mainly for movement."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 (Flat, Long, Short, Sesamoid, Irregular)",
         text="Bones are classified by shape into five classes: {{c1::flat}}, {{c1::long}}, "
              "{{c1::short}}, {{c1::sesamoid}}, and {{c1::irregular}}.",
         back="Mnemonic: Five Lazy Skeletons Sit Idle = Flat, Long, Short, Sesamoid, Irregular."
              "<br><br>Why: shape follows job: long bones are levers, short bones pack into "
              "blocks, flat bones are shields, sesamoids sit in tendons, and irregular bones "
              "fit an odd job."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 speaker notes (Long: femur, radius, ulna, tibia, fibula); slide 5 Q1",
         text="The femur, radius, ulna, tibia, and fibula are all {{c1::long::shape class}} "
              "bones.",
         back="Why: a long bone is defined by its shape (a shaft with an epiphysis at each "
              "end), not its size, so even the small finger bones count as long bones."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 ('Short: in terms of shaft length') + notes (carpals, tarsals); manual p.131",
         text="The carpal (wrist) and tarsal (ankle) bones are {{c1::short::shape class}} "
              "bones.",
         back="Why: short bones are roughly cube-shaped with no real shaft ('short' describes "
              "the shaft, not the overall size), which lets them pack together into a "
              "flexible block."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 speaker notes (Flat: sternum, ribs, skull bones); manual p.131",
         text="The sternum, the ribs, and the curved plates of the braincase are "
              "{{c1::flat::shape class}} bones.",
         back="Why: thin, plate-like bones make broad shields and wide anchor surfaces for "
              "muscle, ideal for covering the brain, heart, and lungs."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 ('Sesamoid: like a seed') + notes (patella); slide 5 Q2 (False)",
         text="The patella (kneecap) is a {{c1::sesamoid::shape class}} bone.",
         back="Why: sesamoid means 'like a sesame seed': a small, rounded bone that forms "
              "inside a tendon. The patella sits in the quadriceps tendon, protecting it and "
              "improving its leverage over the knee.<br><br>Pitfall: the patella is NOT an "
              "irregular bone."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 speaker notes (Irregular: vertebrae, ... hyoid)",
         text="The vertebrae and the hyoid are {{c1::irregular::shape class}} bones.",
         back="Why: the complicated shapes of these bones (processes, arches, horns) are built for special "
              "jobs and don't fit the long, short, flat, or sesamoid templates."),
    dict(deck=BONE, img="s02_bone_classes.jpg",
         ver="slide 2 speaker notes (Irregular: sphenoid, ethmoid, zygomatic, maxilla, mandible, inferior nasal concha)",
         text="The sphenoid, ethmoid, maxilla, mandible, zygomatic, and inferior nasal concha "
              "are {{c1::irregular::shape class}} bones.",
         back="Pitfall: not every skull bone is flat. Only the curved plates of the skull cap "
              "(like the frontal and parietal) are flat; the complex bones of the face and "
              "cranial floor are irregular."),
    dict(deck=BONE, img="m6_03_bone_markings.jpg",
         ver="slide 3 ('two landmark categories: depressions or projections'); manual p.133",
         text="Bone markings are divided into two landmark categories: {{c1::projections}} "
              "and {{c1::depressions}}.",
         back="Why: a bone's surface is shaped by what touches it. Muscles and ligaments pull "
              "up bumps (projections), while joints, vessels, and nerves leave pits, grooves, "
              "and holes (depressions)."),
    dict(deck=BONE, img="m6_03_bone_markings.jpg",
         ver="slide 3 ('Projections usually serve as attachment points for ligaments and tendons')",
         text="Bone projections usually serve as attachment points for {{c1::ligaments and "
              "tendons::two connective tissues}}.",
         back="Why: the steady pull of a tendon or ligament makes bone build up where it "
              "anchors, so the stronger the muscle, the bigger the projection."),
    dict(deck=BONE, img="m6_07_gross_bone.jpg",
         ver="slide 3 ('Compact (load bearing): densely packed hydroxyapatite'); slide 5 Q3; manual p.134",
         text="{{c1::Compact::compact or spongy}} bone is the {{c2::load-bearing::its job}} "
              "bone, built of densely packed {{c3::hydroxyapatite::mineral}}.",
         back="Why: hydroxyapatite is the calcium-phosphate mineral that makes bone hard; "
              "packed solid with no open spaces, it resists the heavy squeezing a femur's "
              "shaft takes when you stand."),
    dict(deck=BONE, img="m6_08_tibia_forces.jpg",
         ver="slide 3 ('Spongy: trabeculae; better manage stress from multiple directions'); manual p.135",
         text="{{c1::Spongy::compact or spongy}} bone is a lattice of bony struts called "
              "{{c2::trabeculae}}, which handles stress from {{c3::multiple "
              "directions::how many directions}}.",
         back="Why: the struts line up along the lines of force, so the light lattice can "
              "brace against pushes and pulls from many angles at once. That is why it fills "
              "the ends of long bones, where many muscles pull."),
    dict(deck=BONE, img="s05_marrow_section.jpg",
         ver="slide 3 ('Red marrow: site of RBC production')",
         text="Red bone marrow is the site of {{c1::red blood cell (RBC) production::what it "
              "makes}}.",
         back="Why: red marrow is packed with blood-forming stem cells that keep dividing to "
              "replace the millions of red blood cells that wear out every second. It looks "
              "red because it is full of new blood cells."),
    dict(deck=BONE, img="s05_marrow_section.jpg",
         ver="slide 3 ('Yellow marrow: filled with adipose'); manual p.131",
         text="Yellow bone marrow is filled with {{c1::adipose::tissue type}} tissue.",
         back="Why: yellow marrow is mostly fat cells, a lightweight energy store that fills the marrow "
              "cavity without making the bone heavy."),
    dict(deck=BONE, img="s03_long_bone.jpg",
         ver="slide 3 figure + notes (proximal & distal epiphysis, one diaphysis)",
         text="The shaft of a long bone is the {{c1::diaphysis}}, and each knobby end is an "
              "{{c2::epiphysis}}.",
         back="Parts: dia- (between) + -physis (growth); epi- (upon) + -physis. The diaphysis "
              "grows between the ends, and the epiphyses sit upon the shaft.<br><br>Cue: one "
              "diaphysis, but two epiphyses (proximal and distal)."),
    dict(deck=BONE, img="s03_long_bone.jpg",
         ver="slide 3 speaker notes ('distinguish between the proximal and distal epiphysis')",
         text="On the humerus, the epiphysis at the shoulder end is the "
              "{{c1::proximal::proximal or distal}} epiphysis.",
         back="Why: proximal means closer to where the limb attaches to the trunk, and the "
              "shoulder end of the humerus is nearest the trunk."),
    dict(deck=BONE, img="s03_long_bone.jpg",
         ver="slide 3 speaker notes ('distinguish between the proximal and distal epiphysis')",
         text="On the femur, the epiphysis at the knee end is the "
              "{{c1::distal::proximal or distal}} epiphysis.",
         back="Why: distal means farther from where the limb attaches to the trunk, and the "
              "knee end is the femur's far end from the hip."),
    dict(deck=BONE, img="s04_compact_bone.jpg",
         ver="slide 4 ('Osteon: basic structural unit'); slide 5 Q4 (False: osteocyte); manual p.134",
         text="The basic structural unit of compact bone is the {{c1::osteon}}.",
         back="Why: each osteon is a column of bone rings around one central canal, so no "
              "bone cell is ever far from its blood supply.<br><br>Pitfall: NOT the "
              "osteocyte, which is a bone CELL living inside the osteon."),
    dict(deck=BONE, img="m6_05_bone_tissue_400x.jpg",
         ver="slide 4 ('Central canal: contains nerves and vasculature'); manual p.134",
         text="The central canal of an osteon carries {{c1::blood vessels}} and "
              "{{c1::nerves}}.",
         back="Why: bone is living tissue, so every osteon needs a supply line down its "
              "middle; the vessels bring oxygen and nutrients and carry wastes away."),
    dict(deck=BONE, img="s04_compact_bone.jpg",
         ver="slide 4 ('Concentric lamellae') + notes ('layered circles that surround a shared center')",
         text="The layered rings of bone matrix that surround an osteon's central canal are "
              "the {{c1::concentric lamellae}}.",
         back="Why: 'concentric' means sharing a center. The rings all surround the same "
              "central canal, like the rings of a tree trunk or the layers of an onion."),
    dict(deck=BONE, img="m6_05_bone_tissue_400x.jpg",
         ver="slide 4 ('Pockets in concentric lamellae are lacuna and contain osteocytes')",
         text="The small pockets within the concentric lamellae are called {{c1::lacunae}}, "
              "and each one holds an {{c2::osteocyte}}.",
         back="Why: an osteocyte is a mature bone cell walled into hard matrix, and the "
              "lacuna is the little chamber it lives in.<br><br>Distinguish: lacuna = the "
              "space; osteocyte = the cell inside it."),
    dict(deck=BONE, img="m6_05_bone_tissue_400x.jpg",
         ver="slide 4 ('Lacuna are connected to central canal via canaliculi') + notes",
         text="Lacunae are connected to the central canal by tiny channels called "
              "{{c1::canaliculi}}.",
         back="Why: osteocytes are sealed inside hard mineral, so these hair-thin channels are "
              "how nutrients and wastes pass between each cell and the blood vessels in the "
              "central canal."),
    dict(deck=BONE, img="m6_09_growth_plate.jpg",
         ver="slide 6 ('Growth occurs between the diaphysis and the epiphysis in the epiphyseal plate'; 'Diaphysis lengthens') + notes ('growth plate')",
         text="A long bone grows in length at its {{c1::epiphyseal plate}}, and it is the "
              "{{c2::diaphysis::which part}} that lengthens.",
         back="Why: the plate is a band of cartilage between the shaft and the end whose "
              "cells keep dividing, pushing the epiphysis away while bone fills in behind "
              "them.<br><br>Meaning: the epiphyseal plate is also called the growth plate."),
    dict(deck=BONE, img="s06_epiphyseal_plate.jpg",
         ver="slide 6 ('Cartilage growth occurs on distal end of plate while bone is added medially'); manual p.136",
         text="Inside the epiphyseal plate, new cartilage is added on the "
              "{{c1::epiphysis::epiphysis or diaphysis}} side, while bone is added on the "
              "{{c1::diaphysis::epiphysis or diaphysis}} side.",
         back="Why: the plate grows at its outer edge while being turned into bone at its "
              "inner edge, so it creeps outward, pushing the end of the bone away and "
              "lengthening the shaft.<br><br>Meaning: the lab words this as cartilage growth "
              "on the distal end of the plate while bone is added medially."),
    dict(deck=BONE, img="s03_long_bone.jpg",
         ver="slide 6 ('When growth is complete, the plate becomes the epiphyseal line'); slide 9 Q2",
         text="When growth is complete, the epiphyseal plate becomes the {{c1::epiphyseal "
              "line}}.",
         back="Why: once its cartilage stops dividing, bone replaces the whole plate, and the "
              "thin bony line left behind is the scar of the old growth plate."),
    dict(deck=BONE, img="m6_04_long_bone_model.jpg",
         ver="slide 6 speaker notes (plate = cartilage, line = bone); slide 9 Q1 (False: line)",
         text="The epiphyseal plate is made of {{c1::cartilage::bone or cartilage}}, while the "
              "epiphyseal line is made of {{c1::bone::bone or cartilage}}.",
         back="Distinguish: the plate (cartilage) marks where growth is still happening; the "
              "line (bone) marks that growth has ended.<br><br>Pitfall: growth happens at the "
              "plate, never at the line."),
    dict(deck=BONE, img="m6_12_cartilages.jpg",
         ver="slide 7 ('Hyaline: most abundant'; 'Elastic: least abundant'); slide 9 Q3 (False)",
         text="The most abundant cartilage in the body is {{c1::hyaline::cartilage type}} "
              "cartilage, and the least abundant is {{c2::elastic::cartilage type}} "
              "cartilage.",
         back="Why: hyaline is used wherever a smooth, slightly flexible surface is needed "
              "(every joint surface, the rib cartilages, the trachea, the nose), while "
              "elastic is needed only where tissue must bend and spring back: the external "
              "ear and the epiglottis."),
    dict(deck=BONE, img="m6_12_cartilages.jpg",
         ver="slide 7 ('Elastic Cartilage: most flexible'); manual p.139",
         text="The most flexible cartilage is {{c1::elastic::cartilage type}} cartilage.",
         back="Why: elastic cartilage's matrix is threaded with elastic fibers, so it bends and snaps back "
              "into shape. Fold your ear and it springs right back."),
    dict(deck=BONE, img="m6_04_long_bone_model.jpg",
         ver="slide 7 ('Hyaline: covers articulating surfaces; flexible'); manual p.138",
         text="Hyaline cartilage is {{c2::flexible::stiff or flexible}} and covers the "
              "{{c1::articulating surfaces::where on the bone}} of bones.",
         back="Why: hyaline cartilage's glassy-smooth surface cuts friction where two bones meet in a joint, "
              "which is why the cartilage on bone ends is called articular cartilage."),
    dict(deck=BONE, img="s07_disc.jpg",
         ver="slide 7 ('Fibrocartilage: stiff and tough; absorbs force; intervertebral discs and meniscus')",
         text="Of the three cartilages, {{c1::fibrocartilage}} is the stiffest and toughest, "
              "which lets it {{c2::absorb force::what it does}}.",
         back="Why: thick bundles of collagen fibers run through its matrix, so it resists "
              "squeezing and tearing, the right material for shock absorbers like the "
              "intervertebral discs and the knee's meniscus."),

    # ================================ SKULL & HYOID ==================================
    dict(deck=SKULL, img="m7_01_axial_skeleton.jpg",
         ver="slide 8 (Cephalic: Cranial, Facial, Auditory Ossicles, Hyoid); manual p.152",
         text="The cephalic (skull) division of the axial skeleton is made of the "
              "{{c1::cranial bones}}, the {{c1::facial bones}}, the {{c1::auditory "
              "ossicles}}, and the {{c1::hyoid}}.",
         back="Why: the cranial bones box in the brain, the facial bones frame the face, the "
              "six tiny ossicles carry sound across the middle ear, and the hyoid anchors "
              "the tongue."),
    dict(deck=SKULL, img="s10_cranial_bones.png",
         ver="slide 10 (Frontal, Sphenoid, Ethmoid, Temporal, Parietal, Occipital); blue page Q3",
         text="The six cranial bone types, remembered as <b>PEST-OF</b>:<br><br>"
              "{{c1::Parietal::P}}<br><br>{{c1::Ethmoid::E}}<br><br>{{c1::Sphenoid::S}}"
              "<br><br>{{c1::Temporal::T}}<br><br>{{c1::Occipital::O}}<br><br>"
              "{{c1::Frontal::F}}",
         back="Why: together they form the braincase: frontal (forehead), parietals (roof "
              "and upper sides), temporals (sides around the ears), occipital (back and "
              "base), and the sphenoid and ethmoid (the floor, behind and between the eyes)."),
    dict(deck=SKULL, num=True, img="s10_cranial_bones.png",
         ver="slide 10 speaker notes ('Temporal and Parietal Bones are paired ... total of 8 cranial bones')",
         text="The cranium has {{c1::8::number of bones}} bones, because the "
              "{{c2::parietal}} and {{c2::temporal}} bones come in left and right pairs.",
         back="Why: six bone types with two of them doubled (6 + 2 = 8). The frontal, "
              "occipital, sphenoid, and ethmoid are single bones that cross the midline."),
    dict(deck=SKULL, num=True, img="s11_facial_bones.png",
         ver="slide 11 speaker notes ('14 total Facial Bones')",
         text="The face has {{c1::14::number of bones}} bones.",
         back="Why: eight bone types; six come in left and right pairs (12 bones) and two "
              "are single, so 12 + 2 = 14."),
    dict(deck=SKULL, img="s11_facial_bones.png",
         ver="slide 11 speaker notes ('Unpaired Bones: Mandible, Vomer')",
         text="The only two UNPAIRED facial bones are the {{c1::mandible}} and the "
              "{{c1::vomer}}.",
         back="Why: both sit exactly on the midline (the mandible is one U-shaped jawbone and "
              "the vomer is one thin blade in the nasal septum), so there is no left and right "
              "copy."),
    dict(deck=SKULL, img="m7_07_sinuses.jpg",
         ver="lab manual p.156 ('Four bones in the skull contain hollow pockets called sinuses'); Popcorn Points slide 5 key",
         text="Four skull bones contain air-filled sinuses: the {{c1::frontal}}, "
              "{{c1::ethmoid}}, {{c1::sphenoid}}, and {{c1::maxillary}} bones.",
         back="Why: the mucus-lined air pockets drain into the nasal cavity, which is why a "
              "cold or allergy can cause sinus pressure and sinus headaches."),
    dict(deck=SKULL, img="m7_07_sinuses.jpg",
         ver="lab manual p.156 (sinuses lighten the facial bones; amplify the voice); blue page Q4",
         text="Two likely functions of the skull's sinuses are to {{c1::lighten the "
              "skull::effect on weight}} and to {{c2::give the voice resonance::effect on "
              "sound}}.",
         back="Why: hollow, air-filled bone weighs far less than solid bone, and the air "
              "spaces act like the body of a guitar, amplifying and coloring the voice."),
    dict(deck=SKULL, img="m7_05_mandible.jpg",
         ver="blue page Q5 (mental foramen); lab manual p.156",
         text="The mental foramen is an opening in the {{c1::mandible::bone}}.",
         back="Why: the mental foramen sits on the front of the jaw below the premolars and lets nerves and "
              "blood vessels out to the skin and muscles of the chin and lower lip."),
    dict(deck=SKULL, img="m7_02b_skull_obl_ant.jpg",
         ver="blue page Q5 (infraorbital foramen); lab manual p.155",
         text="The infraorbital foramen is an opening in the {{c1::maxilla (maxillary "
              "bone)::bone}}.",
         back="Why: the infraorbital foramen sits just below the eye socket (infra-orbital) and passes nerves and "
              "vessels to the skin and muscles of the cheek and upper lip."),
    dict(deck=SKULL, img="m7_02a_skull_post_lat.jpg",
         ver="blue page Q5 (supraorbital foramen); lab manual p.152 and Fig 7-18 (notch 75%, foramen 25%)",
         text="The supraorbital foramen (or notch) is part of the {{c1::frontal::bone}} "
              "bone.",
         back="Why: the supraorbital foramen sits on the upper rim of the eye socket (supra-orbital) and lets "
              "nerves and vessels reach the forehead. In about three of four people it is an "
              "open notch rather than a closed hole."),
    dict(deck=SKULL, img="m7_02a_skull_post_lat.jpg",
         ver="blue page Q5 (mastoid process); lab manual p.152",
         text="The mastoid process is part of the {{c1::temporal::bone}} bone.",
         back="Why: the mastoid process is the bump you can feel behind your ear; the sternocleidomastoid "
              "muscle pulls on it to turn and tilt the head."),
    dict(deck=SKULL, img="m7_02a_skull_post_lat.jpg",
         ver="blue page Q5 (temporal process); lab manual p.155 and Fig 7-2",
         text="The zygomatic arch is formed by the temporal process of the "
              "{{c1::zygomatic::bone}} bone joining the zygomatic process of the "
              "{{c1::temporal::bone}} bone.",
         back="Why: each process is named for the bone it reaches toward, so the names cross "
              "over; the two meet in the middle to make the cheekbone arch.<br><br>Cue: you "
              "can feel the arch just in front of your ear."),
    dict(deck=SKULL, img="m7_05_mandible.jpg",
         ver="lab manual p.156 ('the only skull bone that moves')",
         text="The only skull bone you can move at will is the {{c1::mandible::bone}}.",
         back="Why: the mandible hinges against the temporal bone just in front of the ear; lowering it "
              "opens the mouth and raising it closes the mouth."),
    dict(deck=SKULL, img="s13_hyoid.jpg",
         ver="slide 13 ('Floats at the level of cervical vertebrae 3')",
         text="The hyoid bone 'floats' in the neck at the level of vertebra "
              "{{c1::C3::region + number}}.",
         back="Why: the hyoid sits just above the larynx (Adam's apple), roughly level with the third "
              "cervical vertebra, in the angle between the chin and the neck."),
    dict(deck=SKULL, img="m7_06_hyoid.jpg",
         ver="slide 13 ('Does not articulate other bones'); manual p.156",
         text="The hyoid is said to 'float' in the neck because it {{c1::does not articulate "
              "with any other bone}}.",
         back="Why: instead of a joint, it is slung in place by ligaments and muscles, which "
              "is what lets it rise and fall when you swallow."),
    dict(deck=SKULL, img="m7_02b_skull_obl_ant.jpg",
         ver="slide 13 ('Attached by ligaments from styloid and hangs like a swing'); manual p.152 + Fig 7-2 (styloid process, temporal bone)",
         text="The hyoid hangs like a swing from ligaments attached to the "
              "{{c1::styloid processes::bony projections}} of the {{c2::temporal::bone}} "
              "bones.",
         back="Why: the stylohyoid ligaments run from the pointed styloid processes just below "
              "the ears down to the hyoid's lesser horns.<br><br>Pitfall: one sentence of the "
              "lab manual says sphenoid; everywhere else the manual (correctly) puts the "
              "styloid processes on the temporal bone."),
    dict(deck=SKULL, img="s13_hyoid.jpg",
         ver="slide 13 ('Serves as attachment site for other muscles'); manual p.156 (tongue, swallowing)",
         text="The hyoid serves as an attachment site for the muscles of the {{c1::tongue}} "
              "and of {{c1::swallowing}}.",
         back="Why: because it floats, muscles pulling on it from above and below can lift "
              "and lower the throat, the motion you feel when you swallow."),
    dict(deck=SKULL, img="s13_hyoid.jpg",
         ver="slide 13 ('Cornu = horn')",
         text="In anatomy, {{c1::cornu}} means {{c2::horn}}.",
         back="Ex: the hyoid's greater and lesser cornua stick out like horns, and the sacrum "
              "and coccyx have cornua too.<br><br>Cue: Latin cornu, as in unicorn."),

    # ======================== SKULL FORAMINA & CRANIAL FLOOR ========================
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (red-boxed foramina on the sphenoid)",
         text="The optic canal and the foramina rotundum, ovale, and spinosum all pierce the "
              "{{c1::sphenoid::bone}} bone.",
         back="Why: the sphenoid sits in the middle of the cranial floor, right where the "
              "nerves headed for the eye and face have to leave the skull."),
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (foramen magnum, hypoglossal canal); blue page Q5; manual p.152",
         text="The foramen magnum and the hypoglossal canals are openings in the "
              "{{c1::occipital::bone}} bone.",
         back="Why: the occipital bone forms the back of the cranial floor, where the spinal "
              "cord (foramen magnum) and the tongue's nerve (hypoglossal canal) leave the "
              "skull."),
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (Ethmoid bone: cribriform plate; cribriform foramina)",
         text="The cribriform foramina perforate the cribriform plate of the "
              "{{c1::ethmoid::bone}} bone.",
         back="Why: 'cribriform' means sieve-like; dozens of tiny holes let the smell "
              "(olfactory) nerve fibers pass up from the nose to the brain."),
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (Temporal bone, petrous part; internal acoustic meatus); manual p.152",
         text="The internal acoustic meatus is an opening in the {{c1::temporal::bone}} "
              "bone.",
         back="Why: the inner ear is housed entirely inside the temporal bone, so the nerves "
              "for hearing and balance (with the facial nerve) enter it through this canal."),
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (jugular foramen)",
         text="The jugular foramen lies between the {{c1::temporal}} and {{c1::occipital}} "
              "bones.",
         back="Why: the jugular foramen is the gap left where the two bones meet at the back of the cranial "
              "floor; the internal jugular vein and cranial nerves IX, X, and XI leave "
              "through it."),
    dict(deck=FORAMINA, img="s12_cranial_foramina.png",
         ver="slide 12 (hypophyseal fossa of sella turcica); blue page Q5; manual p.152",
         text="The sella turcica is part of the {{c1::sphenoid::bone}} bone.",
         back="Why: the sella turcica, a saddle-shaped pocket ('Turkish saddle') in the middle "
              "of the cranial floor, holds and protects the pituitary gland."),

    # ================================ VERTEBRAL COLUMN ================================
    dict(deck=SPINE, img="s14_spine_regions.jpg",
         ver="slide 14 (cervical, thoracic, lumbar, sacral, coccyx) + notes",
         text="From top to bottom, the regions of the vertebral column are:<br><br>"
              "{{c1::cervical}}<br><br>{{c1::thoracic}}<br><br>{{c1::lumbar}}<br><br>"
              "{{c1::sacral}}<br><br>{{c1::coccygeal}}",
         back="Why: the regions follow the body from neck to chest to lower back to pelvis "
              "to tailbone."),
    dict(deck=SPINE, num=True, img="m7_08_spinal_curves.jpg",
         ver="slide 8 (Cervical (7)); slide 15 (C1-C7) + slide 14 notes mnemonic",
         text="The cervical region of the spine has {{c1::7::number of vertebrae}} "
              "vertebrae.",
         back="Mnemonic: eat cereal for breakfast at 7 am, so 7 cervical.<br><br>Cue: nearly "
              "every mammal, even a giraffe, has exactly seven neck vertebrae."),
    dict(deck=SPINE, num=True, img="m7_08_spinal_curves.jpg",
         ver="slide 8 (Thoracic (12)); slide 16 (T1-T12) + slide 14 notes mnemonic",
         text="The thoracic region of the spine has {{c1::12::number of vertebrae}} "
              "vertebrae.",
         back="Mnemonic: a turkey sandwich for lunch at 12 noon, so 12 thoracic.<br><br>Why: "
              "one thoracic vertebra for each of the 12 pairs of ribs."),
    dict(deck=SPINE, num=True, img="m7_08_spinal_curves.jpg",
         ver="slide 8 (Lumbar (5)); slide 17 (L1-L5) + slide 14 notes mnemonic",
         text="The lumbar region of the spine has {{c1::5::number of vertebrae}} vertebrae.",
         back="Mnemonic: lobster for dinner at 5 pm, so 5 lumbar.<br><br>Why: five massive "
              "vertebrae carry the whole upper body's weight down to the pelvis."),
    dict(deck=SPINE, img="m7_08_spinal_curves.jpg",
         ver="slide 14 (cervical Concave, thoracic Convex, lumbar Concave, sacral Convex); manual Fig 7-8; blue page Q8, Q14",
         text="Viewed from behind, the spinal curves alternate: the cervical curve is "
              "{{c1::concave::concave or convex}}, the thoracic curve is "
              "{{c1::convex::concave or convex}}, the lumbar curve is "
              "{{c1::concave::concave or convex}}, and the sacral curve is "
              "{{c1::convex::concave or convex}}.",
         back="Why: alternating curves turn the spine into a spring that absorbs shock and "
              "keeps the head balanced over the hips.<br><br>Pitfall: seen from the front, "
              "every word flips."),
    dict(deck=SPINE, img="s14_typical_vertebra.png",
         ver="slide 14 (Body (centrum), red-boxed); manual p.157-158",
         text="The thick, drum-shaped front part of a vertebra that bears weight is the "
              "{{c1::body (centrum)::part}}.",
         back="Why: the bodies stack with discs between them to form the load-bearing "
              "column, and they get larger from neck to lower back as the weight they carry "
              "increases."),
    dict(deck=SPINE, img="s14_typical_vertebra.png",
         ver="slide 14 (Vertebral foramen, red-boxed); manual p.157; blue page Q12",
         text="The large opening in a vertebra that the spinal cord passes through is the "
              "{{c1::vertebral foramen}}.",
         back="Why: stacked one above another, the vertebral foramina line up into the "
              "vertebral canal, a bony tunnel around the spinal cord."),
    dict(deck=SPINE, img="s14_typical_vertebra.png",
         ver="slide 14 (Vertebral arch, Pedicle, Lamina); manual p.157 ('arch is formed by the laminae posteriorly, the pedicles laterally')",
         text="The vertebral arch is formed by two {{c1::pedicles}} on the sides and two "
              "{{c2::laminae}} behind.",
         back="Why: the pedicles are the short 'feet' that anchor the arch to the body, and "
              "the laminae are the flat plates that roof it over behind the spinal cord."),
    dict(deck=SPINE, img="s16_thoracic.png",
         ver="slide 14 (superior articular process); manual p.157 ('superior articular facets and inferior articular facets at which they articulate with the vertebrae above and below')",
         text="Each vertebra joins the vertebrae above and below it at its "
              "{{c1::articular processes (facets)::which processes}}.",
         back="Why: the smooth facets on these paired processes glide against their "
              "neighbors, letting the spine bend and twist while staying stacked."),
    dict(deck=SPINE, img="s07_disc.jpg",
         ver="slide 7 (intervertebral foramen); manual p.156; blue page Q16",
         text="Spinal nerves exit the vertebral column through the {{c1::intervertebral "
              "foramina}}.",
         back="Why: each opening is framed by the notches of two stacked vertebrae, so the "
              "column can fully enclose the spinal cord yet still let a pair of nerves out at "
              "every level."),
    dict(deck=SPINE, img="s15_atlas_axis.jpg",
         ver="slide 15 ('C1=atlas') + notes",
         text="{{c1::C1::vertebra}} is called the {{c2::atlas}}.",
         back="Why: C1 is named for Atlas, the Titan who held up the world; C1 holds up the "
              "skull, which rocks on it for the 'yes' nod."),
    dict(deck=SPINE, img="s15_atlas_axis.jpg",
         ver="slide 15 ('C2=axis') + notes",
         text="{{c1::C2::vertebra}} is called the {{c2::axis}}.",
         back="Why: the dens of C2 is the pivot (axis) that the atlas and skull rotate around when "
              "you shake your head 'no'."),
    dict(deck=SPINE, img="m7_11_atlas_axis_model.jpg",
         ver="slide 15 ('Dens'); manual p.158",
         text="The tooth-shaped process that projects up from C2 is the {{c1::dens}}.",
         back="Why: the atlas fits around the dens like a ring on a peg, held in place by the "
              "transverse ligament, so the head can rotate side to side.<br><br>Meaning: dens "
              "means tooth; it is also called the odontoid process."),
    dict(deck=SPINE, img="m7_11_atlas_axis_model.jpg",
         ver="slide 15 notes ('Be comfortable differentiating between C1 and C2'); manual Fig 7-11",
         text="Of the first two vertebrae, the ring with no body and no spinous process is "
              "{{c1::C1 (atlas)::which vertebra}}, and the one with an upward peg (the dens) "
              "is {{c1::C2 (axis)::which vertebra}}.",
         back="Why: during development the body of C1 fuses onto C2 as the dens, which is why "
              "the atlas is left as a ring and the axis gains its peg."),
    dict(deck=SPINE, img="m7_08_spinal_curves.jpg",
         ver="slide 15 ('C7=vertebral prominens') + notes ('palpate C7 at base of posterior neck'); blue page Q15",
         text="{{c1::C7::vertebra}} is called the {{c2::vertebra prominens}}.",
         back="Why: C7's long spinous process makes the bump you can feel at the base of the "
              "back of your neck, the easiest vertebra to palpate."),
    dict(deck=SPINE, img="s15_cervical_labeled.png",
         ver="slide 15 notes ('Transverse foramen are only found in cervical vertebrae'); blue page Q13",
         text="{{c1::Transverse foramina::openings}} are found only in {{c2::cervical::region}} "
              "vertebrae.",
         back="Why: the holes in the cervical transverse processes carry the vertebral arteries up "
              "the neck to the brain.<br><br>Pitfall: the lab manual says the carotid "
              "arteries pass through them; it is the vertebral arteries (the carotids run in "
              "front of the spine)."),
    dict(deck=SPINE, img="s16_thoracic.png",
         ver="slide 16 ('Costal facets that articulate with ribs') + notes ('Costal facets are only found on thoracic vertebrae')",
         text="The only vertebrae with {{c1::costal facets::joint surfaces}} for the ribs are "
              "the {{c2::thoracic::region}} vertebrae.",
         back="Why: 'costa' means rib. Each rib's head and tubercle make joints on a thoracic "
              "vertebra's body and transverse process, and the costal facets are those joint "
              "surfaces."),
    dict(deck=SPINE, img="m7_13_vertebra_regions.jpg",
         ver="slides 15-17 (small body / medium size body / large bodies); manual p.158",
         text="Vertebral bodies get {{c1::larger::larger or smaller}} from the cervical region "
              "down to the lumbar region.",
         back="Why: each lower vertebra carries more body weight; cervical bodies hold up only "
              "the head, while lumbar bodies carry the head, arms, and whole trunk."),
    dict(deck=SPINE, img="s15_cervical_superior.png",
         ver="slide 15 (Identifying Characteristics: large vertebral foramina, transverse foramen, bifid spinous process, small body) + notes",
         text="A cervical vertebra is identified by a {{c1::small::small, medium, or large}} "
              "body, a {{c1::large::small, medium, or large}} vertebral foramen, "
              "{{c1::transverse foramina}}, and a {{c1::bifid::shape}} spinous process.",
         back="Meaning: bifid means split in two at the tip.<br><br>Cue: from above, a "
              "cervical vertebra looks like a face smiling at you."),
    dict(deck=SPINE, img="m7_14_giraffe_moose.jpg",
         ver="slide 16 (Medium size body; Costal facets; Vertically angled spinous process) + notes (giraffe)",
         text="A thoracic vertebra is identified by a {{c1::medium-sized::small, medium, or "
              "large}} body, {{c1::costal facets}} where the ribs articulate, and a long "
              "spinous process that points steeply {{c1::downward::direction}}.",
         back="Cue: from the side it looks like a giraffe's head, with the long, down-slanting "
              "spinous process as the neck.<br><br>Why: the steep, overlapping spinous "
              "processes stop the thoracic spine from bending far backward, which protects "
              "the chest."),
    dict(deck=SPINE, img="m7_14_giraffe_moose.jpg",
         ver="slide 17 (Large bodies; More horizontal spinous process; Triangular vertebral foramen) + notes (moose)",
         text="A lumbar vertebra is identified by a {{c1::large::small, medium, or large}} "
              "body, a {{c1::triangular::shape}} vertebral foramen, and a spinous process "
              "that sticks out more {{c1::horizontally::direction}}.",
         back="Cue: from the side it looks like a moose's head: a massive body with a short, "
              "square spinous process jutting straight back.<br><br>Why: the huge bodies "
              "carry more weight than any other vertebrae."),
    dict(deck=SPINE, side="front", img="pp7_a_thoracic.jpg",
         ver="Popcorn Points slide 7 key ('Which vertebra is thoracic? A')",
         text="Vertebra A, a lab model seen from the side: which region is it from? "
              "{{c1::thoracic::region}}",
         back="Why: the long spinous process slants steeply down like a giraffe's neck, and "
              "the body is medium-sized with small smooth costal facets for the ribs."),
    dict(deck=SPINE, side="front", img="pp7_b_lumbar.jpg",
         ver="Popcorn Points slide 7 key ('Which vertebra is lumbar? B')",
         text="Vertebra B, a lab model seen from the side: which region is it from? "
              "{{c1::lumbar::region}}",
         back="Why: the massive body and the short, square spinous process jutting straight "
              "back give it the moose-head silhouette."),
    dict(deck=SPINE, side="front", img="pp7_c_cervical.jpg",
         ver="Popcorn Points slide 7 key ('Which vertebra is cervical? C')",
         text="Vertebra C, a lab model seen from above at an angle: which region is it from? "
              "{{c1::cervical::region}}",
         back="Why: the small body, the big triangular vertebral foramen, and a hole in each "
              "transverse process (transverse foramen) only occur together in the neck."),
    dict(deck=SPINE, side="front", img="s17_lumbar_photo.jpg",
         ver="slide 17 photo (lumbar vertebra)",
         text="A vertebra seen from the side, body on the right: which region is it from? "
              "{{c1::lumbar::region}}",
         back="Why: the huge, boxy body and the short, hatchet-shaped spinous process pointing "
              "straight back are the lumbar giveaways."),
    dict(deck=SPINE, side="front", img="s15_cervical_superior.png",
         ver="slide 15 photo (cervical vertebra, superior view) + notes ('look like they are smiling at you')",
         text="A vertebra seen from above: which region is it from? {{c1::cervical::region}}",
         back="Why: a hole in each transverse process (transverse foramen) is found only in "
              "cervical vertebrae, and the small body with a large triangular foramen "
              "confirms it."),
    dict(deck=SPINE, side="front", num=True, img="pp3_front_trunk.png",
         ver="Popcorn Points slide 3 key ('15 thoracic vertebra (12)')",
         text="Skeleton seen from the front: name the specific vertebra at pin 15 (region and "
              "number). {{c1::T12::region + number}}",
         back="Why: T12 is the last vertebra that carries a rib; follow the lowest (floating) "
              "rib back to the spine to find it."),
    dict(deck=SPINE, side="front", num=True, img="pp3_front_trunk.png",
         ver="Popcorn Points slide 3 key ('16 lumbar vertebra (3)')",
         text="Skeleton seen from the front: name the specific vertebra at pin 16 (region and "
              "number). {{c1::L3::region + number}}",
         back="Why: the lumbar vertebrae start right below the last rib-bearing vertebra "
              "(T12); count down three from there."),
    dict(deck=SPINE, img="s19_abnormal_curves.png",
         ver="slide 19 ('Scoliosis: Abnormal lateral curvature'); blue page Q9",
         text="{{c1::Scoliosis}} is an abnormal {{c2::lateral (sideways)::direction}} "
              "curvature of the spine.",
         back="Why: all the normal spinal curves are front-to-back, so any S- or C-shaped bend "
              "seen from behind is abnormal."),
    dict(deck=SPINE, img="s19_abnormal_curves.png",
         ver="slide 19 ('Kyphosis: exaggerated thoracic curvature') + notes ('hunchback'); blue page Q10",
         text="{{c1::Kyphosis}} is an exaggerated {{c2::thoracic::region}} curvature of the "
              "spine.",
         back="Why: kyphosis rounds the upper back forward into a hunchback, which is the lab's "
              "nickname for it."),
    dict(deck=SPINE, img="s19_abnormal_curves.png",
         ver="slide 19 ('Lordosis: exaggerated lumbar curvature') + notes ('common in pregnant women'); blue page Q11",
         text="{{c1::Lordosis}} is an exaggerated {{c2::lumbar::region}} curvature of the "
              "spine.",
         back="Why: the lower back sways inward; it is common in pregnancy, when the growing "
              "belly pulls the lumbar spine forward."),

    # ================================= SACRUM & COCCYX =================================
    dict(deck=SACRUM, num=True, img="s18_sacrum_coccyx.jpg",
         ver="slide 18 ('Sacrum is 5 fused vertebrae'; S1-5) + slide 14 notes mnemonic",
         text="The sacrum is {{c1::5::number of vertebrae}} fused vertebrae.",
         back="Mnemonic: sweets for dessert with dinner at 5, so 5 fused sacral vertebrae."
              "<br><br>Why: five vertebrae fused into one solid wedge make a strong base that "
              "passes the upper body's weight to the hip bones."),
    dict(deck=SACRUM, num=True, img="s18_sacrum_coccyx.jpg",
         ver="slide 18 ('Coccyx is 3-5 fused vertebrae') + notes ('The textbook says 4-5 ... We want you to remember 3-5')",
         text="The coccyx is {{c1::3–5::number of vertebrae}} fused vertebrae.",
         back="Why: the coccyx is the remnant of a tail, and the number of segments varies from "
              "person to person.<br><br>Pitfall: the textbook says 4–5, but the lab wants "
              "3–5."),
    dict(deck=SACRUM, img="m7_15_sacrum_photos.jpg",
         ver="slide 18 (Median sacral crest, red-boxed); lab manual Fig 7-15 ('median sacral crest (fused spinous processes)')",
         text="The median sacral crest is formed by the fused {{c1::spinous "
              "processes::which part of a vertebra}} of the sacral vertebrae.",
         back="Why: when the five sacral vertebrae fused, their spinous processes merged into "
              "one bumpy ridge running down the middle of the sacrum's back."),
    dict(deck=SACRUM, img="m7_15_sacrum_photos.jpg",
         ver="slide 18 (Sacral canal, Sacral hiatus, red-boxed); lab manual p.159",
         text="The sacral canal is the lower end of the {{c1::vertebral canal}}, and it opens "
              "at the bottom as the {{c2::sacral hiatus}}.",
         back="Why: the canal carries the last nerve roots of the spinal cord through the "
              "sacrum; the hiatus is the gap where the lowest sacral laminae never fused."),
    dict(deck=SACRUM, img="s18_sacrum_coccyx.jpg",
         ver="lab manual p.159 ('It articulates with L5 superiorly, the coccyx inferiorly and the ox coxae anterolaterally')",
         text="The sacrum joins {{c1::L5::vertebra}} above, the {{c2::coccyx}} below, and the "
              "{{c3::hip bones (os coxae)::bones}} on each side.",
         back="Why: the sacrum is the keystone of the pelvis; the spine's weight comes down through it "
              "and passes out sideways to the hip bones at the sacroiliac joints."),

    # ================================== THORACIC CAGE ==================================
    dict(deck=CAGE, num=True, img="m7_16_sternum_model.jpg",
         ver="slide 20 ('Sternum is three fused bones') + notes",
         text="The sternum is {{c1::three::number of bones}} fused bones.",
         back="Why: the sternum starts as separate pieces that fuse over time; the xiphoid process is "
              "the last part to ossify and fuse."),
    dict(deck=CAGE, img="s20_sternum.jpg",
         ver="slide 20 ('Manubrium, Body of sternum, and Xiphoid Process') + notes",
         text="From top to bottom, the three parts of the sternum are:<br><br>"
              "{{c1::manubrium}}<br><br>{{c1::body}}<br><br>{{c1::xiphoid process}}",
         back="Cue: the sternum looks like a sword: manubrium = the handle, body = the blade, "
              "xiphoid ('sword-shaped') = the tip."),
    dict(deck=CAGE, img="m7_17_thoracic_cage.jpg",
         ver="slide 20 figure + notes ('jugular notch'); manual p.160",
         text="The notch on the top of the manubrium, between the clavicles, is the "
              "{{c1::jugular notch}}.",
         back="Why: you can feel it as the dip at the base of your neck, right in front of "
              "the trachea."),
    dict(deck=CAGE, img="s20_sternum.jpg",
         ver="slide 20 figure + notes ('sternal angle')",
         text="The ridge where the manubrium joins the body of the sternum is the "
              "{{c1::sternal angle}}.",
         back="Why: the sternal angle is easy to feel and sits level with the second rib, so it is the "
              "starting point for counting ribs."),
    dict(deck=CAGE, img="m7_17_thoracic_cage.jpg",
         ver="slide 20 ('Ribs attached to sternum via costal cartilages'); manual p.160 (hyaline)",
         text="Ribs attach to the sternum by {{c1::costal cartilages}}, which are made of "
              "{{c2::hyaline::cartilage type}} cartilage.",
         back="Why: flexible cartilage bars let the ribcage spring open each time you breathe "
              "instead of acting like a rigid bony box."),
    dict(deck=CAGE, num=True, img="s20_rib_groups.png",
         ver="slide 20 ('True: ribs 1-7') + notes ('attach directly to sternum via their own costal cartilage')",
         text="The true ribs are ribs {{c1::1–7::rib numbers}}, and each attaches to the "
              "sternum by {{c2::its own costal cartilage::how}}.",
         back="Why: a direct cartilage link of its own to the sternum is what makes a rib "
              "'true'."),
    dict(deck=CAGE, num=True, img="s20_rib_groups.png",
         ver="slide 20 ('False: 8-12') + notes ('do NOT attach directly ... ribs 8, 9, & 10 share a costal cartilage'); slide 8 (floating listed under false)",
         text="In the BIOL 214 lab's scheme, the false ribs are ribs {{c1::8–12::rib "
              "numbers}}; ribs 8–10 reach the sternum only by joining the costal cartilage of "
              "rib {{c2::7::rib number}}.",
         back="Why: a false rib has no costal cartilage of its own running to the sternum; "
              "ribs 11–12 never reach the sternum at all.<br><br>Distinguish: BIOL 313 and "
              "the lab manual split them three ways (false = 8–10 only); the lab slides count "
              "the floating ribs among the false ribs."),
    dict(deck=CAGE, num=True, img="m7_17_thoracic_cage.jpg",
         ver="slide 20 ('Floating ribs 11-12') + notes ('do NOT attach to sternum')",
         text="The floating ribs are ribs {{c1::11–12::rib numbers}}, which {{c2::never "
              "attach to the sternum::their front attachment}}.",
         back="Why: the front ends of ribs 11–12 stop short in the muscles of the abdominal wall; they "
              "connect only to the vertebrae behind, so they seem to float."),
    dict(deck=CAGE, num=True, img="s08_rib_counts.png",
         ver="slide 8 ('True Ribs (14 total)') + notes ('memorize ... the number of True, False, and Floating Ribs')",
         text="Counting both sides, there are {{c1::14::number of ribs}} true ribs.",
         back="Why: seven true ribs on each side (ribs 1–7), and 7 × 2 = 14."),
    dict(deck=CAGE, num=True, img="s08_rib_counts.png",
         ver="slide 8 ('False Ribs (10 total)') + notes",
         text="Counting both sides, there are {{c1::10::number of ribs}} false ribs, floating "
              "ribs included.",
         back="Why: five false ribs on each side (ribs 8–12), and 5 × 2 = 10."),
    dict(deck=CAGE, num=True, img="s08_rib_counts.png",
         ver="slide 8 ('Floating (4 total)') + notes",
         text="Counting both sides, there are {{c1::4::number of ribs}} floating ribs.",
         back="Why: two floating ribs on each side (ribs 11–12), and 2 × 2 = 4."),
    dict(deck=CAGE, num=True, img="s08_rib_counts.png",
         ver="slide 8 ('Ribs (24)'); manual p.160",
         text="The adult thoracic cage has {{c1::24::number of ribs}} ribs.",
         back="Why: one pair of ribs for each of the 12 thoracic vertebrae (12 × 2 = 24)."),
]
