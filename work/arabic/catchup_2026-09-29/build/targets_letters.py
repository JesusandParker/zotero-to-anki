#!/usr/bin/env python3
"""Cutter targets for HER voice saying each taught letter's name (letters lane).
yaa and waaw already carry arabic_khouri_u2_{yaa,waaw}.mp3, so they are skipped."""
import json, glob, os

BASE = os.path.expanduser("~/arabic-catchup")
NAMES = {"ا": ("alif", "ألف/الف"), "ب": ("baa", "باء/با"), "ت": ("taa", "تاء/تا"), "ث": ("thaa", "ثاء/ثا"),
         "ج": ("jiim", "جيم"), "ح": ("Haa", "حاء/حا"), "خ": ("khaa", "خاء/خا"), "ء": ("hamza", "همزة/همزه"),
         "د": ("daal", "دال"), "ذ": ("dhaal", "ذال"), "ر": ("raa", "راء/را"), "ز": ("zaay", "زاي/زين/زاء")}
ORDER = {"high": 0, "med": 1, "low": 2}

def main():
    spans = {k: [] for k in NAMES}
    for f in sorted(glob.glob(f"{BASE}/lectures/*.json")):
        for l in json.load(open(f)).get("letters", []):
            if l.get("letter") not in spans: continue
            for u in l.get("her_clear_utterances") or []:
                if u.get("file") and u.get("start") is not None:
                    e = float(u.get("end") or u["start"] + 0.8)
                    if e - float(u["start"]) > 4: e = float(u["start"]) + 4
                    spans[l["letter"]].append((ORDER.get(u.get("confidence"), 3), [u["file"], float(u["start"]), e]))
    T = []
    for k, (name, expect) in NAMES.items():
        at = [a for _, a in sorted(spans[k], key=lambda x: x[0])][:6]
        if not at: continue
        T.append({"slug": f"letter_{name.lower()}", "expect": expect, "at": at, "out": f"arabic_khouri_letter_{name.lower()}.mp3",
                  "dmin": 0.3, "dmax": 1.3, "budget": 200, "priority": 2, "key": f"LETTER:{k}"})
    json.dump(T, open(f"{BASE}/cutter/targets_letters.json", "w"), ensure_ascii=False, indent=1)
    print(len(T), "letter targets:", [t["slug"] for t in T])

if __name__ == "__main__":
    main()
