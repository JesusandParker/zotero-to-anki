#!/usr/bin/env python3
"""
night_shift.py — the orchestrator. Cron starts it nightly; everything else follows.

The night, in order:

    lock -> preflight ping -> fetch Mac state -> detect pending -> open the Anki gate
    -> per unit: [governor -> extract (keys-scoped) -> one fresh Claude session
                  -> verify the write landed -> advance the ledger]
    -> write the morning brief -> copy it to the Mac -> unlock

Design rules it enforces (the doc, 2026-08-25):
  - The unit of work is a set of marks; sessions never learn a chapter boundary.
  - The governor runs BEFORE each unit, never after a failure.
  - The ledger advances ONLY on a confirmed write; failed units come back tomorrow.
  - No new unit starts after the deadline — the five-hour window slides, and spend
    must age out before Parker wakes.
  - The brief's most important section is what the night REFUSED to do.

PAUSE SWITCH: while <state_dir>/PAUSED exists this exits immediately without
spending anything. Parker holds it. Remove the file (and re-enable the cron line)
to resume; --ignore-pause overrides it for deliberate testing.

    python3 night_shift.py             # the real thing (what cron runs)
    python3 night_shift.py --dry-run   # everything except spend + write + ledger
    python3 night_shift.py --once      # real, but a single unit regardless of config
    python3 night_shift.py --no-fetch  # skip the Mac mirror; read the HP's own Zotero
    python3 night_shift.py --ignore-deadline  # deliberate daytime run (see note at the check)
"""
import json, os, shutil, subprocess, sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
sys.path.insert(0, HERE)

import detect_pending as DP            # noqa: E402  (mark_processed lives here)
import unit_prompt                     # noqa: E402
from anki_gate import AnkiGate         # noqa: E402
from fetch_mac_state import fetch      # noqa: E402
from usage_governor import decide      # noqa: E402


def load_cfg():
    with open(os.path.join(HERE, "config.json")) as f:
        cfg = json.load(f)
    local = os.path.join(cfg["state_dir"], "config.local.json")
    if os.path.exists(local):
        with open(local) as f:
            cfg.update(json.load(f))
    return cfg


def claude_bin():
    p = os.path.expanduser("~/.local/bin/claude")
    return p if os.path.exists(p) else (shutil.which("claude") or "claude")


