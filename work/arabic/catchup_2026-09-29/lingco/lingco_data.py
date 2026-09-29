# -*- coding: utf-8 -*-
"""Hand-curated item data for Lingco (Alif Baa 3e) Units 1-4 — every item that has publisher audio.

Sources, in authority order: Lingco lesson text / tables (~/arabic-vault) = the book (Zotero SPRRWAP7)
> Alif Baa answer key (Zotero 8I2BY7AA; dictation + letter-connection answers) > own knowledge (flagged).

Item tuple for word lessons:
    (item_no, arabic_vowelled, translit, meaning, word_type, real_word, confidence, notes)
  * pairs: arabic "A / B", translit "a / b", meaning = [meaning_A, meaning_B], word_type "pair"
  * arabic_vowelled = the printed form plus any missing short vowels / sukuun / shadda (the build flags
    `vowels_added` automatically by diffing against the printed form).
"""

# ----------------------------------------------------------------------------------------------
# UNIT 1
# ----------------------------------------------------------------------------------------------
# Listening Exercise 1 — letter-sound videos (AB3e_pronouncing_NN_<name>.mp4). Close-up of a mouth
# pronouncing the letter; exact utterance (name vs. sound) not verified.
LETTER_VIDEOS = [
    # nn, letter, name (vowelled), translit, sound description
    (1, "ا", "أَلِف", "alif", "long vowel aa (alif is also the seat of hamza)"),
    (2, "ب", "باء", "baa'", "b"),
    (3, "ت", "تاء", "taa'", "t"),
    (4, "ث", "ثاء", "thaa'", "th as in 'three'"),
    (5, "ج", "جيم", "jiim", "j as in 'jam'"),
    (6, "ح", "حاء", "Haa'", "H — a strong, breathy h from the throat (no English equivalent)"),
    (7, "خ", "خاء", "khaa'", "kh — like the ch in German 'Bach'"),
    (8, "د", "دال", "daal", "d"),
    (9, "ذ", "ذال", "dhaal", "dh — th as in 'this'"),
    (10, "ر", "راء", "raa'", "r — tapped/rolled r"),
    (11, "ز", "زاي", "zaay", "z"),
    (12, "س", "سين", "siin", "s"),
    (13, "ش", "شين", "shiin", "sh"),
    (14, "ص", "صاد", "Saad", "S — emphatic (deep) s"),
    (15, "ض", "ضاد", "Daad", "D — emphatic (deep) d"),
    (16, "ط", "طاء", "Taa'", "T — emphatic (deep) t"),
    (17, "ظ", "ظاء", "DHaa'", "DH — emphatic (deep) dh"),
    (18, "ع", "عَيْن", "cayn", "c (cayn) — voiced sound squeezed in the throat (no English equivalent)"),
    (19, "غ", "غَيْن", "ghayn", "gh — like a French/Parisian r"),
    (20, "ف", "فاء", "faa'", "f"),
    (21, "ق", "قاف", "qaaf", "q — a k made deep in the throat"),
    (22, "ك", "كاف", "kaaf", "k"),
    (23, "ل", "لام", "laam", "l"),
    (24, "م", "ميم", "miim", "m"),
    (25, "ن", "نون", "nuun", "n"),
    (26, "ه", "هاء", "haa'", "h"),
    (27, "و", "واو", "waaw", "w / long vowel uu"),
    (28, "ي", "ياء", "yaa'", "y / long vowel ii"),
]

# Listening Exercise 2 — dialect variation. Lingco table columns: Tunisia | Egypt | Lebanon | Oman.
# Clip numbers: Lebanon 01-05, Egypt 06-10 (EXCLUDED), Oman 11-15, Tunisia 16-20; row order inside
# each block = Good morning! / How are you? / Good / Good-bye / I love <country>.
LE2_PHRASES = ["Good morning!", "How are you?", "Good (fine)", "Good-bye", "I love {country}"]
LE2_BLOCKS = {  # first clip number -> (dialect label, register, country name for 'I love …')
    1: ("Lebanese", "shaami", "Lebanon"),
    11: ("Omani", "omani", "Oman"),
    16: ("Tunisian", "tunisian", "Tunisia"),
}

# Drill 3 — Arab countries + capitals. Item = the book's/map's number (= Lingco's on-screen label).
# NOTE: here the publisher file number is NOT the item number: AB3e_U1D3-01..18 run in English
# alphabetical order (Bahrain, Emirates, Iraq, Israel/Palestine, Jordan, … Yemen) with Algeria (19) and
# Egypt (20) appended; Lingco's labels map them back to the map numbers. Mapping is read from the Lingco table.
COUNTRIES = [
    # book no, country (vowelled), capital (vowelled), translit, English
    (1, "المَغْرِب", "الرِّباط", "al-maghrib — ar-ribaaT", "Morocco — capital: Rabat"),
    (2, "موريتانْيا", "نُواكْشوط", "muuriitaanyaa — nuwaakshuuT", "Mauritania — capital: Nouakchott"),
    (3, "الجَزائِر", "الجَزائِر", "al-jazaa'ir — al-jazaa'ir", "Algeria — capital: Algiers (same name as the country)"),
    (4, "تونِس", "تونِس", "tuunis — tuunis", "Tunisia — capital: Tunis (same name as the country)"),
    (5, "ليبْيا", "طَرابُلُس", "liibyaa — Taraabulus", "Libya — capital: Tripoli"),
    (6, "مِصْر", "القاهِرة", "miSr — al-qaahira", "Egypt — capital: Cairo"),
    (7, "السّودان", "الخَرْطوم", "as-suudaan — al-kharTuum", "Sudan — capital: Khartoum"),
    (8, "الصّومال", "مَقَديشو", "aS-Suumaal — maqadiishuu", "Somalia — capital: Mogadishu"),
    (9, "الأُرْدُنّ", "عَمّان", "al-urdunn — cammaan", "Jordan — capital: Amman"),
    (10, "فِلَسْطين", "القُدْس", "filasTiin — al-quds", "Palestine (book: 'Israel/Palestine') — Jerusalem"),
    (11, "لُبْنان", "بَيْروت", "lubnaan — bayruut", "Lebanon — capital: Beirut"),
    (12, "سورْيا", "دِمَشْق", "suuryaa — dimashq", "Syria — capital: Damascus"),
    (13, "العِراق", "بَغْداد", "al-ciraaq — baghdaad", "Iraq — capital: Baghdad"),
    (14, "الكُوَيْت", "الكُوَيْت", "al-kuwayt — al-kuwayt", "Kuwait — capital: Kuwait City (same name)"),
    (15, "السَّعودِيّة", "الرِّياض", "as-sacuudiyya — ar-riyaaD", "Saudi Arabia — capital: Riyadh"),
    (16, "قَطَر", "الدَّوْحة", "qaTar — ad-dawHa", "Qatar — capital: Doha"),
    (17, "البَحْرَيْن", "المَنامة", "al-baHrayn — al-manaama", "Bahrain — capital: Manama"),
    (18, "الإِمارات", "أَبو ظَبْي", "al-imaaraat — abuu DHabii", "United Arab Emirates — capital: Abu Dhabi"),
    (19, "عُمان", "مَسْقَط", "cumaan — masqaT", "Oman — capital: Muscat"),
    (20, "اليَمَن", "صَنْعاء", "al-yaman — Sancaa'", "Yemen — capital: Sanaa"),
]

# ----------------------------------------------------------------------------------------------
# LISTENING EXERCISES + DRILLS (Units 2-4). printed = where the printed form comes from:
#   'lingco'  numbered list in ~/arabic-vault/data/lessons/unit-0N/<file>
#   'table'   Lingco table (other_tables.json; U3 D6 / U3 D9)
#   'key'     Alif Baa answer key (dictation / letter-connection drills print no words)
# ----------------------------------------------------------------------------------------------
LESSONS = []

def L(unit, code, lesson, purpose, targets, marks, printed, items, lesson_file=None, key_printed=None,
      clip_note=None):
    LESSONS.append(dict(unit=unit, code=code, lesson=lesson, purpose=purpose, targets=targets, marks=marks,
                        printed=printed, items=items, lesson_file=lesson_file, key_printed=key_printed,
                        clip_note=clip_note))

EGY_G = ("Clip says the word in the three regional pronunciations of ج (j / zh / hard Egyptian g) — "
         "it CONTAINS an Egyptian variant: trim to the first reading or avoid as card audio.")

