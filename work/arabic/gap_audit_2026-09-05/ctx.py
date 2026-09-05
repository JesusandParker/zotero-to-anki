import json, sys, glob, os, re
OUT=os.path.dirname(os.path.abspath(__file__))
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
date,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
print(f"\n########## {date} {ts(a)}-{ts(b)}")
en=json.load(open(f"{OUT}/mlx/{date}_en.json"))["segments"]; ar=json.load(open(f"{OUT}/mlx/{date}_ar.json"))["segments"]
print("  EN full: "+" ".join(s["text"].strip() for s in en if a-3<=s["start"]<=b)[:700])
print("  AR full: "+" ".join(s["text"].strip() for s in ar if a-3<=s["start"]<=b)[:500])
for f in sorted(glob.glob(f"{OUT}/isl/{date}_*.json")):
    d=json.load(open(f,encoding="utf-8"))
    rows=[x for x in d["islands"] if a<=x["s"]<=b]
    if not rows: continue
    print(f"  islands from {os.path.basename(f)}:")
    for x in rows: print(f"    {ts(x['s'])} +{x['s']%60:04.1f}s d={x['d']:<4} pk={x['peak_dbfs']:<6} AR={x['ar'][:70]!r}" + (f"  EN={x['en'][:50]!r}" if x['en'] else ""))
