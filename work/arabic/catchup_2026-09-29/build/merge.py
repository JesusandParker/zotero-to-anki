#!/usr/bin/env python3
"""Merge the three word lists into ONE master list, and mark what Anki already has.

  A = Anki inventory (inv/anki_inventory.json)          — what he already studies
  L = Lingco Units 1-4 words with audio (lingco/lingco_words.json)
  K = Khouri's words, per lecture (lectures/YYYY-MM-DD.json)

Parker's rule (2026-09-29): every word she taught + every Lingco word with audio, and where
she taught a Lingco word, HER version wins (her voice, her usage notes), Lingco becomes the
backup audio. The master list is keyed on the bare consonant skeleton (+ alif/hamza folding),
with gender pairs split so either half matches.
out: build/master.json + build/master_report.md
"""
import json, os, re, glob, collections
from arabic_read import bare

BASE = os.path.expanduser("~/arabic-catchup")

def key(ar):
    s = bare(ar or "")
    s = re.sub("[أإآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "ء").replace("ئ", "ء")
    s = re.sub(r"[؟?!.,،:\"'()«»\-]", "", s)
    return re.sub(r"\s+", " ", s).strip()

def parts(ar):
    return [p for p in (key(x) for x in re.split(r"[/|]", ar or "")) if p]

def tkey(tr):
    return re.sub(r"[^a-z]", "", (tr or "").lower().replace("c", "c"))

# lecture date -> the Alif Baa unit being taught that day (from the lecture records)
UNIT_BY_DATE = {"2026-08-25": 1, "2026-08-27": 1, "2026-09-01": 2, "2026-09-03": 2, "2026-09-08": 3,
                "2026-09-10": 3, "2026-09-15": 3, "2026-09-17": 3, "2026-09-22": 4, "2026-09-24": 4,
                "2026-09-29": 4}

def load_anki():
    inv = json.load(open(f"{BASE}/inv/anki_inventory.json"))
    idx = {}
    for o in inv:
        is_letter_note = "Name:" in o.get("text", "") or "Letter:" in o.get("text", "")
        for a in o["arabic"]:
            for p in parts(a):
                # a WORD must never be marked "already carded" because it matches a LETTER note: the lone
                # suffix in "ـهُ / اِسْمُهُ" reduces to ه and hid a Unit 4 chart row behind the haa letter card
                if is_letter_note: continue
                idx.setdefault(p, []).append(o)
    return inv, idx

def main():
    inv, aidx = load_anki()
    master = collections.OrderedDict()   # key -> record

    def rec_for(k, seed):
        if k not in master:
            master[k] = {"key": k, "arabic": seed.get("arabic"), "translit": seed.get("translit"),
                         "meaning": seed.get("meaning"), "units": set(), "lingco": [], "khouri": [],
                         "anki": None}
        return master[k]

    # --- Lingco
    L = json.load(open(f"{BASE}/lingco/lingco_words.json")) if os.path.exists(f"{BASE}/lingco/lingco_words.json") else []
    if isinstance(L, dict): L = L.get("items") or L.get("words") or list(L.values())
    for it in L:
        if it.get("word_type") in ("long_clip",): continue
        ps = parts(it.get("arabic") or it.get("arabic_bare"))
        if not ps: continue
        r = rec_for(ps[0], it)
        r["units"].add(it.get("unit"))
        r["lingco"].append(it)
        for p in ps[1:]: master.setdefault(p, r)

    # --- Khouri lectures
    for f in sorted(glob.glob(f"{BASE}/lectures/2026-*.json")):
        d = json.load(open(f))
        for w in d.get("words", []):
            date = w.get("lecture_date") or d.get("lecture") or os.path.basename(f)[:10]
            ps = parts(w.get("arabic") or w.get("arabic_bare"))
            if not ps: continue
            hit = next((master[p] for p in ps if p in master), None)
            r = hit or rec_for(ps[0], w)
            w = dict(w); w["lecture"] = date
            r["khouri"].append(w)
            if not r["units"] or not hit:
                r["units"].add(w.get("book_unit") or UNIT_BY_DATE.get(date))
            for p in ps:
                master.setdefault(p, r)

    # --- mark Anki
    seen = set(); out = []
    for k, r in master.items():
        if id(r) in seen: continue
        seen.add(id(r))
        allkeys = {k2 for k2, r2 in master.items() if r2 is r}
        hits = [o for p in allkeys for o in aidx.get(p, [])]
        r["anki"] = sorted({o["nid"] for o in hits}) or None
        r["units"] = sorted(u for u in r["units"] if u)
        out.append(r)
    json.dump(out, open(f"{BASE}/build/master.json", "w"), ensure_ascii=False, indent=1, default=list)
    n_new = sum(1 for r in out if not r["anki"])
    print(f"master: {len(out)} distinct words | already in Anki {len(out)-n_new} | to add {n_new}")
    print(f"  with Khouri evidence: {sum(1 for r in out if r['khouri'])} | Lingco: {sum(1 for r in out if r['lingco'])}"
          f" | both: {sum(1 for r in out if r['khouri'] and r['lingco'])}")

if __name__ == "__main__":
    main()
