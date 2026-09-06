#!/usr/bin/env python3
"""Fallback for words hunt2 missed: a DENSE grid, but only inside very tight windows
around utterance times read off the English pass. Bounded cost, no cue/valley dependency."""
import sys, os, json, math, re
import numpy as np, mlx_whisper
HERE=os.path.dirname(os.path.abspath(__file__)); SR=16000
M="mlx-community/whisper-large-v3-turbo"
DIA=re.compile(r"[ً-ْٰـ‌‍؟،\.\!\?]")
def norm(s):
    s=DIA.sub("",s); s=re.sub("[أإآٱ]","ا",s); return s.replace("ى","ي").replace("ة","ه").strip()
RAW={}
def raw(d):
    if d not in RAW: RAW[d]=np.fromfile(f"{HERE}/{d}.wav",dtype=np.int16,offset=44)
    return RAW[d]
def tx(c,l): return mlx_whisper.transcribe(c,path_or_hf_repo=M,language=l,task="transcribe",
    condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0,no_speech_threshold=0.8)["text"].strip()
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
targets=json.load(open(sys.argv[1],encoding="utf-8")); OUT=sys.argv[2]
res=json.load(open(OUT,encoding="utf-8")) if os.path.exists(OUT) else {}
for T in targets:
    slug=T["slug"]
    if res.get(slug): print(f"##### {slug} already has hits, skip",flush=True); continue
    want=[norm(w) for w in T["expect"].split("/")]
    print(f"\n##### {slug} DENSE  want={T['expect']}",flush=True)
    cands=[]; tested=0
    for (date,c) in T["at"]:                     # c = a moment she says it, from the English pass
        R=T.get("radius",0.60); STEP=T.get("step",0.075)
        for s0 in np.arange(c-R, c+R, STEP):
            for dur in np.arange(T["dmin"], T["dmax"]+0.001, T.get("dstep",0.12)):
                i0=int(s0*SR); i1=int((s0+dur)*SR)
                if i0<0 or i1>len(raw(date)): continue
                clip=raw(date)[i0:i1].astype(np.float32)/32768.0
                if float(np.abs(clip).max())<0.02: continue
                tested+=1
                got=tx(clip,"ar"); n=norm(got)
                if any(n==w or (w in n and len(n)<=len(w)+3) for w in want):
                    pk=20*math.log10(float(np.abs(clip).max())+1e-9)
                    cands.append({"date":date,"s":round(float(s0),3),"e":round(float(s0+dur),3),
                        "dur":round(float(dur),2),"peak":round(pk,1),"ar":got,"exact":n in want})
    seen=set(); uniq=[]
    for x in sorted(cands,key=lambda z:(-z["exact"],-z["peak"],abs(z["dur"]-0.7))):
        k=(x["date"],round(x["s"],1),round(x["dur"],1))
        if k in seen: continue
        seen.add(k); uniq.append(x)
    for x in uniq[:5]:
        clip=raw(x["date"])[int(x["s"]*SR):int(x["e"]*SR)].astype(np.float32)/32768.0
        x["en"]=tx(clip,"en")
        print(f"     CAND {x['date']} {ts(x['s'])} s={x['s']} d={x['dur']} pk={x['peak']} "
              f"ar={x['ar'][:24]!r} en={x['en'][:32]!r}",flush=True)
    if not uniq: print(f"     nothing ({tested} cuts tested)",flush=True)
    res[slug]=uniq[:5]; json.dump(res,open(OUT,"w"),ensure_ascii=False,indent=1)
print("\nDENSE DONE",flush=True)
