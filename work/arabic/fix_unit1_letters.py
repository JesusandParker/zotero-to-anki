#!/usr/bin/env python3
"""Unit 1 letter/symbol cards: add the BOOK's transliteration symbol + association hooks.

Parker, 2026-08-27: "I don't really have much to associate these letters with... I need
the actual transliteration symbol and the sound... and in the back extra any distinguishing
remarks" — his c1 cards (produce the glyph) were at 4-10 reps with intervals stuck at 0-1d.

GROUNDING (his explicit instruction: "don't just invent a transliteration system it's all
in Zotero"): every symbol + sound string below is read off the book's own charts —
Alif Baa 3e, Unit 1, printed pp. 11-12 = physical PDF pp. 25-26, the two "Transliteration
symbol and sound" consonant charts + the Vowels chart. Crops already live on the cards
(arabic_src_consonants1_v3.png / consonants2 / vowels). Hamza's symbol is the apostrophe,
corroborated by the book's own prose ("Qur'an").

NOT invented, NOT extended: tanwiin / sukuun / shadda / waSla / dagger alif / alif madda /
alif maqSuura / taa marbuuTa get NO transliteration line — Unit 1's symbols chart gives
names only, and guessing is forbidden (SKILL.md rule 2).

Shape:/Hook:/added Distinguish: lines are authored teaching aids, not book text. They carry
no factual claim about the book and are never cloze answers, so R13 grounding is unaffected.
"""
import json, re, sys, urllib.request

ANKI = "http://localhost:8765"
LRM  = "‎"

def anki(action, **params):
    r = json.load(urllib.request.urlopen(
        ANKI, json.dumps({"action": action, "version": 6, "params": params}).encode()))
    if r.get("error"):
        sys.exit(f"AnkiConnect: {r['error']}")
    return r["result"]

# ---------------------------------------------------------------------------
# glyph: (name, translit, shape hook, extra Distinguish line or None)
# translit + the existing Sound line are the book's; shape/distinguish are teaching aids.
# ---------------------------------------------------------------------------
LETTERS = {
 "ا": ("alif", "aa",
       "one bare upright stroke, no dots — the simplest letter on the chart",
       "Distinguish: alif is a plain vertical stroke; laam is the same height but sweeps into a bowl at its base."),
 "ب": ("baa", "b",
       "a shallow boat sitting on the line, one dot slung underneath", None),
 "ت": ("taa", "t",
       "the same shallow boat, two dots riding on top", None),
 "ث": ("thaa", "th",
       "the same shallow boat, three dots stacked on top", None),
 "ج": ("jiim", "j",
       "a curl with a deep belly, one dot tucked inside the belly", None),
 "ح": ("Haa", "H",
       "the same curl and belly, swept clean — no dot anywhere", None),
 "خ": ("khaa", "kh",
       "the same curl and belly, one dot sitting above it", None),
 "د": ("daal", "d",
       "a short bent elbow that opens to the left and rests on the line", None),
 "ذ": ("dhaal", "dh",
       "the same bent elbow, one dot above", None),
 "ر": ("raa", "r",
       "a bare curved stroke that dives below the line, like a comma's tail", None),
 "ز": ("zaay", "z",
       "the same diving tail, one dot above", None),
 "س": ("siin", "s",
       "three little teeth in a row, then a dish that scoops below the line", None),
 "ش": ("shiin", "sh",
       "the same three teeth and dish, with three dots above them", None),
 "ص": ("Saad", "S",
       "a closed loop with a long flat tail — a suitcase with its handle", None),
 "ض": ("Daad", "D",
       "the same loop and flat tail, one dot above", None),
 "ط": ("Taa", "T",
       "a loop lying on the line with a mast standing straight up out of it", None),
 "ظ": ("DHaa", "DH",
       "the same loop and mast, one dot above", None),
 "ع": ("cayn", "c",
       "an open hook with its mouth up, like a numeral 3 turned to face the other way", None),
 "غ": ("ghayn", "gh",
       "the same open hook, one dot above", None),
 "ف": ("faa", "f",
       "a small closed head resting on the line with a short tail, one dot above",
       "Distinguish: faa one dot above, qaaf two dots above — and qaaf's tail scoops below the line while faa's stays on it."),
 "ق": ("qaaf", "q",
       "a closed head with a deep bowl scooping below the line, two dots above", None),
 "ك": ("kaaf", "k",
       "an angular bend with a small stroke tucked inside it, like a folded chair",
       "Distinguish: kaaf carries a little mark inside its angle; laam is a clean stroke with nothing inside."),
 "ل": ("laam", "l",
       "a tall stroke that sweeps into a wide bowl at the bottom — an elongated L, and the letter IS l",
       "Distinguish: laam curves into a bowl at its base; alif is the same height but stops straight."),
 "م": ("miim", "m",
       "a small round head with a tail dropping straight down below the line",
       "Distinguish: miim, waaw and faa all have round heads — miim's tail drops straight down, waaw's sweeps down and left, faa's stays on the line under one dot."),
 "ن": ("nuun", "n",
       "a deep round bowl dipping below the line, one dot above",
       "Distinguish: nuun is a deep bowl with its dot ABOVE; baa is a shallow boat with its dot BELOW."),
 "ه": ("haa", "h",
       "a small closed knot or loop, no dots",
       "Distinguish: haa is the bare knot; taa marbuuTa is that same knot wearing two dots above."),
 "و": ("waaw", "w — as a long vowel, uu",
       "a round head with a tail sweeping down and to the left, below the line",
       "Distinguish: waaw dips below the line with a round head; raa dips below with no head at all."),
 "ي": ("yaa", "y — as a long vowel, ii",
       "a wide bowl swinging below the line with two dots underneath",
       "Distinguish: yaa has TWO dots below and swings deep; baa has ONE dot below and stays shallow."),
}

