#!/usr/bin/env python3
"""Append Dr. Khouri's own-voice clip (and at most one coaching line) to the nine
Unit 1 vocab notes that already exist.

INSERT-ONLY. `Back Extra` is `edited` and `Audio` is `unknown` in the authorship store,
so neither may be rewritten (SKILL.md step 4). This script therefore:
  - never touches Text, Audio, or any of Parker's own fields;
  - inserts a new block immediately BEFORE the trailing <img> reference line, so every
    pre-existing character survives in its original order;
  - asserts that survival before sending anything.
Run with --apply to write; default is a dry run.
"""
import json, subprocess, sys, re

APPLY = "--apply" in sys.argv
AC = "localhost:8765"

def ac(action, params=None):
    d = {"action": action, "version": 6}
    if params: d["params"] = params
    r = subprocess.run(["curl", "-s", AC, "-X", "POST", "-d", json.dumps(d)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    if j.get("error"): raise RuntimeError(f"{action}: {j['error']}")
    return j["result"]

# (clip file, label for the clip line, optional coaching line)
# Only clips that passed the both-language gate appear here. marHaban has NO entry:
# Dr. Khouri never says it outside a running English sentence, so there is no clean cut
# and the note keeps its Alif Baa audio instead.
PLAN = {
 1786229800997: ("salaam_alaykum", "Dr. Khouri in class, 27 Aug",
   'Pitfall: the <i>c</i> is <i>cayn</i>, made down in the throat. Her trick: say "ah", '
   'then start to shock yourself — but only a little.'),
 1786229801072: ("ahlan", "Dr. Khouri in class, 27 Aug",
   'Distinguish: she also teaches Levantine <i>ahla</i> and <i>ahlain</i>, but told the class '
   'to just use this one — "Ahlan is OK. Take that one."'),
 1786229801147: ("ahla_wa_sahla", "Dr. Khouri in class, 27 Aug, saying the Levantine form",
   'Why: <i>sahlan</i> adds no new meaning — the doubling IS the warmth. Repetition is how '
   'emphasis works in Arabic culture.'),
 1786229801295: ("ana", "Dr. Khouri in class, 27 Aug",
   'Pitfall: there is no "am" in Arabic — say <i>ana Parker</i>, never "ana am Parker."'),
 1786229801372: ("ismi", "Dr. Khouri in class, 27 Aug",
   'Distinguish: Dr. Khouri writes it <i>ismi</i> on her slides; the book\'s Formal column '
   'has <i>ismii</i>.'),
 1786229801447: ("min", "Dr. Khouri in class, 27 Aug", None),
 1786229801521: ("ana_min_madiinat", "Dr. Khouri in class, 27 Aug, saying the whole frame",
   'Pitfall: the final <i>-t</i> is pronounced only under possession — <i>madiinat Lynchburg</i>, '
   'but bare <i>madiina</i> standing on its own.'),
 1786229801596: ("fii", "Dr. Khouri in class, 27 Aug", None),
}

notes = {n["noteId"]: n for n in ac("notesInfo", {"notes": list(PLAN)})}
updates = []
for nid, (slug, label, coach) in PLAN.items():
    n = notes[nid]
    old = n["fields"]["Back Extra"]["value"]
    block = f"Ex: {label} — [sound:arabic_khouri_{slug}.mp3]" + (("<br><br>" + coach) if coach else "")

    if f"arabic_khouri_{slug}.mp3" in old:
        print(f"  SKIP {nid} {slug}: already enriched"); continue

    m = re.search(r'(<br>)*<img [^>]*>\s*$', old)
    if m:
        head, tail = old[:m.start()], old[m.start():]
        tail = re.sub(r'^(<br>)*', '', tail)
        new = f"{head}<br><br>{block}<br><br>{tail}"
    else:
        new = f"{old}<br><br>{block}"

    # every original character must survive, in order
    stripped = new.replace(f"<br><br>{block}<br><br>", "<br><br>", 1) \
                  .replace(f"<br><br>{block}", "", 1)
    assert stripped == old, f"INSERT-ONLY VIOLATION on {nid}\n old={old!r}\n got={stripped!r}"
    updates.append((nid, slug, old, new, block))

print(f"\n{len(updates)} notes to enrich (insert-only, verified)\n")
for nid, slug, old, new, block in updates:
    print("=" * 72); print(f"{nid}  {slug}")
    for line in block.split("<br><br>"): print("  +", line[:118])

if not APPLY:
    print("\nDRY RUN — rerun with --apply to write."); sys.exit(0)

for nid, slug, old, new, block in updates:
    ac("updateNoteFields", {"note": {"id": nid, "fields": {"Back Extra": new}}})
    back = ac("notesInfo", {"notes": [nid]})[0]["fields"]["Back Extra"]["value"]
    assert back == new, f"readback mismatch on {nid}"
    print(f"  OK {nid} {slug}")
print(f"\n{len(updates)} notes enriched and read back clean.")
