#!/usr/bin/env python3
"""
sources.py — the source registry: what Claude can point at, and where its cards go.

This is the module that made the pipeline universal. Everything that used to be
hard-coded to the EMT textbook (which PDF, which highlight colors, which page->chapter
map, which Anki deck, which tags, which subject profile) now lives per-source in
`reference/sources.json`, and every script asks this module instead of assuming.

Nothing about CARD CRAFT lives here. The rules, the adversarial editor, the gate, and
the regression suite are subject-independent and stay exactly as they were.

Used as a library by extract_highlights.py / anki_write.py / check_cards.py /
render_page.py / add_source.py, and directly as a CLI:

    python3 scripts/sources.py list                 # every registered source
    python3 scripts/sources.py show emt             # one source, fully resolved
    python3 scripts/sources.py segments emt         # its segment map
    python3 scripts/sources.py deck emt 3           # the deck names for a segment
"""
import json, os, re, shutil, sqlite3, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REGISTRY = os.path.join(SKILL, "reference", "sources.json")
ZOTERO_DB = os.path.expanduser("~/Zotero/zotero.sqlite")
ZOTERO_STORAGE = os.path.expanduser("~/Zotero/storage")


# --------------------------------------------------------------------------- registry

def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def save_registry(reg):
    with open(REGISTRY, "w") as f:
        json.dump(reg, f, indent=1, ensure_ascii=False)
        f.write("\n")


def list_sources():
    reg = load_registry()
    return {k: v.get("label", k) for k, v in reg["sources"].items()}


def get_source(source_id):
    """A source entry with registry defaults merged in. Fails loudly with the list of
    valid ids, so a typo never silently reads the wrong book."""
    reg = load_registry()
    src = reg["sources"].get(source_id)
    if not src:
        known = ", ".join(sorted(reg["sources"])) or "(none registered yet)"
        sys.exit(f"ERROR: unknown source '{source_id}'.\n"
                 f"Registered sources: {known}\n"
                 f"Add one with:  python3 scripts/add_source.py --search \"<title words>\"")
    merged = dict(reg.get("defaults", {}))
    merged.update(src)
    merged["id"] = source_id
    return merged


# ------------------------------------------------------------------------ zotero glue

def _open_db():
    """Read-only against Zotero, always: copy the live DB and open the copy immutable.
    Never touch the original — Zotero may be running and holding locks."""
    tmp = tempfile.mkdtemp(prefix="z2a_")
    copy = os.path.join(tmp, "z.sqlite")
    shutil.copy2(ZOTERO_DB, copy)
    con = sqlite3.connect(f"file:{copy}?immutable=1", uri=True)
    return con, tmp


def resolve_attachment(source):
    """(itemID, absolute PDF path) for a source's Zotero attachment.

    Resolution order: the stable item KEY first (unambiguous), then a path substring
    as a fallback. The key is why this is safe to generalize — the old code matched
    on a filename fragment, which once returned the wrong item entirely (three
    'sick and injured' files, two of them epubs with zero annotations)."""
    con, tmp = _open_db()
    try:
        cur = con.cursor()
        row = None
        key = source.get("attachment_key")
        if key:
            cur.execute("""SELECT ia.itemID, ia.path FROM itemAttachments ia
                           JOIN items i ON i.itemID = ia.itemID WHERE i.key = ?""", (key,))
            row = cur.fetchone()
        if not row and source.get("path_match"):
            cur.execute("SELECT itemID, path FROM itemAttachments WHERE path LIKE ?",
                        (f"%{source['path_match']}%",))
            row = cur.fetchone()
        if not row:
            sys.exit(f"ERROR: could not resolve the Zotero attachment for source "
                     f"'{source['id']}' (key={key!r}, path_match={source.get('path_match')!r}).\n"
                     f"Check the key in reference/sources.json against Zotero "
                     f"(right-click the attachment -> the key is in its item URI).")
        item_id, path = row
        # Zotero stores 'storage:<filename>' relative to ~/Zotero/storage/<KEY>/
        if path and path.startswith("storage:") and key:
            pdf = os.path.join(ZOTERO_STORAGE, key, path[len("storage:"):])
        elif path and path.startswith("storage:"):
            cur.execute("SELECT key FROM items WHERE itemID=?", (item_id,))
            k = cur.fetchone()[0]
            pdf = os.path.join(ZOTERO_STORAGE, k, path[len("storage:"):])
        else:
            pdf = path or ""
        return item_id, pdf
    finally:
        con.close()
        shutil.rmtree(tmp, ignore_errors=True)


def colors(source):
    """The highlight colors that mean 'make me a card' for THIS source.

    Per-source because Parker's convention is not uniform across his library: the EMT
    book is yellow-only, while the organic chemistry text uses a three-color scheme
    (#facd5a / blue / pink) carried over from another annotator."""
    return list(source.get("colors", ["#ffd400", "#facd5a"]))


# ------------------------------------------------------------------------- segmenting

def load_segments(source):
    """The source's segment map (chapters/units/lessons), or None for a flat source
    like a single lecture PDF, which is always addressed whole or by page range."""
    rel = source.get("segments")
    if not rel:
        return None
    path = rel if os.path.isabs(rel) else os.path.join(SKILL, rel)
    if not os.path.exists(path):
        sys.exit(f"ERROR: segment map not found for source '{source['id']}': {path}")
    with open(path) as f:
        return json.load(f)


