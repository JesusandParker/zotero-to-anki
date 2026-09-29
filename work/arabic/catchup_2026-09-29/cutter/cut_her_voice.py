#!/usr/bin/env python3
"""Cut Dr. Khouri's own pronunciation of a word out of a lecture recording, and prove it.

Consolidates the method the 2026-09-05/06 runs settled (playbook §5-6, apply2.py, hunt3.py):
  1. candidates come from a moment she says the word (lecture-agent `her_clear_utterances`);
  2. stage A - cheap: cut on the whisper word-timestamp span, jittered a little;
     stage B - silence-bounded energy islands (and adjacent pairs) inside the window;
     stage C - dense (start, duration) grid in a tight window (hunt3), capped;
     every stage matches the Arabic pass by EDIT DISTANCE (<=0.30) against the expected spelling;
  3. the surviving cut is encoded FROM THE ORIGINAL MEDIA (48 kHz, not the 16 kHz ASR copy),
     padded with DIGITAL SILENCE (never neighbouring audio), and the FINAL mp3 is gated
     again in BOTH -l ar and -l en (R62/R66): Arabic within distance, English pass carrying no
     filler word ("so", "and", "okay"...). The first candidate whose encoded file passes wins.
usage: cut_her_voice.py targets.json out_dir log.json
target: {"slug","expect":"تفضل/تفضل","at":[["teams_2026-09-24",1234.5,1235.3],...],
         "out":"arabic_khouri_tafaddal.mp3","dmin":0.35,"dmax":1.6}
"""
import json, os, sys, math, re, subprocess
import numpy as np, mlx_whisper

BASE = os.path.expanduser("~/arabic-catchup")
FF = os.path.expanduser("~/.local/bin/ffmpeg")
M = "mlx-community/whisper-large-v3-turbo"
SR = 16000
LEC = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-regnerparker@gmail.com/My Drive/"
                         "01_Liberty University /2026 - 2027 Year/Elementary Arabic I/Lectures")
VM = os.path.expanduser("~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings")
PHONE = {"phone_2026-09-22": "20260922 111346-93B386C9.qta", "phone_2026-09-24": "20260924 111511-AC31C378.qta",
         "phone_2026-09-29": "20260929 111210-03ADA704.qta", "phone_2026-09-01": "20260901 114012.m4a"}

def source(fid):
    if fid.startswith("teams_"):
        return f"{LEC}/{fid[6:]} Elementary Arabic I.mp4"
    return f"{VM}/{PHONE[fid]}"

DIA = re.compile(r"[ً-ْٰـ‌‍‎‏؟،\.\!\?\"'«»:]")
def norm(s):
    s = DIA.sub("", s or "")
    s = re.sub("[أإآٱ]", "ا", s)
    return re.sub(r"\s+", " ", s.replace("ى", "ي").replace("ة", "ه")).strip()

def lev(a, b):
    if a == b: return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def dist(got, wants):
    n = norm(got)
    return min((lev(n, w) / max(len(w), 1), w) for w in wants)

FILLER_RE = re.compile(r"^(so|and|or|if|now|okay|ok|well|then|but|you know|like|uh|um|yeah|yes)\b", re.I)
def filler(en):
    e = (en or "").strip().strip(" .!?,'\"")
    return bool(FILLER_RE.match(e)) and len(e.split()) > 1 or e.lower() in {"so", "and", "or", "now", "well", "then", "okay", "ok"}

EXCL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exclusions.json")))
# lecture agents mark stretches that are NOT her (publisher audio from her laptop, a student):
for _f in __import__("glob").glob(os.path.join(BASE, "lectures", "*.json")):
    try:
        for _w in json.load(open(_f)).get("words", []):
            for _sp in _w.get("not_her_spans") or []:
                if isinstance(_sp, dict) and _sp.get("file") and _sp.get("start") is not None:
                    EXCL.setdefault(_sp["file"], []).append([_sp["start"] - 0.3, (_sp.get("end") or _sp["start"] + 1) + 0.3, "not her"])
    except Exception as _e:
        print("exclusion load failed", _f, _e, file=sys.stderr)

