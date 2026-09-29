#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ~/arabic-catchup/lingco/lingco_words.{json,md}: every Lingco (Alif Baa 3e) Units 1-4 item that has
publisher audio, mapped item-by-item to its clip(s), with meanings. Pure function of the inputs; re-run after
~/arabic-catchup/clipcheck/clips_asr.json appears to fill in / refresh the ASR confirmation fields.

No ML is run here. Reads: all_u14.json, the arabic-vault lesson texts/tables, lingco_data.py (curated),
clip_durations.json (ffprobe cache), clips_asr.json (optional)."""
import json, os, re, sys, difflib, collections, datetime

HOME = os.path.expanduser('~')
BASE = f'{HOME}/arabic-catchup'
OUT = f'{BASE}/lingco'
VAULT = f'{HOME}/arabic-vault'
MEDIA = f'{VAULT}/media'
AUD = f'{BASE}/lingco_video/aud'
MP4 = f'{BASE}/lingco_video/mp4'
LETTER_DIR = f'{HOME}/Anki Media Archive/Arabic - Al-Kitaab pronunciation'
ASR_PATH = os.environ.get('LINGCO_ASR_PATH', f'{BASE}/clipcheck/clips_asr.json')
OUT_SUFFIX = os.environ.get('LINGCO_OUT_SUFFIX', '')  # testing only

sys.dont_write_bytecode = True
sys.path.insert(0, OUT)
import lingco_data as D  # noqa: E402

# ------------------------------------------------------------------ Arabic helpers
INVIS = re.compile('[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad]')
MARKS = re.compile('[\u064b-\u065f\u0670\u06d6-\u06ed]')
TATWEEL = '\u0640'
PUNCT = re.compile(r'[؟?…!,،.\"“”]')

def clean(s):
    s = INVIS.sub('', s or '')
    s = s.replace(TATWEEL, '')
    s = re.sub(r'\s*/\s*', ' / ', s)
    return ' '.join(s.split())

def bare(s):
    s = MARKS.sub('', clean(s))
    s = PUNCT.sub('', s)
    return ' '.join(s.split())

def an(s):
    """normalisation for ASR comparison"""
    s = MARKS.sub('', INVIS.sub('', s or '')).replace(TATWEEL, '')
    s = re.sub('[أإآٱ]', 'ا', s)
    s = s.replace('ة', 'ه').replace('ى', 'ي').replace('ؤ', 'و').replace('ئ', 'ي')
    s = re.sub(r'[^\u0621-\u064a ]', ' ', s)
    return ' '.join(s.split())

UNIT_LETTERS = list('ابتثجحخدذرزوي')  # + hamza handled separately
HAMZA_SEATS = {'ء': 'line', 'أ': 'alif', 'إ': 'alif', 'آ': 'alif-madda', 'ؤ': 'waaw', 'ئ': 'yaa'}
# letters that never connect to the FOLLOWING letter
NON_FWD = set('اأإآٱدذرزوؤءةى')
ARABIC_LETTER = re.compile('[\u0621-\u064a\u0671]')

def letter_positions(ar):
    """{letter: [forms in order of occurrence]} for Unit 1-4 letters; hamza -> word position + seat."""
    pos = collections.OrderedDict()
    hamza = []
    for word in re.split(r'[\s/]+', MARKS.sub('', INVIS.sub('', ar or ''))):
        chars = [c for c in word if ARABIC_LETTER.match(c) or c == TATWEEL]
        letters_idx = [i for i, c in enumerate(chars) if c != TATWEEL]
        for i, c in enumerate(chars):
            if c == TATWEEL:
                continue
            prev = chars[i - 1] if i > 0 else None
            nxt = chars[i + 1] if i + 1 < len(chars) else None
            joins_back = c != 'ء'
            joins_fwd = c not in NON_FWD
            conn_prev = bool(prev) and joins_back and (prev == TATWEEL or prev not in NON_FWD)
            conn_next = bool(nxt) and joins_fwd and (nxt == TATWEEL or nxt != 'ء')
            form = {(True, True): 'medial', (True, False): 'final',
                    (False, True): 'initial', (False, False): 'isolated'}[(conn_prev, conn_next)]
            if c in UNIT_LETTERS:
                lst = pos.setdefault(c, [])
                if form not in lst:
                    lst.append(form)
            if c in HAMZA_SEATS:
                wpos = 'initial' if i == letters_idx[0] else ('final' if i == letters_idx[-1] else 'medial')
                lst = pos.setdefault('ء', [])
                if wpos not in lst:
                    lst.append(wpos)
                hamza.append({'char': c, 'seat': HAMZA_SEATS[c], 'word_position': wpos,
                              'glyph_form': form})
    return dict(pos), hamza

# ------------------------------------------------------------------ inputs
W = json.load(open(f'{BASE}/lingco_video/all_u14.json'))
DUR = json.load(open(f'{OUT}/clip_durations.json'))
TABLES = json.load(open(f'{VAULT}/data/other_tables.json'))
ASR = json.load(open(ASR_PATH)) if os.path.exists(ASR_PATH) else None
BY_UUID = {w['uuid']: w for w in W}
LEXF = {}  # vault file -> Arabic exactly as the Lingco vocab cell prints it
for _e in json.load(open(f'{VAULT}/data/lexicon.json'))['entries']:
    for _d, _form in _e['forms'].items():
        for _f in _form.get('files', []):
            LEXF[_f] = _form.get('ar')

def parse_origin(o):
    o = o or ''
    m = re.match(r'^AB3e_U(\d)LE(\d+)-(\d+)\.mp3$', o)
    if m: return ('LE', int(m[1]), int(m[2]), int(m[3]), None)
    m = re.match(r'^(?:AB3e_)?U(\d)D(\d+)[-_](\d+)\.(?:mp3|mp4)$', o)
    if m: return ('D', int(m[1]), int(m[2]), int(m[3]), None)
    m = re.match(r'^AB3e_U(\d)V(St|S|E)-(\d+)\.mp3$', o)
    if m: return ('V', int(m[1]), 0, int(m[3]), {'St': 'formal', 'S': 'shaami', 'E': 'masri'}[m[2]])
    m = re.match(r'^AB3e_Num(St|S|E)-(\d+)\.mp3$', o)
    if m: return ('NUM', 4, 0, int(m[2]), {'St': 'formal', 'S': 'shaami', 'E': 'masri'}[m[1]])
    m = re.match(r'^AB3e_pronouncing_(\d+)_\w+\.mp4$', o)
    if m: return ('LETTER', 1, 1, int(m[1]), None)
    return ('OTHER', None, None, None, None)

IDX = collections.defaultdict(list)
for w in W:
    k = parse_origin(w['origin'])
    IDX[k[:4]].append(w)

USED = collections.Counter()

def clip_entry(w, dialect=None, note=None):
    f = w['file']; stem = os.path.splitext(f)[0]
    vp = f'{MEDIA}/{f}'; ap = f'{AUD}/{stem}.wav'; mp = f'{MP4}/{stem}.mp4'
    if os.path.exists(vp):
        path, video = vp, None
    elif os.path.exists(ap):
        path, video = ap, (mp if os.path.exists(mp) else None)
    elif 'pronouncing' in (w['origin'] or ''):
        path = video = f'{LETTER_DIR}/{w["origin"]}'
    else:
        path, video = None, None
    e = collections.OrderedDict()
    e['file'] = os.path.basename(path) if path else f
    e['path'] = path
    if video: e['video_path'] = video
    e['origin'] = w['origin']
    e['dialect'] = dialect or w.get('dialect') or 'formal'
    e['dur'] = (DUR.get(f) or {}).get('dur')
    e['lingco_uuid'] = w['uuid']
    e['asr_key'] = f
    if note: e['note'] = note
    USED[f] += 1
    return e

def clips_for(kind, unit, lesson_no, item):
    return IDX.get((kind, unit, lesson_no, item), [])

# ------------------------------------------------------------------ printed forms
def lesson_items(relpath):
    t = open(f'{VAULT}/data/lessons/{relpath}', encoding='utf-8').read()
    out = {}
    for line in t.splitlines():
        m = re.match(r'^\s*([0-9\u0660-\u0669]+)\s*\.\s*(.*\S)\s*$', INVIS.sub('', line))
        if m and re.search('[\u0600-\u06ff]', m[2]):
            n = int(m[1].translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
            out[n] = clean(m[2])
    return out

def table_items(unit, lesson):
    out = {}
    for t in TABLES:
        if t['unit'] == unit and t['lesson'] == lesson and len(t['header']) >= 2:
            m = re.match(r'^\.(\d+)$', t['header'][1].strip())
            if m:
                out[int(m[1])] = clean(t['header'][0])
    return out

def u1d3_label_map():
    """Lingco label N -> origin item number (Unit 1 Drill 3)."""
    m = {}
    for t in TABLES:
        if t['unit'] == 1 and t['lesson'] == 'Drill 3':
            for row in t['rows']:
                label = None
                for cell in row:
                    lm = re.match(r'^(\d+)\.$', cell['text'].strip())
                    if lm:
                        label = int(lm[1]); continue
                    for a in cell['audio']:
                        w = BY_UUID[a]
                        m[label] = (parse_origin(w['origin'])[3], w)
    return m

# ------------------------------------------------------------------ record helpers
RECORDS = []
PROBLEMS = []

def base_record(rid, unit, lesson, item, purpose):
    r = collections.OrderedDict()
    r['id'] = rid; r['unit'] = unit; r['lesson'] = lesson; r['item'] = item; r['purpose'] = purpose
    return r

def fill_word(r, arabic, printed, translit, meaning, wt, real, conf, register, audio, targets, marks, notes,
              source, translit_printed=None, members=None, extra=None):
    r['arabic'] = arabic
    r['arabic_printed'] = printed
    r['arabic_bare'] = bare(arabic) if arabic else None
    va = None; spelling_note = None
    if arabic and printed:
        def _flat(x):  # drop punctuation, slashes, commas, spaces; order-insensitive word set
            return ''.join(sorted(re.sub(r'[/,،\s]+', ' ', PUNCT.sub('', clean(x))).split()))
        def _bflat(x):
            return ''.join(sorted(re.sub(r'[/,،\s]+', ' ', bare(x)).split()))
        if _flat(arabic) == _flat(printed):
            va = False
        elif _bflat(arabic) == _bflat(printed) or bare(arabic).replace(' ', '').replace('/', '') == bare(printed).replace(' ', '').replace('/', ''):
            va = True
        else:
            va = True; spelling_note = f'Spelling differs from the printed form {clean(printed)} (see notes).'
    r['vowels_added'] = va
    r['translit'] = translit
    if translit_printed and translit_printed != translit:
        r['translit_printed'] = translit_printed
    r['meaning'] = meaning
    r['word_type'] = wt
    r['real_word'] = real
    r['meaning_confidence'] = conf
    r['register'] = register
    r['audio'] = audio
    r['target_letters'] = targets
    if marks: r['target_marks'] = marks
    if arabic:
        lp, hz = letter_positions(arabic)
    else:
        lp, hz = {}, []
    r['letter_positions'] = lp
    if hz: r['hamza'] = hz
    if members: r['members'] = members
    n = [x for x in [notes, spelling_note] if x]
    r['notes'] = ' '.join(n)
    r['source'] = source
    if extra:
        r.update(extra)
    r['asr_checked'] = False
    r['asr_text'] = None
    RECORDS.append(r)
    return r

# ------------------------------------------------------------------ UNIT 1: letter videos
for nn, letter, name, tr, sound in D.LETTER_VIDEOS:
    ws = clips_for('LETTER', 1, 1, nn)
    assert len(ws) == 1, nn
    r = base_record(f'u1_le1_{nn:02d}', 1, 'Listening Exercise 1', nn, 'Arabic letters and sounds — hear each letter pronounced')
    au = [clip_entry(ws[0], 'formal')]
    dur = au[0]['dur'] or 0
    note = ('Video: close-up of a mouth pronouncing the letter. The exact utterance (letter name vs. sound) is not '
            'verified, and this file is not in the clip-transcription job (it is not in the vault or aud/).')
    if dur >= 12:
        note += f' This clip is {dur:.0f} s — longer than the others, so it probably includes extra sounds/contrasts.'
    fill_word(r, name, None, tr, f'the letter {tr.rstrip(chr(39))} ({letter}) — sound: {sound}', 'letter-name', True,
              'med', 'formal', au, [letter], [], note, 'standard letter name (own knowledge)',
              extra={'letter': letter})

# ------------------------------------------------------------------ UNIT 1: LE2 dialect phrases
for first, (label, register, country) in D.LE2_BLOCKS.items():
    for k in range(5):
        n = first + k
        ws = clips_for('LE', 1, 2, n)
        assert len(ws) == 1, n
        r = base_record(f'u1_le2_{n:02d}', 1, 'Listening Exercise 2', n,
                        'Dialect variation — the same phrases in Tunisian, Egyptian, Lebanese and Omani Arabic')
        meaning = D.LE2_PHRASES[k].format(country=country)
        reg_note = ('Lebanese speaker (Levantine family, close to shaami).' if register == 'shaami' else
                    f'{label} dialect — not a course variety (not formal, not shaami); listening-only.')
        fill_word(r, None, None, None, meaning, 'phrase', True, 'high', register,
                  [clip_entry(ws[0], label.lower())], [], [],
                  f'{label} column of the Lingco table (row: {D.LE2_PHRASES[k].format(country=country)}). '
                  f'{reg_note} Arabic wording is NOT printed anywhere — fill it from the clip transcription; do not invent it.',
                  'Lingco table (column = dialect, row = phrase)',
                  extra={'dialect_label': label, 'needs': 'arabic text from clip transcription'})

# ------------------------------------------------------------------ UNIT 1: Drill 3 countries
lab = u1d3_label_map()
for no, country, capital, tr, en in D.COUNTRIES:
    origin_no, w = lab[no]
    r = base_record(f'u1_d3_{no:02d}', 1, 'Drill 3', no, 'Where is Arabic spoken? — Arab countries and their capitals')
    fill_word(r, f'{country} — {capital}', None, tr, en, 'place', True, 'med', 'formal',
              [clip_entry(w, 'formal')], [], [],
              f'Item = the book/map number (= Lingco on-screen label {no}); the clip is AB3e_U1D3-{origin_no:02d}. '
              'Publisher files 01-18 run in English alphabetical order (Algeria 19, Egypt 20 appended), so the file '
              'number is NOT the item number here. Arabic names are the standard forms (own knowledge; the book '
              'prints only English) — the clip may use a fuller official name.',
              'book map legend (English) + own knowledge for the Arabic', extra={'publisher_file_no': origin_no})

# ------------------------------------------------------------------ LISTENING EXERCISES + DRILLS
for L in D.LESSONS:
    unit, code = L['unit'], L['code']
    kind = 'LE' if code.startswith('le') else 'D'
    lno = int(code[2:] if kind == 'LE' else code[1:])
    lingco_txt = lesson_items(L['lesson_file']) if L.get('lesson_file') else {}
    if L['printed'] == 'table':
        printed_map = table_items(unit, L['lesson'])
    elif L['printed'] == 'key':
        printed_map = {i + 1: clean(x) for i, x in enumerate(L['key_printed'])}
    else:
        printed_map = lingco_txt
    for (n, ar, tr, meaning, wt, real, conf, notes) in L['items']:
        ws = clips_for(kind, unit, lno, n)
        if len(ws) != 1:
            PROBLEMS.append(f'U{unit} {code} item {n}: {len(ws)} clips')
        rid = f'u{unit}_{code}_{n:02d}'
        r = base_record(rid, unit, L['lesson'], n, L['purpose'])
        printed = printed_map.get(n)
        if printed is None:
            PROBLEMS.append(f'{rid}: no printed form')
        src = {'lingco': 'Lingco lesson text (= book)', 'table': 'Lingco table (= book)',
               'key': 'Alif Baa answer key (drill prints no words)'}[L['printed']]
        members = None
        if wt == 'pair':
            ars = [x.strip() for x in ar.split('/')]
            trs = [x.strip() for x in tr.split('/')]
            members = []
            for a, t, m in zip(ars, trs, meaning):
                lp, hz = letter_positions(a)
                mm = collections.OrderedDict(arabic=a, arabic_bare=bare(a), translit=t, meaning=m, letter_positions=lp)
                if hz: mm['hamza'] = hz
                members.append(mm)
            meaning = ' / '.join(meaning)
        audio = [clip_entry(w, 'mixed (j / zh / Egyptian g)' if L.get('clip_note') else 'formal',
                            note=L.get('clip_note')) for w in ws]
        extra = {}
        if L['printed'] == 'key' and n in lingco_txt:
            extra['lingco_text'] = lingco_txt[n]
        if L.get('clip_note'):
            extra['clip_caution'] = L['clip_note']
        fill_word(r, ar, printed, tr, meaning, wt, real, conf, 'formal', audio, L['targets'], L['marks'], notes, src,
                  members=members, extra=extra)
        if printed and bare(ar).replace(' ', '') != bare(printed).replace(' ', '') and 'pelling' not in notes \
                and 'hamza' not in notes and 'تثبت' not in ar:
            PROBLEMS.append(f'{rid}: bare mismatch mine={bare(ar)} printed={bare(printed)}')

# ------------------------------------------------------------------ VOCABULARY
for unit, row, lesson, f, s, notes in D.VOCAB:
    fws = [w for w in clips_for('V', unit, 0, row) if parse_origin(w['origin'])[4] == 'formal']
    sws = [w for w in clips_for('V', unit, 0, row) if parse_origin(w['origin'])[4] == 'shaami']
    lex_id = (fws or sws)[0]['entry']
    purpose = {1: 'Greetings and introductions', 2: 'Meeting people', 3: 'Greetings and daily expressions',
               4: 'Introductions' if lesson.endswith('1') else 'More introductions (family, food, having)'}[unit]
    purpose = f'{lesson}: {purpose}'
    lex_note = f'Lingco vocab entry {lex_id}.'
    if f:
        if len(fws) != 1:
            PROBLEMS.append(f'vocab U{unit} r{row}: {len(fws)} formal clips')
        au = [clip_entry(w, 'formal') for w in fws]
        merged = s is not None and not s['sep']
        if merged:
            for w in sws:
                e = clip_entry(w, 'shaami', note=f"shaami clip — says: {s['tr']}" + (f". {s['note']}" if s.get('note') else ''))
                e['says'] = s['tr']
                au.append(e)
            au[0]['says'] = f['tr']
        rid = f'u{unit}_v{row:02d}'
        r = base_record(rid, unit, lesson, row, purpose)
        lexf = next((w for w in fws), None)
        printed = f['printed'] or (LEXF.get(fws[0]['file']) if fws else None)
        fill_word(r, f['ar'], printed, f['tr'], f['meaning'], f['wt'], True, f['conf'], 'formal', au, [], [],
                  ' '.join(x for x in [notes, lex_note] if x), 'Lingco vocab table (= book vocab chart)',
                  translit_printed=f.get('trp'))
    if s is not None and (s['sep'] or not f):
        if len(sws) != 1:
            PROBLEMS.append(f'vocab U{unit} r{row}: {len(sws)} shaami clips')
        au = [clip_entry(w, 'shaami') for w in sws]
        rid = f'u{unit}_v{row:02d}_shaami' if f else f'u{unit}_v{row:02d}'
        r = base_record(rid, unit, lesson, row, purpose)
        sprinted = s.get('printed') or (LEXF.get(sws[0]['file']) if sws else None)
        fill_word(r, s['ar'], sprinted, s['tr'], s['meaning'], s['wt'], True, s['conf'], 'shaami', au, [], [],
                  ' '.join(x for x in [s.get('note', ''), lex_note,
                                       'Shaami (Levantine) form — Dr. Khouri\'s dialect; allowed but flagged. Formal is what is graded.']
                           if x), 'Lingco vocab table (= book vocab chart)')

# ------------------------------------------------------------------ NUMERALS
for n, (far, ftr), (sar, str_, sep) in D.NUMERALS:
    fws = clips_for('NUM', 4, 0, n)
    fw = [w for w in fws if parse_origin(w['origin'])[4] == 'formal']
    sw = [w for w in fws if parse_origin(w['origin'])[4] == 'shaami']
    assert len(fw) == 1 and len(sw) == 1, n
    au = [clip_entry(fw[0], 'formal')]
    au[0]['says'] = ftr
    if not sep:
        e = clip_entry(sw[0], 'shaami', note=f'shaami clip — says: {str_}'); e['says'] = str_; au.append(e)
    r = base_record(f'u4_num{n:02d}', 4, 'Arabic Numerals', n, 'Numbers 0–10')
    digit = '٠١٢٣٤٥٦٧٨٩'
    ind = ''.join(digit[int(c)] for c in str(n))
    fill_word(r, far, None, ftr, f'{D.NUM_EN[n]} ({n}; Arabic-Indic numeral {ind})', 'number', True, 'high', 'formal', au, [], [],
              'Book numerals chart (p. 71): fully vowelled formal form.', 'Lingco numerals table (= book chart)',
              extra={'numeral': n, 'arabic_indic_numeral': ind})
    if sep:
        r = base_record(f'u4_num{n:02d}_shaami', 4, 'Arabic Numerals', n, 'Numbers 0–10')
        fill_word(r, sar, None, str_, f'{D.NUM_EN[n]} ({n}; Levantine)', 'number', True, 'high', 'shaami',
                  [clip_entry(sw[0], 'shaami')], [], [],
                  'Shaami (Levantine) form — Dr. Khouri\'s dialect; allowed but flagged. Formal is what is graded.',
                  'Lingco numerals table (= book chart)', extra={'numeral': n, 'arabic_indic_numeral': ind})

# ------------------------------------------------------------------ LONG CLIPS
for w in W:
    stem = os.path.splitext(w['file'])[0]
    if stem in D.LONG:
        rid, unit, lesson, kind, register, note = D.LONG[stem]
        r = base_record(rid, unit, lesson, None, kind)
        e = clip_entry(w, register)
        r['arabic'] = None; r['arabic_bare'] = None; r['translit'] = None
        r['meaning'] = note
        r['word_type'] = 'long_clip'
        r['clip_kind'] = kind
        r['real_word'] = None
        r['meaning_confidence'] = None
        r['register'] = register
        r['duration_s'] = e['dur']
        r['audio'] = [e]
        r['target_letters'] = []
        r['letter_positions'] = {}
        r['notes'] = ('Long clip — content deliberately NOT transcribed here; handle from the clip transcription '
                      '(ar + en passes). ' + ('Writing demos are narrated by Prof. El-Shinnawi (an Egyptian '
                      'speaker): check the narration before using any of its audio.' if kind == 'writing demo' else ''))
        r['source'] = 'Lingco lesson (video)'
        r['asr_checked'] = False
        r['asr_text'] = None
        RECORDS.append(r)

# ------------------------------------------------------------------ coverage / exclusions
EXCLUDED = []
for w in W:
    f = w['file']; stem = os.path.splitext(f)[0]
    k = parse_origin(w['origin'])
    if USED[f] == 1:
        continue
    if USED[f] > 1:
        PROBLEMS.append(f'{f} used {USED[f]} times')
        continue
    if w.get('dialect') == 'masri' or k[4] == 'masri':
        why = 'Egyptian (maSri) clip — excluded by rule'
        if k[0] == 'LE' and k[1] == 1:
            why = 'Unit 1 LE2 Egyptian row (exists only as Egyptian audio) — excluded by rule'
    elif stem in D.EXCLUDED_EGYPTIAN_SCENES:
        why = D.EXCLUDED_EGYPTIAN_SCENES[stem] + ' — excluded (Egyptian)'
    else:
        PROBLEMS.append(f'UNASSIGNED clip {f} {w["origin"]} {w["lesson"]}')
        continue
    EXCLUDED.append(collections.OrderedDict(file=f, origin=w['origin'], lesson=w['lesson'], entry=w['entry'],
                                            reason=why, lingco_uuid=w['uuid']))

# ------------------------------------------------------------------ cross references
groups = collections.defaultdict(list)
for r in RECORDS:
    if r.get('arabic_bare') and r['word_type'] not in ('long_clip',):
        groups[(r['arabic_bare'].replace(' ', ''), r['register'])].append(r['id'])
for r in RECORDS:
    if r.get('arabic_bare') and r['word_type'] != 'long_clip':
        others = [x for x in groups[(r['arabic_bare'].replace(' ', ''), r['register'])] if x != r['id']]
        r['also_in'] = others

# ------------------------------------------------------------------ ASR merge
def best_window(e, a):
    if not e or not a: return 0.0
    best = 0.0
    for L in {len(e) - 1, len(e), len(e) + 1}:
        if L <= 0: continue
        for i in range(0, max(1, len(a) - L + 1)):
            best = max(best, difflib.SequenceMatcher(None, e, a[i:i + L]).ratio())
    return best

HALLUCINATION = re.compile('ترجمة|نانسي|قنقر|اشتركوا|القناة|للمشاهدة|موسيقى|المترجم|سبحان الله وبحمده')

def agree(expected, heard):
    if HALLUCINATION.search(heard or ''):
        return 'asr_unusable', 0.0
    e = an(expected).replace(' ', ''); a = an(heard).replace(' ', '')
    if not e or not a: return None, 0.0
    ratio = difflib.SequenceMatcher(None, e, a).ratio()
    win = best_window(e, a)
    score = max(ratio, win)
    if e in a or score >= 0.75: return True, score
    if score >= 0.5: return 'partial', score
    return False, score

ASR_DISAGREE = []
if ASR is not None:
    for r in RECORDS:
        texts = []; verdicts = []; have_all = True
        for e in r['audio']:
            a = ASR.get(e['asr_key'])
            if not a:
                have_all = False; continue
            ar = (a.get('ar') or '').strip()
            en = (a.get('en') or '').strip()
            e['asr_ar'] = ar
            if en: e['asr_en'] = en
            texts.append((e['dialect'], ar))
            if r['word_type'] == 'long_clip' or not r.get('arabic'):
                continue
            if r.get('members'):
                vs = [agree(m['arabic'], ar) for m in r['members']]
                if any(x[0] == 'asr_unusable' for x in vs):
                    v, sc = 'asr_unusable', 0.0
                else:
                    v = True if all(x[0] is True for x in vs) else (False if all(x[0] is False for x in vs) else 'partial')
                    sc = min(x[1] for x in vs)
            else:
                exp = r['arabic']
                v, sc = agree(exp, ar)
            e['asr_agrees'] = v; e['asr_score'] = round(sc, 2)
            verdicts.append(v)
        if texts:
            r['asr_checked'] = have_all
            r['asr_text'] = texts[0][1] if len(texts) == 1 else ' | '.join(f'{d}: {t}' for d, t in texts)
            ens = [e.get('asr_en') for e in r['audio'] if e.get('asr_en')]
            if ens: r['asr_en'] = ens[0] if len(ens) == 1 else ' | '.join(ens)
            if r.get('needs'):
                r['arabic_from_asr'] = texts[0][1]  # unverified machine transcription — review before use
        if verdicts:
            usable = [v for v in verdicts if v != 'asr_unusable']
            if not usable:
                r['asr_agrees'] = 'asr_unusable'
            else:
                r['asr_agrees'] = (True if all(v is True for v in usable) else
                                   (False if any(v is False for v in usable) else 'partial'))
            if r['asr_agrees'] is False:
                ASR_DISAGREE.append(r['id'])

# ------------------------------------------------------------------ write
ORDER = {'LE': 0}
def sort_key(r):
    lesson = r['lesson']
    m = re.match(r'(Listening Exercise|Drill) (\d+)', lesson)
    lk = (0 if lesson.startswith('Listening') else 1, int(m[2])) if m else (2, lesson)
    return (r['unit'], lk[0], lk[1] if isinstance(lk[1], int) else 0, str(lk[1]), r['item'] if isinstance(r['item'], int) else 999, r['id'])

RECORDS.sort(key=sort_key)
json.dump(RECORDS, open(f'{OUT}/lingco_words{OUT_SUFFIX}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(EXCLUDED, open(f'{OUT}/lingco_excluded_clips{OUT_SUFFIX}.json', 'w'), ensure_ascii=False, indent=1)

# counts
cnt_unit_type = collections.Counter((r['unit'], r['word_type']) for r in RECORDS)
real = sum(1 for r in RECORDS if r.get('real_word') is True)
low = [r['id'] for r in RECORDS if r.get('meaning_confidence') == 'low']
stats = dict(records=len(RECORDS), real_words=real, low_confidence=len(low), excluded_clips=len(EXCLUDED),
             asr_available=ASR is not None, asr_disagreements=len(ASR_DISAGREE),
             by_unit={u: sum(1 for r in RECORDS if r['unit'] == u) for u in (1, 2, 3, 4)},
             by_type=dict(collections.Counter(r['word_type'] for r in RECORDS)),
             by_unit_type={f'U{u}': dict(collections.Counter(r['word_type'] for r in RECORDS if r['unit'] == u)) for u in (1, 2, 3, 4)},
             clips_referenced=sum(1 for v in USED.values() if v), problems=PROBLEMS, asr_disagree_ids=ASR_DISAGREE,
             low_confidence_ids=low)
json.dump(stats, open(f'{OUT}/lingco_words_stats{OUT_SUFFIX}.json', 'w'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ markdown
def md_esc(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ')

lines = []
A = lines.append
A('# Lingco (Alif Baa 3e) Units 1-4 — every word with publisher audio')
A('')
A(f'Built {datetime.date.today().isoformat()} by `build_lingco_words.py` (re-run it after `clipcheck/clips_asr.json` lands to fill the ASR columns). '
  f'Machine-readable twin: `lingco_words.json` ({len(RECORDS)} records). Excluded clips: `lingco_excluded_clips.json` ({len(EXCLUDED)}).')
A('')
A('## Counts')
A('')
types = sorted(stats['by_type'])
A('| Unit | ' + ' | '.join(types) + ' | total |')
A('|---|' + '---|' * (len(types) + 1))
for u in (1, 2, 3, 4):
    A(f'| {u} | ' + ' | '.join(str(cnt_unit_type.get((u, t), 0) or '') for t in types) + f' | {stats["by_unit"][u]} |')
A(f'| all | ' + ' | '.join(str(stats['by_type'][t]) for t in types) + f' | {len(RECORDS)} |')
A('')
A(f'- Real words: **{real}**; not-real (syllable/nonword drill strings): {sum(1 for r in RECORDS if r.get("real_word") is False)}; '
  f'long clips (no word content): {stats["by_type"].get("long_clip", 0)}; dialect phrases awaiting transcription: '
  f'{sum(1 for r in RECORDS if r.get("needs"))}.')
A(f'- Low-confidence meanings: **{len(low)}** — {", ".join(low)}.')
A(f'- ASR check: {"available" if ASR is not None else "NOT YET AVAILABLE (clips_asr.json missing) — every record has asr_checked:false"}; '
  f'disagreements: {len(ASR_DISAGREE)}{(" — " + ", ".join(ASR_DISAGREE)) if ASR_DISAGREE else ""}.')
if PROBLEMS:
    A(f'- Build problems: {"; ".join(PROBLEMS)}')
A('')
A('## How to read this')
A('')
A('- **One record per exercise item** (the same word in two exercises = two records; `also_in` cross-links them). '
  'Vocabulary: one record per row for the formal form; the shaami clip rides along as an alternate when it is the same word '
  '(`audio[].dialect = "shaami"`, `says` = what that clip says), and gets its **own record (`register: shaami`)** when the '
  'Levantine form is a different word or has a documented different pronunciation.')
A('- **Item numbers = publisher file numbers** (`AB3e_U4LE5-03` = item 3) everywhere EXCEPT Unit 1 Drill 3 (countries), '
  'whose files are numbered alphabetically; there the item is the book/map number and the file is recorded separately.')
A('- **Arabic**: `arabic` is the printed form with any missing short vowels / sukuun / shadda filled in (`vowels_added: true` when I added or corrected marks; '
  '`arabic_printed` is exactly what Lingco/the book/the key prints). Dictation and letter-connection drills print no words: their Arabic comes from the Alif Baa answer key.')
A('- **letter_positions**: for each Unit 1-4 letter in the word, the glyph form(s) it takes there, in order of occurrence — a list, because a letter can occur twice '
  '(حُدود → د: final, isolated). Hamza is keyed `ء` by word position (initial/medial/final) with seat details in `hamza` (seat alif/waaw/yaa/line). Plain alif `ا` only; alif carrying hamza (أ إ آ) is counted under `ء`.')
A('- **word_type** adds to the requested list: pronoun, preposition, particle, interrogative, demonstrative, adverb, suffix, pair (a clip that says a contrast pair), long_clip.')
A('- **No Egyptian**: every maSri clip, the Egyptian scene videos, and Unit 1 LE2\'s Egyptian column are excluded (listed in `lingco_excluded_clips.json`). '
  'Unit 3 LE1 clips say each word in three ج pronunciations including the Egyptian hard g — flagged `clip_caution`.')
A('')

cur = None
for r in RECORDS:
    key = (r['unit'], r['lesson'])
    if key != cur:
        if cur is not None:
            A('')
        cur = key
        A(f'## Unit {r["unit"]} — {r["lesson"]}' + (f'  ·  _{r["purpose"]}_' if r['word_type'] != 'long_clip' else ''))
        A('')
        A('| id | Arabic | translit | meaning | type | conf | clip(s) | flags |')
        A('|---|---|---|---|---|---|---|---|')
    flags = []
    if r.get('register') not in ('formal', None): flags.append(f'**{r["register"]}**')
    if r.get('real_word') is False: flags.append('not a real word')
    if r.get('vowels_added'): flags.append('vowels added')
    if r.get('clip_caution'): flags.append('clip has Egyptian g variant')
    if r.get('needs'): flags.append('Arabic pending transcription')
    if r.get('asr_agrees') is False: flags.append('**ASR DISAGREES**')
    elif r.get('asr_agrees') == 'partial': flags.append('ASR partial')
    if r['word_type'] == 'long_clip': flags.append(f'{r.get("duration_s") or 0:.0f} s {r.get("clip_kind")}')
    elif any((e.get('dur') or 0) >= 12 for e in r['audio']): flags.append('long clip (>12 s): content unverified')
    if r['word_type'] == 'letter-name' and r['id'].startswith('u1_le1'): flags.append('not in ASR job')
    clips = '<br>'.join(f'{e["file"]} ({e["dialect"]}{", " + str(e["dur"]) + "s" if e.get("dur") else ""})' for e in r['audio'])
    ar = r.get('arabic') or '—'
    A(f'| {r["id"]} | {md_esc(ar)} | {md_esc(r.get("translit") or "—")} | {md_esc(r.get("meaning"))} | {r["word_type"]} | '
      f'{r.get("meaning_confidence") or ""} | {md_esc(clips)} | {md_esc("; ".join(flags))} |')
    if r.get('notes') and (r.get('meaning_confidence') == 'low' or r.get('real_word') is False or r['word_type'] in ('long_clip', 'place', 'letter-name')
                           or 'unverified' in r.get('notes', '') or r['id'].startswith('u1_le2')):
        pass
A('')
A('## Notes on individual items (low confidence / non-words / special cases)')
A('')
for r in RECORDS:
    if r['word_type'] == 'long_clip':
        continue
    if r.get('meaning_confidence') == 'low' or r.get('real_word') is False or r.get('clip_caution') or \
            ('unverified' in (r.get('notes') or '')) or ('typo' in (r.get('notes') or '')) or ('Spelling differs' in (r.get('notes') or '')):
        bits = [f'"{r.get("meaning")}"', r.get('notes') or '', r.get('clip_caution') or '']
        A(f'- `{r["id"]}` {r.get("arabic") or ""} — ' + md_esc(' — '.join(b for b in bits if b)))
A('')
A('## Excluded clips')
A('')
ex_c = collections.Counter(e['reason'].split(' — ')[0] if 'Scene' not in e['reason'] else 'Egyptian scene video' for e in EXCLUDED)
for k, v in ex_c.items():
    A(f'- {v} × {k}')
for e in EXCLUDED:
    if 'Scene' in e['reason']:
        A(f'  - {e["file"]}: {e["reason"]}')
A('')
open(f'{OUT}/lingco_words{OUT_SUFFIX}.md', 'w').write('\n'.join(lines))

print(json.dumps({k: v for k, v in stats.items() if k not in ('low_confidence_ids',)}, ensure_ascii=False, indent=1))
