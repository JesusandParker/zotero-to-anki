#!/usr/bin/env python3
"""Turn build/master.json (+ her clips + Lingco clips) into Anki note specs: build/cards.json.

Card shapes are the pipeline's established ones (playbook §7, check_block_spec.py):
  C_vocab   ‎{{c1::<Arabic>}} / Transliteration: {{c1::<tr>}} / {{c2::<meaning>}} — <qualifier>
            Back Extra: Cue: MSA — ... | Why: letters in order + how it sounds | her notes | dialect/book audio
            Audio: HER voice if a clip survived the dual-language gate, else the Lingco Formal clip
  B_symbols ‎{{c1::٣}} / Number: {{c2::3 — thalaatha}}
Tags: arabic-uN, ARAB101::from::<source>, ARAB101::tier::<chart|class|practice|numbers>, ARAB101::catchup-2026-09-29
"""
import json, os, re, sys, html
from arabic_read import verified_breakdown, spell, bare, forms

BASE = os.path.expanduser("~/arabic-catchup")
ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"
LRM = "‎"

def esc(s): return html.escape(s or "", quote=False)

def deck(unit): return f"{ROOT}::Unit {int(unit):02d}"

def tier_of(r):
    if any((it.get("lesson") or "").startswith("New Vocabulary") for it in r["lingco"]): return "chart"
    if r.get("number"): return "numbers"
    if r["khouri"]: return "class"
    return "practice"

def from_tags(r):
    t = set()
    for w in r["khouri"]:
        d = w.get("lecture_date") or w.get("lecture")
        if d and re.match(r"\d{4}-\d\d-\d\d$", d): t.add(f"ARAB101::from::class-{d}")
    for it in r["lingco"]:
        les = (it.get("lesson") or "").lower()
        if les.startswith("new vocabulary"): t.add("ARAB101::from::book")
        else: t.add(f"ARAB101::from::lingco-u{it.get('unit')}-" + re.sub(r"[^a-z0-9]+", "", les.replace("listening exercise", "le").replace("drill", "d")))
    return sorted(t)

def vocab_note(r, her_clip, lingco_formal, lingco_shaami, lingco_other):
    ar = r["arabic"].strip(); tr = r["translit"].strip()
    meaning = r["meaning_core"]; qual = r.get("qualifier")
    text = (f"{LRM}{{{{c1::{ar}}}}}<br><br>Transliteration: {{{{c1::{esc(tr)}}}}}<br><br>"
            f"{{{{c2::{esc(meaning)}}}}}" + (f" — {esc(qual)}" if qual else ""))
    be = []
    formal_tr = r.get("formal_translit") or (tr if r.get("register") != "shaami" else None)
    if formal_tr: be.append(f"Cue: MSA — {esc(formal_tr)}")
    else: be.append(f"Cue: MSA — none; <i>{esc(tr)}</i> is shaami, her own dialect (the course tests Formal)")
    # how the word is built: letters by name, and how it sounds (only if the reading self-checks)
    ch = verified_breakdown(ar, tr) if "/" not in ar else None
    why = f"Why: {esc(spell(ar))}."
    if ch:
        words = []
        for w in ch:
            syl = []
            for _, t in w:
                if not t: continue
                t = t.replace("-", "")
                if not syl: t = t.lstrip("'")                     # the book leaves word-initial hamza unwritten
                m2 = re.match(r"^(sh|kh|th|dh|gh|DH|[a-zA-Z'])\1", t)
                if syl and m2:                                    # shadda: the doubled consonant closes the
                    syl[-1] += m2.group(1); t = t[len(m2.group(1)):]   # syllable before it and opens the next
                if syl and not re.search(r"[aiu]", t):            # no vowel: it closes the syllable before it
                    syl[-1] += t
                else:
                    syl.append(t)
            words.append(" · ".join(syl))
        if any("·" in w for w in words):
            why += f" Say it in beats: <i>{esc('   '.join(words))}</i>."
    if r.get("why_extra"): why += " " + esc(r["why_extra"])
    be.append(why)
    if r.get("how"): be.append(f"How it works: {esc(r['how'])}")
    if r.get("also"): be.append(f"Also: {esc(r['also'])}")
    for n in r.get("her_notes", [])[:3]: be.append(f"Ex: {esc(n)}")
    for n in r.get("distinguish", [])[:2]: be.append(f"Distinguish: {esc(n)}")
    if r.get("pitfall"): be.append(f"Pitfall: {esc(r['pitfall'])}")
    audio = ""
    if her_clip:
        audio = f"[sound:{her_clip}]"
        if lingco_formal: be.append(f"Ex: book audio [sound:{lingco_formal}]")
    elif lingco_formal:
        audio = f"[sound:{lingco_formal}]"
    elif lingco_other:
        audio = f"[sound:{lingco_other[0]}]"
    elif lingco_shaami and not formal_tr:
        audio = f"[sound:{lingco_shaami}]"; lingco_shaami = None
    if lingco_shaami and r.get("shaami_translit"):
        sh = "the same word" if r["shaami_translit"] == "same word" else f"<i>{esc(r['shaami_translit'])}</i>"
        be.append(f"Ex: shaami (her dialect) — {sh} [sound:{lingco_shaami}]")
    for extra in (lingco_other or [])[1 if (not her_clip and not lingco_formal) else 0:][:1]:
        if extra not in audio: be.append(f"Ex: book practice audio [sound:{extra}]")
    return {"block": "C_vocab", "Text": text, "Back Extra": "<br><br>".join(be), "Audio": audio}

