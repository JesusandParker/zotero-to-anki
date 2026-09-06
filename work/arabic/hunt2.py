#!/usr/bin/env python3
"""Find a target Arabic word inside running English speech — three stages, cheapest first.

  1. LOCATE  English word timestamps over the region: her Arabic word lands as a garbled
             English token at roughly the right time. Narrows ~15 s to ~1 s.
  2. SEGMENT Arabic word timestamps on a 3 s window around it: gives the word's approximate
             span directly. Drifts 100-300 ms, so it is a hint, not a cut.
  3. REFINE  Snap start/end to nearby ENERGY VALLEYS and try only those few cuts, gating each
             in Arabic. Survivors are then gated in English too.
Writes results after every target, unbuffered, so partial work is never lost.
"""
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
def tx(clip,lang,wts=False):
    return mlx_whisper.transcribe(clip,path_or_hf_repo=M,language=lang,task="transcribe",
        condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0,
        word_timestamps=wts,no_speech_threshold=0.8)
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
def envelope(d,a,b,hop=0.01,win=0.025):
    seg=raw(d)[int(a*SR):int(b*SR)].astype(np.float32)
    n=int(win*SR); h=int(hop*SR); k=max(1,(len(seg)-n)//h)
    idx=np.arange(k)[:,None]*h+np.arange(n)[None,:]
    idx=np.clip(idx,0,len(seg)-1)
    return a+np.arange(k)*hop, 20*np.log10(np.sqrt((seg[idx]**2).mean(axis=1))/32768+1e-9)
def valleys(d,a,b,lo=-46.0):
    """times where energy dips — plausible cut points"""
    t,db=envelope(d,a,b)
    out=[]
    for i in range(1,len(db)-1):
        if db[i]<=db[i-1] and db[i]<=db[i+1] and db[i]<lo: out.append(float(t[i]))
    # thin to >=40 ms apart
    keep=[]
    for v in out:
        if not keep or v-keep[-1]>0.04: keep.append(v)
    return keep

targets=json.load(open(sys.argv[1],encoding="utf-8")); OUT=sys.argv[2]
results={}
if os.path.exists(OUT):
    try: results=json.load(open(OUT,encoding="utf-8"))
    except Exception: results={}
for T in targets:
    slug=T["slug"]
    if slug in results and results[slug]: print(f"##### {slug} — already done, skipping",flush=True); continue
    want=[norm(w) for w in T["expect"].split("/")]
    cues=[c.lower() for c in T.get("cue","").split("/") if c]
    print(f"\n##### {slug}  want={T['expect']}",flush=True)
    cands=[]; tested=0
    for (date,a,b) in T["regions"]:
        seg=raw(date)[int(a*SR):int(b*SR)].astype(np.float32)/32768.0
        r=tx(seg,"en",wts=True)
        words=[w for s in r.get("segments",[]) for w in s.get("words",[])]
        spots=[]
        for w in words:
            tok=re.sub(r"[^a-z]","",w.get("word","").lower())
            if tok and any(c in tok or tok in c for c in cues):
                spots.append((w["start"]+a, w["end"]+a, tok))
        if not spots:
            toks=[re.sub(r"[^a-z]","",w.get("word","").lower()) for w in words]
            print(f"   [{date} {ts(a)}] no cue hit; saw: {[t for t in toks if t][:16]}",flush=True)
            continue
        for (ws,we,tok) in spots[:4]:
            print(f"   [{date}] cue '{tok}' {ts(ws)} ({ws:.2f}-{we:.2f})",flush=True)
            # stage 2: arabic word timestamps on a 3 s window
            w0,w1=max(0,ws-1.0), we+2.0
            ar=tx(raw(date)[int(w0*SR):int(w1*SR)].astype(np.float32)/32768.0,"ar",wts=True)
            aw=[w for s in ar.get("segments",[]) for w in s.get("words",[])]
            hints=[]
            for w in aw:
                if any(x in norm(w.get("word","")) for x in want):
                    hints.append((w["start"]+w0, w["end"]+w0))
            if not hints: hints=[(ws,we)]
            # stage 3: snap to valleys and test only those cuts
            for (hs,he) in hints[:2]:
                vs=[v for v in valleys(date,max(0,hs-0.6),hs+0.6)] or [hs-0.1,hs,hs+0.1]
                ve=[v for v in valleys(date,max(0,he-0.5),he+0.9)] or [he,he+0.1,he+0.2]
                for s0 in vs[:8]:
                    for e0 in ve[:8]:
                        dur=e0-s0
                        if not (T["dmin"]<=dur<=T["dmax"]): continue
                        clip=raw(date)[int(s0*SR):int(e0*SR)].astype(np.float32)/32768.0
                        if len(clip)<int(0.15*SR) or float(np.abs(clip).max())<0.02: continue
                        tested+=1
                        got=tx(clip,"ar")["text"].strip(); n=norm(got)
                        if any(n==w or (w in n and len(n)<=len(w)+3) for w in want):
                            pk=20*math.log10(float(np.abs(clip).max())+1e-9)
                            cands.append({"date":date,"s":round(float(s0),3),"e":round(float(e0),3),
                                "dur":round(float(dur),2),"peak":round(pk,1),"ar":got,"exact":n in want})
    seen=set(); uniq=[]
    for c in sorted(cands,key=lambda x:(-x["exact"],-x["peak"],abs(x["dur"]-0.65))):
        k=(c["date"],round(c["s"],1),round(c["dur"],1))
        if k in seen: continue
        seen.add(k); uniq.append(c)
    for c in uniq[:5]:
        clip=raw(c["date"])[int(c["s"]*SR):int(c["e"]*SR)].astype(np.float32)/32768.0
        c["en"]=tx(clip,"en")["text"].strip()
        print(f"     CAND {c['date']} {ts(c['s'])} s={c['s']} d={c['dur']} pk={c['peak']} "
              f"ar={c['ar'][:24]!r} en={c['en'][:32]!r}",flush=True)
    if not uniq: print(f"     nothing matched ({tested} cuts tested)",flush=True)
    results[slug]=uniq[:5]
    json.dump(results,open(OUT,"w"),ensure_ascii=False,indent=1)
print("\nHUNT DONE",flush=True)
