#!/usr/bin/env python3
"""Find a target Arabic word INSIDE running English speech.

Two stages, because a silence-bounded island is the wrong unit when she never pauses:
  1. LOCATE — run the English pass with word timestamps over the search region. Her Arabic
     word lands as a garbled English token at roughly the right time (timing is reliable
     even when the spelling is not), so this narrows ~15 s to a ~1 s neighbourhood.
  2. SWEEP — inside that neighbourhood only, try many (start, duration) cuts, transcribe
     each forcing Arabic, and keep the ones that read as the target word. Survivors are
     then gated in English too.
usage: hunt.py targets.json out.json
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
def tx(clip, lang, wts=False):
    r=mlx_whisper.transcribe(clip, path_or_hf_repo=M, language=lang, task="transcribe",
        condition_on_previous_text=False, fp16=True, verbose=None, temperature=0.0,
        word_timestamps=wts, no_speech_threshold=0.8)
    return r
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"

targets=json.load(open(sys.argv[1],encoding="utf-8"))
results={}
for T in targets:
    slug=T["slug"]; want=[norm(w) for w in T["expect"].split("/")]
    print(f"\n##### {slug}  want={T['expect']}  cue={T.get('cue','')}")
    best=[]
    for (date,a,b) in T["regions"]:
        seg=raw(date)[int(a*SR):int(b*SR)].astype(np.float32)/32768.0
        # ---- stage 1: locate via English word timestamps
        r=tx(seg,"en",wts=True)
        words=[w for s in r.get("segments",[]) for w in s.get("words",[])]
        cues=[c.lower() for c in T.get("cue","").split("/") if c]
        spots=[]
        for w in words:
            tok=re.sub(r"[^a-z]","",w.get("word","").lower())
            if not tok: continue
            if any(c in tok or tok in c for c in cues) if cues else False:
                spots.append((w["start"]+a, w["end"]+a, tok))
        if not spots and cues:
            print(f"   [{date} {ts(a)}-{ts(b)}] no cue token; words seen: "
                  f"{[re.sub(chr(91)+'^a-z'+chr(93),'',w.get('word','').lower()) for w in words][:14]}")
            continue
        if not spots: spots=[(a,b,"(whole region)")]
        # ---- stage 2: fine sweep around each spot
        for (ws,we,tok) in spots:
            print(f"   [{date}] cue '{tok}' at {ts(ws)} {ws:.2f}-{we:.2f}")
            for st in np.arange(ws-0.45, ws+0.45, 0.06):
                for dur in np.arange(T["dmin"], T["dmax"]+0.001, 0.10):
                    i0=max(0,int((st)*SR)); i1=min(len(raw(date)),int((st+dur)*SR))
                    if i1-i0 < int(0.15*SR): continue
                    clip=raw(date)[i0:i1].astype(np.float32)/32768.0
                    if float(np.abs(clip).max())<0.02: continue
                    ar=tx(clip,"ar")["text"].strip()
                    n=norm(ar)
                    if any(n==w or (w in n and len(n)<=len(w)+3) for w in want):
                        pk=20*math.log10(float(np.abs(clip).max())+1e-9)
                        best.append({"date":date,"s":round(float(st),3),"e":round(float(st+dur),3),
                                     "dur":round(float(dur),2),"peak":round(pk,1),"ar":ar,"exact":n in want})
    # dedupe + rank: exact match first, then loudest, then middling duration
    seen=set(); uniq=[]
    for c in sorted(best,key=lambda x:(-x["exact"], -x["peak"], abs(x["dur"]-0.6))):
        k=(c["date"],round(c["s"],1),round(c["dur"],1))
        if k in seen: continue
        seen.add(k); uniq.append(c)
    # gate the top few in English too
    for c in uniq[:6]:
        clip=raw(c["date"])[int(c["s"]*SR):int(c["e"]*SR)].astype(np.float32)/32768.0
        c["en"]=tx(clip,"en")["text"].strip()
        print(f"     CAND {c['date']} {ts(c['s'])} s={c['s']} d={c['dur']} pk={c['peak']} "
              f"ar={c['ar'][:26]!r} en={c['en'][:34]!r}")
    results[slug]=uniq[:6]
    if not uniq: print("     (nothing matched)")
json.dump(results,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
print("\nwrote",sys.argv[2])
