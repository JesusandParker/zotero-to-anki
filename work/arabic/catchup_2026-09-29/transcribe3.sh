#!/bin/zsh
BASE=~/arabic-catchup
source <(sed -n '/^EN_PROMPT=/p;/^AR_PROMPT=/p' $BASE/transcribe.sh)
log(){ echo "[$(date +%T)] $*" | tee -a $BASE/logs/transcribe.log; }
while kill -0 72836 2>/dev/null; do sleep 20; done
for id in phone_2026-09-24 phone_2026-09-22; do
  [ -s $BASE/mlx/${id}_en.json ] && continue
  log "whisper $id en start"
  ~/.local/bin/mlx_whisper $BASE/wav/$id.wav --model mlx-community/whisper-large-v3-turbo --language en --task transcribe \
    --output-dir $BASE/mlx --output-name ${id}_en --output-format json --condition-on-previous-text False \
    --temperature 0 --word-timestamps True --initial-prompt "$EN_PROMPT" --verbose False > $BASE/logs/${id}_en.log 2>&1
  log "whisper $id en done"
done
log "ALL3 DONE"
