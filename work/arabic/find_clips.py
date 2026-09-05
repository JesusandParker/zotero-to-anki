"""For each target word, list candidate islands (Khouri's own voice) ranked for cutting.
Her lapel peaks -3..-6 dBFS; students sit at -8..-18. A single-word island is what we want."""
import json, glob, re, os, sys
OUT=os.path.dirname(os.path.abspath(__file__))
DI=re.compile(r"[ً-ْٰـ‌‍؟،\.\!\?،]")
def norm(s):
    s=DI.sub("",s); s=re.sub("[أإآٱ]","ا",s); return s.replace("ى","ي").replace("ة","ه")
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
TARGETS=json.load(open(f"{OUT}/targets.json",encoding="utf-8"))
EN={}
def en_ctx(date,t,before=8,after=5):
    if date not in EN:
        EN[date]=json.load(open(f"{OUT}/mlx/{date}_en.json"))["segments"]
    return " ".join(x["text"].strip() for x in EN[date] if t-before<=x["start"]<=t+after)
isl=[]
for f in sorted(glob.glob(f"{OUT}/isl/*.json")):
    date=os.path.basename(f)[:10]
    for x in json.load(open(f,encoding="utf-8"))["islands"]:
        x["date"]=date; x["win"]=os.path.basename(f)[11:-5]; isl.append(x)
print(f"{len(isl)} islands total\n")
for t in TARGETS:
    pats=[norm(v.strip()) for v in t["match"].split("/")]
    hits=[]
    for x in isl:
        n=norm(x["ar"])
        toks=n.split()
        for p in pats:
            if re.search(r"(?<![ء-ي])"+re.escape(p)+r"(?![ء-ي])", n):
                # score: fewer tokens is better, duration in the plausible band, loud = her mic
                score = (len(toks)<=2)*3 + (len(toks)<=4)*2 + (t["dmin"]<=x["d"]<=t["dmax"])*3 + (x["peak_dbfs"]>-8)*2
                hits.append((score,x)); break
    hits.sort(key=lambda h:(-h[0], h[1]["d"]))
    print(f"===== {t['slug']}  ({t['tr']} = {t['gloss']})   {len(hits)} candidate islands")
    for score,x in hits[:8]:
        print(f"   [{score}] {x['date']} {ts(x['s'])}  s={x['s']:<8} d={x['d']:<5} pk={x['peak_dbfs']:<6} AR={x['ar'][:48]!r}")
        print(f"        EN@ {en_ctx(x['date'],x['s'])[:150]!r}")
    if not hits: print("   (none — needs a manual window or the publisher clip)")
