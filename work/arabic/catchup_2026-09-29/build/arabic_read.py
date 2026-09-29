#!/usr/bin/env python3
"""Read fully-vowelled Arabic the way a beginner sounds it out, for the cards' "How it's built" line.

Two jobs:
  forms(word)      -> [(letter, 'isolated'|'initial'|'medial'|'final')] contextual shapes, exact
  breakdown(word)  -> (chunks, translit) e.g. دَجاج -> ([('دَ','da'),('جا','jaa'),('ج','j')], 'dajaaj')

The breakdown is only ever PRINTED on a card when its transliteration matches the known one
(self-check), so a rule this module gets wrong can cost a line, never teach a wrong reading.
Transliteration follows Parker's book convention (UPPERCASE emphatics, doubled long vowels,
c = cayn, ' = hamza).
"""
import re, unicodedata

FATHA, DAMMA, KASRA, SUKUUN, SHADDA = "َ", "ُ", "ِ", "ْ", "ّ"
TANWIN = {"ً": "an", "ٌ": "un", "ٍ": "in"}
DAGGER = "ٰ"
MARKS = set("ًٌٍَُِّْٰ")
JUNK = "ـ‌‍‎‏"

CONS = {"ب": "b", "ت": "t", "ث": "th", "ج": "j", "ح": "H", "خ": "kh", "د": "d", "ذ": "dh", "ر": "r",
        "ز": "z", "س": "s", "ش": "sh", "ص": "S", "ض": "D", "ط": "T", "ظ": "DH", "ع": "c", "غ": "gh",
        "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "و": "w", "ي": "y",
        "ء": "'", "أ": "'", "إ": "'", "ؤ": "'", "ئ": "'", "ة": "t"}
NAMES = {"ا": "alif", "ب": "baa", "ت": "taa", "ث": "thaa", "ج": "jiim", "ح": "Haa", "خ": "khaa",
         "د": "daal", "ذ": "dhaal", "ر": "raa", "ز": "zaay", "س": "siin", "ش": "shiin", "ص": "Saad",
         "ض": "Daad", "ط": "Taa", "ظ": "DHaa", "ع": "cayn", "غ": "ghayn", "ف": "faa", "ق": "qaaf",
         "ك": "kaaf", "ل": "laam", "م": "miim", "ن": "nuun", "ه": "haa", "و": "waaw", "ي": "yaa",
         "ء": "hamza", "أ": "hamza on alif", "إ": "hamza under alif", "آ": "alif madda",
         "ؤ": "hamza on waaw", "ئ": "hamza on yaa", "ة": "taa marbuuTa", "ى": "alif maqSuura"}
# letters that never join to the letter AFTER them
NONJOIN = set("اأإآدذرزوؤةءى")
SUN = set("تثدذرزسشصضطظلن")

def clean(s):
    s = unicodedata.normalize("NFC", s or "")
    return "".join(ch for ch in s if ch not in JUNK).strip()

def bare(s):
    return "".join(ch for ch in clean(s) if ch not in MARKS)

def units(word):
    """[(base_letter, marks_string)] ignoring spaces/punctuation."""
    out = []
    for ch in clean(word):
        if ch in MARKS:
            if out: out[-1] = (out[-1][0], out[-1][1] + ch)
        elif ch in NAMES:
            out.append((ch, ""))
        else:
            out.append((ch, ""))   # space / punctuation kept as separators
    return out

def forms(word):
    """Contextual shape of every letter, word by word (spaces break joining)."""
    res = []
    for w in re.split(r"[\s/،؟?!.]+", bare(word)):
        letters = [c for c in w if c in NAMES]
        for i, c in enumerate(letters):
            prev_joins = i > 0 and letters[i - 1] not in NONJOIN and letters[i - 1] != "ء"
            next_joins = i < len(letters) - 1 and c not in NONJOIN and c != "ء"
            if c == "ء":  # hamza on the line joins neither side
                prev_joins = next_joins = False
            f = {(False, False): "isolated", (False, True): "initial",
                 (True, True): "medial", (True, False): "final"}[(prev_joins, next_joins)]
            res.append((c, f))
    return res

