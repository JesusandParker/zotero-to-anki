"""Stage 2.5 helper: merge the edited unit files + LEX into one list, report coverage of marks 0-69,
list duplicate candidates (shared marks / shared answers), and write chapter_11_cards.json.
Usage: python3 consolidate.py [--write]"""
import json, glob, re, sys, hashlib, os
D='work/genetics/ch11_drafts'
CLOZE=re.compile(r'\{\{c(\d+)::(.*?)(?:::.*?)?\}\}')
units=['D1','D2','D3','D4','D5','D6','D7']
cards=[]; dropped=[]
for u in units:
    p=f'{D}/{u}_edited.json'
    if not os.path.exists(p):
        print(f"!! missing {p}"); continue
    for c in json.load(open(p)):
        v=c.get('_editor_verdict','PASS')
        if v=='DROP': dropped.append(c)
        else: cards.append(c)
lex=json.load(open(f'{D}/LEX_cards.json'))
cards+=lex
h=json.load(open('work/genetics/chapter_11_highlights.json'))
covered={}
for i,c in enumerate(cards):
    for m in c.get('from_idx') or []:
        covered.setdefault(m,[]).append(i)
missing=[i for i in range(len(h)) if i not in covered]
print(f"cards: {len(cards)} (dropped by editors: {len(dropped)}) | marks covered: {len(covered)}/{len(h)} | missing: {missing}")
for m in missing:
    print(f"   MISSING mark {m}: p{h[m]['page']} {h[m]['kind']} '{(h[m].get('highlight') or '')[:90]}'")
# lexicon fold-in candidates: a yellow card whose Text contains a purple term
terms={c['lexicon']['term'].rstrip('s').lower():i for i,c in enumerate(cards) if c.get('kind')=='lexicon'}
for i,c in enumerate(cards):
    if c.get('kind')=='lexicon': continue
    low=c['Text'].lower()
    for t,li in terms.items():
        if t in low and re.search(r'\{\{c\d+::[^}]*'+re.escape(t), low):
            print(f"   FOLD-IN CHECK: card {i} ({c.get('block')}) clozes purple term '{t}' (lexicon card {li})")
# duplicate candidates: shared cloze answers (normalised) across cards
ans={}
for i,c in enumerate(cards):
    for n,a in CLOZE.findall(c['Text']):
        k=re.sub(r'[^a-z0-9 ]','',a.lower()).strip()
        if len(k)>=4: ans.setdefault(k,set()).add(i)
dups={k:v for k,v in ans.items() if len(v)>1}
print(f"shared-answer candidates: {len(dups)}")
for k,v in sorted(dups.items(), key=lambda kv:-len(kv[1]))[:40]:
    print(f"   '{k}' -> cards {sorted(v)}")
if '--write' in sys.argv:
    for i,c in enumerate(cards):
        c['_unit_idx']=i
    json.dump(cards, open('work/genetics/chapter_11_cards.json','w'), indent=1, ensure_ascii=False)
    json.dump(dropped, open(f'{D}/editor_dropped.json','w'), indent=1, ensure_ascii=False)
    print("wrote work/genetics/chapter_11_cards.json and editor_dropped.json")