# ---------------- UNIT 2 ----------------
L(2, "le1", "Listening Exercise 1", "Frontal vs deep alif (each clip = a contrast pair)", ["ا"], [],
  "lingco", lesson_file="unit-02/00_listening_exercise_1.txt", items=[
    (1, "تاب / طاب", "taab / Taab", ["he repented", "it was good, pleasant"], "pair", True, "med",
     "Pausal verb readings assumed (taab(a) / Taab(a)). Contrast: frontal ت vs deep ط."),
    (2, "ساح / صاح", "saaH / SaaH", ["it flowed; he roamed, toured", "he shouted, cried out"], "pair", True, "low",
     "ساحَ is 'to flow (liquid) / to travel about'; صاحَ 'to shout' is certain. Contrast س vs ص."),
    (3, "داني / ضاني", "daanii / Daanii", ["near, close (also the name Dani)", "of sheep — mutton/lamb (Egyptian usage: لَحْم ضاني)"],
     "pair", True, "low", "Minimal pair for د vs ض; both meanings uncertain/rare."),
    (4, "ذال / ظالِم", "dhaal / DHaalim", ["the letter dhaal (ذ)", "unjust; an oppressor, wrongdoer"], "pair", True, "high",
     "Contrast ذ vs ظ."),
])
L(2, "le2", "Listening Exercise 2", "Pronouncing ب (frontal vowels)", ["ب"], [], "lingco",
  lesson_file="unit-02/03_listening_exercise_2.txt", items=[
    (1, "باء", "baa'", "the letter name baa (ب)", "letter-name", True, "high", ""),
    (2, "باب", "baab", "door", "noun", True, "high", ""),
    (3, "لُبْنان", "lubnaan", "Lebanon", "place", True, "high", ""),
    (4, "ليبْيا", "liibyaa", "Libya", "place", True, "high", ""),
    (5, "بَيْت", "bayt", "house", "noun", True, "high", ""),
    (6, "حُبّ", "Hubb", "love", "noun", True, "high", "Printed حب; shadda (Unit 5) added."),
])
L(2, "le3", "Listening Exercise 3", "Pronouncing ت", ["ت"], [], "lingco",
  lesson_file="unit-02/05_listening_exercise_3.txt", items=[
    (1, "تاء", "taa'", "the letter name taa (ت)", "letter-name", True, "high", ""),
    (2, "بات", "baat", "he spent the night", "verb", True, "med", "Pausal reading of باتَ (baata)."),
    (3, "توت", "tuut", "mulberries; berries (collective)", "noun", True, "high", "Dr. Khouri added توت ('berries') to the required list."),
    (4, "وَتَد", "watad", "tent peg, stake", "noun", True, "high", ""),
    (5, "بِنْت", "bint", "girl; daughter", "noun", True, "high", ""),
    (6, "شِتاء", "shitaa'", "winter", "noun", True, "high", ""),
])
L(2, "d2", "Drill 2", "Dictation (ا ب ت) — video; write what you hear", ["ا", "ب", "ت"], [], "key", items=[
    (1, "با", "baa", "(syllable 'baa' — no meaning)", "syllable", False, "high", "Sound drill."),
    (2, "تاب", "taab", "he repented", "verb", True, "med", "Pausal reading of تابَ."),
    (3, "باتا", "baataa", "(no meaning — sound/spelling drill)", "nonword", False, "high", ""),
    (4, "تابا", "taabaa", "(no meaning here — sound/spelling drill)", "nonword", False, "med",
     "Could technically be read as the dual verb 'the two of them repented', but here it is a syllable string."),
    (5, "باب", "baab", "door", "noun", True, "high", ""),
    (6, "بات", "baat", "he spent the night", "verb", True, "med", "Pausal reading of باتَ."),
], key_printed=["با", "تاب", "باتا", "تابا", "باب", "بات"])
L(2, "le4", "Listening Exercise 4", "Listening to ث", ["ث"], [], "lingco",
  lesson_file="unit-02/08_listening_exercise_4.txt", items=[
    (1, "ثاء", "thaa'", "the letter name thaa (ث)", "letter-name", True, "high", ""),
    (2, "ثابِت", "thaabit", "firm, fixed, stable (also a man's name, Thabit)", "adjective", True, "high", ""),
    (3, "تثبت", "tathbut / tuthbit (unclear)", "unclear without the audio: tathbut 'she stays firm / you (m.) stay firm' OR tuthbit 'she proves / you (m.) prove'",
     "verb", True, "low", "Printed unvowelled; vowels NOT added because the reading is ambiguous — confirm from the clip."),
    (4, "أَثاث", "athaath", "furniture", "noun", True, "high", "Lingco prints اثاث without the hamza (hamza is taught in Unit 4); correct spelling أَثاث."),
    (5, "بَثّ", "bathth", "broadcast, transmission (noun)", "noun", True, "med", "Printed بث; shadda added."),
])
L(2, "le5", "Listening Exercise 5", "Contrasting ث (th) and ذ (dh) (each clip = a pair)", ["ث", "ذ"], [], "lingco",
  lesson_file="unit-02/09_listening_exercise_5.txt", items=[
    (1, "ثاب / ذاب", "thaab / dhaab", ["he returned, came back", "it melted, dissolved"], "pair", True, "med", "Pausal verb readings."),
    (2, "بُثور / بُذور", "buthuur / budhuur", ["pimples, blisters (plural of بَثْرة)", "seeds (plural of بَذْرة)"], "pair", True, "high", ""),
    (3, "آثار / آذار", "aathaar / aadhaar", ["traces; ruins, antiquities (plural of أَثَر)", "March (month name used in the Levant and Iraq)"], "pair", True, "high", ""),
    (4, "تَثوب / تَذوب", "tathuub / tadhuub", ["she returns; you (m.) return (to your senses)", "she/it melts; you (m.) melt"], "pair", True, "med", ""),
    (5, "جَثّ / جَذّ", "jathth / jadhdh", ["he uprooted (rare)", "he cut off (rare)"], "pair", True, "low",
     "Rare/obscure verbs — basically a sound contrast. Printed جث / جذ; vowels and shadda assumed."),
])
L(2, "le6", "Listening Exercise 6", "Long vowel و (uu) — give it full length", ["و"], [], "lingco",
  lesson_file="unit-02/12_listening_exercise_6.txt", items=[
    (1, "توت", "tuut", "mulberries; berries (collective)", "noun", True, "high", ""),
    (2, "تابوت", "taabuut", "coffin, casket", "noun", True, "high", "Dr. Khouri glossed it 'casket'."),
    (3, "ثُبوت", "thubuut", "firmness; proof, being established", "noun", True, "med", ""),
    (4, "تونِس", "tuunis", "Tunisia; Tunis", "place", True, "high", ""),
    (5, "تَحْبو", "taHbuu", "she crawls; you (m.) crawl (like a baby)", "verb", True, "low",
     "Printed تحبو; reading taHbuu assumed (verb حَبا 'to crawl') — confirm from the clip."),
])
L(2, "d4", "Drill 4", "Dictation (ث, و) — video", ["ث", "و"], [], "key", items=[
    (1, "ثاب", "thaab", "he returned, came back", "verb", True, "med", "Pausal reading of ثابَ."),
    (2, "توت", "tuut", "mulberries; berries (collective)", "noun", True, "high", ""),
    (3, "توب", "tuub", "(no formal-Arabic meaning; colloquially 'robe, dress' or 'repent!')", "nonword", False, "low",
     "Formal 'repent!' is تُبْ (tub) and 'robe' is ثَوْب (thawb); treat as a sound/spelling item."),
    (4, "تابوت", "taabuut", "coffin, casket", "noun", True, "high", ""),
], key_printed=["ثاب", "توت", "توب", "تابوت"])
L(2, "le7", "Listening Exercise 7", "Long vowel ي (ii)", ["ي"], [], "lingco",
  lesson_file="unit-02/15_listening_exercise_7.txt", items=[
    (1, "توبي", "tuubii", "repent! (said to a female)", "verb", True, "med", ""),
    (2, "تَثْبيت", "tathbiit", "fixing, securing; confirmation; (software) installation", "noun", True, "high", ""),
    (3, "ليبي", "liibii", "Libyan (m.)", "adjective", True, "high", ""),
    (4, "تُثْبِتي", "tuthbitii", "(that) you (f.) prove / confirm", "verb", True, "low",
     "Printed تثبتي unvowelled; reading tuthbitii assumed from Unit 2 LE11 item 2 (تُثبِتي) — could be tathbutii."),
])
L(2, "d5", "Drill 5", "Dictation (ي) — video", ["ي"], [], "key", items=[
    (1, "ثوبا", "thuubaa", "(no meaning — sound/spelling drill)", "nonword", False, "med", ""),
    (2, "بيتي", "biitii", "my house (Dr. Khouri's gloss; the formal word is بَيْتي baytii)", "noun", True, "med",
     "Before short vowels are taught the clip probably reads it with a long ii; Dr. Khouri taught it in class as 'my house' (بيت + ي)."),
    (3, "بيتا", "biitaa", "(no meaning — sound/spelling drill)", "nonword", False, "med", ""),
    (4, "باتي", "baatii", "(no meaning — sound/spelling drill)", "nonword", False, "med", ""),
], key_printed=["ثوبا", "بيتي", "بيتا", "باتي"])
L(2, "le8", "Listening Exercise 8", "Hearing vowel length — first word long vowel, second short (each clip = a pair)", [], ["long vs short vowels"], "lingco",
  lesson_file="unit-02/18_listening_exercise_8.txt", items=[
    (1, "ساد / سَدّ", "saad / sadd", ["he prevailed, ruled", "dam; blocking"], "pair", True, "med", "Printed سَد; shadda added."),
    (2, "توب / تُب", "tuub / tub", ["(no formal meaning — colloquial 'robe' / 'repent!')", "repent! (said to a male)"], "pair", True, "low",
     "First member is not a formal-Arabic word."),
    (3, "شابّ / شَبّ", "shaabb / shabb", ["young man", "he grew up; (a fire) blazed"], "pair", True, "med", "Printed شاب / شَب; shadda added."),
    (4, "بير / بِرّ", "biir / birr", ["a well (informal spelling of بِئْر)", "righteousness; kindness (especially to parents)"], "pair", True, "med", "Printed بِر; shadda added."),
    (5, "تَقول / تَقُل", "taquul / taqul", ["she says; you (m.) say", "(don't) say — short form, as in لا تَقُلْ"], "pair", True, "med", ""),
])
L(2, "le9", "Listening Exercise 9", "Contrasting alif (aa) and fatHa (a)", ["ا"], ["fatHa"], "lingco",
  lesson_file="unit-02/21_listening_exercise_9.txt", items=[
    (1, "ثابَت", "thaabat", "she returned, came back", "verb", True, "med", ""),
    (2, "تابَ", "taaba", "he repented", "verb", True, "high", ""),
    (3, "باتَت", "baatat", "she spent the night", "verb", True, "high", ""),
    (4, "تابَت", "taabat", "she repented", "verb", True, "high", ""),
    (5, "ثَبات", "thabaat", "firmness, stability", "noun", True, "high", ""),
])
L(2, "d8", "Drill 8", "FatHa dictation — add fatHa where you hear it", [], ["fatHa"], "key",
  lesson_file="unit-02/23_drill_8.txt", items=[
    (1, "تَثْبيت", "tathbiit", "fixing, securing; confirmation; installation", "noun", True, "high", ""),
    (2, "بَتات", "bataat", "(rare) household goods; best known in بَتاتاً 'absolutely (not), at all'", "noun", True, "low", ""),
    (3, "باتَت", "baatat", "she spent the night", "verb", True, "high", ""),
    (4, "ثَبات", "thabaat", "firmness, stability", "noun", True, "high", ""),
    (5, "ثَبَت", "thabat", "he/it stood firm (the verb ثَبَتَ said without its final vowel)", "verb", True, "med", ""),
    (6, "ثابَت", "thaabat", "she returned, came back", "verb", True, "med", ""),
], key_printed=["تَثبيت", "بَتات", "باتَت", "ثَبات", "ثَبَت", "ثابَت"])
L(2, "le10", "Listening Exercise 10", "Hearing and pronouncing Damma", [], ["Damma"], "lingco",
  lesson_file="unit-02/24_listening_exercise_10.txt", items=[
    (1, "تُب", "tub", "repent! (said to a male)", "verb", True, "med", ""),
    (2, "بُثّ", "buthth", "broadcast! / spread! (said to a male)", "verb", True, "low", "Printed بُث; shadda added."),
    (3, "ثُبوت", "thubuut", "firmness; proof, being established", "noun", True, "med", ""),
    (4, "حُبوب", "Hubuub", "grains, seeds; pills (plural of حَبّة)", "noun", True, "high", ""),
    (5, "صُبّ", "Subb", "pour! (said to a male)", "verb", True, "med", "Printed صُب; shadda added."),
    (6, "تَثْبُت", "tathbut", "she stays firm; you (m.) stay firm", "verb", True, "med", ""),
])
L(2, "le11", "Listening Exercise 11", "Pronouncing kasra", [], ["kasra"], "lingco",
  lesson_file="unit-02/26_listening_exercise_11.txt", items=[
    (1, "ثِب", "thib", "jump! leap! (said to a male)", "verb", True, "med", "Imperative of وَثَبَ."),
    (2, "تُثْبِتي", "tuthbitii", "(that) you (f.) prove / confirm", "verb", True, "med", ""),
    (3, "بِت", "bit", "spend the night! (said to a male)", "verb", True, "med", ""),
    (4, "طِبّ", "Tibb", "medicine (the field)", "noun", True, "high", "Printed طِب; shadda added."),
    (5, "تُحِبّ", "tuHibb", "you (m.) love; she loves", "verb", True, "high", "Printed تُحِب; shadda added."),
    (6, "كِتابي", "kitaabii", "my book", "noun", True, "high", ""),
])
L(2, "d10", "Drill 10", "Short vowel dictation — write all short vowels", [], ["fatHa", "Damma", "kasra"], "key",
  lesson_file="unit-02/28_drill_10.txt", items=[
    (1, "ثَبُتَت", "thabutat", "she/it became firm", "verb", True, "med", ""),
    (2, "تُبْتُ", "tubtu", "I repented", "verb", True, "med", ""),
    (3, "تَبيت", "tabiit", "she spends the night; you (m.) spend the night", "verb", True, "high", ""),
    (4, "تَتوب", "tatuub", "she repents; you (m.) repent", "verb", True, "high", ""),
    (5, "تَثْبُت", "tathbut", "she stays firm; you (m.) stay firm", "verb", True, "med", ""),
    (6, "ثُبوت", "thubuut", "firmness; proof, being established", "noun", True, "med", ""),
], key_printed=["ثَبُتَت", "تُبتُ", "تَبيت", "تَتوب", "تَثبُت", "ثُبوت"])
L(2, "d11", "Drill 11", "Dictation with all vowels — video", [], ["long + short vowels"], "key", items=[
    (1, "بابي", "baabii", "my door", "noun", True, "high", ""),
    (2, "توبي", "tuubii", "repent! (said to a female)", "verb", True, "med", ""),
    (3, "ثُبوت", "thubuut", "firmness; proof, being established", "noun", True, "med", ""),
    (4, "توبا", "tuubaa", "repent! (said to two people)", "verb", True, "low", "Rare dual imperative — may just be a sound string."),
    (5, "تَبيت", "tabiit", "she spends the night; you (m.) spend the night", "verb", True, "high", ""),
    (6, "ثَبات", "thabaat", "firmness, stability", "noun", True, "high", ""),
    (7, "تابَت", "taabat", "she repented", "verb", True, "high", ""),
    (8, "ثوبي", "thuubii", "my robe / my garment (formal spelling ثَوْبي thawbii)", "noun", True, "low",
     "The key prints no fatHa, so the clip reads a long uu (colloquial 'thoob'); formal is thawbii."),
], key_printed=["بابي", "توبي", "ثُبوت", "توبا", "تَبيت", "ثَبات", "تابَت", "ثوبي"])
L(2, "d12", "Drill 12", "Reading aloud — check your pronunciation", [], [], "lingco",
  lesson_file="unit-02/30_drill_12.txt", items=[
    (1, "بَثّ", "bathth", "broadcast, transmission (noun)", "noun", True, "med", "Printed بَث; shadda added."),
    (2, "بابي", "baabii", "my door", "noun", True, "high", ""),
    (3, "تُثْبِت", "tuthbit", "she proves; you (m.) prove / confirm", "verb", True, "med", ""),
    (4, "ثُب", "thub", "come back! return! (said to a male; rare)", "verb", True, "low", "Imperative of ثابَ يَثوبُ."),
    (5, "ثَبات", "thabaat", "firmness, stability", "noun", True, "high", ""),
    (6, "تَبات", "tabaat", "(no standard meaning found — reading-practice string)", "nonword", False, "low",
     "Colloquial 'she spends the night' (formal تَبيت) is possible."),
    (7, "تابا", "taabaa", "the two of them (m.) repented", "verb", True, "low", "Rare dual form; may just be a sound string."),
    (8, "ثابِت", "thaabit", "firm, fixed, stable", "adjective", True, "high", ""),
    (9, "توبي", "tuubii", "repent! (said to a female)", "verb", True, "med", ""),
    (10, "تيتو", "tiituu", "(no meaning — reading-practice string; possibly the name 'Tito')", "nonword", False, "low", ""),
    (11, "ثابَت", "thaabat", "she returned, came back", "verb", True, "med", ""),
    (12, "تَثْبيت", "tathbiit", "fixing, securing; confirmation; installation", "noun", True, "high", ""),
])

