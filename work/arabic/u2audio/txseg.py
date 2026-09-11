import sys,json,os,math
import numpy as np, mlx_whisper
M="mlx-community/whisper-large-v3-turbo"
for n in sys.argv[1:]:
    raw=np.fromfile(f"vw_{n}.wav",dtype=np.int16,offset=44).astype(np.float32)/32768.0
    print(f"\n##### {n}  ({len(raw)/16000:.2f}s)")
    for lang in ("ar","en"):
        r=mlx_whisper.transcribe(raw,path_or_hf_repo=M,language=lang,task="transcribe",
            condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0)
        print(f"  [{lang}] {r['text'].strip()[:150]}")
        for s in r["segments"]:
            print(f"      {s['start']:6.2f}-{s['end']:6.2f}  {s['text'].strip()[:90]}")