def segment_range(source, n):
    """(start_page, end_page, name) for segment n, in physical PDF pages."""
    smap = load_segments(source)
    if not smap:
        sys.exit(f"ERROR: source '{source['id']}' has no segment map, so --segment "
                 f"does not apply. Use --pages A-B, or --all for the whole document.")
    for s in smap["segments"]:
        if s["n"] == n:
            return s["start"], s["end"], s.get("name", "")
    have = ", ".join(str(s["n"]) for s in smap["segments"])
    sys.exit(f"ERROR: source '{source['id']}' has no segment {n}. Available: {have}")


def segment_of_page(source, page_label):
    """(n, name) for the segment containing a page, or (None, None)."""
    smap = load_segments(source)
    if not smap:
        return None, None
    try:
        p = int(re.sub(r"[^0-9]", "", str(page_label)))
    except (TypeError, ValueError):
        return None, None
    for s in smap["segments"]:
        if s["start"] <= p <= s["end"]:
            return s["n"], s.get("name", "")
    return None, None


def segment_noun(source):
    smap = load_segments(source)
    if smap and smap.get("noun"):
        return smap["noun"]
    return source.get("segment_noun", "Section")


# ----------------------------------------------------------------------- deck routing

def _fill(template, source, segment):
    return (template
            .replace("{root}", source.get("deck_root", "all"))
            .replace("{segment}", "" if segment is None else str(segment))
            .replace("{segment_noun}", segment_noun(source))
            .replace("{id}", source.get("id", "")))


def deck_names(source, segment=None):
    """(staging_deck, promote_deck) for this source/segment.

    Every source keeps the two-deck promotion gate: the pipeline only ever writes to
    the staging deck, and Parker promotes keepers into the sibling himself. The NAMES
    are per-source so a lecture doesn't inherit book-shaped naming."""
    staging = _fill(source.get("staging", "{root}::claude review"), source, segment)
    promote = _fill(source.get("promote", "{root}::Keepers"), source, segment)
    return staging, promote


def audit_deck(source, segment=None):
    """The deck to sweep when auditing what Parker is ACTUALLY studying.

    That has to cover both the staging deck and the deck he promotes into, so it is the
    longest shared '::' prefix of the two — for EMT that's 'all::EMT::Chapter 3', which
    Anki matches inclusive of its subdecks. Falls back to the source root."""
    staging, promote = deck_names(source, segment)
    a, b = staging.split("::"), promote.split("::")
    shared = []
    for x, y in zip(a, b):
        if x != y:
            break
        shared.append(x)
    return "::".join(shared) or source.get("deck_root", "all")


def tags_for(source, segment=None):
    return [_fill(t, source, segment) for t in source.get("tags", [])]


def model(source):
    return source.get("model", "AnKing Cloze")


def profile_path(source):
    """The subject profile that layers emphasis on top of the universal card rules."""
    name = source.get("profile", "default")
    path = os.path.join(SKILL, "reference", "profiles", f"{name}.md")
    if not os.path.exists(path):
        path = os.path.join(SKILL, "reference", "profiles", "default.md")
    return path


# ------------------------------------------------------------------------------- cli

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = args[0]

    if cmd == "list":
        reg = load_registry()
        srcs = reg["sources"]
        if not srcs:
            print("No sources registered yet. Add one with scripts/add_source.py")
            return
        print(f"{len(srcs)} registered source(s):\n")
        for sid in sorted(srcs):
            s = get_source(sid)
            smap = load_segments(s)
            seg = f"{len(smap['segments'])} {segment_noun(s).lower()}s" if smap else "flat (no segments)"
            print(f"  {sid:<16} {s.get('label','')}")
            print(f"  {'':<16} {seg} · profile={s.get('profile')} · {s.get('deck_root')}")
        return

    if cmd == "show":
        s = get_source(args[1])
        item_id, pdf = resolve_attachment(s)
        staging, promote = deck_names(s, 1 if load_segments(s) else None)
        print(json.dumps({
            "id": s["id"], "label": s.get("label"), "kind": s.get("kind"),
            "zotero_item_id": item_id, "pdf": pdf, "pdf_exists": os.path.exists(pdf),
            "colors": colors(s), "profile": os.path.basename(profile_path(s)),
            "segment_noun": segment_noun(s),
            "segments": (len(load_segments(s)["segments"]) if load_segments(s) else None),
            "staging_example": staging, "promote_example": promote,
            "tags_example": tags_for(s, 1 if load_segments(s) else None),
        }, indent=2))
        return

    if cmd == "segments":
        s = get_source(args[1])
        smap = load_segments(s)
        if not smap:
            print(f"{s['id']}: flat source (no segment map)")
            return
        for seg in smap["segments"]:
            print(f"  {segment_noun(s)} {seg['n']:>3}  p{seg['start']}-{seg['end']}  {seg.get('name','')}")
        return

    if cmd == "deck":
        s = get_source(args[1])
        n = int(args[2]) if len(args) > 2 else None
        staging, promote = deck_names(s, n)
        print(f"staging: {staging}\npromote: {promote}\ntags:    {tags_for(s, n)}")
        return

    sys.exit(f"unknown command '{cmd}' — try: list | show <id> | segments <id> | deck <id> [n]")


if __name__ == "__main__":
    main()