def median_f0(x, sr=SR):
    """Median pitch of the voiced frames (autocorrelation, 120-400 Hz); None if too few voiced frames."""
    n = int(0.040 * sr); hop = int(0.010 * sr); f0s = []
    for k in range(0, len(x) - n, hop):
        fr = x[k:k + n] - x[k:k + n].mean()
        if 20 * math.log10(math.sqrt(float((fr * fr).mean())) + 1e-9) < -35: continue
        ac = np.correlate(fr, fr, "full")[n - 1:]
        lo, hi = int(sr / 400), int(sr / 120)
        if ac[0] <= 0: continue
        seg = ac[lo:hi]; i = int(seg.argmax())
        if seg[i] / ac[0] > 0.45: f0s.append(sr / (lo + i))
    return float(np.median(f0s)) if len(f0s) >= 5 else None
def excluded(fid, s, e):
    return any(s < b and e > a for a, b, *_ in EXCL.get(fid, []))

RAW = {}
def raw(fid):
    if fid not in RAW:
        RAW[fid] = np.fromfile(f"{BASE}/wav/{fid}.wav", dtype=np.int16, offset=44)
    return RAW[fid]

def tx(clip, lang, prompt=None):
    return mlx_whisper.transcribe(clip, path_or_hf_repo=M, language=lang, task="transcribe",
                                  condition_on_previous_text=False, fp16=True, verbose=None,
                                  temperature=0.0, no_speech_threshold=0.8,
                                  initial_prompt=prompt)["text"].strip()

def slice16(fid, s, e):
    r = raw(fid); i0, i1 = max(0, int(s * SR)), min(len(r), int(e * SR))
    return r[i0:i1].astype(np.float32) / 32768.0

def islands(fid, a, b, thr=-42.0, minpause=0.10, minlen=0.13):
    x = slice16(fid, a, b); hop = int(0.010 * SR); win = int(0.025 * SR)
    on = []
    for k in range(0, max(0, len(x) - win), hop):
        seg = x[k:k + win]
        if 20 * math.log10(math.sqrt(float((seg * seg).mean())) + 1e-9) > thr:
            on.append(a + k / SR)
    if not on: return []
    segs = []; st = prev = on[0]
    for t in on[1:]:
        if t - prev > minpause: segs.append((st, prev + 0.01)); st = t
        prev = t
    segs.append((st, prev + 0.01))
    return [(s, e) for s, e in segs if e - s >= minlen]

def encode(fid, s, e, pad, out):
    dur = e - s
    tmp = os.path.abspath(out) + ".tmp"
    subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", "-ss", f"{max(0, s):.3f}", "-t", f"{dur:.3f}",
                    "-i", source(fid), "-map", "0:a:0", "-af",
                    f"afade=t=in:st=0:d=0.012,afade=t=out:st={max(0.0, dur - 0.02):.3f}:d=0.02",
                    "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", tmp + "_c.wav"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", "-f", "lavfi", "-t", f"{pad:.3f}",
                    "-i", "anullsrc=r=44100:cl=mono", "-c:a", "pcm_s16le", tmp + "_s.wav"], check=True)
    open(tmp + "_l.txt", "w").write(f"file '{tmp}_s.wav'\nfile '{tmp}_c.wav'\nfile '{tmp}_s.wav'\n")
    # plain peak normalisation to -1.5 dBFS: phone clips sit ~12 dB under Teams clips, and a
    # loudness filter pumps on sub-second audio. One gain value, nothing dynamic.
    c = np.fromfile(tmp + "_c.wav", dtype=np.int16, offset=44).astype(np.float32) / 32768.0
    pk = float(np.abs(c).max()) if len(c) else 1.0
    gain = min(24.0, -1.5 - 20 * math.log10(pk + 1e-9))
    subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "_l.txt",
                    "-af", f"volume={gain:.2f}dB", "-c:a", "libmp3lame", "-b:a", "160k", "-ar", "44100", "-ac", "1", out], check=True)
    for suf in ("_c.wav", "_s.wav", "_l.txt"):
        try: os.remove(tmp + suf)
        except OSError: pass