# ---------------- UNIT 3 ----------------
L(3, "le1", "Listening Exercise 1", "Regional variation of ج (j / zh / g)", ["ج"], [], "lingco",
  lesson_file="unit-03/00_listening_exercise_1.txt", clip_note=EGY_G, items=[
    (1, "تاج", "taaj", "crown", "noun", True, "high", ""),
    (2, "جُبّ", "jubb", "well, pit (like the well Joseph was thrown into)", "noun", True, "med", "Printed جُب; shadda added."),
    (3, "تُجيب", "tujiib", "she answers; you (m.) answer", "verb", True, "high", ""),
    (4, "دَجاج", "dajaaj", "chicken (collective — one hen is دَجاجة)", "noun", True, "high", ""),
])
L(3, "d1", "Drill 1", "Dictation (ج) — video", ["ج"], [], "key", items=[
    (1, "جاب", "jaab", "he roamed, crossed (formal جابَ); in spoken Arabic 'he brought'", "verb", True, "med", ""),
    (2, "تاج", "taaj", "crown", "noun", True, "high", ""),
    (3, "جوبي", "juubii", "roam! explore! (said to a female)", "verb", True, "low", ""),
    (4, "جُبَب", "jubab", "robes, cloaks (plural of جُبّة jubba)", "noun", True, "med", ""),
    (5, "جُثَث", "juthath", "corpses, dead bodies (plural of جُثّة)", "noun", True, "high", ""),
    (6, "جيب", "jiib", "spoken Arabic 'bring!' (to a male) — or jayb 'pocket' if the clip has the diphthong", "verb", True, "low",
     "The key prints no fatHa (long ii), so not the diphthong jayb; confirm from the clip."),
], key_printed=["جاب", "تاج", "جوبي", "جُبَب", "جُثَث", "جيب"])
L(3, "le2", "Listening Exercise 2", "Pronouncing ح in various positions", ["ح"], [], "lingco",
  lesson_file="unit-03/03_listening_exercise_2.txt", items=[
    (1, "حَبيب", "Habiib", "beloved, darling, dear", "noun", True, "high", ""),
    (2, "بَحْث", "baHth", "research; search", "noun", True, "high", ""),
    (3, "تَبوح", "tabuuH", "she reveals (a secret); you (m.) reveal", "verb", True, "med", ""),
    (4, "صَباح", "SabaaH", "morning", "noun", True, "high", ""),
])
L(3, "d2", "Drill 2", "Dictation (ح) — video", ["ح"], [], "key", items=[
    (1, "حوت", "Huut", "whale", "noun", True, "high", ""),
    (2, "بَحْث", "baHth", "research; search", "noun", True, "high", ""),
    (3, "حَبيب", "Habiib", "beloved, darling, dear", "noun", True, "high", ""),
    (4, "تَحْت", "taHt", "under, below", "preposition", True, "high", ""),
    (5, "بوحي", "buuHii", "reveal it! tell! (said to a female)", "verb", True, "med", ""),
    (6, "باحَت", "baaHat", "she revealed (a secret)", "verb", True, "med", "Key prints باحَت (ت, not ث)."),
], key_printed=["حوت", "بَحث", "حَبيب", "تَحت", "بوحي", "باحَت"])
L(3, "le3", "Listening Exercise 3", "Pronouncing خ", ["خ"], [], "lingco",
  lesson_file="unit-03/06_listening_exercise_3.txt", items=[
    (1, "خاب", "khaab", "he failed; he was disappointed", "verb", True, "med", "Pausal reading of خابَ."),
    (2, "بَخيل", "bakhiil", "stingy; a miser", "adjective", True, "high", ""),
    (3, "باخ", "baakh", "it went stale, lost its flavor; (heat) died down", "verb", True, "low", ""),
    (4, "بَخْت", "bakht", "luck, fortune", "noun", True, "high", ""),
    (5, "تَخْتي", "takhtii", "my bed", "noun", True, "high", ""),
])
L(3, "d4", "Drill 4", "Letter connection — listen and write in the short vowels", ["ج", "ح", "خ"], ["short vowels"], "key", items=[
    (1, "خابَت", "khaabat", "she failed; she was disappointed", "verb", True, "high", ""),
    (2, "حِجاب", "Hijaab", "headscarf, veil", "noun", True, "high", ""),
    (3, "حَبيب", "Habiib", "beloved, darling, dear", "noun", True, "high", ""),
    (4, "تُخوت", "tukhuut", "beds (plural of تَخْت)", "noun", True, "med", ""),
    (5, "تَجوب", "tajuub", "she roams, travels through; you (m.) roam", "verb", True, "med", ""),
    (6, "بُحوث", "buHuuth", "research studies, papers (plural of بَحْث)", "noun", True, "high", ""),
    (7, "تَبوحي", "tabuuHii", "(that) you (f.) reveal (a secret)", "verb", True, "med", ""),
    (8, "حَجَبَت", "Hajabat", "she hid, veiled, blocked", "verb", True, "high", ""),
], key_printed=["خابَت", "حِجاب", "حَبيب", "تُخوت", "تَجوب", "بُحوث", "تَبوحي", "حَجَبَت"])
L(3, "d5", "Drill 5", "Dictation (ج ح خ) — video", ["ج", "ح", "خ"], [], "key", items=[
    (1, "حَجَبَ", "Hajaba", "he hid, veiled, blocked", "verb", True, "high", ""),
    (2, "باخ", "baakh", "it went stale, lost its flavor; (heat) died down", "verb", True, "low", ""),
    (3, "تَخْتي", "takhtii", "my bed", "noun", True, "high", ""),
    (4, "حاجّ", "Haajj", "pilgrim (someone who has made the Hajj)", "noun", True, "high", "Printed حاج; shadda added."),
    (5, "باحِث", "baaHith", "researcher", "noun", True, "high", ""),
    (6, "جابَت", "jaabat", "she roamed, crossed (formal); in spoken Arabic 'she brought'", "verb", True, "med", ""),
], key_printed=["حَجَبَ", "باخ", "تَختي", "حاج", "باحِث", "جابَت"])
L(3, "d6", "Drill 6", "Reading aloud — vowel length, ح and خ", ["ح", "خ"], [], "table", items=[
    (1, "تَحْتاج", "taHtaaj", "she needs; you (m.) need", "verb", True, "high", ""),
    (2, "جابي", "jaabii", "collector (of taxes or fees)", "noun", True, "low", ""),
    (3, "حَجّ", "Hajj", "the Hajj (pilgrimage to Mecca)", "noun", True, "high", "Printed حَج; shadda added."),
    (4, "حِجاب", "Hijaab", "headscarf, veil", "noun", True, "high", ""),
    (5, "جُبَب", "jubab", "robes, cloaks (plural of جُبّة jubba)", "noun", True, "med", ""),
    (6, "حاجّ", "Haajj", "pilgrim (someone who has made the Hajj)", "noun", True, "high", "Printed حاج; shadda added."),
    (7, "جابَت", "jaabat", "she roamed, crossed (formal); in spoken Arabic 'she brought'", "verb", True, "med", ""),
    (8, "خاب", "khaab", "he failed; he was disappointed", "verb", True, "med", ""),
    (9, "حُبّ", "Hubb", "love", "noun", True, "high", "Printed حُب; shadda added."),
    (10, "باحِث", "baaHith", "researcher", "noun", True, "high", ""),
    (11, "تُجاب", "tujaab", "she/it is answered; you (m.) are answered (passive)", "verb", True, "low", ""),
    (12, "بُحْ", "buH", "reveal it! (said to a male)", "verb", True, "low", "Printed بُح."),
    (13, "جيبوتي", "jiibuutii", "Djibouti", "place", True, "high", ""),
    (14, "تُخوت", "tukhuut", "beds (plural of تَخْت)", "noun", True, "med", ""),
    (15, "خوجا", "khuujaa", "khawaja / hodja — an old title for a teacher or a (foreign) gentleman", "noun", True, "low", ""),
])
L(3, "le4", "Listening Exercise 4", "Reading sukuun", [], ["sukuun"], "lingco",
  lesson_file="unit-03/12_listening_exercise_4.txt", items=[
    (1, "تَحْتَجْ", "taHtaj", "(you/she) need — short form, as in لَمْ تَحْتَجْ 'you did not need'", "verb", True, "low", ""),
    (2, "تَخْتي", "takhtii", "my bed", "noun", True, "high", ""),
    (3, "تَحْجُبُ", "taHjubu", "she hides, veils; you (m.) hide", "verb", True, "high", ""),
    (4, "تُثْبِتي", "tuthbitii", "(that) you (f.) prove / confirm", "verb", True, "med", ""),
    (5, "بَحْثي", "baHthii", "my research", "noun", True, "high", ""),
])
L(3, "le5", "Listening Exercise 5", "Consonant و (w)", ["و"], [], "lingco",
  lesson_file="unit-03/14_listening_exercise_5.txt", items=[
    (1, "وَثَب", "wathab", "he jumped, leaped", "verb", True, "high", "Pausal reading of وَثَبَ."),
    (2, "واجِب", "waajib", "homework; duty", "noun", True, "high", ""),
    (3, "جَواب", "jawaab", "answer, reply", "noun", True, "high", ""),
    (4, "حِوار", "Hiwaar", "dialogue, conversation", "noun", True, "high", ""),
    (5, "خاوي", "khaawii", "empty (spoken form of formal خاوٍ)", "adjective", True, "med", ""),
])
L(3, "le6", "Listening Exercise 6", "Diphthong aw (ـَوْ)", ["و"], ["diphthong aw"], "lingco",
  lesson_file="unit-03/15_listening_exercise_6.txt", items=[
    (1, "ثَوْب", "thawb", "garment, robe", "noun", True, "high", ""),
    (2, "زَوْج", "zawj", "husband; pair", "noun", True, "high", ""),
    (3, "تَوْبيخ", "tawbiikh", "scolding, reprimand", "noun", True, "high", ""),
    (4, "خَوْخ", "khawkh", "peaches (collective — one peach is خَوْخة)", "noun", True, "high", ""),
    (5, "حَوْل", "Hawl", "around; about", "preposition", True, "high", ""),
])
L(3, "d7", "Drill 7", "Dictation (aw) — video", ["و"], [], "key", items=[
    (1, "خَوْخ", "khawkh", "peaches (collective — one peach is خَوْخة)", "noun", True, "high", ""),
    (2, "تَبْويب", "tabwiib", "arranging into chapters/sections; tabulation", "noun", True, "med", ""),
    (3, "جَواب", "jawaab", "answer, reply", "noun", True, "high", ""),
    (4, "ثَواب", "thawaab", "reward (especially God's reward for good deeds)", "noun", True, "high", ""),
], key_printed=["خَوْخ", "تَبْويب", "جَواب", "ثَواب"])
L(3, "le7", "Listening Exercise 7", "Consonant ي (y)", ["ي"], [], "lingco",
  lesson_file="unit-03/17_listening_exercise_7.txt", items=[
    (1, "بُيوت", "buyuut", "houses (plural of بَيْت)", "noun", True, "high", ""),
    (2, "ثِياب", "thiyaab", "clothes (plural of ثَوْب)", "noun", True, "high", ""),
    (3, "جُيوب", "juyuub", "pockets (plural of جَيْب)", "noun", True, "high", ""),
    (4, "يَجِب", "yajib", "it is necessary; (one) must", "verb", True, "high", ""),
    (5, "يَثوب", "yathuub", "he returns, comes back (to his senses)", "verb", True, "med", ""),
])
L(3, "le8", "Listening Exercise 8", "Diphthong ay (ـَيْ)", ["ي"], ["diphthong ay"], "lingco",
  lesson_file="unit-03/18_listening_exercise_8.txt", items=[
    (1, "حَيْث", "Hayth", "where (as in 'the place where'); since, because", "adverb", True, "med", ""),
    (2, "خَيْر", "khayr", "good; goodness, well-being", "noun", True, "high", ""),
    (3, "جَيْب", "jayb", "pocket", "noun", True, "high", ""),
    (4, "بَيْت", "bayt", "house", "noun", True, "high", ""),
    (5, "بَيْن", "bayn", "between", "preposition", True, "high", ""),
])
L(3, "d8", "Drill 8", "Dictation with vowels and sukuun — video", [], ["sukuun"], "key", items=[
    (1, "ثِياب", "thiyaab", "clothes (plural of ثَوْب)", "noun", True, "high", ""),
    (2, "حَياتي", "Hayaatii", "my life", "noun", True, "high", ""),
    (3, "جُيوبي", "juyuubii", "my pockets", "noun", True, "high", ""),
    (4, "يَحْجُب", "yaHjub", "he hides, veils, blocks", "verb", True, "high", ""),
], key_printed=["ثِياب", "حَياتي", "جُيوبي", "يَحْجُب"])
L(3, "d9", "Drill 9", "Reading aloud — check your pronunciation", [], [], "table", items=[
    (1, "يَخْت", "yakht", "yacht", "noun", True, "high", ""),
    (2, "ثِيابي", "thiyaabii", "my clothes", "noun", True, "high", ""),
    (3, "واجِبات", "waajibaat", "homework assignments; duties (plural of واجِب)", "noun", True, "high", ""),
    (4, "حَبيبي", "Habiibii", "my darling, my dear (to a male)", "noun", True, "high", ""),
    (5, "حَبيبَتي", "Habiibatii", "my darling, my dear (to a female)", "noun", True, "high", ""),
    (6, "حَيْث", "Hayth", "where (as in 'the place where'); since, because", "adverb", True, "med", ""),
    (7, "ثَواب", "thawaab", "reward (especially God's reward for good deeds)", "noun", True, "high", ""),
    (8, "جَيْبي", "jaybii", "my pocket", "noun", True, "high", ""),
    (9, "جُيوب", "juyuub", "pockets (plural of جَيْب)", "noun", True, "high", ""),
    (10, "تَبوحي", "tabuuHii", "(that) you (f.) reveal (a secret)", "verb", True, "med", ""),
    (11, "بَحْث", "baHth", "research; search", "noun", True, "high", ""),
    (12, "بَيْتي", "baytii", "my house", "noun", True, "high", ""),
    (13, "بُيوت", "buyuut", "houses (plural of بَيْت)", "noun", True, "high", ""),
    (14, "وُجوب", "wujuub", "necessity, obligation", "noun", True, "high", ""),
    (15, "تُجيبي", "tujiibii", "(that) you (f.) answer", "verb", True, "med", ""),
    (16, "خابَ", "khaaba", "he failed; he was disappointed", "verb", True, "high", ""),
    (17, "يَجِب", "yajib", "it is necessary; (one) must", "verb", True, "high", ""),
    (18, "جُثَث", "juthath", "corpses, dead bodies (plural of جُثّة)", "noun", True, "high", ""),
    (19, "جَواب", "jawaab", "answer, reply", "noun", True, "high", ""),
    (20, "جَوابات", "jawaabaat", "answers; (in spoken Arabic) letters (plural of جَواب)", "noun", True, "med", ""),
])
L(3, "d10", "Drill 10", "Letter connection — listen and write in the short vowels", [], ["short vowels"], "key", items=[
    (1, "جابَت", "jaabat", "she roamed, crossed (formal); in spoken Arabic 'she brought'", "verb", True, "med", ""),
    (2, "حُجُب", "Hujub", "veils, screens, curtains (plural of حِجاب)", "noun", True, "med", ""),
    (3, "خَوْخ", "khawkh", "peaches (collective — one peach is خَوْخة)", "noun", True, "high", ""),
    (4, "ثِيابي", "thiyaabii", "my clothes", "noun", True, "high", ""),
    (5, "جيبوتي", "jiibuutii", "Djibouti", "place", True, "high", ""),
    (6, "حَبيبَتي", "Habiibatii", "my darling, my dear (to a female)", "noun", True, "high", ""),
    (7, "بُحوث", "buHuuth", "research studies, papers (plural of بَحْث)", "noun", True, "high", ""),
    (8, "واجِبات", "waajibaat", "homework assignments; duties (plural of واجِب)", "noun", True, "high", ""),
    (9, "بُيوت", "buyuut", "houses (plural of بَيْت)", "noun", True, "high", ""),
    (10, "جُيوب", "juyuub", "pockets (plural of جَيْب)", "noun", True, "high", ""),
], key_printed=["جابَت", "حُجُب", "خَوْخ", "ثِيابي", "جيبوتي", "حَبيبَتي", "بُحوث", "واجِبات", "بُيوت", "جُيوب"])
L(3, "d11", "Drill 11", "Dictation — video", [], [], "key", items=[
    (1, "واجِب", "waajib", "homework; duty", "noun", True, "high", ""),
    (2, "بَيْتي", "baytii", "my house", "noun", True, "high", ""),
    (3, "يَبوح", "yabuuH", "he reveals (a secret)", "verb", True, "med", ""),
    (4, "يَخيب", "yakhiib", "he fails; he is disappointed", "verb", True, "med", ""),
    (5, "يَحْجُب", "yaHjub", "he hides, veils, blocks", "verb", True, "high", ""),
    (6, "تَحْتاج", "taHtaaj", "she needs; you (m.) need", "verb", True, "high", ""),
], key_printed=["واجِب", "بَيْتي", "يَبوح", "يَخيب", "يَحْجُب", "تَحْتاج"])

