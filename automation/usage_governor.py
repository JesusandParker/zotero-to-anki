#!/usr/bin/env python3
"""
usage_governor.py — the check that runs BEFORE each unit, never after.

Reads the same usage buckets Claude Code itself tracks — five_hour, seven_day,
seven_day_opus, seven_day_sonnet — from the OAuth usage endpoint the CLI uses
internally (GET /api/oauth/usage with the subscription's access token). This is
Parker's real subscription meter, not an estimate.

Why before: checking after a unit has already failed on a limit means the failure was
paid for and nothing was learned that couldn't have been known first. The orchestrator
calls decide() between units; a unit in flight is never interrupted.

The three-line policy (design doc, 2026-08-25):
  - five-hour window crowded            -> stop for the night (it slides; morning matters)
  - weekly bucket at the hard ceiling   -> stop (the weekly cap is the real budget)
  - weekly bucket past the soft line    -> step effort down, never the model
    ("hold the model, drop the effort, and below that defer to tomorrow" — three
    excellent segments beat six mediocre ones, and deferred marks are still queued)

FAIL CLOSED. If usage cannot be read after a token refresh, the governor refuses the
night rather than spending blind. The brief says exactly that.

CLI (for testing):
    python3 usage_governor.py --show      # raw buckets, normalized
    python3 usage_governor.py --decide    # the go/step_down/stop decision
"""
import json, os, subprocess, sys, time, urllib.request

CREDS = os.path.expanduser("~/.claude/.credentials.json")
USAGE_URL = "https://api.anthropic.com/api/oauth/usage"


def _read_token():
    with open(CREDS) as f:
        d = json.load(f)
    o = d.get("claudeAiOauth", d)          # both layouts exist in the wild
    return o.get("accessToken"), o.get("expiresAt")


def _refresh_token(claude_bin="claude"):
    """The CLI refreshes and rewrites the credentials file as part of any run — that is
    how the 04:30 frame-art cron has survived every token expiry. A one-word haiku ping
    is the cheapest way to trigger it."""
    subprocess.run([claude_bin, "-p", "Reply with exactly: OK", "--model", "haiku",
                    "--effort", "low"],
                   capture_output=True, text=True, timeout=120,
                   stdin=subprocess.DEVNULL)


def _fetch(token):
    req = urllib.request.Request(USAGE_URL, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "anthropic-beta": "oauth-2025-04-20",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _pct(v):
    """Normalize a utilization value to 0-100 whatever the field's scale."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f * 100.0 if 0 <= f <= 1 else f


def _walk(node, path, out):
    """Find every dict that looks like a usage bucket, wherever the schema nests it."""
    if isinstance(node, dict):
        for field in ("utilization", "used_percentage", "used_pct", "percent_used"):
            if field in node:
                p = _pct(node[field])
                if p is not None and path:
                    out[path[-1]] = {"pct": p, "resets_at": node.get("resets_at")}
                break
        for k, v in node.items():
            _walk(v, path + [k], out)
    elif isinstance(node, list):
        for v in node:
            _walk(v, path, out)


def read_usage(state_dir=None, claude_bin="claude"):
    """-> (buckets, raw). buckets: {name: {pct, resets_at}}. Raises on failure.

    Retries once through a token refresh: at 23:04 the access token from the afternoon
    is routinely expired, and the refresh is what any claude run would do anyway.
    """
    last_err = None
    for attempt in (1, 2):
        try:
            token, expires = _read_token()
            if not token:
                raise RuntimeError(f"no access token in {CREDS}")
            if expires and expires / 1000 < time.time() and attempt == 1:
                raise RuntimeError("token expired")       # -> refresh path
            raw = _fetch(token)
            buckets = {}
            _walk(raw, [], buckets)
            if state_dir:                                  # keep one raw sample per night
                os.makedirs(state_dir, exist_ok=True)      # for schema-drift debugging
                with open(os.path.join(state_dir, "usage-last-raw.json"), "w") as f:
                    json.dump(raw, f, indent=1)
            if not buckets:
                raise RuntimeError(f"no usage buckets recognized in response "
                                   f"(raw saved to {state_dir or 'nowhere'})")
            return buckets, raw
        except Exception as e:
            last_err = e
            if attempt == 1:
                _refresh_token(claude_bin)
    raise RuntimeError(f"usage unreadable after token refresh: {last_err}")


def decide(cfg, state_dir=None, claude_bin="claude"):
    """-> {action: go|step_down|stop, effort, reason, buckets}. Fail-closed on stop."""
    try:
        buckets, _ = read_usage(state_dir, claude_bin)
    except Exception as e:
        return {"action": "stop", "effort": None,
                "reason": f"governor fail-closed: {e}", "buckets": {}}

    five = buckets.get("five_hour", {}).get("pct", 0.0)
    weekly = max((buckets[b]["pct"] for b in
                  ("seven_day", "seven_day_opus", "seven_day_sonnet") if b in buckets),
                 default=0.0)
    summary = {k: round(v["pct"], 1) for k, v in sorted(buckets.items())}

    if five >= cfg["five_hour_stop_pct"]:
        return {"action": "stop", "effort": None, "buckets": summary,
                "reason": f"five-hour window at {five:.0f}% "
                          f"(stop line {cfg['five_hour_stop_pct']}%) — it slides, and "
                          f"tonight's spend must age out before morning"}
    if weekly >= cfg["weekly_stop_pct"]:
        return {"action": "stop", "effort": None, "buckets": summary,
                "reason": f"weekly bucket at {weekly:.0f}% "
                          f"(ceiling {cfg['weekly_stop_pct']}%) — the reserve is for "
                          f"daytime work; pending marks stay queued"}
    if weekly >= cfg["weekly_soft_pct"]:
        return {"action": "step_down", "effort": cfg["step_down_effort"], "buckets": summary,
                "reason": f"weekly bucket at {weekly:.0f}% (soft line "
                          f"{cfg['weekly_soft_pct']}%) — effort stepped to "
                          f"{cfg['step_down_effort']}, model held"}
    return {"action": "go", "effort": cfg["effort"], "buckets": summary,
            "reason": f"five-hour {five:.0f}%, weekly {weekly:.0f}% — clear"}


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "config.json")) as f:
        cfg = json.load(f)
    if "--show" in sys.argv:
        buckets, raw = read_usage(cfg.get("state_dir"))
        print(json.dumps({k: v for k, v in sorted(buckets.items())}, indent=1))
    else:
        print(json.dumps(decide(cfg, cfg.get("state_dir")), indent=1))
