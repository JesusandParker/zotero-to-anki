#!/usr/bin/env python3
"""Letter lane for the catch-up: Unit 4 connected-form notes (daal, dhaal, raa, zaay), hamza seat
notes, and example-word picking for every (letter x form) note old and new.

Shape = block A_letter_forms (check_block_spec F1-F4): ‎{{c1::<shape>}} / Letter: {{c2::name}} /
Position: {{c2::position}}; Back Extra carries Distinguish/Shape/Sound lines, the book's own
printed Writing row (plate) with a Roster: line, an example word WITH audio, and her voice.
Explanations are the BOOK's (Alif Baa 3e pp. 67-83, printed) in plain words — nothing invented.
"""
from arabic_read import forms, bare

U4_FORMS = [
    {"letter": "د", "name": "daal", "shape": "ـد", "position": "medial and final::name both",
     "plate": "arabic_u4_forms_daal_v1.png", "video": "arabic_pron_08_daal.mp4",
     "distinguish": "daal never joins to the letter after it, so the next letter always starts fresh. "
                    "daal and dhaal share this one shape — only dhaal's dot sets it apart.",
     "shape_line": "a sharp angle that sits ON the line: slant down from well above the line, turn sharply, "
                   "finish along the line. Joined from the right, start from the connecting stroke, go up, then back down.",
     "sound": "a clear, frontal d, as in deep (not the darker d of puddle) — and keep the vowels around it frontal too.",
     "roster": "daal's four written forms run right to left across the row — independent, initial, <b>medial</b>, <b>final</b>."},
    {"letter": "ذ", "name": "dhaal", "shape": "ـذ", "position": "medial and final::name both",
     "plate": "arabic_u4_forms_dhaal_v1.png", "video": "arabic_pron_09_dhaal.mp4",
     "distinguish": "dhaal is written exactly like daal plus one dot above; like daal it never joins forward.",
     "shape_line": "daal's sharp angle on the line, with a single dot above.",
     "sound": "the th of the and other — the book's pun: dhaal is the OTHER th (thaa is the th of three).",
     "roster": "dhaal's four written forms run right to left across the row — independent, initial, <b>medial</b>, <b>final</b>."},
    {"letter": "ر", "name": "raa", "shape": "ـر", "position": "medial and final::name both",
     "plate": "arabic_u4_forms_raa_v1.png", "video": "arabic_pron_10_raa.mp4",
     "distinguish": "raa never joins forward. Tell it from daal by where it sits: raa's wide curve drops BELOW the line; "
                    "daal's sharp angle stays on top of it.",
     "shape_line": "joined from the right, start on the line and drop straight down — no little tooth going up first.",
     "sound": "a flap, like the Spanish r — the same flick your tongue makes in 'gotta go'. raa also deepens a nearby "
              "alif or fatHa so it sounds like the a in father.",
     "roster": "raa's four written forms run right to left across the row — independent, initial, <b>medial</b>, <b>final</b>."},
    {"letter": "ز", "name": "zaay", "shape": "ـز", "position": "medial and final::name both",
     "plate": "arabic_u4_forms_zaay_v1.png", "video": "arabic_pron_11_zaay.mp4",
     "distinguish": "zaay is written exactly like raa plus one dot above; like raa it never joins forward.",
     "shape_line": "raa's curve dropping below the line, with one dot above.",
     "sound": "z as in zebra.",
     "roster": "zaay's four written forms run right to left across the row — independent, initial, <b>medial</b>, <b>final</b>."},
]

HAMZA_FORMS = [
    {"letter": "أ", "name": "hamza on alif", "shape": "أ", "position": "start of a word, with fatHa or Damma",
     "plate": "arabic_u4_forms_hamza_v1.png", "video": None,
     "distinguish": "at the start of a word, alif is ALWAYS a seat for hamza, never a long vowel. The vowel written "
                    "on it tells you which sound follows the catch: fatHa a, Damma u.",
     "shape_line": "hamza is a small c-shape that runs into a short line at the bottom; here it sits on top of the alif.",
     "sound": "a glottal stop, the catch in uh-oh, then the vowel.",
     "roster": "the plate shows hamza on its own (on the line) and <b>hamza on alif</b>."},
    {"letter": "إ", "name": "hamza under alif", "shape": "إ", "position": "start of a word, with kasra",
     "plate": "arabic_u4_forms_hamza_v1.png", "video": None,
     "distinguish": "hamza written UNDER the alif always means the vowel is kasra (i) — the kasra goes under too.",
     "shape_line": "the same small c-shaped hamza, hanging below the alif.",
     "sound": "a glottal stop followed by i.",
     "roster": "the plate shows hamza on the line and hamza on alif; this card is its kasra version, <b>under</b> the alif."},
    {"letter": "ء", "name": "hamza on the line", "shape": "ـاء", "position": "end of a word, after a long vowel",
     "plate": "arabic_u4_forms_hamza_v1.png", "video": None,
     "distinguish": "after a long vowel at the end of a word, hamza has no seat — it sits on the line by itself, a "
                    "little bigger. The letter names baa', taa', thaa', Haa', khaa' all end this way.",
     "shape_line": "a free-standing hamza on the line; the alif before it does not join to it.",
     "sound": "the long vowel, then a catch in the throat to finish.",
     "roster": "the plate shows <b>hamza on the line</b> (right) and hamza on alif."},
]

def letter_form_of(word, letter, want):
    """True if `letter` appears in `word` with contextual form matching `want`.
    For non-connectors, 'medial and final' means joined from the right (forms() calls that 'final')."""
    for c, f in forms(word):
        if c != letter: continue
        if want in ("medial and final", "connected") and f in ("final", "medial"): return True
        if f == want: return True
    return False

