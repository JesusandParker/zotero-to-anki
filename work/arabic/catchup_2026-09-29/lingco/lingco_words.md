# Lingco (Alif Baa 3e) Units 1-4 — every word with publisher audio

Built 2026-09-29 by `build_lingco_words.py` (re-run it after `clipcheck/clips_asr.json` lands to fill the ASR columns). Machine-readable twin: `lingco_words.json` (545 records). Excluded clips: `lingco_excluded_clips.json` (99).

## Counts

| Unit | adjective | adverb | demonstrative | interrogative | letter-name | long_clip | nonword | noun | number | pair | particle | phrase | place | preposition | pronoun | suffix | syllable | verb | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  | 28 | 2 |  | 3 |  |  |  | 22 | 20 | 3 | 1 |  |  |  | 79 |
| 2 | 3 |  |  | 6 | 3 | 10 | 8 | 36 |  | 14 | 3 | 7 | 3 |  | 8 | 4 | 1 | 37 | 143 |
| 3 | 5 | 2 | 4 | 2 |  | 6 |  | 86 |  |  | 4 | 9 | 2 | 3 |  |  |  | 38 | 161 |
| 4 | 6 |  |  |  | 7 | 9 |  | 76 | 18 |  | 1 | 16 | 1 |  | 4 | 4 |  | 20 | 162 |
| all | 14 | 2 | 4 | 8 | 38 | 27 | 8 | 201 | 18 | 14 | 8 | 54 | 26 | 6 | 13 | 8 | 1 | 95 | 545 |

- Real words: **509**; not-real (syllable/nonword drill strings): 9; long clips (no word content): 27; dialect phrases awaiting transcription: 15.
- Low-confidence meanings: **26** — u2_le1_02, u2_le1_03, u2_le4_03, u2_le5_05, u2_le6_05, u2_le7_04, u2_le8_02, u2_le10_02, u2_d4_03, u2_d8_02, u2_d11_04, u2_d11_08, u2_d12_04, u2_d12_06, u2_d12_07, u2_d12_10, u3_le3_03, u3_le4_01, u3_d1_03, u3_d1_06, u3_d5_02, u3_d6_02, u3_d6_11, u3_d6_12, u3_d6_15, u4_d9_02.
- ASR check: NOT YET AVAILABLE (clips_asr.json missing) — every record has asr_checked:false; disagreements: 0.

## How to read this

- **One record per exercise item** (the same word in two exercises = two records; `also_in` cross-links them). Vocabulary: one record per row for the formal form; the shaami clip rides along as an alternate when it is the same word (`audio[].dialect = "shaami"`, `says` = what that clip says), and gets its **own record (`register: shaami`)** when the Levantine form is a different word or has a documented different pronunciation.
- **Item numbers = publisher file numbers** (`AB3e_U4LE5-03` = item 3) everywhere EXCEPT Unit 1 Drill 3 (countries), whose files are numbered alphabetically; there the item is the book/map number and the file is recorded separately.
- **Arabic**: `arabic` is the printed form with any missing short vowels / sukuun / shadda filled in (`vowels_added: true` when I added or corrected marks; `arabic_printed` is exactly what Lingco/the book/the key prints). Dictation and letter-connection drills print no words: their Arabic comes from the Alif Baa answer key.
- **letter_positions**: for each Unit 1-4 letter in the word, the glyph form(s) it takes there, in order of occurrence — a list, because a letter can occur twice (حُدود → د: final, isolated). Hamza is keyed `ء` by word position (initial/medial/final) with seat details in `hamza` (seat alif/waaw/yaa/line). Plain alif `ا` only; alif carrying hamza (أ إ آ) is counted under `ء`.
- **word_type** adds to the requested list: pronoun, preposition, particle, interrogative, demonstrative, adverb, suffix, pair (a clip that says a contrast pair), long_clip.
- **No Egyptian**: every maSri clip, the Egyptian scene videos, and Unit 1 LE2's Egyptian column are excluded (listed in `lingco_excluded_clips.json`). Unit 3 LE1 clips say each word in three ج pronunciations including the Egyptian hard g — flagged `clip_caution`.

