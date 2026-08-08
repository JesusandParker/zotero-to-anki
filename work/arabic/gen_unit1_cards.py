#!/usr/bin/env python3
"""Unit 1 card generator — Alif Baa (source: arabic).

Overseer run 2026-08-08. Every fact below was transcribed from a RENDERED page of
Parker's scan (the text layer contains zero Arabic) or from the Lingco lesson JSON
(class.lingco.io /api/content/lessons/8174 — the publisher's own Unicode + audio).
RTL rule: a line is either PURE Arabic or pure Latin, never mixed (bidi scrambles
mixed lines; verified in-browser 2026-08-08). Gate-legal HTML only: b/i/br/img.
"""
import json, os

W = os.path.dirname(os.path.abspath(__file__))
AR = lambda s: s  # marker for pure-Arabic lines (readability of the data below)

# ---------------------------------------------------------------- letters -----
# glyph, book name, book sound gloss (pp.11-12 charts, rendered p25/p26),
# video file, family key
LETTERS = [
 ("ا","alif","long vowel <i>aa</i> — ranges from <i>e</i> in <i>bet</i> to <i>a</i> in <i>father</i>","arabic_pron_01_alif.mp4","solo"),
 ("ب","baa","<i>b</i> as in <i>bet</i>","arabic_pron_02_baa.mp4","btt"),
 ("ت","taa","<i>t</i> as in <i>tip</i>","arabic_pron_03_taa.mp4","btt"),
 ("ث","thaa","<i>th</i> as in <i>three</i>","arabic_pron_04_thaa.mp4","btt"),
 ("ج","jiim","<i>j</i> or <i>g</i>, varies according to region","arabic_pron_05_jiim.mp4","jhk"),
 ("ح","Haa","a raspy, breathy <i>h</i>","arabic_pron_06_Haa.mp4","jhk"),
 ("خ","khaa","like a German or Hebrew <i>ch</i>","arabic_pron_07_khaa.mp4","jhk"),
 ("د","daal","<i>d</i> as in <i>dip</i>","arabic_pron_08_daal.mp4","dd"),
 ("ذ","dhaal","<i>th</i> in <i>the</i> and <i>other</i>","arabic_pron_09_dhaal.mp4","dd"),
 ("ر","raa","like Spanish or Italian <i>r</i>","arabic_pron_10_raa.mp4","rz"),
 ("ز","zaay","<i>z</i> as in <i>zip</i>","arabic_pron_11_zaay.mp4","rz"),
 ("س","siin","<i>s</i> as in <i>sip</i>","arabic_pron_12_seen.mp4","ss"),
 ("ش","shiin","<i>sh</i> as in <i>she</i>","arabic_pron_13_sheen.mp4","ss"),
 ("ص","Saad","emphatic S — similar to <i>s</i> in <i>subtle</i>","arabic_pron_14_Saad.mp4","sd"),
 ("ض","Daad","emphatic D — close to the <i>d</i> in <i>duh!</i>","arabic_pron_15_Daad.mp4","sd"),
 ("ط","Taa","emphatic T — similar to <i>t</i> in <i>bottle</i>","arabic_pron_16_Taaa.mp4","tdh"),
 ("ظ","DHaa","emphatic DH — close to <i>th</i> in <i>thy</i>","arabic_pron_17_Dhaa.mp4","tdh"),
 ("ع","cayn","a sound produced deep in the throat","arabic_pron_18_ayn.mp4","ag"),
 ("غ","ghayn","like French or Hebrew <i>r</i>","arabic_pron_19_ghayn.mp4","ag"),
 ("ف","faa","<i>f</i> as in <i>fun</i>","arabic_pron_20_faa.mp4","fq"),
 ("ق","qaaf","like <i>k</i> but deeper in the throat","arabic_pron_21_qaaf.mp4","fq"),
 ("ك","kaaf","<i>k</i> as in <i>keep</i>","arabic_pron_22_kaaf.mp4","solo"),
 ("ل","laam","like Spanish or Italian <i>l</i>","arabic_pron_23_laam.mp4","solo"),
 ("م","miim","<i>m</i> as in <i>mat</i>","arabic_pron_24_miim.mp4","solo"),
 ("ن","nuun","<i>n</i> as in <i>neat</i>","arabic_pron_25_nuun.mp4","solo"),
 ("ه","haa","<i>h</i> as in <i>aha!</i>","arabic_pron_26_ha.mp4","solo"),
 ("و","waaw","<i>w</i> as in <i>wow!</i> — also long vowel <i>uu</i> (<i>oo</i> in <i>poodle</i>)","arabic_pron_27_waaw.mp4","solo"),
 ("ي","yaa","<i>y</i> as in <i>yes</i> — also long vowel <i>ii</i> (<i>ie</i> in <i>piece</i>)","arabic_pron_28_yaa.mp4","solo"),
]
FAMILIES = {
 "btt": ("ب ت ث", "one skeleton, dots decide — baa 1 below, taa 2 above, thaa 3 above"),
 "jhk": ("ج ح خ", "one skeleton — jiim dot below, Haa no dot, khaa dot above"),
 "dd":  ("د ذ",   "same shape — daal plain, dhaal dot above"),
 "rz":  ("ر ز",   "same shape — raa plain, zaay dot above"),
 "ss":  ("س ش",  "same shape — siin plain, shiin 3 dots above"),
 "sd":  ("ص ض", "same shape — Saad plain, Daad dot above"),
 "tdh": ("ط ظ",  "same shape — Taa plain, DHaa dot above"),
 "ag":  ("ع غ",  "same shape — cayn plain, ghayn dot above"),
 "fq":  ("ف ق", "one dot above vs two dots above (qaaf also sits deeper in the throat)"),
}

