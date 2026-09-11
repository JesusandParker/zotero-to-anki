import sys,json,subprocess,os,math
import numpy as np, mlx_whisper
FF=os.path.expanduser("~/.local/bin/ffmpeg"); M="mlx-community/whisper-large-v3-turbo"
V="/Users/parkerregner/arabic-vault/media"
out=[]
for name in sys.argv[1:]:
    p=os.path.join(V,name)
    w="/tmp/_tx.wav"
    subprocess.run([FF,"-y","-loglevel","error","-i",p,"-ac","1","-ar","16000","-c:a","pcm_s16le",w],check=True)
    raw=np.fromfile(w,dtype=np.int16,offset=44).astype(np.float32)/32768.0
    d=len(raw)/16000
    r=mlx_whisper.transcribe(raw,path_or_hf_repo=M,language="ar",task="transcribe",
        condition_on_previous_text=False,fp16=True,verbose=None,temperature=0.0)
    out.append({"file":name,"dur":round(d,2),"ar":r["text"].strip()})
    print(f"{name:26} {d:5.2f}s  {r['text'].strip()[:95]}",flush=True)
json.dump(out,open("le_tx.json","w"),ensure_ascii=False,indent=1)
