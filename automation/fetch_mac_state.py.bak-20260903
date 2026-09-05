#!/usr/bin/env python3
"""
fetch_mac_state.py — bring the HP's view of Zotero up to the minute, from the Mac.

The HP's own Zotero stopped syncing on 2026-08-02 and is never going to be trusted
again; running a second sync client would just create a second fork to worry about
(see what happened to Anki). Instead the Mac's library IS the truth and the HP takes
a nightly read-only mirror of it:

    1. zotero.sqlite  — snapshotted on the Mac with sqlite3's .backup (transaction-safe
       even if Zotero is open mid-write), then copied over and swapped in atomically.
    2. storage/       — rsync'd (delta after the first pass), because the pipeline needs
       the actual PDFs: pdftotext grounding, render_page, figure crops.

The HP's Zotero APP must never run against this mirror — it would see a database it
didn't write and could "repair" it. Guard: abort if a zotero process exists on the HP.

The pre-mirror stale database is preserved once as zotero.sqlite.stale-fork-20260802,
in case anything from the fork era is ever needed.

CLI:
    python3 fetch_mac_state.py            # full fetch, prints a report
    python3 fetch_mac_state.py --db-only  # skip the storage rsync (fast)
"""
import json, os, sqlite3, subprocess, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def _cfg():
    with open(os.path.join(HERE, "config.json")) as f:
        cfg = json.load(f)
    local = os.path.join(cfg["state_dir"], "config.local.json")
    if os.path.exists(local):
        with open(local) as f:
            cfg.update(json.load(f))
    return cfg


def _run(cmd, timeout=900):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL)


def fetch(cfg, db_only=False):
    """-> report dict. Raises RuntimeError with a clear message on any guard failure."""
    mac = cfg["mac_host"]
    hp_dir = cfg["hp_zotero_dir"]
    report = {"started": datetime.now().astimezone().isoformat(timespec="seconds")}

    # Guard: the mirror must never race a live Zotero on this machine.
    p = _run(["pgrep", "-x", "zotero"])
    if p.returncode == 0:
        raise RuntimeError("a zotero process is RUNNING on this machine — the mirror "
                           "would fight it over the database. Close it (the HP's Zotero "
                           "is retired; the Mac's library is the truth).")

    # Guard: the Mac is reachable.
    p = _run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", mac, "echo ok"])
    if p.returncode != 0:
        raise RuntimeError(f"cannot reach the Mac over ssh ({mac}): "
                           f"{(p.stderr or p.stdout).strip()[:200]}")

    # 1 — snapshot on the Mac, then pull it. NOT sqlite .backup: Zotero holds an
    # exclusive lock on its database for as long as the app is open (found the hard
    # way, first dry run, 2026-08-26 — "database is locked" with Parker mid-chapter).
    # A plain copy is what the extractor itself has always done against a live
    # Zotero; at night the app is idle, so the file on disk is a committed state.
    # The quick_check-and-retry loop covers the rare mid-write copy.
    remote_tmp = "/tmp/night-shift-zotero.sqlite"
    p = _run(["ssh", mac,
              f"for i in 1 2 3; do "
              f"  cp ~/{cfg['mac_zotero_dir']}/zotero.sqlite {remote_tmp}; "
              f"  ok=$(/usr/bin/sqlite3 {remote_tmp} 'PRAGMA quick_check;' 2>/dev/null); "
              f"  if [ \"$ok\" = ok ]; then echo BACKUP-OK; exit 0; fi; sleep 2; "
              f"done; echo BACKUP-BAD"])
    if "BACKUP-OK" not in p.stdout:
        raise RuntimeError(f"snapshot copy on the Mac failed integrity after 3 tries: "
                           f"{(p.stderr or p.stdout).strip()[:300]}")

    incoming = os.path.join(hp_dir, ".zotero.sqlite.incoming")
    p = _run(["scp", "-q", f"{mac}:{remote_tmp}", incoming])
    if p.returncode != 0:
        raise RuntimeError(f"scp of the snapshot failed: {p.stderr.strip()[:300]}")
    _run(["ssh", mac, f"rm -f {remote_tmp}"])

    # Sanity before swapping it in: right shape, plausibly fresh.
    con = sqlite3.connect(f"file:{incoming}?immutable=1", uri=True)
    try:
        items = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        latest = con.execute(
            "SELECT MAX(i.dateAdded) FROM itemAnnotations a "
            "JOIN items i ON i.itemID=a.itemID").fetchone()[0]
    finally:
        con.close()
    if items < 1000:
        raise RuntimeError(f"snapshot looks wrong: only {items} items — refusing to "
                           f"swap it in over the current database.")
    report["db_items"] = items
    report["db_latest_annotation"] = latest

    # One-time: preserve the stale fork before the first overwrite.
    live = os.path.join(hp_dir, "zotero.sqlite")
    keep = os.path.join(hp_dir, "zotero.sqlite.stale-fork-20260802")
    if os.path.exists(live) and not os.path.exists(keep):
        os.replace(live, keep)
        report["stale_fork_preserved"] = keep
    os.replace(incoming, live)                      # atomic swap

    # 2 — the PDFs. --delete keeps parity with the Mac (guarded: source must exist and
    # be non-trivial, so a bad path can never empty the local copy).
    if not db_only:
        p = _run(["ssh", mac,
                  f"test -d ~/{cfg['mac_zotero_dir']}/storage && "
                  f"ls ~/{cfg['mac_zotero_dir']}/storage | head -5 | wc -l"])
        if p.returncode != 0 or int((p.stdout or "0").strip() or 0) < 3:
            raise RuntimeError("the Mac's Zotero storage directory is missing or "
                               "near-empty — refusing to rsync --delete against it.")
        p = _run(["rsync", "-a", "--delete", "--timeout=120",
                  f"{mac}:{cfg['mac_zotero_dir']}/storage/",
                  os.path.join(hp_dir, "storage") + "/"],
                 timeout=3600)
        if p.returncode != 0:
            raise RuntimeError(f"storage rsync failed (rc {p.returncode}): "
                               f"{p.stderr.strip()[:300]}")
        report["storage_rsync"] = "ok"

    report["finished"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return report


if __name__ == "__main__":
    cfg = _cfg()
    try:
        r = fetch(cfg, db_only="--db-only" in sys.argv)
        print(json.dumps(r, indent=1))
    except RuntimeError as e:
        sys.exit(f"FETCH FAILED: {e}")
