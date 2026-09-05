#!/usr/bin/env python3
"""Cut Dr. Khouri's own voice for the 2026-09-05 gap-audit batch, then RE-GATE the final mp3.
Playbook 5: cut exactly one silence-bounded island, ~95 ms of REAL room lead-in (never adelay),
and gate the encoded file in BOTH languages before it is allowed near a card."""
import json, os, subprocess, math, sys
import numpy as np, mlx_whisper
HERE=os.path.dirname(os.path.abspath(__file__)); OUTD=os.path.join(HERE,"clips"); os.makedirs(OUTD,exist_ok=True)
FF=os.path.expanduser("~/.local/bin/ffmpeg"); M="mlx-community/whisper-large-v3-turbo"; LEAD=0.095; TAIL=0.05
SPEC=json.load(open(os.path.join(HERE,"clip_spec.json"),encoding="utf-8"))
log=[]
for c in SPEC:
    src=os.path.join(HERE,f"{c['date']}.wav")
    out=os.path.join(OUTD,f"arabic_khouri_{c['slug']}.mp3")
    ss=max(0.0,c["s"]-LEAD); dur=(c["e"]+TAIL)-ss
    subprocess.run([FF,"-y","-loglevel","error","-ss",f"{ss:.3f}","-t",f"{dur:.3f}","-i",src,
                    "-af","afade=t=in:st=0:d=0.02,afade=t=out:st=%.3f:d=0.03" % max(0.0,dur-0.03),
                    "-c:a","libmp3lame","-b:a","96k","-ar","44100","-ac","1",out],check=True)
    # re-gate the ENCODED file, both languages
    wav="/tmp/_g.wav"
    subprocess.run([FF,"-y","-loglevel","error","-i",out,"-ac","1","-ar","16000","-c:a","pcm_s16le",wav],check=True)
    raw=np.fromfile(wav,dtype=np.int16,offset=44).astype(np.float32)/32768.0
    pk=20*math.log10(float(np.abs(raw).max())+1e-9)
    tr={}
    for lang in ("ar","en"):
        r=mlx_whisper.transcribe(raw,path_or_hf_repo=M,language=lang,task="transcribe",
                                 condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0)
        tr[lang]=r["text"].strip()
    rec=dict(slug=c["slug"],file=os.path.basename(out),date=c["date"],s=c["s"],e=c["e"],
             dur=round(len(raw)/16000,2),peak_dbfs=round(pk,1),ar=tr["ar"],en=tr["en"],
             expect=c["expect"],why=c.get("why",""),bytes=os.path.getsize(out))
    log.append(rec)
    print(f"{c['slug']:<18} {rec['dur']:4.2f}s pk={pk:5.1f} | AR={tr['ar'][:38]!r:42} | EN={tr['en'][:40]!r}")
json.dump(log,open(os.path.join(HERE,"clips_gate.json"),"w"),ensure_ascii=False,indent=1)
print(f"\n{len(log)} clips written to {OUTD}")