# ---------------- UNIT 4 ----------------
L(4, "le1", "Listening Exercise 1", "Listening to and pronouncing hamza ء", ["ء"], [], "lingco",
  lesson_file="unit-04/00_listening_exercise_1.txt", items=[
    (1, "أَخَوات", "akhawaat", "sisters (plural of أُخْت)", "noun", True, "high", ""),
    (2, "أَب", "ab", "father", "noun", True, "high", ""),
    (3, "سَبَأ", "saba'", "Sheba (the ancient kingdom of Saba' in Yemen)", "place", True, "high", ""),
    (4, "تَأْتَأ", "ta'ta'", "he stammered, stuttered", "verb", True, "med", ""),
    (5, "بَأْس", "ba's", "harm (as in لا بَأْس 'no problem'); also might, courage", "noun", True, "high", ""),
])
L(4, "le2", "Listening Exercise 2", "Initial hamza with fatHa (أَ)", ["ء"], ["fatHa"], "lingco",
  lesson_file="unit-04/02_listening_exercise_2.txt", items=[
    (1, "أَب", "ab", "father", "noun", True, "high", ""),
    (2, "أَتَت", "atat", "she came", "verb", True, "high", ""),
    (3, "أَخ", "akh", "brother", "noun", True, "high", ""),
    (4, "أَخَوات", "akhawaat", "sisters (plural of أُخْت)", "noun", True, "high", ""),
    (5, "أَثاث", "athaath", "furniture", "noun", True, "high", ""),
])
L(4, "le3", "Listening Exercise 3", "Initial hamza with Damma (أُ) and kasra (إِ)", ["ء"], ["Damma", "kasra"], "lingco",
  lesson_file="unit-04/03_listening_exercise_3.txt", items=[
    (1, "إِبْحار", "ibHaar", "sailing, setting sail", "noun", True, "high", ""),
    (2, "أُخْت", "ukht", "sister", "noun", True, "high", ""),
    (3, "إِثْبات", "ithbaat", "proof, confirmation", "noun", True, "high", ""),
    (4, "أُخْرِجَ", "ukhrija", "he was taken out, expelled (passive)", "verb", True, "med", ""),
    (5, "إِخْبار", "ikhbaar", "informing; reporting news", "noun", True, "high", ""),
    (6, "أُثْبِتَ", "uthbita", "it was proven, confirmed (passive)", "verb", True, "med", ""),
])
L(4, "le4", "Listening Exercise 4", "Final hamza — names of letters", ["ء"], [], "lingco",
  lesson_file="unit-04/05_listening_exercise_4.txt", items=[
    (1, "باء", "baa'", "the letter name baa (ب)", "letter-name", True, "high", ""),
    (2, "تاء", "taa'", "the letter name taa (ت)", "letter-name", True, "high", ""),
    (3, "ثاء", "thaa'", "the letter name thaa (ث)", "letter-name", True, "high", ""),
    (4, "حاء", "Haa'", "the letter name Haa (ح)", "letter-name", True, "high", ""),
    (5, "خاء", "khaa'", "the letter name khaa (خ)", "letter-name", True, "high", ""),
])
L(4, "d2", "Drill 2", "Dictation (hamza) — video", ["ء"], [], "key", items=[
    (1, "ثاء", "thaa'", "the letter name thaa (ث)", "letter-name", True, "high", ""),
    (2, "أَب", "ab", "father", "noun", True, "high", ""),
    (3, "أَثاث", "athaath", "furniture", "noun", True, "high", ""),
    (4, "أَخي", "akhii", "my brother", "noun", True, "high", ""),
    (5, "باء", "baa'", "the letter name baa (ب)", "letter-name", True, "high", ""),
    (6, "أَتَت", "atat", "she came", "verb", True, "high", ""),
], key_printed=["ثاء", "أَب", "أَثاث", "أَخي", "باء", "أَتَت"])
L(4, "le5", "Listening Exercise 5", "Recognizing and pronouncing د", ["د"], [], "lingco",
  lesson_file="unit-04/12_listening_exercise_5.txt", items=[
    (1, "دَجاج", "dajaaj", "chicken (collective — one hen is دَجاجة)", "noun", True, "high", ""),
    (2, "خُدود", "khuduud", "cheeks (plural of خَدّ)", "noun", True, "high", ""),
    (3, "حُدود", "Huduud", "borders, limits (plural of حَدّ)", "noun", True, "high", ""),
    (4, "جَديد", "jadiid", "new", "adjective", True, "high", ""),
    (5, "أَدَب", "adab", "literature; good manners", "noun", True, "high", ""),
    (6, "أَحْداث", "aHdaath", "events (plural of حَدَث)", "noun", True, "high", ""),
])
L(4, "le6", "Listening Exercise 6", "Reading and pronouncing ذ", ["ذ"], [], "lingco",
  lesson_file="unit-04/14_listening_exercise_6.txt", items=[
    (1, "ذُباب", "dhubaab", "flies (the insects; collective — one fly is ذُبابة)", "noun", True, "high", ""),
    (2, "ذات", "dhaat", "self; essence", "noun", True, "med", ""),
    (3, "بَذَرَ", "badhara", "he sowed (seeds)", "verb", True, "high", ""),
    (4, "خُذ", "khudh", "take! (said to a male)", "verb", True, "high", ""),
    (5, "حَذارِ", "Hadhaari", "beware! watch out!", "particle", True, "high", ""),
    (6, "تَذَبْذُب", "tadhabdhub", "fluctuation, wavering", "noun", True, "high", ""),
])
L(4, "d6", "Drill 6", "Pronouncing ذ vs ث — read aloud, then check with the audio", ["ذ", "ث"], [], "lingco",
  lesson_file="unit-04/15_drill_6.txt", items=[
    (1, "ذابَ", "dhaaba", "it melted, dissolved", "verb", True, "high", ""),
    (2, "ثابَ", "thaaba", "he returned, came back (to his senses)", "verb", True, "med", ""),
    (3, "ذُباب", "dhubaab", "flies (the insects; collective — one fly is ذُبابة)", "noun", True, "high", ""),
    (4, "ثَبات", "thabaat", "firmness, stability", "noun", True, "high", ""),
    (5, "ثَواب", "thawaab", "reward (especially God's reward for good deeds)", "noun", True, "high", ""),
    (6, "ذَوات", "dhawaat", "selves, beings (plural of ذات)", "noun", True, "med", ""),
    (7, "جُثَث", "juthath", "corpses, dead bodies (plural of جُثّة)", "noun", True, "high", ""),
    (8, "جاذِب", "jaadhib", "attractive; attracting", "adjective", True, "high", ""),
])
L(4, "le7", "Listening Exercise 7", "Pronouncing ر (ر deepens alif and fatHa)", ["ر"], [], "lingco",
  lesson_file="unit-04/19_listening_exercise_7.txt", items=[
    (1, "رَباب", "rabaab", "rebab (a bowed string instrument); also a woman's name", "noun", True, "med", ""),
    (2, "رُدود", "ruduud", "replies, responses (plural of رَدّ)", "noun", True, "high", ""),
    (3, "خَراج", "kharaaj", "land tax, tribute (historical)", "noun", True, "med", "Not خُراج (khuraaj) 'abscess'."),
    (4, "تَبْرير", "tabriir", "justification", "noun", True, "high", ""),
    (5, "جار", "jaar", "neighbor (m.)", "noun", True, "high", ""),
    (6, "وُرود", "wuruud", "roses, flowers (plural of وَرْد); also 'arrival'", "noun", True, "med", ""),
])
L(4, "le8", "Listening Exercise 8", "Pronouncing ز", ["ز"], [], "lingco",
  lesson_file="unit-04/21_listening_exercise_8.txt", items=[
    (1, "زَوْج", "zawj", "husband; pair", "noun", True, "high", ""),
    (2, "أَحْزاب", "aHzaab", "(political) parties (plural of حِزْب)", "noun", True, "high", ""),
    (3, "زُجاج", "zujaaj", "glass (the material)", "noun", True, "high", ""),
    (4, "يَزور", "yazuur", "he visits", "verb", True, "high", ""),
    (5, "جَواز", "jawaaz", "passport (short for جَواز سَفَر); permission", "noun", True, "high", ""),
    (6, "تَزيد", "taziid", "she/it increases; you (m.) increase", "verb", True, "high", "Lingco prints it with a stray space (تَـز يـد)."),
])
L(4, "d9", "Drill 9", "Letter connection — listen and write in the short vowels", ["د", "ذ", "ر", "ز"], ["short vowels"], "key", items=[
    (1, "رَذاذ", "radhaadh", "drizzle; fine spray", "noun", True, "high", ""),
    (2, "خادِر", "khaadir", "drowsy, sluggish; (of a lion) in its den", "adjective", True, "low", ""),
    (3, "زَرَد", "zarad", "chain mail (armor)", "noun", True, "med", ""),
    (4, "حُروب", "Huruub", "wars (plural of حَرْب)", "noun", True, "high", ""),
    (5, "رَجاء", "rajaa'", "hope; request; 'please'", "noun", True, "high", ""),
    (6, "بِحار", "biHaar", "seas (plural of بَحْر)", "noun", True, "high", ""),
    (7, "أَزْواج", "azwaaj", "husbands; couples, pairs (plural of زَوْج)", "noun", True, "high", ""),
    (8, "حُدود", "Huduud", "borders, limits (plural of حَدّ)", "noun", True, "high", ""),
    (9, "رُدود", "ruduud", "replies, responses (plural of رَدّ)", "noun", True, "high", ""),
    (10, "تَحْذير", "taHdhiir", "warning", "noun", True, "high", ""),
    (11, "أَدْوار", "adwaar", "roles; turns; floors of a building (plural of دَوْر)", "noun", True, "high", ""),
    (12, "يَخْرُج", "yakhruj", "he goes out, leaves", "verb", True, "high", ""),
    (13, "تَجارِب", "tajaarib", "experiments; experiences (plural of تَجْرِبة)", "noun", True, "high", ""),
    (14, "ذَبَحَت", "dhabaHat", "she slaughtered", "verb", True, "high", ""),
], key_printed=["رَذاذ", "خادِر", "زَرَد", "حُروب", "رَجاء", "بِحار", "أَزْواج", "حُدود", "رُدود", "تَحْذير", "أَدْوار", "يَخْرُج", "تَجارِب", "ذَبَحَت"])
L(4, "d10", "Drill 10", "Dictation — video", [], [], "key", items=[
    (1, "أُخْت", "ukht", "sister", "noun", True, "high", ""),
    (2, "أَبي", "abii", "my father", "noun", True, "high", ""),
    (3, "واحِد", "waaHid", "one", "number", True, "high", ""),
    (4, "زَوْجات", "zawjaat", "wives (plural of زَوْجة)", "noun", True, "high", ""),
    (5, "ذُباب", "dhubaab", "flies (the insects; collective — one fly is ذُبابة)", "noun", True, "high", ""),
    (6, "دَجاج", "dajaaj", "chicken (collective — one hen is دَجاجة)", "noun", True, "high", ""),
    (7, "أَزْرار", "azraar", "buttons (plural of زِرّ)", "noun", True, "high", ""),
    (8, "رَباب", "rabaab", "rebab (a bowed string instrument); also a woman's name", "noun", True, "med", ""),
    (9, "يُريد", "yuriid", "he wants", "verb", True, "high", ""),
    (10, "أَحْزاب", "aHzaab", "(political) parties (plural of حِزْب)", "noun", True, "high", ""),
], key_printed=["أُخْت", "أَبي", "واحِد", "زَوْجات", "ذُباب", "دَجاج", "أَزْرار", "رَباب", "يُريد", "أَحْزاب"])