# Book-given transliteration for symbols. Unit 1's Vowels chart supplies the three short
# vowels; the consonant chart supplies hamza. Everything else is deliberately absent.
SYMBOLS = {"بَ": "a", "بُ": "u", "بِ": "i", "ء": "'"}

IMG = re.compile(r'<img\s[^>]*>')


def rebuild_text(text, translit):
    """Insert 'Transliteration: {{c2::X}}' between the Name and Sound lines.

    Idempotent: an existing Transliteration line is replaced, not duplicated.
    """
    text = re.sub(r'Transliteration:\s*\{\{c2::.*?\}\}(<br>)*', '', text)
    line = f'Transliteration: {{{{c2::{translit}}}}}'
    if 'Sound:' in text:
        return text.replace('<br><br>Sound:', f'<br><br>{line}<br><br>Sound:', 1)
    return text.rstrip() + f'<br><br>{line}'          # symbols with no Sound line


def rebuild_back(back, additions):
    """Preserve Parker's Back Extra byte-for-byte; add new lines before the image.

    Back Extra is `edited` on all 28 letters (his own notes live there — e.g. khaa's
    'like clearing your pharanix'), so this NEVER rewrites what is there. It splits off
    the trailing <img>, keeps the prefix exactly, appends, then re-attaches the image.
    """
    m = IMG.search(back)
    img = m.group(0) if m else ""
    prefix = back[:m.start()] if m else back
    prefix = re.sub(r'(<br>\s*)+$', '', prefix)
    # idempotence: drop any Shape:/Hook: lines a previous run of THIS script added
    prefix = re.sub(r'(<br>)*\s*(Shape|Hook):[^<]*(?=(<br>|$))', '', prefix)
    prefix = re.sub(r'(<br>\s*)+$', '', prefix)
    parts = [p for p in [prefix.strip()] if p] + additions
    body = "<br><br>".join(parts)
    return (body + ("<br><br>" + img if img else "")) if body else img


