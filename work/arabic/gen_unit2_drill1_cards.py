#!/usr/bin/env python3
"""Generate the Unit 2 Drill 1 listening cards ("Hearing frontal and deep alif").

Parker's margin comment on the Drill 1 heading (physical p41, Zotero NSNM2FEZ):
  "literally go into Linco. Find those things and create for me flashcards that are like
   tell me whether this one is frontal or deep and then you play the sound and then I guess
   whether it's frontal or deep."

The night shift of 2026-09-04 could not reach Lingco (browser automation on the Mac was
blocked by the session's permission policy), so it prepared this generator instead. A
daytime session finishes the job in two steps:

  1. HARVEST (playbook §0/§1): in Chrome on the Mac, logged in to class.lingco.io,
       GET /api/courses/4839/modules/27015           -> the Unit 2 lesson list; find Drill 1
       GET /api/content/lessons/<drill1LessonId>      -> per item: audio asset UUID + the
                                                         correct answer (F or D)
     then for each UUID:  curl -L https://class.lingco.io/api/assets/<uuid> -o <file>
     (the 302 target needs no cookies). Lowercase filenames, into work/arabic/media/:
       arabic_u2_drill1_01.mp3 … arabic_u2_drill1_12.mp3
     Snapshot the answer key + UUIDs as work/arabic/lingco_unit2_drill1.json:
       {"source": "...", "fetched": "YYYY-MM-DD", "lesson_id": ...,
        "items": [{"n": 1, "answer": "F", "uuid": "...", "file": "arabic_u2_drill1_01.mp3",
                   "word_ar": "(optional)", "word_tr": "(optional)"}, ...]}
  2. GENERATE + GATE + WRITE, as for any unit:
       python3 work/arabic/gen_unit2_drill1_cards.py --highlights <the highlights file carrying the Drill 1 mark>
       python3 scripts/verify_report.py work/arabic/unit_2_drill1_cards.json --highlights <same>
       python3 scripts/check_block_spec.py work/arabic/unit_2_drill1_cards.json
       python3 scripts/check_cards.py work/arabic/unit_2_drill1_cards.json --highlights <same> --source arabic
       python3 scripts/anki_write.py work/arabic/unit_2_drill1_cards.json --run runs/arabic/2/<run>
     then media_audit.py and render_check.py (the clip must play on the FRONT: it lives in
     Text, never in the Audio field, which autoplays only on flip).

Card shape (one note per word; the answer is a forced-choice binary, card-rules #4/#13):
    [sound:<clip>]  Listen: is the alif in this word frontal or deep?  {{c1::frontal::frontal or deep}}
The frontal/deep cue lines on the back are grounded in the Drill 1 mark's own context
(p41: emphatic consonants are "pronounced with the tongue lower and farther back in the
mouth" and "affect the pronunciation of surrounding vowel sounds") and p40 (deep ~ father,
frontal ~ e in bet). --fixture builds two sample cards from fake data to prove the shape.
"""
import argparse, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, "media")
LRM = "‎"
SEP = "<br><br>"
ANSWER = {"F": "frontal", "D": "deep"}

def build(items, from_idx, verified_against):
    cards, seen = [], set()
    for it in items:
        ans = ANSWER[it["answer"].strip().upper()[0]]
        fn = it["file"]
        assert fn == fn.lower() and re.fullmatch(r"arabic_u2_drill1_\d\d\.mp3", fn), f"bad filename {fn}"
        assert fn not in seen, f"duplicate clip {fn}"; seen.add(fn)
        text = (f"[sound:{fn}]{SEP}Listen: is the alif in this word <i>frontal</i> or <i>deep</i>? "
                f"{{{{c1::{ans}::frontal or deep}}}}")
        back = ["Cue: a deep alif sits beside an emphatic consonant — the tongue is lower and farther back in the mouth, so the alif sounds like the <i>a</i> in <i>father</i>; a frontal alif leans toward the <i>e</i> in <i>bet</i>.",
                "Why: hearing frontal versus deep alif is the best way to tell an emphatic consonant from a plain one — the consonant colours the vowel next to it."]
        if it.get("word_tr"):
            back.append(f"Ex: the word is <i>{it['word_tr']}</i> (Drill 1, item {it['n']}).")
        if it.get("word_ar"):
            back.append(LRM + it["word_ar"])           # pure-script line (language.md §7a)
        cards.append({
            "Text": text, "Back Extra": SEP.join(back),
            "source": "arabic", "segment": 2, "from_idx": from_idx, "block": "M_listening_drill1",
            "numeric": False,
            "verified_against": verified_against,
            "verified_by": f"answer key + clip taken from the Lingco lesson snapshot (item {it['n']}, asset {it.get('uuid','?')}); cue lines grounded in the Drill 1 mark's context (p41) and p40",
            "needs_human_check": False, "visual_source": None, "image": None,
            "drill_item": it["n"],
        })
    return cards

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(HERE, "lingco_unit2_drill1.json"))
    ap.add_argument("--highlights", help="highlights JSON carrying the Drill 1 mark (NSNM2FEZ)")
    ap.add_argument("--out", default=os.path.join(HERE, "unit_2_drill1_cards.json"))
    ap.add_argument("--fixture", action="store_true", help="build two sample cards from fake data (no media check)")
    a = ap.parse_args()
    if a.fixture:
        items = [{"n": 1, "answer": "F", "uuid": "fixture", "file": "arabic_u2_drill1_01.mp3", "word_tr": "taab"},
                 {"n": 2, "answer": "D", "uuid": "fixture", "file": "arabic_u2_drill1_02.mp3", "word_ar": "طاب", "word_tr": "Taab"}]
        cards = build(items, [2], "FIXTURE — not real data")
        print(json.dumps(cards, ensure_ascii=False, indent=1)); return
    data = json.load(open(a.data, encoding="utf-8"))
    items = data["items"]
    assert len(items) == 12, f"Drill 1 has 12 items on p41; got {len(items)}"
    missing = [it["file"] for it in items if not os.path.exists(os.path.join(MEDIA, it["file"]))]
    assert not missing, f"clips missing from work/arabic/media: {missing}"
    if not a.highlights:
        sys.exit("--highlights is required: the cards must cite the Drill 1 mark (NSNM2FEZ) by index")
    hl = json.load(open(a.highlights, encoding="utf-8"))
    idx = [i for i, h in enumerate(hl) if h.get("zotero_key") == "NSNM2FEZ"]
    assert idx, "the highlights file does not carry the Drill 1 mark NSNM2FEZ"
    cards = build(items, idx, f"Lingco lesson {data.get('lesson_id','?')} answer key + audio, snapshot {os.path.basename(a.data)} fetched {data.get('fetched','?')}")
    json.dump(cards, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {len(cards)} cards -> {a.out}")

if __name__ == "__main__":
    main()
