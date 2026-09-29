# Lingco Units 1-4: accuracy audit (fixes and drops only)

Audited **457** entries: **417 ok**, **25 fix**, **15 drop**. The full per-entry verdicts are in `lingco_audit.json`, which also holds the singular for every plural.

How I checked: every Arabic form was compared with the Lingco lesson text, the raw Lingco harvest, and the Alif Baa answer key (key pages 3-7, read from the page images). Every formal transliteration was regenerated from the vowelling to catch mismatches. Rare glosses were checked against Lane's Lexicon. Where the book prints no vowels, I resolved the reading from the publisher clip with spectrograms and LPC formant tracks (ffmpeg plus pure Python, no ML model), always comparing against clips whose vowels are printed.

Also confirmed by the same method, no change needed: حُبّ is Hubb (not Habb); تَحْبو is taHbuu (via its correct clip); the shaami بْحِبّ / بِتْحِبّ / بِتْحِبّي are bHibb, bitHibb, bitHibbi; the shaami كيفك clip says both kiifak and kiifik; the Unit 1 LE2 column order is Tunisia, Egypt, Lebanon, Oman, so the Lebanese entries are the right clips; the Unit 1 Drill 3 country order is right. U4 Drill 10's odd table order is only layout: file N is item N, and spectrograms confirm it.

## Fixes
### Audio attached to the WRONG word: U2 Listening Exercise 6 files are numbered in reverse
Lingco's page order for this lesson is files 05,04,03,02,01, and every other lesson I checked is in ascending order. Spectrograms of all five files agree with the page order: -01 = taHbuu, -02 = tuunis, -03 = thubuut, -04 = taabuut, -05 = tuut. The builder mapped file number to item number, so four of the five cards would play another word. The words and meanings themselves are fine. I spot-checked first and last items in 12 other exercises and found no other reversal.

| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u2_le6_01` | توت | tuut | mulberries; berries (collective) | AUDIO: the U2 LE6 publisher files are numbered in REVERSE of the printed items (Lingco page order is 05,04,03,02,01; spectrograms confirm). This word is AB3e_U2LE6-05 (u02_extra_c7121c0c.mp3); the file currently attached, -01 actually says taHbuu. collective; one berry = توتة tuuta |
| `u2_le6_02` | تابوت | taabuut | coffin, casket | AUDIO: the U2 LE6 publisher files are numbered in REVERSE of the printed items (Lingco page order is 05,04,03,02,01; spectrograms confirm). This word is AB3e_U2LE6-04 (u02_extra_52788deb.mp3); the file currently attached, -02 actually says tuunis. |
| `u2_le6_04` | تونِس | tuunis | Tunisia; Tunis | AUDIO: the U2 LE6 publisher files are numbered in REVERSE of the printed items (Lingco page order is 05,04,03,02,01; spectrograms confirm). This word is AB3e_U2LE6-02 (u02_extra_b940dc0f.mp3); the file currently attached, -04 actually says taabuut. |
| `u2_le6_05` | تَحْبو | taHbuu | she crawls; you (m.) crawl (like a baby) | AUDIO: the U2 LE6 publisher files are numbered in REVERSE of the printed items (Lingco page order is 05,04,03,02,01; spectrograms confirm). This word is AB3e_U2LE6-01 (u02_extra_e5fa3e1e.mp3); the file currently attached, -05 actually says tuut. That correct clip clearly says ta-H-b-uu, which confirms taHbuu. |

### Audio contains the Egyptian ج (brief: no Egyptian audio, ever)
Each Unit 3 LE1 clip says the word three times, once each as j, zh and Egyptian g (see the u3_le1_01 spectrogram). Keep only the j take.

| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u3_le1_01` | تاج | taaj | crown | AUDIO: this U3 LE1 clip says the word three times, once per ج variant (j, zh, Egyptian g); the brief bans Egyptian audio. Trim it to the j take (the first take, ~0.5-1.2 s; the third take, ~3.6-4.4 s, is the g) or use u3_d1_02's clip. |
| `u3_le1_02` | جُبّ | jubb | well, pit (like the well Joseph was thrown into) | AUDIO: this U3 LE1 clip says the word three times, once per ج variant (j, zh, Egyptian g); the brief bans Egyptian audio. Trim it to the j take (the spectrogram of u3_le1_01 shows the order j, zh, g; verify here). There is no other clip for this word. |
| `u3_le1_03` | تُجيب | tujiib | she answers; you (m.) answer | AUDIO: this U3 LE1 clip says the word three times, once per ج variant (j, zh, Egyptian g); the brief bans Egyptian audio. Trim it to the j take (the spectrogram of u3_le1_01 shows the order j, zh, g; verify here). There is no other clip for this word. |
| `u3_le1_04` | دَجاج | dajaaj | chicken (collective — one hen is دَجاجة) | AUDIO: this U3 LE1 clip says the word three times, once per ج variant (j, zh, Egyptian g); the brief bans Egyptian audio. Trim it to the j take (the spectrogram of u3_le1_01 shows the order j, zh, g; verify here) or use u4_le5_01 / u4_d10_06's clip. collective; one hen = دَجاجة dajaaja |

