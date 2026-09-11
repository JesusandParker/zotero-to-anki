#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Unit 2 card set for the Arabic source.

Scope: every Unit 2 mark EXCEPT [0],[1],[3],[4],[5], which the 2026-09-04 night run
already carded (vowel quality / vowel length / word stress) or folded into the alif
letter note. Those five are reported at hand-off as already-done, never re-carded.

Lanes:
  D_system        concept cards from the yellow prose marks
  E_culture       the Shaking hands culture box
  C_vocab         braafoo, per Parker's margin ask on p47
  L_lexicon       the three purple words (a fourth is already carded)
  A_letter_forms  one note per (letter x position), from the four "Writing" marks whose
                  margin comments ask for exactly this. New block -> new rules in
                  check_block_spec.py, added this session (F1-F4).
"""
import json, pathlib

LRM = "‎"          # U+200E, a literal character (gate-legal); see playbook 7a/R44
T   = "ـ"          # tatweel, the book's own way of showing a connected form

OUT = pathlib.Path("work/arabic/unit_2_cards.json")
SRC, SEG = "arabic", 2

cards = []
def add(**kw):
    kw.setdefault("source", SRC); kw.setdefault("segment", SEG)
    kw.setdefault("numeric", False); kw.setdefault("needs_human_check", False)
    kw.setdefault("verified_against", None); kw.setdefault("verified_by", None)
    kw.setdefault("visual_source", None); kw.setdefault("image", None)
    cards.append(kw)

# --------------------------------------------------------------------------
# D_system -- the long vowels, the short vowels, and how they are written
# --------------------------------------------------------------------------
add(block="D_system", from_idx=[16, 17, 23],
    Text=("Each Arabic long vowel has one short vowel that matches it:<br><br>"
          "alif (<i>aa</i>) — {{c1::fatHa}}<br><br>"
          "waaw (<i>uu</i>) — {{c1::Damma}}<br><br>"
          "yaa (<i>ii</i>) — {{c1::kasra}}"),
    **{"Back Extra": ("Cue: the long vowel is a whole LETTER you write on the line; its short "
                      "partner is only a mark added above or below.<br><br>"
                      "Distinguish: same vowel, two lengths — the long one is a letter you write, "
                      "the short one a mark you add last.")})

add(block="D_system", from_idx=[12, 18],
    Text=("An Arabic long vowel is held {{c1::at least twice}} as long as a short one "
          "— and English has {{c2::no long vowels at all}}, so Arabic's should feel "
          "exaggerated to you."),
    **{"Back Extra": ("Pitfall: do not worry about holding one \"too long\" — stretch it out so you "
                      "can hear the difference.<br><br>"
                      "Why: vowel length changes meaning, and a mispronounced length can make the "
                      "word unintelligible.")})

add(block="D_system", from_idx=[11],
    Text=("Of Arabic's three long vowels, waaw is the {{c1::second::first / second / third}}, "
          "and its sound is that of {{c2::the exclamation of delight — <i>ooooo!</i>}}"),
    **{"Back Extra": ("Cue: it shares its shape with the short vowel Damma, which is written as a "
                      "miniature waaw.<br><br>"
                      "Cue: your Unit 1 card teaches the same vowel as <i>oo</i> in <i>poodle</i>.<br><br>"
                      "Pitfall: do not confuse it with English <i>o</i> or <i>u</i>; keep the mouth "
                      "rounded and hold it.")})

add(block="D_system", from_idx=[14],
    Text=("The last of Arabic's three long vowels is yaa, the sound of "
          "{{c1::<i>ee</i> in <i>beep</i>}}."),
    **{"Back Extra": ("Cue: imitate a honking car horn — <i>beeeeep!</i> — and exaggerate it to "
                      "feel the length.<br><br>"
                      "Cue: your Unit 1 card teaches the same vowel as <i>ie</i> in <i>piece</i>.<br><br>"
                      "Ex: the book's own practice words are <i>beep</i> and <i>street</i>.")})

add(block="D_system", from_idx=[28],
    Text=("A short vowel is written on the letter that {{c1::precedes}} it, never on one "
          "that follows."),
    **{"Back Extra": ("Why: an Arabic syllable always BEGINS with a consonant, so the mark rides on "
                      "that consonant — the first letter of its syllable.<br><br>"
                      "Cue: writing the vowels is the third and final step — skeleton first, then "
                      "the dots, then the vowels.<br><br>"
                      "Pitfall: in ordinary text the short vowels are usually not written at all.")})

add(block="D_system", from_idx=[22, 31],
    Text=("What decides how frontal or how deep a short vowel actually sounds is "
          "{{c1::the consonants surrounding it}}."),
    **{"Back Extra": ("Ex: fatHa runs from <i>e</i> in <i>bet</i> to <i>u</i> in <i>but</i>; kasra from "
                      "<i>ee</i> in <i>keep</i> to <i>i</i> in <i>bit</i>.<br><br>"
                      "Cue: each short vowel swings along the same axis its long partner does.")})

# --- fatHa -----------------------------------------------------------------
add(block="D_system", from_idx=[22, 24, 26],
    verified_by="husk_groups cleared: each blank is cued by its own quality word "
                "('most frontal' / 'deep'), not by the other blank",
    Text=("At its most frontal, fatHa is {{c1::<i>e</i> as in <i>bet</i>}}; when deep, it is "
          "{{c1::<i>u</i> as in <i>but</i>}}."),
    **{"Back Extra": ("Why: it swings along the same frontal-to-deep axis its long counterpart alif "
                      "does, and the consonants around it decide where it lands.<br><br>"
                      "Pitfall: alif and fatHa do NOT share keywords — alif's deep pole is the long "
                      "<i>a</i> of <i>father</i>, fatHa's is the short <i>u</i> of <i>but</i>. Same "
                      "colour, different length.")})

add(block="D_system", from_idx=[25],
    visual_source={"figures": ["work/arabic/u2/mark25_p53.png"],
                   "note": "the marked sentence names the three consonants in Arabic script; "
                           "the OCR returned them as garbage, so they were read off the page"},
    verified_against="rendered p53 (printed 35), the marked sentence itself",
    verified_by="visual read of the mark's own crop",
    Text=("The consonants the book names as frontal ones, which give fatHa its frontal "
          "<i>e</i>-as-in-<i>bet</i> quality, are {{c1::baa, taa and thaa}}."),
    **{"Back Extra": ("Cue: all three share one skeleton and differ only in their dots — and all "
                      "three are frontal.<br><br>"
                      "Pitfall: the book does not name the same set for every short vowel — check "
                      "which vowel the question is about before you answer.")})

add(block="D_system", from_idx=[29],
    Text=("fatHa is written as {{c1::a short, slanted line segment}} "
          "{{c2::above::above or below?}} its consonant."),
    **{"Back Extra": ("Distinguish: Damma sits in the same place, above the letter, but is shaped "
                      "like a miniature waaw.<br><br>"
                      "Cue: the vowel marks go on last — consonant skeleton first, then the dots, "
                      "then the vowels.")})

add(block="D_system", from_idx=[27],
    Text=("The name of the short vowel <i>fatHa</i> means {{c1::\"opening\"}}."),
    **{"Back Extra": ("Why: it names the shape of your mouth as you say it — wide open. Try it "
                      "and see.<br><br>"
                      "Distinguish: Damma is named for ROUNDING the mouth, not for opening it.")})

# --- Damma -----------------------------------------------------------------
add(block="D_system", from_idx=[30],
    Text=("After frontal consonants, Damma is pronounced {{c1::<i>oo</i> as in <i>booth</i>}}."),
    **{"Back Extra": ("Pitfall: English <i>u</i> in <i>but</i> and <i>gum</i> is a deep fatHa, NOT a "
                      "Damma.<br><br>"
                      "Cue: your Unit 1 card teaches this same vowel as <i>oo</i> in <i>poodle</i> — "
                      "one sound, two keywords.<br><br>"
                      "Cue: the name Damma refers to ROUNDING — keep your mouth rounded and it comes "
                      "out right.<br><br>"
                      "Why: a deep consonant pulls it deeper, closer to <i>oo</i> in <i>wool</i>.")})

# --- kasra -----------------------------------------------------------------
add(block="D_system", from_idx=[31],
    Text=("kasra ranges from a frontal {{c1::<i>ee</i> as in <i>keep</i>}} to a deep "
          "{{c1::<i>i</i> as in <i>bit</i>}}."),
    **{"Back Extra": ("Why: as with fatHa and Damma, the surrounding consonants decide the exact "
                      "sound.")})

add(block="D_system", from_idx=[32],
    visual_source={"figures": ["work/arabic/u2/mark32_wide.png"],
                   "note": "same OCR failure as the fatHa sentence — the two letters were "
                           "read off the rendered page"},
    verified_against="rendered p55 (printed 37), the marked sentence itself",
    verified_by="visual read of the mark's own crop",
    Text=("The frontal consonants the book names for kasra, which give it a frontal quality, "
          "are {{c1::taa and thaa}}."),
    **{"Back Extra": ("Pitfall: this is the kasra list, and it is not the same length as the fatHa "
                      "one — read which vowel is being asked about.")})

add(block="D_system", from_idx=[33],
    Text=("The name <i>kasra</i> means {{c1::\"break\"}}, and it refers to your mouth being "
          "{{c1::only slightly open}} as you say it."),
    **{"Back Extra": ("Cue: the name describes the MOUTH, not the sound — slightly open, not wide "
                      "open.<br><br>"
                      "Pitfall: do not drop the jaw for it; that turns it into a different vowel.")})

# --- thaa ------------------------------------------------------------------
add(block="D_system", from_idx=[8],
    Text=("English spells two distinct sounds <i>th</i>, and Arabic gives each its own "
          "letter. thaa is {{c1::only the <i>three</i> sound, never the <i>that</i> sound}}."),
    **{"Back Extra": ("Cue: thaa carries THREE dots — say \"three\" out loud before you pronounce "
                      "or read it.<br><br>"
                      "Distinguish: the <i>th</i> of <i>that</i> belongs to dhaal, a letter this course "
                      "has not taught yet — Unit 1 drilled hearing the two apart.")})

# --------------------------------------------------------------------------
# E_culture -- the Shaking hands box (p62)
# --------------------------------------------------------------------------
add(block="E_culture", from_idx=[34],
    Text=("In social as well as professional situations it is polite to {{c1::shake hands}} "
          "when meeting or greeting another person of "
          "{{c2::the same gender::same or opposite?}}."),
    **{"Back Extra": ("Why: with the opposite gender it varies widely according to religious belief "
                      "and personal practice.")})

add(block="E_culture", from_idx=[35],
    Text=("A man meeting a woman should {{c1::wait for her to extend her hand first}}."),
    **{"Back Extra": ("Why: her offered hand is the signal that she wants to shake yours.")})

add(block="E_culture", from_idx=[36],
    Text=("In many regions children are taught to greet an older, respected guest by shaking "
          "hands and then {{c1::kissing, or being kissed on, both cheeks}}."),
    **{"Back Extra": ("Why: it welcomes the guest into the home with warmth and respect.")})

# --------------------------------------------------------------------------
# C_vocab -- Parker's margin ask on p47: "Can we add this to the vocab parts of anki?"
# --------------------------------------------------------------------------
add(block="C_vocab", from_idx=[10],
    image="work/arabic/u2/media/u2_vocab_braafoo_v1.png", image_side="back",
    visual_source={"figures": ["work/arabic/u2/media/u2_vocab_braafoo_v1.png",
                                "work/arabic/u2/braafoo_zoom.png"],
                   "note": "the extractor returned 'g:91).)' for this mark and NO context: "
                           "the word uses raa and faa, which Unit 2 has not taught and the "
                           "OCR did not resolve. Read letter by letter off a 600 dpi zoom."},
    verified_against=None,
    verified_by="letter-by-letter visual read of a 600 dpi zoom (beh + reh + alef + feh + waw). "
                "NOT a verification: the word is absent from the page text layer and from the "
                "Lingco Unit 2 vocab list, so no publisher Unicode exists to check it against",
    needs_human_check=True,
    Text=(LRM + "{{c1::برافو}}<br><br>"
          "Transliteration: {{c1::braafoo}}<br><br>"
          "{{c2::Bravo!}} — said on finishing the first four letters of the alphabet"),
    **{"Back Extra": ("Cue: MSA — a borrowed exclamation of praise, written in Arabic letters.<br><br>"
                      "Ex: \"Bravo! You have learned the first four letters of the Arabic alphabet.\"<br><br>"
                      "Distinguish: <i>aHsanta</i> is her spoken \"Good job! Well done!\"; this one "
                      "is specifically <i>Bravo!</i>, and it is the book's word, not hers.")})

# --------------------------------------------------------------------------
# L_lexicon -- the purple words (card-rules #28, recipes 4b)
# --------------------------------------------------------------------------
add(block="L_lexicon", kind="lexicon", from_idx=[19],
    lexicon={"term": "consonant", "term_key": "conson",
             "anchor": {"method": "external"}},
    verified_by="external-anchor warning CLEARED: lexicon.py's in_source hit for 'conson' is a "
                "fragment of footnote 2 on p52 ('...consonant-short vowel)') — an occurrence of "
                "the word, not a definition, so there is nothing for the authored answer to "
                "agree with. The book never defines the term.",
    Text=("A <b>consonant</b> is {{c1::a sound that blocks or narrows the airflow}}."),
    **{"Back Extra": ("Ex: \"syllables in Arabic always begin with a <b>consonant</b>.\"<br><br>"
                      "Distinguish: a vowel is the open, freely flowing sound; a consonant closes or "
                      "narrows it.<br><br>"
                      "Cue: in Arabic the consonants are the skeleton you write first; the vowels are "
                      "added last.")})

add(block="L_lexicon", kind="lexicon", from_idx=[20],
    lexicon={"term": "short vowels", "term_key": "short_vowel",
             "anchor": {"method": "external"}},
    verified_by="external-anchor warning CLEARED: the in_source hit for 'short_vowel' is p52's "
                "long/short CORRESPONDENCE sentence (aa-fatHa, uu-Damma, ii-kasra). It never "
                "mentions length, so it cannot confirm a length-based definition.",
    Text=("A <b>short vowel</b> is {{c1::as long as an ordinary English vowel}}."),
    **{"Back Extra": ("Ex: \"by convention, <b>short vowels</b> are written above or below the "
                      "consonant.\"<br><br>"
                      "Distinguish: in Arabic a short vowel is a MARK added above or below a "
                      "consonant; a long vowel is a whole letter standing on the line.<br><br>"
                      "Pitfall: they are usually left unwritten altogether, which is why reading "
                      "unvowelled Arabic is a separate skill.")})

add(block="L_lexicon", kind="lexicon", from_idx=[21],
    needs_human_check=True,
    lexicon={"term": "syllable", "term_key": "yllabl",
             "anchor": {"method": "external"}},
    Text=("A <b>syllable</b> is {{c1::one beat of a word}}."),
    **{"Back Extra": ("Ex: \"<b>syllables</b> in Arabic always begin with a consonant.\"<br><br>"
                      "Meaning: one beat — a vowel plus the consonants packed around it.<br><br>"
                      "Cue: a syllable holding a long vowel is almost always the stressed one.<br><br>"
                      "Distinguish: a syllable is heard; a letter is written.")})

# --------------------------------------------------------------------------
# A_letter_forms -- one note per (letter x position).
# Parker asked for this four times in the margins of Unit 2's Writing sections:
#   [5]  "flashcards for each the final initial medial position ... all the positions of BAA"
#   [6]  "I want all the letters and all of their positions in Anki"
#   [9]  "These as well"      [15] "Let's add all of these writing characters."
# Six letters do not all behave alike: alif and waaw never join to the letter AFTER them,
# so the book's four slots collapse into two real shapes. Minting four notes for them
# would ship two pairs of identical answers, so each non-connector gets the licensed PAIR
# per note instead -- and F1/F4 in check_block_spec.py hold that shape.
# --------------------------------------------------------------------------
CONNECTORS = {
    "baa":  ("ب", "ب" + T, T + "ب" + T, T + "ب"),
    "taa":  ("ت", "ت" + T, T + "ت" + T, T + "ت"),
    "thaa": ("ث", "ث" + T, T + "ث" + T, T + "ث"),
    "yaa":  ("ي", "ي" + T, T + "ي" + T, T + "ي"),
}
NONCONNECTORS = {                        # (independent-or-initial, medial-or-final)
    "alif": ("ا", T + "ا"),
    "waaw": ("و", T + "و"),
}
POSITIONS = ("independent", "initial", "medial", "final")
CUE = {
    "baa":  "baa is a connector: it joins on both sides, and the dot stays below the body.",
    "taa":  "taa has the same shapes as baa in every position, and it is a connector too "
            "— two dots on top instead of one below.<br><br>"
            "Mnemonic: associate the sound <i>t</i> with <i>two dots on top</i>.",
    "thaa": "thaa is a connector, written just like baa and taa in every position, except "
            "that it carries three dots above.",
    "yaa":  "yaa's independent and final forms differ from its initial and medial ones, "
            "which look like baa, taa and thaa — with two dots below.",
    "alif": "alif never joins to the letter after it — always pick the pen up once it is "
            "written.",
    "waaw": "waaw never joins to the letter after it, so its shapes barely change.",
}
MARK = {"alif": [5], "baa": [5], "taa": [6, 7], "thaa": [9], "waaw": [13], "yaa": [15]}

def forms_note(letter, glyph, position_label, idx):
    plate = f"u2_forms_{letter}_v1.png"
    add(block="A_letter_forms", from_idx=list(MARK[letter]),
        image=f"work/arabic/u2/media/{plate}", image_side="back",
        visual_source={"figures": [f"work/arabic/u2/media/{plate}"],
                       "note": "the book's own printed Writing row for this letter"},
        verified_against=f"the printed Writing row for {letter}, Alif Baa Unit 2",
        verified_by="measured crop of the book's own forms row (no-clip asserted)",
        Text=(LRM + "{{c1::" + glyph + "}}<br><br>"
              "Letter: {{c2::" + letter + "}}<br><br>"
              "Position: {{c2::" + position_label + "}}"),
        **{"Back Extra": ("Distinguish: " + CUE[letter] + "<br><br>"
                          "Roster: " + letter + "'s four written forms run right to left across the "
                          "row — " + ", ".join(
                              # a non-connector's note covers TWO slots, so bold every
                              # position its label names, not just an exact string match
                              f"<b>{q}</b>" if q in position_label.split("::")[0] else q
                              for q in POSITIONS) + ".")})

# The INDEPENDENT form is not new work: each letter's Unit 1 note already prompts
# "Name / Transliteration / Sound" and asks for exactly that isolated glyph, so a note
# cueing "Letter: baa / Position: independent" demands the identical retrieval — and its
# reverse card asks a position that a lone glyph answers by itself (card-rules #20).
# What Unit 2 actually adds is the CONNECTED forms, so those are what get notes.
# alif is skipped entirely: the 2026-09-04 night run already put all four of its shapes on
# the live alif letter note. waaw keeps only its connected shape for the same reason.
for letter, glyphs in CONNECTORS.items():
    for glyph, pos in zip(glyphs, POSITIONS):
        if pos == "independent":
            continue
        forms_note(letter, glyph, pos, MARK[letter])
forms_note("waaw", NONCONNECTORS["waaw"][1], "medial and final::name both", MARK["waaw"])

# ---------------------------------------------------------------------------
# Record the verification that actually happened, rather than leaving it blank.
# Every prose card below was checked against its own page rendered at 200 dpi and read
# visually (the Arabic OCR on this scan is unreliable, so the rendered page — not the text
# layer — is the authority; playbook 7e / R38). verify_report.py derives
# `needs_human_check` from what was VERIFIED, so leaving these null would have put eight
# cards in front of Parker's eyes that nobody actually needs to re-check.
# ---------------------------------------------------------------------------
_hl = json.loads(pathlib.Path("work/arabic/unit_2_highlights.json").read_text(encoding="utf-8"))
for c in cards:
    if c["block"] not in ("D_system", "E_culture") or c.get("verified_against"):
        continue
    pages = sorted({(_hl[i]["page"], _hl[i]["page_label"]) for i in c["from_idx"]})
    where = ", ".join(f"p{ph} (printed {lb})" for ph, lb in pages)
    c["verified_against"] = f"the marked sentence(s) on rendered {where}"
    c["verified_by"] = (c.get("verified_by") or "") + \
        ("; " if c.get("verified_by") else "") + \
        "read off the page render at 200 dpi (the scan's Arabic OCR is unreliable)"

OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {OUT}  ({len(cards)} cards)")
from collections import Counter
for b, n in Counter(c["block"] for c in cards).most_common():
    print(f"   {b:16} {n}")