# ----------------------------------------------------------------------------------------------
# VOCABULARY (New Vocabulary tables). Row = publisher row number (AB3e_U{u}VSt-NN / VS-NN).
# F = formal/written form; S = shaami form. S['sep']=True -> the shaami form is a different word or has a
# documented (Lingco/book transliteration) different pronunciation -> its own record (register shaami).
# Otherwise the shaami clip is attached to the formal record as an alternate (dialect "shaami").
# Tuple: (unit, row, lesson, F dict|None, S dict|None, notes)
# ----------------------------------------------------------------------------------------------
def F(ar, tr, meaning, wt, conf="high", printed=None, trp=None):
    return dict(ar=ar, tr=tr, meaning=meaning, wt=wt, conf=conf, printed=printed, trp=trp)

def S(ar, tr, meaning=None, wt=None, sep=True, conf="high", printed=None, note=""):
    return dict(ar=ar, tr=tr, meaning=meaning, wt=wt, sep=sep, conf=conf, printed=printed, note=note)

VOCAB = [
    # ---- Unit 1 (New Vocabulary) ----
    (1, 1, "New Vocabulary", F("السَّلامُ عَلَيْكُم", "assalaamu calaykum", "Peace be upon you — the Islamic greeting ('hello')", "phrase"),
     S("السَّلامُ عَلَيْكُم", "assalaamu calaykum", sep=False), ""),
    (1, 2, "New Vocabulary", F("أَهْلاً", "ahlan", "Hello! / Hi!", "phrase"),
     S("أَهْلا", "ahla", "Hello! / Hi! (Levantine pronunciation)", "phrase"), "Lingco: 'used more in Egypt than the Levant'."),
    (1, 3, "New Vocabulary", F("أَهْلاً وَسَهْلاً", "ahlan wa sahlan", "Hello! / Welcome!", "phrase"),
     S("أَهْلا وْسَهْلا", "ahla w sahla", "Hello! / Welcome! (Levantine pronunciation)", "phrase"), ""),
    (1, 4, "New Vocabulary", F("مَرْحَباً", "marHaban", "Hello! (used especially in the Levant)", "phrase"),
     S("مَرْحَبا", "marHaba", "Hello! (Levantine)", "phrase"), ""),
    (1, 5, "New Vocabulary", F("أَنا", "ana", "I", "pronoun"), S("أَنا", "ana", sep=False), ""),
    (1, 6, "New Vocabulary", F("اِسْمي", "ismii", "my name", "noun"), S("اِسْمي", "ismi", sep=False),
     "Shaami clip says ismi (short final vowel)."),
    (1, 7, "New Vocabulary", F("مِن", "min", "from", "preposition"), S("مِن", "min", sep=False), ""),
    (1, 8, "New Vocabulary", F("مَدينة", "madiinat", "the city of … (used right before a city's name)", "noun"),
     S("مَدينة", "madiinit", "the city of … (Levantine pronunciation)", "noun"), ""),
    (1, 9, "New Vocabulary", F("في", "fii", "in", "preposition"),
     S("بِـ", "bi-", "in (Levantine; attached to the next word)", "preposition"), ""),
    # ---- Unit 2 (New Vocabulary) ----
    (2, 1, "New Vocabulary", F("باب", "baab", "door", "noun"), S("باب", "baab", sep=False), ""),
    (2, 2, "New Vocabulary", F("اِسْم", "ism", "name", "noun"), S("اِسْم", "ism", sep=False), ""),
    (2, 3, "New Vocabulary", F("ما؟", "maa?", "what?", "interrogative"), S("شو؟", "shuu?", "what? (Levantine)", "interrogative"), ""),
    (2, 4, "New Vocabulary", F("أَهْلاً بِكَ", "ahlan bika", "Hello to you too — reply to 'ahlan wa sahlan' (to a male)", "phrase"),
     S("أَهْلاً فيك", "ahlan fiik", "Hello to you too — reply to 'ahla w sahla' (to a male; Levantine)", "phrase"), ""),
    (2, 5, "New Vocabulary", F("أَهْلاً بِكِ", "ahlan biki", "Hello to you too — reply to 'ahlan wa sahlan' (to a female)", "phrase"),
     S("أَهْلاً فيكِ", "ahlan fiiki", "Hello to you too — reply to 'ahla w sahla' (to a female; Levantine)", "phrase"), ""),
    (2, 6, "New Vocabulary", F("وَعَلَيْكُمُ السَّلام", "wa calaykumu s-salaam", "And upon you be peace — reply to 'assalaamu calaykum'", "phrase"),
     S("وَعَلَيْكُمُ السَّلام", "wa calaykumu s-salaam", sep=False), ""),
    (2, 7, "New Vocabulary", F("حَضْرَتُكَ", "HaDratuka", "you (polite, to a male) — literally 'your presence'", "pronoun"),
     S("حَضِرْتَك", "HaDәrtak", "you (polite, to a male; Levantine)", "pronoun"), ""),
    (2, 8, "New Vocabulary", F("حَضْرَتُكِ", "HaDratuki", "you (polite, to a female) — literally 'your presence'", "pronoun"),
     S("حَضِرْتِك", "HaDәrtik", "you (polite, to a female; Levantine)", "pronoun"), ""),
    (2, 9, "New Vocabulary", F("تَشَرَّفْنا", "tasharrafnaa", "Nice to meet you! (literally 'we have been honored')", "phrase"),
     S("تْشَرَّفْنا", "tsharrafna", "Nice to meet you! (Levantine)", "phrase"), ""),
    (2, 10, "New Vocabulary", F("أَنْتَ", "anta", "you (to a male)", "pronoun"),
     S("إِنْتَ", "inte", "you (to a male; Levantine)", "pronoun", printed="إنتِ",
       note="Lingco prints إنتِ (with kasra) — apparently a typo; the book prints إنتَ, pronounced inte."), ""),
    (2, 11, "New Vocabulary", F("أَنْتِ", "anti", "you (to a female)", "pronoun"),
     S("إِنْتِ", "inti", "you (to a female; Levantine)", "pronoun"), ""),
    (2, 13, "New Vocabulary", F("ـكَ / اِسْمُكَ", "-ka / ismuka", "your (to a male; suffix) / your name", "suffix"),
     S("ـَك / اِسْمَك", "-ak / ismak", "your (to a male; suffix) / your name (Levantine)", "suffix"),
     "Book row 12 (ـي / اِسْمي 'my') has no Lingco audio."),
    (2, 14, "New Vocabulary", F("ـكِ / اِسْمُكِ", "-ki / ismuki", "your (to a female; suffix) / your name", "suffix"),
     S("ـِك / اِسْمِك", "-ik / ismik", "your (to a female; suffix) / your name (Levantine)", "suffix"), ""),
    (2, 15, "New Vocabulary", F("أَيْنَ؟", "ayna?", "where?", "interrogative"), S("وين؟", "ween?", "where? (Levantine)", "interrogative"), ""),
    (2, 16, "New Vocabulary", F("مِن أَيْنَ؟", "min ayna?", "from where?", "interrogative"),
     S("مِن وين؟", "min ween?", "from where? (Levantine)", "interrogative"), ""),
    (2, 17, "New Vocabulary", F("نَعَم", "nacam", "yes", "particle"), S("إيه", "ee", "yes (Levantine)", "particle"), ""),
    (2, 18, "New Vocabulary", F("لا", "laa", "no", "particle"), S("لا", "la / laa", sep=False), ""),
    # ---- Unit 3 (New Vocabulary) ----
    (3, 1, "New Vocabulary", F("وَ", "wa", "and", "particle"), S("و", "w- / u- (unverified)", sep=False,
       note="Shaami clip pronunciation not transcribed in Lingco/book."), ""),
    (3, 2, "New Vocabulary", F("حِجاب", "Hijaab", "headscarf, veil (head covering)", "noun"), S("حِجاب", "Hijaab", sep=False), ""),
    (3, 3, "New Vocabulary", F("بَيْت", "bayt", "house", "noun"), S("بيت", "beet? (unverified)", sep=False,
       note="Levantine usually says 'beet'; Lingco/book give no transliteration."), ""),
    (3, 4, "New Vocabulary", F("شارِع", "shaaric", "street", "noun"), S("شارِع", "shaaric", sep=False), ""),
    (3, 5, "New Vocabulary", F("واجِب", "waajib", "homework (also: duty)", "noun"),
     S("وَظيفة", "waZiife", "homework (Levantine)", "noun"), "Levantine pronounces ظ as an emphatic z — the book writes waZiife."),
    (3, 6, "New Vocabulary", F("أَخْبار", "akhbaar", "news (plural of خَبَر, a piece of news)", "noun"), S("أَخْبار", "akhbaar", sep=False), ""),
    (3, 7, "New Vocabulary", F("كِتاب", "kitaab", "book", "noun"), S("كِتاب", "kitaab / ktaab", sep=False,
       note="Lingco gives shaami kitaab; the book prints ktaab."), ""),
    (3, 8, "New Vocabulary", F("حَبيبي", "Habiibii", "my darling, my dear (to a male; also used with children, parents, close friends)", "noun"),
     S("حَبيبي", "Habiibi", sep=False), ""),
    (3, 9, "New Vocabulary", F("حَبيبَتي", "Habiibatii", "my darling, my dear (to a female)", "noun"),
     S("حَبيبْتي", "Habiibti? (unverified)", sep=False, note="Shaami spelling drops the fatHa (book: حَبيبتي), i.e. probably 'Habiibti'."), ""),
    (3, 10, "New Vocabulary", F("صَباح الخَيْر", "SabaaH al-khayr", "Good morning!", "phrase"),
     S("صَباح الخير", "SabaaH il-kheer", "Good morning! (Levantine)", "phrase"), ""),
    (3, 11, "New Vocabulary", F("صَباح النّور", "SabaaH an-nuur", "Good morning! (reply) — literally 'morning of light'", "phrase"),
     S("صَباح النّور", "SabaaH in-nuur", "Good morning! (reply; Levantine)", "phrase", note="Lingco truncates the translit to 'SabaaH'; the book gives SabaaH in-nuur."), ""),
    (3, 12, "New Vocabulary", F("يا …", "yaa …", "O …! — put before a name when calling or addressing someone directly (yaa Ahmad)", "particle"),
     S("يا …", "yaa …", sep=False), ""),
    (3, 13, "New Vocabulary", F("كَيْفَ؟", "kayfa?", "how?", "interrogative"), S("كيف؟", "kiif?", "how? (Levantine)", "interrogative"), ""),
    (3, 14, "New Vocabulary", F("كَيْفَ الحال؟", "kayfa al-Haal?", "How are you? (literally 'how is the condition?')", "phrase", trp="kayf al-Haal?"),
     S("كيفَك؟ / كيفِك؟", "kiifak? / kiifik?", "How are you? (to a male / to a female; Levantine)", "phrase",
       note="Lingco prints one cell كيفك؟ with translit 'kiifak/–ik' (masc./fem.); written out here as both forms. The clip may say one or both."), ""),
    (3, 15, "New Vocabulary", F("الحَمْدُ لِلّه", "al-Hamdu lillaah", "Praise be to God — the reply to 'How are you?' (fine, thank God)", "phrase"),
     S("الحَمْدُ لِلّه", "il-Hamdilla", "Thank God (reply to 'How are you?'; Levantine pronunciation)", "phrase", printed="الْحَمد لِلّها",
       note="Lingco prints الْحَمد لِلّها; the book prints الحَمدُ لِلّه for all three varieties (shaami pronounced il-Hamdilla)."), ""),
    (3, 16, "New Vocabulary", F("جَيِّد", "jayyid", "good, fine", "adjective"), S("تَمام", "tamaam", "great, fine (Levantine)", "adjective"),
     "The book also lists the feminine جَيِّدة jayyida (not in the Lingco clip)."),
    (3, 17, "New Vocabulary", None, S("ماشي", "maashi", "OK (Levantine)", "particle"), "No formal equivalent in the table."),
    (3, 18, "New Vocabulary", F("هٰذا", "haadhaa", "this (masc.)", "demonstrative"),
     S("هَيدا", "hayda (or haada)", "this (masc.; Levantine)", "demonstrative", conf="med",
       note="Lingco pairs the spelling هَيدا with translit 'haada'; the book lists both haada (هادا) and hayda (هَيدا). Which one the clip says is unverified."), ""),
    (3, 19, "New Vocabulary", F("هٰذِهِ", "haadhihi", "this (fem.)", "demonstrative"),
     S("هَيدي", "haydi (or haadi)", "this (fem.; Levantine)", "demonstrative", conf="med",
       note="Lingco pairs هَيدي with 'haadi'; the book lists haadi (هادي) and haydi (هَيدي). Unverified which the clip says."), ""),
    (3, 20, "New Vocabulary", F("بِخَيْر", "bi-khayr", "fine, well (reply to 'kayfa al-Haal?')", "phrase"),
     S("مْنيح / مْنيحة", "mniiH / mniiHa", "good, fine (masc. / fem.; Levantine)", "adjective"), ""),
    (3, 21, "New Vocabulary", F("لَيْسَ", "laysa", "is not / am not / are not (negating verb)", "verb", printed="ليَسَ"),
     S("مو", "muu", "not (Levantine)", "particle"), "Lingco prints ليَسَ (misplaced fatHa); correct لَيْسَ."),
    # ---- Unit 4 (New Vocabulary 1) ----
    (4, 9, "New Vocabulary 1", F("تَفَضَّل", "tafaDDal", "Please come in / go ahead / here you are (to a male)", "phrase"),
     S("تْفَضَّل", "tfaDDal", "Please come in / go ahead (to a male; Levantine)", "phrase"), ""),
    (4, 10, "New Vocabulary 1", F("تَفَضَّلي", "tafaDDalii", "Please come in / go ahead / here you are (to a female)", "phrase"),
     S("تْفَضّْلي", "tfaDDli", "Please come in / go ahead (to a female; Levantine)", "phrase"), ""),
    (4, 11, "New Vocabulary 1", F("تَفَضَّلوا", "tafaDDaluu", "Please come in / go ahead / here you are (to a group)", "phrase"),
     S("تْفَضّْلوا", "tfaDDlu", "Please come in / go ahead (to a group; Levantine)", "phrase"), ""),
    (4, 14, "New Vocabulary 1", F("صاحِبي", "SaaHibii", "my friend (m.); my boyfriend", "noun"),
     S("صاحْبي / رْفيقي", "SaaHbi / rfii'i", "my friend (m.) — two Levantine words", "noun"), "Levantine pronounces ق as a hamza (rfii'i)."),
    (4, 15, "New Vocabulary 1", F("صاحِبَتي", "SaaHibatii", "my friend (f.); my girlfriend", "noun"),
     S("صاحِبْتي / رْفيقْتي", "SaaHibti / rfii'ti", "my friend (f.) — two Levantine words", "noun"), ""),
    (4, 16, "New Vocabulary 1", F("هُوَ", "huwa", "he; it (masc.)", "pronoun"), S("هُوِّ", "huwwe", "he; it (masc.; Levantine)", "pronoun", printed="هو"), ""),
    (4, 17, "New Vocabulary 1", F("هِيَ", "hiya", "she; it (fem.)", "pronoun"), S("هِيِّ", "hiyye", "she; it (fem.; Levantine)", "pronoun", printed="هي"), ""),
    (4, 18, "New Vocabulary 1", F("ـهُ / اِسْمُهُ", "-hu / ismuhu", "his (suffix) / his name", "suffix"),
     S("ـه / اِسْمه", "-o / ismo", "his (suffix) / his name (Levantine)", "suffix", printed="ـه / اسمه",
       note="Written اسمه, pronounced ismo in Levantine."), ""),
    (4, 19, "New Vocabulary 1", F("ـها / اِسْمُها", "-haa / ismuhaa", "her (suffix) / her name", "suffix", trp="-ha / ismuha"),
     S("ـها / اِسْمها", "-a / isma", "her (suffix) / her name (Levantine)", "suffix"), ""),
    (4, 23, "New Vocabulary 1", F("طالِب", "Taalib", "student (male)", "noun"), S("طالِب", "Taalib", sep=False), ""),
    (4, 24, "New Vocabulary 1", F("طالِبة", "Taaliba", "student (female)", "noun"),
     S("طالْبِة", "Taalbe", "student (female; Levantine)", "noun", printed="طالبة"), "Lingco's meaning 'your student (female)' is a typo; book: 'student (female)'."),
    (4, 25, "New Vocabulary 1", F("أُسْتاذ", "ustaadh", "professor, teacher (male)", "noun"),
     S("إِسْتاذ", "istaaz", "professor, teacher (male; Levantine)", "noun"), ""),
    (4, 26, "New Vocabulary 1", F("أُسْتاذة", "ustaadha", "professor, teacher (female)", "noun"),
     S("إِسْتاذِة", "istaaze", "professor, teacher (female; Levantine)", "noun", printed="إِستاذة"), ""),
    (4, 27, "New Vocabulary 1", F("جامِعة", "jaamicat", "the university of … (used right before a name)", "noun"),
     S("جامْعِة", "jaamcit", "the university of … (Levantine)", "noun", printed="جامعة"), ""),
    # ---- Unit 4 (New Vocabulary 2) ----
    (4, 1, "New Vocabulary 2", F("خُبْز", "khubz", "bread", "noun"), S("خُبْز", "khubz", sep=False), ""),
    (4, 2, "New Vocabulary 2", F("دَجاج", "dajaaj", "chicken", "noun"), S("دجاج", "dajaaj / djaaj? (unverified)", sep=False,
       note="Levantine often says 'djaaj'; Lingco/book give no transliteration."), ""),
    (4, 3, "New Vocabulary 2", F("جار", "jaar", "neighbor (male)", "noun"), S("جار", "jaar", sep=False), ""),
    (4, 4, "New Vocabulary 2", F("جارة", "jaara", "neighbor (female)", "noun"), S("جارة", "jaara", sep=False), ""),
    (4, 5, "New Vocabulary 2", F("أَخ", "akh", "brother", "noun"), S("أَخ", "akh", sep=False), ""),
    (4, 6, "New Vocabulary 2", F("أُخْت", "ukht", "sister", "noun"), S("أُخْت", "ukht", sep=False), ""),
    (4, 7, "New Vocabulary 2", F("جَديد", "jadiid", "new (masc.)", "adjective"), S("جديد", "jdiid? (unverified)", sep=False,
       note="The feminine row gives shaami jdiide, so this clip probably says jdiid."), ""),
    (4, 8, "New Vocabulary 2", F("جَديدة", "jadiida", "new (fem.)", "adjective"),
     S("جْديدِة", "jdiide", "new (fem.; Levantine)", "adjective", printed="جديدة"), ""),
    (4, 12, "New Vocabulary 2", F("مَساء الخَيْر", "masaa' al-khayr", "Good evening!", "phrase"),
     S("مَسا الخير", "masa l-kheer", "Good evening! (Levantine)", "phrase"), ""),
    (4, 13, "New Vocabulary 2", F("مَساء النّور", "masaa' an-nuur", "Good evening! (reply) — literally 'evening of light'", "phrase"),
     S("مَسا النّور", "masa n-nuur", "Good evening! (reply; Levantine)", "phrase"), ""),
    (4, 20, "New Vocabulary 2", F("عِنْدي", "cindii", "I have (literally 'with me')", "phrase", trp="cindi"),
     S("عِنْدي", "candi", "I have (Levantine)", "phrase", printed="عندي"), ""),
    (4, 21, "New Vocabulary 2", F("لَيْسَ عِنْدي", "laysa cindii", "I don't have", "phrase", trp="laysa cindi"),
     S("ما عِنْدي", "maa candi", "I don't have (Levantine)", "phrase", printed="ما عندي"), ""),
    (4, 22, "New Vocabulary 2", F("سُؤال", "su'aal", "question", "noun"), S("سُؤال", "su'aal", sep=False), ""),
    (4, 28, "New Vocabulary 2", F("أُحِبّ", "uHibb", "I love; I like", "verb"),
     S("بْحِبّ", "bHibb", "I love; I like (Levantine)", "verb", conf="med", printed="بحِبّ",
       note="Lingco/book give no transliteration; standard Damascene form assumed."), ""),
    (4, 29, "New Vocabulary 2", F("تُحِبّ", "tuHibb", "you (m.) love / like", "verb"),
     S("بِتْحِبّ", "bitHibb", "you (m.) love / like (Levantine)", "verb", conf="med", printed="بِتحِبّ",
       note="Lingco/book give no transliteration; standard Damascene form assumed."), ""),
    (4, 30, "New Vocabulary 2", F("تُحِبّين", "tuHibbiin", "you (f.) love / like", "verb"),
     S("بِتْحِبّي", "bitHibbi", "you (f.) love / like (Levantine)", "verb", conf="med", printed="بِتحِبّي",
       note="Lingco/book give no transliteration; standard Damascene form assumed."), ""),
    (4, 42, "New Vocabulary 2", F("رَقْم تِليفون", "raqm tilifuun", "telephone number", "phrase"),
     S("نِمْرِة تِليفون", "nimrit tilifuun", "telephone number (Levantine)", "phrase", printed="نِمرة تليفون"), ""),
]

