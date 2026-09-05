"""Scan island JSONs (dual-language) for candidate words; print island hits with both transcriptions + VTT."""
import json, re, sys, os, glob
OUT = os.path.dirname(os.path.abspath(__file__))
DIAC = re.compile(r"[ً-ْٰـ‌‍؟،\.!]")
def norm(s):
    s = DIAC.sub("", s); s = re.sub("[أإآٱ]", "ا", s); return s.replace("ى","ي").replace("ة","ه")
CANDS = [l.split("#")[0].strip() for l in open(f"{OUT}/candidates.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
files = sys.argv[1:] or sorted(glob.glob(f"{OUT}/isl/*.json"))
_en={}
def en_ctx(date, t, before=6, after=4):
    if date not in _en:
        p=f"{OUT}/mlx/{date}_en.json"; _en[date]=json.load(open(p))["segments"] if os.path.exists(p) else []
    return " ".join(x["text"].strip() for x in _en[date] if t-before<=x["start"]<=t+after)
for f in files:
    d = json.load(open(f, encoding="utf-8")); isl = d["islands"]
    print(f"\n######## {os.path.basename(f)}  ({len(isl)} islands)  {d['source'][:60]}")
    for c in CANDS:
        word, gloss = (c.split("|")+[""])[:2]
        hits=[]
        for x in isl:
            nt = norm(x["ar"])
            if any(re.search(r"(?<![ء-ي])"+re.escape(norm(v.strip()))+r"(?![ء-ي])", nt) for v in word.split("/") if v.strip()):
                hits.append(x)
        if not hits: continue
        # drop obvious translation-hallucinations: long English islands whose EN pass has no Arabic-ish token
        print(f"  == {word} ({gloss}): {len(hits)}")
        for x in hits[:10]:
            date=os.path.basename(f)[:10]
            en = x['en'] or en_ctx(date, x['s'])
            print(f"     {ts(x['s'])} d={x['d']:<4} pk={x['peak_dbfs']:<6} AR={x['ar'][:55]!r:60} EN={en[:90]!r}")
