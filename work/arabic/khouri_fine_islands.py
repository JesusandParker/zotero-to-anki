# fine-grained island view inside a window: envelope at 10ms hops, tighter pause, prints islands at two thresholds
import array,math,sys,json
SR=16000; HOP=0.010; WIN=0.025
_f=open("full.wav","rb");_f.seek(44);BUF=array.array("h");BUF.frombytes(_f.read());_f.close()
def env(a,b):
    out=[];t=a
    while t<b:
        i0=int(t*SR);i1=min(len(BUF),int((t+WIN)*SR))
        if i1<=i0: break
        ss=0;c=0
        for i in range(i0,i1,2): v=BUF[i];ss+=v*v;c+=1
        out.append((t,20*math.log10(math.sqrt(ss/max(c,1))/32768+1e-9)))
        t+=HOP
    return out
def islands(a,b,thr,minpause,minlen=0.08):
    e=env(a,b); on=[t for t,d in e if d>thr]
    if not on: return []
    segs=[];st=on[0];prev=on[0]
    for t in on[1:]:
        if t-prev>minpause: segs.append((st,prev+HOP)); st=t
        prev=t
    segs.append((st,prev+HOP))
    return [(s,en) for s,en in segs if en-s>=minlen]
a,b=float(sys.argv[1]),float(sys.argv[2])
for thr,mp in ((-42,0.10),(-38,0.06),(-34,0.05)):
    print(f"--- thr={thr} minpause={mp}")
    for s,en in islands(a,b,thr,mp): print(f"   {s:8.2f}-{en:8.2f} d={en-s:4.2f}")
# envelope print (coarse, 50ms) for eyeballing
import os
if os.environ.get("ENV")!="1": sys.exit(0)
print("--- envelope (50ms) ---")
e=env(a,b)
for i in range(0,len(e),5):
    t,d=e[i]; bar='#'*max(0,int((d+60)/2))
    print(f"{t:8.2f} {d:6.1f} {bar}")
