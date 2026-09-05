"""Gate EVERY mp3 that will ship, in both languages. This is the authoritative log."""
import glob, os, json, subprocess, math
import numpy as np, mlx_whisper
HERE=os.path.dirname(os.path.abspath(__file__)); M="mlx-community/whisper-large-v3-turbo"
FF=os.path.expanduser("~/.local/bin/ffmpeg")
EXPECT=json.load(open(os.path.join(HERE,"expect.json"),encoding="utf-8"))
out=[]
for f in sorted(glob.glob(os.path.join(HERE,"clips","*.mp3"))):
    b=os.path.basename(f)
    subprocess.run([FF,"-y","-loglevel","error","-i",f,"-ac","1","-ar","16000","-c:a","pcm_s16le","/tmp/_gf.wav"],check=True)
    raw=np.fromfile("/tmp/_gf.wav",dtype=np.int16,offset=44).astype(np.float32)/32768.0
    tr={}
    for lang in ("ar","en"):
        r=mlx_whisper.transcribe(raw,path_or_hf_repo=M,language=lang,task="transcribe",
                                 condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0)
        tr[lang]=r["text"].strip()
    rec=dict(file=b, dur=round(len(raw)/16000,2), peak_dbfs=round(20*math.log10(float(np.abs(raw).max())+1e-9),1),
             ar=tr["ar"], en=tr["en"], expect=EXPECT.get(b,""), bytes=os.path.getsize(f))
    ok = EXPECT.get(b,"") and (EXPECT[b] in tr["ar"].replace("ً","").replace("َ","").replace("ُ",""))
    rec["gate"]="PASS" if ok else "REVIEW"
    out.append(rec)
    print(f"{rec['gate']:<7} {b:<40} {rec['dur']:4.2f}s pk={rec['peak_dbfs']:5.1f} | AR={tr['ar'][:30]!r:34} | EN={tr['en'][:34]!r}")
json.dump(out,open(os.path.join(HERE,"clips_gate.json"),"w"),ensure_ascii=False,indent=1)
print(f"\n{sum(1 for r in out if r['gate']=='PASS')}/{len(out)} PASS")
