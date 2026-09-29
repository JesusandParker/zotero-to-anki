#!/usr/bin/env python3
"""Build cutter targets (her own voice) from master.json.

Who gets a cut, in priority order:
  1. words that will become NEW notes and she taught (Audio field = her voice)
  2. existing notes whose audio is not hers yet (her clip goes in the empty Lecture Notes field)
  3. letter names/sounds (letters lane)
Skips anything whose note already carries an arabic_khouri_* clip.
out: cutter/targets.json
"""
import json, os, re
from arabic_read import bare

BASE = os.path.expanduser("~/arabic-catchup")

def slugify(tr):
    s = (tr or "").lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:40] or "w"

def spans(k):
    out = []
    order = {"high": 0, "med": 1, "low": 2}
    ut = sorted(k.get("her_clear_utterances") or [], key=lambda u: order.get(u.get("confidence"), 3))
    for u in ut:
        if not u.get("file") or u.get("start") is None: continue
        s = float(u["start"]); e = float(u.get("end") or s + 0.8)
        if e - s > 6: e = s + 6          # an agent span that swallows a sentence: keep the head
        out.append([u["file"], round(s, 2), round(e, 2)])
    return out

def main():
    master = json.load(open(f"{BASE}/build/master.json"))
    inv = {o["nid"]: o for o in json.load(open(f"{BASE}/inv/anki_inventory.json"))}
    targets, used = [], set()
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gen_cards import resolve
    for r in master:
        if not r.get("khouri"): continue
        if all(k.get("kind") == "letter-name" for k in r["khouri"]): continue   # letters lane cuts these
        if not r.get("anki") and resolve(r) is None: continue                  # will not become a note
        has_her = r.get("anki") and any("khouri" in s for n in r["anki"] for s in inv.get(n, {}).get("sounds", []))
        if has_her: continue
        at = [a for k in r["khouri"] for a in spans(k)]
        if not at: continue
        ar = r["arabic"] or r["khouri"][0].get("arabic")
        tr = r["translit"] or r["khouri"][0].get("translit")
        expects = {bare(x).strip() for x in re.split(r"[/|]", ar or "") if bare(x).strip()}
        for k in r["khouri"]:
            for x in re.split(r"[/|]", k.get("arabic_bare") or k.get("arabic") or ""):
                if bare(x).strip(): expects.add(bare(x).strip())
        n = max(len(bare(x).replace(" ", "")) for x in expects)
        slug = slugify(tr.split("/")[0] if tr else "w")
        base_slug = slug; i = 2
        while slug in used: slug = f"{base_slug}_{i}"; i += 1
        used.add(slug)
        date = (r["khouri"][0].get("lecture_date") or r["khouri"][0].get("lecture") or "")[5:].replace("-", "")
        targets.append({"slug": slug, "expect": "/".join(sorted(expects)), "at": at[:6],
                        "out": f"arabic_khouri_{date}_{slug}.mp3" if date else f"arabic_khouri_{slug}.mp3",
                        "dmin": round(0.25 + 0.05 * n, 2), "dmax": round(min(3.6, 0.8 + 0.2 * n), 2),
                        "budget": 350, "priority": 0 if not r.get("anki") else 1, "key": r["key"]})
    targets.sort(key=lambda t: t["priority"])
    os.makedirs(f"{BASE}/cutter", exist_ok=True)
    json.dump(targets, open(f"{BASE}/cutter/targets.json", "w"), ensure_ascii=False, indent=1)
    print(len(targets), "targets;", sum(t["priority"] == 0 for t in targets), "for new notes")

if __name__ == "__main__":
    main()
