#!/usr/bin/env python3
"""One-off for the chapter 9 'do it for me' run (2026-08-08).

Parker asked for chapter 9 cards but had only marked pp.212-215 + one purple on
p225. He explicitly delegated selection for the rest of the chapter, so this
script appends CLAUDE-SELECTED coverage marks to chapter_9_highlights.json —
each one labeled `"selected_by": "claude"` so no future session can mistake
them for Parker's own marks. Contexts are extracted with the extractor's own
page_text()/locate_context() so the R13 grounding gate verifies them exactly
like real marks. Idempotent: it rebuilds the file's coverage tail each run.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import sources as S
from extract_highlights import page_text, locate_context, norm

SRC = S.get_source("genetics")
_item, PDF = S.resolve_attachment(SRC)
HL = os.path.join(HERE, "chapter_9_highlights.json")

# (page, the sentence being selected) — quotes must exist verbatim on the page.
SELECTIONS = [
    # p211 — chapter opener history
    (211, "In 1868, Johann Friedrich Miescher, a young Swiss medical student, became fascinated with an acidic substance that he isolated from pus cells"),
    (211, "The role of nucleic acids in storing and transmitting genetic information was not established until 1944, and the double-helix structure of DNA was not discovered until 1953."),
    # p216 — nucleotides
    (216, "Nucleic acids, the major constituents of Miescher's nuclein, are macromolecules composed of repeating subunits called nucleotides."),
    (216, "Each nucleotide is composed of (1) a phosphate group, (2) a five-carbon sugar, or pentose, and (3) a cyclic nitrogen-containing compound called a base"),
    # p217 — sugars, bases, purine/pyrimidine, single vs double strand
    (217, "in RNA, the sugar is ribose (thus ribonucleic acid). Four different bases commonly are found in DNA: adenine (A), guanine (G), thymine (T), and cytosine (C)."),
    (217, "RNA also usually contains adenine, guanine, and cytosine but has a different base, uracil (U), in place of thymine."),
    (217, "Adenine and guanine are double-ring bases called purines; cytosine, thymine, and uracil are single-ring bases called pyrimidines."),
    (217, "RNA usually exists as a single-stranded polymer that is composed of a long sequence of nucleotides."),
    (217, "1953 when James Watson and Francis Crick"),
    (217, "the concentration of thymine was always equal to the concentration of adenine and the concentration of cytosine was always equal to the concentration of guanine"),
    (217, "the total concentration of pyrimidines (thymine plus cytosine) was always equal to the total concentration of purines"),
    # p219 — X-ray, Nobel, phosphodiester + hydrogen bonds
    (219, "These data indicated that DNA was a highly ordered, two-stranded structure with repeating substructures spaced every 0.34 nanometer"),
    (219, "Watson and Crick proposed that DNA exists as a right-handed double helix in which the two polynucleotide chains are coiled about one another in a spiral"),
    (219, "Watson, Crick, and Wilkins shared the 1962 Nobel Prize in Physiology or Medicine for their work on the double-helix model."),
    (219, "nucleotides linked together by covalent phosphodiester bonds"),
    (219, "The two polynucleotide strands are held together in their helical configuration by hydrogen bonding"),
    # p220 — base pairing, complementarity, antiparallel, stacking, grooves
    (220, "Adenine is always paired with thymine, and guanine is always paired with cytosine. Thus, all base pairs consist of one purine and one pyrimidine."),
    (220, "adenine and thymine form two hydrogen bonds, and guanine and cytosine form three hydrogen bonds"),
    (220, "The two strands of a DNA double helix are thus said to be complementary."),
    (220, "The base pairs in DNA are stacked about 0.34 nm apart, with 10 base pairs per turn"),
    (220, "The sugar-phosphate backbones of the two complementary strands are antiparallel"),
    (220, "in part from the hydrophobic bonding (or stacking forces) between adjacent base pairs"),
    (220, "one, the major groove, is much wider than the other, the minor groove"),
    # p221 — B-DNA, A-DNA + worked Chargaff problem
    (221, "B-DNA is the conformation that DNA takes under physiological conditions"),
    (221, "intracellular B-DNA appears to have an average of 10.4 nucleotide pairs per turn"),
    (221, "DNA exists as A-DNA, which is a right-handed helix like B-DNA, but with 11 nucleotide pairs per turn"),
    (221, "if 33 percent of the bases are guanines, 33 percent of the bases are cytosines. That means that 66 percent of the bases are G's and C's and 34 percent"),
    (221, "In the single-stranded DNA of bacteriophage ΦX174, there is no strict base pairing"),
    # p222 — A-DNA heteroduplex, Z-DNA, supercoiling
    (222, "the A-DNA conformation is important because DNA-RNA heteroduplexes (double helices containing a DNA strand base-paired with a complementary RNA strand) or RNA-RNA duplexes exist in a very similar structure in vivo"),
    (222, "left-handed, doublehelical form called Z-DNA (Z for the zigzagged path of the sugar-phosphate backbones of the structure)"),
    (222, "Z-DNA occurs in double helices that are G:C-rich and that contain alternating purine and pyrimidine residues"),
    (222, "they are supercoiled. Supercoils are introduced into a DNA molecule when one or both strands are cleaved and when the complementary strands at one end are rotated or twisted around each other with the other end held fixed"),
    (222, "Supercoiling occurs only in DNA molecules with fixed ends, ends that are not free to rotate."),
    (222, "If we rotate the free end in the same direction as the DNA double helix is wound (righthanded), a positive supercoil (overwound DNA) will be produced. If we rotate the free end in the opposite direction (left-handed), a negative supercoil (underwound DNA) will result."),
    (222, "The DNA molecules of almost all organisms, from the smallest viruses to the largest eukaryotes, exhibit negative supercoiling in vivo"),
    # p223-224 — viruses and prokaryotes
    (223, "In most viruses and prokaryotes, the genes reside in a single chromosome that consists of a single molecule of nucleic acid, either RNA or DNA."),
    (223, "the genome of bacteriophage X174 is a single DNA molecule 5386 nucleotides long and contains 11 genes"),
    (223, "E. coli K12, a strain used for genetic analysis in many laboratories, has 4.6 million base pairs in its genome"),
    (224, "The contour length of the circular DNA molecule present in the chromosome of the bacterium Escherichia coli is about 1500 μm."),
    (224, "This structure, called the folded genome, is the functional state of a bacterial chromosome."),
    (224, "the large DNA molecule in an E. coli chromosome is organized into 50 to 100 domains or loops, each of which is independently negatively supercoiled"),
    # p225 — relaxing the folded genome; chromatin & histones
    (225, "the introduction of single-strand “nicks” in DNA by treatment of the chromosomes with a DNase that cleaves DNA at internal sites will relax the DNA only in the nicked domains, and all unnicked loops will remain supercoiled"),
    (225, "Treatment with RNase will unfold the folded genome partially by eliminating the RNA molecules that anchor each of its loops."),
    (225, "This change in appearance results from the compaction of all the material in each chromosome into a smaller volume, a process called condensation."),
    (225, "Chemical analysis of isolated chromatin shows that it consists primarily of DNA and proteins with lesser amounts of RNA"),
    (225, "(1) basic (positively charged at neutral pH) proteins called histones and (2) a heterogeneous, largely acidic (negatively charged at neutral pH) group of proteins collectively referred to as nonhistone chromosomal proteins"),
    (225, "All plants and animals have five different types of histones, denoted as H1, H2a, H2b, H3, and H4."),
    (225, "most notably some sperm, where the histones are replaced by another class of small basic proteins called protamines"),
    (225, "The five histone types are present in molar ratios of approximately 1 H1:2 H2a:2 H2b:2 H3:2 H4."),
    (226, "histones to act as polycations. These side groups are important in the interactions between histones and DNA, which is polyanionic because of its negatively charged phosphate groups."),
    (225, "However, a few are basic and a few are acidic. The histones are basic because they contain 20 to 30 percent arginine and lysine"),
    # p226 — histone conservation vs nonhistone variability; one DNA per chromosome
    (226, "The remarkable constancy of histones H2a, H2b, H3, and H4 in all cell types of an organism and even among widely divergent species is consistent with the idea that these proteins are important in chromatin structure"),
    (226, "the nonhistone chromosomal proteins are likely candidates for regulating the expression of specific genes"),
    # p227 — Kavenoff & Zimm; one giant molecule
    (227, "we do, however, have high confidence that each eukaryotic chromosome consists of a single giant DNA molecule"),
    (227, "Kavenoff and Zimm repeated the experiment with a DNA solution that had been treated with pronase, an enzyme that degrades protein. The size of the largest DNA molecule was unchanged."),
    # p227-228 — nucleosomes
    (227, "it is found to consist of a series of ellipsoidal beads (about 11 nm in diameter and 6.5 nm high) joined by thin threads"),
    (228, "Partial digestion of chromatin with these nucleases yields fragments of DNA in a set of discrete sizes that are integral multiples of the smallest size fragment."),
    (228, "chromatin subunit is called the nucleosome. According to the present concept of chromatin structure, the threads that connect adjacent nucleosomes are DNA linkers"),
    (228, "a segment of DNA 146 nucleotide pairs long is protected from degradation because it is tightly associated with the histones in a structure called the nucleosome core"),
    (228, "the segment of DNA is associated with two molecules each of histones H2a, H2b, H3, and H4. This octamer of histones protects the DNA from degradation"),
    (228, "the DNA forms a superhelix that winds 1.65 times around the outside of the histone octamer"),
    (228, "all stabilized by the binding of one molecule of histone H1 to the outside of the structure"),
    (228, "the complete nucleosome (as opposed to the nucleosome core) contains two full turns of DNA superhelix (a 166-nucleotide-pair length of DNA)"),
    (228, "The size of the linker DNA varies from species to species and from one cell type to another. Linkers as short as eight nucleotide pairs and as long as 114 nucleotide pairs have been reported."),
    # p229 — 30-nm fiber, solenoid/zigzag, scaffold, three levels
    (229, "These chromatin fibers have an average diameter of 30 nm."),
    (229, "The two most popular models of the substructure of these chromatin fibers are the solenoid model (◾ Figure 9.21c) and the zigzag model"),
    (229, "The tight packaging of these chromosomes facilitates their segregation into daughter nuclei during the ensuing anaphase, and it helps to prevent different chromosomes from becoming entangled"),
    (229, "This core, called a scaffold, can be seen in electron micrographs of isolated metaphase chromosomes from which the histones have been removed"),
    (229, "The first level of condensation involves packaging DNA as a negative supercoil into nucleosomes, to produce the 11-nmdiameter interphase chromatin fiber."),
    (229, "The second level of condensation involves an additional folding or supercoiling of the 11-nm nucleosome fiber, to produce the 30-nm chromatin fiber. Histone H1 is involved in this supercoiling."),
    (229, "nonhistone chromosomal proteins form a scaffold that is involved in condensing the 30-nm chromatin fiber into the tightly packed metaphase chromosomes"),
    # p231 — repetitive DNA
    (231, "the human genome has 700 times more DNA than the E. coli genome, but only 4.5 times more genes"),
    (232, "The main fraction consists of typical DNA sequences and the other fractions consist of DNA sequences that are either G:C- or A:T-rich. These other fractions are called satellite DNAs"),
    (232, "G:C-rich DNA—will be found at a lower position than typical DNA sequences because the tighter hydrogen bonding of G:C base pairs makes this DNA more dense"),
    (232, "When DNA molecules in aqueous solution are heated to near 100°C, these bonds are broken and the complementary strands of DNA separate. This process is called denaturation."),
    (232, "If the complementary single strands of DNA are cooled slowly, they find each other and re-form base-paired double helices. This process is called renaturation."),
    (232, "the repetitive sequences re-form duplex molecules at a faster rate than the unique DNA sequences"),
    (232, "The degree of repetition is called the copy number."),
    (232, "with a copy number from 103 to 106"),
    (232, "the technique is called in situ hybridization"),
    (232, "Highly repetitive DNA sequences are located primarily in the regions around the centromeres of eukaryotic chromosomes"),
    # p233 — transposons, centromeres/kinetochores
    (233, "In humans, the value is 44 percent"),
    (233, "This movement depends on the attachment of spindle microtubules to the kinetochores, which are complex protein structures associated with the centromeres of each of the sister chromatids"),
    (233, "A chromosome or chromosome fragment that lacks a centromere will usually be lost during cell division."),
    (233, "The centromeres of the yeast Saccharomyces cerevisiae consist of a DNA segment 125 base pairs long."),
    (233, "Human centromeres are 500,000 to 1.5 million base pairs long and contain 5000 to 15,000 copies of a 171 base-pair-long sequence called the alpha satellite sequence"),
    (233, "the heterochromatin, which comprises the parts of chromosomes that stain deeply with certain dyes. The heterochromatin is packaged more tightly than the euchromatin"),
    (233, "A protein variant of histone H3 called CENP-A binds to the centromeres of eukaryotes"),
    # p233-234 — telomeres
    (233, "The ends of chromosomes are called telomeres, from the Greek words telos (“end”) and meros (“part”). The word was coined in 1938 by Hermann J. Muller"),
    (233, "They prevent dioxyribonucleases from degrading the ends of linear DNA molecules, they prevent fusion of the ends with other DNA molecules, and they facilitate the replication of these ends without the loss of material."),
    (234, "the repeat sequence in humans and other vertebrates is TTAGGG"),
    (234, "In normal (noncancerous) human somatic cells, telomeres usually contain 500 to 3000 TTAGGG repeats and gradually shorten with age. In contrast, the telomeres of germ-line cells and cancer cells do not shorten with age"),
    (234, "Most telomeres terminate with a G-rich single-stranded region in the DNA strand with the 3′ end (a so-called 3′ overhang)."),
    (234, "called t-loops, in which the single strand at the 3′ terminus invades an upstream telomeric repeat (TTAGGG in mammals) and pairs with the complementary strand"),
    (235, "and/or modification by DNA repair processes by a telomere-specific protein complex called shelterin. Shelterin is composed of six different proteins, three of which bind specifically to telomere repeat sequences."),
    (235, "TRF1 and TRF2 (Telomere Repeat Factors) bind to double-stranded repeat sequences, and POT1 (Protection Of Telomeres 1) binds to single-stranded repeat sequences."),
    (215, "There was one problem with Hershey and Chase's proof that the genetic material of phage T2 is DNA. Their results showed that a significant amount of 35S (and thus protein) was injected into the host cells with the DNA."),
    (235, "the top strand of the double helix should be written 5′-ATCG-3′ and the complementary strand, 5′-CGAT-3′."),
    (232, "the genes for these RNAs are highly redundant; hundreds or even thousands of copies may be present in a eukaryotic genome"),
]

items = json.load(open(HL))
items = [it for it in items if it.get("selected_by") != "claude"]  # rebuild tail
base = len(items)

page_cache = {}
bad = []
for n, (page, quote) in enumerate(SELECTIONS):
    if page not in page_cache:
        page_cache[page] = page_text(PDF, page)
    status, ctx = locate_context(quote, page_cache[page])
    if status == "NOT_FOUND" or not ctx:
        bad.append((page, quote[:60], status))
        continue
    items.append({
        "source": "genetics", "kind": "text",
        "segment": 9, "segment_name": "DNA and the Molecular Structure of Chromosomes",
        "page": page, "page_label": str(page - 22), "color": None,
        "selected_by": "claude",
        "highlight": norm(quote), "context": ctx,
        "grounding": status, "content": "FULL",
        "page_text_chars": len(page_cache[page]),
        "next_page_text_chars": None, "list_lead_in": False,
        "user_comment": None, "sort": f"coverage|{page:05d}|{n:03d}",
        "page_sparse": False, "needs_visual": False,
    })

with open(HL, "w") as f:
    json.dump(items, f, indent=1, ensure_ascii=False)

print(f"kept {base} extractor marks, appended {len(items) - base} claude-coverage marks "
      f"(indices {base}..{len(items) - 1})")
grounded = sum(1 for it in items[base:] if it["grounding"] == "EXACT")
print(f"coverage grounding: {grounded}/{len(items) - base} EXACT")
for b in bad:
    print("  NOT FOUND:", b)
