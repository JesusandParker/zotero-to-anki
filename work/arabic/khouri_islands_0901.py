import array,math,sys,json,re,os
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
cues=[]
V=os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures/2026-09-01 Elementary Arabic I.vtt")
for b in open(V,encoding="utf-8").read().split("\n\n"):
    m=re.search(r"(\d\d):(\d\d):(\d\d)\.(\d+) --> (\d\d):(\d\d):(\d\d)\.(\d+)",b)
    if not m: continue
    s=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))+int(m.group(4))/1000
    e=int(m.group(5))*3600+int(m.group(6))*60+int(m.group(7))+int(m.group(8))/1000
    txt=" ".join(l for l in b.split("\n") if "-->" not in l and not re.match(r"^[0-9a-f-]{20,}/",l)).strip()
    if txt: cues.append((s,e,txt))
a,b=float(sys.argv[1]),float(sys.argv[2])
isl=islands(a,b)
out=[]
for s,en in isl:
    vt=[t for cs,ce,t in cues if ce>=s-0.3 and cs<=en+0.3]
    out.append({"s":round(s,2),"e":round(en,2),"d":round(en-s,2),"peak":round(peak(s,en),1),"vtt":" | ".join(vt)[:200]})
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False,indent=0)
print(len(isl),"islands in",a,b)
for o in out: print(f"{o['s']:8.2f}-{o['e']:8.2f} d={o['d']:4.2f} pk={o['peak']:5.1f}  {o['vtt'][:110]}")
