#!/usr/bin/env python3
"""Cut + gate, trying EVERY hunt candidate for a word until one survives the ENCODED check.

Two lessons this run taught, both now enforced here:
  * The hunt verifies a RAW slice; the card ships an ENCODED mp3. They can disagree, so the
    encoded file is the only thing that counts — and if the first candidate fails, try the next.
  * A one-letter difference from a sub-second clip is ASR noise, not a wrong word (harf ->
    'هارف و', tashkiil -> 'تشكين'). Judge by edit distance, and let the ENGLISH pass be what
    rules out a neighbouring filler word, which is what the gate is actually for.
"""
import json, os, sys, math, subprocess, re
import numpy as np, mlx_whisper
HERE=os.path.dirname(os.path.abspath(__file__)); FF=os.path.expanduser("~/.local/bin/ffmpeg")
M="mlx-community/whisper-large-v3-turbo"
DIA=re.compile(r"[ً-ْٰـ‌‍؟،\.\!\?]")
def norm(s):
    s=DIA.sub("",s); s=re.sub("[أإآٱ]","ا",s); return s.replace("ى","ي").replace("ة","ه").strip()
def lev(a,b):
    if a==b: return 0
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(prev[j]+1, cur[j-1]+1, prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
FILLER_RE=re.compile(r"^(so|and|or|if|now|okay|ok|well|then|but then|you know)\b[ ,]", re.I)
def filler(en):
    e=en.strip().strip(" .!?,'\"")
    return bool(FILLER_RE.match(e+" ")) or e.lower() in {"so","and","or","now","well","then","okay","ok"}
def encode(date,s,e,pad,out):
    dur=e-s
    subprocess.run([FF,"-y","-loglevel","error","-ss",f"{s:.3f}","-t",f"{dur:.3f}","-i",f"{HERE}/{date}.wav",
        "-af","afade=t=in:st=0:d=0.012,afade=t=out:st=%.3f:d=0.02"%max(0.0,dur-0.02),
        "-ac","1","-ar","44100","-c:a","pcm_s16le","/tmp/_c.wav"],check=True)
    subprocess.run([FF,"-y","-loglevel","error","-f","lavfi","-t",f"{pad:.3f}",
        "-i","anullsrc=r=44100:cl=mono","-c:a","pcm_s16le","/tmp/_s.wav"],check=True)
    open("/tmp/_l.txt","w").write("file '/tmp/_s.wav'\nfile '/tmp/_c.wav'\nfile '/tmp/_s.wav'\n")
    subprocess.run([FF,"-y","-loglevel","error","-f","concat","-safe","0","-i","/tmp/_l.txt",
        "-c:a","libmp3lame","-b:a","128k","-ar","44100","-ac","1",out],check=True)
def gate(path):
    subprocess.run([FF,"-y","-loglevel","error","-i",path,"-ac","1","-ar","16000","-c:a","pcm_s16le","/tmp/_g.wav"],check=True)
    raw=np.fromfile("/tmp/_g.wav",dtype=np.int16,offset=44).astype(np.float32)/32768.0
    o={}
    for l in ("ar","en"):
        o[l]=mlx_whisper.transcribe(raw,path_or_hf_repo=M,language=l,task="transcribe",
            condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0)["text"].strip()
    return o, len(raw)/16000, 20*math.log10(float(np.abs(raw).max())+1e-9)

picks=json.load(open(sys.argv[1],encoding="utf-8"))
hunt=json.load(open(f"{HERE}/hunt_out.json",encoding="utf-8"))
os.makedirs(f"{HERE}/clips2",exist_ok=True)
report=[]
for p in picks:
    slug=p["slug"]; want=[norm(w) for w in p["expect"].split("/")]
    tries=[{"s":p["s"],"e":p["e"]}]+[{"s":c["s"],"e":c["e"]} for c in hunt.get(slug,[])
                                     if abs(c["s"]-p["s"])>1e-6 or abs(c["e"]-p["e"])>1e-6]
    chosen=None
    for i,t in enumerate(tries):
        for pad in (0.09,0.14):
            out=f"{HERE}/clips2/{p['file']}"
            encode(p["date"],t["s"],t["e"],pad,out)
            o,dur,pk=gate(out)
            n=norm(o["ar"]); best=min((lev(n,w)/max(len(w),1),w) for w in want)
            ok = best[0]<=0.30 and not filler(o["en"])
            tag="PASS" if ok else "fail"
            print(f"  {tag} {slug:<16} try{i+1} pad={pad} {dur:4.2f}s | ar={o['ar'][:22]!r:26} "
                  f"(dist {best[0]:.2f}) | en={o['en'][:26]!r}",flush=True)
            if ok:
                chosen=dict(slug=slug,file=p["file"],date=p["date"],s=t["s"],e=t["e"],pad=pad,
                            dur=round(dur,2),peak=round(pk,1),ar=o["ar"],en=o["en"],
                            dist=round(best[0],3),why=p["why"]); break
        if chosen: break
    if chosen: report.append(chosen)
    else: report.append(dict(slug=slug,file=p["file"],gate="NO CANDIDATE SURVIVED",why=p["why"]))
    print(f"{'OK  ' if chosen else 'NONE'} {slug}",flush=True)
json.dump(report,open(f"{HERE}/fixes_gate.json","w"),ensure_ascii=False,indent=1)
ok=[r for r in report if r.get("dur")]
print(f"\n{len(ok)}/{len(report)} words have a clip that survives the encoded gate")