### Reading settled from the publisher clip (Arabic vowelling / translit changed)
These are printed unvowelled in the book, or Lingco's text and transliteration disagree. I settled each one by comparing vowel formants (spectrogram plus pure-Python LPC; no ML) against clips whose vowels are printed.

| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u2_le4_03` | تثبت → **تُثْبِت** | tathbut / tuthbit (unclear) → **tuthbit** | ~~unclear without the audio: tathbut 'she stays firm / you (m.) stay firm' OR tuthbit 'she proves / you (m.) prove'~~ → **she proves; you (m.) prove / confirm** | Printed unvowelled; the prior entry left it ambiguous. The clip has u…i vowels (LPC: V1 F1~370; V2 F2~1.9 kHz), matching the known تُثْبِت clip (U2 D12-03), so it is tuthbit, not tathbut. |
| `u2_le7_04` | تُثْبِتي → **تَثْبُتي** | tuthbitii → **tathbutii** | ~~(that) you (f.) prove / confirm~~ → **(that) you (f.) stay firm** | Printed unvowelled; the prior entry assumed tuthbitii. The clip has a…u…ii (LPC: V1 F1~650; V2 F1~300, F2~950), matching the known tathbut clip (U2 LE10-06), so it is تَثْبُتي, the subjunctive/jussive of تَثْبُتين. |
| `u3_v18_shaami` | هَيدا → **هادا** | hayda (or haada) → **haada** | this (masc.; Levantine) | Lingco pairs the spelling هَيدا with the transliteration haada. The clip's first vowel matches this speaker's aa (F1~756, F2~1754; his maashi aa ~634/1887), not his ee (ween ~420/2115). The book prints both هادا haada and هَيْدا hayda, so pair this audio with هادا. |
| `u3_v19_shaami` | هَيدي → **هادي** | haydi (or haadi) → **haadi** | this (fem.; Levantine) | Same speaker and test as u3_v18_shaami: first vowel F1~635, F2~1804 = his aa, not ee. The book prints هادي haadi / هَيدي haydi, so pair this audio with هادي. |

### Arabic vowel marks contradicted the Levantine pronunciation
Lingco prints these unvowelled. The builder copied the formal kasra onto them.

| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u4_v20_shaami` | عِنْدي → **عَنْدي** | candi | I have (Levantine) | Lingco prints عندي unvowelled for shaami. The kasra was copied from the formal عِنْدي and contradicts candi. |
| `u4_v21_shaami` | ما عِنْدي → **ما عَنْدي** | maa candi | I don't have (Levantine) | Lingco prints ما عندي unvowelled. The kasra was copied from the formal form and contradicts maa candi. |

### Meaning corrected
| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u2_le6_03` | ثُبوت | thubuut | ~~firmness; proof, being established~~ → **being proven (established); firmness** | ثُبوت is the verbal noun of ثَبَتَ, "to be firm / be proven". "Proof" is إِثْبات (ithbaat, u4_le3_03), so that gloss would mix the two up. Audio is OK here: LE6-03 is the middle item, so the reversal leaves it in place. |
| `u2_le10_03` | ثُبوت | thubuut | ~~firmness; proof, being established~~ → **being proven (established); firmness** | ثُبوت is the verbal noun of ثَبَتَ, "to be firm / be proven". "Proof" is إِثْبات (ithbaat, u4_le3_03), so that gloss would mix the two up. |
| `u2_d10_06` | ثُبوت | thubuut | ~~firmness; proof, being established~~ → **being proven (established); firmness** | ثُبوت is the verbal noun of ثَبَتَ, "to be firm / be proven". "Proof" is إِثْبات (ithbaat, u4_le3_03), so that gloss would mix the two up. |
| `u2_d11_03` | ثُبوت | thubuut | ~~firmness; proof, being established~~ → **being proven (established); firmness** | ثُبوت is the verbal noun of ثَبَتَ, "to be firm / be proven". "Proof" is إِثْبات (ithbaat, u4_le3_03), so that gloss would mix the two up. |
| `u3_le3_03` | باخ | baakh | ~~it went stale, lost its flavor; (heat) died down~~ → **it died down (fire, heat, anger); it went stale** | Core sense first, per Lane: (fire/heat/anger) abated. "Went stale" is secondary. Rare verb (باخَ يَبوخُ). |
| `u3_d5_02` | باخ | baakh | ~~it went stale, lost its flavor; (heat) died down~~ → **it died down (fire, heat, anger); it went stale** | Core sense first, per Lane: (fire/heat/anger) abated. "Went stale" is secondary. Rare verb (باخَ يَبوخُ). |
| `u3_d6_15` | خوجا | khuujaa | ~~khawaja / hodja — an old title for a teacher or a (foreign) gentleman~~ → **hodja: old title for a teacher or religious scholar (from Turkish hoca)** | The prior gloss mixed in خَواجة khawaaja ("(foreign) gentleman"), which is a different word. Rare, old-fashioned. |
| `u3_d9_20` | جَوابات | jawaabaat | ~~answers; (in spoken Arabic) letters (plural of جَواب)~~ → **answers, replies (plural of جَواب)** | Dropped the "letters" sense, which is Egyptian usage (brief: no Egyptian forms). sing. جَواب jawaab |

### Transliteration / convention
| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u3_v14` | كَيْفَ الحال؟ | kayfa al-Haal? → **kayfa l-Haal?** | How are you? (literally 'how is the condition?') | The Arabic has the fatHa on كَيْفَ, and the a of al- drops after a vowel. The book writes kayf al-Haal. "kayfa al-Haal" matches neither. |
| `u3_v12` | يا … | yaa … | ~~O …! — put before a name when calling or addressing someone directly (yaa Ahmad)~~ → **O …! — put before a name when calling or addressing someone directly (yaa aHmad)** | Cosmetic: the example transliteration now follows the convention (ح = H), so aHmad, not Ahmad. |
| `u3_v20` | بِخَيْر | bi-khayr | ~~fine, well (reply to 'kayfa al-Haal?')~~ → **fine, well (reply to 'kayfa l-Haal?')** | Cosmetic: the embedded transliteration now matches the u3_v14 fix (kayfa l-Haal). |

