#!/usr/bin/env python3
"""Targets for words not in any earlier batch -> cutter/targets<N>.json (N = next free number)."""
import json, os, glob, subprocess, sys
BASE = os.path.expanduser("~/arabic-catchup")
subprocess.run([sys.executable, f"{BASE}/build/merge.py"], check=True, capture_output=True)
prev = set(); used = set()
for f in [f"{BASE}/cutter/targets_batch1.json"] + sorted(glob.glob(f"{BASE}/cutter/targets[0-9]*.json")):
    for t in json.load(open(f)): prev.add(t["key"]); used.add(t["slug"])
subprocess.run([sys.executable, f"{BASE}/build/targets.py"], check=True, capture_output=True)   # rewrites targets.json
allt = json.load(open(f"{BASE}/cutter/targets.json"))
json.dump(json.load(open(f"{BASE}/cutter/targets_batch1.json")), open(f"{BASE}/cutter/targets.json", "w"), ensure_ascii=False, indent=1)
new = [t for t in allt if t["key"] not in prev]
n = 2
while os.path.exists(f"{BASE}/cutter/targets{n}.json"): n += 1
for t in new:
    if t["slug"] in used: t["slug"] += f"_b{n}"; t["out"] = t["out"].replace(".mp3", f"_b{n}.mp3")
json.dump(new, open(f"{BASE}/cutter/targets{n}.json", "w"), ensure_ascii=False, indent=1)
print(f"targets{n}.json: {len(new)} new targets")
