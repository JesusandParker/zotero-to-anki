#!/bin/zsh
while kill -0 73077 2>/dev/null; do sleep 20; done
echo "[$(date +%T)] clipcheck start" >> ~/arabic-catchup/logs/transcribe.log
~/.local/share/uv/tools/mlx-whisper/bin/python -u ~/arabic-catchup/clipcheck/transcribe_clips.py > ~/arabic-catchup/logs/clipcheck.log 2>&1
echo "[$(date +%T)] clipcheck done" >> ~/arabic-catchup/logs/transcribe.log
