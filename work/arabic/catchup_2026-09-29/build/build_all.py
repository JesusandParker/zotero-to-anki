#!/usr/bin/env python3
"""Assemble every NEW note for the 2026-09-29 catch-up into build/cards.json, then run the guards.

  vocab   (C_vocab)        : master.json -> gen_cards.build_vocab
  letters (A_letter_forms) : Unit 4 connected forms + hamza seats, with example words + her voice
  digits  (B_symbols)      : ٠-١٠ with the number word and its audio
Guards: check_block_spec.py (Parker's accumulated requirements) + local checks (media exists,
lowercase names, no Egyptian, pure-script Back Extra lines, no duplicate Text).
"""
import json, os, re, sys, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_cards as G
import letters as LT
from arabic_read import bare

BASE = os.path.expanduser("~/arabic-catchup")
SKILL = os.path.expanduser("~/.claude/skills/zotero-to-anki")
ROOT = G.ROOT

def load_audit():
    p = f"{BASE}/audit/lingco_audit.json"
    if not os.path.exists(p): return {}
    return {a["id"]: a for a in json.load(open(p))}

def example_pool(vocab_notes, inv):
    """Words with audio he will study: new notes + existing vocab notes (existing media referenced by name)."""
    pool = []
    for n in vocab_notes:
        m = re.search(r"\{\{c1::([^}]+)\}\}<br><br>Transliteration: \{\{c1::([^}]+)\}\}<br><br>\{\{c2::([^}]+)\}\}", n["Text"])
        a = re.search(r"\[sound:([^\]]+)\]", n["Audio"] or "")
        if not (m and a): continue
        pr = {"chart": 0, "class": 2, "numbers": 2, "practice": 4}.get(n["tier"], 5)
        if "ARAB101::required" in n.get("tags", []): pr = min(pr, 1)
        if re.sub(r"<[^>]+>", "", m.group(3)).split()[0].lower().strip(",;") in (
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"): pr = min(pr, 1)
        pool.append({"arabic": m.group(1), "translit": m.group(2), "meaning": re.sub(r"<[^>]+>", "", m.group(3)),
                     "audio": a.group(1), "audio_src": n["media"].get(a.group(1)), "priority": pr})
    tiers = json.load(open(f"{BASE}/build/existing_tiers.json")) if os.path.exists(f"{BASE}/build/existing_tiers.json") else {}
    chart_ids = set(tiers.get("chart", []))
    for o in inv:
        if not (o["arabic"] and o["translit"] and o["audio_field"]): continue
        if o["model"] != "AnKing Cloze" or "/" in o["arabic"][0] or "Name:" in o["text"] or "Letter:" in o["text"]: continue
        pool.append({"arabic": o["arabic"][0], "translit": o["translit"], "meaning": (o["c2"] or [""])[0],
                     "audio": o["audio_field"][0], "audio_src": None, "priority": 0 if o["nid"] in chart_ids else 2})
    return [w for w in pool if w["audio"].endswith(".mp3")]

def letter_notes(pool, letter_clips):
    out = []
    for F in LT.U4_FORMS + LT.HAMZA_FORMS:
        want = F["position"].split("::")[0]
        if F["letter"] in ("أ", "إ"): want_form = ("isolated", "initial")
        ex = None
        if F["letter"] in ("د", "ذ", "ر", "ز"):
            ex = LT.pick_example(pool, F["letter"], "medial and final")
        else:   # hamza seats: pick by spelling, not by joining form
            for w in sorted(pool, key=lambda w: (w["priority"], len(bare(w["arabic"])))):
                b = bare(w["arabic"])
                if F["letter"] == "أ" and b.startswith("أ"): ex = {**w, "why": "it opens the word, so the hamza sits on an alif seat"}; break
                if F["letter"] == "إ" and b.startswith("إ"): ex = {**w, "why": "it opens the word with an i-vowel, so the hamza hangs under the alif"}; break
                if F["letter"] == "ء" and b.endswith("اء"): ex = {**w, "why": "a long aa ends the word, so the hamza sits on the line"}; break
        clip = letter_clips.get({"hamza on alif": "ء", "hamza under alif": "ء", "hamza on the line": "ء"}.get(F["name"], F["letter"]))
        spec = LT.form_note(F, [ex] if ex else [], her_clip=clip)
        spec["tier"] = "letters"; spec["key"] = "FORM:" + F["shape"]
        out.append(spec)
    return out

DIGITS = "٠١٢٣٤٥٦٧٨٩"
DIGIT_TIPS = {0: "zero is written as a dot, not a circle", 5: "five is the little circle — it looks like an English zero, but it is 5",
              2: "two has one hook on top; three has two", 3: "three has two hooks on top; two has one",
              6: "six looks like a 7 with a curl; seven is a V", 7: "seven opens upward like a V; eight is the same shape upside down",
              8: "eight is an upside-down V; seven opens upward", 4: "four has a looped back, like a backwards 3 with a tail",
              9: "nine looks like an English 9", 1: "one is a single upright stroke", 10: "ten is simply a one followed by the zero dot"}

def digit_notes(num_words):
    """num_words: {n: {translit, audio, audio_src}} from the number vocab notes."""
    out = []
    for n in range(0, 11):
        glyph = "١٠" if n == 10 else DIGITS[n]
        w = num_words.get(n, {})
        text = f"{G.LRM}{{{{c1::{glyph}}}}}<br><br>Number: {{{{c2::{n}}}}}"
        be = [f"Say it: <i>{w['translit']}</i>" if w.get("translit") else "",
              f"Distinguish: {DIGIT_TIPS[n]}.",
              "Why: these are the digits used across the Arab East (she calls them Hindi numerals); phone numbers and prices use them."]
        spec = {"block": "B_symbols", "Text": text, "Back Extra": "<br><br>".join(x for x in be if x),
                "Audio": f"[sound:{w['audio']}]" if w.get("audio") else "", "media": ({w["audio"]: w["audio_src"]} if w.get("audio_src") else {}),
                "deck": f"{ROOT}::Unit 04", "tier": "numbers", "key": f"DIGIT:{n}",
                "tags": ["arabic-u4", "ARAB101::tier::numbers", "ARAB101::catchup-2026-09-29", "ARAB101::from::book"]}
        out.append(spec)
    return out

AR = re.compile(r"[؀-ۿ]"); LAT = re.compile(r"[A-Za-z]")
def local_checks(cards):
    errs = []
    texts = collections.Counter(c["Text"] for c in cards)
    for c in cards:
        if texts[c["Text"]] > 1: errs.append(("dup-text", c["Text"][:60]))
        for name, src in (c.get("media") or {}).items():
            if name != name.lower(): errs.append(("upper-media", name))
            if src is None: continue
            if not os.path.exists(src): errs.append(("missing-media", name, src))
        for ref in re.findall(r"\[sound:([^\]]+)\]|src=\"([^\"]+)\"", c["Text"] + c["Back Extra"] + c["Audio"]):
            r = ref[0] or ref[1]
            if "masri" in r: errs.append(("egyptian", r))
        for line in re.split(r"<br><br>|<br>", c["Back Extra"]):
            plain = re.sub(r"<[^>]+>|\[sound:[^\]]+\]", "", line)
            if AR.search(plain) and LAT.search(plain): errs.append(("mixed-line", c["Text"][:40], plain[:80]))
    return errs

def main():
    master = json.load(open(f"{BASE}/build/master.json"))
    inv = json.load(open(f"{BASE}/inv/anki_inventory.json"))
    vocab, held = G.build_vocab(master, G.her_clips_by_key(), load_audit())
    pool = example_pool(vocab, inv)
    letter_clips = {}
    lp = f"{BASE}/cutter/cut_log_letters.json"
    if os.path.exists(lp):
        T = {t["slug"]: t for t in json.load(open(f"{BASE}/cutter/targets_letters.json"))}
        for slug, v in json.load(open(lp)).items():
            if v.get("status") == "PASS" and slug in T: letter_clips[T[slug]["key"].split(":")[1]] = v["out"]
    letters = letter_notes(pool, letter_clips)
    nums = {}
    for n in vocab:
        m = re.search(r"\{\{c2::(zero|one|two|three|four|five|six|seven|eight|nine|ten)\b", n["Text"])
        if m and n["tier"] in ("numbers", "class", "chart"):
            k = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"].index(m.group(1))
            if k in nums: continue
            tr = re.search(r"Transliteration: \{\{c1::([^}]+)\}\}", n["Text"]).group(1)
            a = re.search(r"\[sound:([^\]]+)\]", n["Audio"] or "")
            if a: nums[k] = {"translit": tr, "audio": a.group(1), "audio_src": n["media"].get(a.group(1))}
    digits = digit_notes(nums)
    cards = vocab + letters + digits
    json.dump(cards, open(f"{BASE}/build/cards.json", "w"), ensure_ascii=False, indent=1)
    json.dump(held, open(f"{BASE}/build/held.json", "w"), ensure_ascii=False, indent=1)
    # guards
    spec = [{"Text": c["Text"], "Back Extra": c["Back Extra"], "Audio": c["Audio"], "block": c["block"],
             "image": c.get("image")} for c in cards]
    json.dump(spec, open(f"{BASE}/build/cards_spec.json", "w"), ensure_ascii=False)
    r = subprocess.run(["python3", f"{SKILL}/scripts/check_block_spec.py", f"{BASE}/build/cards_spec.json"], capture_output=True, text=True)
    print(r.stdout[-3000:])
    errs = local_checks(cards)
    print(f"local checks: {len(errs)} problems"); [print("  ", e) for e in errs[:25]]
    tiers = collections.Counter(c["tier"] for c in cards); decks = collections.Counter(c["deck"][-7:] for c in cards)
    print(f"{len(cards)} notes = {len(vocab)} vocab + {len(letters)} letter forms + {len(digits)} digits | held {len(held)}")
    print("tiers", dict(tiers), "| decks", dict(decks))
    print("audio:", collections.Counter("her" if "khouri" in c["Audio"] else ("book" if c["Audio"] else "none") for c in cards))

if __name__ == "__main__":
    main()