class Night:
    def __init__(self, cfg, dry=False, once=False, ignore_pause=False,
                 no_fetch=False, ignore_deadline=False):
        self.cfg, self.dry = cfg, dry
        self.ignore_pause = ignore_pause
        self.no_fetch = no_fetch
        self.anki_lost = False
        self.ignore_deadline = ignore_deadline
        self.max_units = 1 if once else cfg["max_units_per_night"]
        self.start = datetime.now().astimezone()
        self.date = self.start.strftime("%Y-%m-%d")
        self.night_tag = f"night::{self.date}"
        self.state = cfg["state_dir"]
        for d in ("logs", "briefs", "results"):
            os.makedirs(os.path.join(self.state, d), exist_ok=True)
        self.brief = [f"# Night Shift — {self.date}", ""]
        self.refused = []              # the section that matters most
        self.done = self.failed = 0
        # No new unit after the deadline. Started in the evening, the deadline is
        # tomorrow morning; started after midnight (a manual run), it is this morning.
        hh, mm = map(int, cfg["no_new_units_after"].split(":"))
        base = self.start if self.start.hour < 12 else self.start + timedelta(days=1)
        self.deadline = base.replace(hour=hh, minute=mm, second=0, microsecond=0)

    # ---------------------------------------------------------------- utilities
    def log(self, msg):
        line = f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] {msg}"
        print(line, flush=True)

    def say(self, msg):                # -> brief AND log
        self.brief.append(msg)
        self.log(msg.strip("# ").strip() or ".")

    def refuse(self, what, why):
        self.refused.append(f"- {what}: {why}")
        self.log(f"REFUSED {what}: {why}")

    # ---------------------------------------------------------------- the night
    def run(self):
        # PAUSE: checked before the lock and before ANY spend, because the preflight
        # ping costs tokens. Parker holds the switch — the file is created when he
        # says pause and removed when he says go, and while it exists this exits
        # cleanly no matter who or what invoked it (cron, a stray manual run, a
        # --dry-run). --ignore-pause is the deliberate override for testing.
        paused = os.path.join(self.state, "PAUSED")
        if os.path.exists(paused) and not self.ignore_pause:
            why = ""
            try:
                why = open(paused).read().strip()
            except OSError:
                pass
            self.log("PAUSED — not running. " + (why.splitlines()[0] if why else ""))
            self.log(f"Resume with:  rm {paused}   (and re-enable the cron line)")
            return 0

        lock = os.path.join(self.state, "lock")
        if os.path.exists(lock):
            pid = open(lock).read().strip()
            if pid and os.path.exists(f"/proc/{pid}"):
                self.log(f"another night_shift is running (pid {pid}); exiting.")
                return 0
            os.remove(lock)            # stale lock from a dead run
        with open(lock, "w") as f:
            f.write(str(os.getpid()))
        try:
            return self._run()
        finally:
            os.path.exists(lock) and os.remove(lock)

    def _run(self):
        cb = claude_bin()
        self.log(f"night shift starting (dry={self.dry}, max_units={self.max_units}, "
                 f"deadline {self.deadline:%H:%M})")

        # Preflight: proves claude+model work tonight AND refreshes the OAuth token
        # the governor reads (it is routinely expired by 23:04).
        p = subprocess.run([cb, "-p", "Reply with exactly: OK", "--model",
                            self.cfg["model"], "--effort", "low"],
                           capture_output=True, text=True, timeout=300,
                           stdin=subprocess.DEVNULL)
        if p.returncode != 0 or "OK" not in p.stdout:
            self.say(f"Preflight FAILED — claude -p with model {self.cfg['model']} "
                     f"did not answer (rc {p.returncode}): "
                     f"{(p.stderr or p.stdout).strip()[:300]}")
            self.say("Nothing was spent. The queue is untouched.")
            return self.finish(1)
        self.log(f"preflight ok (model {self.cfg['model']})")

        # Fresh truth from the Mac -- unless the HP's own Zotero is the truth.
        # fetch_mac_state was written on 2026-08-02, when the HP's Zotero was a dead
        # fork and the mirror had to come from the Mac. That stopped being true: as of
        # 2026-09-03 the HP runs a live, fully-synced Zotero holding 4423 items (same
        # as the Mac) and ALL 523 attachment folders, 16 GB, where the Mac had only 45
        # materialised locally. The HP is now the more complete copy, and the
        # Claude<->Zotero bridge depends on that instance staying open -- which the
        # fetch guard forbids. --no-fetch reads the HP's library in place instead.
        # Safe to read live: sources.py copies the DB and opens it immutable=1, so it
        # can never lock Zotero or be locked by it.
        try:
            if self.no_fetch:
                rep = None
                self.say("Zotero: using the HP's own live library (--no-fetch); "
                         "no Mac mirror, nothing overwritten.")
            else:
                rep = fetch(self.cfg)
                self.say(f"Zotero mirror: {rep['db_items']} items, latest annotation "
                         f"{rep.get('db_latest_annotation')}")
        except Exception as e:
            self.say(f"FETCH FAILED — {e}")
            self.say("Nothing was spent. The queue is untouched.")
            return self.finish(1)

        # What is pending? (Same code path as the morning CLI — one truth.)
        q = subprocess.run([sys.executable,
                            os.path.join(SKILL, "scripts", "detect_pending.py"),
                            "--json", "--cap", str(self.cfg["unit_cap"])],
                           capture_output=True, text=True, cwd=SKILL)
        if q.returncode != 0:
            self.say(f"DETECTOR FAILED: {q.stderr.strip()[:300]}")
            return self.finish(1)
        det = json.loads(q.stdout)
        if det.get("ledger_missing"):
            self.say("NO LEDGER — refusing to treat the whole library as pending. "
                     "Run detect_pending.py --baseline first.")
            return self.finish(1)
        units = det["units"]
        if self.cfg.get("order", "newest_first") == "newest_first":
            # Recent reading first — tonight's chapter beats a three-week backlog —
            # but a segment's parts stay in page order regardless of which part
            # happens to hold the newest mark. Two stable sorts: parts ascending,
            # then whole segments by their newest mark, descending.
            seg_newest = {}
            for u in units:
                k = (u["source"], u["segment"])
                seg_newest[k] = max(seg_newest.get(k, ""), u.get("newest_mark") or "")
            units.sort(key=lambda u: u["part"])
            units.sort(key=lambda u: seg_newest[(u["source"], u["segment"])],
                       reverse=True)
        for u in det.get("blocked", []):
            self.refuse(f"{u['source']} ({u['marks']} marks)", u["skip_reason"])
        for s in det.get("unregistered", []):
            self.refuse(f"unregistered: {s['name'][:50]}",
                        f"{s['marks']} marks, not a registered source")
        if det.get("external_excluded"):
            for sid, n in det["external_excluded"].items():
                self.refuse(f"{sid}: {n} external mark(s)",
                            "isExternal — present in the PDF before Parker; not his")
        if not units:
            self.say("Queue empty — every mark in every registered source is carded. "
                     "Nothing spent.")
            return self.finish(0)
        self.say(f"Queue: {len(units)} unit(s), "
                 f"{sum(u['marks'] for u in units)} marks pending. "
                 f"Tonight's cap: {self.max_units} unit(s).")
        self.brief.append("")

        # The gate: identity-checked tunnel to the Mac's real collection.
        try:
            gate = AnkiGate(self.cfg).open()
            self.say(f"Anki gate: tunnel up, profile verified "
                     f"{self.cfg['expected_profiles']}.")
        except Exception as e:
            self.say(f"ANKI GATE FAILED — {e}")
            self.say("No cards were made: making them with no way to deliver would "
                     "spend tokens for nothing. The queue is untouched.")
            return self.finish(1)

        try:
            for i, unit in enumerate(units, 1):
                if self.done >= self.max_units:
                    self.refuse("remaining queue",
                                f"nightly cap of {self.max_units} unit(s) reached")
                    break
                if self.failed >= self.cfg["max_failed_units"]:
                    self.refuse("remaining queue",
                                f"{self.failed} failed unit(s) — stopping rather "
                                f"than burning the same wall repeatedly")
                    break
                # The deadline exists so overnight spend ages out of the rolling
                # five-hour window before Parker wakes. A run he asked for while he
                # is awake has no such constraint -- and because base is today when
                # start.hour < 12, ANY morning run computes a deadline already in the
                # past and refuses every unit. --ignore-deadline is for that case.
                if not self.ignore_deadline and \
                        datetime.now().astimezone() >= self.deadline:
                    self.refuse("remaining queue",
                                f"deadline {self.deadline:%H:%M} — spend must age "
                                f"out of the five-hour window before morning")
                    break

                g = decide(self.cfg, self.state, cb)
                if g["action"] == "stop":
                    self.refuse("remaining queue", g["reason"])
                    break
                effort = g["effort"]
                self.log(f"governor: {g['action']} ({g['reason']})")

                self.run_unit(unit, i, gate, cb, effort)
                if self.anki_lost:
                    self.refuse("remaining queue",
                                "Anki became unreachable mid-run — no further units "
                                "can be verified, let alone written")
                    break
        finally:
            gate.close()

        return self.finish(0)

    # ------------------------------------------------------------------ one unit
    def run_unit(self, unit, idx, gate, cb, effort):
        tag = f"night-unit::{self.start:%Y%m%d-%H%M}-{idx}"
        name = (f"{unit['source']} "
                + (f"{unit['segment_noun']} {unit['segment']}"
                   if unit["segment"] is not None else "(flat)")
                + (f" [{unit['part']}/{unit['parts']}]" if unit["parts"] > 1 else ""))
        hdr = (f"## Unit {idx}: {name} — {unit['marks']} marks, "
               f"p{unit['page_first']}-{unit['page_last']}")
        self.log(f"unit {idx}: {name}")

        # Keys file + scoped extraction (deterministic, before any model spend).
        kpath = os.path.join(self.state, "results", f"{tag.split('::')[1]}.keys.json")
        hlpath = os.path.join(SKILL, "work", unit["source"],
                              f"night_{tag.split('::')[1]}_highlights.json")
        rpath = os.path.join(self.state, "results", f"{tag.split('::')[1]}.result.json")
        with open(kpath, "w") as f:
            json.dump(unit["keys"], f)
        cmd = [sys.executable, os.path.join(SKILL, "scripts", "extract_highlights.py"),
               "--source", unit["source"], "--keys", kpath, "--out", hlpath]
        if unit["segment"] is not None:
            cmd += ["--segment", str(unit["segment"])]
        ex = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL, timeout=900)
        if ex.returncode != 0 or not os.path.exists(hlpath):
            self.failed += 1
            self.say(f"{hdr}\nEXTRACTION FAILED (rc {ex.returncode}): "
                     f"{(ex.stderr or ex.stdout).strip()[:400]}\n")
            return
        items = json.load(open(hlpath))
        extra = {i.get("zotero_key") for i in items} - set(unit["keys"])
        if extra:
            self.failed += 1
            self.say(f"{hdr}\nSCOPE VIOLATION: extraction returned keys outside the "
                     f"unit ({sorted(extra)[:5]}) — refusing to run it.\n")
            return
        if len(items) < len(unit["keys"]):
            self.refuse(f"{name}: {len(unit['keys']) - len(items)} mark(s)",
                        "produced no extractable item (see extractor output in log)")
        if not items:
            DP.mark_processed(unit["keys"], unit["source"], tag,
                              note="no extractable items")
            self.say(f"{hdr}\nNo extractable items at all — keys marked processed so "
                     f"they stop re-queueing; see refusals.\n")
            return

        if self.dry:
            self.say(f"{hdr}\nDRY RUN — extraction verified ({len(items)} items, "
                     f"scope exact). Would run {self.cfg['model']}/{effort} and write "
                     f"to {unit['deck']}.\n")
            self.done += 1
            return

        # One fresh session. Its whole world is the prompt + the scoped file.
        prompt = unit_prompt.build(self.cfg, unit, hlpath, rpath, self.night_tag, tag)
        before = gate.deck_count(unit["deck"])
        ulog = os.path.join(self.state, "logs", f"unit-{tag.split('::')[1]}.json")
        t0 = datetime.now()
        try:
            gate.verify()                                    # identity, every time
            p = subprocess.run(
                [cb, "-p", prompt, "--model", self.cfg["model"], "--effort", effort,
                 "--output-format", "json"],
                capture_output=True, text=True, cwd=SKILL,
                stdin=subprocess.DEVNULL, start_new_session=True,
                timeout=self.cfg["unit_timeout_seconds"])
            timed_out = False
        except subprocess.TimeoutExpired as e:
            p, timed_out = e, True
        mins = (datetime.now() - t0).total_seconds() / 60

        out = (p.stdout or "") if hasattr(p, "stdout") else ""
        with open(ulog, "w") as f:
            f.write(out if isinstance(out, str) else str(out))
        cost = None
        try:
            j = json.loads(out)
            cost = j.get("total_cost_usd")
        except Exception:
            pass

        # Did cards actually land? The deck count is the ground truth; the session's
        # report is testimony. Both are read, and disagreement is said out loud.
        # Anki can vanish MID-RUN -- Parker quits it, or the Mac sleeps. The gate
        # checks Anki at the start, but nothing covered it disappearing later. On
        # 2026-09-03 he quit Anki at 21:17; this call raised ConnectionResetError,
        # the exception went uncaught, and it killed the entire night: unit 2 never
        # ran and no brief was written. An unreachable Anki is a failed unit and a
        # reason to stop, not a stack trace.
        try:
            after = gate.deck_count(unit["deck"])
        except Exception as e:
            self.anki_lost = True
            self.failed += 1
            self.say(f"{hdr}\nANKI WENT AWAY mid-run ({type(e).__name__}) — the write "
                     f"could not be verified, so nothing was marked processed and this "
                     f"unit re-queues. Whatever the session built is still on disk. "
                     f"Stopping the night here; reopen Anki on the Mac and re-run.\n")
            return
        delta = after - before
        res = {}
        if os.path.exists(rpath):
            try:
                res = json.load(open(rpath))
            except Exception:
                res = {}
        status = res.get("status")
        costs = f", ~${cost:.2f}" if isinstance(cost, (int, float)) else ""

        if timed_out:
            if delta > 0:
                DP.mark_processed(unit["keys"], unit["source"], tag,
                                  note=f"TIMEOUT after write ({delta} cards landed)")
                self.done += 1
                self.say(f"{hdr}\nTIMED OUT at {mins:.0f} min BUT {delta} card(s) had "
                         f"already landed in {unit['deck']} — marks marked processed "
                         f"so they will not re-run and duplicate. REVIEW THIS DECK: "
                         f"the run may be incomplete (figures, audit). Tag: {tag}\n")
            else:
                self.failed += 1
                self.say(f"{hdr}\nTIMED OUT at {mins:.0f} min with nothing written. "
                         f"This unit is too big for the timeout — it will re-queue; "
                         f"if it happens twice, lower unit_cap or raise "
                         f"unit_timeout_seconds.\n")
            return

        if delta > 0:
            note = "written" if status == "written" else f"written (session said "f"{status or 'nothing'})"
            DP.mark_processed(unit["keys"], unit["source"], tag, note=note)
            self.done += 1
            hand = (res.get("handoff") or "").strip()
            flags = res.get("flags") or []
            self.say(f"{hdr}\n{delta} card(s) -> {unit['deck']}  "
                     f"({mins:.0f} min{costs}, tag {tag})"
                     + (f"\nFlags: {'; '.join(flags)}" if flags else "")
                     + (f"\n\n{hand}\n" if hand else "\n"))
            if status != "written":
                self.say(f"NOTE: cards landed but the session reported "
                         f"'{status or 'no result file'}' — treated as written so "
                         f"nothing re-runs and duplicates; review the deck.\n")
        elif status == "no_cards":
            DP.mark_processed(unit["keys"], unit["source"], tag,
                              note=f"no_cards: {(res.get('handoff') or '')[:120]}")
            self.done += 1
            self.say(f"{hdr}\nSession finished with no cards to write "
                     f"({mins:.0f} min{costs}). Its reasons:\n"
                     f"{(res.get('handoff') or '(none given)')}\n")
        else:
            self.failed += 1
            tail = out[-500:] if isinstance(out, str) else ""
            self.say(f"{hdr}\nFAILED — nothing landed in the deck and the session "
                     f"reported '{status or 'no result file'}' ({mins:.0f} min{costs})."
                     f"\nMarks stay queued for tomorrow. Log: {ulog}\nTail: {tail}\n")

    # ---------------------------------------------------------------- the brief
    def finish(self, rc):
        self.brief.append("")
        g = decide(self.cfg, self.state, claude_bin())
        self.brief.append(f"Usage at close: {g.get('buckets') or 'unreadable'}")
        self.brief.append(f"Units: {self.done} done, {self.failed} failed. "
                          f"Window: {self.start:%H:%M} -> "
                          f"{datetime.now().astimezone():%H:%M}.")
        self.brief.append("")
        self.brief.append("## What the night refused to do")
        self.brief.extend(self.refused or
                          ["- nothing — everything pending was either run or capped"])
        text = "\n".join(self.brief) + "\n"
        path = os.path.join(self.state, "briefs", f"{self.date}.md")
        with open(path, "w") as f:
            f.write(text)
        self.log(f"brief written: {path}")
        try:
            subprocess.run(["scp", "-q", path,
                            f"{self.cfg['mac_host']}:{self.cfg['brief_mac_path']}"],
                           timeout=60, stdin=subprocess.DEVNULL)
            self.log("brief copied to the Mac")
        except Exception as e:
            self.log(f"brief copy to Mac failed (kept locally): {e}")
        return rc


if __name__ == "__main__":
    cfg = load_cfg()
    night = Night(cfg, dry="--dry-run" in sys.argv, once="--once" in sys.argv,
                  ignore_pause="--ignore-pause" in sys.argv,
                  no_fetch="--no-fetch" in sys.argv,
                  ignore_deadline="--ignore-deadline" in sys.argv)
    sys.exit(night.run())