# ---------------------------------------------------------------- symbols -----
# display line (pure Arabic, carrier baa for combining marks), name, extra sound
SYMBOLS = [
 ("بَ","fatHa","short <i>a</i> (vowel chart: <i>e</i> in <i>bet</i> to <i>a</i> in <i>father</i>)"),
 ("بُ","Damma","short <i>u</i> (<i>oo</i> in <i>poodle</i>, short)"),
 ("بِ","kasra","short <i>i</i> (<i>i</i> as in <i>bit</i>)"),
 ("بً","tanwiin al-fatH",None),
 ("بٌ","tanwiin aD-Damm",None),
 ("بٍ","tanwiin al-kasr",None),
 ("بْ","sukuun",None),
 ("بّ","shadda",None),
 ("ٱ","waSla",None),
 ("هٰ","dagger alif",None),
 ("آ","alif madda",None),
 ("ى","alif maqSuura",None),
 ("ء","hamza","the sound you hear between vowels in <i>uh-oh!</i> (glottal stop)"),
 ("ة","taa marbuuTa",None),
]

# ---------------------------------------------------------------- vocab -------
# arabic (Lingco verbatim), meaning line (disambiguated), formal translit,
# audio formal / masri / shaami, distinguish/extra
VOCAB = [
 ("السَّلامُ عَلَيكُم",("Greetings!","the Islamic greeting"),"assalaamu <sup>c</sup>alaykum".replace("<sup>c</sup>","c"),
  "arabic_vocab_u1_01_salaam_alaykum_formal.mp3","arabic_vocab_u1_01_salaam_alaykum_masri.mp3","arabic_vocab_u1_01_salaam_alaykum_shaami.mp3",
  "Egyptian <i>issalaamu calaykum</i> (initial i-)."),
 ("أَهلاً",("Hello! or Hi!","used more in Egypt than in the Levant"),"ahlan",
  "arabic_vocab_u1_02_ahlan_formal.mp3","arabic_vocab_u1_02_ahlan_masri.mp3","arabic_vocab_u1_02_ahlan_shaami.mp3",
  "Levantine drops the final -n: <i>ahla</i>."),
 ("أَهلاً وسَهلاً",("Hello!","the fuller two-word greeting"),"ahlan wa sahlan",
  "arabic_vocab_u1_03_ahlan_wa_sahlan_formal.mp3","arabic_vocab_u1_03_ahlan_wa_sahlan_masri.mp3","arabic_vocab_u1_03_ahlan_wa_sahlan_shaami.mp3",
  "Levantine: <i>ahla w sahla</i>."),
 ("مَرحَباً",("Hello!","used in the Levant"),"marHaban",
  "arabic_vocab_u1_04_marhaba_formal.mp3",None,"arabic_vocab_u1_04_marhaba_shaami.mp3",
  "Levantine says <i>marHaba</i>; no Egyptian column in the book for this one."),
 ("أَنا",("I",None),"ana",
  "arabic_vocab_u1_05_ana_formal.mp3","arabic_vocab_u1_05_ana_masri.mp3","arabic_vocab_u1_05_ana_shaami.mp3",None),
 ("اسمي",("my name",None),"ismii",
  "arabic_vocab_u1_06_ismi_formal.mp3","arabic_vocab_u1_06_ismi_masri.mp3","arabic_vocab_u1_06_ismi_shaami.mp3",
  "Egyptian and Levantine both say <i>ismi</i> (short final i)."),
 ("مِن",("from",None),"min",
  "arabic_vocab_u1_07_min_formal.mp3","arabic_vocab_u1_07_min_masri.mp3","arabic_vocab_u1_07_min_shaami.mp3",None),
 ("مدينة",("the city of …",None),"madiinat",
  "arabic_vocab_u1_08_madiinat_formal.mp3","arabic_vocab_u1_08_madiinat_masri.mp3","arabic_vocab_u1_08_madiinat_shaami.mp3",
  "Egyptian <i>midiinit</i> · Levantine <i>madiinit</i>."),
 ("في",("in",None),"fii",
  "arabic_vocab_u1_09_fii_formal.mp3","arabic_vocab_u1_09_fii_masri.mp3","arabic_vocab_u1_09_fii_shaami.mp3",
  "Levantine often uses <i>bi-</i> instead."),
]

