"""Phone vs Teams audio for the same lecture: align by envelope cross-correlation, then compare
noise floor, speech level, SNR and bandwidth on the SAME stretches of her speech."""
import numpy as np, subprocess, sys, json
PY_SR=16000
def load(path, sr=PY_SR):
    raw=subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',path,'-map','0:a:0','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
def env(x,sr,hop=0.1):
    n=int(sr*hop); m=len(x)//n
    return 20*np.log10(np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))+1e-9)
def align(ea,eb):
    a=(ea-ea.mean())/ea.std(); b=(eb-eb.mean())/eb.std()
    c=np.correlate(a,b,'full'); lag=c.argmax()-(len(b)-1)
    return lag, c.max()/min(len(a),len(b))
res={}
LEC="/Users/parkerregner/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures"
VM="/Users/parkerregner/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
pairs={"2026-09-22":("20260922 111346-93B386C9.qta"),"2026-09-24":("20260924 111511-AC31C378.qta")}
for d,ph in pairs.items():
    T=load(f"{LEC}/{d} Elementary Arabic I.mp4",44100); P=load(f"{VM}/{ph}",44100)
    eT=env(T,44100); eP=env(P,44100)
    lag,score=align(eP,eT)   # phone index = teams index + lag
    # frames where BOTH are in her loud speech (teams speech = her lapel)
    L=min(len(eT),len(eP)-lag) if lag>=0 else min(len(eT)+lag,len(eP))
    t0=max(0,-lag); p0=max(0,lag)
    eT2=eT[t0:t0+L]; eP2=eP[p0:p0+L]
    def stats(e):
        return {"noise_floor_db":round(float(np.percentile(e,5)),1),"speech_db":round(float(np.percentile(e,95)),1),"snr_db":round(float(np.percentile(e,95)-np.percentile(e,5)),1)}
    # bandwidth: spectral rolloff 95% on her speech frames (teams loudest 20%)
    def rolloff(x,sr,frames):
        out=[]
        n=int(sr*0.1)
        for i in frames[:400]:
            seg=x[i*n:(i+1)*n]
            if len(seg)<n: continue
            S=np.abs(np.fft.rfft(seg*np.hanning(n)))**2; c=np.cumsum(S); f=np.fft.rfftfreq(n,1/sr)
            out.append(f[np.searchsorted(c,0.95*c[-1])])
        return round(float(np.median(out)))
    loud=np.where(eT2>np.percentile(eT2,80))[0]
    res[d]={"lag_s":lag*0.1,"xcorr":round(float(score),2),
            "teams":stats(eT2),"phone":stats(eP2),
            "teams_rolloff_hz":rolloff(T[t0*4410:],44100,loud),"phone_rolloff_hz":rolloff(P[p0*4410:],44100,loud),
            "teams_dur_min":round(len(T)/44100/60,1),"phone_dur_min":round(len(P)/44100/60,1)}
    print(d,json.dumps(res[d]))
json.dump(res,open('/Users/parkerregner/arabic-catchup/quality/compare.json','w'),indent=1)
