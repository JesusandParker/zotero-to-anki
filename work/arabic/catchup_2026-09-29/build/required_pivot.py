#!/usr/bin/env python3
"""2026-09-30 pivot: keep ONLY what Dr. Khouri requires for the Tue 10/6 quizzes (Unit 1-4 vocab
matching, Unit 1-4 writing, Unit 4 numbers); suspend everything else in ARAB 101.

REQUIRED VOCAB = her five vocab lists (= the book's Unit 1-4 charts, formal column; Lingco "New
Vocabulary" rows) + the words she told the class to add or learn, with the recording + timestamp
that says so (EXPLICIT below). Shaami/maSri are optional in her words (8/25 51:42 "I'm not going to
require them in your quizzes"), so dialect-only rows are out.
WRITING = the letters of Units 1-4 (Unit 1 has none; U2 ا ب ت ث و ي / U3 ج ح خ / U4 ء د ذ ر ز) in every
position, the vowel marks those units teach (fatHa Damma kasra sukuun), and the script-mechanics
facts. NUMBERS = 0-10 as digits and as words (9/22: "learn how to count from zero to ten ... read
them and write them").
usage: required_pivot.py            -> writes build/required_plan.json + prints the split
"""
import json, os, re, sys, urllib.request, collections
sys.path.insert(0, os.path.dirname(__file__))
from merge import key, parts

BASE = os.path.expanduser("~/arabic-catchup")
ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"

def ac(action, **params):
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://localhost:8765", json.dumps({"action": action, "version": 6, "params": params}).encode()), timeout=120))
    if r.get("error"): raise RuntimeError(f"{action}: {r['error']}")
    return r["result"]

# words she told the class to add / learn, beyond her slide lists (recording, seconds, her words)
EXPLICIT = [
    ("أسكن",  "askun",   "2026-08-27", 4303, "This is not in the list, add it to the list"),
    ("شكرا",  "shukran", "2026-08-27", 4457, "practice this list of vocab, add the few words that I added"),
    ("عفوا",  "cafwan",  "2026-08-27", 4457, "practice this list of vocab, add the few words that I added"),
    ("فصحى",  "fuSHaa",  "2026-08-27", 3724, "fuSHa, learn this word"),
    ("الفصحى", "fuSHaa", "2026-08-27", 3724, "fuSHa, learn this word"),
    ("أب",    "ab",      "2026-08-27", 3234, "you learned your first word (ab, father)"),
    ("باب",   "baab",    "2026-09-01", 1540, "baab is required"),
    ("توت",   "tuut",    "2026-09-01", 2187, "This is required. Write it also."),
    ("هل",    "hal",     "2026-09-01", 2848, "her second vocab list (Unit 2) + hal"),
    ("ما اسمك", "maa ismuka?", "2026-09-01", 2848, "her second vocab list"),
    ("من أين أنت", "min ayna anta?", "2026-09-01", 2848, "her second vocab list"),
    ("من أين حضرتك", "min ayna HaDratuka?", "2026-09-01", 2848, "her second vocab list"),
    ("تشكيل", "tashkiil", "2026-09-03", 2678, "You need to learn these words. Tashkiil, all short vowels. FatHa..."),
    ("فتحة",  "fatHa",   "2026-09-03", 2678, "You need to learn these words"),
    ("ضمة",   "Damma",   "2026-09-03", 2678, "You need to learn these words"),
    ("كسرة",  "kasra",   "2026-09-03", 2678, "You need to learn these words"),
    ("سكون",  "sukuun",  "2026-09-03", 2678, "You need to learn these words"),
    ("تحت",   "taHt",    "2026-09-10", 3671, "I need you to learn taHt (takht, bed, is optional)"),
    ("خوخ",   "khawkh",  "2026-09-15", 1611, "khawkh and bayt, these two words you have to learn ... add them"),
    ("بيت",   "bayt",    "2026-09-15", 1611, "khawkh and bayt, these two words you have to learn ... add them"),
    ("أخ",    "akh",     "2026-09-22", 4616, "those are required, add them to your vocab list, brother and sister"),
    ("أخت",   "ukht",    "2026-09-22", 4616, "those are required, add them to your vocab list, brother and sister"),
    ("دجاج",  "dajaaj",  "2026-09-29", 298,  "So add it to your vocab list. You could start memorizing it."),
    ("رقم تليفون", "raqm tilifuun", "2026-09-29", 3452, "raqm tilifuun. You should know that."),
    ("عندي سؤال", "cindii su'aal", "2026-09-29", 3188, "a new word for you, you have to learn ... ustaadha, cindii su'aal"),
    ("أستاذة عندي سؤال", "ustaadha, cindii su'aal", "2026-09-29", 3188, "from this moment onward if you have a question you have to say: ustaadha, cindii su'aal"),
]
NUMBER_WORDS = ["صفر", "واحد", "اثنين", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة", "عشرة", "رقم"]

# the letters + marks of book units 2-4 (Lingco "Writing ..." lessons: U2 ا ب ت ث و ي + 3 short vowels,
# U3 ج ح خ + sukuun, U4 ء د ذ ر ز)
U14_LETTERS = {"alif", "baa", "taa", "thaa", "waaw", "yaa", "jiim", "Haa", "khaa", "daal", "dhaal", "raa", "zaay",
               "hamza", "hamza on alif", "hamza under alif", "hamza on the line", "fatHa", "Damma", "kasra", "sukuun"}
# script-mechanics concept cards (how letters are written, joined and vowelled) - the writing quiz
WRITING_CONCEPTS = {1786229801725, 1786229801777, 1786229801828, 1786229801876, 1786229801927, 1786229801977,
                    1786229802121, 1788627829648, 1789129139566, 1789129140103, 1789129140620}
# duplicates of a kept note (keep the older one)
DUPLICATE_OF = {1790710584464: 1790070513772}    # "yaa ..." (new) == "yaa" (studied)
# matched a chart row only through its abbreviated second half ("/ anti?"); taught in the 9/5 spoken
# round, never on her lists
NOT_REQUIRED = {1788627828502: "taught in class (9/5 speaking round), not on her lists and never called required"}

def nk(s):
    return key((s or "").replace("\u2026", " ").replace("...", " "))

def ks_of(s):
    return [x for x in (nk(p) for p in re.split(r"[/|]", s or "")) if x]

def c1(note):
    t = note["fields"].get("Text", {}).get("value", "")
    m = re.search(r"\{\{c1::(.+?)\}\}", t)
    return m.group(1) if m else ""

def plain(note):
    f = note["fields"]; t = (f.get("Text") or f.get("Front") or next(iter(f.values())))["value"]
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\{\{c\d::(.*?)(::[^}]*)?\}\}", r"\1", t).replace("‎", "")
    return re.sub(r"\s+", " ", t).strip()

