"""Gate EXACT candidate cuts in both languages (playbook §5 trap 1).
Input: JSON list of {slug,date,s,e}. Prints AR + EN for the exact bytes that would be cut."""
import sys, os, math, json
import numpy as np, mlx_whisper
OUT=os.path.dirname(os.path.abspath(__file__)); SR=16000
MODEL="mlx-community/whisper-large-v3-turbo"
cands=json.load(open(sys.argv[1],encoding="utf-8"))
raws={}
res=[]
for c in cands:
    d=c["date"]
    if d not in raws: raws[d]=np.fromfile(f"{OUT}/{d}.wav",dtype=np.int16,offset=44)
    raw=raws[d]
    i0=max(0,int((c["s"]-c.get("lead",0.095))*SR)); i1=min(len(raw),int((c["e"]+c.get("tail",0.05))*SR))
    clip=raw[i0:i1].astype(np.float32)/32768.0
    pk=20*math.log10(float(np.abs(clip).max())+1e-9)
    out={}
    for lang in ("ar","en"):
        r=mlx_whisper.transcribe(clip,path_or_hf_repo=MODEL,language=lang,task="transcribe",
                                 condition_on_previous_text=False,fp16=True,verbose=None,
                                 temperature=0.0,no_speech_threshold=0.8)
        out[lang]=r["text"].strip()
    c.update(ar=out["ar"], en=out["en"], peak=round(pk,1), dur=round(c["e"]-c["s"],2))
    res.append(c)
    print(f"{c['slug']:<18} {d} {c['s']:8.2f} d={c['dur']:<5} pk={pk:5.1f} | AR={out['ar'][:42]!r:46} | EN={out['en'][:52]!r}")
json.dump(res, open(sys.argv[2],"w"), ensure_ascii=False, indent=1)