def load_original_meta():
    """glyph -> the original card's provenance, so the enriched card keeps it."""
    try:
        orig = json.load(open("work/arabic/unit_1_cards.json"))
    except FileNotFoundError:
        return {}
    out = {}
    for c in orig:
        m = re.match(r'\s*‎?\{\{c1::([^\}]+)\}\}', c["Text"])
        if m:
            out[m.group(1)] = c
    return out


ORIG = {}


def main():
    global ORIG
    ORIG = load_original_meta()
    apply = "--apply" in sys.argv
    notes = anki("notesInfo", notes=anki(
        "findNotes",
        query='deck:"all::LIBERTY::LIBERTY FALL 2026::ARAB 101 - Elementary Arabic I::Unit 1::Book Highlights"'))

    updates, cards = [], []
    for n in notes:
        text = n["fields"]["Text"]["value"]
        back = n["fields"]["Back Extra"]["value"]
        m = re.match(r'\s*‎?\{\{c1::([^\}]+)\}\}', text)
        if not m:
            continue
        g = m.group(1)

        if g in LETTERS:
            name, translit, shape, extra_dist = LETTERS[g]
            # The name-opens-with-its-own-sound rule holds for all 27 consonants and is
            # the single strongest association here: recall either the name or the symbol
            # and the other falls out. alif is the one letter it does NOT fit — it is a
            # long vowel, so it gets the honest exception instead of a false hook.
            hook = ("Hook: alif is the exception — every other letter's name opens with "
                    "its own sound, but alif is a long vowel and carries no consonant."
                    if g == "ا" else
                    f"Hook: the name {name} opens with its own sound, "
                    f"{translit.split(' —')[0]}.")
            adds = ([extra_dist] if extra_dist and "Distinguish:" not in back else []) + [
                f"Shape: {shape}.", hook,
            ]
            new_text, new_back = rebuild_text(text, translit), rebuild_back(back, adds)
            block = "A_letters"
        elif g in SYMBOLS:
            new_text, new_back = rebuild_text(text, SYMBOLS[g]), back
            block = "B_symbols"
        else:
            continue

        if new_text != text or new_back != back:
            updates.append({"id": n["noteId"],
                            "fields": {"Text": new_text, "Back Extra": new_back}})
        # Inherit provenance from the original Unit 1 batch so Rule 1 stays verifiable —
        # this is the SAME card, enriched, not a new one.
        meta = ORIG.get(g, {})
        cards.append({"Text": new_text, "Back Extra": new_back, "block": block,
                      "source": "arabic", "segment": 1,
                      "from_idx": meta.get("from_idx", []),
                      "verified_against": (meta.get("verified_against") or "") +
                          " + transliteration symbol read off the 'Transliteration symbol "
                          "and sound' charts, printed pp.11-12 (physical pp.25-26)",
                      "verified_by": (meta.get("verified_by") or "") +
                          "; transliteration transcribed from page renders 2026-08-27",
                      "visual_source": meta.get("visual_source"),
                      "noteId": n["noteId"], "glyph": g})

    json.dump(cards, open("work/arabic/unit_1_letters_fixed_cards.json", "w"),
              ensure_ascii=False, indent=1)
    print(f"{len(cards)} cards rebuilt, {len(updates)} notes need writing")

    if not apply:
        print("\n(dry run — pass --apply to write)")
        for u in updates[:2]:
            print("\n", u["fields"]["Text"], "\n --\n", u["fields"]["Back Extra"])
        return

    import authorship as A
    store = A.load("arabic")
    for u in updates:
        anki("updateNoteFields", note=u)
        A.record("arabic", u["id"], {"Text": u["fields"]["Text"]}, store=store)
    A.save("arabic", store)
    print(f"wrote {len(updates)} notes; authorship recorded for Text")


if __name__ == "__main__":
    sys.path.insert(0, "scripts")
    main()
