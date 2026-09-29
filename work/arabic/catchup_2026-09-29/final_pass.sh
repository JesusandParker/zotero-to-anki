#!/bin/zsh
# Final pass after every cutter finished: validate clips -> rebuild -> upgrade written notes -> extend existing
# notes (no unsuspends while the cram hold is on) -> media audit -> review page.
set -e
PY=~/.local/share/uv/tools/mlx-whisper/bin/python
cd ~/arabic-catchup
$PY cutter/validate_clips.py
cd build
$PY merge.py | tail -1
$PY build_all.py | tail -4
$PY updater.py --apply
$PY plan_existing.py | tail -1
$PY apply_existing.py existing_plan.json --apply | tail -2
cd ~/.claude/skills/zotero-to-anki && python3 scripts/media_audit.py --deck 'all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I' --prefix arabic_ | grep -vE "^    arabic_" | tail -3
cd ~/arabic-catchup/review && $PY build_review.py