# ---------------------------------------------------------------- countries ---
COUNTRIES = [  # map legend, p27 render (physical), numbered 1-20
 ("Morocco","Rabat"),("Mauritania","Nouakchott"),("Algeria","Algiers"),("Tunisia","Tunis"),
 ("Libya","Tripoli"),("Egypt","Cairo"),("Sudan","Khartoum"),("Somalia","Mogadishu"),
 ("Jordan","Amman"),("Israel/Palestine","Jerusalem"),("Lebanon","Beirut"),("Syria","Damascus"),
 ("Iraq","Baghdad"),("Kuwait","Kuwait"),("Saudi Arabia","Riyadh"),("Qatar","Doha"),
 ("Bahrain","Manama"),("United Arab Emirates","Abu Dhabi"),("Oman","Muscat"),("Yemen","Sanaa"),
]

IMG = lambda name: os.path.join(W, name)
cards = []
def add(text, back, block, from_idx, image=None, image_side=None, numeric=False,
        verified_against=None, verified_by=None, visual_source=None):
    c = {"Text": text, "Back Extra": back, "source": "arabic", "segment": 1,
         "from_idx": from_idx, "block": block, "numeric": numeric,
         "verified_against": verified_against, "verified_by": verified_by,
         "needs_human_check": False, "visual_source": visual_source}
    if image: c["image"] = IMG(image); c["image_side"] = image_side or "back"
    cards.append(c)

# --- A. letters (28 notes, 2 cards each: c1 = write the glyph, c2 = name+sound)
for glyph, name, sound, video, fam in LETTERS:
    text = (f"{{{{c1::{glyph}}}}}<br>"
            f"Name: {{{{c2::{name}}}}}<br>"
            f"Sound: {{{{c2::{sound}}}}}")
    lines = [f"Cue: hear it and watch the mouth — [sound:{video}]"]
    if fam != "solo":
        f_glyphs, f_note = FAMILIES[fam]
        lines.append(f"Distinguish: {f_glyphs}<br>{f_note}.")
    back = "<br><br>".join(lines)
    add(text, back, "A_letters", [1,12,15] + ([13] if glyph in "اوي" else []),
        image="src_alphabet_chart.png",
        verified_against="p16 chart + p25/p26 sound charts (rendered) + AB3e official video "+video,
        verified_by="glyph/name/sound transcribed from page renders 2026-08-08; name cross-checked against publisher video filename",
        visual_source="work/arabic/page_16.png; work/arabic/page_25.png; work/arabic/page_26.png")

# --- B. symbols (14 notes)
for shown, name, sound in SYMBOLS:
    if sound:
        text = (f"{{{{c1::{shown}}}}}<br>"
                f"Name: {{{{c2::{name}}}}}<br>"
                f"Sound: {{{{c2::{sound}}}}}")
    else:
        text = (f"{{{{c1::{shown}}}}}<br>"
                f"Name: {{{{c2::{name}}}}}")
    back = ("Cue: one of the 14 extra-alphabetical symbols — short vowels, pronunciation "
            "symbols, grammatical endings, spelling variants (each is taught fully in Units 2-10).")
    if shown.startswith("ب"):
        back += "<br><br>Cue: shown here on a carrier <i>baa</i> — the mark itself is the symbol."
    add(text, back, "B_symbols", [2] + ([13,15] if name in ("fatHa","Damma","kasra") else []),
        image="src_symbols_chart.png",
        verified_against="p17 symbols chart (rendered)" + ("; p26 vowel chart" if name in ("fatHa","Damma","kasra") else "") + ("; p26 consonant chart (glottal stop)" if name=="hamza" else ""),
        verified_by="symbol/name transcribed from page render 2026-08-08",
        visual_source="work/arabic/page_17.png")

