#!/usr/bin/env python3
"""
anki_gate.py — the ONLY door to Anki, and it checks ID before opening.

The single unrecoverable failure in this whole design is a write into the wrong
collection. Two Anki collections exist: the Mac's real one (profile "Parkers Anki",
85k+ notes, alive) and the HP's abandoned fork (profile "User 1", 49k notes, frozen
2026-08-02). If the fork ever got written to and then synced, "Upload" would destroy
the real collection — see reference_anki_sync_conflict.

So the gate enforces three things, in order:

  1. Port 8765 on this machine must be FREE before the tunnel opens. Anything already
     listening here is, by definition, not the Mac — it is the HP's own Anki, which
     must never be written to. Hard abort, never reuse.
  2. The tunnel is an SSH -L forward to the Mac's AnkiConnect, so "localhost:8765"
     becomes the Mac's live collection and the pipeline's hardcoded URL just works.
  3. IDENTITY: getProfiles must equal exactly ["Parkers Anki"]. The fork answers
     ["User 1"], so this check cannot pass against the wrong collection. It runs after
     the tunnel opens and the orchestrator repeats it before every unit.

CLI:
    python3 anki_gate.py --test    # open, verify, report, close
"""
import json, os, socket, subprocess, sys, time, urllib.request


def _call(action, params=None, port=8765, timeout=30):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}",
        data=json.dumps({"action": action, "version": 6,
                         "params": params or {}}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        res = json.loads(r.read())
    if res.get("error"):
        raise RuntimeError(f"AnkiConnect {action}: {res['error']}")
    return res.get("result")


def _port_open(port):
    with socket.socket() as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


class AnkiGate:
    def __init__(self, cfg):
        self.cfg = cfg
        self.port = cfg["anki_port"]
        self.proc = None

    def open(self):
        if _port_open(self.port):
            raise RuntimeError(
                f"port {self.port} is already in use on this machine BEFORE the tunnel "
                f"— that is a local Anki (the stale fork), not the Mac. Close it. "
                f"The Night Shift never writes to a collection it cannot identify.")
        self.proc = subprocess.Popen(
            ["ssh", "-N", "-o", "BatchMode=yes", "-o", "ExitOnForwardFailure=yes",
             "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3",
             "-L", f"{self.port}:127.0.0.1:{self.port}", self.cfg["mac_host"]],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, text=True)
        for _ in range(30):                              # up to ~15s to come up
            if self.proc.poll() is not None:
                err = (self.proc.stderr.read() or "").strip()[:300]
                raise RuntimeError(f"ssh tunnel to the Mac died at open: {err}")
            if _port_open(self.port):
                break
            time.sleep(0.5)
        else:
            self.close()
            raise RuntimeError("tunnel opened but nothing answered on the forwarded "
                               "port — is Anki running on the Mac?")
        self.verify()
        return self

    def verify(self):
        """The identity check. Runs at open and again before every unit."""
        v = _call("version", port=self.port)
        profiles = _call("getProfiles", port=self.port)
        expected = self.cfg["expected_profiles"]
        if sorted(profiles) != sorted(expected):
            self.close()
            raise RuntimeError(
                f"WRONG COLLECTION: AnkiConnect answered with profiles {profiles}, "
                f"expected exactly {expected}. Refusing to write. (The HP fork answers "
                f"['User 1'] — this check exists so it can never be written to.)")
        return {"version": v, "profiles": profiles}

    # -- helpers the orchestrator uses for delivery verification ----------------
    def deck_count(self, deck):
        notes = _call("findNotes", {"query": f'deck:"{deck}"'}, port=self.port)
        return len(notes or [])

    def notes_added_today(self, deck):
        notes = _call("findNotes", {"query": f'deck:"{deck}" added:1'}, port=self.port)
        return notes or []

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None

    def __enter__(self):
        return self.open()

    def __exit__(self, *a):
        self.close()


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "config.json")) as f:
        cfg = json.load(f)
    with AnkiGate(cfg) as g:
        info = g.verify()
        print(json.dumps({
            "tunnel": "up", **info,
            "sample_deck_counts": {
                d: g.deck_count(d) for d in
                ["all::EMT::Chapter 11::Book Highlights",
                 "all::EMT::Chapter 5::Book Highlights"]},
        }, indent=1))
    print("closed cleanly")