def gate(path, prompt=None):
    r = subprocess.run([FF, "-nostdin", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                       capture_output=True, check=True).stdout
    x = np.frombuffer(r, dtype=np.int16).astype(np.float32) / 32768.0
    # the English pass is NEVER prompted: it is the filler detector and must hear what is really there
    return {"ar": tx(x, "ar", prompt), "en": tx(x, "en")}, len(x) / SR

QUICK = os.environ.get("CUT_MODE", "deep") == "quick"

def find_candidates(T, wants, budget, prompt=None):
    cands = []; tested = 0
    ats = T["at"][:3] if QUICK else T["at"]
    jit = ((0.0, 0.0), (-0.10, 0.10), (-0.20, 0.0), (0.0, 0.20), (-0.10, 0.20), (0.10, -0.10)) if QUICK else \
          [(a, b) for a in (0.0, -0.10, -0.20, 0.10) for b in (0.0, 0.10, 0.20, -0.10)]
    def test(fid, s, e, how):
        nonlocal tested
        if e - s < 0.15 or excluded(fid, s, e): return
        clip = slice16(fid, s, e)
        if not len(clip) or float(np.abs(clip).max()) < 0.02: return
        tested += 1
        got = tx(clip, "ar", prompt); d, w = dist(got, wants)
        if d <= 0.30:
            pk = 20 * math.log10(float(np.abs(clip).max()) + 1e-9)
            cands.append({"file": fid, "s": round(s, 3), "e": round(e, 3), "ar": got, "d": round(d, 3), "peak": round(pk, 1), "how": how})
    for at in ats:
        fid, t0 = at[0], at[1]; t1 = at[2] if len(at) > 2 else t0 + 0.8
        # stage A: the timestamp span, jittered
        for ds, de in jit:
            test(fid, t0 + ds, t1 + de, "A")
        # stage B: islands and adjacent pairs inside the window
        isl = islands(fid, t0 - 1.5, t1 + 1.5)
        for i, (s, e) in enumerate(isl):
            test(fid, s - 0.05, e + 0.05, "B1")
            if i + 1 < len(isl) and isl[i + 1][0] - e < 0.45:
                test(fid, s - 0.05, isl[i + 1][1] + 0.05, "B2")
        if len(cands) >= 3: break
    if not cands and not prompt and not QUICK:
        # stage C: dense grid, capped
        for at in T["at"]:
            fid, t0 = at[0], at[1]; t1 = at[2] if len(at) > 2 else t0 + 0.8
            c = (t0 + t1) / 2
            for s0 in np.arange(t0 - 0.45, t0 + 0.35, 0.075):
                for dur in np.arange(T.get("dmin", 0.35), T.get("dmax", 1.6) + 1e-3, 0.12):
                    if tested >= budget: break
                    test(fid, float(s0), float(s0 + dur), "C")
            if cands or tested >= budget: break
    seen = set(); uniq = []
    for x in sorted(cands, key=lambda z: (z["d"], -z["peak"], z["how"])):
        k = (x["file"], round(x["s"], 1), round(x["e"], 1))
        if k in seen: continue
        seen.add(k); uniq.append(x)
    return uniq[:6], tested

def main(tpath, outdir, logpath):
    targets = json.load(open(tpath, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    log = json.load(open(logpath, encoding="utf-8")) if os.path.exists(logpath) else {}
    for T in targets:
        slug = T["slug"]
        done = ("PASS", "PASS_HINTED", "PASS_NEAR", "NONE") + (("NONE_QUICK",) if QUICK else ())
        if slug in log and log[slug].get("status") in done: continue
        wants = [norm(w) for w in T["expect"].split("/") if w.strip()]
        if not QUICK and T.get("priority", 0) >= 1 and T.get("budget", 450) <= 150:
            # deep retry is only spent on words that will become NEW notes; an existing card keeps its book audio
            log[slug] = {"status": "NONE", "out": None, "expect": T["expect"], "chosen": None, "tested": 0, "tries": [], "why": "deep retry skipped (existing note)"}
            json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            continue
        cands, tested = find_candidates(T, wants, min(T.get("budget", 450), 100 if T.get("budget", 450) <= 150 else 450))
        prompt = None
        if not cands and QUICK:
            log[slug] = {"status": "NONE_QUICK", "out": None, "expect": T["expect"], "chosen": None, "tested": tested, "tries": []}
            print(f"NONE_QUICK  {slug:28} tested={tested:4d}", flush=True)
            json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            continue
        if not cands:
            # fallback: whisper mishears some short words as something common (ukht -> "8").
            # Re-test the timestamp and island cuts with the expected word as a HINT; such a clip
            # is only accepted as a single island with a filler-free unprompted English pass, and is
            # marked PASS_HINTED so his ear review sees it first.
            prompt = "، ".join(sorted(set(T["expect"].split("/"))))
            cands, t2 = find_candidates(T, wants, 120, prompt=prompt)
            cands = [c for c in cands if c["how"] in ("A", "B1")]
            tested += t2
        chosen = None; tries = []
        def quiet_tail(c):
            x = slice16(c["file"], c["e"], c["e"] + 0.15)
            if not len(x): return c
            rms = 20 * math.log10(math.sqrt(float((x * x).mean())) + 1e-9)
            pk = 20 * math.log10(float(np.abs(x).max()) + 1e-9)
            return {**c, "e": round(c["e"] + 0.10, 3), "tail": "extended"} if (rms < -40 and pk < -26) else c
        cands = [v for c in cands for v in ([quiet_tail(c), c] if quiet_tail(c) is not c else [c])]
        kept = []
        for c in cands:
            f0 = median_f0(slice16(c["file"], c["s"], c["e"]))
            c["f0"] = round(f0) if f0 else None
            # Pitch cannot separate her (median ~216 Hz, down to ~168 on pharyngeals) from the publisher's
            # female voice (~160-185 Hz, as loud through her lapel). It CAN reject a male voice.
            if f0 is not None and f0 < 150:
                tries.append({**c, "ok": False, "why": f"pitch {f0:.0f} Hz: a male voice, not hers"}); continue
            kept.append(c)
        cands = kept
        for c in cands:
            for pad in (0.09, 0.14):
                out = f"{outdir}/{T['out']}"
                encode(c["file"], c["s"], c["e"], pad, out)
                o, dur = gate(out, prompt); d, w = dist(o["ar"], wants)
                ok = d <= 0.30 and not filler(o["en"])
                tries.append({**c, "pad": pad, "final_ar": o["ar"], "final_en": o["en"], "final_d": round(d, 3), "ok": ok})
                if ok:
                    chosen = {**c, "pad": pad, "dur": round(dur, 2), "final_ar": o["ar"], "final_en": o["en"], "final_d": round(d, 3)}
                    break
            if chosen: break
        if not chosen and os.path.exists(f"{outdir}/{T['out']}"):
            os.remove(f"{outdir}/{T['out']}")
        status = "NONE"
        if chosen:
            status = "PASS_HINTED" if prompt else ("PASS_NEAR" if chosen["final_d"] > 0 else "PASS")
        log[slug] = {"status": status, "out": T["out"] if chosen else None, "expect": T["expect"],
                     "chosen": chosen, "tested": tested, "tries": tries[:8]}
        print(f"{log[slug]['status']:11} {slug:28} tested={tested:4d} "
              + (f"{chosen['file']} {chosen['s']:.2f}-{chosen['e']:.2f} ar={chosen['final_ar'][:20]!r} en={chosen['final_en'][:24]!r}" if chosen else ""),
              flush=True)
        json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("CUT DONE", sum(v["status"].startswith("PASS") for v in log.values()), "/", len(log), flush=True)

if __name__ == "__main__":
    main(*sys.argv[1:4])