# --- hamza gotcha
add("One consonant is, for historical reasons, NOT in the 28-letter alphabet chart: "
    "{{c1::hamza}} — it appears in the extra-symbols chart instead.",
    "Pitfall: easy exam trap — the chart has 28 letters, but Arabic has this 29th consonant "
    "living among the symbols.<br><br>Cue: its sound is the glottal stop in <i>uh-oh!</i>",
    "B_symbols", [2], image="src_symbols_chart.png",
    verified_against="p17 prose (text layer) + p26 consonant chart",
    visual_source="work/arabic/page_17.png")

# --- C. vocab (9 notes, 2 cards each) — MSA primary, dialects on the back
for arabic, meaning, translit, a_formal, a_masri, a_shaami, extra in VOCAB:
    core, qual = meaning
    mline = f"{{{{c2::{core}}}}}" + (f" — {qual}" if qual else "")
    text = (f"{{{{c1::{arabic}}}}}<br>" + mline)
    lines = [f"Cue: MSA (Formal/written) — <i>{translit}</i> [sound:{a_formal}]"]
    dial = []
    if a_masri: dial.append(f"Egyptian [sound:{a_masri}]")
    if a_shaami: dial.append(f"Levantine [sound:{a_shaami}]")
    if dial: lines.append("Ex: " + " · ".join(dial))
    if extra: lines.append(f"Distinguish: {extra}")
    add(text, "<br><br>".join(lines), "C_vocab", [23],
        image="src_vocab_table.png",
        verified_against="Lingco lesson 8174 JSON (publisher Unicode + AB3e official audio, snapshot lingco_unit1_vocab.json)",
        verified_by="Arabic text taken verbatim from Lingco lesson JSON 2026-08-08 (NOT read off the scan); audio mapping cross-confirmed by publisher origin filenames (U1VE/U1VS/U1VSt)",
        visual_source="work/arabic/page_29.png")

# --- D. system / script facts
add("The Arabic alphabet contains {{c1::twenty-eight}} letters — consonants and long vowels — "
    "plus {{c2::fourteen}} symbols that act as short vowels, pronunciation markers, or grammatical markers.",
    "Cue: letters carry the skeleton; the symbol layer rides above and below it.",
    "D_system", [0], numeric=True,
    verified_against="p16 text layer (grounded EXACT)")
add("Arabic is written and read from {{c1::right to left}}.",
    "Cue: books and magazines open the \"other way\" from English ones.",
    "D_system", [3], verified_against="p17 text layer")
add("Arabic letters are connected {{c1::in both print AND script}} — unlike Latin letters, "
    "which connect only in handwriting.",
    "Why: this is why letters change shape by position — they must join their neighbors.",
    "D_system", [4], verified_against="p17 text layer")
add("\"{{c1::Initial}} position\" = the letter is not connected to a previous letter; "
    "\"{{c2::medial}} position\" = the letter sits between two other letters.",
    "Cue: Unit 1 teaches only the independent (isolated) forms — position variants come in Units 2-10.",
    "D_system", [5], verified_against="p17-18 text layer")
add("The basic skeleton of an Arabic word is made of {{c1::the consonants and long vowels}}; "
    "short vowels and other markers are {{c1::a separate layer}} written above and below it.",
    "Cue: two layers — skeleton first, vowelling second.",
    "D_system", [6], verified_against="p18 text layer")
add("The vowelling layer (vocalization) is normally {{c1::omitted}} in written Arabic — "
    "readers recognize words {{c1::without it}}.",
    "Pitfall: your textbook prints vowels while you learn; newspapers will not.",
    "D_system", [7,8], verified_against="p18 text layer (+ p21 recap)")
add("The Arabic writing system is regularly {{c1::phonetic}}: a one-to-one correspondence "
    "between sound and letter — words are written {{c1::the way they are pronounced}}.",
    "Distinguish: English spelling is the opposite — think <i>though / tough / through</i>.",
    "D_system", [8,9], verified_against="p21 text layer")
add("In this book's transliteration, emphatic sounds are marked by {{c1::UPPERCASE letters (S vs s)}}, "
    "and long vowels by {{c1::doubled vowels (aa, ii, uu)}}.",
    "Ex: <i>S</i> = emphatic ص while <i>s</i> = plain س; <i>aa</i> is held longer than <i>a</i>.",
    "D_system", [12], image="src_consonants1.png",
    verified_against="p25 text layer + chart render")