## Drops (`keep:false`)
### Drill tokens whose clip teaches a non-standard pronunciation or a sound string
| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u2_d5_02` | بيتي | biitii | (drill token biitii; "my house" = بَيْتي baytii) | Clip says biitii: steady ii (F1~295, F2~2250 from onset), no ay glide. It is a Unit 2 long-vowel dictation token. "My house" is بَيْتي baytii, already carded with correct audio (u3_d9_12, u3_d11_02); this clip would teach the wrong vowel. |
| `u2_d11_08` | ثوبي | thuubii | (drill token thuubii; "my robe" = ثَوْبي thawbii) | Clip says thuubii: steady uu (F1~450, F2~1100), no aw glide (real ثَوْب onset F1~650). It is a dictation token, not formal Arabic. ثَوْب/ثِياب are carded. |
| `u2_d11_04` | توبا | tuubaa | (sound-string drill item tuubaa) | Clip = tuubaa (u…aa confirmed). A long-vowel drill string, like بابا and باتا in Drill 13. The only real reading is the dual imperative "repent, you two!", which is not worth a card. |
| `u2_d12_07` | تابا | taabaa | (sound-string drill item taabaa) | A long-vowel drill string, printed next to non-words (تيتو, تَبات). The only real reading is the dual "they two repented", which is not worth a card. |

### Meaning cannot be pinned down (and collides with a carded word)
| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u3_d1_06` | جيب | jiib | (jiib: "jeep" or spoken "bring!"; not جَيْب "pocket") | Clip says jiib: steady ii (F1~300-400, F2~2300), unlike the ay glide in the known جَيْب clip (U3 LE8-03). That makes it "jeep" or spoken "bring!", and the intended word cannot be known. It would also clash with جَيْب jayb "pocket", which is carded (u3_le8_03, u3_d9_*). |

### Non-course dialect samples (Unit 1 LE2, Omani and Tunisian columns)
| id | Arabic | translit | meaning | why |
|---|---|---|---|---|
| `u1_le2_11` | — | — | Good morning! | Omani sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_12` | — | — | How are you? | Omani sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_13` | — | — | Good (fine) | Omani sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_14` | — | — | Good-bye | Omani sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_15` | — | — | I love Oman | Omani sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_16` | — | — | Good morning! | Tunisian sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_17` | — | — | How are you? | Tunisian sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_18` | — | — | Good (fine) | Tunisian sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_19` | — | — | Good-bye | Tunisian sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |
| `u1_le2_20` | — | — | I love Tunisia | Tunisian sample from the "hear four dialects" exercise: not a course variety, no printed Arabic; a third dialect for the same greeting would compete with the formal and Levantine forms he is graded on. |

## Kept but flagged rare (low priority, still `keep:true`)
These are real words and their glosses are verified, but they are literary, classical or rare, so they deserve low review priority: `u2_le9_01`, `u2_d8_06`, `u2_d12_11`, `u2_d4_01`, `u4_d6_02`, `u3_le7_05`, `u2_d12_04`, `u2_d8_02`, `u4_d9_02`, `u4_d9_03`, `u3_d1_03`, `u3_d6_11`, `u3_d6_12`, `u3_le3_03`, `u3_d5_02`, `u3_d6_15`. The Lebanese LE2 rows (`u1_le2_01`-`05`) are kept, but they still need their Arabic transcribed from the clip before they can become cards.
