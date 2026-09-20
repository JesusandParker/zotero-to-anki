"""Write runs/<run>/provenance.jsonl in the chapter-10 record shape from the staged cards file."""
import json, hashlib, sys
cards=json.load(open('work/genetics/chapter_11_cards.json'))
run=open('work/genetics/run_dir.txt').read().strip()
with open(f'{run}/provenance.jsonl','w') as f:
    for i,c in enumerate(cards):
        rec={"card_index": i, "block": c.get('block'), "unit": c.get('_unit'),
             "from_idx": c.get('from_idx') or [], "kind": c.get('kind','text'),
             "text_sha1": hashlib.sha1(c['Text'].encode()).hexdigest()[:12],
             "verified_against": c.get('verified_against'), "verified_by": c.get('verified_by'),
             "needs_human_check": c.get('needs_human_check', False), "image": c.get('image'),
             "lexicon": c.get('lexicon'), "authorization": c.get('authorization'),
             "editor_note": c.get('_editor_notes'), "judge": c.get('_judge')}
        f.write(json.dumps(rec, ensure_ascii=False)+'\n')
print(f"provenance.jsonl: {len(cards)} records -> {run}")
