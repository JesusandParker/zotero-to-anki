#!/bin/zsh
BASE=~/arabic-catchup
source <(sed -n '/^EN_PROMPT=/p;/^AR_PROMPT=/p' $BASE/transcribe.sh)
LEC="$HOME/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures"
log(){ echo "[$(date +%T)] $*" | tee -a $BASE/logs/transcribe.log; }
while kill -0 68583 2>/dev/null; do sleep 20; done
pass(){ local id=$1 lang=$2 prompt=$3
  [ -s $BASE/mlx/${id}_${lang}.json ] && { log "skip $id $lang"; return; }
  log "whisper $id $lang start"
  ~/.local/bin/mlx_whisper $BASE/wav/$id.wav --model mlx-community/whisper-large-v3-turbo --language $lang --task transcribe \
    --output-dir $BASE/mlx --output-name ${id}_${lang} --output-format json --condition-on-previous-text False \
    --temperature 0 --word-timestamps True --initial-prompt "$prompt" --verbose False > $BASE/logs/${id}_${lang}.log 2>&1
  log "whisper $id $lang done: $(python3 -c "import json,collections;d=json.load(open('$BASE/mlx/${id}_${lang}.json'));c=collections.Counter(s['text'].strip() for s in d['segments']);print(len(d['segments']), c.most_common(1))" 2>&1 | tail -1)"; }
until [ -f "$LEC/2026-09-29 Elementary Arabic I.mp4" ]; do sleep 30; done
cat "$LEC/2026-09-29 Elementary Arabic I.mp4" > /dev/null
~/.local/bin/ffmpeg -nostdin -loglevel error -y -i "$LEC/2026-09-29 Elementary Arabic I.mp4" -vn -ac 1 -ar 16000 -c:a pcm_s16le $BASE/wav/teams_2026-09-29.wav && log "wav ok teams_2026-09-29"
for id in teams_2026-09-29 phone_2026-09-29; do pass $id en "$EN_PROMPT"; pass $id ar "$AR_PROMPT"; touch $BASE/mlx/$id.READY; done
log "ALL2 DONE"
