#!/usr/bin/env python3
"""Build Dr. Khouri's own-voice clips for the Thursday (2026-09-03) vocab set from the
2026-09-01 lecture recording, then re-gate every FINAL mp3 in both languages.

Source: `full.wav` = 16 kHz mono PCM extracted from
  My Drive/01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures/2026-09-01 Elementary Arabic I.mp4
  (ffmpeg -vn -ac 1 -ar 16000 -c:a pcm_s16le).  Pass its path as argv[1].

Every segment below is a silence-bounded energy island (or a tight sub-island / two adjacent
islands of ONE utterance) chosen by the method in reference/arabic-unit-playbook.md §5:
island list -> whisper `-l en` AND `-l ar` on every island -> pick -> re-gate.  Timestamps
are seconds into the recording.  A "join" entry concatenates the masculine and feminine
forms with 350 ms of real silence between them (generated with anullsrc, mixed BEFORE the
mp3 encode, so the muxer sees monotonic timestamps).
"""
import json, os, subprocess, sys
SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(HERE, "media")
SPEC = json.load(open(os.path.join(HERE, "khouri_thursday_clips_spec.json"), encoding="utf-8"))
LEAD, TAIL = 0.095, 0.04
M = os.path.expanduser("~/.cache/whisper-cpp/ggml-large-v3-turbo-q5_0.bin")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"FAILED: {' '.join(cmd)}\n{r.stderr}")
    return r.stdout

def cut(seg, out):
    s = max(0.0, seg[0] - LEAD); d = seg[1] - seg[0] + LEAD + TAIL
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC,
         "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", out])

def whisper(path, lang):
    r = subprocess.run(["whisper-cli", "-m", M, "-l", lang, "-mc", "0", "-nt", "-np", "-f", path],
                       capture_output=True, text=True)
    return " ".join(r.stdout.split())

tmp = os.path.join(HERE, "_clipbuild"); os.makedirs(tmp, exist_ok=True); os.makedirs(MEDIA, exist_ok=True)
gate_log = []
for slug, e in SPEC.items():
    fn = f"arabic_khouri_{slug}.mp3"
    parts = []
    for k, seg in enumerate(e["segments"]):
        p = os.path.join(tmp, f"{slug}_{k}.wav"); cut(seg, p); parts.append(p)
    joined = os.path.join(tmp, f"{slug}.wav")
    if len(parts) == 1:
        os.replace(parts[0], joined)
    else:
        sil = os.path.join(tmp, "sil350.wav")
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono", "-t", "0.35",
             "-c:a", "pcm_s16le", sil])
        lst = os.path.join(tmp, f"{slug}.txt")
        with open(lst, "w") as f:
            for i, p in enumerate(parts):
                if i: f.write(f"file '{sil}'\n")
                f.write(f"file '{p}'\n")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", joined])
    out = os.path.join(MEDIA, fn)
    run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-ar", "44100", "-codec:a", "libmp3lame", "-b:a", "96k", out])
    dur = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).strip()
    # re-gate the FINAL file (decode the mp3 back to wav so the gate hears exactly what Anki plays)
    back = os.path.join(tmp, f"{slug}_final.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", out, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", back])
    en, ar = whisper(back, "en"), whisper(back, "ar")
    gate_log.append({"file": fn, "duration_s": float(dur), "segments": e["segments"], "gate_en": en, "gate_ar": ar,
                     "expect_ar": e["expect_ar"], "note": e["note"]})
    ok = all(w in ar.replace("ً", "") for w in e["expect_ar"].split())
    print(f"{'OK ' if ok else '?? '} {fn:44s} {float(dur):4.2f}s  en={en[:34]!r:36s} ar={ar}")
json.dump(gate_log, open(os.path.join(HERE, "khouri_thursday_clips_gate.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# the mapping the card generator consumes
clips = {slug: {"file": f"arabic_khouri_{slug}.mp3", "label": e["label"], "audio_source": e["note"]} for slug, e in SPEC.items()}
json.dump(clips, open(os.path.join(HERE, "khouri_thursday_clips.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n{len(clips)} clips built into {MEDIA}; gate log -> khouri_thursday_clips_gate.json")
