"""Scan the English mlx pass for Arabic words rendered in Latin letters."""
import json, re, sys, os
OUT = os.path.dirname(os.path.abspath(__file__))
def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d}"
PAT = re.compile(r"\b(tamam|tamaam|yalla|yallah|khalas|khala[sS]|tayyib|tayeb|sah|saH|mumtaz|mumtaaz|habibi|habibti|ahsant|ahsanti|aHsant|shukran|afwan|marhaba|ahlan|sahlan|salam|alaykum|alaikum|tasharrafna|ismi|ismuka|ismuki|hadratuka|hadratuki|ayna|wayn|shuu|shu|naam|laa|hal|askun|madinat|madina|dimashq|damascus|suriya|baba|abi|abu|abuka|abuki|tuut|toot|thawb|thob|taab|baat|tabut|taabuut|harf|hamza|alif|aleph|baa|taa|thaa|waaw|waw|yaa|fatha|damma|kasra|sukun|sukoon|tashkeel|tashkil|umm|huna|ayy|bil|arabi|inglizi|inglisi|kayf|kayfa|keef|sabah|masaa|inshallah|insha|allah|hamdulillah|yani|ya)\b", re.I)
for date in sys.argv[1:]:
    d=json.load(open(f"{OUT}/mlx/{date}_en.json"))
    print(f"\n######## {date}")
    for s in d["segments"]:
        m=PAT.findall(s["text"])
        if m: print(f"  {ts(s['start'])}  [{', '.join(sorted(set(x.lower() for x in m)))}]  {s['text'].strip()[:170]}")
