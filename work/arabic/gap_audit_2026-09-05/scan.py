"""Scan the Arabic mlx pass for candidate vocabulary and print hits with English context."""
import json, re, sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
from merge import load_vtt, load_mlx, ts
DIAC = re.compile(r"[ً-ْٰـ‌‍؟،\.،؟!]")
def norm(s):
    s = DIAC.sub("", s)
    s = re.sub("[أإآٱ]", "ا", s); s = s.replace("ى","ي").replace("ة","ه")
    return s
CANDS = [l.split("#")[0].strip() for l in open(f"{OUT}/candidates.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
def scan(date, window=25):
    vtt=load_vtt(date); en=load_mlx(date,"en"); ar=load_mlx(date,"ar")
    hits={}
    for s,e,t in ar:
        nt=norm(t)
        for c in CANDS:
            word, gloss = (c.split("|")+[""])[:2]
            for variant in word.split("/"):
                v=norm(variant.strip())
                if v and re.search(r"(?<![ء-ي])"+re.escape(v)+r"(?![ء-ي])", nt):
                    hits.setdefault(c,[]).append((s,t))
                    break
    print(f"\n######## {date}: {len(hits)} candidates hit")
    for c in CANDS:
        if c not in hits: continue
        print(f"\n=== {c}  ({len(hits[c])} hits)")
        for s,t in hits[c][:14]:
            ctx=" ".join(x for st,_,x in en if s-window<=st<=s+8)
            print(f"  {ts(s)}  AR: {t[:110]}\n           EN: {ctx[:230]}")
if __name__=="__main__":
    for d in sys.argv[1:]: scan(d)