## Unit 1 — Listening Exercise 1  ·  _Arabic letters and sounds — hear each letter pronounced_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u1_le1_01 | أَلِف | alif | the letter alif (ا) — sound: long vowel aa (alif is also the seat of hamza) | letter-name | med | AB3e_pronouncing_01_alif.mp4 (formal, 3.98s) | not in ASR job |
| u1_le1_02 | باء | baa' | the letter baa (ب) — sound: b | letter-name | med | AB3e_pronouncing_02_baa.mp4 (formal, 3.88s) | not in ASR job |
| u1_le1_03 | تاء | taa' | the letter taa (ت) — sound: t | letter-name | med | AB3e_pronouncing_03_taa.mp4 (formal, 4.55s) | not in ASR job |
| u1_le1_04 | ثاء | thaa' | the letter thaa (ث) — sound: th as in 'three' | letter-name | med | AB3e_pronouncing_04_thaa.mp4 (formal, 3.95s) | not in ASR job |
| u1_le1_05 | جيم | jiim | the letter jiim (ج) — sound: j as in 'jam' | letter-name | med | AB3e_pronouncing_05_jiim.mp4 (formal, 3.58s) | not in ASR job |
| u1_le1_06 | حاء | Haa' | the letter Haa (ح) — sound: H — a strong, breathy h from the throat (no English equivalent) | letter-name | med | AB3e_pronouncing_06_Haa.mp4 (formal, 3.68s) | not in ASR job |
| u1_le1_07 | خاء | khaa' | the letter khaa (خ) — sound: kh — like the ch in German 'Bach' | letter-name | med | AB3e_pronouncing_07_khaa.mp4 (formal, 3.18s) | not in ASR job |
| u1_le1_08 | دال | daal | the letter daal (د) — sound: d | letter-name | med | AB3e_pronouncing_08_daal.mp4 (formal, 3.45s) | not in ASR job |
| u1_le1_09 | ذال | dhaal | the letter dhaal (ذ) — sound: dh — th as in 'this' | letter-name | med | AB3e_pronouncing_09_dhaal.mp4 (formal, 18.23s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_10 | راء | raa' | the letter raa (ر) — sound: r — tapped/rolled r | letter-name | med | AB3e_pronouncing_10_raa.mp4 (formal, 3.98s) | not in ASR job |
| u1_le1_11 | زاي | zaay | the letter zaay (ز) — sound: z | letter-name | med | AB3e_pronouncing_11_zaay.mp4 (formal, 3.31s) | not in ASR job |
| u1_le1_12 | سين | siin | the letter siin (س) — sound: s | letter-name | med | AB3e_pronouncing_12_seen.mp4 (formal, 4.38s) | not in ASR job |
| u1_le1_13 | شين | shiin | the letter shiin (ش) — sound: sh | letter-name | med | AB3e_pronouncing_13_sheen.mp4 (formal, 4.68s) | not in ASR job |
| u1_le1_14 | صاد | Saad | the letter Saad (ص) — sound: S — emphatic (deep) s | letter-name | med | AB3e_pronouncing_14_Saad.mp4 (formal, 18.49s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_15 | ضاد | Daad | the letter Daad (ض) — sound: D — emphatic (deep) d | letter-name | med | AB3e_pronouncing_15_Daad.mp4 (formal, 17.93s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_16 | طاء | Taa' | the letter Taa (ط) — sound: T — emphatic (deep) t | letter-name | med | AB3e_pronouncing_16_Taaa.mp4 (formal, 16.63s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_17 | ظاء | DHaa' | the letter DHaa (ظ) — sound: DH — emphatic (deep) dh | letter-name | med | AB3e_pronouncing_17_Dhaa.mp4 (formal, 18.76s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_18 | عَيْن | cayn | the letter cayn (ع) — sound: c (cayn) — voiced sound squeezed in the throat (no English equivalent) | letter-name | med | AB3e_pronouncing_18_ayn.mp4 (formal, 16.33s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_19 | غَيْن | ghayn | the letter ghayn (غ) — sound: gh — like a French/Parisian r | letter-name | med | AB3e_pronouncing_19_ghayn.mp4 (formal, 19.83s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_20 | فاء | faa' | the letter faa (ف) — sound: f | letter-name | med | AB3e_pronouncing_20_faa.mp4 (formal, 4.35s) | not in ASR job |
| u1_le1_21 | قاف | qaaf | the letter qaaf (ق) — sound: q — a k made deep in the throat | letter-name | med | AB3e_pronouncing_21_qaaf.mp4 (formal, 4.45s) | not in ASR job |
| u1_le1_22 | كاف | kaaf | the letter kaaf (ك) — sound: k | letter-name | med | AB3e_pronouncing_22_kaaf.mp4 (formal, 16.49s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_23 | لام | laam | the letter laam (ل) — sound: l | letter-name | med | AB3e_pronouncing_23_laam.mp4 (formal, 4.05s) | not in ASR job |
| u1_le1_24 | ميم | miim | the letter miim (م) — sound: m | letter-name | med | AB3e_pronouncing_24_miim.mp4 (formal, 4.35s) | not in ASR job |
| u1_le1_25 | نون | nuun | the letter nuun (ن) — sound: n | letter-name | med | AB3e_pronouncing_25_nuun.mp4 (formal, 4.75s) | not in ASR job |
| u1_le1_26 | هاء | haa' | the letter haa (ه) — sound: h | letter-name | med | AB3e_pronouncing_26_ha.mp4 (formal, 18.13s) | long clip (>12 s): content unverified; not in ASR job |
| u1_le1_27 | واو | waaw | the letter waaw (و) — sound: w / long vowel uu | letter-name | med | AB3e_pronouncing_27_waaw.mp4 (formal, 4.15s) | not in ASR job |
| u1_le1_28 | ياء | yaa' | the letter yaa (ي) — sound: y / long vowel ii | letter-name | med | AB3e_pronouncing_28_yaa.mp4 (formal, 3.58s) | not in ASR job |

## Unit 1 — Listening Exercise 2  ·  _Dialect variation — the same phrases in Tunisian, Egyptian, Lebanese and Omani Arabic_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u1_le2_01 | — | — | Good morning! | phrase | high | u01_extra_d5c1ae02.mp3 (lebanese, 1.4s) | **shaami**; Arabic pending transcription |
| u1_le2_02 | — | — | How are you? | phrase | high | u01_extra_380334e6.mp3 (lebanese, 1.03s) | **shaami**; Arabic pending transcription |
| u1_le2_03 | — | — | Good (fine) | phrase | high | u01_extra_98bbb415.mp3 (lebanese, 0.93s) | **shaami**; Arabic pending transcription |
| u1_le2_04 | — | — | Good-bye | phrase | high | u01_extra_42ae3d12.mp3 (lebanese, 1.19s) | **shaami**; Arabic pending transcription |
| u1_le2_05 | — | — | I love Lebanon | phrase | high | u01_extra_3ecafbb6.mp3 (lebanese, 1.71s) | **shaami**; Arabic pending transcription |
| u1_le2_11 | — | — | Good morning! | phrase | high | u01_extra_272d9f47.mp3 (omani, 1.22s) | **omani**; Arabic pending transcription |
| u1_le2_12 | — | — | How are you? | phrase | high | u01_extra_bb79a47c.mp3 (omani, 0.96s) | **omani**; Arabic pending transcription |
| u1_le2_13 | — | — | Good (fine) | phrase | high | u01_extra_64868ad4.mp3 (omani, 0.85s) | **omani**; Arabic pending transcription |
| u1_le2_14 | — | — | Good-bye | phrase | high | u01_extra_eafcf2c9.mp3 (omani, 1.17s) | **omani**; Arabic pending transcription |
| u1_le2_15 | — | — | I love Oman | phrase | high | u01_extra_3f70f419.mp3 (omani, 1.3s) | **omani**; Arabic pending transcription |
| u1_le2_16 | — | — | Good morning! | phrase | high | u01_extra_b2d50fb9.mp3 (tunisian, 1.4s) | **tunisian**; Arabic pending transcription |
| u1_le2_17 | — | — | How are you? | phrase | high | u01_extra_ab602e45.mp3 (tunisian, 1.35s) | **tunisian**; Arabic pending transcription |
| u1_le2_18 | — | — | Good (fine) | phrase | high | u01_extra_77605002.mp3 (tunisian, 1.19s) | **tunisian**; Arabic pending transcription |
| u1_le2_19 | — | — | Good-bye | phrase | high | u01_extra_343a1e5e.mp3 (tunisian, 1.27s) | **tunisian**; Arabic pending transcription |
| u1_le2_20 | — | — | I love Tunisia | phrase | high | u01_extra_461b3952.mp3 (tunisian, 1.48s) | **tunisian**; Arabic pending transcription |

## Unit 1 — Drill 3  ·  _Where is Arabic spoken? — Arab countries and their capitals_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u1_d3_01 | المَغْرِب — الرِّباط | al-maghrib — ar-ribaaT | Morocco — capital: Rabat | place | med | u01_extra_ce3a382c.mp3 (formal, 3.36s) |  |
| u1_d3_02 | موريتانْيا — نُواكْشوط | muuriitaanyaa — nuwaakshuuT | Mauritania — capital: Nouakchott | place | med | u01_extra_5f45a9a3.mp3 (formal, 3.96s) |  |
| u1_d3_03 | الجَزائِر — الجَزائِر | al-jazaa'ir — al-jazaa'ir | Algeria — capital: Algiers (same name as the country) | place | med | u01_extra_19e61e01.mp3 (formal, 3.78s) |  |
| u1_d3_04 | تونِس — تونِس | tuunis — tuunis | Tunisia — capital: Tunis (same name as the country) | place | med | u01_extra_0ff87cb3.mp3 (formal, 3.18s) |  |
| u1_d3_05 | ليبْيا — طَرابُلُس | liibyaa — Taraabulus | Libya — capital: Tripoli | place | med | u01_extra_03cf1866.mp3 (formal, 3.86s) |  |
| u1_d3_06 | مِصْر — القاهِرة | miSr — al-qaahira | Egypt — capital: Cairo | place | med | u01_extra_8c7c616c.mp3 (formal, 3.57s) |  |
| u1_d3_07 | السّودان — الخَرْطوم | as-suudaan — al-kharTuum | Sudan — capital: Khartoum | place | med | u01_extra_8982224e.mp3 (formal, 4.3s) |  |
| u1_d3_08 | الصّومال — مَقَديشو | aS-Suumaal — maqadiishuu | Somalia — capital: Mogadishu | place | med | u01_extra_84cd880d.mp3 (formal, 4.38s) |  |
| u1_d3_09 | الأُرْدُنّ — عَمّان | al-urdunn — cammaan | Jordan — capital: Amman | place | med | u01_extra_8f549bec.mp3 (formal, 3.88s) |  |
| u1_d3_10 | فِلَسْطين — القُدْس | filasTiin — al-quds | Palestine (book: 'Israel/Palestine') — Jerusalem | place | med | u01_extra_39cfb6aa.mp3 (formal, 4.98s) |  |
| u1_d3_11 | لُبْنان — بَيْروت | lubnaan — bayruut | Lebanon — capital: Beirut | place | med | u01_extra_90f90bc4.mp3 (formal, 3.23s) |  |
| u1_d3_12 | سورْيا — دِمَشْق | suuryaa — dimashq | Syria — capital: Damascus | place | med | u01_extra_062914c6.mp3 (formal, 3.55s) |  |
| u1_d3_13 | العِراق — بَغْداد | al-ciraaq — baghdaad | Iraq — capital: Baghdad | place | med | u01_extra_14b9bd2d.mp3 (formal, 3.59s) |  |
| u1_d3_14 | الكُوَيْت — الكُوَيْت | al-kuwayt — al-kuwayt | Kuwait — capital: Kuwait City (same name) | place | med | u01_extra_dcc28cc6.mp3 (formal, 3.57s) |  |
| u1_d3_15 | السَّعودِيّة — الرِّياض | as-sacuudiyya — ar-riyaaD | Saudi Arabia — capital: Riyadh | place | med | u01_extra_48457f02.mp3 (formal, 3.79s) |  |
| u1_d3_16 | قَطَر — الدَّوْحة | qaTar — ad-dawHa | Qatar — capital: Doha | place | med | u01_extra_51e7738a.mp3 (formal, 3.02s) |  |
| u1_d3_17 | البَحْرَيْن — المَنامة | al-baHrayn — al-manaama | Bahrain — capital: Manama | place | med | u01_extra_352e384a.mp3 (formal, 3.83s) |  |
| u1_d3_18 | الإِمارات — أَبو ظَبْي | al-imaaraat — abuu DHabii | United Arab Emirates — capital: Abu Dhabi | place | med | u01_extra_fd175d7d.mp3 (formal, 4.22s) |  |
| u1_d3_19 | عُمان — مَسْقَط | cumaan — masqaT | Oman — capital: Muscat | place | med | u01_extra_9444e8e1.mp3 (formal, 3.26s) |  |
| u1_d3_20 | اليَمَن — صَنْعاء | al-yaman — Sancaa' | Yemen — capital: Sanaa | place | med | u01_extra_66a28bac.mp3 (formal, 3.28s) |  |

## Unit 1 — Drill 4

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u1_d4_scene1_colloquial | — | — | Scene 1 'Ahlan wa sahlan' — colloquial version; speakers from across the Arab world, MAY INCLUDE EGYPTIAN speakers — check before using any audio. | long_clip |  | u01_extra_cd8b92ed.wav (mixed colloquial, 46.55s) | **mixed colloquial**; 47 s dialogue scene |
| u1_d4_scene1_formal | — | — | Scene 1 'Ahlan wa sahlan' — formal version (people introduce themselves). | long_clip |  | u01_extra_c14b5902.wav (formal, 52.68s) | 53 s dialogue scene |

## Unit 1 — New Vocabulary  ·  _New Vocabulary: Greetings and introductions_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u1_v01 | السَّلامُ عَلَيْكُم | assalaamu calaykum | Peace be upon you — the Islamic greeting ('hello') | phrase | high | u01_0006_assalaamu_calaykum_formal.mp3 (formal, 2.04s)<br>u01_0006_assalaamu_calaykum_shaami.mp3 (shaami, 2.3s) | vowels added |
| u1_v02 | أَهْلاً | ahlan | Hello! / Hi! | phrase | high | u01_0007_ahlan_formal.mp3 (formal, 1.04s) | vowels added |
| u1_v02_shaami | أَهْلا | ahla | Hello! / Hi! (Levantine pronunciation) | phrase | high | u01_0007_ahla_shaami.mp3 (shaami, 1.28s) | **shaami**; vowels added |
| u1_v03 | أَهْلاً وَسَهْلاً | ahlan wa sahlan | Hello! / Welcome! | phrase | high | u01_0008_ahlan_wa_sahlan_formal.mp3 (formal, 1.65s) | vowels added |
| u1_v03_shaami | أَهْلا وْسَهْلا | ahla w sahla | Hello! / Welcome! (Levantine pronunciation) | phrase | high | u01_0008_ahla_w_sahla_shaami.mp3 (shaami, 1.78s) | **shaami**; vowels added |
| u1_v04 | مَرْحَباً | marHaban | Hello! (used especially in the Levant) | phrase | high | u01_0009_marhaban_formal.mp3 (formal, 1.33s) | vowels added |
| u1_v04_shaami | مَرْحَبا | marHaba | Hello! (Levantine) | phrase | high | u01_0009_marhaba_shaami.mp3 (shaami, 1.41s) | **shaami**; vowels added |
| u1_v05 | أَنا | ana | I | pronoun | high | u01_0010_ana_formal.mp3 (formal, 1.28s)<br>u01_0010_ana_shaami.mp3 (shaami, 1.12s) |  |
| u1_v06 | اِسْمي | ismii | my name | noun | high | u01_0011_ismii_formal.mp3 (formal, 1.44s)<br>u01_0011_ismi_shaami.mp3 (shaami, 1.36s) | vowels added |
| u1_v07 | مِن | min | from | preposition | high | u01_0012_min_formal.mp3 (formal, 1.2s)<br>u01_0012_min_shaami.mp3 (shaami, 1.02s) |  |
| u1_v08 | مَدينة | madiinat | the city of … (used right before a city's name) | noun | high | u01_0013_madiinat_formal.mp3 (formal, 1.51s) | vowels added |
| u1_v08_shaami | مَدينة | madiinit | the city of … (Levantine pronunciation) | noun | high | u01_0013_madiinit_shaami.mp3 (shaami, 1.25s) | **shaami**; vowels added |
| u1_v09 | في | fii | in | preposition | high | u01_0014_fii_formal.mp3 (formal, 1.2s) |  |
| u1_v09_shaami | بِـ | bi- | in (Levantine; attached to the next word) | preposition | high | u01_0014_bi_shaami.mp3 (shaami, 1.12s) | **shaami** |

## Unit 2 — Listening Exercise 1  ·  _Frontal vs deep alif (each clip = a contrast pair)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le1_01 | تاب / طاب | taab / Taab | he repented / it was good, pleasant | pair | med | u02_extra_b2a926ce.mp3 (formal, 3.72s) |  |
| u2_le1_02 | ساح / صاح | saaH / SaaH | it flowed; he roamed, toured / he shouted, cried out | pair | low | u02_extra_bd698848.mp3 (formal, 3.72s) |  |
| u2_le1_03 | داني / ضاني | daanii / Daanii | near, close (also the name Dani) / of sheep — mutton/lamb (Egyptian usage: لَحْم ضاني) | pair | low | u02_extra_8afeb36b.mp3 (formal, 3.55s) |  |
| u2_le1_04 | ذال / ظالِم | dhaal / DHaalim | the letter dhaal (ذ) / unjust; an oppressor, wrongdoer | pair | high | u02_extra_91a480de.mp3 (formal, 3.53s) | vowels added |

## Unit 2 — Listening Exercise 2  ·  _Pronouncing ب (frontal vowels)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le2_01 | باء | baa' | the letter name baa (ب) | letter-name | high | u02_extra_b76d65d9.mp3 (formal, 3.29s) |  |
| u2_le2_02 | باب | baab | door | noun | high | u02_extra_96c244e7.mp3 (formal, 3.29s) |  |
| u2_le2_03 | لُبْنان | lubnaan | Lebanon | place | high | u02_extra_607af667.mp3 (formal, 2.88s) | vowels added |
| u2_le2_04 | ليبْيا | liibyaa | Libya | place | high | u02_extra_a92d8ff0.mp3 (formal, 2.26s) | vowels added |
| u2_le2_05 | بَيْت | bayt | house | noun | high | u02_extra_49bfae12.mp3 (formal, 2.83s) | vowels added |
| u2_le2_06 | حُبّ | Hubb | love | noun | high | u02_extra_6a1c8cf7.mp3 (formal, 2.14s) | vowels added |

## Unit 2 — Listening Exercise 3  ·  _Pronouncing ت_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le3_01 | تاء | taa' | the letter name taa (ت) | letter-name | high | u02_extra_6fbe7679.mp3 (formal, 1.73s) |  |
| u2_le3_02 | بات | baat | he spent the night | verb | med | u02_extra_08eb5c86.mp3 (formal, 2.9s) |  |
| u2_le3_03 | توت | tuut | mulberries; berries (collective) | noun | high | u02_extra_c8987fb7.mp3 (formal, 2.3s) |  |
| u2_le3_04 | وَتَد | watad | tent peg, stake | noun | high | u02_extra_561b7467.mp3 (formal, 2.3s) | vowels added |
| u2_le3_05 | بِنْت | bint | girl; daughter | noun | high | u02_extra_9f03cae0.mp3 (formal, 1.82s) | vowels added |
| u2_le3_06 | شِتاء | shitaa' | winter | noun | high | u02_extra_a741b38d.mp3 (formal, 2.84s) | vowels added |

## Unit 2 — Listening Exercise 4  ·  _Listening to ث_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le4_01 | ثاء | thaa' | the letter name thaa (ث) | letter-name | high | u02_extra_a56730d2.mp3 (formal, 3.17s) |  |
| u2_le4_02 | ثابِت | thaabit | firm, fixed, stable (also a man's name, Thabit) | adjective | high | u02_extra_0735f7da.mp3 (formal, 2.06s) | vowels added |
| u2_le4_03 | تثبت | tathbut / tuthbit (unclear) | unclear without the audio: tathbut 'she stays firm / you (m.) stay firm' OR tuthbit 'she proves / you (m.) prove' | verb | low | u02_extra_535995dd.mp3 (formal, 2.71s) |  |
| u2_le4_04 | أَثاث | athaath | furniture | noun | high | u02_extra_c570a205.mp3 (formal, 2.11s) | vowels added |
| u2_le4_05 | بَثّ | bathth | broadcast, transmission (noun) | noun | med | u02_extra_487464e0.mp3 (formal, 2.07s) | vowels added |

## Unit 2 — Listening Exercise 5  ·  _Contrasting ث (th) and ذ (dh) (each clip = a pair)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le5_01 | ثاب / ذاب | thaab / dhaab | he returned, came back / it melted, dissolved | pair | med | u02_extra_80332747.mp3 (formal, 4.01s) |  |
| u2_le5_02 | بُثور / بُذور | buthuur / budhuur | pimples, blisters (plural of بَثْرة) / seeds (plural of بَذْرة) | pair | high | u02_extra_286b3e87.mp3 (formal, 3.94s) | vowels added |
| u2_le5_03 | آثار / آذار | aathaar / aadhaar | traces; ruins, antiquities (plural of أَثَر) / March (month name used in the Levant and Iraq) | pair | high | u02_extra_03bd912e.mp3 (formal, 4.22s) |  |
| u2_le5_04 | تَثوب / تَذوب | tathuub / tadhuub | she returns; you (m.) return (to your senses) / she/it melts; you (m.) melt | pair | med | u02_extra_145f8eb2.mp3 (formal, 3.96s) | vowels added |
| u2_le5_05 | جَثّ / جَذّ | jathth / jadhdh | he uprooted (rare) / he cut off (rare) | pair | low | u02_extra_bbc18380.mp3 (formal, 3.5s) | vowels added |

## Unit 2 — Listening Exercise 6  ·  _Long vowel و (uu) — give it full length_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le6_01 | توت | tuut | mulberries; berries (collective) | noun | high | u02_extra_e5fa3e1e.mp3 (formal, 2.01s) |  |
| u2_le6_02 | تابوت | taabuut | coffin, casket | noun | high | u02_extra_b940dc0f.mp3 (formal, 1.7s) |  |
| u2_le6_03 | ثُبوت | thubuut | firmness; proof, being established | noun | med | u02_extra_e564d02c.mp3 (formal, 1.59s) | vowels added |
| u2_le6_04 | تونِس | tuunis | Tunisia; Tunis | place | high | u02_extra_52788deb.mp3 (formal, 1.93s) | vowels added |
| u2_le6_05 | تَحْبو | taHbuu | she crawls; you (m.) crawl (like a baby) | verb | low | u02_extra_c7121c0c.mp3 (formal, 1.65s) | vowels added |

## Unit 2 — Listening Exercise 7  ·  _Long vowel ي (ii)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le7_01 | توبي | tuubii | repent! (said to a female) | verb | med | u02_extra_7c4bfdeb.mp3 (formal, 3.05s) |  |
| u2_le7_02 | تَثْبيت | tathbiit | fixing, securing; confirmation; (software) installation | noun | high | u02_extra_43e758b7.mp3 (formal, 3.26s) | vowels added |
| u2_le7_03 | ليبي | liibii | Libyan (m.) | adjective | high | u02_extra_c508ab56.mp3 (formal, 2.9s) |  |
| u2_le7_04 | تُثْبِتي | tuthbitii | (that) you (f.) prove / confirm | verb | low | u02_extra_b459fb64.mp3 (formal, 2.91s) | vowels added |

## Unit 2 — Listening Exercise 8  ·  _Hearing vowel length — first word long vowel, second short (each clip = a pair)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le8_01 | ساد / سَدّ | saad / sadd | he prevailed, ruled / dam; blocking | pair | med | u02_extra_1f15366a.mp3 (formal, 3.53s) | vowels added |
| u2_le8_02 | توب / تُب | tuub / tub | (no formal meaning — colloquial 'robe' / 'repent!') / repent! (said to a male) | pair | low | u02_extra_e6a28c2c.mp3 (formal, 3.1s) |  |
| u2_le8_03 | شابّ / شَبّ | shaabb / shabb | young man / he grew up; (a fire) blazed | pair | med | u02_extra_d6ac85fd.mp3 (formal, 2.93s) | vowels added |
| u2_le8_04 | بير / بِرّ | biir / birr | a well (informal spelling of بِئْر) / righteousness; kindness (especially to parents) | pair | med | u02_extra_a3b038db.mp3 (formal, 2.95s) | vowels added |
| u2_le8_05 | تَقول / تَقُل | taquul / taqul | she says; you (m.) say / (don't) say — short form, as in لا تَقُلْ | pair | med | u02_extra_6f8793b0.mp3 (formal, 3.53s) | vowels added |

## Unit 2 — Listening Exercise 9  ·  _Contrasting alif (aa) and fatHa (a)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le9_01 | ثابَت | thaabat | she returned, came back | verb | med | u02_extra_ceb2ba6b.mp3 (formal, 3.27s) |  |
| u2_le9_02 | تابَ | taaba | he repented | verb | high | u02_extra_fd8cd9c2.mp3 (formal, 2.71s) |  |
| u2_le9_03 | باتَت | baatat | she spent the night | verb | high | u02_extra_454fcc4f.mp3 (formal, 2.45s) |  |
| u2_le9_04 | تابَت | taabat | she repented | verb | high | u02_extra_b4e8a392.mp3 (formal, 2.78s) |  |
| u2_le9_05 | ثَبات | thabaat | firmness, stability | noun | high | u02_extra_81fa93d5.mp3 (formal, 3.75s) |  |

## Unit 2 — Listening Exercise 10  ·  _Hearing and pronouncing Damma_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le10_01 | تُب | tub | repent! (said to a male) | verb | med | u02_extra_23814888.mp3 (formal, 2.62s) |  |
| u2_le10_02 | بُثّ | buthth | broadcast! / spread! (said to a male) | verb | low | u02_extra_e59cfea2.mp3 (formal, 1.99s) | vowels added |
| u2_le10_03 | ثُبوت | thubuut | firmness; proof, being established | noun | med | u02_extra_34366a57.mp3 (formal, 3.29s) |  |
| u2_le10_04 | حُبوب | Hubuub | grains, seeds; pills (plural of حَبّة) | noun | high | u02_extra_4f76591f.mp3 (formal, 2.78s) |  |
| u2_le10_05 | صُبّ | Subb | pour! (said to a male) | verb | med | u02_extra_76c1770a.mp3 (formal, 2.28s) | vowels added |
| u2_le10_06 | تَثْبُت | tathbut | she stays firm; you (m.) stay firm | verb | med | u02_extra_c4765da5.mp3 (formal, 3.26s) | vowels added |

## Unit 2 — Listening Exercise 11  ·  _Pronouncing kasra_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_le11_01 | ثِب | thib | jump! leap! (said to a male) | verb | med | u02_extra_43c117b8.mp3 (formal, 2.09s) |  |
| u2_le11_02 | تُثْبِتي | tuthbitii | (that) you (f.) prove / confirm | verb | med | u02_extra_22979ea6.mp3 (formal, 3.12s) | vowels added |
| u2_le11_03 | بِت | bit | spend the night! (said to a male) | verb | med | u02_extra_78f63f10.mp3 (formal, 2.23s) |  |
| u2_le11_04 | طِبّ | Tibb | medicine (the field) | noun | high | u02_extra_f99d4837.mp3 (formal, 1.97s) | vowels added |
| u2_le11_05 | تُحِبّ | tuHibb | you (m.) love; she loves | verb | high | u02_extra_b16a07fb.mp3 (formal, 2.3s) | vowels added |
| u2_le11_06 | كِتابي | kitaabii | my book | noun | high | u02_extra_22a971bf.mp3 (formal, 3.05s) |  |

## Unit 2 — Drill 2  ·  _Dictation (ا ب ت) — video; write what you hear_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d2_01 | با | baa | (syllable 'baa' — no meaning) | syllable | high | u02_extra_bfe6b20d.wav (formal, 1.83s) | not a real word |
| u2_d2_02 | تاب | taab | he repented | verb | med | u02_extra_6bcd2634.wav (formal, 1.9s) |  |
| u2_d2_03 | باتا | baataa | (no meaning — sound/spelling drill) | nonword | high | u02_extra_a5de3854.wav (formal, 2.56s) | not a real word |
| u2_d2_04 | تابا | taabaa | (no meaning here — sound/spelling drill) | nonword | med | u02_extra_7e0d7a28.wav (formal, 2.82s) | not a real word |
| u2_d2_05 | باب | baab | door | noun | high | u02_extra_1986d36a.wav (formal, 2.15s) |  |
| u2_d2_06 | بات | baat | he spent the night | verb | med | u02_extra_b2f7d0ab.wav (formal, 2.52s) |  |

## Unit 2 — Drill 4  ·  _Dictation (ث, و) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d4_01 | ثاب | thaab | he returned, came back | verb | med | u02_extra_4a845e54.wav (formal, 1.6s) |  |
| u2_d4_02 | توت | tuut | mulberries; berries (collective) | noun | high | u02_extra_83d9b314.wav (formal, 1.56s) |  |
| u2_d4_03 | توب | tuub | (no formal-Arabic meaning; colloquially 'robe, dress' or 'repent!') | nonword | low | u02_extra_6952954d.wav (formal, 2.15s) | not a real word |
| u2_d4_04 | تابوت | taabuut | coffin, casket | noun | high | u02_extra_f505bc97.wav (formal, 2.69s) |  |

## Unit 2 — Drill 5  ·  _Dictation (ي) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d5_01 | ثوبا | thuubaa | (no meaning — sound/spelling drill) | nonword | med | u02_extra_0fa4cd59.wav (formal, 2.37s) | not a real word |
| u2_d5_02 | بيتي | biitii | my house (Dr. Khouri's gloss; the formal word is بَيْتي baytii) | noun | med | u02_extra_bdba079e.wav (formal, 2.15s) |  |
| u2_d5_03 | بيتا | biitaa | (no meaning — sound/spelling drill) | nonword | med | u02_extra_169e0023.wav (formal, 2.52s) | not a real word |
| u2_d5_04 | باتي | baatii | (no meaning — sound/spelling drill) | nonword | med | u02_extra_8338e7ed.wav (formal, 2.62s) | not a real word |

## Unit 2 — Drill 8  ·  _FatHa dictation — add fatHa where you hear it_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d8_01 | تَثْبيت | tathbiit | fixing, securing; confirmation; installation | noun | high | u02_extra_5bbcb4ef.mp3 (formal, 1.98s) | vowels added |
| u2_d8_02 | بَتات | bataat | (rare) household goods; best known in بَتاتاً 'absolutely (not), at all' | noun | low | u02_extra_03f573ba.mp3 (formal, 1.98s) |  |
| u2_d8_03 | باتَت | baatat | she spent the night | verb | high | u02_extra_b1bd109b.mp3 (formal, 1.84s) |  |
| u2_d8_04 | ثَبات | thabaat | firmness, stability | noun | high | u02_extra_b48540d1.mp3 (formal, 1.93s) |  |
| u2_d8_05 | ثَبَت | thabat | he/it stood firm (the verb ثَبَتَ said without its final vowel) | verb | med | u02_extra_fd4b5d6f.mp3 (formal, 1.59s) |  |
| u2_d8_06 | ثابَت | thaabat | she returned, came back | verb | med | u02_extra_fe0b3c07.mp3 (formal, 1.88s) |  |

## Unit 2 — Drill 10  ·  _Short vowel dictation — write all short vowels_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d10_01 | ثَبُتَت | thabutat | she/it became firm | verb | med | u02_extra_1c89bdcd.mp3 (formal, 2.79s) |  |
| u2_d10_02 | تُبْتُ | tubtu | I repented | verb | med | u02_extra_e871ff6c.mp3 (formal, 2.86s) | vowels added |
| u2_d10_03 | تَبيت | tabiit | she spends the night; you (m.) spend the night | verb | high | u02_extra_0df9313f.mp3 (formal, 3.22s) |  |
| u2_d10_04 | تَتوب | tatuub | she repents; you (m.) repent | verb | high | u02_extra_0ca07e3d.mp3 (formal, 2.93s) |  |
| u2_d10_05 | تَثْبُت | tathbut | she stays firm; you (m.) stay firm | verb | med | u02_extra_6a3b0bf3.mp3 (formal, 3.01s) | vowels added |
| u2_d10_06 | ثُبوت | thubuut | firmness; proof, being established | noun | med | u02_extra_d1620978.mp3 (formal, 3.94s) |  |

## Unit 2 — Drill 11  ·  _Dictation with all vowels — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d11_01 | بابي | baabii | my door | noun | high | u02_extra_2b436750.wav (formal, 2.82s) |  |
| u2_d11_02 | توبي | tuubii | repent! (said to a female) | verb | med | u02_extra_5f992198.wav (formal, 2.69s) |  |
| u2_d11_03 | ثُبوت | thubuut | firmness; proof, being established | noun | med | u02_extra_8b4c406f.wav (formal, 2.43s) |  |
| u2_d11_04 | توبا | tuubaa | repent! (said to two people) | verb | low | u02_extra_08a61f1f.wav (formal, 2.97s) |  |
| u2_d11_05 | تَبيت | tabiit | she spends the night; you (m.) spend the night | verb | high | u02_extra_6522e4fc.wav (formal, 2.15s) |  |
| u2_d11_06 | ثَبات | thabaat | firmness, stability | noun | high | u02_extra_c134a1f1.wav (formal, 2.45s) |  |
| u2_d11_07 | تابَت | taabat | she repented | verb | high | u02_extra_b4fd5ea2.wav (formal, 2.5s) |  |
| u2_d11_08 | ثوبي | thuubii | my robe / my garment (formal spelling ثَوْبي thawbii) | noun | low | u02_extra_95889e8a.wav (formal, 2.58s) |  |

## Unit 2 — Drill 12  ·  _Reading aloud — check your pronunciation_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d12_01 | بَثّ | bathth | broadcast, transmission (noun) | noun | med | u02_extra_94a726a6.mp3 (formal, 2.54s) | vowels added |
| u2_d12_02 | بابي | baabii | my door | noun | high | u02_extra_8352a125.mp3 (formal, 2.9s) |  |
| u2_d12_03 | تُثْبِت | tuthbit | she proves; you (m.) prove / confirm | verb | med | u02_extra_044cafe7.mp3 (formal, 2.98s) | vowels added |
| u2_d12_04 | ثُب | thub | come back! return! (said to a male; rare) | verb | low | u02_extra_dfd466e3.mp3 (formal, 2.69s) |  |
| u2_d12_05 | ثَبات | thabaat | firmness, stability | noun | high | u02_extra_7201a5b2.mp3 (formal, 3.34s) |  |
| u2_d12_06 | تَبات | tabaat | (no standard meaning found — reading-practice string) | nonword | low | u02_extra_fbe5c87c.mp3 (formal, 3.0s) | not a real word |
| u2_d12_07 | تابا | taabaa | the two of them (m.) repented | verb | low | u02_extra_d42447be.mp3 (formal, 2.98s) |  |
| u2_d12_08 | ثابِت | thaabit | firm, fixed, stable | adjective | high | u02_extra_ee54c93f.mp3 (formal, 2.9s) |  |
| u2_d12_09 | توبي | tuubii | repent! (said to a female) | verb | med | u02_extra_5e99171e.mp3 (formal, 2.98s) |  |
| u2_d12_10 | تيتو | tiituu | (no meaning — reading-practice string; possibly the name 'Tito') | nonword | low | u02_extra_1a870b07.mp3 (formal, 2.79s) | not a real word |
| u2_d12_11 | ثابَت | thaabat | she returned, came back | verb | med | u02_extra_5bdd1d83.mp3 (formal, 2.41s) |  |
| u2_d12_12 | تَثْبيت | tathbiit | fixing, securing; confirmation; installation | noun | high | u02_extra_e4420d95.mp3 (formal, 2.08s) | vowels added |

## Unit 2 — Drill 17

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_d17_scene2_levantine | — | — | Scene 2, Levantine version: 'inti min ween?'. | long_clip |  | u02_extra_34fb243b.wav (shaami, 37.08s) | **shaami**; 37 s dialogue scene |

## Unit 2 — New Vocabulary  ·  _New Vocabulary: Meeting people_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_v01 | باب | baab | door | noun | high | u02_0015_door_formal.mp3 (formal, 1.38s)<br>u02_0015_door_shaami.mp3 (shaami, 1.41s) |  |
| u2_v02 | اِسْم | ism | name | noun | high | u02_0016_ism_formal.mp3 (formal, 1.33s)<br>u02_0016_ism_shaami.mp3 (shaami, 1.31s) | vowels added |
| u2_v03 | ما؟ | maa? | what? | interrogative | high | u02_0017_maa_formal.mp3 (formal, 1.36s) |  |
| u2_v03_shaami | شو؟ | shuu? | what? (Levantine) | interrogative | high | u02_0017_shuu_shaami.mp3 (shaami, 1.38s) | **shaami** |
| u2_v04 | أَهْلاً بِكَ | ahlan bika | Hello to you too — reply to 'ahlan wa sahlan' (to a male) | phrase | high | u02_0018_ahlan_bika_formal.mp3 (formal, 1.67s) | vowels added |
| u2_v04_shaami | أَهْلاً فيك | ahlan fiik | Hello to you too — reply to 'ahla w sahla' (to a male; Levantine) | phrase | high | u02_0018_ahlan_fiik_shaami.mp3 (shaami, 1.57s) | **shaami**; vowels added |
| u2_v05 | أَهْلاً بِكِ | ahlan biki | Hello to you too — reply to 'ahlan wa sahlan' (to a female) | phrase | high | u02_0019_ahlan_biki_formal.mp3 (formal, 1.78s) | vowels added |
| u2_v05_shaami | أَهْلاً فيكِ | ahlan fiiki | Hello to you too — reply to 'ahla w sahla' (to a female; Levantine) | phrase | high | u02_0019_ahlan_fiiki_shaami.mp3 (shaami, 1.57s) | **shaami**; vowels added |
| u2_v06 | وَعَلَيْكُمُ السَّلام | wa calaykumu s-salaam | And upon you be peace — reply to 'assalaamu calaykum' | phrase | high | u02_0020_wa_calaykumu_s_salaam_formal.mp3 (formal, 2.12s)<br>u02_0020_wa_calaykumu_s_salaam_shaami.mp3 (shaami, 1.88s) | vowels added |
| u2_v07 | حَضْرَتُكَ | HaDratuka | you (polite, to a male) — literally 'your presence' | pronoun | high | u02_0021_hadratuka_formal.mp3 (formal, 1.59s) | vowels added |
| u2_v07_shaami | حَضِرْتَك | HaDәrtak | you (polite, to a male; Levantine) | pronoun | high | u02_0021_had_rtak_shaami.mp3 (shaami, 1.57s) | **shaami**; vowels added |
| u2_v08 | حَضْرَتُكِ | HaDratuki | you (polite, to a female) — literally 'your presence' | pronoun | high | u02_0022_hadratuki_formal.mp3 (formal, 1.49s) | vowels added |
| u2_v08_shaami | حَضِرْتِك | HaDәrtik | you (polite, to a female; Levantine) | pronoun | high | u02_0022_had_rtik_shaami.mp3 (shaami, 1.51s) | **shaami**; vowels added |
| u2_v09 | تَشَرَّفْنا | tasharrafnaa | Nice to meet you! (literally 'we have been honored') | phrase | high | u02_0023_tasharrafnaa_formal.mp3 (formal, 1.72s) | vowels added |
| u2_v09_shaami | تْشَرَّفْنا | tsharrafna | Nice to meet you! (Levantine) | phrase | high | u02_0023_tsharrafna_shaami.mp3 (shaami, 1.41s) | **shaami**; vowels added |
| u2_v10 | أَنْتَ | anta | you (to a male) | pronoun | high | u02_0024_anta_formal.mp3 (formal, 1.31s) | vowels added |
| u2_v10_shaami | إِنْتَ | inte | you (to a male; Levantine) | pronoun | high | u02_0024_inte_shaami.mp3 (shaami, 1.25s) | **shaami**; vowels added |
| u2_v11 | أَنْتِ | anti | you (to a female) | pronoun | high | u02_0025_anti_formal.mp3 (formal, 1.12s) | vowels added |
| u2_v11_shaami | إِنْتِ | inti | you (to a female; Levantine) | pronoun | high | u02_0025_inti_shaami.mp3 (shaami, 1.31s) | **shaami**; vowels added |
| u2_v13 | ـكَ / اِسْمُكَ | -ka / ismuka | your (to a male; suffix) / your name | suffix | high | u02_0026_ka_or_kismuka_formal.mp3 (formal, 3.03s) | vowels added |
| u2_v13_shaami | ـَك / اِسْمَك | -ak / ismak | your (to a male; suffix) / your name (Levantine) | suffix | high | u02_0026_akismak_shaami.mp3 (shaami, 2.82s) | **shaami**; vowels added |
| u2_v14 | ـكِ / اِسْمُكِ | -ki / ismuki | your (to a female; suffix) / your name | suffix | high | u02_0027_kiismuki_formal.mp3 (formal, 2.95s) | vowels added |
| u2_v14_shaami | ـِك / اِسْمِك | -ik / ismik | your (to a female; suffix) / your name (Levantine) | suffix | high | u02_0027_ikismik_shaami.mp3 (shaami, 2.69s) | **shaami**; vowels added |
| u2_v15 | أَيْنَ؟ | ayna? | where? | interrogative | high | u02_0028_ayna_formal.mp3 (formal, 1.1s) |  |
| u2_v15_shaami | وين؟ | ween? | where? (Levantine) | interrogative | high | u02_0028_ween_shaami.mp3 (shaami, 1.07s) | **shaami** |
| u2_v16 | مِن أَيْنَ؟ | min ayna? | from where? | interrogative | high | u02_0029_min_ayna_formal.mp3 (formal, 1.28s) |  |
| u2_v16_shaami | مِن وين؟ | min ween? | from where? (Levantine) | interrogative | high | u02_0029_min_ween_shaami.mp3 (shaami, 1.36s) | **shaami**; vowels added |
| u2_v17 | نَعَم | nacam | yes | particle | high | u02_0030_nacam_formal.mp3 (formal, 1.36s) |  |
| u2_v17_shaami | إيه | ee | yes (Levantine) | particle | high | u02_0030_ee_shaami.mp3 (shaami, 0.89s) | **shaami** |
| u2_v18 | لا | laa | no | particle | high | u02_0031_laa_formal.mp3 (formal, 1.36s)<br>u02_0031_la_laa_shaami.mp3 (shaami, 1.07s) |  |

## Unit 2 — Writing ا

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_alif | — | — | El-Shinnawi writes alif. | long_clip |  | u02_extra_618d24fe.wav (formal, 62.48s) | 62 s writing demo |

## Unit 2 — Writing ب

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_baa | — | — | El-Shinnawi writes baa. | long_clip |  | u02_extra_1f3117ea.wav (formal, 231.66s) | 232 s writing demo |

## Unit 2 — Writing ت

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_taa | — | — | El-Shinnawi writes taa (publisher file is oddly named ABU2LE3.mp4). | long_clip |  | u02_extra_5fbb4784.wav (formal, 158.19s) | 158 s writing demo |

## Unit 2 — Writing ث

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_thaa | — | — | El-Shinnawi writes thaa. | long_clip |  | u02_extra_4c1ddaa4.wav (formal, 191.61s) | 192 s writing demo |

## Unit 2 — Writing ـَـ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_fatha | — | — | El-Shinnawi writes fatHa. | long_clip |  | u02_extra_de196f61.wav (formal, 12.98s) | 13 s writing demo |

## Unit 2 — Writing ـُـ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_damma | — | — | El-Shinnawi writes Damma (short clip, still a demo, not a word). | long_clip |  | u02_extra_33def406.wav (formal, 9.91s) | 10 s writing demo |

## Unit 2 — Writing ـِـ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_kasra | — | — | El-Shinnawi writes kasra. | long_clip |  | u02_extra_2c57693e.wav (formal, 12.1s) | 12 s writing demo |

## Unit 2 — Writing و

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_waaw | — | — | El-Shinnawi writes waaw. | long_clip |  | u02_extra_f807f722.wav (formal, 52.2s) | 52 s writing demo |

## Unit 2 — Writing ي

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u2_writing_yaa | — | — | El-Shinnawi writes yaa. | long_clip |  | u02_extra_d10ae207.wav (formal, 172.61s) | 173 s writing demo |

## Unit 3 — Listening Exercise 1  ·  _Regional variation of ج (j / zh / g)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le1_01 | تاج | taaj | crown | noun | high | u03_extra_d2f78e95.mp3 (mixed (j / zh / Egyptian g), 4.8s) | clip has Egyptian g variant |
| u3_le1_02 | جُبّ | jubb | well, pit (like the well Joseph was thrown into) | noun | med | u03_extra_43ad77c0.mp3 (mixed (j / zh / Egyptian g), 4.18s) | vowels added; clip has Egyptian g variant |
| u3_le1_03 | تُجيب | tujiib | she answers; you (m.) answer | verb | high | u03_extra_02ee14c7.mp3 (mixed (j / zh / Egyptian g), 4.92s) | clip has Egyptian g variant |
| u3_le1_04 | دَجاج | dajaaj | chicken (collective — one hen is دَجاجة) | noun | high | u03_extra_faaf141f.mp3 (mixed (j / zh / Egyptian g), 4.99s) | clip has Egyptian g variant |

## Unit 3 — Listening Exercise 2  ·  _Pronouncing ح in various positions_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le2_01 | حَبيب | Habiib | beloved, darling, dear | noun | high | u03_extra_205d3b70.mp3 (formal, 2.77s) |  |
| u3_le2_02 | بَحْث | baHth | research; search | noun | high | u03_extra_0f9a4213.mp3 (formal, 1.94s) | vowels added |
| u3_le2_03 | تَبوح | tabuuH | she reveals (a secret); you (m.) reveal | verb | med | u03_extra_fe788319.mp3 (formal, 2.11s) |  |
| u3_le2_04 | صَباح | SabaaH | morning | noun | high | u03_extra_331ef59a.mp3 (formal, 2.31s) |  |

## Unit 3 — Listening Exercise 3  ·  _Pronouncing خ_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le3_01 | خاب | khaab | he failed; he was disappointed | verb | med | u03_extra_2c3a9759.mp3 (formal, 1.54s) |  |
| u3_le3_02 | بَخيل | bakhiil | stingy; a miser | adjective | high | u03_extra_9c172d95.mp3 (formal, 1.57s) |  |
| u3_le3_03 | باخ | baakh | it went stale, lost its flavor; (heat) died down | verb | low | u03_extra_c161fcee.mp3 (formal, 1.51s) |  |
| u3_le3_04 | بَخْت | bakht | luck, fortune | noun | high | u03_extra_ed48189b.mp3 (formal, 1.28s) | vowels added |
| u3_le3_05 | تَخْتي | takhtii | my bed | noun | high | u03_extra_09e07400.mp3 (formal, 1.62s) | vowels added |

## Unit 3 — Listening Exercise 4  ·  _Reading sukuun_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le4_01 | تَحْتَجْ | taHtaj | (you/she) need — short form, as in لَمْ تَحْتَجْ 'you did not need' | verb | low | u03_extra_792e2c04.mp3 (formal, 3.05s) |  |
| u3_le4_02 | تَخْتي | takhtii | my bed | noun | high | u03_extra_61a50d45.mp3 (formal, 2.31s) |  |
| u3_le4_03 | تَحْجُبُ | taHjubu | she hides, veils; you (m.) hide | verb | high | u03_extra_8a8a4ed1.mp3 (formal, 2.3s) |  |
| u3_le4_04 | تُثْبِتي | tuthbitii | (that) you (f.) prove / confirm | verb | med | u03_extra_583cd08b.mp3 (formal, 2.3s) |  |
| u3_le4_05 | بَحْثي | baHthii | my research | noun | high | u03_extra_885a474c.mp3 (formal, 2.31s) |  |

## Unit 3 — Listening Exercise 5  ·  _Consonant و (w)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le5_01 | وَثَب | wathab | he jumped, leaped | verb | high | u03_extra_91914b5e.mp3 (formal, 1.2s) |  |
| u3_le5_02 | واجِب | waajib | homework; duty | noun | high | u03_extra_089c4105.mp3 (formal, 1.46s) |  |
| u3_le5_03 | جَواب | jawaab | answer, reply | noun | high | u03_extra_cb544192.mp3 (formal, 1.46s) |  |
| u3_le5_04 | حِوار | Hiwaar | dialogue, conversation | noun | high | u03_extra_5bc5bed8.mp3 (formal, 1.67s) |  |
| u3_le5_05 | خاوي | khaawii | empty (spoken form of formal خاوٍ) | adjective | med | u03_extra_553e9cb9.mp3 (formal, 1.93s) |  |

## Unit 3 — Listening Exercise 6  ·  _Diphthong aw (ـَوْ)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le6_01 | ثَوْب | thawb | garment, robe | noun | high | u03_extra_ba1825f3.mp3 (formal, 1.62s) |  |
| u3_le6_02 | زَوْج | zawj | husband; pair | noun | high | u03_extra_2bb90971.mp3 (formal, 1.44s) |  |
| u3_le6_03 | تَوْبيخ | tawbiikh | scolding, reprimand | noun | high | u03_extra_f64d92fa.mp3 (formal, 1.85s) |  |
| u3_le6_04 | خَوْخ | khawkh | peaches (collective — one peach is خَوْخة) | noun | high | u03_extra_5ae376a5.mp3 (formal, 1.28s) |  |
| u3_le6_05 | حَوْل | Hawl | around; about | preposition | high | u03_extra_e206756f.mp3 (formal, 1.88s) |  |

## Unit 3 — Listening Exercise 7  ·  _Consonant ي (y)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le7_01 | بُيوت | buyuut | houses (plural of بَيْت) | noun | high | u03_extra_915d9da4.mp3 (formal, 2.07s) |  |
| u3_le7_02 | ثِياب | thiyaab | clothes (plural of ثَوْب) | noun | high | u03_extra_d8fefc8d.mp3 (formal, 1.92s) |  |
| u3_le7_03 | جُيوب | juyuub | pockets (plural of جَيْب) | noun | high | u03_extra_9fd5da59.mp3 (formal, 2.07s) |  |
| u3_le7_04 | يَجِب | yajib | it is necessary; (one) must | verb | high | u03_extra_b14cea0b.mp3 (formal, 1.54s) |  |
| u3_le7_05 | يَثوب | yathuub | he returns, comes back (to his senses) | verb | med | u03_extra_57b8fafc.mp3 (formal, 2.06s) |  |

## Unit 3 — Listening Exercise 8  ·  _Diphthong ay (ـَيْ)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_le8_01 | حَيْث | Hayth | where (as in 'the place where'); since, because | adverb | med | u03_extra_69381eb8.mp3 (formal, 2.31s) |  |
| u3_le8_02 | خَيْر | khayr | good; goodness, well-being | noun | high | u03_extra_ae4d02d2.mp3 (formal, 2.3s) |  |
| u3_le8_03 | جَيْب | jayb | pocket | noun | high | u03_extra_b0221b24.mp3 (formal, 2.6s) |  |
| u3_le8_04 | بَيْت | bayt | house | noun | high | u03_extra_9c6bcb4a.mp3 (formal, 2.59s) |  |
| u3_le8_05 | بَيْن | bayn | between | preposition | high | u03_extra_18a3546c.mp3 (formal, 2.59s) |  |

## Unit 3 — Drill 1  ·  _Dictation (ج) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d1_01 | جاب | jaab | he roamed, crossed (formal جابَ); in spoken Arabic 'he brought' | verb | med | u03_extra_e08d607b.wav (formal, 1.79s) |  |
| u3_d1_02 | تاج | taaj | crown | noun | high | u03_extra_d8f0686f.wav (formal, 1.98s) |  |
| u3_d1_03 | جوبي | juubii | roam! explore! (said to a female) | verb | low | u03_extra_542e8e38.wav (formal, 1.75s) |  |
| u3_d1_04 | جُبَب | jubab | robes, cloaks (plural of جُبّة jubba) | noun | med | u03_extra_9c30ace1.wav (formal, 1.69s) |  |
| u3_d1_05 | جُثَث | juthath | corpses, dead bodies (plural of جُثّة) | noun | high | u03_extra_ff84bbcd.wav (formal, 1.69s) |  |
| u3_d1_06 | جيب | jiib | spoken Arabic 'bring!' (to a male) — or jayb 'pocket' if the clip has the diphthong | verb | low | u03_extra_83fa53fe.wav (formal, 1.26s) |  |

## Unit 3 — Drill 2  ·  _Dictation (ح) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d2_01 | حوت | Huut | whale | noun | high | u03_extra_c0a8e9f0.wav (formal, 2.22s) |  |
| u3_d2_02 | بَحْث | baHth | research; search | noun | high | u03_extra_2cc3e716.wav (formal, 2.09s) | vowels added |
| u3_d2_03 | حَبيب | Habiib | beloved, darling, dear | noun | high | u03_extra_3706c0d8.wav (formal, 2.26s) |  |
| u3_d2_04 | تَحْت | taHt | under, below | preposition | high | u03_extra_2b280226.wav (formal, 1.98s) | vowels added |
| u3_d2_05 | بوحي | buuHii | reveal it! tell! (said to a female) | verb | med | u03_extra_f73d72f7.wav (formal, 2.92s) |  |
| u3_d2_06 | باحَت | baaHat | she revealed (a secret) | verb | med | u03_extra_e9a8b3ba.wav (formal, 2.73s) |  |

## Unit 3 — Drill 4  ·  _Letter connection — listen and write in the short vowels_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d4_01 | خابَت | khaabat | she failed; she was disappointed | verb | high | u03_extra_02f2d3d6.mp3 (formal, 3.31s) |  |
| u3_d4_02 | حِجاب | Hijaab | headscarf, veil | noun | high | u03_extra_2115a5ec.mp3 (formal, 3.31s) |  |
| u3_d4_03 | حَبيب | Habiib | beloved, darling, dear | noun | high | u03_extra_f45a62be.mp3 (formal, 2.83s) |  |
| u3_d4_04 | تُخوت | tukhuut | beds (plural of تَخْت) | noun | med | u03_extra_a02f1d02.mp3 (formal, 2.83s) |  |
| u3_d4_05 | تَجوب | tajuub | she roams, travels through; you (m.) roam | verb | med | u03_extra_0d20d6b8.mp3 (formal, 2.86s) |  |
| u3_d4_06 | بُحوث | buHuuth | research studies, papers (plural of بَحْث) | noun | high | u03_extra_02c2c132.mp3 (formal, 2.71s) |  |
| u3_d4_07 | تَبوحي | tabuuHii | (that) you (f.) reveal (a secret) | verb | med | u03_extra_9c52118a.mp3 (formal, 3.26s) |  |
| u3_d4_08 | حَجَبَت | Hajabat | she hid, veiled, blocked | verb | high | u03_extra_5d814705.mp3 (formal, 3.05s) |  |

## Unit 3 — Drill 5  ·  _Dictation (ج ح خ) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d5_01 | حَجَبَ | Hajaba | he hid, veiled, blocked | verb | high | u03_extra_2f50ff92.wav (formal, 1.9s) |  |
| u3_d5_02 | باخ | baakh | it went stale, lost its flavor; (heat) died down | verb | low | u03_extra_7b1079dd.wav (formal, 2.13s) |  |
| u3_d5_03 | تَخْتي | takhtii | my bed | noun | high | u03_extra_728d534a.wav (formal, 2.58s) | vowels added |
| u3_d5_04 | حاجّ | Haajj | pilgrim (someone who has made the Hajj) | noun | high | u03_extra_2d5e1d96.wav (formal, 2.15s) | vowels added |
| u3_d5_05 | باحِث | baaHith | researcher | noun | high | u03_extra_e2c6a003.wav (formal, 2.13s) |  |
| u3_d5_06 | جابَت | jaabat | she roamed, crossed (formal); in spoken Arabic 'she brought' | verb | med | u03_extra_c1e8820c.wav (formal, 2.22s) |  |

## Unit 3 — Drill 6  ·  _Reading aloud — vowel length, ح and خ_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d6_01 | تَحْتاج | taHtaaj | she needs; you (m.) need | verb | high | u03_extra_6becee96.mp3 (formal, 1.72s) | vowels added |
| u3_d6_02 | جابي | jaabii | collector (of taxes or fees) | noun | low | u03_extra_adf8cca0.mp3 (formal, 1.78s) |  |
| u3_d6_03 | حَجّ | Hajj | the Hajj (pilgrimage to Mecca) | noun | high | u03_extra_5d158c7d.mp3 (formal, 0.97s) | vowels added |
| u3_d6_04 | حِجاب | Hijaab | headscarf, veil | noun | high | u03_extra_ea632183.mp3 (formal, 1.8s) |  |
| u3_d6_05 | جُبَب | jubab | robes, cloaks (plural of جُبّة jubba) | noun | med | u03_extra_f5c8d0db.mp3 (formal, 1.46s) |  |
| u3_d6_06 | حاجّ | Haajj | pilgrim (someone who has made the Hajj) | noun | high | u03_extra_6129b354.mp3 (formal, 1.49s) | vowels added |
| u3_d6_07 | جابَت | jaabat | she roamed, crossed (formal); in spoken Arabic 'she brought' | verb | med | u03_extra_ec053625.mp3 (formal, 1.57s) |  |
| u3_d6_08 | خاب | khaab | he failed; he was disappointed | verb | med | u03_extra_fbc4466c.mp3 (formal, 1.41s) |  |
| u3_d6_09 | حُبّ | Hubb | love | noun | high | u03_extra_c130c83d.mp3 (formal, 1.12s) | vowels added |
| u3_d6_10 | باحِث | baaHith | researcher | noun | high | u03_extra_7bf0977e.mp3 (formal, 1.38s) |  |
| u3_d6_11 | تُجاب | tujaab | she/it is answered; you (m.) are answered (passive) | verb | low | u03_extra_47c0303b.mp3 (formal, 1.78s) |  |
| u3_d6_12 | بُحْ | buH | reveal it! (said to a male) | verb | low | u03_extra_ac2aa199.mp3 (formal, 1.07s) | vowels added |
| u3_d6_13 | جيبوتي | jiibuutii | Djibouti | place | high | u03_extra_21a212d7.mp3 (formal, 1.72s) |  |
| u3_d6_14 | تُخوت | tukhuut | beds (plural of تَخْت) | noun | med | u03_extra_605cfad4.mp3 (formal, 1.46s) |  |
| u3_d6_15 | خوجا | khuujaa | khawaja / hodja — an old title for a teacher or a (foreign) gentleman | noun | low | u03_extra_bca22f98.mp3 (formal, 1.7s) |  |

## Unit 3 — Drill 7  ·  _Dictation (aw) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d7_01 | خَوْخ | khawkh | peaches (collective — one peach is خَوْخة) | noun | high | u03_extra_205a2044.wav (formal, 1.43s) |  |
| u3_d7_02 | تَبْويب | tabwiib | arranging into chapters/sections; tabulation | noun | med | u03_extra_27a9d83f.wav (formal, 1.92s) |  |
| u3_d7_03 | جَواب | jawaab | answer, reply | noun | high | u03_extra_16483a05.wav (formal, 1.98s) |  |
| u3_d7_04 | ثَواب | thawaab | reward (especially God's reward for good deeds) | noun | high | u03_extra_03bc4220.wav (formal, 1.96s) |  |

## Unit 3 — Drill 8  ·  _Dictation with vowels and sukuun — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d8_01 | ثِياب | thiyaab | clothes (plural of ثَوْب) | noun | high | u03_extra_8a6a884a.wav (formal, 2.5s) |  |
| u3_d8_02 | حَياتي | Hayaatii | my life | noun | high | u03_extra_18a4403d.wav (formal, 3.03s) |  |
| u3_d8_03 | جُيوبي | juyuubii | my pockets | noun | high | u03_extra_3c99f6e7.wav (formal, 2.9s) |  |
| u3_d8_04 | يَحْجُب | yaHjub | he hides, veils, blocks | verb | high | u03_extra_ab764fa5.wav (formal, 2.2s) |  |

## Unit 3 — Drill 9  ·  _Reading aloud — check your pronunciation_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d9_01 | يَخْت | yakht | yacht | noun | high | u03_extra_3570ba2c.mp3 (formal, 1.36s) |  |
| u3_d9_02 | ثِيابي | thiyaabii | my clothes | noun | high | u03_extra_f0180763.mp3 (formal, 1.75s) |  |
| u3_d9_03 | واجِبات | waajibaat | homework assignments; duties (plural of واجِب) | noun | high | u03_extra_322bb8e1.mp3 (formal, 1.91s) |  |
| u3_d9_04 | حَبيبي | Habiibii | my darling, my dear (to a male) | noun | high | u03_extra_ee8b3e91.mp3 (formal, 1.8s) |  |
| u3_d9_05 | حَبيبَتي | Habiibatii | my darling, my dear (to a female) | noun | high | u03_extra_a0f0df6d.mp3 (formal, 1.93s) |  |
| u3_d9_06 | حَيْث | Hayth | where (as in 'the place where'); since, because | adverb | med | u03_extra_2fda9c3d.mp3 (formal, 1.2s) |  |
| u3_d9_07 | ثَواب | thawaab | reward (especially God's reward for good deeds) | noun | high | u03_extra_3e9c133c.mp3 (formal, 1.62s) |  |
| u3_d9_08 | جَيْبي | jaybii | my pocket | noun | high | u03_extra_976097c8.mp3 (formal, 1.67s) |  |
| u3_d9_09 | جُيوب | juyuub | pockets (plural of جَيْب) | noun | high | u03_extra_0dfffe94.mp3 (formal, 1.59s) |  |
| u3_d9_10 | تَبوحي | tabuuHii | (that) you (f.) reveal (a secret) | verb | med | u03_extra_c0411424.mp3 (formal, 1.7s) |  |
| u3_d9_11 | بَحْث | baHth | research; search | noun | high | u03_extra_023093e2.mp3 (formal, 1.33s) |  |
| u3_d9_12 | بَيْتي | baytii | my house | noun | high | u03_extra_746c0607.mp3 (formal, 1.7s) | vowels added |
| u3_d9_13 | بُيوت | buyuut | houses (plural of بَيْت) | noun | high | u03_extra_8f1e50bf.mp3 (formal, 1.72s) |  |
| u3_d9_14 | وُجوب | wujuub | necessity, obligation | noun | high | u03_extra_dac27994.mp3 (formal, 1.78s) |  |
| u3_d9_15 | تُجيبي | tujiibii | (that) you (f.) answer | verb | med | u03_extra_a69fb045.mp3 (formal, 1.75s) |  |
| u3_d9_16 | خابَ | khaaba | he failed; he was disappointed | verb | high | u03_extra_7deda868.mp3 (formal, 1.2s) |  |
| u3_d9_17 | يَجِب | yajib | it is necessary; (one) must | verb | high | u03_extra_b6cc8c88.mp3 (formal, 1.23s) |  |
| u3_d9_18 | جُثَث | juthath | corpses, dead bodies (plural of جُثّة) | noun | high | u03_extra_f138dfad.mp3 (formal, 1.25s) |  |
| u3_d9_19 | جَواب | jawaab | answer, reply | noun | high | u03_extra_a2985dc4.mp3 (formal, 1.54s) |  |
| u3_d9_20 | جَوابات | jawaabaat | answers; (in spoken Arabic) letters (plural of جَواب) | noun | med | u03_extra_c956a285.mp3 (formal, 2.19s) |  |

## Unit 3 — Drill 10  ·  _Letter connection — listen and write in the short vowels_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d10_01 | جابَت | jaabat | she roamed, crossed (formal); in spoken Arabic 'she brought' | verb | med | u03_extra_5f83f5f3.mp3 (formal, 1.67s) |  |
| u3_d10_02 | حُجُب | Hujub | veils, screens, curtains (plural of حِجاب) | noun | med | u03_extra_85b8bab2.mp3 (formal, 1.59s) |  |
| u3_d10_03 | خَوْخ | khawkh | peaches (collective — one peach is خَوْخة) | noun | high | u03_extra_302b4b6e.mp3 (formal, 1.57s) |  |
| u3_d10_04 | ثِيابي | thiyaabii | my clothes | noun | high | u03_extra_436a5112.mp3 (formal, 1.8s) |  |
| u3_d10_05 | جيبوتي | jiibuutii | Djibouti | place | high | u03_extra_ddc76422.mp3 (formal, 1.91s) |  |
| u3_d10_06 | حَبيبَتي | Habiibatii | my darling, my dear (to a female) | noun | high | u03_extra_6235a486.mp3 (formal, 2.14s) |  |
| u3_d10_07 | بُحوث | buHuuth | research studies, papers (plural of بَحْث) | noun | high | u03_extra_e0ea10d4.mp3 (formal, 1.72s) |  |
| u3_d10_08 | واجِبات | waajibaat | homework assignments; duties (plural of واجِب) | noun | high | u03_extra_cab9503c.mp3 (formal, 2.43s) |  |
| u3_d10_09 | بُيوت | buyuut | houses (plural of بَيْت) | noun | high | u03_extra_d9284cc9.mp3 (formal, 1.51s) |  |
| u3_d10_10 | جُيوب | juyuub | pockets (plural of جَيْب) | noun | high | u03_extra_a0e97267.mp3 (formal, 1.62s) |  |

## Unit 3 — Drill 11  ·  _Dictation — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d11_01 | واجِب | waajib | homework; duty | noun | high | u03_extra_c086caf5.wav (formal, 2.26s) |  |
| u3_d11_02 | بَيْتي | baytii | my house | noun | high | u03_extra_b23333ec.wav (formal, 2.26s) |  |
| u3_d11_03 | يَبوح | yabuuH | he reveals (a secret) | verb | med | u03_extra_dab9c1d7.wav (formal, 1.49s) |  |
| u3_d11_04 | يَخيب | yakhiib | he fails; he is disappointed | verb | med | u03_extra_ddfeaaa7.wav (formal, 2.05s) |  |
| u3_d11_05 | يَحْجُب | yaHjub | he hides, veils, blocks | verb | high | u03_extra_5cb65d33.wav (formal, 2.37s) |  |
| u3_d11_06 | تَحْتاج | taHtaaj | she needs; you (m.) need | verb | high | u03_extra_b93af1a7.wav (formal, 1.69s) |  |

## Unit 3 — Drill 15

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_d15_scene3a_levantine | — | — | Scene 3A, Levantine version: 'kiifik?'. | long_clip |  | u03_extra_89f203cc.wav (shaami, 28.29s) | **shaami**; 28 s dialogue scene |
| u3_d15_scene3b_levantine | — | — | Scene 3B, Levantine version: 'SabaaH l-kheer'. | long_clip |  | u03_extra_fd57795c.wav (shaami, 21.31s) | **shaami**; 21 s dialogue scene |

## Unit 3 — New Vocabulary  ·  _New Vocabulary: Greetings and daily expressions_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_v01 | وَ | wa | and | particle | high | u03_0032_and_formal.mp3 (formal, 1.45s)<br>u03_0032_and_shaami.mp3 (shaami, 0.8s) |  |
| u3_v02 | حِجاب | Hijaab | headscarf, veil (head covering) | noun | high | u03_0033_veil_head_covering_formal.mp3 (formal, 2.13s)<br>u03_0033_veil_head_covering_shaami.mp3 (shaami, 1.22s) |  |
| u3_v03 | بَيْت | bayt | house | noun | high | u03_0034_house_formal.mp3 (formal, 1.31s)<br>u03_0034_house_shaami.mp3 (shaami, 1.18s) |  |
| u3_v04 | شارِع | shaaric | street | noun | high | u03_0035_shaaric_formal.mp3 (formal, 1.46s)<br>u03_0035_shaaric_shaami.mp3 (shaami, 1.44s) |  |
| u3_v05 | واجِب | waajib | homework (also: duty) | noun | high | u03_0036_homework_formal.mp3 (formal, 1.38s) |  |
| u3_v05_shaami | وَظيفة | waZiife | homework (Levantine) | noun | high | u03_0036_waziife_shaami.mp3 (shaami, 1.62s) | **shaami** |
| u3_v06 | أَخْبار | akhbaar | news (plural of خَبَر, a piece of news) | noun | high | u03_0037_akhbaar_formal.mp3 (formal, 1.49s)<br>u03_0037_akhbaar_shaami.mp3 (shaami, 1.59s) |  |
| u3_v07 | كِتاب | kitaab | book | noun | high | u03_0038_kitaab_formal.mp3 (formal, 1.54s)<br>u03_0038_kitaab_shaami.mp3 (shaami, 1.31s) |  |
| u3_v08 | حَبيبي | Habiibii | my darling, my dear (to a male; also used with children, parents, close friends) | noun | high | u03_0039_my_male_dear_darling_formal.mp3 (formal, 1.67s)<br>u03_0039_my_male_dear_darling_shaami.mp3 (shaami, 1.41s) |  |
| u3_v09 | حَبيبَتي | Habiibatii | my darling, my dear (to a female) | noun | high | u03_0040_my_female_dear_darling_formal.mp3 (formal, 1.78s)<br>u03_0040_my_female_dear_darling_shaami.mp3 (shaami, 1.57s) |  |
| u3_v10 | صَباح الخَيْر | SabaaH al-khayr | Good morning! | phrase | high | u03_0041_sabaah_al_khayr_formal.mp3 (formal, 1.7s) | vowels added |
| u3_v10_shaami | صَباح الخير | SabaaH il-kheer | Good morning! (Levantine) | phrase | high | u03_0041_sabaah_il_kheer_shaami.mp3 (shaami, 1.91s) | **shaami**; vowels added |
| u3_v11 | صَباح النّور | SabaaH an-nuur | Good morning! (reply) — literally 'morning of light' | phrase | high | u03_0042_sabaah_an_nuur_formal.mp3 (formal, 1.57s) |  |
| u3_v11_shaami | صَباح النّور | SabaaH in-nuur | Good morning! (reply; Levantine) | phrase | high | u03_0042_sabaah_shaami.mp3 (shaami, 1.59s) | **shaami** |
| u3_v12 | يا … | yaa … | O …! — put before a name when calling or addressing someone directly (yaa Ahmad) | particle | high | u03_0043_signal_that_you_are_addressi_formal.mp3 (formal, 1.59s)<br>u03_0043_signal_that_you_are_addressi_shaami.mp3 (shaami, 1.12s) |  |
| u3_v13 | كَيْفَ؟ | kayfa? | how? | interrogative | high | u03_0044_kayfa_formal.mp3 (formal, 1.23s) |  |
| u3_v13_shaami | كيف؟ | kiif? | how? (Levantine) | interrogative | high | u03_0044_kiif_shaami.mp3 (shaami, 1.23s) | **shaami** |
| u3_v14 | كَيْفَ الحال؟ | kayfa al-Haal? | How are you? (literally 'how is the condition?') | phrase | high | u03_0045_kayf_al_haal_formal.mp3 (formal, 1.54s) |  |
| u3_v14_shaami | كيفَك؟ / كيفِك؟ | kiifak? / kiifik? | How are you? (to a male / to a female; Levantine) | phrase | high | u03_0045_kiifak_ik_shaami.mp3 (shaami, 3.34s) | **shaami**; vowels added |
| u3_v15 | الحَمْدُ لِلّه | al-Hamdu lillaah | Praise be to God — the reply to 'How are you?' (fine, thank God) | phrase | high | u03_0046_al_hamdu_lillaah_formal.mp3 (formal, 1.67s) | vowels added |
| u3_v15_shaami | الحَمْدُ لِلّه | il-Hamdilla | Thank God (reply to 'How are you?'; Levantine pronunciation) | phrase | high | u03_0046_il_hamdilla_shaami.mp3 (shaami, 1.36s) | **shaami**; vowels added |
| u3_v16 | جَيِّد | jayyid | good, fine | adjective | high | u03_0047_jayyid_formal.mp3 (formal, 1.15s) | vowels added |
| u3_v16_shaami | تَمام | tamaam | great, fine (Levantine) | adjective | high | u03_0047_tamaam_shaami.mp3 (shaami, 1.46s) | **shaami** |
| u3_v17 | ماشي | maashi | OK (Levantine) | particle | high | u03_0048_maashi_shaami.mp3 (shaami, 1.41s) | **shaami** |
| u3_v18 | هٰذا | haadhaa | this (masc.) | demonstrative | high | u03_0049_haadhaa_formal.mp3 (formal, 1.41s) |  |
| u3_v18_shaami | هَيدا | hayda (or haada) | this (masc.; Levantine) | demonstrative | med | u03_0049_haada_shaami.mp3 (shaami, 1.25s) | **shaami** |
| u3_v19 | هٰذِهِ | haadhihi | this (fem.) | demonstrative | high | u03_0050_haadhihi_formal.mp3 (formal, 1.38s) |  |
| u3_v19_shaami | هَيدي | haydi (or haadi) | this (fem.; Levantine) | demonstrative | med | u03_0050_haadi_shaami.mp3 (shaami, 1.36s) | **shaami** |
| u3_v20 | بِخَيْر | bi-khayr | fine, well (reply to 'kayfa al-Haal?') | phrase | high | u03_0051_bi_khayr_formal.mp3 (formal, 1.25s) | vowels added |
| u3_v20_shaami | مْنيح / مْنيحة | mniiH / mniiHa | good, fine (masc. / fem.; Levantine) | adjective | high | u03_0051_mniih_mniiha_shaami.mp3 (shaami, 2.61s) | **shaami**; vowels added |
| u3_v21 | لَيْسَ | laysa | is not / am not / are not (negating verb) | verb | high | u03_0052_laysa_formal.mp3 (formal, 1.2s) | vowels added |
| u3_v21_shaami | مو | muu | not (Levantine) | particle | high | u03_0052_muu_shaami.mp3 (shaami, 1.1s) | **shaami** |

## Unit 3 — Writing ج

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_writing_jiim | — | — | El-Shinnawi writes ج and similar letters. | long_clip |  | u03_extra_e0f17593.wav (formal, 218.43s) | 218 s writing demo |

## Unit 3 — Writing ح

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_writing_Haa | — | — | El-Shinnawi writes ح in the word حَبيب. | long_clip |  | u03_extra_e3742b68.wav (formal, 158.31s) | 158 s writing demo |

## Unit 3 — Writing خ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_writing_khaa | — | — | El-Shinnawi writes خ. | long_clip |  | u03_extra_e237cddb.wav (formal, 160.38s) | 160 s writing demo |

## Unit 3 — Writing ـْـ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u3_writing_sukuun | — | — | El-Shinnawi writes sukuun. | long_clip |  | u03_extra_749a6fcd.wav (formal, 19.77s) | 20 s writing demo |

## Unit 4 — Listening Exercise 1  ·  _Listening to and pronouncing hamza ء_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le1_01 | أَخَوات | akhawaat | sisters (plural of أُخْت) | noun | high | u04_extra_85a26f0e.mp3 (formal, 2.21s) | vowels added |
| u4_le1_02 | أَب | ab | father | noun | high | u04_extra_17fa4cd4.mp3 (formal, 1.32s) |  |
| u4_le1_03 | سَبَأ | saba' | Sheba (the ancient kingdom of Saba' in Yemen) | place | high | u04_extra_f6199f50.mp3 (formal, 1.56s) |  |
| u4_le1_04 | تَأْتَأ | ta'ta' | he stammered, stuttered | verb | med | u04_extra_a0942a0e.mp3 (formal, 1.78s) | vowels added |
| u4_le1_05 | بَأْس | ba's | harm (as in لا بَأْس 'no problem'); also might, courage | noun | high | u04_extra_61e8fe42.mp3 (formal, 1.59s) | vowels added |

## Unit 4 — Listening Exercise 2  ·  _Initial hamza with fatHa (أَ)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le2_01 | أَب | ab | father | noun | high | u04_extra_509a1077.mp3 (formal, 1.8s) |  |
| u4_le2_02 | أَتَت | atat | she came | verb | high | u04_extra_d06409fd.mp3 (formal, 1.32s) |  |
| u4_le2_03 | أَخ | akh | brother | noun | high | u04_extra_b0896b5e.mp3 (formal, 1.39s) |  |
| u4_le2_04 | أَخَوات | akhawaat | sisters (plural of أُخْت) | noun | high | u04_extra_7ee63ef0.mp3 (formal, 2.06s) |  |
| u4_le2_05 | أَثاث | athaath | furniture | noun | high | u04_extra_b6c8f146.mp3 (formal, 1.73s) |  |

## Unit 4 — Listening Exercise 3  ·  _Initial hamza with Damma (أُ) and kasra (إِ)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le3_01 | إِبْحار | ibHaar | sailing, setting sail | noun | high | u04_extra_eb340eef.mp3 (formal, 2.07s) |  |
| u4_le3_02 | أُخْت | ukht | sister | noun | high | u04_extra_c5881e16.mp3 (formal, 1.33s) |  |
| u4_le3_03 | إِثْبات | ithbaat | proof, confirmation | noun | high | u04_extra_2e05347d.mp3 (formal, 2.06s) |  |
| u4_le3_04 | أُخْرِجَ | ukhrija | he was taken out, expelled (passive) | verb | med | u04_extra_7075a28b.mp3 (formal, 2.06s) |  |
| u4_le3_05 | إِخْبار | ikhbaar | informing; reporting news | noun | high | u04_extra_fbe917bb.mp3 (formal, 2.06s) |  |
| u4_le3_06 | أُثْبِتَ | uthbita | it was proven, confirmed (passive) | verb | med | u04_extra_ce719bb4.mp3 (formal, 2.07s) |  |

## Unit 4 — Listening Exercise 4  ·  _Final hamza — names of letters_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le4_01 | باء | baa' | the letter name baa (ب) | letter-name | high | u04_extra_fe8e9185.mp3 (formal, 1.79s) |  |
| u4_le4_02 | تاء | taa' | the letter name taa (ت) | letter-name | high | u04_extra_fd914648.mp3 (formal, 1.54s) |  |
| u4_le4_03 | ثاء | thaa' | the letter name thaa (ث) | letter-name | high | u04_extra_c8fa267f.mp3 (formal, 1.54s) |  |
| u4_le4_04 | حاء | Haa' | the letter name Haa (ح) | letter-name | high | u04_extra_316a41af.mp3 (formal, 1.54s) |  |
| u4_le4_05 | خاء | khaa' | the letter name khaa (خ) | letter-name | high | u04_extra_2a90c591.mp3 (formal, 1.54s) |  |

## Unit 4 — Listening Exercise 5  ·  _Recognizing and pronouncing د_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le5_01 | دَجاج | dajaaj | chicken (collective — one hen is دَجاجة) | noun | high | u04_extra_8f052c84.mp3 (formal, 2.07s) |  |
| u4_le5_02 | خُدود | khuduud | cheeks (plural of خَدّ) | noun | high | u04_extra_a8c9c9bc.mp3 (formal, 2.06s) |  |
| u4_le5_03 | حُدود | Huduud | borders, limits (plural of حَدّ) | noun | high | u04_extra_f0aa9d1a.mp3 (formal, 2.06s) |  |
| u4_le5_04 | جَديد | jadiid | new | adjective | high | u04_extra_48806d2b.mp3 (formal, 2.06s) |  |
| u4_le5_05 | أَدَب | adab | literature; good manners | noun | high | u04_extra_d4fde32e.mp3 (formal, 2.06s) |  |
| u4_le5_06 | أَحْداث | aHdaath | events (plural of حَدَث) | noun | high | u04_extra_0d3aaa62.mp3 (formal, 2.07s) | vowels added |

## Unit 4 — Listening Exercise 6  ·  _Reading and pronouncing ذ_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le6_01 | ذُباب | dhubaab | flies (the insects; collective — one fly is ذُبابة) | noun | high | u04_extra_7d4cdae7.mp3 (formal, 1.66s) |  |
| u4_le6_02 | ذات | dhaat | self; essence | noun | med | u04_extra_913931f0.mp3 (formal, 1.66s) |  |
| u4_le6_03 | بَذَرَ | badhara | he sowed (seeds) | verb | high | u04_extra_c1822a85.mp3 (formal, 1.66s) |  |
| u4_le6_04 | خُذ | khudh | take! (said to a male) | verb | high | u04_extra_ad36b699.mp3 (formal, 1.66s) |  |
| u4_le6_05 | حَذارِ | Hadhaari | beware! watch out! | particle | high | u04_extra_f0e647d8.mp3 (formal, 1.66s) |  |
| u4_le6_06 | تَذَبْذُب | tadhabdhub | fluctuation, wavering | noun | high | u04_extra_1d76a64f.mp3 (formal, 1.68s) |  |

## Unit 4 — Listening Exercise 7  ·  _Pronouncing ر (ر deepens alif and fatHa)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le7_01 | رَباب | rabaab | rebab (a bowed string instrument); also a woman's name | noun | med | u04_extra_ee0961b3.mp3 (formal, 2.06s) |  |
| u4_le7_02 | رُدود | ruduud | replies, responses (plural of رَدّ) | noun | high | u04_extra_2007aaf9.mp3 (formal, 1.99s) |  |
| u4_le7_03 | خَراج | kharaaj | land tax, tribute (historical) | noun | med | u04_extra_91067059.mp3 (formal, 1.99s) |  |
| u4_le7_04 | تَبْرير | tabriir | justification | noun | high | u04_extra_31df9606.mp3 (formal, 1.99s) |  |
| u4_le7_05 | جار | jaar | neighbor (m.) | noun | high | u04_extra_e204dd5b.mp3 (formal, 1.99s) |  |
| u4_le7_06 | وُرود | wuruud | roses, flowers (plural of وَرْد); also 'arrival' | noun | med | u04_extra_c820b369.mp3 (formal, 2.07s) |  |

## Unit 4 — Listening Exercise 8  ·  _Pronouncing ز_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_le8_01 | زَوْج | zawj | husband; pair | noun | high | u04_extra_702e478f.mp3 (formal, 1.63s) |  |
| u4_le8_02 | أَحْزاب | aHzaab | (political) parties (plural of حِزْب) | noun | high | u04_extra_1f736dcf.mp3 (formal, 1.63s) |  |
| u4_le8_03 | زُجاج | zujaaj | glass (the material) | noun | high | u04_extra_63a07412.mp3 (formal, 1.63s) |  |
| u4_le8_04 | يَزور | yazuur | he visits | verb | high | u04_extra_a0e89aa0.mp3 (formal, 1.64s) |  |
| u4_le8_05 | جَواز | jawaaz | passport (short for جَواز سَفَر); permission | noun | high | u04_extra_8d3eb449.mp3 (formal, 1.63s) |  |
| u4_le8_06 | تَزيد | taziid | she/it increases; you (m.) increase | verb | high | u04_extra_189e678e.mp3 (formal, 1.64s) |  |

## Unit 4 — Drill 2  ·  _Dictation (hamza) — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d2_01 | ثاء | thaa' | the letter name thaa (ث) | letter-name | high | u04_extra_ecd5fb06.wav (formal, 1.73s) |  |
| u4_d2_02 | أَب | ab | father | noun | high | u04_extra_1a2c1aad.wav (formal, 1.39s) |  |
| u4_d2_03 | أَثاث | athaath | furniture | noun | high | u04_extra_47049faf.wav (formal, 1.92s) |  |
| u4_d2_04 | أَخي | akhii | my brother | noun | high | u04_extra_f959f65c.wav (formal, 1.98s) |  |
| u4_d2_05 | باء | baa' | the letter name baa (ب) | letter-name | high | u04_extra_2dcfc0af.wav (formal, 1.73s) |  |
| u4_d2_06 | أَتَت | atat | she came | verb | high | u04_extra_177d586b.wav (formal, 1.96s) |  |

## Unit 4 — Drill 4

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d4_scene4a_levantine | — | — | Scene 4A, Levantine version: 'kiifak?'. | long_clip |  | u04_extra_77649ac5.wav (shaami, 37.84s) | **shaami**; 38 s dialogue scene |
| u4_d4_scene4b_levantine | — | — | Scene 4B, Levantine version: 'l-Hamdilla'. | long_clip |  | u04_extra_6d19ec1c.wav (shaami, 44.63s) | **shaami**; 45 s dialogue scene |

## Unit 4 — Drill 6  ·  _Pronouncing ذ vs ث — read aloud, then check with the audio_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d6_01 | ذابَ | dhaaba | it melted, dissolved | verb | high | u04_extra_64245b46.mp3 (formal, 3.32s) |  |
| u4_d6_02 | ثابَ | thaaba | he returned, came back (to his senses) | verb | med | u04_extra_32fda0d5.mp3 (formal, 2.3s) |  |
| u4_d6_03 | ذُباب | dhubaab | flies (the insects; collective — one fly is ذُبابة) | noun | high | u04_extra_fbf5a2a1.mp3 (formal, 2.02s) |  |
| u4_d6_04 | ثَبات | thabaat | firmness, stability | noun | high | u04_extra_e82c4bde.mp3 (formal, 2.45s) |  |
| u4_d6_05 | ثَواب | thawaab | reward (especially God's reward for good deeds) | noun | high | u04_extra_31ee05c1.mp3 (formal, 2.4s) |  |
| u4_d6_06 | ذَوات | dhawaat | selves, beings (plural of ذات) | noun | med | u04_extra_120afdd2.mp3 (formal, 2.33s) |  |
| u4_d6_07 | جُثَث | juthath | corpses, dead bodies (plural of جُثّة) | noun | high | u04_extra_1bb892d7.mp3 (formal, 2.26s) |  |
| u4_d6_08 | جاذِب | jaadhib | attractive; attracting | adjective | high | u04_extra_e14329c9.mp3 (formal, 2.26s) |  |

## Unit 4 — Drill 9  ·  _Letter connection — listen and write in the short vowels_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d9_01 | رَذاذ | radhaadh | drizzle; fine spray | noun | high | u04_extra_e00f9145.mp3 (formal, 3.53s) |  |
| u4_d9_02 | خادِر | khaadir | drowsy, sluggish; (of a lion) in its den | adjective | low | u04_extra_c2f113d0.mp3 (formal, 2.59s) |  |
| u4_d9_03 | زَرَد | zarad | chain mail (armor) | noun | med | u04_extra_a59a45f7.mp3 (formal, 2.4s) |  |
| u4_d9_04 | حُروب | Huruub | wars (plural of حَرْب) | noun | high | u04_extra_f19dc439.mp3 (formal, 2.33s) |  |
| u4_d9_05 | رَجاء | rajaa' | hope; request; 'please' | noun | high | u04_extra_d5dd228c.mp3 (formal, 2.57s) |  |
| u4_d9_06 | بِحار | biHaar | seas (plural of بَحْر) | noun | high | u04_extra_b1a50ef3.mp3 (formal, 2.04s) |  |
| u4_d9_07 | أَزْواج | azwaaj | husbands; couples, pairs (plural of زَوْج) | noun | high | u04_extra_9e40cdfc.mp3 (formal, 2.4s) |  |
| u4_d9_08 | حُدود | Huduud | borders, limits (plural of حَدّ) | noun | high | u04_extra_d5f41feb.mp3 (formal, 2.62s) |  |
| u4_d9_09 | رُدود | ruduud | replies, responses (plural of رَدّ) | noun | high | u04_extra_69a12c53.mp3 (formal, 2.78s) |  |
| u4_d9_10 | تَحْذير | taHdhiir | warning | noun | high | u04_extra_9e7b24a8.mp3 (formal, 2.71s) |  |
| u4_d9_11 | أَدْوار | adwaar | roles; turns; floors of a building (plural of دَوْر) | noun | high | u04_extra_19280e1a.mp3 (formal, 2.42s) |  |
| u4_d9_12 | يَخْرُج | yakhruj | he goes out, leaves | verb | high | u04_extra_59583a8d.mp3 (formal, 2.35s) |  |
| u4_d9_13 | تَجارِب | tajaarib | experiments; experiences (plural of تَجْرِبة) | noun | high | u04_extra_e1e8342c.mp3 (formal, 2.59s) |  |
| u4_d9_14 | ذَبَحَت | dhabaHat | she slaughtered | verb | high | u04_extra_e8c84662.mp3 (formal, 2.81s) |  |

## Unit 4 — Drill 10  ·  _Dictation — video_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d10_01 | أُخْت | ukht | sister | noun | high | u04_extra_ec54d25f.wav (formal, 1.79s) |  |
| u4_d10_02 | أَبي | abii | my father | noun | high | u04_extra_db61f4f2.wav (formal, 1.98s) |  |
| u4_d10_03 | واحِد | waaHid | one | number | high | u04_extra_04e5f193.wav (formal, 2.5s) |  |
| u4_d10_04 | زَوْجات | zawjaat | wives (plural of زَوْجة) | noun | high | u04_extra_f772c6a6.wav (formal, 2.2s) |  |
| u4_d10_05 | ذُباب | dhubaab | flies (the insects; collective — one fly is ذُبابة) | noun | high | u04_extra_764cd1bf.wav (formal, 2.15s) |  |
| u4_d10_06 | دَجاج | dajaaj | chicken (collective — one hen is دَجاجة) | noun | high | u04_extra_8119fad2.wav (formal, 2.45s) |  |
| u4_d10_07 | أَزْرار | azraar | buttons (plural of زِرّ) | noun | high | u04_extra_96fe3f6a.wav (formal, 1.96s) |  |
| u4_d10_08 | رَباب | rabaab | rebab (a bowed string instrument); also a woman's name | noun | med | u04_extra_83e0a3bd.wav (formal, 1.79s) |  |
| u4_d10_09 | يُريد | yuriid | he wants | verb | high | u04_extra_f3f5c9dc.wav (formal, 2.43s) |  |
| u4_d10_10 | أَحْزاب | aHzaab | (political) parties (plural of حِزْب) | noun | high | u04_extra_7861b9d6.wav (formal, 2.56s) |  |

## Unit 4 — Drill 18

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_d18_scene4c_levantine | — | — | Scene 4C, Levantine version ('tsharrafna'). Same office set as the Levantine Scene 2 video. | long_clip |  | u04_extra_d00e502a.wav (shaami, 50.64s) | **shaami**; 51 s dialogue scene |

## Unit 4 — Arabic Numerals  ·  _Numbers 0–10_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_num00 | صِفْر | Sifr | zero (0; Arabic-Indic numeral ٠) | number | high | u04_extra_2ea28a38.mp3 (formal, 1.49s)<br>u04_extra_13889d2e.mp3 (shaami, 1.23s) |  |
| u4_num01 | واحِد | waaHid | one (1; Arabic-Indic numeral ١) | number | high | u04_extra_c4502005.mp3 (formal, 1.57s)<br>u04_extra_a679d43e.mp3 (shaami, 1.33s) |  |
| u4_num02 | اِثْنَيْن | ithnayn | two (2; Arabic-Indic numeral ٢) | number | high | u04_extra_bf64928c.mp3 (formal, 1.57s) |  |
| u4_num02_shaami | اتنين | tneen | two (2; Levantine) | number | high | u04_extra_cc38e78e.mp3 (shaami, 1.07s) | **shaami** |
| u4_num03 | ثَلاثة | thalaatha | three (3; Arabic-Indic numeral ٣) | number | high | u04_extra_76cce3bc.mp3 (formal, 1.57s) |  |
| u4_num03_shaami | تلاتة | tlaate | three (3; Levantine) | number | high | u04_extra_1bee60fc.mp3 (shaami, 1.15s) | **shaami** |
| u4_num04 | أَرْبَعة | arbaca | four (4; Arabic-Indic numeral ٤) | number | high | u04_extra_38165901.mp3 (formal, 1.51s)<br>u04_extra_ef16d49c.mp3 (shaami, 1.15s) |  |
| u4_num05 | خَمْسة | khamsa | five (5; Arabic-Indic numeral ٥) | number | high | u04_extra_2baff3fc.mp3 (formal, 1.49s) |  |
| u4_num05_shaami | خمسة | khamse | five (5; Levantine) | number | high | u04_extra_747f0e74.mp3 (shaami, 1.44s) | **shaami** |
| u4_num06 | سِتّة | sitta | six (6; Arabic-Indic numeral ٦) | number | high | u04_extra_807ddfa8.mp3 (formal, 1.57s) |  |
| u4_num06_shaami | سِتّة | sitte | six (6; Levantine) | number | high | u04_extra_ea19f740.mp3 (shaami, 1.38s) | **shaami** |
| u4_num07 | سَبْعة | sabca | seven (7; Arabic-Indic numeral ٧) | number | high | u04_extra_dc351f44.mp3 (formal, 1.67s)<br>u04_extra_dc5ef6ff.mp3 (shaami, 1.38s) |  |
| u4_num08 | ثَمانِية | thamaaniya | eight (8; Arabic-Indic numeral ٨) | number | high | u04_extra_bd6fd2ef.mp3 (formal, 1.83s) |  |
| u4_num08_shaami | تمانية | tmaane | eight (8; Levantine) | number | high | u04_extra_a6428991.mp3 (shaami, 1.18s) | **shaami** |
| u4_num09 | تِسْعة | tisca | nine (9; Arabic-Indic numeral ٩) | number | high | u04_extra_27d2de1b.mp3 (formal, 1.41s)<br>u04_extra_2a6ef943.mp3 (shaami, 1.25s) |  |
| u4_num10 | عَشَرة | cashara | ten (10; Arabic-Indic numeral ١٠) | number | high | u04_extra_1bea90f7.mp3 (formal, 1.65s) |  |
| u4_num10_shaami | عَشَرة | cashra | ten (10; Levantine) | number | high | u04_extra_b549a2b0.mp3 (shaami, 1.31s) | **shaami** |

## Unit 4 — New Vocabulary 1  ·  _New Vocabulary 1: Introductions_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_v09 | تَفَضَّل | tafaDDal | Please come in / go ahead / here you are (to a male) | phrase | high | u04_0053_tafaddal_formal.mp3 (formal, 1.57s) | vowels added |
| u4_v09_shaami | تْفَضَّل | tfaDDal | Please come in / go ahead (to a male; Levantine) | phrase | high | u04_0053_tfaddal_shaami.mp3 (shaami, 1.44s) | **shaami**; vowels added |
| u4_v10 | تَفَضَّلي | tafaDDalii | Please come in / go ahead / here you are (to a female) | phrase | high | u04_0054_tafaddalii_formal.mp3 (formal, 1.51s) | vowels added |
| u4_v10_shaami | تْفَضّْلي | tfaDDli | Please come in / go ahead (to a female; Levantine) | phrase | high | u04_0054_tfaddli_shaami.mp3 (shaami, 1.33s) | **shaami**; vowels added |
| u4_v11 | تَفَضَّلوا | tafaDDaluu | Please come in / go ahead / here you are (to a group) | phrase | high | u04_0055_tafaddaluu_formal.mp3 (formal, 1.51s) | vowels added |
| u4_v11_shaami | تْفَضّْلوا | tfaDDlu | Please come in / go ahead (to a group; Levantine) | phrase | high | u04_0055_tfaddlu_shaami.mp3 (shaami, 1.31s) | **shaami**; vowels added |
| u4_v14 | صاحِبي | SaaHibii | my friend (m.); my boyfriend | noun | high | u04_0056_saahibii_formal.mp3 (formal, 1.57s) |  |
| u4_v14_shaami | صاحْبي / رْفيقي | SaaHbi / rfii'i | my friend (m.) — two Levantine words | noun | high | u04_0056_saahbi_rfii_i_shaami.mp3 (shaami, 3.0s) | **shaami**; vowels added |
| u4_v15 | صاحِبَتي | SaaHibatii | my friend (f.); my girlfriend | noun | high | u04_0057_saahibatii_formal.mp3 (formal, 1.67s) |  |
| u4_v15_shaami | صاحِبْتي / رْفيقْتي | SaaHibti / rfii'ti | my friend (f.) — two Levantine words | noun | high | u04_0057_saahibti_rfii_ti_shaami.mp3 (shaami, 3.29s) | **shaami**; vowels added |
| u4_v16 | هُوَ | huwa | he; it (masc.) | pronoun | high | u04_0058_huwa_formal.mp3 (formal, 1.31s) |  |
| u4_v16_shaami | هُوِّ | huwwe | he; it (masc.; Levantine) | pronoun | high | u04_0058_huwwe_shaami.mp3 (shaami, 1.33s) | **shaami**; vowels added |
| u4_v17 | هِيَ | hiya | she; it (fem.) | pronoun | high | u04_0059_hiya_formal.mp3 (formal, 1.31s) |  |
| u4_v17_shaami | هِيِّ | hiyye | she; it (fem.; Levantine) | pronoun | high | u04_0059_hiyye_shaami.mp3 (shaami, 1.04s) | **shaami**; vowels added |
| u4_v18 | ـهُ / اِسْمُهُ | -hu / ismuhu | his (suffix) / his name | suffix | high | u04_0060_huismuhu_formal.mp3 (formal, 2.85s) | vowels added |
| u4_v18_shaami | ـه / اِسْمه | -o / ismo | his (suffix) / his name (Levantine) | suffix | high | u04_0060_oismo_shaami.mp3 (shaami, 2.61s) | **shaami**; vowels added |
| u4_v19 | ـها / اِسْمُها | -haa / ismuhaa | her (suffix) / her name | suffix | high | u04_0061_haismuha_formal.mp3 (formal, 3.11s) | vowels added |
| u4_v19_shaami | ـها / اِسْمها | -a / isma | her (suffix) / her name (Levantine) | suffix | high | u04_0061_aisma_shaami.mp3 (shaami, 2.4s) | **shaami**; vowels added |
| u4_v23 | طالِب | Taalib | student (male) | noun | high | u04_0062_taalib_formal.mp3 (formal, 1.62s)<br>u04_0062_taalib_shaami.mp3 (shaami, 1.23s) |  |
| u4_v24 | طالِبة | Taaliba | student (female) | noun | high | u04_0063_taaliba_formal.mp3 (formal, 1.38s) |  |
| u4_v24_shaami | طالْبِة | Taalbe | student (female; Levantine) | noun | high | u04_0063_taalbe_shaami.mp3 (shaami, 1.54s) | **shaami**; vowels added |
| u4_v25 | أُسْتاذ | ustaadh | professor, teacher (male) | noun | high | u04_0064_ustaadh_formal.mp3 (formal, 1.59s) |  |
| u4_v25_shaami | إِسْتاذ | istaaz | professor, teacher (male; Levantine) | noun | high | u04_0064_istaaz_shaami.mp3 (shaami, 1.65s) | **shaami**; vowels added |
| u4_v26 | أُسْتاذة | ustaadha | professor, teacher (female) | noun | high | u04_0065_ustaadha_formal.mp3 (formal, 1.67s) | vowels added |
| u4_v26_shaami | إِسْتاذِة | istaaze | professor, teacher (female; Levantine) | noun | high | u04_0065_istaaze_shaami.mp3 (shaami, 1.62s) | **shaami**; vowels added |
| u4_v27 | جامِعة | jaamicat | the university of … (used right before a name) | noun | high | u04_0066_jaamicat_formal.mp3 (formal, 1.57s) |  |
| u4_v27_shaami | جامْعِة | jaamcit | the university of … (Levantine) | noun | high | u04_0066_jaamcit_shaami.mp3 (shaami, 1.57s) | **shaami**; vowels added |

## Unit 4 — New Vocabulary 2  ·  _New Vocabulary 2: More introductions (family, food, having)_

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_v01 | خُبْز | khubz | bread | noun | high | u04_0067_bread_formal.mp3 (formal, 1.33s)<br>u04_0067_bread_shaami.mp3 (shaami, 1.33s) | vowels added |
| u4_v02 | دَجاج | dajaaj | chicken | noun | high | u04_0068_chicken_formal.mp3 (formal, 1.57s)<br>u04_0068_chicken_shaami.mp3 (shaami, 1.44s) |  |
| u4_v03 | جار | jaar | neighbor (male) | noun | high | u04_0069_neighbor_male_formal.mp3 (formal, 1.36s)<br>u04_0069_neighbor_male_shaami.mp3 (shaami, 1.41s) |  |
| u4_v04 | جارة | jaara | neighbor (female) | noun | high | u04_0070_jaara_formal.mp3 (formal, 1.41s)<br>u04_0070_jaara_shaami.mp3 (shaami, 1.33s) |  |
| u4_v05 | أَخ | akh | brother | noun | high | u04_0071_brother_formal.mp3 (formal, 1.2s)<br>u04_0071_brother_shaami.mp3 (shaami, 1.31s) |  |
| u4_v06 | أُخْت | ukht | sister | noun | high | u04_0072_sister_formal.mp3 (formal, 1.25s)<br>u04_0072_sister_shaami.mp3 (shaami, 1.36s) | vowels added |
| u4_v07 | جَديد | jadiid | new (masc.) | adjective | high | u04_0073_new_masc_formal.mp3 (formal, 1.62s)<br>u04_0073_new_masc_shaami.mp3 (shaami, 1.57s) | vowels added |
| u4_v08 | جَديدة | jadiida | new (fem.) | adjective | high | u04_0074_jadiida_formal.mp3 (formal, 1.51s) |  |
| u4_v08_shaami | جْديدِة | jdiide | new (fem.; Levantine) | adjective | high | u04_0074_jdiide_shaami.mp3 (shaami, 1.44s) | **shaami**; vowels added |
| u4_v12 | مَساء الخَيْر | masaa' al-khayr | Good evening! | phrase | high | u04_0075_masaa_al_khayr_formal.mp3 (formal, 1.91s) | vowels added |
| u4_v12_shaami | مَسا الخير | masa l-kheer | Good evening! (Levantine) | phrase | high | u04_0075_masa_l_kheer_shaami.mp3 (shaami, 1.62s) | **shaami**; vowels added |
| u4_v13 | مَساء النّور | masaa' an-nuur | Good evening! (reply) — literally 'evening of light' | phrase | high | u04_0076_masaa_an_nuur_formal.mp3 (formal, 1.85s) | vowels added |
| u4_v13_shaami | مَسا النّور | masa n-nuur | Good evening! (reply; Levantine) | phrase | high | u04_0076_masa_n_nuur_shaami.mp3 (shaami, 1.57s) | **shaami**; vowels added |
| u4_v20 | عِنْدي | cindii | I have (literally 'with me') | phrase | high | u04_0077_cindi_formal.mp3 (formal, 1.59s) | vowels added |
| u4_v20_shaami | عِنْدي | candi | I have (Levantine) | phrase | high | u04_0077_candi_shaami.mp3 (shaami, 1.15s) | **shaami**; vowels added |
| u4_v21 | لَيْسَ عِنْدي | laysa cindii | I don't have | phrase | high | u04_0078_laysa_cindi_formal.mp3 (formal, 1.72s) | vowels added |
| u4_v21_shaami | ما عِنْدي | maa candi | I don't have (Levantine) | phrase | high | u04_0078_maa_candi_shaami.mp3 (shaami, 1.36s) | **shaami**; vowels added |
| u4_v22 | سُؤال | su'aal | question | noun | high | u04_0079_su_aal_formal.mp3 (formal, 1.65s)<br>u04_0079_su_aal_shaami.mp3 (shaami, 1.44s) |  |
| u4_v28 | أُحِبّ | uHibb | I love; I like | verb | high | u04_0080_i_love_formal.mp3 (formal, 1.33s) |  |
| u4_v28_shaami | بْحِبّ | bHibb | I love; I like (Levantine) | verb | med | u04_0080_i_love_shaami.mp3 (shaami, 1.28s) | **shaami**; vowels added |
| u4_v29 | تُحِبّ | tuHibb | you (m.) love / like | verb | high | u04_0081_you_masc_love_formal.mp3 (formal, 1.38s) |  |
| u4_v29_shaami | بِتْحِبّ | bitHibb | you (m.) love / like (Levantine) | verb | med | u04_0081_you_masc_love_shaami.mp3 (shaami, 1.28s) | **shaami**; vowels added |
| u4_v30 | تُحِبّين | tuHibbiin | you (f.) love / like | verb | high | u04_0082_tuhibbiin_formal.mp3 (formal, 1.78s) |  |
| u4_v30_shaami | بِتْحِبّي | bitHibbi | you (f.) love / like (Levantine) | verb | med | u04_0082_you_fem_love_shaami.mp3 (shaami, 1.54s) | **shaami**; vowels added |
| u4_v42 | رَقْم تِليفون | raqm tilifuun | telephone number | phrase | high | u04_0083_raqm_tilifuun_formal.mp3 (formal, 2.12s) | vowels added |
| u4_v42_shaami | نِمْرِة تِليفون | nimrit tilifuun | telephone number (Levantine) | phrase | high | u04_0083_nimrit_tilifuun_shaami.mp3 (shaami, 1.91s) | **shaami**; vowels added |

## Unit 4 — Writing Numbers 1–10

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_numbers | — | — | El-Shinnawi writes the numerals 0-10. | long_clip |  | u04_extra_c8ae0afc.wav (formal, 114.49s) | 114 s writing demo |

## Unit 4 — Writing ء

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_hamza | — | — | El-Shinnawi writes hamza. | long_clip |  | u04_extra_15701a54.wav (formal, 58.58s) | 59 s writing demo |

## Unit 4 — Writing د

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_daal | — | — | El-Shinnawi writes daal. | long_clip |  | u04_extra_5265a8a1.wav (formal, 52.2s) | 52 s writing demo |

## Unit 4 — Writing ذ

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_dhaal | — | — | El-Shinnawi writes dhaal (connected and unconnected). | long_clip |  | u04_extra_08d604b3.wav (formal, 104.23s) | 104 s writing demo |

## Unit 4 — Writing ر

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_raa | — | — | El-Shinnawi writes raa. | long_clip |  | u04_extra_9e9472be.wav (formal, 54.61s) | 55 s writing demo |

## Unit 4 — Writing ز

| id | Arabic | translit | meaning | type | conf | clip(s) | flags |
|---|---|---|---|---|---|---|---|
| u4_writing_zaay | — | — | El-Shinnawi writes zaay. | long_clip |  | u04_extra_f1255177.wav (formal, 64.22s) | 64 s writing demo |

## Notes on individual items (low confidence / non-words / special cases)

- `u2_le1_02` ساح / صاح — "it flowed; he roamed, toured / he shouted, cried out" — ساحَ is 'to flow (liquid) / to travel about'; صاحَ 'to shout' is certain. Contrast س vs ص.
- `u2_le1_03` داني / ضاني — "near, close (also the name Dani) / of sheep — mutton/lamb (Egyptian usage: لَحْم ضاني)" — Minimal pair for د vs ض; both meanings uncertain/rare.
- `u2_le4_03` تثبت — "unclear without the audio: tathbut 'she stays firm / you (m.) stay firm' OR tuthbit 'she proves / you (m.) prove'" — Printed unvowelled; vowels NOT added because the reading is ambiguous — confirm from the clip.
- `u2_le4_04` أَثاث — "furniture" — Lingco prints اثاث without the hamza (hamza is taught in Unit 4); correct spelling أَثاث. Spelling differs from the printed form اثاث (see notes).
- `u2_le5_05` جَثّ / جَذّ — "he uprooted (rare) / he cut off (rare)" — Rare/obscure verbs — basically a sound contrast. Printed جث / جذ; vowels and shadda assumed.
- `u2_le6_05` تَحْبو — "she crawls; you (m.) crawl (like a baby)" — Printed تحبو; reading taHbuu assumed (verb حَبا 'to crawl') — confirm from the clip.
- `u2_le7_04` تُثْبِتي — "(that) you (f.) prove / confirm" — Printed تثبتي unvowelled; reading tuthbitii assumed from Unit 2 LE11 item 2 (تُثبِتي) — could be tathbutii.
- `u2_le8_02` توب / تُب — "(no formal meaning — colloquial 'robe' / 'repent!') / repent! (said to a male)" — First member is not a formal-Arabic word.
- `u2_le10_02` بُثّ — "broadcast! / spread! (said to a male)" — Printed بُث; shadda added.
- `u2_d2_01` با — "(syllable 'baa' — no meaning)" — Sound drill.
- `u2_d2_03` باتا — "(no meaning — sound/spelling drill)"
- `u2_d2_04` تابا — "(no meaning here — sound/spelling drill)" — Could technically be read as the dual verb 'the two of them repented', but here it is a syllable string.
- `u2_d4_03` توب — "(no formal-Arabic meaning; colloquially 'robe, dress' or 'repent!')" — Formal 'repent!' is تُبْ (tub) and 'robe' is ثَوْب (thawb); treat as a sound/spelling item.
- `u2_d5_01` ثوبا — "(no meaning — sound/spelling drill)"
- `u2_d5_03` بيتا — "(no meaning — sound/spelling drill)"
- `u2_d5_04` باتي — "(no meaning — sound/spelling drill)"
- `u2_d8_02` بَتات — "(rare) household goods; best known in بَتاتاً 'absolutely (not), at all'"
- `u2_d11_04` توبا — "repent! (said to two people)" — Rare dual imperative — may just be a sound string.
- `u2_d11_08` ثوبي — "my robe / my garment (formal spelling ثَوْبي thawbii)" — The key prints no fatHa, so the clip reads a long uu (colloquial 'thoob'); formal is thawbii.
- `u2_d12_04` ثُب — "come back! return! (said to a male; rare)" — Imperative of ثابَ يَثوبُ.
- `u2_d12_06` تَبات — "(no standard meaning found — reading-practice string)" — Colloquial 'she spends the night' (formal تَبيت) is possible.
- `u2_d12_07` تابا — "the two of them (m.) repented" — Rare dual form; may just be a sound string.
- `u2_d12_10` تيتو — "(no meaning — reading-practice string; possibly the name 'Tito')"
- `u2_v10_shaami` إِنْتَ — "you (to a male; Levantine)" — Lingco prints إنتِ (with kasra) — apparently a typo; the book prints إنتَ, pronounced inte. Lingco vocab entry u02_0024. Shaami (Levantine) form — Dr. Khouri's dialect; allowed but flagged. Formal is what is graded.
- `u3_le1_01` تاج — "crown" — Clip says the word in the three regional pronunciations of ج (j / zh / hard Egyptian g) — it CONTAINS an Egyptian variant: trim to the first reading or avoid as card audio.
- `u3_le1_02` جُبّ — "well, pit (like the well Joseph was thrown into)" — Printed جُب; shadda added. — Clip says the word in the three regional pronunciations of ج (j / zh / hard Egyptian g) — it CONTAINS an Egyptian variant: trim to the first reading or avoid as card audio.
- `u3_le1_03` تُجيب — "she answers; you (m.) answer" — Clip says the word in the three regional pronunciations of ج (j / zh / hard Egyptian g) — it CONTAINS an Egyptian variant: trim to the first reading or avoid as card audio.
- `u3_le1_04` دَجاج — "chicken (collective — one hen is دَجاجة)" — Clip says the word in the three regional pronunciations of ج (j / zh / hard Egyptian g) — it CONTAINS an Egyptian variant: trim to the first reading or avoid as card audio.
- `u3_le3_03` باخ — "it went stale, lost its flavor; (heat) died down"
- `u3_le4_01` تَحْتَجْ — "(you/she) need — short form, as in لَمْ تَحْتَجْ 'you did not need'"
- `u3_d1_03` جوبي — "roam! explore! (said to a female)"
- `u3_d1_06` جيب — "spoken Arabic 'bring!' (to a male) — or jayb 'pocket' if the clip has the diphthong" — The key prints no fatHa (long ii), so not the diphthong jayb; confirm from the clip.
- `u3_d5_02` باخ — "it went stale, lost its flavor; (heat) died down"
- `u3_d6_02` جابي — "collector (of taxes or fees)"
- `u3_d6_11` تُجاب — "she/it is answered; you (m.) are answered (passive)"
- `u3_d6_12` بُحْ — "reveal it! (said to a male)" — Printed بُح.
- `u3_d6_15` خوجا — "khawaja / hodja — an old title for a teacher or a (foreign) gentleman"
- `u3_v14_shaami` كيفَك؟ / كيفِك؟ — "How are you? (to a male / to a female; Levantine)" — Lingco prints one cell كيفك؟ with translit 'kiifak/–ik' (masc./fem.); written out here as both forms. The clip may say one or both. Lingco vocab entry u03_0045. Shaami (Levantine) form — Dr. Khouri's dialect; allowed but flagged. Formal is what is graded. Spelling differs from the printed form كيفك؟ (see notes).
- `u3_v15_shaami` الحَمْدُ لِلّه — "Thank God (reply to 'How are you?'; Levantine pronunciation)" — Lingco prints الْحَمد لِلّها; the book prints الحَمدُ لِلّه for all three varieties (shaami pronounced il-Hamdilla). Lingco vocab entry u03_0046. Shaami (Levantine) form — Dr. Khouri's dialect; allowed but flagged. Formal is what is graded. Spelling differs from the printed form الْحَمد لِلّها (see notes).
- `u3_v18_shaami` هَيدا — "this (masc.; Levantine)" — Lingco pairs the spelling هَيدا with translit 'haada'; the book lists both haada (هادا) and hayda (هَيدا). Which one the clip says is unverified. Lingco vocab entry u03_0049. Shaami (Levantine) form — Dr. Khouri's dialect; allowed but flagged. Formal is what is graded.
- `u4_d9_02` خادِر — "drowsy, sluggish; (of a lion) in its den"
- `u4_v24` طالِبة — "student (female)" — Lingco's meaning 'your student (female)' is a typo; book: 'student (female)'. Lingco vocab entry u04_0063.

## Excluded clips

- 5 × Unit 1 LE2 Egyptian row (exists only as Egyptian audio)
- 88 × Egyptian (maSri) clip
- 6 × Egyptian scene video
  - u02_extra_4710d5d5.mp3: Unit 2 Drill 17 — Scene 2, Egyptian version ('HaDritak min maSr?') — excluded (Egyptian)
  - u03_extra_557e65e5.mp3: Unit 3 Drill 15 — Scene 3A, Egyptian version ('izzay Hadritik?') — excluded (Egyptian)
  - u03_extra_fb69a342.mp3: Unit 3 Drill 15 — Scene 3B, Egyptian version ('SabaaH l-kheer') — excluded (Egyptian)
  - u04_extra_625eeae3.mp3: Unit 4 Drill 4 — Scene 4A, Egyptian version ('izayyak?') — excluded (Egyptian)
  - u04_extra_676c38b8.mp3: Unit 4 Drill 4 — Scene 4B, Egyptian version ('al-Hamdu Lillah') — excluded (Egyptian)
  - u04_extra_cda3daa4.mp3: Unit 4 Drill 18 — Scene 4C, first video (Lingco label 'tasharrafna'); PROBABLY EGYPTIAN: Egyptian-first order on every other scene pair, and a different set from the Levantine videos — verify before ever using — excluded (Egyptian)
