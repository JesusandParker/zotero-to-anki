import sys,math,json
import numpy as np, mlx_whisper
M="mlx-community/whisper-large-v3-turbo"; SR=16000; HOP=0.010; WIN=0.025
def env(raw,a,b):
    o=[];t=a
    while t<b:
        i0=int(t*SR);i1=min(len(raw),int((t+WIN)*SR))
        if i1<=i0:break
        s=raw[i0:i1].astype(np.float32)
        o.append((t,20*math.log10(math.sqrt(float((s*s).mean()))/32768+1e-9)));t+=HOP
    return o
def islands(raw,a,b,thr,mp,ml=0.12):
    e=env(raw,a,b);on=[t for t,d in e if d>thr]
    if not on:return []
    segs=[];st=on[0];pv=on[0]
    for t in on[1:]:
        if t-pv>mp: segs.append((st,pv+HOP)); st=t
        pv=t
    segs.append((st,pv+HOP))
    return [(s,e2) for s,e2 in segs if e2-s>=ml]
for n in sys.argv[1:]:
    raw=np.fromfile(f"vw_{n}.wav",dtype=np.int16,offset=44)
    dur=len(raw)/SR
    print(f"\n##### {n} ({dur:.2f}s)")
    for thr,mp in ((-42.0,0.10),(-38.0,0.06)):
        isl=islands(raw,0,dur,thr,mp)
        print(f"  -- thr={thr} minpause={mp}: {len(isl)} islands")
        for i,(s,e) in enumerate(isl):
            i0=max(0,int((s-0.06)*SR)); i1=min(len(raw),int((e+0.05)*SR))
            c=raw[i0:i1].astype(np.float32)/32768.0
            pk=20*math.log10(float(np.abs(c).max())+1e-9)
            r=mlx_whisper.transcribe(c,path_or_hf_repo=M,language="ar",task="transcribe",
                condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0,no_speech_threshold=0.8)
            print(f"     [{i}] {s:6.2f}-{e:6.2f} d={e-s:4.2f} pk={pk:5.1f} | {r['text'].strip()[:60]}")
