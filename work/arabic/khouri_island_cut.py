import array,math,sys,json,re
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
def islands(a,b,thr=-42.0,minpause=0.10,minlen=0.13):
    e=env(a,b); on=[t for t,d in e if d>thr]
    if not on: return []
    segs=[];st=on[0];prev=on[0]
    for t in on[1:]:
        if t-prev>minpause: segs.append((st,prev+HOP)); st=t
        prev=t
    segs.append((st,prev+HOP))
    return [(s,en) for s,en in segs if en-s>=minlen]
def peak(a,b):
    i0,i1=max(0,int(a*SR)),min(len(BUF),int(b*SR))
    m=0
    for i in range(i0,i1,3): m=max(m,abs(BUF[i]))
    return 20*math.log10(m/32768+1e-9)
# vtt lookup
cues=[]
import os
V=os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures/2026-08-27 Elementary Arabic I.vtt")
for b in open(V,encoding="utf-8").read().split("\n\n"):
    m=re.search(r"(\d\d):(\d\d):(\d\d)\.(\d+) --> (\d\d):(\d\d):(\d\d)\.(\d+)",b)
    if not m: continue
    s=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))+int(m.group(4))/1000
    e=int(m.group(5))*3600+int(m.group(6))*60+int(m.group(7))+int(m.group(8))/1000
    txt=" ".join(l for l in b.split("\n") if "-->" not in l and not re.match(r"^[0-9a-f-]{20,}/",l)).strip()
    if txt: cues.append((s,e,txt))
for name,a,b in json.load(open(sys.argv[1])):
    print(f"\n{'='*78}\n##### {name}   [{a} - {b}]")
    for s,e,t in cues:
        if e>=a and s<=b: print(f"    VTT {s:8.2f}-{e:8.2f}  {t}")
    print("   --- islands ---")
    for s,en in islands(a,b):
        print(f"    ISL {s:8.2f}-{en:8.2f}  d={en-s:4.2f}  peak={peak(s,en):5.1f}")