def pick_examples(pool, letter, want, n=1, avoid=()):
    """pool: [{arabic, translit, meaning, audio, priority}] -> best n examples showing the form."""
    cands = [w for w in pool if w.get("audio") and w["arabic"] not in avoid
             and letter_form_of(w["arabic"], letter, want)]
    cands.sort(key=lambda w: (w.get("priority", 9), len(bare(w["arabic"])), w["translit"]))
    return cands[:n]

# ---------------------------------------------------------------- note specs
import os, html
LRM = "‎"
ROOT = "all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I"
PLATES = os.path.expanduser("~/.claude/skills/zotero-to-anki/work/arabic/u4/media")

def example_lines(ex):
    """Latin line + pure-Arabic line + audio, never mixing scripts on one line (playbook 7a)."""
    out = []
    for w in ex:
        out.append(f"Ex: <i>{html.escape(w['translit'], quote=False)}</i> ({html.escape(w['meaning'], quote=False)}) — {html.escape(w['why'], quote=False)} [sound:{w['audio']}]")
        out.append(f"<span style='font-size:28px'>{LRM}{w['arabic']}</span>")
    return out

def form_note(F, examples, her_clip=None, unit=4):
    text = (f"{LRM}{{{{c1::{F['shape']}}}}}<br><br>Letter: {{{{c2::{F['name']}}}}}<br><br>"
            f"Position: {{{{c2::{F['position']}}}}}")
    be = [f"Distinguish: {F['distinguish']}", f"Shape: {F['shape_line']}", f"Sound: {F['sound']}",
          f"Roster: {F['roster']}", f"<img src=\"{F['plate']}\">"] + example_lines(examples)
    if her_clip: be.append(f"Dr. Khouri says it: [sound:{her_clip}]")
    media = {F["plate"]: f"{PLATES}/{F['plate']}"}
    for w in examples: media[w["audio"]] = w["audio_src"]
    if her_clip: media[her_clip] = os.path.expanduser(f"~/arabic-catchup/clips/{her_clip}")
    audio = f"[sound:{F['video']}]" if F.get("video") else (f"[sound:{her_clip}]" if her_clip else "")
    if her_clip and audio == f"[sound:{her_clip}]":        # one home per clip (U3): not also in Back Extra
        be = [l for l in be if l != f"Dr. Khouri says it: [sound:{her_clip}]"]
    if not audio and examples:                              # no video, no clip of her: the example plays on flip
        a = examples[0]["audio"]; audio = f"[sound:{a}]"
        be = [l.replace(f" [sound:{a}]", "") for l in be]
    return {"block": "A_letter_forms", "image": F["plate"], "Text": text, "Back Extra": "<br><br>".join(be),
            "Audio": audio,
            "deck": f"{ROOT}::Unit {unit:02d}", "media": media,
            "tags": ["arabic-u4", "ARAB101::tier::letters", "ARAB101::catchup-2026-09-29", "ARAB101::from::book", "u4-positions"]}

WHY_FORM = {"medial and final::name both": "joined from the right, so it takes this connected shape",
            "start of a word, with fatHa or Damma": "it opens the word, so the hamza sits on an alif seat",
            "start of a word, with kasra": "it opens the word with an i-vowel, so the hamza hangs under the alif",
            "end of a word, after a long vowel": "it follows a long aa at the end, so it sits on the line"}

from arabic_read import NAMES, NONJOIN, bare as _bare
def form_instances(word):
    """[(letter, form, prev_letter, next_letter)] per word-part, same joining rules as forms()."""
    out = []
    import re as _re
    for w in _re.split(r"[\s/،؟?!.]+", _bare(word)):
        L = [c for c in w if c in NAMES]
        for i, c in enumerate(L):
            pj = i > 0 and L[i - 1] not in NONJOIN and L[i - 1] != "ء" and c != "ء"
            nj = i < len(L) - 1 and c not in NONJOIN and c != "ء"
            f = {(False, False): "isolated", (False, True): "initial", (True, True): "medial", (True, False): "final"}[(pj, nj)]
            out.append((c, f, L[i - 1] if i > 0 else None, L[i + 1] if i < len(L) - 1 else None))
    return out

def reason(letter, form, prev, nxt, want):
    n = NAMES.get(letter, letter); p = NAMES.get(prev, prev); x = NAMES.get(nxt, nxt)
    if want in ("initial",):
        if prev:   # initial shape mid-word: the letter before it is a non-connector
            return f"{p} never joins forward, so {n} starts fresh and reaches forward to join {x}"
        return f"{n} opens the word and reaches forward to join {x}"
    if want == "medial":
        return f"{p} joins {n} from the right, and {n} reaches forward to {x}"
    if want == "final":
        return f"{p} joins {n} from the right, and the word ends there"
    if want.startswith("medial and final"):
        tail = " — and since it never joins forward, " + (f"{x} after it starts fresh" if nxt else "the word simply ends") 
        return f"{p} joins {n} from the right{tail}"
    return ""

def pick_example(pool, letter, want, avoid=()):
    """pool items: {arabic, translit, meaning, audio, audio_src, priority}. want: initial|medial|final|medial and final"""
    best = None
    for w in pool:
        if not w.get("audio") or w["arabic"] in avoid: continue
        for (c, f, p, x) in form_instances(w["arabic"]):
            if c != letter: continue
            ok = (f == want) or (want.startswith("medial and final") and f in ("final", "medial"))
            if not ok: continue
            key = (w.get("priority", 9), len(_bare(w["arabic"])), w["translit"])
            if best is None or key < best[0]:
                best = (key, {**w, "why": reason(letter, f, p, x, want)})
            break
    return best[1] if best else None
