# ARAB 101 catch-up — brief for every subagent (2026-09-29)

Parker (premed, Liberty University) is behind in **ARAB 101 Elementary Arabic I** (Dr. Sherene
Khouri, section 003, textbook *Alif Baa* 3rd ed., homework on Lingco). A **Unit 1-4 vocab quiz
(matching) + Unit 1-4 writing quiz (paper, connecting letters)** is ~2 weeks out. He wants his
Anki deck to hold **every word she has taught in class, plus every Unit 1-4 word Lingco has
publisher audio for**, each with the best audio available (HER voice first), plus every
positional form of every letter taught so far. Maximum coverage, not a minimum. Card quality
must be excellent: accurate Arabic, simple plain-language explanations.

You are one worker. Do ONLY your assigned package and write your output file. Be exhaustive and
precise; when unsure, say so in the output rather than guessing.

## Hard rules
- **Never run mlx_whisper, whisper-cli, or any ML model.** The GPU is running a queued job; a
  second model halves it and can thrash the 18 GB Mac. All transcripts you need are pre-made
  (below). ffmpeg (CPU) for frames/short audio slices is fine — keep it light (one ffmpeg at a
  time, sample sparsely).
- **Never write to Anki** (AnkiConnect localhost:8765 is read-only for you) and never edit files
  outside your output directory.
- **No Egyptian (maSri) forms or audio, ever.** Formal Arabic (FuSHa) is graded; Levantine
  (shaami) is her own dialect and allowed but must be flagged `register: "shaami"`.
- **Transliteration = Parker's book convention:** UPPERCASE for emphatics/pharyngeal H only
  (S D T DH H = ص ض ط ظ ح), doubled vowels for long (aa ii uu), `c` = cayn (ع), `'` = hamza,
  `kh` خ, `dh` ذ, `th` ث, `sh` ش, `gh` غ. Examples: marHaban, ahlan wa sahlan, shukran, cafwan,
  tasharrafnaa, HaDratuka, SabaaH al-khayr, tafaDDal, SaaHibii, Taalib, ustaadh, jaamica,
  su'aal, masaa' al-khayr. Her slides sometimes sentence-case the first letter (Shukran) —
  that capital means nothing; don't copy it.
- **Arabic spelling authority, in order:** her slide text (read the frame image yourself) >
  Lingco/book (`~/arabic-vault/scripts/arabic <english|translit|arabic>`, `--unit N`) > the Alif
  Baa answer key PDF > your own knowledge (flag it). **Never quote Arabic from the Teams
  .vtt/.txt — Teams ASR is English-only and garbles every Arabic word** ("marhaba" -> "my but").
  Use Teams captions to find WHEN and what she said in English around it.
- The whisper `ar` pass translates English speech into Arabic and hallucinates YouTube boilerplate
  on quiet audio ("ترجمة نانسي قنقر", "اشتركوا في القناة"). A hit counts only when the `en` pass
  at the same time shows she was actually saying an Arabic word there.
- Fully vowelled Arabic (tashkiil) on every word, the way the book/Lingco prints it.

## Paths
- Teams lecture trio (mp4/vtt/txt): `~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures/YYYY-MM-DD Elementary Arabic I.{mp4,vtt,txt}`
  (mp4 is a Drive file — reading it hydrates it; first read of a 600 MB file takes ~1 min).
- Whisper large-v3-turbo passes (clean flags, word timestamps): `~/arabic-catchup/mlx/<id>_en.json`
  and `<id>_ar.json`, ids `teams_YYYY-MM-DD` and `phone_YYYY-MM-DD`. A `<id>.READY` file marks
  both passes done. JSON = `{"segments":[{"start","end","text","words":[{"word","start","end"}]}]}`.
- 16 kHz mono WAVs: `~/arabic-catchup/wav/<id>.wav`.
- Nightly distilled lecture records (English summaries of every class, very useful as a map of
  what was taught when): `~/arabic-catchup/brief/ARAB101-YYYY-MM-DD.json`.
- Phone (Voice Memos) recordings exist for 9/22, 9/24, 9/29 (and a partial 9/1). Offsets:
  9/22 phone_t = teams_t - 10 s; **9/24 phone_t = teams_t + 34 s and the last ~12 min of class
  (after Teams stopped at 12:18) exist ONLY on the phone**; **9/29 phone_t = teams_t + 742 s and
  the first ~12 min of class exist ONLY on the phone**. Teams audio = her lapel mic (clean, noise
  gated); phone = room audio (noisier). Prefer Teams for her voice where both exist.
- Lingco vault: `~/arabic-vault/` (README.md; `data/lexicon.json`, `data/lessons/unit-NN/*.txt`,
  `data/other_tables.json`, `media/*.mp3`). Units 1-4 clip -> publisher origin filename map:
  `~/arabic-catchup/lingco_video/all_u14.json` (origin like `AB3e_U4LE5-03.mp3` = Unit 4,
  Listening Exercise 5, item 3; `U4VSt-09` = Unit 4 vocab row 9 Formal; `VS` = shaami;
  `VE` = Egyptian — never use). Fetched drill/writing videos' audio: `~/arabic-catchup/lingco_video/aud/*.wav`.
- Alif Baa answer key PDF: `~/Zotero/storage/8I2BY7AA/*.pdf` (Unit 3 = key pages 4-5,
  Unit 4 = PDF pages 5-6). Book (600 dpi scan, Arabic text layer): `~/Zotero/storage/SPRRWAP7/*.pdf`,
  physical page = printed + 18 from printed 6 on (Unit 2 = printed 19-44, Unit 3 = 45-64, Unit 4 = 65-90).
- Parker's current Anki inventory (221 notes, read-only reference): `~/arabic-catchup/inv/anki_inventory.json`.
- Prior audit of the first four lectures (8/25-9/3), already carded: `~/.claude/skills/zotero-to-anki/work/arabic/gap_audit_2026-09-05/inventory_final.json`.

## Units 1-4 scope (Alif Baa)
Unit 1 overview + greetings; Unit 2 ا ب ت ث + و ي as long vowels + fatHa/Damma/kasra;
Unit 3 ج ح خ + sukuun; Unit 4 hamza ء, د ذ ر ز, numerals 0-10. (Shadda is Unit 5.)