# ----------------------------------------------------------------------------------------------
# NUMERALS 0-10 (Unit 4, Arabic Numerals). AB3e_NumSt-NN formal, NumS-NN shaami, NumE excluded.
# ----------------------------------------------------------------------------------------------
NUMERALS = [
    # n, formal (ar, tr), shaami (ar, tr, sep)
    (0, ("صِفْر", "Sifr"), ("صِفِر", "Sifәr", False)),
    (1, ("واحِد", "waaHid"), ("واحِد", "waaHid", False)),
    (2, ("اِثْنَيْن", "ithnayn"), ("اتنين", "tneen", True)),
    (3, ("ثَلاثة", "thalaatha"), ("تلاتة", "tlaate", True)),
    (4, ("أَرْبَعة", "arbaca"), ("اربعة", "arbaca", False)),
    (5, ("خَمْسة", "khamsa"), ("خمسة", "khamse", True)),
    (6, ("سِتّة", "sitta"), ("سِتّة", "sitte", True)),
    (7, ("سَبْعة", "sabca"), ("سَبعة", "sabca", False)),
    (8, ("ثَمانِية", "thamaaniya"), ("تمانية", "tmaane", True)),
    (9, ("تِسْعة", "tisca"), ("تِسعة", "tisca", False)),
    (10, ("عَشَرة", "cashara"), ("عَشَرة", "cashra", True)),
]
NUM_EN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