def _one_word(w):
    """Sound out ONE vowelled word -> (chunks, translit) or (None, reason)."""
    u = [(c, m) for c, m in units(w) if c in NAMES]
    if not u: return None, "empty"
    chunks, tr = [], []
    i = 0
    # definite article al- (with sun-letter assimilation)
    if len(u) >= 2 and u[0][0] == "ا" and u[1][0] == "ل":
        nxt = u[2] if len(u) > 2 else None
        if nxt and nxt[0] in SUN and SHADDA in nxt[1]:
            chunks.append(("ال", "a" + CONS[nxt[0]] + "-")); tr.append("a" + CONS[nxt[0]] + "-")
        else:
            chunks.append(("ال", "al-")); tr.append("al-")
        i = 2
    while i < len(u):
        c, m = u[i]
        nxt = u[i + 1] if i + 1 < len(u) else None
        if c == "ا":                      # a bare alif inside the word = long aa carrier already consumed
            if i == 0:                    # initial bare alif = hamzat al-wasl / a
                v = "i" if KASRA in m else ("u" if DAMMA in m else "a")
                chunks.append((c + m, v)); tr.append(v); i += 1; continue
            return None, f"stray alif at {i}"
        if c == "ى":
            return None, "alif maqSuura"
        if c == "آ":
            chunks.append((c + m, "'aa")); tr.append("'aa"); i += 1; continue
        cons = CONS.get(c)
        if cons is None: return None, f"no cons for {c}"
        if c == "ة" and i == len(u) - 1:
            # taa marbuuTa: pronounced -a in pause (the -t only under possession, e.g. madiinat).
            # It rides on the previous chunk; if that chunk already ends in fatHa's a, add nothing.
            if not chunks: return None, "bare taa marbuuTa"
            prev_ar, prev_tr = chunks[-1]
            add = "" if prev_tr.endswith("a") else "a"
            if any(x in m for x in TANWIN): add = ("" if prev_tr.endswith("a") else "a") + "n"
            chunks[-1] = (prev_ar + c + m, prev_tr + add); tr[-1] = prev_tr + add
            i += 1; continue
        seg_ar = c + m
        s = cons * (2 if SHADDA in m else 1)
        vowel = None
        if FATHA in m: vowel = "a"
        elif DAMMA in m: vowel = "u"
        elif KASRA in m: vowel = "i"
        for t, v in TANWIN.items():
            if t in m: vowel = v
        if DAGGER in m: vowel = "aa"
        # long vowels: consonant + short vowel + matching letter (or bare long letter after an unmarked consonant)
        if nxt and nxt[0] == "ا" and (vowel in (None, "a")) and not any(t in m for t in TANWIN):
            seg_ar += nxt[0] + nxt[1]; s += "aa"; i += 2
            if nxt[1] and any(t in nxt[1] for t in TANWIN): s = s[:-2] + "an"
        elif nxt and nxt[0] == "ا" and vowel == "an":   # tanwiin al-fatH on the consonant, alif seat
            seg_ar += nxt[0] + nxt[1]; s += "an"; i += 2
        elif nxt and nxt[0] == "و" and vowel in (None, "u") and not nxt[1].strip(SUKUUN):
            if vowel == "u" or not nxt[1]:
                seg_ar += nxt[0] + nxt[1]; s += "uu"; i += 2
            else:
                s += vowel or ""; i += 1
        elif nxt and nxt[0] == "ي" and vowel in (None, "i") and not nxt[1].strip(SUKUUN):
            if vowel == "i" or not nxt[1]:
                seg_ar += nxt[0] + nxt[1]; s += "ii"; i += 2
            else:
                s += vowel or ""; i += 1
        else:
            s += vowel or ""; i += 1
        chunks.append((seg_ar, s)); tr.append(s)
    return chunks, "".join(tr)

def breakdown(phrase):
    words = [w for w in re.split(r"\s+", clean(phrase).replace("؟", "").replace("?", "")) if w]
    allc, trs = [], []
    for w in words:
        ch, tr = _one_word(w)
        if ch is None: return None, tr
        allc.append(ch); trs.append(tr)
    return allc, " ".join(trs)

def norm_tr(s):
    s = (s or "").replace("’", "'").replace("‘", "'").replace("ʾ", "'").replace("ʿ", "c")
    s = re.sub(r"[\s\-?.!,/]+", "", s)
    return s

def verified_breakdown(arabic, translit):
    """Return the chunks only if sounding them out reproduces the known transliteration."""
    ch, tr = breakdown(arabic)
    if ch is None: return None
    a, b = norm_tr(tr), norm_tr(translit)
    # Only three legitimate differences are forgiven: an unwritten word-initial hamza, tanwiin
    # endings (-an/-un/-in) read in pause, and taa marbuuTa's -a written -at under possession.
    def variants(x):
        v = {x, x.lstrip("'")}
        for y in list(v):
            for suf in ("an", "un", "in"):
                if y.endswith(suf): v.add(y[: -len(suf)])
            if y.endswith("at"): v.add(y[:-1])
        return v
    if variants(a) & variants(b):
        return ch
    return None

def spell(arabic):
    """'daal + jiim + alif + jiim' — the letters in order, by name."""
    parts = []
    for w in re.split(r"\s+", bare(arabic)):
        names = [NAMES[c] for c in w if c in NAMES]
        if names: parts.append(" + ".join(names))
    return "  |  ".join(parts)

if __name__ == "__main__":
    for w, t in [("دَجاج", "dajaaj"), ("جَديد", "jadiid"), ("أُخْت", "ukht"), ("تَفَضَّل", "tafaDDal"),
                 ("بَيْت", "bayt"), ("كِتاب", "kitaab"), ("صَباح الْخَير", "SabaaH al-khayr"),
                 ("سُؤال", "su'aal"), ("خُدود", "khuduud"), ("طالِبة", "Taaliba"), ("مَرحَباً", "marHaban"),
                 ("أُسْتاذ", "ustaadh"), ("إِثْبات", "ithbaat"), ("الْحَمدُ لِلّه", "al-Hamdu lillaah"),
                 ("مدينة", "madiinat"), ("مَدينة", "madiina"), ("جَديدة", "jadiida"), ("هٰذِهِ", "haadhihi"),
                 ("شُكْراً", "shukran"), ("طالِب", "Taalib"), ("طالِبة", "Taalib")]:
        print(w, forms(w), breakdown(w)[1], "VERIFIED" if verified_breakdown(w, t) else "no", spell(w))
