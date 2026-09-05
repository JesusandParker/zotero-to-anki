"""Fine islands inside a window, each transcribed in BOTH en and ar (playbook §5 trap 1).
usage: gate.py DATE START END [thr] [minpause] [minlen]"""
import sys, os, math, json
import numpy as np, mlx_whisper
OUT=os.path.dirname(os.path.abspath(__file__)); SR=16000; HOP=0.010; WIN=0.025
MODEL="mlx-community/whisper-large-v3-turbo"
date,A,B=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
THR=float(sys.argv[4]) if len(sys.argv)>4 else -42.0
MP=float(sys.argv[5]) if len(sys.argv)>5 else 0.10
ML=float(sys.argv[6]) if len(sys.argv)>6 else 0.13
raw=np.fromfile(f"{OUT}/{date}.wav",dtype=np.int16,offset=44)
seg=raw[int(A*SR):int(B*SR)].astype(np.float32); n=int(WIN*SR); h=int(HOP*SR); k=(len(seg)-n)//h
idx=np.arange(k)[:,None]*h+np.arange(n)[None,:]
db=20*np.log10(np.sqrt((seg[idx]**2).mean(axis=1))/32768+1e-9); on=np.where(db>THR)[0]
if len(on)==0: print("no speech"); sys.exit()
t=on*HOP+A; cuts=np.where(np.diff(t)>MP)[0]
starts=np.concatenate([[t[0]],t[cuts+1]]); ends=np.concatenate([t[cuts]+HOP,[t[-1]+HOP]])
def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d}"
for s,e in zip(starts,ends):
    if e-s < ML: continue
    i0=max(0,int((s-0.095)*SR)); i1=min(len(raw),int((e+0.05)*SR))
    clip=raw[i0:i1].astype(np.float32)/32768.0
    pk=20*math.log10(float(np.abs(clip).max())+1e-9)
    out={}
    for lang in ("ar","en"):
        r=mlx_whisper.transcribe(clip,path_or_hf_repo=MODEL,language=lang,task="transcribe",
                                 condition_on_previous_text=False,fp16=True,verbose=None,
                                 temperature=0.0,no_speech_threshold=0.8)
        out[lang]=r["text"].strip()
    print(f"{s:9.2f}-{e:8.2f} ({ts(s)}) d={e-s:4.2f} pk={pk:5.1f} | AR={out['ar'][:52]!r:56} | EN={out['en'][:60]!r}")
