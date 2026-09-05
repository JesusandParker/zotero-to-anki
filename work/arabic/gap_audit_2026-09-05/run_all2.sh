#!/bin/zsh
OUT="/private/tmp/claude-501/-Users-parkerregner/5067ba34-f9e9-49f7-ae61-c5a1b13a4dd9/scratchpad/arab"
PY=~/.local/share/uv/tools/mlx-whisper/bin/python
AR_PROMPT="درس اللغة العربية. مرحبا. أهلا وسهلا. السلام عليكم. وعليكم السلام. شكرا. عفوا. تشرفنا. أنا. اسمي. من. مدينة. أسكن. في. باب. توت. أب. بابا. أبي. ثوب. تاب. بات. همزة. ألف. باء. تاء. ثاء. واو. ياء. فتحة. ضمة. كسرة. سكون. هل. أين. أنت. نعم. لا. حضرتك. أحسنت."
log(){ echo "[$(date +%T)] $*"; }
while [ ! -f "$OUT/isl/2026-09-03_yaa_ab_abii.json" ]; do sleep 10; done
log "first window landed; continuing with AR-only islands"
isl(){ local d=$1 a=$2 b=$3 n=$4
  [ -f "$OUT/isl/${d}_${n}.json" ] && { log "skip islands $d $n"; return; }
  log "islands $d $n [$a-$b] start"
  $PY "$OUT/islands_mlx.py" $d $a $b "$OUT/isl/${d}_${n}.json" -42 0.10 ar > "$OUT/isl/${d}_${n}.log" 2>&1
  log "islands $d $n done (exit $?)"; }
full(){ local d=$1 lang=$2
  [ -f "$OUT/mlx/${d}_${lang}.json" ] && { log "skip $d $lang (exists)"; return; }
  log "full $d $lang start"
  ~/.local/bin/mlx_whisper "$OUT/$d.wav" --model mlx-community/whisper-large-v3-turbo --language $lang --task transcribe \
    --output-dir "$OUT/mlx" --output-name "${d}_${lang}" --output-format json --condition-on-previous-text False \
    --initial-prompt "$AR_PROMPT" --verbose False > "$OUT/mlx/${d}_${lang}.log" 2>&1
  log "full $d $lang done (exit $?)"; }
isl 2026-09-03 3630 4480 speaking_practice_end
isl 2026-08-27 3290 4620 vocab_list
isl 2026-09-01 1900 2800 harf_waaw_tuut_thawb
isl 2026-08-27 2360 3290 alif_baa_hamza_ab
isl 2026-09-03 560 2480 drills_5_4_11_p33
isl 2026-09-03 2480 3630 short_vowels
isl 2026-09-01 600 1300 taa_thaa_names_baab
isl 2026-08-27 130 280 marhaba_intro
isl 2026-08-27 0 130 opening
isl 2026-09-01 0 140 opening
isl 2026-09-03 0 170 opening
isl 2026-08-25 0 140 opening_greetings
for d in 2026-09-03 2026-09-01 2026-08-27 2026-08-25; do full $d ar; done
isl 2026-08-25 3680 4560 alphabet_overview
log "RUN_ALL DONE"