# ---------------------------------------------------------------- resolve one master record
SKIP_TYPES = {"letter-name", "nonword", "syllable", "pair", "long_clip"}
CONF = {"high": 0, "med": 1, "medium": 1, "low": 2, None: 3}

def is_chart(it): return (it.get("lesson") or "").startswith("New Vocabulary")

def split_meaning(m):
    """'Please come in / go ahead (to a male)' -> ('Please come in / go ahead', 'to a male')"""
    m = (m or "").strip()
    mm = re.match(r"^(.*?[^\s(])\s*\(([^()]*)\)\s*$", m)
    if mm and not m.startswith("("):
        return mm.group(1).strip(), mm.group(2).strip()
    return m, None

def resolve(r):
    """-> dict with arabic, translit, meaning_core, qualifier, register, unit, tier, notes... or None to skip."""
    L = [it for it in r["lingco"] if it.get("word_type") not in SKIP_TYPES and it.get("real_word", True)]
    K = [k for k in r["khouri"] if k.get("kind") not in ("letter-name",)]
    if not L and not K: return None
    chart = [it for it in L if is_chart(it) and it.get("register", "formal") != "shaami" and "_shaami" not in (it.get("id") or "")]
    chart_sh = [it for it in L if is_chart(it) and ("_shaami" in (it.get("id") or "") or it.get("register") == "shaami")]
    kslide = [k for k in K if k.get("spelling_source") == "slide"]
    other = sorted([it for it in L if not is_chart(it)], key=lambda it: CONF.get(it.get("meaning_confidence"), 3))
    if chart:
        src = chart[0]; arabic, tr, meaning = src["arabic"], src.get("translit") or "", src.get("meaning")
    elif kslide:
        src = kslide[0]; arabic, tr, meaning = src["arabic"], src["translit"], src["meaning"]
    elif K:
        src = sorted(K, key=lambda k: (CONF.get(k.get("confidence"), 3), {"required": 0, "taught": 1, "drilled": 2, "used": 3}.get(k.get("status"), 4)))[0]
        arabic, tr, meaning = src["arabic"], src["translit"], src["meaning"]
        # a publisher spelling of the same word outranks her own-knowledge spelling
        if src.get("spelling_source") == "own-knowledge" and other and bare(other[0]["arabic"]) == bare(arabic):
            arabic = other[0]["arabic"]
    elif other:
        src = other[0]; arabic, tr, meaning = src["arabic"], src.get("translit") or "", src.get("meaning")
        if CONF.get(src.get("meaning_confidence")) == 2: return None   # low-confidence gloss: held back
    elif chart_sh:
        src = chart_sh[0]; arabic, tr, meaning = src["arabic"], src.get("translit") or "", src.get("meaning")
    else:
        return None
    if not tr:
        tr = next((k["translit"] for k in K if k.get("translit")), "") or next((it.get("translit") for it in L if it.get("translit")), "")
    if not tr or not arabic or not meaning: return None
    core, qual = split_meaning(meaning)
    core, qual, extra_meaning = clean_meaning(core, qual)
    tr = clean_translit(tr)
    if not tr or not core: return None
    regs = {k.get("register") for k in K} | {it.get("register", "formal") for it in L}
    register = "shaami" if regs <= {"shaami"} else "formal"
    notes, seen = [], set()
    for k in K:
        for n in k.get("card_notes") or []:
            n = clean_note(n)
            if n and n.lower() not in seen and len(notes) < 3:
                seen.add(n.lower()); notes.append(n)
    also = None
    if extra_meaning:
        also = re.sub(r"^but\s+", "", extra_meaning).strip()
        also = also[:1].upper() + also[1:]
    required = any(k.get("status") == "required" for k in K)
    # deck = the unit he met it in: the chart's unit; else the Lingco unit (1-4); else the unit being
    # taught on the earliest lecture date she used it (a Unit-5 book word taught in week 5 lives in Unit 4)
    from merge import UNIT_BY_DATE
    lec_units = sorted(UNIT_BY_DATE.get((k.get("lecture_date") or k.get("lecture") or "")[:10]) or 9 for k in K)
    lin_units = sorted(it["unit"] for it in L if it.get("unit") in (1, 2, 3, 4))
    unit = chart[0]["unit"] if chart else (lin_units[0] if lin_units else (lec_units[0] if lec_units and lec_units[0] <= 4 else None))
    if unit is None: return None
    tier = "chart" if chart else ("class" if K else ("numbers" if any(it.get("word_type") == "number" for it in L) else "practice"))
    if any(it.get("word_type") == "number" for it in L) and not K: tier = "numbers"
    return {"arabic": arabic.strip(), "translit": tr.strip(), "meaning_core": core, "qualifier": qual,
            "register": register, "unit": unit, "tier": tier, "her_notes": notes, "required": required,
            "shaami_translit": (chart_sh[0].get("translit") if chart_sh else None),
            "formal_translit": tr.strip() if register == "formal" else None,
            "pitfall": "she called this REQUIRED." if required else None, "also": also,
            "lingco_items": L, "khouri_items": K, "chart_shaami": chart_sh}

