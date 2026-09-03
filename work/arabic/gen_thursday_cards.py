#!/usr/bin/env python3
"""Generate the Khouri Thursday (2026-09-03) vocab notes — Alif Baa Unit 2 "Meeting People"
as Dr. Khouri presented it on 2026-09-01, plus `hal`, which she added beyond the book list.

Sources (all snapshotted in this folder):
  * lingco_unit2_vocab.json       — publisher Unicode + transliteration (external authority)
  * lingco_unit2_audio_manifest.json — official AB3e clips, one per dialect cell
  * khouri_thursday_clips.json    — her own-voice clips cut from the 9/1 recording
                                    (slug -> {file, label, audio_source}); a slug that is
                                    absent means NO clean single-island cut exists, and the
                                    note keeps the publisher Formal clip in `Audio`.
Media single-home rule (language.md 7d): the Audio field wins; Back Extra only carries clips
that are NOT in the Audio field.  Shape rules V1/V2/V3 (check_block_spec.py) are satisfied
by construction: c1 = Arabic + transliteration, c2 = meaning, `Cue: MSA` present.
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
U2 = {r["row"]: r for r in json.load(open(os.path.join(HERE, "lingco_unit2_vocab.json"), encoding="utf-8"))["rows"]}
MAN = {(m["row"], m["dialect"]): m["file"] for m in json.load(open(os.path.join(HERE, "lingco_unit2_audio_manifest.json")))}
CLIPS = json.load(open(os.path.join(HERE, "khouri_thursday_clips.json"), encoding="utf-8"))
LRM = "‎"
SEP = "<br><br>"

def snd(row, dia):
    if isinstance(row, dict): row = row["row"]
    fn = MAN.get((row, dia))
    return f"[sound:{fn}]" if fn else None

# reference/sources.json -> sources.arabic.excluded_audio_dialects. Parker, 2026-09-03 (R61):
# no Egyptian (maSri) audio, ever. Khouri grades FuSHa and speaks Levantine; an Egyptian clip
# on the back was a pronunciation he must NOT imitate sitting beside one he should.
EXCLUDED_DIALECTS = set(json.load(open(os.path.join(HERE, "..", "..", "reference", "sources.json"),
                                       encoding="utf-8"))["sources"]["arabic"].get("excluded_audio_dialects", []))
CARDED_DIALECTS = [d for d in ("shaami",) if d not in EXCLUDED_DIALECTS]
LABEL = {"shaami": "Levantine", "masri": "Egyptian"}

def dialect_line(rows, prefix="Ex:"):
    """'Ex: Levantine [..]' for one row, or per-gender for two rows."""
    def cell(r):
        return " · ".join(f"{LABEL[d]} {snd(r, d)}" for d in CARDED_DIALECTS if snd(r, d))
    if len(rows) == 1:
        got = cell(rows[0])
        return f"{prefix} {got}" if got else None
    m, f = rows
    parts = []
    if cell(m): parts.append(f"{prefix} to a man — {cell(m)}")
    if cell(f): parts.append(f"{prefix} to a woman — {cell(f)}")
    return SEP.join(parts) if parts else None

def formal_line(rows, label="book audio — Formal"):
    if len(rows) == 1:
        return f"Ex: {label} {snd(rows[0],'formal')}"
    m, f = rows
    return f"Ex: {label} — to a man {snd(m,'formal')} · to a woman {snd(f,'formal')}"

SHORT_TR = {3: "maa", 7: "HaDratuka", 8: "HaDratuki", 10: "anta", 11: "anti", 12: "ismuka", 13: "ismuki", 14: "ayna", 15: "min ayna"}
def short_tr(r): return SHORT_TR.get(r["row"], r["formal"]["tr"].rstrip("?"))

def text(ar, tr, meaning, qualifier=None):
    t = f"{LRM}{{{{c1::{ar}}}}}{SEP}Transliteration: {{{{c1::{tr}}}}}{SEP}{{{{c2::{meaning}}}}}"
    return t + (f" — {qualifier}" if qualifier else "")

# ---------------------------------------------------------------------------------------
# One entry per note, in HER slide order (transcript 00:48:41 -> 01:07:30).
# `rows` = Lingco/book rows the note draws on (publisher Unicode is taken from them).
# ---------------------------------------------------------------------------------------
def A(row): return U2[row]["formal"]["ar"]

NOTES = [
 dict(slug="baab", rows=[1],
      ar=A(1), tr="baab", meaning="door",
      qualifier="the first word she had you spell out letter by letter",
      back=[
       "Why: <i>baa + alif + baa</i>. The first <i>baa</i> carries a vowel (the <i>alif</i>), the second does not — and because <i>alif</i> never connects to its left, the final <i>baa</i> stands in its independent form. She built it on the board exactly this way on 1 Sep.",
       "Ex: it came back as word 5 of the Unit 2 dictation Drill 2 she did on the board — \"baab. That's the door.\"",
      ],
      evidence="slide 'door' at 00:48:41; drilled as the first word of Unit 2 Drill 2 at 00:22:02 and 00:28:06"),
 dict(slug="ism", rows=[2],
      ar=A(2), tr="ism", meaning="name",
      qualifier="the bare noun, before any \"my\" / \"your\" ending is attached",
      back=[
       "Distinguish: <i>ism</i> is \"a name\"; add the <i>-i</i> ending and it becomes <i>ismi</i>, \"my name\". Dr. Khouri: \"If you say ismi, that's my name. If you say ism, that's a name.\"",
       "Why: possessive pronouns in Arabic are suffixes — they hang on the END of the noun.",
      ],
      evidence="slide 'name' at 00:49:20"),
 dict(slug="maa", rows=[3],
      ar="ما", tr="maa", meaning="what?",
      qualifier="the question word used before a NOUN: \"___ ismuka?\"",
      back=[
       "Pitfall: <i>maa</i> only goes with a noun — \"what's your NAME\". Verbs take a different word, which she is saving for later. Her line: \"maa comes with a noun only.\"",
       "Distinguish: Levantine says <i>shuu</i> — <i>shuu ismak?</i> \"Even in Saudi Arabia they used to say shuu. Everybody knows shuu.\"",
      ],
      evidence="slide 'what?' at 00:50:20; 'shuu ismi' modelled 00:51:30"),
 dict(slug="ahlan_bika", rows=[4, 5],
      ar=f"{A(4)} / {A(5)}", tr="ahlan bika / ahlan biki",
      meaning="(reply to) ahlan wa sahlan", qualifier="to a man / to a woman",
      back=[
       "Why: <i>bi-</i> is a preposition like <i>fii</i>, and <i>-ka / -ki</i> is \"you\" — literally \"welcome in you\". Dr. Khouri: \"We don't say that in English, but in Arabic this is what we mean.\"",
       "Distinguish: Levantine swaps the preposition — <i>ahlan fiik / ahlan fiiki</i>.",
       "Ex: you asked whether you can just say <i>ahlan</i> back — \"You can say ahlan, but this is another way.\" And it is safe upward: \"not very casual, this is neutral — older people, professors, your future boss.\"",
      ],
      evidence="slide '(reply to) ahlan' at 00:51:40; drilled 00:52:44–00:54:30 (Parker's question at 00:52:50)"),
 dict(slug="hadratuka", rows=[7, 8],
      ar=f"{A(7)} / {A(8)}", tr="HaDratuka / HaDratuki",
      meaning="you (polite, formal)", qualifier="to a man / to a woman — strangers, your boss, older people",
      back=[
       "Why: <i>HaDra</i> is \"presence\", so it is literally \"your presence\". The <i>-uka / -uki</i> ending is the \"you\".",
       "Ex: Dr. Khouri: \"It's not just you, but a formal you. We use it with strangers, people we meet for the first time, with the boss, older people, to show extra respect.\" Egyptians use it a lot — \"they use a lot of titles.\"",
       "Distinguish: Levantine <i>HaDartak / HaDartik</i> — same word, the vowels shift. \"If Shami is harder, use FuSHa. If FuSHa is harder, use Shami.\"",
       "Pitfall: she said this one WILL be on the final — \"if I bring HaDratuka on the exam, you should know what it is and how it is written.\"",
       "Pitfall: capital H = <i>Haa</i>, the throat sound (\"not from my chest, from my throat\"); capital D = <i>Daad</i>, the emphatic d.",
      ],
      evidence="slide 'you (polite)' at 00:54:40; 'repeat after me' drill 00:55:30–00:57:20"),
 dict(slug="anta", rows=[10, 11],
      ar=f"{A(10)} / {A(11)}", tr="anta / anti",
      meaning="you", qualifier="the everyday form: to a man / to a woman",
      back=[
       "Distinguish: <i>ana</i> = I, <i>anta</i> = you — she drilled them as a pair: \"ana, anta.\"",
       "Distinguish: Levantine <i>inte / inti</i> — \"the a sound, most of the time, turns into e in Shami.\"",
       "Distinguish: the final vowel is the whole gender — <i>-a</i> to a man, <i>-i</i> to a woman. Same pattern as <i>-ka / -ki</i>.",
      ],
      evidence="slide 'you (masculine)' at 00:57:30; feminine guessed by the class at 00:58:45"),
 dict(slug="ismuka", rows=[12, 13],
      ar="اِسمُكَ / اِسمُكِ", tr="ismuka / ismuki",
      meaning="your name", qualifier="to a man / to a woman — the \"your\" is a suffix on the noun",
      back=[
       "Why: possessive pronouns are suffixes — <i>-i</i> = my (<i>ismi</i>), <i>-ka</i> = your (m), <i>-ki</i> = your (f). The <i>u</i> in the middle is a vowel on the last letter of <i>ism</i>, so the pieces are <i>ism + u + ka</i>.",
       "Distinguish: Levantine <i>ismak / ismik</i> — \"the suffix that indicates you-masculine is -ka or -ak.\"",
      ],
      evidence="slide 'your (suffix) / your name' at 00:58:50–01:00:12"),
 dict(slug="maa_ismuka", rows=[3, 12, 13],
      ar="ما اِسمُكَ؟ / ما اِسمُكِ؟", tr="maa ismuka? / maa ismuki?",
      meaning="What is your name?", qualifier="to a man / to a woman — the question you will be asked on Thursday",
      back=[
       "Why: there is no \"is\" in Arabic — the question is just \"what + your name\". Dr. Khouri: \"ma ismuka or shuu ismak, both are the same.\"",
       "Distinguish: Levantine <i>shuu ismak? / shuu ismik?</i> — what Sydney answered first, and she took it.",
       "Ex: to ask HER you say <i>maa ismuki?</i> (she is a woman) — \"Who would like to ask me about my name?\"",
       "Ex: answer with <i>ismi Parker</i>.",
      ],
      evidence="'ma ismuka / ma ismuki' modelled 01:00:12–01:01:20; translation check 01:04:49"),
 dict(slug="ayna", rows=[14],
      ar=A(14).rstrip("؟"), tr="ayna", meaning="where?",
      qualifier="the question word: \"min ___ anta?\"",
      back=[
       "Ex: Dr. Khouri: \"or sometimes, out of habit, we pronounce it <i>ayn</i>.\"",
       "Distinguish: Levantine <i>wayn</i>.",
      ],
      evidence="slide 'where?' at 01:01:20"),
 dict(slug="min_ayna_anta", rows=[15, 10, 11],
      ar="مِن أَيْنَ أَنتَ؟ / مِن أَيْنَ أَنتِ؟", tr="min ayna anta? / min ayna anti?",
      meaning="Where are you from?", qualifier="to a man / to a woman — Arabic puts it \"from where you\"",
      back=[
       "Why: the order is \"from where are you\" — <i>min</i> (from) + <i>ayna</i> (where) + <i>anta</i>. Dr. Khouri: \"start word for word, but then make it make sense in English.\"",
       "Ex: your answer: <i>ana min madiinat Snellville</i>.",
       "Distinguish: Levantine <i>min wayn inte?</i>",
      ],
      evidence="slide 'from where' at 01:02:23; translation drill 01:03:40–01:04:49"),
 dict(slug="naam", rows=[16],
      ar=A(16), tr="nacam", meaning="yes", qualifier=None,
      back=[
       "Pitfall: the <i>c</i> is <i>cayn</i> — say \"ah\", then start to shock yourself, but only a little.",
       "Distinguish: Levantine <i>eeh</i>.",
      ],
      evidence="slide 'yes' at 01:03:00; 'say after me' drill"),
 dict(slug="laa", rows=[17],
      ar=A(17), tr="laa", meaning="no", qualifier=None,
      back=[
       "Distinguish: Levantine sometimes clips it with a glottal stop — <i>la'</i>. \"All works.\"",
      ],
      evidence="slide 'no' at 01:03:20"),
 dict(slug="hal", rows=[],
      ar="هَل", tr="hal", meaning="the word that opens a yes/no question",
      qualifier="\"___ anta min madiinat Lynchburg?\" = \"Are you from the city of Lynchburg?\"",
      back=[
       "Why: Arabic has no \"are / is / do\" at the front of a question, so <i>hal</i> does that job. Dr. Khouri: \"Anytime you want to ask 'are you, is he, is she, are we', in Arabic we add hal.\"",
       "Distinguish: <i>hal</i> opens a yes/no question · <i>maa</i> opens a \"what\" question · <i>ayna</i> opens a \"where\" question.",
       "Pitfall: NOT in the Alif Baa Unit 2 list — she put it on the slide on 1 Sep, the way she added <i>askun</i> last week. No book audio exists for it.",
       "Ex: <i>hal anta min madiinat Lynchburg?</i> — answer <i>nacam</i> or <i>laa</i>.",
      ],
      evidence="'hal anta / hal anti min madiinat Lynchburg' at 01:05:10–01:06:40"),
 dict(slug="min_ayna_hadratuka", rows=[15, 7, 8],
      ar="مِن أَيْنَ حَضرَتُكَ؟ / مِن أَيْنَ حَضرَتُكِ؟", tr="min ayna HaDratuka? / min ayna HaDratuki?",
      meaning="Where are you from?", qualifier="the POLITE version: to a man / to a woman you show extra respect",
      back=[
       "Distinguish: the same question as <i>min ayna anta?</i> with the polite \"you\" swapped in — her last slide of the day: \"Where are you from? Those are formal you.\"",
       "Ex: the version to use on Dr. Khouri herself: <i>min ayna HaDratuki?</i>",
      ],
      evidence="last slide at 01:06:49–01:07:30"),
]

COMPOUND = {"maa_ismuka", "min_ayna_anta", "min_ayna_hadratuka"}
EXTRA = {
    "hal": [("hal_sentence", "the whole question, Dr. Khouri, 1 Sep"),
            ("hal_anti", "to a woman, Dr. Khouri, 1 Sep")],
    "hadratuka": [("hadartak_lev", "Dr. Khouri saying the Levantine form, 1 Sep")],
    "ahlan_bika": [("ahlan_fiik_lev", "Dr. Khouri saying the Levantine form, 1 Sep")],
}

def build():
    cards = []
    for n in NOTES:
        clip = CLIPS.get(n["slug"])
        back = [f"Cue: MSA — <i>{n['tr']}</i>"] + n["back"]
        rows = [U2[r] for r in n["rows"]]
        gender_rows = [r for r in rows if r["row"] in (4,5,7,8,10,11,12,13)]
        single_rows = [r for r in rows if r["row"] not in (4,5,7,8,10,11,12,13)]
        # publisher clips: the Formal clip is the Audio field unless her voice takes it
        formal_rows = gender_rows if len(gender_rows) == 2 and n["slug"] in ("ahlan_bika","hadratuka","anta","ismuka") else single_rows[:1]
        if n["slug"] in COMPOUND:
            formal_rows = []          # a compound has no single publisher clip: list its components instead
        if clip:
            audio = f"[sound:{clip['file']}]"
            audio_source = clip["audio_source"]
            if formal_rows:
                back.append(formal_line(formal_rows))
            elif rows:   # compound: component formal clips
                back.append("Ex: book audio — " + " · ".join(f"<i>{short_tr(r)}</i> {snd(r,'formal')}" for r in rows))
        else:
            if formal_rows:
                audio = snd(formal_rows[0], "formal")
                audio_source = f"lingco-formal (Alif Baa U2 row {formal_rows[0]['row']}) — no clean single-island cut of Dr. Khouri saying this on the 2026-09-01 recording; every instance runs inside English"
                if len(formal_rows) == 2:
                    back.append(f"Ex: book audio — to a woman {snd(formal_rows[1],'formal')}")
            elif rows:
                audio = ""
                audio_source = "none — compound phrase with no publisher clip and no clean Khouri cut; component clips in Back Extra"
                back.append("Ex: book audio — " + " · ".join(f"<i>{short_tr(r)}</i> {snd(r,'formal')}" for r in rows))
            else:
                audio = ""
                audio_source = "none — hal has no publisher clip and no clean Khouri cut"
        # dialect clips (never in Audio)
        if n["slug"] in ("ahlan_bika","hadratuka","anta","ismuka"):
            back.append(dialect_line(gender_rows))          # may be None; filtered on join
        elif n["slug"] in ("maa_ismuka","min_ayna_anta","min_ayna_hadratuka"):
            pass  # compounds: dialects already described in prose; components carry the book clips
        elif single_rows:
            back.append(dialect_line(single_rows[:1]))      # may be None; filtered on join
        for cs, label in EXTRA.get(n["slug"], []):
            if cs in CLIPS:
                back.append(f"Ex: {label} — [sound:{CLIPS[cs]['file']}]")
        cards.append({
            "slug": n["slug"],
            "Text": text(n["ar"], n["tr"], n["meaning"], n["qualifier"]),
            "Back Extra": SEP.join(b for b in back if b),
            "Audio": audio,
            "audio_source": audio_source,
            "source": "arabic", "segment": 2,
            "origin": "khouri-lecture-2026-09-01",
            "evidence": n["evidence"],
            "verified_against": "lingco_unit2_vocab.json (lesson 8282) + Alif Baa 3e pp. 41-42 (physical 55-56)",
            "numeric": False, "needs_human_check": False, "block": "C_vocab",
        })
    return cards

if __name__ == "__main__":
    cards = build()
    out = os.path.join(HERE, "khouri_thursday_cards.json")
    json.dump(cards, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # every [sound:] must appear exactly once per note (single-home rule), and resolve to a file
    media = os.path.join(HERE, "media")
    for c in cards:
        blob = c["Audio"] + c["Back Extra"]
        refs = re.findall(r"\[sound:([^\]]+)\]", blob)
        dup = {r for r in refs if refs.count(r) > 1}
        missing = [r for r in refs if not os.path.exists(os.path.join(media, r))]
        assert not dup, f"{c['slug']}: duplicate media ref {dup}"
        assert not missing, f"{c['slug']}: missing media {missing}"
        assert c["Text"].startswith(LRM)
    print(f"wrote {len(cards)} notes -> {out}")
    for c in cards:
        print(f"  {c['slug']:20s} Audio={c['Audio'] or '(none)'}")