# ----------------------------------------------------------------------------------------------
# LONG CLIPS (writing demos + dialogue scenes) keyed by vault 'file' stem. Egyptian scenes are excluded.
# (id, unit, lesson, kind, register, note)
# ----------------------------------------------------------------------------------------------
LONG = {
    "u01_extra_c14b5902": ("u1_d4_scene1_formal", 1, "Drill 4", "dialogue scene",
                           "formal", "Scene 1 'Ahlan wa sahlan' — formal version (people introduce themselves)."),
    "u01_extra_cd8b92ed": ("u1_d4_scene1_colloquial", 1, "Drill 4", "dialogue scene",
                           "mixed colloquial", "Scene 1 'Ahlan wa sahlan' — colloquial version; speakers from across the Arab world, MAY INCLUDE EGYPTIAN speakers — check before using any audio."),
    "u02_extra_618d24fe": ("u2_writing_alif", 2, "Writing ا", "writing demo", "formal", "El-Shinnawi writes alif."),
    "u02_extra_1f3117ea": ("u2_writing_baa", 2, "Writing ب", "writing demo", "formal", "El-Shinnawi writes baa."),
    "u02_extra_5fbb4784": ("u2_writing_taa", 2, "Writing ت", "writing demo", "formal", "El-Shinnawi writes taa (publisher file is oddly named ABU2LE3.mp4)."),
    "u02_extra_4c1ddaa4": ("u2_writing_thaa", 2, "Writing ث", "writing demo", "formal", "El-Shinnawi writes thaa."),
    "u02_extra_f807f722": ("u2_writing_waaw", 2, "Writing و", "writing demo", "formal", "El-Shinnawi writes waaw."),
    "u02_extra_d10ae207": ("u2_writing_yaa", 2, "Writing ي", "writing demo", "formal", "El-Shinnawi writes yaa."),
    "u02_extra_de196f61": ("u2_writing_fatha", 2, "Writing ـَـ", "writing demo", "formal", "El-Shinnawi writes fatHa."),
    "u02_extra_33def406": ("u2_writing_damma", 2, "Writing ـُـ", "writing demo", "formal", "El-Shinnawi writes Damma (short clip, still a demo, not a word)."),
    "u02_extra_2c57693e": ("u2_writing_kasra", 2, "Writing ـِـ", "writing demo", "formal", "El-Shinnawi writes kasra."),
    "u02_extra_34fb243b": ("u2_d17_scene2_levantine", 2, "Drill 17", "dialogue scene", "shaami",
                           "Scene 2, Levantine version: 'inti min ween?'."),
    "u03_extra_e0f17593": ("u3_writing_jiim", 3, "Writing ج", "writing demo", "formal", "El-Shinnawi writes ج and similar letters."),
    "u03_extra_e3742b68": ("u3_writing_Haa", 3, "Writing ح", "writing demo", "formal", "El-Shinnawi writes ح in the word حَبيب."),
    "u03_extra_e237cddb": ("u3_writing_khaa", 3, "Writing خ", "writing demo", "formal", "El-Shinnawi writes خ."),
    "u03_extra_749a6fcd": ("u3_writing_sukuun", 3, "Writing ـْـ", "writing demo", "formal", "El-Shinnawi writes sukuun."),
    "u03_extra_89f203cc": ("u3_d15_scene3a_levantine", 3, "Drill 15", "dialogue scene", "shaami", "Scene 3A, Levantine version: 'kiifik?'."),
    "u03_extra_fd57795c": ("u3_d15_scene3b_levantine", 3, "Drill 15", "dialogue scene", "shaami", "Scene 3B, Levantine version: 'SabaaH l-kheer'."),
    "u04_extra_15701a54": ("u4_writing_hamza", 4, "Writing ء", "writing demo", "formal", "El-Shinnawi writes hamza."),
    "u04_extra_5265a8a1": ("u4_writing_daal", 4, "Writing د", "writing demo", "formal", "El-Shinnawi writes daal."),
    "u04_extra_08d604b3": ("u4_writing_dhaal", 4, "Writing ذ", "writing demo", "formal", "El-Shinnawi writes dhaal (connected and unconnected)."),
    "u04_extra_9e9472be": ("u4_writing_raa", 4, "Writing ر", "writing demo", "formal", "El-Shinnawi writes raa."),
    "u04_extra_f1255177": ("u4_writing_zaay", 4, "Writing ز", "writing demo", "formal", "El-Shinnawi writes zaay."),
    "u04_extra_c8ae0afc": ("u4_writing_numbers", 4, "Writing Numbers 1–10", "writing demo", "formal", "El-Shinnawi writes the numerals 0-10."),
    "u04_extra_77649ac5": ("u4_d4_scene4a_levantine", 4, "Drill 4", "dialogue scene", "shaami", "Scene 4A, Levantine version: 'kiifak?'."),
    "u04_extra_6d19ec1c": ("u4_d4_scene4b_levantine", 4, "Drill 4", "dialogue scene", "shaami", "Scene 4B, Levantine version: 'l-Hamdilla'."),
    "u04_extra_d00e502a": ("u4_d18_scene4c_levantine", 4, "Drill 18", "dialogue scene", "shaami",
                           "Scene 4C, Levantine version ('tsharrafna'). Same office set as the Levantine Scene 2 video."),
}
EXCLUDED_EGYPTIAN_SCENES = {
    "u02_extra_4710d5d5": "Unit 2 Drill 17 — Scene 2, Egyptian version ('HaDritak min maSr?')",
    "u03_extra_557e65e5": "Unit 3 Drill 15 — Scene 3A, Egyptian version ('izzay Hadritik?')",
    "u03_extra_fb69a342": "Unit 3 Drill 15 — Scene 3B, Egyptian version ('SabaaH l-kheer')",
    "u04_extra_625eeae3": "Unit 4 Drill 4 — Scene 4A, Egyptian version ('izayyak?')",
    "u04_extra_676c38b8": "Unit 4 Drill 4 — Scene 4B, Egyptian version ('al-Hamdu Lillah')",
    "u04_extra_cda3daa4": "Unit 4 Drill 18 — Scene 4C, first video (Lingco label 'tasharrafna'); PROBABLY EGYPTIAN: Egyptian-first order on every other scene pair, and a different set from the Levantine videos — verify before ever using",
}
