#!/bin/zsh
# sequential GPU queue: batch 3 (quick) -> letters (deep) -> deep retry of every quick miss
PY=~/.local/share/uv/tools/mlx-whisper/bin/python
cd ~/arabic-catchup/cutter
while kill -0 6646 2>/dev/null; do sleep 15; done
echo "[$(date +%T)] batch3 quick start"
CUT_MODE=quick $PY -u cut_her_voice.py targets3.json ../clips cut_log3.json >> ../logs/cutter3.log 2>&1
echo "[$(date +%T)] letters start"
CUT_MODE=deep $PY -u cut_her_voice.py targets_letters.json ../clips cut_log_letters.json >> ../logs/cutter_letters.log 2>&1
while kill -0 1804 2>/dev/null; do sleep 15; done          # batch 1 quick must be finished
echo "[$(date +%T)] deep retry start"
for pair in "targets_batch1.json cut_log.json" "targets2.json cut_log2.json" "targets3.json cut_log3.json"; do
  set -- ${=pair}
  $PY - "$1" "$2" <<'PYEOF'
import json, sys
t, l = sys.argv[1], sys.argv[2]
log = json.load(open(l))
# quick misses and encode-gate failures from the quick pass get a deep retry (budget 150)
retry = [x for x in json.load(open(t)) if log.get(x["slug"], {}).get("status") in ("NONE_QUICK", "NONE")]
for x in retry:
    x["budget"] = 150; log.pop(x["slug"], None)
json.dump(log, open(l, "w"), ensure_ascii=False, indent=1)
json.dump(retry, open(t.replace(".json", "_deep.json"), "w"), ensure_ascii=False, indent=1)
print(t, "deep retry:", len(retry))
PYEOF
  CUT_MODE=deep $PY -u cut_her_voice.py ${1%.json}_deep.json ../clips $2 >> ../logs/cutter_deep.log 2>&1
done
echo "[$(date +%T)] QUEUE DONE"
