"""card-rules #36 — class-context detector (2026-10-02).
A card must stand alone in 10 years: no professor names, no lecture/slide/presentation, no "the book"/unit/
chapter/page/figure refs, no lab/test/quiz logistics, no class dates, no cross-card references.
scan_text(raw, deck="") -> [(term, match, context)]. Terms in HARD_TERMS block the write; the rest warn.
Shared with course-to-anki (work/universal-context-2026-10-02/terms.py is the same file)."""
import re, html
TERMS = {
 "howell": r"\bhowell'?s?\b", "blais": r"\bblais'?s?\b", "khouri": r"\bkhouri'?s?\b", "isaacs": r"\bisaacs'?s?\b",
 "drambi": r"\bdrambi'?s?\b", "kk": r"\b(dr\.? ?kk|kk'?s)\b", "ryder": r"\bryder'?s?\b", "sydney": r"\bsydney\b",
 "nathan": r"\bnathan'?s?\b", "dr.": r"\bdr\.\s?[A-Z]", "prof": r"\bprof\.|\bprofessor'?s?\b", "instructor": r"\binstructor'?s?\b",
 "teacher": r"\bteacher'?s?\b", "the TA": r"\bthe ta\b",
 "she-says": r"\b(she|he)\s+(said|says|used|uses|calls?|called|emphasi[sz]e[sd]?|stress(es|ed)|mention(s|ed)|want(s|ed)|likes?|wrote|writes|told|tells|teaches|taught|asked|asks|pronounc\w+|expects?|drew|draws|put|puts|had|has us|gave|gives|showed|shows|repeated|read|reads|drill(s|ed)|note[sd]?|point(s|ed) out|describ\w+|explain\w+|defin\w+|skips?|skipped|spells?|confirmed|added|pulled|built|walked|quotes?|stopped|insists?|prefers?|accepts?|marks?|counts?|lists?|labels?|names?|lumps?|splits?|treats?|follows?|ignores?|covers?|flags?|frames?)\b",
 "his/her-X": r"\b(his|her)\s+(own\s+)?(lecture|slides?|outline|list|check-?word|phrase|wording|version|scheme|notes?|class|test|exam|quiz|handout|lab|voice|pronunciation|way|rule|definition|example|drawing|diagram|photo|picture|table|chart|words|answer|key|emphasis|style|students|deck|plates?|figures?|bullet|homework|trick|dialect|course|material|question|usage|term|label|point|note|gait|gloss|recording|audio|s\d+)\b",
 "lecture": r"\blectures?\b", "slide": r"\bslides?\b(?!\s*(of|under|on)\s+(the\s+)?(microscope|tissue|glass))|\bs\d{1,2}\b", "presentation": r"\b(the|his|her|this)\s+presentations?\b|\bpowerpoint|\bppt",
 "in-class": r"\b(in|the|this|our|during|after|before|whole|entire|her|his)\s+class\b|\bclass(mate|room|work)s?\b|\bat the board\b|\bon the board\b|\bthe board\b|\bin lab\b|\bin lecture\b",
 "course": r"\b(this|the|our)\s+course\b|\bsyllabus\b|\bcanvas\b|\btop ?hat\b|\blingco\b|\bthe deck\b|\bthis deck\b|\bsibling card\b|\bsister card\b|\bthe next card\b|\banother card\b|\bother cards?\b",
 "homework": r"\bhomework\b|\bhw\b|\bhandouts?\b|\bworksheets?\b",
 "test/exam": r"\b(on|for|in)\s+(the|a|this|his|her|our|next)\s+(test|exam|quiz|practical|midterm|final)s?\b|\b(test|exam|quiz)\s+(question|answer|day|prep|material|stem)s?\b|\btestable\b|\bexam\s*[1-5]\b|\btest\s*[1-5]\b|\bquiz\s*\d\b|\bpractical\s*[12]\b|\bthe\s+practical\b|\bmidterm\b|\bhigh[- ]yield\b|\bnot (be )?asked\b|\bwon'?t (be )?ask\w*\b|\bwill (be )?ask\w*\b|\bexpect it\b|\bknow (this|these|them|it) for\b|\bextra (card|practice)\b|\bthis card is extra\b|\bthese cards are extra\b",
 "required": r"\bcalled (this|it|these|that) required\b|\bnot required\b|\brequired (for|on) the (test|exam|quiz|practical)\b",
 "course-code": r"\b(biol|arab|phys|chem|psyc|theo|engl|math)\s?\d{3}\b",
 "the-lab": r"\b(the|our|this)\s+lab('s)?\b(?!\s*(coat|value|result|test|finding|work-?up|report))|\blab\s+(station|scheme|list|manual|practical|photo|specimen|slide|notes|tables?|instructor|bone list|audio)s?\b|\bstation\s*\d|\bthe station\b|\bstation model\b",
 "the-book": r"\b(the|this|that|our|his|her)\s+(text)?book('s)?\b|\btextbooks?\b|\bthe\s+(reading|chapter|unit|section|lesson|module|page|figure|chart|table|diagram|map|dialogue|dialog|recording|drill|exercise|passage|prose|caption|answer key|outline|notes|manual|manual's|practice page|blue page|appendix)('s)?\b|\bthe book\b",
 "book-title": r"\balif ?baa('s)?\b|\bmoore('s)?\b|\bgrant'?s\b|\bseeley'?s?\b|\bmarieb\b|\bnetter'?s?\b|\brohen'?s?\b|\bclinically oriented anatomy\b|\bkaplan\b|\bemt textbook\b|\borange book\b|\baaos\b|\bjones\s*&\s*bartlett\b|\blippincott\b|\bal-kitaab\b|\bhaps\b",
 "page/fig-ref": r"\b(p|pp|pg)\.\s?\d+\b|\b(p|pp|pg)\s\d+\b|\bpages?\s+\d+|\bfig(ure|\.)?\s?\d+[\.-]?\d*\b|\btable\s+\d+[\.-]?\d*\b|\bplate\s+\d+\b|\bblue[- ]pages?\b|\bQ\d{1,2}\b|\bquestion\s+\d+\b|\b#\d+\b",
 "unit/chapter": r"\b(unit|chapter|ch\.|lesson|module|week|wk|section|part|drill|exercise)\s?\d+\b|\bW0\d\b|\bL\d\d\b|\blecture\s?\d+\b|\bunits?\s+\d",
 "scheme/list": r"\b(scheme|on the list|list of ten|the ten|the list|the roster)\b",
 "we/our/you": r"\b(we|we'll|we've|our|us)\b(?!\s*=)|\byou'?ll\s+(be asked|need to know|get asked|meet)\b|\bremember for\b|\bbe able to\b|\bfor the (test|exam|quiz)\b|\byou asked\b|\byou were\b",
 "mcq-letters": r"\bletter\s+[A-H]\b|\boption\s+[a-eA-E]\b|\bchoice\s+[a-eA-E]\b|\banswer\s+[a-eA-E]\b",
 "according-to": r"\bper\s+(the|his|her|howell|blais|khouri|isaacs|lecture|class|slides?)\b|\bas (taught|given|stated|defined|presented|drawn|shown|used|written|said|phrased)\s+(in|on|by|at)\b|\bin (his|her|the) (words|phrasing|terms|version)\b|\bcites?\b|\bcited\b|\bquot(es|ed|ing)\b",
 "dates": r"\b\d{1,2}/\d{1,2}\b|\b\d{1,2} (aug|sep|sept|oct|nov|dec|jan|feb|mar|apr|may|jun|jul)\b|\b(aug|sep|sept|oct|nov|dec|jan|feb|mar|apr|may|jun|jul)\.? \d{1,2}\b|\bspring 20\d\d\b|\bfall 20\d\d\b",
 "ryder-screenshot": r"screenshot",
}
RX = {k: re.compile(v, re.I) for k, v in TERMS.items()}
# benign patterns to ignore (false positives seen in calibration)
IGNORE = [
 re.compile(r"WHERE YOU'LL SEE IT", re.I),
 re.compile(r"\bU[1-6]\b(?=.*snRN)|\bU[1-6] snRN|snRNAs? U\d", re.I),
 re.compile(r"\bin class (gastropoda|bivalvia|cephalopoda|mammalia|aves|reptilia|amphibia|insecta|arachnida|\w+idae|\w+poda)\b", re.I),
 re.compile(r"\bcayn\b|\bcarabi\b"),
]
def strip(s):
    s = re.sub(r"\[sound:[^\]]*\]", " ", s); s = re.sub(r"<img[^>]*>", " [img] ", s)
    s = re.sub(r"<br\s*/?>", " / ", s); s = re.sub(r"<[^>]+>", " ", s); return html.unescape(s)
