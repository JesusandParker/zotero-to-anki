#!/usr/bin/env python3
"""Writer pass for genetics chapter 9 (2026-08-08). Emits chapter_9_cards.json.

Kept as a script so the editor/consolidation stages can regenerate deterministically.
Cards 0.. are Parker's-marks lane; blocks prefixed X_cov are the Claude-coverage lane
(he delegated selection for the unmarked pages). All numeric values verified against
the physical pages cited in verified_against by reading the page text this session.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "chapter_9_cards.json")
cards = []

def card(text, back, idxs, block, numeric=False, va=None, vb=None, kind=None, lexicon=None):
    c = {
        "Text": text,
        "Back Extra": back,
        "source": "genetics",
        "segment": 9,
        "from_idx": idxs,
        "block": block,
        "numeric": numeric,
        "verified_against": va,
        "verified_by": vb,
        "needs_human_check": False,
        "visual_source": None,
        "image": None,
    }
    if kind:
        c["kind"] = kind
    if lexicon:
        c["lexicon"] = lexicon
    cards.append(c)

AGENT = "agent, read from page text this run"

# ============================== A. Proof: transformation (his marks) ==============
card(
    "Chromosomes are composed of two types of macromolecules: {{c1::nucleic acids}} and {{c1::proteins}}.",
    "Why: the classic 1940s–50s experiments (Avery's transformation work, Hershey–Chase) established that the genetic information lives in the nucleic acids, not the proteins.<br><br>Cue: the two kinds of nucleic acid are DNA and RNA.",
    [1], "A_proof_transformation")

card(
    "In Griffith's experiment, mice injected with a mix of heat-killed virulent Type IIIS and living avirulent Type IIR pneumococci {{c1::died of pneumonia}}, and {{c1::living Type IIIS}} cells were recovered from their carcasses.",
    "Cue: neither part alone kills — the IIIS cells are dead and the living IIR strain is avirulent.<br><br>Why: something heritable must have passed from the dead IIIS cells into the living IIR cells.",
    [6], "A_proof_transformation")

card(
    "The unknown agent from heat-killed Type IIIS cells that converted living Type IIR cells into Type IIIS was named the {{c1::“transforming principle”::historic term}} — the conversion changed the cells' {{c2::hereditary material::what kind of material}}.",
    "Distinguish: the conversion is genetic, not a temporary change in appearance — the transformed cells breed true as Type IIIS.",
    [9], "A_proof_transformation")

card(
    "In {{c1::1931::year}}, {{c1::Richard Sia and Martin Dawson::two researchers}} showed that pneumococcal transformation happens {{c2::in vitro — the mice played no role::where}}.",
    "Why: Griffith's original experiment ran inside mice; showing the same conversion in a culture dish proved the animal contributed nothing.<br><br>Cue: their in vitro system set the stage for Avery, MacLeod, and McCarty.",
    [10], "A_proof_transformation", numeric=True, va="p212", vb=AGENT)

card(
    "{{c1::Oswald Avery, Colin MacLeod, and Maclyn McCarty::three researchers}} showed that {{c2::DNA::molecule}} is the only component of Type IIIS cells able to transform Type IIR cells into Type IIIS.",
    "Distinguish: Griffith discovered THAT transformation happens; Avery's team identified WHAT does the transforming.<br><br>Cue: the purified transforming extract kept working after protein and RNA were destroyed — only destroying DNA stopped it.",
    [12], "A_proof_transformation")

card(
    "To rule out protein contamination of their DNA extract, Avery's team destroyed one candidate molecule at a time: transforming activity survived {{c1::protease}} and {{c1::RNase}} treatment but was eliminated entirely by {{c2::DNase::enzyme}}.",
    "Why: each enzyme degrades exactly one macromolecule, so the treatment that kills the activity names the molecule carrying it.",
    [13, 17], "A_proof_transformation")

card(
    "A cell-free bacterial extract carries genetic information of unknown molecular identity. Treating it with DNase destroys the activity, while protease and RNase leave it intact. The information is stored in {{c1::DNA::molecule}}.",
    "Cue: the logic runs backward from destruction — whichever single enzyme abolishes the activity, its substrate is the carrier.",
    [13, 17], "A_proof_transformation")

# ============================== B. Proof: Hershey-Chase (his marks) ===============
card(
    "Proof that DNA is the genetic material of bacteriophage T2 was published in {{c1::1952::year}} by {{c1::Alfred Hershey and Martha Chase::two researchers}}.",
    "Cue: Hershey went on to win the 1969 Nobel Prize.<br><br>Distinguish: Avery's team proved it by transformation in pneumococcus; Hershey and Chase proved it by radioactive labeling of a phage.",
    [18], "B_hershey_chase", numeric=True, va="p213", vb=AGENT)

card(
    "The Hershey–Chase labeling strategy exploits one chemical difference: {{c1::phosphorus::element}} is found in DNA but not protein, while {{c1::sulfur::element}} is found in protein but virtually absent from DNA.",
    "Why: with an element unique to each macromolecule, a radioactive isotope of that element tags one molecule cleanly.",
    [21], "B_hershey_chase")

card(
    "In the Hershey–Chase experiment, growing phage in medium with radioactive {{c1::³²P::isotope}} labeled the phage {{c2::DNA}}, and growing them with radioactive {{c1::³⁵S::isotope}} labeled the phage {{c2::protein coats}}.",
    "Why: DNA contains phosphorus but no sulfur; protein contains sulfur but virtually no phosphorus.",
    [22, 21], "B_hershey_chase")

card(
    "Hershey and Chase found that the phage's {{c1::DNA}} entered the E. coli cell, while most of the phage's {{c1::protein}} remained adsorbed to the outside of the cell.",
    "Why: progeny viruses are assembled inside the cell, so whatever entered must carry the instructions for building them — the genetic material is the DNA.<br><br>Ex: progeny particles carried some of the parental ³²P but none of the ³⁵S.",
    [20], "B_hershey_chase")

card(
    "In the Hershey–Chase experiment, shearing ³⁵S-labeled infected cells in a blender removed most of the radioactivity {{c1::without affecting::with or without affecting}} progeny phage production.",
    "Why: the sheared-off material was empty protein coats — reproduction runs entirely on the DNA already inside the cell.<br><br>Distinguish: with ³²P-labeled phage, essentially all the radioactivity stayed inside the cells and could not be sheared away.",
    [22, 20], "B_hershey_chase")

card(
    "The loose end in Hershey and Chase's proof — a significant amount of {{c1::³⁵S (protein)::isotope}} entered the cells with the DNA — was closed by {{c2::transfection}} experiments, in which E. coli {{c2::protoplasts::cell preparation}} infected with pure phage DNA yield normal progeny phage.",
    "Why: if naked DNA alone produces complete infective progeny, no protein contaminant can be the genetic material.<br><br>Cue: a protoplast is a cell with its wall removed.",
    [126, 23], "B_hershey_chase")

# ============================== C. Proof: RNA viruses (his marks) =================
card(
    "Most living organisms store their genetic information in {{c1::DNA}}; some viruses instead store it in {{c2::RNA}}.",
    "Cue: those viruses contain RNA and proteins but no DNA at all.<br><br>Why: every organism studied stores its genetic information in a nucleic acid — never in protein.",
    [23], "C_rna_viruses")

card(
    "RNA was established as the genetic material of RNA viruses by the {{c1::reconstitution}} experiment of {{c1::Heinz Fraenkel-Conrat::researcher}} and coworkers, published in {{c1::1957::year}}.",
    "Cue: the experiment mixed and matched the two components of tobacco mosaic virus — protein coat from one strain, RNA from another.",
    [24], "C_rna_viruses", numeric=True, va="p215", vb=AGENT)

card(
    "Fraenkel-Conrat reconstituted hybrid TMV particles from the {{c1::protein coat}} of strain A and the {{c1::RNA}} of strain B; the progeny viruses were always identical to the strain that donated the {{c2::RNA::protein coat or RNA}}.",
    "Why: offspring follow the nucleic acid, not the coat — so TMV's genes are its RNA.<br><br>Cue: TMV contains no DNA at all, just one RNA molecule in a protein coat.",
    [28], "C_rna_viruses",
    vb="answer_in_stem cleared: c2 is a forced choice between the two components the stem must name; recall is which one, not the word")

# ============================== D. History (coverage) =============================
card(
    "In {{c1::1868::year}}, {{c1::Johann Friedrich Miescher::person}} isolated an acidic, phosphorus-rich substance from pus-cell nuclei and named it {{c2::“nuclein”}} — the first isolation of what we now call nucleic acid.",
    "Cue: a skeptical journal editor repeated the experiments himself, delaying publication until 1871.<br><br>Why: nitrogen and phosphorus together was an oddity — at the time the pair was known to coexist only in certain fats.",
    [30], "D_cov_history", numeric=True, va="p211", vb=AGENT)

card(
    "Two dates frame molecular genetics: the genetic role of nucleic acids was established in {{c1::1944::year}}, and the double-helix structure of DNA was solved in {{c1::1953::year}}.",
    "Distinguish: Miescher had isolated nuclein back in 1868 — it took ~75 years to prove what it was for.",
    [31], "D_cov_history", numeric=True, va="p211", vb=AGENT)

# ============================== E. Nucleotides & bases (coverage) =================
card(
    "The repeating subunit of a nucleic acid is the {{c1::nucleotide}}.",
    "Cue: a poly-nucleotide chain is just many of these joined in a row.",
    [32], "E_cov_nucleotides")

card(
    "Each nucleotide is composed of three parts:<br><br>{{c1::a phosphate group}}<br><br>{{c1::a five-carbon sugar (pentose)}}<br><br>{{c1::a cyclic, nitrogen-containing base}}",
    "Cue: sugar + base + phosphate — the sugar sits in the middle, bridging the other two.",
    [33], "E_cov_nucleotides")

card(
    "The pentose sugar in DNA is {{c1::2-deoxyribose}}; in RNA it is {{c1::ribose}}.",
    "Cue: the names carry the answer — DEOXYribonucleic acid vs RIBOnucleic acid.<br><br>Distinguish: deoxyribose lacks the hydroxyl (OH) group at the 2′ carbon that ribose carries.",
    [34], "E_cov_nucleotides", vb="husk_groups cleared: each blank is cued by its own key (DNA vs RNA), answerable with the other hidden")

card(
    "The four bases commonly found in DNA are {{c1::adenine (A)}}, {{c1::guanine (G)}}, {{c1::thymine (T)}}, and {{c1::cytosine (C)}}.",
    "Distinguish: RNA keeps A, G, and C but swaps thymine for uracil.",
    [34], "E_cov_nucleotides")

card(
    "RNA contains the base {{c1::uracil (U)}} in place of DNA's {{c1::thymine (T)}}.",
    "Cue: U replaces T — the other three bases (A, G, C) are shared by both nucleic acids.",
    [35], "E_cov_nucleotides")

card(
    "The double-ring bases (purines) are {{c1::adenine and guanine::2 bases}}.",
    "Mnemonic: PURe As Gold — the two purines are A and G.<br><br>Distinguish: purines have two rings but only two members; pyrimidines have one ring and three members.",
    [36], "E_cov_nucleotides")

card(
    "The single-ring bases (pyrimidines) are {{c1::cytosine, thymine, and uracil::3 bases}}.",
    "Mnemonic: CUT the PY — the pyrimidines are C, U, and T.<br><br>Cue: DNA uses C and T; RNA uses C and U.",
    [36], "E_cov_nucleotides")

card(
    "RNA usually exists as a {{c1::single::single or double}}-stranded polymer, whereas DNA is usually {{c1::double::single or double}}-stranded.",
    "Pitfall: “usually” matters — some viral genomes break the pattern (ΦX174 packages single-stranded DNA).",
    [37], "E_cov_nucleotides")

# ============================== F. The double helix (coverage) ====================
card(
    "In {{c1::1953::year}}, {{c1::James Watson and Francis Crick::two researchers}} deduced that DNA is a {{c2::right::right or left}}-handed double helix — two polynucleotide chains coiled about one another in a spiral.",
    "Cue: the model rested on two kinds of evidence — Chargaff's base chemistry and Wilkins & Franklin's X-ray diffraction data.",
    [38, 42], "F_cov_double_helix", numeric=True, va="p217, p219", vb=AGENT)

card(
    "The 1962 Nobel Prize for the double helix went to Watson, Crick, and {{c1::Maurice Wilkins::third laureate}}.",
    "Pitfall: Rosalind Franklin, whose X-ray data were central, died in 1958 at age 37 — and Nobel Prizes are never awarded posthumously.",
    [43], "F_cov_double_helix", numeric=True, va="p219", vb=AGENT)

card(
    "Chargaff's chemical analysis of DNA from many organisms: the concentration of thymine always equals that of {{c1::adenine}}, the concentration of cytosine always equals that of {{c1::guanine}}, and total purines always equal total {{c2::pyrimidines}}.",
    "Why: fixed pairwise ratios hinted that T sits with A and C sits with G in some fixed physical relationship — the base pairs Watson and Crick then modeled.",
    [39, 40], "F_cov_double_helix")

card(
    "Double-stranded DNA is 33% guanine. Its adenine content is {{c1::17%::percent}}.",
    "Pathway: %G = %C → G+C = 66% → A+T = 100−66 = 34% → A = 17%.<br><br>Pitfall: this arithmetic is only legal for DOUBLE-stranded nucleic acid — single strands have no strict pairing.",
    [56], "F_cov_double_helix", numeric=True, va="p221 (book's own worked answer)", vb=AGENT)

card(
    "Chargaff-style base arithmetic (%A from %G) fails for the DNA packaged in phage ΦX174, because that DNA is {{c1::single::single or double}}-stranded — there is no strict base pairing.",
    "Pitfall: exam stems love this trap — check WHETHER the nucleic acid is double-stranded before using A=T and G=C.",
    [57], "F_cov_double_helix")

card(
    "The X-ray diffraction data behind the double-helix model came from {{c1::Maurice Wilkins and Rosalind Franklin::two researchers}}, and showed a highly ordered, two-stranded structure with repeats every {{c2::0.34 nm::distance}} along the axis.",
    "Cue: the cross-shaped diffraction pattern says “helix”; the strong top/bottom bands say “stacked bases, 0.34 nm apart.”",
    [41], "F_cov_double_helix", numeric=True, va="p219", vb=AGENT)

card(
    "Within one DNA strand, adjacent nucleotides are joined by covalent {{c1::phosphodiester}} bonds; the two strands of the helix are held together by {{c2::hydrogen}} bonds between opposing bases.",
    "Distinguish: strong covalent bonds build the backbone; individually weak (but numerous) hydrogen bonds zip the strands together.<br><br>Cue: a phosphodiester linkage runs C—O—P—O—C, joining the 5′ carbon of one sugar to the 3′ carbon of the next.",
    [44, 45], "F_cov_double_helix")

card(
    "Watson–Crick base pairing is specific: adenine always pairs with {{c1::thymine}}, and guanine always pairs with {{c1::cytosine}} — so every base pair consists of one {{c2::purine}} and one {{c2::pyrimidine}}.",
    "Why: the pairing is set by the bases' hydrogen-bonding capacities in their normal configurations — A cannot hydrogen-bond with C, nor T with G.",
    [46], "F_cov_double_helix")

card(
    "A–T base pairs form {{c1::two::number of}} hydrogen bonds; G–C pairs form {{c1::three::number of}}.",
    "Why: the third bond makes G:C-rich DNA denser and harder to pull apart.",
    [47, 103], "F_cov_double_helix", numeric=True, va="p220", vb=AGENT)

card(
    "Because base pairing is strict, the sequence of one DNA strand fixes the sequence of the other — the two strands are said to be {{c1::complementary}}.",
    "Why: complementarity is what makes DNA uniquely suited to store and transmit genetic information — each strand can serve as the template for rebuilding the other (the heart of replication, Chapter 10).",
    [48], "F_cov_double_helix")

card(
    "One DNA strand reads 5′-ATCG-3′. Written in the conventional 5′→3′ direction, its complementary strand is {{c1::5′-CGAT-3′}}.",
    "Pathway: pair each base (TAGC), then read the new strand from ITS OWN 5′ end — i.e., reverse it.<br><br>Pitfall: writing TAGC forgets the reversal; the convention is always 5′ on the left.",
    [127, 48], "F_cov_double_helix")

card(
    "In the B-DNA double helix, base pairs stack {{c1::0.34 nm::distance}} apart, with {{c1::10::bp per turn}} base pairs per full 360° turn.",
    "Distinguish: DNA inside cells averages 10.4 base pairs per turn — the textbook 10 is the idealized model.",
    [49, 54], "F_cov_double_helix", numeric=True, va="p220-221", vb=AGENT)

card(
    "The two sugar-phosphate backbones of a double helix run in opposite directions — one 5′→3′, the other 3′→5′ — a relationship called {{c1::antiparallel::orientation term}}.",
    "Why: this opposite chemical polarity shapes how replication, transcription, and recombination must work.",
    [50], "F_cov_double_helix")

card(
    "Double-helix stability comes from two forces: the many weak {{c1::hydrogen bonds}} between paired bases, and the hydrophobic {{c1::base-stacking forces}} between adjacent stacked pairs.",
    "Why: the flat faces of the base pairs are nonpolar, so the stacked core hides from water — in an aqueous cell that insolubility itself holds the helix together.",
    [51], "F_cov_double_helix", vb="husk_groups cleared: blanks are cued independently ('between paired bases' vs 'between adjacent stacked pairs'), each cold-solvable")

card(
    "The double helix's surface carries two unequal {{c1::grooves::helix feature}} — and gene-regulatory proteins read them: some bind one groove, others the other.",
    "Distinguish: the major groove is the much wider one; the minor groove is the narrower. The difference matters for protein-DNA recognition.",
    [52], "F_cov_double_helix")

# ============================== G. A/B/Z and supercoiling (coverage) ==============
card(
    "{{c1::B}}-DNA is the conformation DNA takes under physiological conditions — a {{c2::right::right or left}}-handed helix with about 10 base pairs per turn.",
    "Cue: the vast majority of DNA in living cells is B-form; the Watson–Crick model IS B-DNA.",
    [53, 54], "G_cov_dna_forms")

card(
    "{{c1::A}}-DNA forms in high salt or partial dehydration — right-handed like B-DNA but shorter and thicker, with {{c2::11::bp per turn}} base pairs per turn.",
    "Why it matters in vivo: DNA–RNA heteroduplexes and RNA–RNA duplexes adopt a very similar structure, even though pure DNA almost never sits in the A form inside cells.",
    [55, 58], "G_cov_dna_forms", numeric=True, va="p221", vb=AGENT)

card(
    "{{c1::Z}}-DNA is the {{c2::left::right or left}}-handed double-helical form — named for the {{c2::zigzag}} path of its backbone — occurring in {{c3::G:C-rich}} sequences with alternating purines and pyrimidines.",
    "Pitfall: Z-DNA's function in living cells is still unclear.<br><br>Cue: 12 base pairs per turn, a single deep groove.",
    [59, 60], "G_cov_dna_forms")

card(
    "Supercoils enter DNA when one or both strands are {{c1::cleaved}}, the ends are {{c1::twisted around each other}}, and — the precondition — the molecule's ends are {{c2::fixed (not free to rotate)}}.",
    "Ex: circular chromosomes fix their own ends; eukaryotic linear DNA is fixed by attachments to non-DNA chromosome components — both can therefore be supercoiled.",
    [61, 62], "G_cov_dna_forms")

card(
    "Twisting cut DNA in the same direction as the helix winds produces a {{c1::positive::positive or negative}} supercoil ({{c2::overwound::overwound or underwound}} DNA); twisting opposite to the winding produces a {{c1::negative}} supercoil ({{c2::underwound}} DNA).",
    "Cue: with-the-twist = over; against-the-twist = under.",
    [63], "G_cov_dna_forms")

card(
    "In vivo, the functional DNA of almost all organisms is {{c1::negatively::positively or negatively}} supercoiled.",
    "Pitfall: the exception — the DNA of some viruses infecting Archaea is POSITIVELY supercoiled.<br><br>Why: negative supercoiling is involved in replication, recombination, and the regulation of gene expression.",
    [64], "G_cov_dna_forms")

# ============================== H. Viral & prokaryotic chromosomes (coverage) =====
card(
    "In most viruses and prokaryotes, all the genes reside in {{c1::a single chromosome}} consisting of {{c1::one molecule of nucleic acid (DNA or RNA)}}.",
    "Distinguish: exceptions exist — Vibrio cholerae carries a second chromosome, and many prokaryotes also carry small plasmids.",
    [65], "H_cov_prokaryote")

card(
    "Not every DNA genome is double-stranded: bacteriophage {{c1::ΦX174::phage}} packages its genome as {{c2::single}}-stranded DNA.",
    "Cue: 5386 nucleotides, 11 genes — the ultimate in genetic economy.<br><br>Pitfall: single-strandedness is why Chargaff arithmetic fails on ΦX174.",
    [66, 57], "H_cov_prokaryote")

card(
    "The E. coli K12 genome is {{c1::4.6 million::number}} base pairs of DNA.",
    "Distinguish: prokaryotic genomes generally run from just under 2 million to over 5 million base pairs, carrying roughly 2000–5000 genes.",
    [67], "H_cov_prokaryote", numeric=True, va="p223", vb=AGENT)

card(
    "The E. coli chromosome's circular DNA has a contour length of about {{c1::1500 μm::length}} — packed into a cell only 1–2 μm across.",
    "Why: a molecule ~1000× longer than its container forces an extremely condensed, folded state.",
    [68], "H_cov_prokaryote", numeric=True, va="p224", vb=AGENT)

card(
    "The functional state of a bacterial chromosome is the {{c1::folded genome}}: the DNA is organized into {{c2::50 to 100::how many}} loops (domains), each one {{c3::independently negatively supercoiled}}.",
    "Cue: RNA and protein are both structural components of the folded genome — it is not naked DNA.",
    [69, 70], "H_cov_prokaryote", numeric=True, va="p224", vb=AGENT)

card(
    "Probing the folded genome:<br><br>One single-strand DNase nick → relaxes {{c1::only the nicked domain::one domain or all}}<br><br>RNase → {{c1::unfolds the loops; supercoiling unchanged}}",
    "Why: supercoiling is per-domain (so a nick relaxes locally), while the folding itself hangs on RNA anchors — cut those and the loops open, still supercoiled.",
    [71, 72], "H_cov_prokaryote")

# ============================== I. Chromatin & histones (coverage) ================
card(
    "The compaction of a chromosome's material into a much smaller volume for mitosis or meiosis is called {{c1::condensation}}.",
    "Why: tight metaphase packaging eases segregation into daughter nuclei and keeps chromosomes from tangling and breaking.<br><br>Cue: interphase chromosomes are metabolically active but nearly invisible; metaphase chromosomes are thick, visible bodies on the spindle.",
    [73, 96], "I_cov_chromatin")

card(
    "Chemical analysis shows chromatin consists primarily of {{c1::DNA}} and {{c1::proteins}}, with lesser amounts of {{c1::RNA}}.",
    "Distinguish: the DNA and histone contents are relatively constant; the nonhistone protein fraction varies with the isolation procedure.",
    [74], "I_cov_chromatin")

card(
    "Chromatin's proteins fall into two classes: the basic, positively charged {{c1::histones}}, and the heterogeneous, largely acidic {{c1::nonhistone chromosomal proteins}}.",
    "Distinguish: histones = packaging hardware, nearly identical everywhere; nonhistones = diverse, cell-type-specific — the likely gene regulators.",
    [75], "I_cov_chromatin")

card(
    "All plants and animals have five histone types: {{c1::H1, H2a, H2b, H3, and H4::5 names}}.",
    "Cue: four of them (H2a, H2b, H3, H4) build the nucleosome core; H1 works outside it.",
    [76], "I_cov_chromatin")

card(
    "The five histones occur in molar ratios of approximately {{c1::1 H1 : 2 H2a : 2 H2b : 2 H3 : 2 H4::ratio}}.",
    "Why: the 2:2:2:2 stoichiometry is the octamer — two of each core histone per nucleosome — with a single H1 per complete nucleosome.",
    [78], "I_cov_chromatin", numeric=True, va="p225",
    vb=AGENT + "; bloated_blank cleared: the ratio is one numeric chunk recalled as a unit, hint labels it")

card(
    "Histones are basic because 20–30% of their amino acids are {{c1::arginine and lysine::2 amino acids}} — their positive charges grip DNA's negatively charged {{c2::phosphate}} backbone.",
    "Mechanism: exposed –NH₃⁺ groups make histones polycations; DNA is a polyanion — electrostatic attraction does the binding.",
    [80, 79], "I_cov_chromatin", numeric=True, va="p225-226", vb=AGENT)

card(
    "Histone exception: in some {{c1::sperm::cell type}}, histones are replaced by another class of small basic proteins called {{c2::protamines}}.",
    "Cue: almost every other cell type in plants and animals keeps the standard five histones.",
    [77], "I_cov_chromatin")

card(
    "The nearly invariant core histones fit a {{c1::structural / DNA-packaging::structural or regulatory}} role; the widely varying nonhistone proteins fit a {{c1::gene-regulatory::structural or regulatory}} role.",
    "Why: a protein doing the same mechanical job everywhere cannot afford to change; regulators must differ between cell types precisely because gene expression differs.",
    [81, 82], "I_cov_chromatin")

# ============================== J. One molecule per chromosome (coverage) =========
card(
    "Each eukaryotic chromosome contains {{c1::one single, giant::how many}} DNA molecule, continuous through the centromere.",
    "Ex: every fully sequenced yeast chromosome reads end-to-end as one continuous molecule.",
    [83], "J_cov_one_molecule")

card(
    "Kavenoff and Zimm sized the largest Drosophila DNA by its stretch-relaxation behavior in solution; the result was unchanged by treatment with {{c1::pronase (a protein-degrading enzyme)::treatment}} — so a chromosome is {{c2::one continuous DNA molecule}}, not segments glued by protein linkers.",
    "Mechanism: the time a stretched DNA coil takes to relax scales with molecule size; the largest molecule matched the whole chromosome's DNA content — with or without its proteins.",
    [84], "J_cov_one_molecule")

# ============================== K. Nucleosomes (coverage) =========================
card(
    "Gently isolated interphase chromatin looks like beads on a string: ellipsoidal beads about {{c1::11 nm::diameter}} across — the {{c2::nucleosomes}} — joined by thin threads of nuclease-sensitive {{c2::linker DNA}}.",
    "Cue: the beads protect their DNA from nucleases; the exposed linkers between them are where nucleases cut.",
    [85, 87], "K_cov_nucleosomes", numeric=True, va="p227", vb=AGENT)

card(
    "Partial nuclease digestion of chromatin releases DNA fragments in discrete sizes that are {{c1::integral multiples of the smallest fragment::size pattern}} — evidence that chromatin has a repeating structural unit.",
    "Why: protected DNA comes in fixed-size packets (nucleosomes); cutting different numbers of exposed linkers yields 1×, 2×, 3×… packet sizes.",
    [86, 87], "K_cov_nucleosomes")

card(
    "The nucleosome core is {{c1::146::bp count}} nucleotide pairs of DNA wrapped around {{c2::a histone octamer::what structure}} — two molecules each of {{c3::H2a, H2b, H3, and H4::4 histones}}.",
    "Cue: extensive nuclease digestion chews everything except this protected 146-bp core particle.",
    [88, 89], "K_cov_nucleosomes", numeric=True, va="p228", vb=AGENT)

card(
    "In the nucleosome core, the DNA winds {{c1::1.65::number of turns}} times around the outside of the histone octamer as a negative superhelix.",
    "Cue: X-ray diffraction at 0.28-nm resolution located all eight histones and the wound DNA precisely.",
    [90], "K_cov_nucleosomes", numeric=True, va="p228", vb=AGENT)

card(
    "The complete nucleosome contains {{c1::166::bp count}} nucleotide pairs — two full superhelical turns — stabilized by one molecule of {{c2::histone H1::which histone}} bound to the outside of the structure.",
    "Distinguish: the core alone is 146 bp and involves only the octamer histones — H1 is NOT part of the octamer.",
    [91, 92], "K_cov_nucleosomes", numeric=True, va="p228", vb=AGENT)

card(
    "Between nucleosome cores, the {{c1::linker DNA}} varies in length from species to species and cell type to cell type (reported from 8 to 114 bp).",
    "Cue: the cores are invariant; the linkers are where the variability lives.",
    [93], "K_cov_nucleosomes", numeric=True, va="p228", vb=AGENT)

# ============================== L. Packaging levels (coverage) ====================
card(
    "The chromatin fibers of metaphase chromosomes average {{c1::30 nm::diameter}} in diameter — formed by condensing the 11-nm nucleosome fiber.",
    "Cue: carefully isolated interphase chromatin shows the same 30-nm fibers — the light microscope simply sees where they pack tightly.",
    [94], "L_cov_packaging", numeric=True, va="p229", vb=AGENT)

card(
    "The two competing models for the 30-nm fiber's substructure are the {{c1::solenoid}} model and the {{c1::zigzag}} model.",
    "Cue: the zigzag appears when chromatin is cryopreserved (quick-frozen) rather than chemically fixed; which structure exists in vivo — or whether both do — is still uncertain.",
    [95], "L_cov_packaging")

card(
    "Eukaryotic DNA is packaged through three levels of condensation:<br><br>Level 1 — DNA wound into nucleosomes → {{c1::the 11-nm interphase chromatin fiber}}<br><br>Level 2 — folding/supercoiling with histone H1 → {{c1::the 30-nm chromatin fiber}}<br><br>Level 3 — nonhistone scaffold → {{c1::supercoiled loops/domains of the metaphase chromosome}}",
    "Cue: 2-nm naked DNA → 11-nm beads → 30-nm fiber → scaffold-anchored loops — a lengthwise compression of several thousand-fold.<br><br>Roster: Level 1 = 11-nm nucleosome fiber · Level 2 = 30-nm fiber (H1) · Level 3 = scaffold loops → metaphase chromosome.",
    [98, 99, 100], "L_cov_packaging")

card(
    "The central core of a metaphase chromosome — the {{c1::scaffold}} — is composed of {{c2::nonhistone::histone or nonhistone}} chromosomal proteins.",
    "Ex: strip the histones from an isolated metaphase chromosome and the scaffold remains, shaped like the chromosome, surrounded by a huge halo of DNA.",
    [97, 100], "L_cov_packaging")

# ============================== M. Repetitive DNA (coverage) ======================
card(
    "The human genome has about {{c1::700::factor}}× more DNA than E. coli's but only {{c1::4.5::factor}}× more genes — because human genes are larger AND much human DNA is {{c2::nongenic}}.",
    "Cue: the nongenic majority was once dismissed as “junk” DNA — now known to matter for chromosome structure.",
    [101], "M_cov_repetitive", numeric=True, va="p231", vb=AGENT)

card(
    "In density-gradient centrifugation, the genomic fractions that settle away from the main band (because they are G:C- or A:T-rich) are called {{c1::satellite DNAs}} — short sequences repeated over and over.",
    "Cue: from Latin satelles, “attendant” — side bands attending the main band.",
    [102], "M_cov_repetitive")

card(
    "G:C-rich DNA settles {{c1::lower (it is denser)::higher or lower}} in a density gradient than typical DNA, because G:C pairs' {{c2::tighter hydrogen bonding (three bonds)::bonding property}} packs the molecule denser; A:T-rich DNA rides higher.",
    "Cue: three bonds beat two — same reason G:C-rich DNA also needs more heat to melt apart.",
    [103, 47], "M_cov_repetitive")

card(
    "Heating DNA to near 100°C separates its strands — {{c1::denaturation}}; cooling slowly lets complementary strands re-form double helices — {{c1::renaturation}}.",
    "Why: heat breaks the many weak hydrogen bonds; slow cooling gives complements time to find each other.",
    [104, 105], "M_cov_repetitive", numeric=True, va="p232", vb=AGENT)

card(
    "In renaturation experiments, repetitive sequences re-form duplexes {{c1::faster::faster or slower}} than unique sequences, because they are relatively {{c2::more concentrated — present many times over}}.",
    "Cue: renaturation rate tracks concentration — the basis for separating repetitive from unique DNA and estimating repetition.",
    [106], "M_cov_repetitive")

card(
    "The number of times a sequence is repeated in a genome is its {{c1::copy number}}; highly repetitive (satellite) sequences reach {{c2::10³ to 10⁶::range}} copies.",
    "Distinguish: eukaryotic genomes are a mix of unique, moderately repetitive, and highly repetitive sequence classes — unique sequences hold most of the genes.",
    [107, 108], "M_cov_repetitive", numeric=True, va="p232 (superscripts restored: 103→10³, 106→10⁶)", vb=AGENT)

card(
    "Exception to “genes are unique sequences”: the {{c1::ribosomal RNA::which RNA}} genes are highly redundant — hundreds or even thousands of copies per genome.",
    "Why: cells carry enormous numbers of ribosomes, so rRNA demand outstrips what single-copy genes could supply.",
    [128], "M_cov_repetitive")

card(
    "{{c1::In situ hybridization}} finds a sequence's chromosomal home: a labeled single-stranded {{c2::probe}} renatures with its complement in chromosomes spread on a slide, and the label (usually a fluorescent dye) marks the spot.",
    "Cue: Latin “in position” — the hybrid forms exactly where the complement naturally sits; this is the basis of chromosome painting.",
    [109], "M_cov_repetitive")

card(
    "Highly repetitive DNA is concentrated primarily {{c1::in the regions around the centromeres::where}} of eukaryotic chromosomes.",
    "Distinguish: less highly repetitive sequences sit out in the chromosome arms — some in tandem arrays, others dispersed (many of those dispersed ones are mobile transposons).",
    [110], "M_cov_repetitive")

card(
    "Transposable elements (transposons) and their derivatives make up about {{c1::44::percent}}% of the human genome.",
    "Distinguish: ~15% in Drosophila melanogaster; over 80% in maize.<br><br>Cue: dispersed repetitive sequences that can move to new genomic positions.",
    [111], "M_cov_repetitive", numeric=True, va="p233", vb=AGENT)

# ============================== N. Centromeres (coverage) =========================
card(
    "Spindle microtubules attach to a chromosome at its {{c1::kinetochores}} — complex protein structures assembled on the {{c2::centromeres}} of the sister chromatids.",
    "Why: that attachment is what moves sister chromatids to opposite poles — the basis of proper disjunction in mitosis and meiosis.",
    [112], "N_cov_centromeres")

card(
    "A chromosome or fragment that lacks a centromere is usually {{c1::lost::its fate}} during cell division.",
    "Why: with nothing for spindle microtubules to grab, the fragment cannot be pulled into either daughter nucleus.",
    [113], "N_cov_centromeres")

card(
    "The simplest known centromeres belong to {{c1::yeast (Saccharomyces cerevisiae)::organism}} — a DNA segment only {{c2::125::bp count}} base pairs long is sufficient for proper mitotic behavior.",
    "Distinguish: the centromeres of multicellular plants and animals span thousands to millions of base pairs of repetitive DNA.",
    [114], "N_cov_centromeres", numeric=True, va="p233", vb=AGENT)

card(
    "Human centromeres are built of long tandem arrays of the {{c1::alpha satellite}} sequence — a {{c2::171::bp count}}-bp repeat present in 5000–15,000 copies per centromere.",
    "Cue: whole centromeres run 500,000 to 1.5 million bp — these massive repeat arrays are exactly why centromeric DNA resisted sequencing.",
    [115], "N_cov_centromeres", numeric=True, va="p233", vb=AGENT)

card(
    "{{c1::Heterochromatin}} stains deeply and is packaged more tightly; {{c1::euchromatin}} stains less deeply and is looser.",
    "Ex: centromeres and their flanking (pericentric) regions are heterochromatin — mostly repetitive, though some genes (e.g., rRNA gene arrays in Drosophila) live there.",
    [116], "N_cov_centromeres")

card(
    "The centromere-marking protein {{c1::CENP-A::protein}} is a variant of histone {{c2::H3::which histone}} that binds eukaryotic centromeres — even yeast's tiny ones.",
    "Cue: in complex centromeres a methylated H3 is present too, and Heterochromatin Protein 1 (HP1) may help package the region.",
    [117], "N_cov_centromeres")

# ============================== O. Telomeres (coverage) ===========================
card(
    "The specialized structures at the ends of eukaryotic chromosomes are the {{c1::telomeres}} — the term was coined in {{c2::1938::year}} by {{c2::Hermann J. Muller::person}}.",
    "Parts: telo- (Greek telos, end) + -mere (meros, part) — literally “end part.”<br><br>Cue: prokaryotes' circular chromosomes have no ends, so they need no telomeres.",
    [118], "O_cov_telomeres", numeric=True, va="p233", vb=AGENT)

card(
    "Telomeres serve three functions:<br><br>{{c1::they block nucleases from degrading the ends of linear DNA}}<br><br>{{c1::they prevent the ends from fusing with other DNA molecules}}<br><br>{{c1::they let the ends replicate fully, without loss of material}}",
    "Cue: protect · don't stick · finish copying — broken (telomere-less) ends notoriously fuse to each other.",
    [119], "O_cov_telomeres")

card(
    "The telomere repeat unit of humans — and vertebrates generally — is {{c1::TTAGGG::6 bases}}.",
    "Distinguish: Tetrahymena uses TTGGGG; Arabidopsis uses TTTAGGG — the general pattern is 5′ T₁₄A₀₁G₁₈ 3′.<br><br>Cue: conserved across 100+ vertebrate species, from fishes to mammals.",
    [120], "O_cov_telomeres")

card(
    "Normal human somatic telomeres (500–3000 TTAGGG repeats) gradually {{c1::shorten::shorten or lengthen}} with age — but the telomeres of {{c2::germ-line cells and cancer cells::2 cell types}} do not.",
    "Why it matters: telomere length ties into aging and the unlimited division of cancer cells (Chapter 10 takes this up with telomerase).",
    [121], "O_cov_telomeres", numeric=True, va="p234", vb=AGENT)

card(
    "Most telomeres end in a G-rich, single-stranded {{c1::3′::3′ or 5′}} overhang, which can invade an upstream stretch of telomere repeats and pair with the complementary strand — forming a protective loop called a {{c2::t-loop}}.",
    "Cue: human 3′ overhangs run 50–500 bases (ciliates': only 12–16).<br><br>Why: tucking the free end away hides it from nucleases and repair enzymes.",
    [122, 123], "O_cov_telomeres")

card(
    "Telomeric DNA is coated and protected by the six-protein complex {{c1::shelterin}}: {{c2::TRF1 and TRF2}} bind the double-stranded repeats, while {{c2::POT1}} binds the single-stranded overhang.",
    "Cue: TIN2 and TPP1 tether POT1 to the TRFs, and TRF2-associated Rap1 helps regulate telomere length.<br><br>Why: shelterin shields telomeric DNA from degradation and from being “repaired” as damage.",
    [124, 125], "O_cov_telomeres")

# ============================== P. Lexicon (his purple marks) =====================
def lex(term, key, method, page, text, back, idxs):
    card(text, back, idxs, "P_lexicon", kind="lexicon",
         lexicon={"term": term, "term_key": key,
                  "anchor": {"method": method, "page": str(page)}})

lex("chromosome", "chromosom", "glossary", 609,
    "A <b>chromosome</b> is {{c1::one packaged unit of a cell's DNA}}.",
    "Ex: “<b>Chromosomes</b> are composed of two types of large organic molecules (macromolecules): nucleic acids and proteins.”<br><br>Distinguish: chromatin is the DNA–protein material in its loose working form; a chromosome is the organized, countable package.<br><br>Formal: “darkly staining nucleoprotein bodies observed in cells during division; each carries a linear array of genes.”",
    [0])

lex("nucleic acids", "nucl_acid", "glossary", 619,
    "A <b>nucleic acid</b> is {{c1::an information-carrying macromolecule built of nucleotide chains}}.",
    "Ex: “Chromosomes are composed of two types of large organic molecules: <b>nucleic acids</b> and proteins.”<br><br>Cue: the two kinds are DNA and RNA.<br><br>Formal: “a macromolecule composed of phosphoric acid, pentose sugar, and organic bases.”",
    [2])

lex("proteins", "protein", "glossary", 622,
    "A <b>protein</b> is {{c1::a macromolecule made of amino-acid (polypeptide) chains}}.",
    "Ex: “Chromosomes are composed of two types of large organic molecules: nucleic acids and <b>proteins</b>.”<br><br>Distinguish: in chromosomes, proteins do the packaging — the nucleic acids carry the genetic information.",
    [3])

lex("deoxyribonucleic acid (DNA)", "deoxyribonucl_acid_dna", "glossary", 611,
    "<b>DNA (deoxyribonucleic acid)</b> is {{c1::the double-stranded nucleic acid that stores genetic information}}.",
    "Ex: “There are two types of nucleic acids: <b>deoxyribonucleic acid (DNA)</b> and ribonucleic acid (RNA).”<br><br>Distinguish: RNA is usually single-stranded, uses the sugar ribose, and swaps thymine for uracil.",
    [4])

lex("ribonucleic acid (RNA)", "ribonucl_acid_rna", "glossary", 623,
    "<b>RNA (ribonucleic acid)</b> is {{c1::a usually single-stranded nucleic acid}} — and the genetic material of some viruses.",
    "Ex: “There are two types of nucleic acids: deoxyribonucleic acid (DNA) and <b>ribonucleic acid (RNA)</b>.”<br><br>Distinguish: DNA is double-stranded, uses deoxyribose, and keeps thymine where RNA uses uracil.",
    [5])

lex("Type IIIS", "type_iiis", "in_source", 212,
    "In the pneumococcus transformation experiments, <b>Type IIIS</b> is {{c1::the virulent, capsule-bearing strain}}.",
    "Ex: “heat-killed <b>Type IIIS</b> bacteria (virulent when alive)…”<br><br>Distinguish: Type IIR = no capsule, avirulent. The capsule is what makes IIIS deadly — and what shows up as smooth colonies.<br><br>Cue: S strains killed the mice; R strains alone did not.",
    [7])

lex("Type IIR", "type_iir", "in_source", 212,
    "In the pneumococcus transformation experiments, <b>Type IIR</b> is {{c1::the avirulent strain lacking a capsule}}.",
    "Ex: “…and living <b>Type IIR</b> bacteria (avirulent) into mice…”<br><br>Distinguish: Type IIIS = capsule, virulent. IIR is the safe strain that the transforming principle converts into a killer.",
    [8])

lex("in vitro", "in_vitr", "glossary", 616,
    "<b>In vitro</b> means {{c1::“within glass” — outside a living organism}}.",
    "Ex: “In 1931, Richard Sia and Martin Dawson analyzed this genetic transformation <b>in vitro</b>, and showed that the mice played no role.”<br><br>Parts: in (in) + vitro (glass) — done in labware.<br><br>Distinguish: in vivo = inside the living organism.",
    [11])

lex("deoxyribonuclease (DNase)", "deoxyribonucleas_dnas", "glossary", 611,
    "<b>Deoxyribonuclease (DNase)</b> is {{c1::an enzyme that cuts up DNA}}.",
    "Ex: “…treated with the enzymes (1) <b>deoxyribonuclease (DNase)</b>, which degrades DNA…”<br><br>Parts: deoxyribo- (DNA's sugar) + nucle- (nucleic acid) + -ase (enzyme).<br><br>Formal: “any enzyme that hydrolyzes DNA.”",
    [14])

lex("ribonuclease (RNase)", "ribonucleas_rnas", "glossary", 623,
    "<b>Ribonuclease (RNase)</b> is {{c1::an enzyme that cuts up RNA}}.",
    "Ex: “…(2) <b>ribonuclease (RNase)</b>, which degrades RNA…”<br><br>Parts: ribo- (RNA's sugar) + nucle- + -ase (enzyme).<br><br>Formal: “any enzyme that hydrolyzes RNA.”",
    [15])

lex("protease", "proteas", "glossary", 622,
    "A <b>protease</b> is {{c1::an enzyme that cuts up proteins}}.",
    "Ex: “…or (3) <b>protease</b>, which degrades proteins…”<br><br>Parts: prote- (protein) + -ase (enzyme) — the -ase family names the enzyme by its target.<br><br>Formal: “any enzyme that hydrolyzes proteins.”",
    [16])

lex("Bacteriophage T2", "bacteriophag_t2", "glossary", 607,
    "<b>Bacteriophage T2</b> is {{c1::a virus that infects E. coli bacteria}}.",
    "Ex: “<b>Bacteriophage T2</b> infects the common colon bacterium E. coli and is similar to bacteriophage T4.”<br><br>Parts: bacterio- (bacteria) + -phage (eater).<br><br>Cue: about 50% DNA and 50% protein — the two-part composition that made the Hershey–Chase labeling possible.",
    [19])

lex("tobacco mosaic virus (TMV)", "tobacc_mosa_viru_tmv", "in_source", 215,
    "<b>Tobacco mosaic virus (TMV)</b> is {{c1::a plant virus: RNA in a protein coat}}.",
    "Ex: “Their simple, but definitive, experiment was done with <b>tobacco mosaic virus (TMV)</b>, a small virus composed of a single molecule of RNA encapsulated in a protein coat.”<br><br>Cue: no DNA at all — which is why TMV could prove RNA can be genetic material.",
    [25])

lex("phenotypically", "phenotypicall", "glossary", 621,
    "<b>Phenotypically</b> means {{c1::in terms of observable traits}}.",
    "Ex: “…the progeny viruses were always <b>phenotypically</b> and genotypically identical to the parent strain from which the RNA had been obtained.”<br><br>Parts: pheno- (to show/appear) + -typically.<br><br>Distinguish: genotypically = in terms of genetic makeup — what the genes say, not what shows.",
    [26])

lex("genotypically", "genotypicall", "glossary", 614,
    "<b>Genotypically</b> means {{c1::in terms of genetic makeup}}.",
    "Ex: “…the progeny viruses were always phenotypically and <b>genotypically</b> identical to the parent strain from which the RNA had been obtained.”<br><br>Parts: geno- (gene) + -typically.<br><br>Distinguish: phenotypically = in terms of what is observable — the traits the genes produce.",
    [27])

lex("chromatin", "chromatin", "glossary", 609,
    "<b>Chromatin</b> is {{c1::the DNA–protein complex that chromosomes are made of}}.",
    "Ex: “…studies of isolated <b>chromatin</b> — the complex of DNA, proteins, and other material present in nuclei…”<br><br>Distinguish: a chromosome is the organized package; chromatin is the material it is packaged from. Heterochromatin = tightly packed, euchromatin = loose.<br><br>Formal: “the complex of DNA and proteins in eukaryotic chromosomes.”",
    [29])

with open(OUT, "w") as f:
    json.dump(cards, f, indent=1, ensure_ascii=False)
print(f"wrote {len(cards)} cards to {OUT}")
blocks = {}
for c in cards:
    blocks[c["block"]] = blocks.get(c["block"], 0) + 1
for b, n in blocks.items():
    print(f"  {b:24s} {n}")
