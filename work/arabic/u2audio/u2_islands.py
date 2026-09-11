"""Silence-bounded islands for MANY windows, model loaded once.
usage: u2_islands.py windows.json out.json"""
import sys, json, math, os, re
import numpy as np, mlx_whisper
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures")
MODEL="mlx-community/whisper-large-v3-turbo"; SR=16000; HOP=0.010; WIN=0.025
WINDOWS=json.load(open(sys.argv[1])); OUTF=sys.argv[2]
_cache={}
def wav(date):
    if date not in _cache: _cache[date]=np.fromfile(f"{HERE}/{date}.wav",dtype=np.int16,offset=44)
    return _cache[date]
def env(raw,a,b):
    out=[];t=a
    while t<b:
        i0=int(t*SR); i1=min(len(raw),int((t+WIN)*SR))
        if i1<=i0: break
        seg=raw[i0:i1].astype(np.float32)
        out.append((t,20*math.log10(math.sqrt(float((seg*seg).mean()))/32768+1e-9)))
        t+=HOP
    return out
def islands(raw,a,b,thr=-42.0,minpause=0.10,minlen=0.13):
    e=env(raw,a,b); on=[t for t,d in e if d>thr]
    if not on: return []
    segs=[];st=on[0];prev=on[0]
    for t in on[1:]:
        if t-prev>minpause: segs.append((st,prev+HOP)); st=t
        prev=t
    segs.append((st,prev+HOP))
    return [(s,en) for s,en in segs if en-s>=minlen]
res=[]
for w in WINDOWS:
    date,A,B,label=w["date"],w["s"],w["e"],w["label"]
    raw=wav(date)
    thr=w.get("thr",-42.0); mp=w.get("minpause",0.10)
    isl=islands(raw,A,B,thr,mp)
    print(f"\n##### {label}  {date} {A}-{B}  -> {len(isl)} islands",file=sys.stderr)
    for i,(s,e) in enumerate(isl):
        i0=max(0,int((s-0.095)*SR)); i1=min(len(raw),int((e+0.05)*SR))
        clip=raw[i0:i1].astype(np.float32)/32768.0
        peak=20*math.log10(float(np.abs(clip).max())+1e-9)
        tr={}
        for lang in ("ar","en"):
            r=mlx_whisper.transcribe(clip,path_or_hf_repo=MODEL,language=lang,task="transcribe",
                condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0,no_speech_threshold=0.8)
            tr[lang]=r["text"].strip()
        rec={"label":label,"date":date,"i":i,"s":round(s,2),"e":round(e,2),"d":round(e-s,2),
             "peak_dbfs":round(peak,1),"ar":tr["ar"],"en":tr["en"]}
        res.append(rec)
        print(f"  [{i:2}] {s:8.2f}-{e:8.2f} d={e-s:4.2f} pk={peak:5.1f} | AR: {tr['ar'][:45]} | EN: {tr['en'][:55]}",file=sys.stderr)
json.dump(res,open(OUTF,"w"),ensure_ascii=False,indent=1)
print(f"\nwrote {len(res)} islands -> {OUTF}",file=sys.stderr)