def scan_text(raw, deck=""):
    txt = strip(raw)
    out = []
    for k, rx in RX.items():
        for m in rx.finditer(txt):
            a, b = max(0, m.start()-50), min(len(txt), m.end()+50)
            ctx = txt[a:b]
            if any(ig.search(ctx) for ig in IGNORE): continue
            if k == "unit/chapter" and re.fullmatch(r"U\d", m.group(0)) and "ARAB" not in deck: continue
            if k == "homework" and "ARAB" in deck and re.search(r"waajib|waZiif|homework\}\}|homework assignments|\(homework\)|\(my homework\)", txt, re.I): continue
            if k == "prof" and "ARAB" in deck and re.search(r"ustaadh|brofesoor", txt, re.I) and not re.search(r"khouri", ctx, re.I): continue
            if k == "teacher" and "ARAB" in deck and re.search(r"ustaadh", txt, re.I) and not re.search(r"her class|the class|khouri", ctx, re.I): continue
            out.append((k, m.group(0), ctx.replace("\n", " ")))
    return out

HARD_TERMS = {"howell","blais","khouri","isaacs","drambi","kk","ryder","sydney","nathan","lecture","slide",
              "presentation","in-class","course","homework","course-code","unit/chapter","page/fig-ref",
              "book-title","ryder-screenshot","the-lab","test/exam","according-to","scheme/list"}
