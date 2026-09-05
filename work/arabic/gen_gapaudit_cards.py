#!/usr/bin/env python3
"""Cards for the 2026-09-05 Khouri gap audit: the words she taught by VOICE that were on
no slide list. Shapes enforced by check_block_spec.py — V1 (two-way), V2 (Cue: MSA),
V3 (translit clozed WITH the Arabic, R60), U1 (LRM), U2 (lowercase media), U3 (one home
per clip), U4 (no boilerplate), V4 (no maSri).
Audio provenance is in clips_gate.json (her voice, both-language gated on the FINAL mp3)
and ling/ (Lingco publisher clips, each verified by transcription before use)."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
LRM="‎"; SEP="<br><br>"
SRC="arabic"; SEG=2

def text(ar, tr, meaning, qualifier=None):
    t=f"{LRM}{{{{c1::{ar}}}}}{SEP}Transliteration: {{{{c1::{tr}}}}}{SEP}{{{{c2::{meaning}}}}}"
    return t+(f" — {qualifier}" if qualifier else "")

def snd(f): return f"[sound:{f}]"

N=[]
def V(slug, ar, tr, meaning, qualifier, back, audio=None, block="C_vocab", ev=""):
    N.append(dict(slug=slug, Text=text(ar,tr,meaning,qualifier),
                  **{"Back Extra": SEP.join([f"Cue: MSA — {tr}"]+back)},
                  Audio=snd(audio) if audio else "", block=block, source=SRC, segment=SEG,
                  origin="khouri-gap-audit-2026-09-05", evidence=ev, numeric=False,
                  verified_against="lecture recording + Alif Baa 3e answer key",
                  verified_by="mlx-whisper large-v3-turbo dual-language gate on the final mp3",
                  needs_human_check=False, image=None))

# ---------------------------------------------------------------- REQUIRED
V("ab","أب","ab","father","the formal word — and the first word she ever had you write",
  ["Why: <i>alif</i> + <i>baa</i>. The word opens on a glottal stop, so the <i>alif</i> carries a <i>hamza</i> on top.",
   "Distinguish: <i>ab</i> is the formal word for father; <i>baaba</i> is what a child calls him.",
   "Ex: she taught it as the payoff of the <i>hamza</i> lesson — \"and you learned your first word, <i>ab</i>.\"",
   "Pitfall: she called this REQUIRED."],
  "arabic_khouri_ab.mp3", ev="27 Aug 00:52:13 board work; reprised 3 Sep 00:07:20")
V("tuut","توت","tuut","berries, mulberries","the word she built to teach waaw as a long uu",
  ["Why: <i>taa</i> + <i>waaw</i> + <i>taa</i> — the <i>waaw</i> in the middle is the long <i>uu</i>.",
   "Ex: she added that for Arab children <i>tuut</i> is also the noise a train makes.",
   f"Ex: book audio {snd('arabic_vocab_u2_le6_tuut.mp3')}",
   "Pitfall: she called this REQUIRED, twice — \"This is required, write it also.\""],
  "arabic_khouri_tuut.mp3", ev="1 Sep 00:36:30; drilled again 3 Sep 00:24:09")

# ---------------------------------------------------------------- the father family
V("baaba","بابا","baaba","dad, papa","the child's word — the very first word she wrote on the board",
  ["Distinguish: <i>baaba</i> is informal, what a child says; <i>ab</i> is the formal word.",
   "Why: she chose it to show that <i>baa</i> and <i>alif</i> cannot simply sit side by side — the <i>alif</i> forces the <i>baa</i> before it into its initial form."],
  "arabic_khouri_baaba.mp3", ev="25 Aug 01:05:05; again 27 Aug 00:42:12")
V("abii","أبي","abii","my father","ab with the ending that means \"my\"",
  ["Why: the possessive \"my\" is a <i>yaa</i> stuck on the end of the noun — <i>ab</i> + <i>ii</i>. She wrote it on the board the day she taught <i>yaa</i>.",
   "Ex: her own answer when the class asked her — <i>ism abii Elias</i>, \"Elijah in English.\"",
   "Distinguish: the same <i>-ii</i> turns <i>baab</i> into <i>baabii</i>, my door."],
  "arabic_khouri_abii.mp3", ev="3 Sep 00:07:40 and 00:09:01")
V("abuuka_abuuki","أبوكَ / أبوكِ","abuuka / abuuki","your father","to a man / to a woman",
  ["Distinguish: <i>-ka</i> to a man, <i>-ki</i> to a woman — the same pair of endings as <i>ismuka</i> / <i>ismuki</i>.",
   "Ex: she went round the room asking it, switching gender as she went: \"I'm switching between men and women because I'm talking to men and women.\""],
  "arabic_khouri_abuuka_abuuki.mp3", ev="3 Sep 01:07:53-01:08:34")
V("maa_ism_abuuka","ما اسم أبوكَ؟ / ما اسم أبوكِ؟","maa ism abuuka? / maa ism abuuki?",
  "What is your father's name?","to a man / to a woman — she asked the whole room this",
  ["Why: no verb \"is\" — the question is just <i>what</i> + <i>the name of your father</i>.",
   "Ex: you answer <i>ism abii</i> + the name. Hers: <i>ism abii Elias</i>.",
   "Pitfall: <i>maa</i> goes with a noun, so it is <i>maa</i> here and never <i>hal</i>."],
  "arabic_khouri_maa_ism_abuuki.mp3", ev="3 Sep 01:11:19-01:11:50")

# ---------------------------------------------------------------- drill words she glossed
V("baat","بات","baat","he slept over","somewhere other than home — drill 2, and the long-aa half of her contrast",
  ["Distinguish: <i>baat</i> holds the <i>aa</i>; <i>bat</i> is the same letters said short. She drilled the pair to show what a long vowel is.",
   "Pitfall: nothing to do with the English word \"but\", which is what it sounds like."],
  "arabic_vocab_u2_le3_baat.mp3", ev="1 Sep 00:30; contrast drilled 3 Sep 00:40:46")
V("taabuut","تابوت","taabuut","a casket, a coffin","drill 4, the longest word in it",
  ["Why: <i>taa</i> + <i>alif</i> + <i>baa</i> + <i>waaw</i> + <i>taa</i>. She used it as the hard one because it carries both a long <i>aa</i> and a long <i>uu</i>.",
   "Ex: Sydney wrote it at the board and she said \"this is longer\" as the class worked through it."],
  "arabic_vocab_u2_le6_taabuut.mp3", ev="3 Sep 00:24:51-00:25:15")
V("baabii","بابي","baabii","my door","drill 11 — baab with the same \"my\" ending as abii",
  ["Why: <i>baab</i> + <i>-ii</i>. The <i>-ii</i> is a <i>yaa</i> on the end, exactly as in <i>abii</i>.",
   f"Ex: book audio {snd('arabic_vocab_u2_d11_baabii.mp3')}",
   "Ex: at the board she asked \"what's <i>baabii</i>?\" and answered it herself — \"my door.\""],
  "arabic_khouri_baabii.mp3", ev="3 Sep 00:30:02-00:31:47")
V("thawb","ثوب","thawb","a garment","the long white robe a Saudi man wears; also a woman's dress",
  ["Distinguish: in Syria the same garment is a <i>jallabiyya</i>; in Egypt <i>thawb</i> is closer to a jacket.",
   "Why: she built it letter by letter on the board — <i>thaa</i> + <i>waaw</i> + <i>baa</i>."],
  None, ev="1 Sep 00:40:18-00:40:47")
V("thawaab","ثواب","thawaab","a reward","she taught it as the opposite of punishment",
  ["Distinguish: the opposite of <i>caqaab</i>, punishment — that is how she introduced it, by asking the class for the antonym.",
   "Why: another word she built on the board from <i>thaa</i>, <i>waaw</i> and <i>alif</i>."],
  None, ev="1 Sep 00:42:58-00:43:06")
V("tuubuu","توبوا","tuubuu","repent!","said to a GROUP — the -uu on the end is the plural",
  ["Why: the <i>-uu</i> ending is what makes a verb plural. To one person it would be <i>tub</i>.",
   "Pitfall: she warned that Arabic plurals are \"very inconsistent\" and that broken plurals are a 102 topic — do not generalise this ending yet."],
  None, ev="1 Sep 00:45:10-00:45:31")

# ---------------------------------------------------------------- classroom words
V("harf","حَرف","Harf","a letter of the alphabet","the word she uses for the thing she teaches every class",
  ["Pitfall: the capital H is <i>Haa</i>, made in the throat with the muscles tightened — not an English h.",
   "Ex: she introduced it while starting the <i>waaw</i> lesson — \"<i>Harf waaw</i>.\""],
  None, ev="1 Sep 00:32-00:34, written on the board")
V("ahsant","أَحسَنتَ / أَحسَنتِ","aHsanta / aHsanti","Good job! Well done!","to a man / to a woman — she says this to the class constantly",
  ["Distinguish: <i>-a</i> to a man, <i>-i</i> to a woman. Her words: \"you're going to hear <i>aHsant</i> for a man, <i>aHsanti</i> for ladies. You're going to learn those.\"",
   f"Ex: on a student by name {snd('arabic_khouri_ahsant_kyle.mp3')}",
   "Pitfall: the capital H is <i>Haa</i>, from the throat."],
  "arabic_khouri_ahsant.mp3", ev="27 Aug 01:09:00-01:09:16, then every class since")
V("sahh","صَحّ","SaHH","Correct! / Right?","her check-word at the board, both as praise and as a question",
  ["Distinguish: as a statement it means \"correct\"; said with a rising tone at the end of her own sentence it means \"right?\" and expects the class to answer.",
   "Pitfall: capital S is <i>Saad</i>, the emphatic s — not the <i>siin</i> of <i>ism</i>."],
  None, ev="1 Sep 00:44:16 \"SaHH means correct\"; used again 3 Sep 01:12:37")
V("yalla","يَلّا","yalla","Come on! Let's go!","how she moves the class along",
  ["Ex: \"Good job, Parker — <i>yalla</i>, who wants to ask me a question?\"",
   "Distinguish: colloquial and used everywhere, but it is not Formal Arabic — you will not be asked to write it."],
  "arabic_khouri_yalla.mp3", ev="3 Sep 01:06:31")

# ---------------------------------------------------------------- the speaking round
V("bil_arabi","بِالعَرَبي","bil-carabi","in Arabic","the tail of her vocabulary check: \"maa baab ___?\"",
  ["Why: <i>bi-</i> is the preposition \"in\" (the same <i>bi-</i> as in <i>ahlan bika</i>) stuck onto <i>al-carabi</i>.",
   "Ex: she asks <i>maa baab bil-carabi?</i> and wants the meaning back.",
   "Pitfall: the c is <i>cayn</i> — say \"ah\", then start to shock yourself, but only a little."],
  "arabic_khouri_bil_arabi.mp3", ev="3 Sep 01:02:47-01:04:01")
V("bil_inglizi","بِالإنجليزي","bil-ingliizi","in English","the other half of her check — she flips between the two to catch you",
  ["Ex: <i>maa baab bil-ingliizi?</i> — and the answer she wanted was the English word \"door\". She said \"I tricked you\" when the class answered in the wrong language.",
   "Distinguish: same <i>bi-</i> + <i>al-</i> frame as <i>bil-carabi</i>; only the language name changes."],
  "arabic_khouri_bil_inglizi.mp3", ev="3 Sep 01:03:09-01:04:05")
V("ayy","أيّ","ayy","which","the word that makes her question pick ONE out of many: \"min ___ madiina anta?\"",
  ["Distinguish: <i>ayy</i> asks which one out of a set; <i>ayna</i> asks where. They are different words that look alike in transliteration.",
   "Ex: it came up because a student wanted to ask about a city rather than a place."],
  "arabic_khouri_ayy.mp3", ev="3 Sep 01:08:50-01:09:53")
V("min_ayy_madiina","مِن أيّ مدينة أنتَ؟ / أنتِ؟","min ayy madiina anta? / anti?",
  "From which city are you?","to a man / to a woman — the city version of min ayna anta",
  ["Distinguish: <i>min ayna anta?</i> asks where from in general; this asks specifically which CITY.",
   "Ex: her own answer — <i>ana min madiinat Dimashq</i>.",
   "Pitfall: <i>ayy</i> and <i>ayna</i> cannot both appear; pick one."],
  None, ev="3 Sep 01:09:44-01:10:02")
V("dimashq","دِمَشق","Dimashq","Damascus","her city — the answer she gives when the class asks her",
  ["Ex: <i>ana min madiinat Dimashq</i> — \"I am from the city of Damascus.\"",
   "Pitfall: the English name Damascus and the Arabic <i>Dimashq</i> share almost nothing — you cannot guess this one."],
  None, ev="27 Aug 01:10:55; again 3 Sep 01:10")
V("suuriya","سوريا","Suuriya","Syria","the country she is from",
  ["Ex: her full answer to you on 3 Sep — <i>ana min Suuriya, askun fii Lynchburg</i>: I am from Syria, I live in Lynchburg."],
  "arabic_khouri_ana_min_suuriya.mp3", ev="3 Sep 01:06:15")

# ---------------------------------------------------------------- writing system
V("tashkiil","تَشكيل","tashkiil","the short-vowel marks, as a set","fatHa, Damma, kasra and sukuun together",
  ["Why: her words — \"<i>tashkiil</i> means everything, all short vowels.\" She then said \"you need to learn these words.\"",
   "Pitfall: ordinary written Arabic carries NO <i>tashkiil</i> — not newspapers, not subtitles. You will be weaned off it."],
  None, ev="3 Sep 00:44:31; flagged as vocabulary 1 Sep 01:04")

# ---------------------------------------------------------------- extra / incidental
V("taab","تاب","taab","he repented","drill 2 — she offered this one as optional extra",
  ["Pitfall: nothing to do with an English \"tab\". She said so directly: \"not the English tab, Arabic <i>taab</i>, he repented.\"",
   "Distinguish: she marked <i>baab</i> as required and this one as extra — \"if you want to learn extra, you could add that one.\""],
  "arabic_khouri_taab.mp3", ev="1 Sep 00:24:40")
V("umm","أُمّ","umm","mother","her example of an alif carrying hamza with a Damma",
  ["Why: the word opens on a glottal stop with a <i>u</i> sound, so the <i>hamza</i> sits ON TOP of the <i>alif</i> and takes a <i>Damma</i>.",
   "Distinguish: <i>ab</i> is father, <i>umm</i> is mother."],
  "arabic_khouri_umm.mp3", ev="3 Sep 00:48:42")
V("jaaa","جاءَ","jaa'a","he came","her example of a hamza standing alone on the line",
  ["Why: at the END of a word a <i>hamza</i> can sit by itself on the line — it is only at the START that it must ride an <i>alif</i>."],
  None, ev="27 Aug 00:51:35")
V("jallabiyya","جَلّابيّة","jallabiyya","a long robe","the Syrian word for the garment a Saudi calls a thawb",
  ["Distinguish: same garment, different country's word — <i>thawb</i> in Saudi Arabia, <i>jallabiyya</i> in Syria."],
  None, ev="1 Sep 00:40:28")

# ---------------------------------------------------------------- script concepts (not vocab)
N.append(dict(slug="al_no_hamza",
  Text=("A word that begins with a glottal stop has to be written {{c1::with a hamza on its alif}} — "
        "above the alif for a and u, below it for i. The one word that takes no hamza at all is "
        "the definite article {{c2::<i>al-</i>}}."),
  **{"Back Extra": SEP.join([
     "Why: she taught it as a listening test — if you hear a word start with a glottal stop, think <i>hamza</i> straight away.",
     "Ex: <i>ab</i> and <i>umm</i> both take the <i>hamza</i>; <i>al-</i> does not.",
     "Pitfall: the <i>alif</i> still sounds the same either way — the <i>hamza</i> is about how it is written, not how it is said."])},
  Audio="", block="D_script", source=SRC, segment=SEG, origin="khouri-gap-audit-2026-09-05",
  evidence="3 Sep 00:48:26-00:49:26", numeric=False,
  verified_against="lecture recording", verified_by="mlx-whisper english pass",
  needs_human_check=False, image=None))
N.append(dict(slug="letter_names_hamza",
  Text=("The NAME of a letter ends in a <i>hamza</i> that the letter itself does not have — so "
        "baa, taa and thaa are written {{c1::باء · تاء · ثاء}}, not {{c2::با · تا · ثا}}."),
  **{"Back Extra": SEP.join([
     "Why: she wrote the names beside the letters on the board and stopped to point the <i>hamza</i> out.",
     "Pitfall: she also warned not to confuse the mark <i>hamza</i> with the personal name Hamza, which has a <i>Haa</i>.",
     "Ex: <i>waaw</i> and <i>yaa</i> follow the same pattern — واو and ياء."])},
  Audio="", block="D_script", source=SRC, segment=SEG, origin="khouri-gap-audit-2026-09-05",
  evidence="1 Sep 00:10:51-00:12:22, board", numeric=False,
  verified_against="lecture recording + board frame at 00:25:00", verified_by="board frame + english pass",
  needs_human_check=False, image=None))
N.append(dict(slug="waaw_al_jamaaca",
  Text=("The <i>-uu</i> that turns a verb plural — as in tuubuu — is called "
        "{{c1::<i>waaw al-jamaaca</i>}}, literally {{c2::the waaw of the group}}."),
  **{"Back Extra": SEP.join([
     "Ex: <i>tub</i> is \"repent\" to one person; <i>tuubuu</i> is \"repent\" to a group.",
     "Pitfall: this is one plural pattern, not the rule. She called Arabic plurals \"very inconsistent\" and pushed broken plurals to 102."])},
  Audio="", block="D_script", source=SRC, segment=SEG, origin="khouri-gap-audit-2026-09-05",
  evidence="1 Sep 00:45:31", numeric=False,
  verified_against="lecture recording", verified_by="mlx-whisper english pass",
  needs_human_check=False, image=None))

json.dump(N, open(os.path.join(HERE,"gapaudit_cards.json"),"w"), ensure_ascii=False, indent=1)
print(f"{len(N)} notes")
from collections import Counter
print(Counter(n["block"] for n in N))
print("with audio:", sum(1 for n in N if n["Audio"]))
