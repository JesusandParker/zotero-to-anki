#!/usr/bin/env python3
"""R63: a publisher clip is identified by TRANSCRIBING it. Compare each Lingco clip that a card will play
with the word the card says. Distance = normalized edit distance on bare consonant skeletons.
out: clipcheck/mismatches.json  (clip file -> {expected, heard, dist})"""
import json, os, re, sys
BASE = os.path.expanduser("~/arabic-catchup")
sys.path.insert(0, f"{BASE}/build")
from arabic_read import bare

def norm(s):
    s = bare(s or "")
    s = re.sub("[أإآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي").replace("ء", "")
    return re.sub(r"[^ء-ي ]", "", s).strip()

def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def main():
    asr = json.load(open(f"{BASE}/clipcheck/clips_asr.json"))
    by_origin = {}
    for f, r in asr.items():
        o = (r.get("origin") or "").rsplit(".", 1)[0].lower().replace("ab3e_", "")
        by_origin[re.sub(r"[^a-z0-9]+", "_", o)] = (f, r)
    cards = json.load(open(f"{BASE}/build/cards.json"))
    out, checked = {}, 0
    for c in cards:
        m = re.search(r"\{\{c1::([^}]+)\}\}", c["Text"])
        if not m or c["block"] != "C_vocab": continue
        expected = norm(m.group(1).split("—")[0])
        for name in c.get("media", {}):
            mm = re.match(r"arabic_lingco_(.+?)(?:_j)?\.mp3$", name)
            if not mm or mm.group(1) not in by_origin: continue
            f, r = by_origin[mm.group(1)]
            heard = norm(r.get("ar", ""))
            if not heard or not expected: continue
            checked += 1
            # the clip may say the word inside a longer utterance: score the best-matching window
            words = heard.split(); n = max(1, len(expected.split()))
            best = min((lev(" ".join(words[i:i + n]), expected) / max(len(expected), 1)
                        for i in range(max(1, len(words) - n + 1))), default=1.0)
            if best > 0.34:
                out[name] = {"expected": m.group(1), "heard": r.get("ar"), "dist": round(best, 2), "text": c["Text"][:70]}
    json.dump(out, open(f"{BASE}/clipcheck/mismatches.json", "w"), ensure_ascii=False, indent=1)
    print(f"checked {checked} card clips; {len(out)} disagree")
    for k, v in list(out.items())[:40]: print(" ", k, "| expected", v["expected"], "| heard", v["heard"], "|", v["dist"])

if __name__ == "__main__":
    main()
