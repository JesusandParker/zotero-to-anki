"""Every note in the ARAB 101 tree -> inventory.json (arabic, translit, meaning, audio refs, suspended, tags, kind)."""
import json,urllib.request,re,collections
def ac(a,**p):
    r=json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765',json.dumps({"action":a,"version":6,"params":p}).encode())))
    if r['error']: raise Exception(f"{a}: {r['error']}")
    return r['result']
ROOT='all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I'
nids=ac('findNotes',query=f'"deck:{ROOT}"')
notes=ac('notesInfo',notes=nids)
cards=ac('cardsInfo',cards=[c for n in notes for c in n['cards']])
cmap=collections.defaultdict(list)
for c in cards: cmap[c['note']].append(c)
AR=re.compile(r'[؀-ۿ][؀-ۿً-ْٰ\s/،؟‌‍]*')
def clean(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>|&nbsp;',' ',s)).strip()
out=[]
for n in notes:
    f={k:v['value'] for k,v in n['fields'].items()}
    main=f.get('Text') or f.get('Front') or ''
    allf=' '.join(f.values())
    sounds=re.findall(r'\[sound:([^\]]+)\]',allf)
    audio_field=re.findall(r'\[sound:([^\]]+)\]',f.get('Audio',''))
    m=re.search(r'Transliteration:\s*(?:\{\{c\d::)?([^}<]+)',main)
    cz=re.findall(r'\{\{c(\d)::(.*?)\}\}',main)
    ar=[clean(x) for x in AR.findall(clean(re.sub(r'\{\{c\d::|\}\}','',main)))]
    cs=cmap[n['noteId']]
    out.append({"nid":n['noteId'],"model":n['modelName'],"deck":cs[0]['deckName'].split('::')[-1] if cs else None,
      "tags":n['tags'],"arabic":[a for a in ar if a],"translit":clean(m.group(1)) if m else None,
      "c2":[clean(x) for k,x in cz if k=='2'],"text":clean(re.sub(r'\{\{c\d::|\}\}','',main))[:300],
      "back":clean(f.get('Back Extra',f.get('Back','')))[:400],
      "audio_field":audio_field,"sounds":sounds,"n_cards":len(cs),
      "suspended":sum(c['queue']==-1 for c in cs),"new":sum(c['type']==0 for c in cs),
      "reviewed":sum(c['reps']>0 for c in cs)})
json.dump(out,open('anki_inventory.json','w'),ensure_ascii=False,indent=1)
print(len(out),'notes')
print(collections.Counter(o['deck'] for o in out))
print('with any audio:',sum(bool(o['sounds']) for o in out),' audio field filled:',sum(bool(o['audio_field']) for o in out))
print('fully suspended notes:',sum(o['suspended']==o['n_cards'] for o in out))
