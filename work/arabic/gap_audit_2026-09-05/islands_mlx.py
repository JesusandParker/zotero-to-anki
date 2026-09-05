"""Silence-bounded energy islands inside [a,b] of <date>.wav, each transcribed by mlx-whisper in BOTH en and ar.
usage: islands_mlx.py DATE START END OUT.json [thr] [minpause]"""
import sys, json, math, os, re, array
import numpy as np
import mlx_whisper
OUT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures")
MODEL = "mlx-community/whisper-large-v3-turbo"
SR=16000; HOP=0.010; WIN=0.025
date, A, B, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
THR = float(sys.argv[5]) if len(sys.argv)>5 else -42.0
MINPAUSE = float(sys.argv[6]) if len(sys.argv)>6 else 0.10
LANGS = (sys.argv[7] if len(sys.argv)>7 else "ar").split(",")
raw = np.fromfile(f"{OUT}/{date}.wav", dtype=np.int16, offset=44)
def env(a,b):
    out=[]; t=a
    while t<b:
        i0=int(t*SR); i1=min(len(raw),int((t+WIN)*SR))
        if i1<=i0: break
        seg=raw[i0:i1].astype(np.float32)
        out.append((t,20*math.log10(math.sqrt(float((seg*seg).mean()))/32768+1e-9)))
        t+=HOP
    return out
def islands(a,b,thr,minpause,minlen=0.13):
    e=env(a,b); on=[t for t,d in e if d>thr]
    if not on: return []
    segs=[]; st=on[0]; prev=on[0]
    for t in on[1:]:
        if t-prev>minpause: segs.append((st,prev+HOP)); st=t
        prev=t
    segs.append((st,prev+HOP))
    return [(s,en) for s,en in segs if en-s>=minlen]
cues=[]
for b in open(f"{SRC}/{date} Elementary Arabic I.vtt",encoding="utf-8").read().split("\n\n"):
    m=re.search(r"(\d\d):(\d\d):(\d\d)\.(\d+) --> (\d\d):(\d\d):(\d\d)\.(\d+)",b)
    if not m: continue
    s=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))+int(m.group(4))/1000
    e=int(m.group(5))*3600+int(m.group(6))*60+int(m.group(7))+int(m.group(8))/1000
    txt=" ".join(l for l in b.split("\n") if "-->" not in l and not re.match(r"^[0-9a-f-]{20,}/",l)).strip()
    if txt: cues.append((s,e,re.sub(r"<[^>]+>","",txt)))
isl=islands(A,B,THR,MINPAUSE)
print(len(isl),"islands in",A,B, file=sys.stderr)
res=[]
for i,(s,e) in enumerate(isl):
    i0=max(0,int((s-0.095)*SR)); i1=min(len(raw),int((e+0.05)*SR))
    clip=raw[i0:i1].astype(np.float32)/32768.0
    peak=20*math.log10(float(np.abs(clip).max())+1e-9)
    tr={"en":"","ar":""}
    for lang in LANGS:
        r=mlx_whisper.transcribe(clip, path_or_hf_repo=MODEL, language=lang, task="transcribe",
                                 condition_on_previous_text=False, fp16=True, verbose=None,
                                 temperature=0.0, no_speech_threshold=0.8)
        tr[lang]=r["text"].strip()
    vt=" | ".join(t for cs,ce,t in cues if ce>=s-0.3 and cs<=e+0.3)[:200]
    res.append({"i":i,"s":round(s,2),"e":round(e,2),"d":round(e-s,2),"peak_dbfs":round(peak,1),"en":tr["en"],"ar":tr["ar"],"vtt":vt})
    print(f"{s:8.2f}-{e:8.2f} d={e-s:4.2f} pk={peak:5.1f} | EN: {tr['en'][:60]} | AR: {tr['ar'][:60]}", file=sys.stderr)
json.dump({"source":f"{date} {A}-{B} thr={THR} minpause={MINPAUSE} model={MODEL}","islands":res},open(out,"w"),ensure_ascii=False,indent=0)
