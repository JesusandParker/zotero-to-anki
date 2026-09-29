"""Flatten ARAB 101 into one deck per unit (Unit 01, Unit 02, ...).
The old subdeck each note came from is kept as an ARAB101::from::* tag. Backup of every
card's deck + scheduling is written first to reorg_units_2026-09-29_backup.json."""
import json,urllib.request,re,collections,sys
def ac(a,**p):
    r=json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765',json.dumps({"action":a,"version":6,"params":p}).encode())))
    if r['error']: raise Exception(f"{a}: {r['error']}")
    return r['result']
ROOT='all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I'
FROM={'Book Highlights':'book','Khouri Tuesday 2026-09-01':'class-2026-09-01',
      'Khouri Thursday 2026-09-03':'class-2026-09-03','Khouri Spoken 2026-09-05':'class-spoken-2026-09-05',
      'Quiz Cram 2026-09-22':'quiz-prep-2026-09-22'}
SCHED=('deckName','queue','type','due','interval','factor','reps','lapses','left','mod')
cards=ac('cardsInfo',cards=ac('findCards',query=f'"deck:{ROOT}"'))
json.dump([{k:c[k] for k in ('cardId','note','ord')+SCHED} for c in cards],open('reorg_units_2026-09-29_backup.json','w'),ensure_ascii=False,indent=0)
preset=ac('getDeckConfig',deck=ROOT)['id']
moves=collections.defaultdict(list); tags=collections.defaultdict(set)
for c in cards:
    m=re.fullmatch(re.escape(ROOT)+r'::Unit (\d+)::(.+)',c['deckName'])
    if not m: sys.exit(f"unexpected deck {c['deckName']}")
    moves[f"{ROOT}::Unit {int(m[1]):02d}"].append(c['cardId'])
    tags[FROM[m[2]]].add(c['note'])
for d,cids in moves.items():
    ac('createDeck',deck=d); ac('setDeckConfigId',decks=[d],configId=preset); ac('changeDeck',cards=cids,deck=d)
    print(f"{d[len(ROOT)+2:]}: {len(cids)} cards")
for slug,nids in tags.items(): ac('addTags',notes=list(nids),tags=f'ARAB101::from::{slug}')
# alif position card: tagged Unit 3 by the cram build, but alif is a Unit 2 letter and it lives in Unit 2
ac('replaceTags',notes=[1790070935881],tag_to_replace='arabic-u3',replace_with_tag='arabic-u2')
old=[d for d in ac('deckNames') if re.fullmatch(re.escape(ROOT)+r'::Unit \d(::.+)?',d)]
left={d:len(ac('findCards',query=f'"deck:{d}"')) for d in old}
if any(left.values()): sys.exit(f"old decks not empty, not deleting: {left}")
ac('deleteDecks',decks=old,cardsToo=True); print('deleted empty:',[d[len(ROOT)+2:] for d in old])
