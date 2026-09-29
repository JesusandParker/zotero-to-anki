#!/usr/bin/env python3
"""Fill review/template.html -> review/index.html with the clip list and the full word list.
Clip audio is published beside the page as clips/<file>.mp3 (supporting files)."""
import json, os, re, sys, glob, collections
BASE = os.path.expanduser("~/arabic-catchup")
sys.path.insert(0, f"{BASE}/build")
import gen_cards as G

def mmss(t):
    t = int(t); return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"

def main():
    master = json.load(open(f"{BASE}/build/master.json"))
    cards = json.load(open(f"{BASE}/build/cards.json"))
    held = json.load(open(f"{BASE}/build/held.json"))
    inv = {o["nid"]: o for o in json.load(open(f"{BASE}/inv/anki_inventory.json"))}
    created = {c.get("key") for c in cards}
    heldk = {h["key"]: h["why"] for h in held}
    # targets (slug -> key) across all batches
    tmap = {}
    for tp in [f"{BASE}/cutter/targets_batch1.json"] + sorted(glob.glob(f"{BASE}/cutter/targets[0-9]*.json")) + [f"{BASE}/cutter/targets_letters.json"]:
        if os.path.exists(tp):
            for t in json.load(open(tp)): tmap[t["slug"]] = t
    rec = {r["key"]: r for r in master}
    # only clips that actually sit on a card (new cards, or lines added to existing notes) are reviewed
    used = set()
    for c in cards:
        used |= set(re.findall(r"\[sound:([^\]]+)\]", " ".join(str(c.get(f, "")) for f in ("Text", "Back Extra", "Audio", "Lecture Notes"))))
    if os.path.exists(f"{BASE}/build/existing_plan.json"):
        for u in json.load(open(f"{BASE}/build/existing_plan.json"))["field_updates"]:
            used |= set(re.findall(r"\[sound:([^\]]+)\]", u["value"]))
    card_by_key = {c.get("key"): c for c in cards}
    clips = []
    for lp in sorted(glob.glob(f"{BASE}/cutter/cut_log*.json")):
        for slug, v in json.load(open(lp)).items():
            if not v.get("status", "").startswith("PASS") or not v.get("out"): continue
            if not os.path.exists(f"{BASE}/clips/{v['out']}"): continue
            t = tmap.get(slug, {}); key = t.get("key", "")
            if v["out"] not in used and not key.startswith("LETTER:"): continue
            c = v["chosen"]; fid = c["file"]
            where = f"{G.md(fid.split('_')[-1])} · {mmss(c['s'])}" + (" · phone" if fid.startswith("phone") else "")
            if key.startswith("LETTER:"):
                L = key.split(":")[1]
                arabic, tr, meaning, unit = L, slug.replace("letter_", ""), "the letter's name", 4
                card = "letter cards" if v["out"] in used else "not on a card yet: confirm it and I add it"
            else:
                r = rec.get(key) or {}
                cd = card_by_key.get(key)
                if cd:
                    m = re.search(r"\{\{c1::([^}]+)\}\}<br><br>Transliteration: \{\{c1::([^}]+)\}\}<br><br>\{\{c2::([^}]+)\}\}", cd["Text"])
                    arabic, tr, meaning = (m.group(1), m.group(2), re.sub(r"<[^>]+>", "", m.group(3))) if m else (r.get("arabic"), r.get("translit"), r.get("meaning"))
                    unit = int(cd["deck"][-2:]); card = "new card"
                elif r.get("anki"):
                    o = inv[r["anki"][0]]
                    arabic, tr, meaning = o["arabic"][0], o["translit"], (o["c2"] or [""])[0]
                    unit = int((o["deck"] or "Unit 00")[-2:]); card = "your existing card (Lecture Notes)"
                else:
                    continue    # a word that was held back: its clip is not used anywhere
            flag = {"PASS_NEAR": "near match: is it the right word?", "PASS_HINTED": "found with a hint: check it"}.get(v["status"])
            if key.startswith("LETTER:") and not flag:
                flag = "letter name: whisper is weak on single syllables, check it"
            clips.append({"slug": slug, "src": f"clips/{v['out']}", "file": v["out"], "arabic": arabic, "translit": tr,
                          "meaning": meaning, "unit": unit, "flag": flag, "where": where, "card": card})
    clips.sort(key=lambda c: (0 if c["flag"] else 1, -c["unit"], c["translit"] or ""))
    for c in clips: c["group"] = "Check these first" if c["flag"] else f"Unit {c['unit']}"
    # every word
    words = []
    for r in master:
        k = r["key"]
        if r.get("anki"): state = "had"
        elif k in created: state = "added"
        else: state = "held"
        dates = sorted({(x.get("lecture_date") or x.get("lecture") or "")[:10] for x in r["khouri"] if x.get("lecture_date") or x.get("lecture")})
        dates = [d for d in dates if re.match(r"\d{4}-\d\d-\d\d", d)]
        les = sorted({f"U{it.get('unit')} {it.get('lesson')}" for it in r["lingco"]})
        frm = "; ".join(filter(None, ["class " + ", ".join(G.md(d) for d in dates) if dates else "", ", ".join(les[:3])]))
        cd = card_by_key.get(k)
        audio = ("her voice" if cd and "khouri" in cd["Audio"] else "book" if cd and cd["Audio"] else "none") if cd else ("—" if state == "held" else "")
        meaning = r.get("meaning") or (r["khouri"][0].get("meaning") if r["khouri"] else "")
        if cd:
            m = re.search(r"\{\{c2::([^}]+)\}\}", cd["Text"]); meaning = re.sub(r"<[^>]+>", "", m.group(1)) if m else meaning
        words.append({"arabic": r.get("arabic") or "", "bare": k, "translit": r.get("translit") or "", "meaning": meaning,
                      "unit": ", ".join(str(u) for u in r.get("units") or []), "from": frm, "state": state,
                      "why": heldk.get(k, "") if state == "held" else "", "her": bool(r["khouri"]), "audio": audio})
    tiers = collections.Counter(c["tier"] for c in cards)
    n_her = sum(1 for c in cards if "khouri" in c["Audio"])
    summary = {"lede": "Every word Dr. Khouri has taught in class so far, plus every Unit 1–4 word Lingco has audio for, "
                       "checked against your deck. Play each new clip of her voice and mark it; I recut anything you flag.",
               "stats": [{"k": "new notes", "v": len(cards)}, {"k": "Unit 4 chart words", "v": tiers.get("chart", 0)},
                         {"k": "her class words", "v": tiers.get("class", 0)}, {"k": "Lingco practice words", "v": tiers.get("practice", 0)},
                         {"k": "letter forms + digits", "v": tiers.get("letters", 0) + tiers.get("numbers", 0)},
                         {"k": "clips of her voice", "v": len(clips)}, {"k": "words already in Anki", "v": sum(1 for w in words if w["state"] == "had")}]}
    data = {"summary": summary, "clips": clips, "words": words}
    html = open(f"{BASE}/review/template.html").read().replace('/*__DATA__*/{"summary":{},"clips":[],"words":[]}',
                                                              json.dumps(data, ensure_ascii=False))
    open(f"{BASE}/review/index.html", "w").write(html)
    os.makedirs(f"{BASE}/review/clips", exist_ok=True)
    for c in clips:
        dst = f"{BASE}/review/clips/{c['file']}"
        if not os.path.exists(dst): os.link(f"{BASE}/clips/{c['file']}", dst) if os.stat(f"{BASE}/clips/{c['file']}").st_dev == os.stat(f"{BASE}/review").st_dev else __import__("shutil").copy(f"{BASE}/clips/{c['file']}", dst)
    print(f"index.html: {len(clips)} clips ({sum(1 for c in clips if c['flag'])} flagged), {len(words)} words")

if __name__ == "__main__":
    main()