add("Transliteration is used only for words containing {{c1::letters you have not yet learned}} — "
    "and it does not replace {{c1::listening to the audio}}.",
    "Cue: the book drops transliteration for a word once its letters are all taught.",
    "D_system", [17], verified_against="p27 text layer")
add("Formal Arabic has only {{c1::three::how many}} vowel qualities — {{c1::a, i, u}} — each short or long; "
    "spoken Arabic adds {{c2::e and o}}.",
    "Cue: vowel length distinguishes emphatic consonants from their plain counterparts — listen for it.",
    "D_system", [13], numeric=True, image="src_vowels.png",
    verified_against="p26 text layer + vowel chart render")
add("Levantine pronunciation sometimes uses a very short, unstressed {{c1::schwa}} sound (ə).",
    "Ex: the <i>e</i> in <i>listen</i>.",
    "D_system", [14], verified_against="p26 text layer")

# --- E. registers & dialects
add("Formal Arabic — also called {{c1::Modern Standard}} or {{c1::Classical}} Arabic — is learned "
    "{{c2::at school (not at home)}} and is more a {{c2::written}} register than a spoken one.",
    "Cue: you hear it on news broadcasts; educated speakers mix it with dialect in formal settings.",
    "E_dialects", [10], verified_against="p22 text layer")
add("The {{c1::Levantine}} dialect group covers the Syrian, Lebanese, Palestinian, and Jordanian dialects.",
    "Cue: the Levant = the eastern Mediterranean coast region.",
    "E_dialects", [11], verified_against="p22 text layer")
add("This book's two colloquial varieties: <i>shaami</i> = {{c1::Levantine}}, and <i>maSri</i> = {{c1::Egyptian}}.",
    "Cue: <i>shaami</i> can mean Syrian, Damascene, or Levantine.<br><br>Cue: the dialogues use one city's flavor of each — see the sibling card.",
    "E_dialects", [20], verified_against="p28 text layer + Lingco lesson 8174 intro")
add("The book's <i>shaami</i> dialogues use the dialect of {{c1::Damascus}}; its <i>maSri</i> is the dialect of {{c2::Cairo}}.",
    "Cue: one city stands in for each dialect group.",
    "E_dialects", [18,19], verified_against="p28 text layer")
add("Egyptian (maSri) pronunciation is marked by a hard {{c1::g}} where other dialects say <i>j</i>, "
    "and by stress on the {{c1::second-to-last}} syllable.",
    "Ex: <i>gamiil</i> for <i>jamiil</i>.",
    "E_dialects", [21], verified_against="p28 text layer")
add("Levantine dialects are marked by a final {{c1::e}} vowel on certain nouns/adjectives where "
    "other dialects have <i>a</i>, and by a distinctive {{c1::intonation}}.",
    "Ex: Levantine <i>ahla</i> vs formal <i>ahlan</i>.",
    "E_dialects", [22], verified_against="p28 text layer")

# --- F. culture
add("Polite behavior requires you to say hello to {{c1::everyone in a room or place you enter}} — "
    "including a loosely defined {{c1::\"space\" someone regularly occupies}}.",
    "Ex: an outdoor work area, or a guard's position outside a building.<br><br>Cue: entering = greeting; the room does not have to have walls.",
    "F_culture", [24,25], verified_against="p31 text layer (grounded EXACT; page is photo-heavy)",
    visual_source="work/arabic/page_31.png")

# --- G. countries (20 notes, map legend p27)
for country, capital in COUNTRIES:
    if country == capital:
        text = f"Arab country whose capital city shares the country's name: {{{{c1::{country}}}}}."
    else:
        text = f"Arab country: <b>{country}</b> — capital {{{{c1::{capital}}}}}."
    add(text,
        "Cue: one of the 20 countries where Arabic is the main language of education and daily life.",
        "G_countries", [16], image="src_arab_map.png",
        verified_against="p27 map legend (rendered)",
        verified_by="country/capital pairs transcribed from map legend render 2026-08-08",
        visual_source="work/arabic/page_27.png")

out = os.path.join(W, "unit_1_cards.json")
json.dump(cards, open(out, "w"), indent=1, ensure_ascii=False)
counts = {}
for c in cards: counts[c["block"]] = counts.get(c["block"],0)+1
print(f"{len(cards)} notes -> {out}")
for k in sorted(counts): print(f"  {k}: {counts[k]}")
