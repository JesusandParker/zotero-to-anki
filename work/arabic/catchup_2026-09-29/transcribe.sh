#!/bin/zsh
# Sequential whisper passes for the ARAB 101 catch-up (2026-09-29). One MLX job at a time.
BASE=~/arabic-catchup
LEC="$HOME/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures"
VM="$HOME/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
FF=~/.local/bin/ffmpeg; [ -x $FF ] || FF=ffmpeg
EN_PROMPT="Arabic 101 lecture with Dr. Khouri, Alif Baa textbook. marHaba, ahlan wa sahlan, as-salaamu calaykum, tasharrafna, shukran, cafwan, ana, ismi, min, madiinat, askun, fii, baab, bayt, kitaab, waajib, Habiibi, SabaaH al-khayr, kayfa al-Haal, al-Hamdu lillaah, haadhaa, haadhihi, laysa, tafaDDal, SaaHibii, huwa, hiya, Taalib, ustaadh, jaamica, khubz, dajaaj, jaar, akh, ukht, jadiid, masaa' al-khayr, cindi, su'aal, uHibb, raqm tilifuun. Letters alif, baa, taa, thaa, jiim, Haa, khaa, daal, dhaal, raa, zaay, waaw, yaa, hamza, fatHa, Damma, kasra, sukuun, shadda, tanwiin, tashkiil. Lingco, drill, dictation."
AR_PROMPT="درس اللغة العربية. مرحبا. أهلا وسهلا. السلام عليكم. شكرا. عفوا. تشرفنا. أنا. اسمي. من. مدينة. أسكن. في. باب. بيت. كتاب. واجب. حبيبي. صباح الخير. كيف الحال. الحمد لله. هذا. هذه. ليس. تفضل. صاحبي. هو. هي. طالب. أستاذ. جامعة. خبز. دجاج. جار. أخ. أخت. جديد. مساء الخير. عندي. سؤال. أحب. رقم تلفون. ألف. باء. تاء. ثاء. جيم. حاء. خاء. دال. ذال. راء. زاي. واو. ياء. همزة. فتحة. ضمة. كسرة. سكون. شدة. تنوين. تشكيل. واحد. اثنان. ثلاثة. أربعة. خمسة. ستة. سبعة. ثمانية. تسعة. عشرة."
log(){ echo "[$(date +%T)] $*" | tee -a $BASE/logs/transcribe.log; }
mkwav(){ local id=$1 src=$2 map=$3
  [ -s $BASE/wav/$id.wav ] && return
  log "hydrate+wav $id"; cat "$src" > /dev/null
  $FF -nostdin -loglevel error -y -i "$src" $map -vn -ac 1 -ar 16000 -c:a pcm_s16le $BASE/wav/$id.wav && log "wav ok $id"; }
pass(){ local id=$1 lang=$2 prompt=$3
  [ -s $BASE/mlx/${id}_${lang}.json ] && { log "skip $id $lang"; return; }
  log "whisper $id $lang start"
  ~/.local/bin/mlx_whisper $BASE/wav/$id.wav --model mlx-community/whisper-large-v3-turbo --language $lang --task transcribe \
    --output-dir $BASE/mlx --output-name ${id}_${lang} --output-format json --condition-on-previous-text False \
    --temperature 0 --word-timestamps True --initial-prompt "$prompt" --verbose False > $BASE/logs/${id}_${lang}.log 2>&1
  local rc=$?
  local top=$(python3 -c "import json,collections;d=json.load(open('$BASE/mlx/${id}_${lang}.json'));c=collections.Counter(s['text'].strip() for s in d['segments']);print(len(d['segments']), c.most_common(1))" 2>&1)
  log "whisper $id $lang done rc=$rc segs/top=$top"; }
ORDER=(phone_2026-09-29 teams_2026-09-24 teams_2026-09-22 teams_2026-09-17 teams_2026-09-15 teams_2026-09-10 teams_2026-09-08)
mkwav phone_2026-09-29 "$VM/20260929 111210-03ADA704.qta" "-map 0:0"
for id in $ORDER; do
  case $id in teams_*) d=${id#teams_}; mkwav $id "$LEC/$d Elementary Arabic I.mp4" "";; esac
  pass $id en "$EN_PROMPT"; pass $id ar "$AR_PROMPT"
  touch $BASE/mlx/${id}.READY
done
mkwav phone_2026-09-22 "$VM/20260922 111346-93B386C9.qta" "-map 0:0"
mkwav phone_2026-09-24 "$VM/20260924 111511-AC31C378.qta" "-map 0:0"
log "ALL DONE"