# ---------------------------------------------------------------- media
import subprocess, shutil
FF = os.path.expanduser("~/.local/bin/ffmpeg")
MEDIA_DIR = f"{BASE}/build/media"
OK_DIALECTS = {"formal", "shaami"}

def lingco_name(a):
    o = (a.get("origin") or a.get("file") or "").rsplit(".", 1)[0].lower()
    o = re.sub(r"^ab3e_", "", o)
    return "arabic_lingco_" + re.sub(r"[^a-z0-9]+", "_", o).strip("_") + ".mp3"

def lingco_src(a):
    """path of an mp3 for this clip (wav sources are encoded once into build/media)."""
    p = a.get("path")
    if not p or not os.path.exists(p): return None
    if p.endswith(".mp3"): return p
    os.makedirs(MEDIA_DIR, exist_ok=True)
    out = f"{MEDIA_DIR}/{lingco_name(a)}"
    if not os.path.exists(out):
        subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", "44100",
                        "-c:a", "libmp3lame", "-b:a", "128k", out], check=True)
    return out

# Audio corrections from the 2026-09-29 gloss audit (spectrogram-verified):
#  * Unit 2 LE6 files are numbered in REVERSE of the printed items (R63 again): item n is file 6-n.
#  * Unit 3 LE1 clips say each word three times (j, zh, Egyptian g) — only the first (j) take may ship.
VAULT = os.path.expanduser("~/arabic-vault/media")
AUDIO_FIX = {"u2_le6_01": {"file": "u02_extra_c7121c0c.mp3", "origin": "AB3e_U2LE6-05"},
             "u2_le6_02": {"file": "u02_extra_52788deb.mp3", "origin": "AB3e_U2LE6-04"},
             "u2_le6_04": {"file": "u02_extra_b940dc0f.mp3", "origin": "AB3e_U2LE6-02"},
             "u2_le6_05": {"file": "u02_extra_e5fa3e1e.mp3", "origin": "AB3e_U2LE6-01"},
             "u3_le1_01": {"trim_first": True}, "u3_le1_02": {"trim_first": True},
             "u3_le1_03": {"trim_first": True}, "u3_le1_04": {"trim_first": True}}