def main():
    lingco = json.load(open(f"{BASE}/lingco/lingco_words.json"))
    chart = {}
    for x in lingco:
        if x["unit"] in (1, 2, 3, 4) and x["lesson"].startswith("New Vocabulary") and x.get("register") == "formal":
            for p in ks_of(x["arabic"]) + [nk(x["arabic"])]:
                chart[p] = x["id"]
    explicit = {nk(a): (a, tr, d, t, q) for a, tr, d, t, q in EXPLICIT}
    numbers = {nk(a) for a in NUMBER_WORDS}

    nids = ac("findNotes", query=f'"deck:{ROOT}"')
    notes = ac("notesInfo", notes=nids)
    cids = ac("findCards", query=f'"deck:{ROOT}"')
    cards = ac("cardsInfo", cards=cids)
    susp = dict(zip(cids, ac("areSuspended", cards=cids)))
    by_note = collections.defaultdict(list)
    for c in cards: by_note[c["note"]].append(c)

    plan = {"keep": {}, "suspend": {}}
    for n in notes:
        nid, tags = n["noteId"], n["tags"]
        tier = next((t.split("::")[-1] for t in tags if t.startswith("ARAB101::tier::")), "?")
        txt = plain(n)
        why = None; cat = None
        if nid in DUPLICATE_OF:
            why = f"duplicate of note {DUPLICATE_OF[nid]}"
        elif nid in NOT_REQUIRED:
            why = NOT_REQUIRED[nid]
        elif tier == "letters":
            m = re.search(r"(?:Name|Letter): (.+?)(?: Transliteration:| Position:| Sound:| Dot:|$)", txt)
            name = (m.group(1).strip() if m else "")
            if name in U14_LETTERS or txt.startswith("The NAME of a letter ends in a hamza") \
               or re.match(r"Write all four positional forms: [جحخ]", txt):
                cat = "writing"
            else:
                why = "letter or symbol from Unit 5 or later (not on the Units 1-4 writing quiz)"
        elif tier == "numbers":
            cat = "numbers"
        elif tier == "concept":
            if nid in WRITING_CONCEPTS: cat = "writing"
            elif "Write what you hear" in txt: why = "dictation drill (her writing quiz joins letters; no dictation)"
            else: why = "background fact (culture, geography, dialects, phonetics), not tested"
        else:
            ks = ks_of(c1(n)) or [nk(c1(n))]
            full = nk(c1(n))
            if any(x in chart for x in ks) or full in chart:
                cat = "vocab"
            elif full in explicit or any(x in explicit for x in ks):
                cat = "vocab"
            elif full in numbers:
                cat = "numbers"
            else:
                why = {"class": "taught or used in class, but not on her lists and never called required",
                       "practice": "Lingco practice word (not on her lists)",
                       "chart": "dialect-only row (she tests fuSHa only)"}.get(tier, "not required")
        rec = {"text": txt[:140], "tier": tier, "cards": [c["cardId"] for c in by_note[nid]],
               "types": [c["type"] for c in by_note[nid]], "was_suspended": [susp[c["cardId"]] for c in by_note[nid]],
               "deck": by_note[nid][0]["deckName"].split("::")[-1]}
        if cat: plan["keep"][str(nid)] = {**rec, "cat": cat}
        else:   plan["suspend"][str(nid)] = {**rec, "why": why}

    json.dump(plan, open(f"{BASE}/build/required_plan.json", "w"), ensure_ascii=False, indent=0)
    def tally(d, field):
        out = collections.Counter()
        for r in d.values():
            for t in r["types"]:
                out[(r[field], "new" if t == 0 else "seen")] += 1
        return out
    print("KEEP notes:", len(plan["keep"]), " SUSPEND notes:", len(plan["suspend"]))
    for k, v in sorted(tally(plan["keep"], "cat").items()): print("  keep", k, v)
    for k, v in sorted(tally(plan["suspend"], "why").items()): print("  susp", k, v)

if __name__ == "__main__":
    main()
