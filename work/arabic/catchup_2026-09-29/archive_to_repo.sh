#!/bin/zsh
# Copy the catch-up's scripts + data (no audio/video/frames/raw transcripts) into the skill repo and commit.
DEST=~/.claude/skills/zotero-to-anki/work/arabic/catchup_2026-09-29
mkdir -p $DEST
rsync -a --prune-empty-dirs \
  --include='*/' --include='*.py' --include='*.sh' --include='*.mjs' --include='*.json' --include='*.md' --include='*.html' \
  --exclude='wav/***' --exclude='mlx/***' --exclude='clips/***' --exclude='frames/***' --exclude='lingco_video/aud/***' \
  --exclude='lingco_video/mp4/***' --exclude='review/clips/***' --exclude='build/media/***' --exclude='*' \
  ~/arabic-catchup/ $DEST/
du -sh $DEST
cd ~/.claude/skills/zotero-to-anki && git add -A work/arabic/catchup_2026-09-29 reference/arabic-unit-playbook.md reference/sources.json work/arabic/u4 \
  && git commit -q -m "Arabic Units 1-4 catch-up: every Khouri word + every Lingco word with audio (488 notes), her voice cut from the lectures, playbook §8

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q && git log --oneline -1