def first_take(src, name):
    """Cut the first spoken island out of a multi-take clip (the formal j take of U3 LE1)."""
    import numpy as np
    raw = subprocess.run([FF, "-nostdin", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop = 160; e = [20 * np.log10(np.sqrt((x[i:i + 400] ** 2).mean()) + 1e-9) for i in range(0, len(x) - 400, hop)]
    on = [i * hop / 16000 for i, v in enumerate(e) if v > -40]
    if not on: return None
    s = on[0]; end = s
    for t in on[1:]:
        if t - end > 0.30: break          # a pause of 300 ms ends the first take
        end = t
    s, end = max(0, s - 0.08), end + 0.12
    out = f"{MEDIA_DIR}/{name}"
    os.makedirs(MEDIA_DIR, exist_ok=True)
    subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", "-ss", f"{s:.3f}", "-t", f"{end - s:.3f}", "-i", src,
                    "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "128k", out], check=True)
    return out

def audio_of(items, dialect):
    for it in items:
        fix = AUDIO_FIX.get(it.get("id"))
        for a in it.get("audio") or []:
            trim_ok = bool(fix and fix.get("trim_first") and dialect == "formal")   # the j take IS the formal reading
            if trim_ok or (a.get("dialect") == dialect and a.get("dialect") in OK_DIALECTS):
                if fix and fix.get("file"):
                    a = {**a, "path": f"{VAULT}/{fix['file']}", "origin": fix["origin"] + ".mp3"}
                src = lingco_src(a)
                if not src: continue
                if fix and fix.get("trim_first"):
                    name = lingco_name(a).replace(".mp3", "_j.mp3")
                    src = first_take(src, name)
                    if not src: continue
                    return name, src
                return lingco_name(a), src
    return None, None

# ---------------------------------------------------------------- assemble
AR_CHARS = re.compile(r"[؀-ۿ]")
META = re.compile(r"\b(slides?|projector|recording|screen[- ]?shar\w*|own knowledge|not explained|lingco|transcri\w*|"
                  r"captions?|whisper|asr|en pass|ar pass|frames?|agent|spelling (?:is|from)|unverified|listen before|"
                  r"check by ear|low confidence|timestamps?|the class said|students? (?:said|answered)|picture:)\b", re.I)
TS = re.compile(r"\s*\((?:~?\d{1,2}:\d{2}(?::\d{2})?|\d{3,5}(?:\.\d+)?)(?:\s*[-–]\s*(?:\d{1,2}:\d{2}(?::\d{2})?|\d{3,5}(?:\.\d+)?))?\)")
def clean_note(n):
    n = re.sub(r"\s+", " ", n or "").strip()
    if not n or AR_CHARS.search(n): return None     # Back Extra lines stay pure-Latin (playbook 7a)
    if META.search(n): return None                  # a worker's working note, not something she taught
    n = re.sub(r"\s+([.,;])", r"\1", TS.sub("", n)).strip()
    if len(n) > 280:                                   # cut at a sentence end, never mid-word
        cut = max(n.rfind(". ", 0, 280), n.rfind("; ", 0, 280))
        n = n[:cut + 1] if cut > 80 else n[:n.rfind(" ", 0, 277)] + "…"
    return n

def clean_translit(tr):
    """'khawkh (Shami: khookh)' -> 'khawkh'; gender pairs like 'anta / anti' are kept."""
    tr = re.sub(r"\s*\([^)]*\)", "", tr or "").split(";")[0]
    return re.sub(r"\s+", " ", tr).strip()

def clean_meaning(core, qual):
    """No Arabic script on the Text's English line (bidi scrambles it), and a crisp recalled span.
    -> (core, qualifier, extra) where extra is a 'but ...' tail moved to Back Extra."""
    def strip_ar(x):
        if not x: return x
        if AR_CHARS.search(x):
            x = re.sub(r"\s*(?:of|from|:)\s*[؀-ۿ\s]+", "", x)
            x = AR_CHARS.sub("", x)
        return re.sub(r"\s+", " ", x).strip(" ,;:-—")
    core, qual = strip_ar(core), strip_ar(qual)
    if qual and qual.lower() in ("plural", "singular", "noun", "verb", "adjective"): qual = None
    extra = None
    m = re.match(r"^(.{3,40}?)\s+(?:-|—|–)\s+(but .{12,})$", core or "")
    if m: core, extra = m.group(1), m.group(2)
    return core, (qual or None), extra

def md(date):  # 2026-09-24 -> 9/24
    y, m, d = date.split("-"); return f"{int(m)}/{int(d)}"

OVERRIDES = json.load(open(f"{BASE}/build/overrides.json")) if os.path.exists(f"{BASE}/build/overrides.json") else {}
SPLITS = []   # sibling words split off a shared skeleton during build_vocab; built as their own records
EDITOR = {}
for _p in (f"{BASE}/build/editor_output.json", f"{BASE}/build/editor_output2.json"):
    if os.path.exists(_p):
        try:
            EDITOR.update({e["key"]: e for e in json.load(open(_p))})
        except Exception as _e:
            print("editor output unreadable:", _p, _e, file=sys.stderr)

def her_clips_by_key():
    """key -> cut-log entry for every PASS* clip (targets.json carries the merge key of each slug)."""
    out = {}
    import glob as _g
    pairs = [(f"{BASE}/cutter/targets_batch1.json", f"{BASE}/cutter/cut_log.json")]
    for tp in sorted(_g.glob(f"{BASE}/cutter/targets[0-9]*.json")):
        n = os.path.basename(tp)[7:-5]
        pairs.append((tp, f"{BASE}/cutter/cut_log{n}.json"))
    pairs.append((f"{BASE}/cutter/targets_fix.json", f"{BASE}/cutter/cut_log_fix.json"))   # re-cuts override
    # spans marked NOT HER after a cutter had started (student turns, publisher audio, deliberate mistakes)
    excl = {}
    for f in _g.glob(f"{BASE}/lectures/*.json"):
        d = json.load(open(f))
        for w in d.get("words", []):
            for sp in w.get("not_her_spans") or []:
                if isinstance(sp, dict) and sp.get("file") and sp.get("start") is not None:
                    excl.setdefault(sp["file"], []).append((sp["start"] - 0.3, (sp.get("end") or sp["start"] + 1) + 0.3))
        for key in ("non_her_audio_windows", "do_not_clip_spans"):
            for sp in d.get(key) or []:
                if isinstance(sp, dict) and sp.get("start") is not None:
                    excl.setdefault(sp.get("file") or "teams_" + d.get("lecture", ""), []).append((sp["start"] - 0.3, (sp.get("end") or sp["start"] + 2) + 0.3))
    for fid, spans in json.load(open(f"{BASE}/cutter/exclusions.json")).items():
        if not fid.startswith("_"): excl.setdefault(fid, []).extend((a, b) for a, b, *_ in spans)
    def clean_clip(e):
        c = e.get("chosen") or {}
        return not any(c.get("s", 0) < b and c.get("e", 0) > a for a, b in excl.get(c.get("file"), []))
    for tp, lp in pairs:
        if not (os.path.exists(tp) and os.path.exists(lp)): continue
        log = json.load(open(lp))
        for t in json.load(open(tp)):
            e = log.get(t["slug"])
            if e and e.get("status", "").startswith("PASS") and clean_clip(e) and os.path.exists(f"{BASE}/clips/{e.get('out')}"):
                out[t["key"]] = e
    return out

def build_vocab(master, her_by_key, audit=None):
    notes, held = [], []
    audit = audit or {}
    drops = json.load(open(f"{BASE}/build/drop_list.json"))["keys"] if os.path.exists(f"{BASE}/build/drop_list.json") else {}
    for r in master:
        if r.get("anki"): continue
        if r["key"] in drops: held.append({"key": r["key"], "why": drops[r["key"]]}); continue
        x = resolve(r)
        if x is None: held.append({"key": r["key"], "why": "resolve: letter-name / pair / nonword / low-confidence gloss / no unit"}); continue
        # apply the gloss audit: a dropped Lingco ITEM leaves the word (its clip may say something else);
        # the word goes only when no item and no class evidence is left
        dropped = [it for it in x["lingco_items"] if (audit.get(it.get("id")) or {}).get("verdict") == "drop"
                   or (audit.get(it.get("id")) or {}).get("keep") is False]
        x["lingco_items"] = [it for it in x["lingco_items"] if it not in dropped]
        if dropped and not x["lingco_items"] and not x["khouri_items"]:
            held.append({"key": r["key"], "why": "gloss audit: drop — " + ((audit.get(dropped[0].get("id")) or {}).get("note") or "")[:160]}); continue
        for it in x["lingco_items"]:
            a = audit.get(it.get("id"))
            if a and not x["khouri_items"]:
                if a.get("meaning"):
                    c0, q0 = split_meaning(a["meaning"])
                    x["meaning_core"], x["qualifier"], _ = clean_meaning(c0, q0)
                if a.get("translit"):
                    t0 = clean_translit(a["translit"])
                    x["translit"] = t0; x["formal_translit"] = t0 if x["register"] == "formal" else None
        if x is None: held.append({"key": r["key"], "why": "gloss audit: drop"}); continue
        ov = OVERRIDES.get(r["key"], {})
        # two different words can share a consonant skeleton (jiib 'jeep' vs jayb 'pocket'): a Lingco item
        # whose FORMAL reading differs from this card's transliteration is not this word — it must not lend
        # its audio here, and it becomes its own practice card (queued in SPLITS for the caller)
        def _tn(t): return re.sub(r"[^a-z']", "", (t or "").lower().replace("-", ""))
        own, other = [], []
        for it in x["lingco_items"]:
            if (it.get("register") in (None, "formal") and it.get("translit") and x["khouri_items"]
                    and _tn(it["translit"]).rstrip("aiu") != _tn(x["translit"]).rstrip("aiu")
                    and bare(it.get("arabic") or "") == bare(x["arabic"])
                    and it.get("arabic") != x["arabic"]):
                other.append(it)
            else:
                own.append(it)
        if other:
            x["lingco_items"] = own
            sib_tr = _tn(other[0]["translit"])
            k_other = [k for k in x["khouri_items"] if _tn(k.get("translit")).rstrip("aiu") == sib_tr.rstrip("aiu")]
            x["khouri_items"] = [k for k in x["khouri_items"] if k not in k_other]
            SPLITS.append({"key": r["key"] + "#" + sib_tr, "arabic": other[0]["arabic"],
                           "translit": other[0]["translit"], "meaning": other[0].get("meaning"),
                           "units": [other[0].get("unit")], "lingco": other, "khouri": k_other, "anki": None})
        if ov.get("translit"): x["translit"] = ov["translit"]; x["formal_translit"] = ov["translit"] if x["register"] == "formal" else None
        if ov.get("arabic"): x["arabic"] = ov["arabic"]
        if ov.get("required"): x["required"] = True; x["pitfall"] = "she called this REQUIRED."
        ed = EDITOR.get(r["key"])
        if ed:
            if ed.get("flag") and not ov.get("unflag"):
                held.append({"key": r["key"], "why": "editor flag: " + ed["flag"], "arabic": x["arabic"], "translit": x["translit"]}); continue
            if ed.get("meaning_core"):
                x["meaning_core"], x["qualifier"], _ = clean_meaning(ed["meaning_core"], ed.get("qualifier"))
            x["her_notes"] = [n for n in (clean_note(n) for n in ed.get("notes") or []) if n][:3]
            x["also"] = ed.get("also") or x.get("also")
            x["how"] = clean_note(ed.get("how")) if ed.get("how") else None
        # audio
        media = {}
        slug_hit = her_by_key.get(r["key"])
        her = None
        if slug_hit:
            her = slug_hit["out"]; media[her] = f"{BASE}/clips/{her}"
        order = sorted(x["lingco_items"], key=lambda it: (not is_chart(it), bool((AUDIO_FIX.get(it.get("id")) or {}).get("trim_first"))))
        f_name, f_src = audio_of(order, "formal")
        s_name, s_src = audio_of(x["chart_shaami"] or x["lingco_items"], "shaami")
        if s_name and not x.get("shaami_translit"):
            src_it = next((it for it in (x["chart_shaami"] or x["lingco_items"]) for a in it.get("audio") or []
                           if a.get("dialect") == "shaami" and lingco_name(a) == s_name), None)
            if src_it and src_it.get("translit") and src_it.get("translit") != x["translit"]:
                x["shaami_translit"] = clean_translit(src_it["translit"])
            else:
                x["shaami_translit"] = "same word"
        if f_name: media[f_name] = f_src
        if s_name: media[s_name] = s_src
        her_audio_field = her if (her and slug_hit["status"] == "PASS") else None
        spec = vocab_note(x, her_audio_field, f_name, s_name, [])
        if her and not her_audio_field:
            spec["Back Extra"] += f"<br><br>Dr. Khouri says it: [sound:{her}]"
            if not spec["Audio"]: spec["Audio"] = f"[sound:{her}]"; spec["Back Extra"] = spec["Back Extra"].replace(f"<br><br>Dr. Khouri says it: [sound:{her}]", "")
        dates = sorted({(k.get("lecture_date") or k.get("lecture"))[:10] for k in x["khouri_items"] if (k.get("lecture_date") or k.get("lecture"))})
        if dates: spec["Back Extra"] += "<br><br>Class: " + ", ".join(md(d) for d in dates)
        tags = [f"arabic-u{x['unit']}", f"ARAB101::tier::{x['tier']}", "ARAB101::catchup-2026-09-29"] + from_tags(r)
        if x["required"]: tags.append("ARAB101::required")
        if not spec["Audio"]: tags.append("ARAB101::no-audio")
        spec.update({"deck": deck(x["unit"]), "tags": sorted(set(tags)), "media": media, "key": r["key"],
                     "her_status": slug_hit["status"] if slug_hit else None, "tier": x["tier"]})
        notes.append(spec)
    if SPLITS and not getattr(build_vocab, "_in_split", False):
        build_vocab._in_split = True
        todo = list(SPLITS); SPLITS.clear()
        extra, held2 = build_vocab(todo, {}, audit)
        build_vocab._in_split = False
        notes += extra; held += held2
    return notes, held
