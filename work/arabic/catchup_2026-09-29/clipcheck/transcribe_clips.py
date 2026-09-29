"""Transcribe every Units 1-4 Lingco clip (vault mp3 formal/shaami/extras + fetched drill/writing videos)
in Arabic (and English for the long narrated videos). R63: a publisher clip is identified by transcribing it.
Output: clips_asr.json {file: {origin, lesson, dialect, dur, ar, en?}}"""
import json, os, subprocess, sys, numpy as np, mlx_whisper
BASE=os.path.expanduser('~/arabic-catchup'); VAULT=os.path.expanduser('~/arabic-vault/media')
MODEL="mlx-community/whisper-large-v3-turbo"
W=json.load(open(f'{BASE}/lingco_video/all_u14.json'))
out_p=f'{BASE}/clipcheck/clips_asr.json'
out=json.load(open(out_p)) if os.path.exists(out_p) else {}
def load(path):
    raw=subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',path,'-map','0:a:0','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
todo=[]
for w in W:
    if w.get('dialect')=='masri': continue
    f=w['file']
    p=f'{VAULT}/{f}'
    if not os.path.exists(p):
        p=f"{BASE}/lingco_video/aud/{f.replace('.mp3','.wav')}"
    if not os.path.exists(p): continue
    todo.append((f,p,w))
print(len(todo),'clips',file=sys.stderr)
for i,(f,p,w) in enumerate(todo):
    if f in out: continue
    x=load(p); dur=len(x)/16000
    rec={"origin":w.get('origin'),"lesson":w['lesson'],"dialect":w.get('dialect'),"entry":w.get('entry'),"dur":round(dur,2)}
    langs=['ar'] if dur<12 else ['ar','en']
    for lang in langs:
        r=mlx_whisper.transcribe(x,path_or_hf_repo=MODEL,language=lang,task='transcribe',condition_on_previous_text=False,
                                 temperature=0.0,word_timestamps=(dur>=12),verbose=None)
        rec[lang]=r['text'].strip()
        if dur>=12: rec[lang+'_segments']=[{"s":round(s['start'],2),"e":round(s['end'],2),"t":s['text'].strip()} for s in r['segments']]
    out[f]=rec
    if i%25==0:
        json.dump(out,open(out_p,'w'),ensure_ascii=False,indent=0); print(i,f,rec.get('ar','')[:40],file=sys.stderr)
json.dump(out,open(out_p,'w'),ensure_ascii=False,indent=0)
print('DONE',len(out),file=sys.stderr)
