"""Merge Teams VTT + mlx en + mlx ar into one timeline per lecture, bucketed by 20 s."""
import json, re, sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures")
def load_vtt(date):
    cues=[]
    for b in open(f"{SRC}/{date} Elementary Arabic I.vtt",encoding="utf-8").read().split("\n\n"):
        m=re.search(r"(\d\d):(\d\d):(\d\d)\.(\d+) --> (\d\d):(\d\d):(\d\d)\.(\d+)",b)
        if not m: continue
        s=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))+int(m.group(4))/1000
        txt=" ".join(l for l in b.split("\n") if "-->" not in l and not re.match(r"^[0-9a-f-]{20,}/",l) and not l.strip().isdigit()).strip()
        txt=re.sub(r"<[^>]+>","",txt)
        if txt: cues.append((s,txt))
    return cues
def load_mlx(date,lang):
    p=f"{OUT}/mlx/{date}_{lang}.json"
    if not os.path.exists(p): return []
    d=json.load(open(p))
    return [(s["start"],s["end"],s["text"].strip()) for s in d["segments"]]
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
def merge(date,bucket=20):
    vtt=load_vtt(date); en=load_mlx(date,"en"); ar=load_mlx(date,"ar")
    end=max([s for s,_ in vtt]+[e for _,e,_ in en]+[e for _,e,_ in ar]+[0])+bucket
    lines=[]
    for b0 in range(0,int(end),bucket):
        b1=b0+bucket
        v=" ".join(t for s,t in vtt if b0<=s<b1)
        e=" ".join(t for s,_,t in en if b0<=s<b1)
        a=" ".join(t for s,_,t in ar if b0<=s<b1)
        if not (v or e or a): continue
        lines.append(f"[{ts(b0)}]\n  VTT: {v}\n  EN : {e}\n  AR : {a}")
    open(f"{OUT}/merged_{date}.txt","w",encoding="utf-8").write("\n".join(lines))
    print(date, "buckets:", len(lines), "en segs:", len(en), "ar segs:", len(ar))
if __name__=="__main__":
    for d in sys.argv[1:]: merge(d)
