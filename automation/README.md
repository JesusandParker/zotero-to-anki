# The Night Shift

Unattended overnight card-making. Cron on the HP home server starts `night_shift.py`
nightly at 23:04; by morning, the day's highlights are Anki cards and the spend has
aged out of the five-hour window. Design doc (2026-08-25, the reasoning behind every
rule here): the "Night Shift" artifact.

## The shape

    MacBook  = the truth. Live Zotero, live Anki ("Parkers Anki"), never sleeps.
    HP       = the factory. Mirrors Zotero nightly, runs the sessions, writes back
               through an identity-checked SSH tunnel. Its own Zotero/Anki are
               retired forks and must never run or sync.

    night_shift.py         orchestrator (cron entry: night-shift-cron)
    fetch_mac_state.py     Mac -> HP mirror: sqlite .backup + storage rsync
    usage_governor.py      reads the real subscription buckets; go / step_down / stop
    anki_gate.py           the ONLY door to Anki; getProfiles must be ["Parkers Anki"]
    unit_prompt.py         the factory session's briefing
    config.json            the knobs (per-machine overrides: state_dir/config.local.json)
    ../scripts/detect_pending.py   what is pending (ledger of processed mark keys)

## The rules the code enforces

1. A unit is a SET OF MARKS (max `unit_cap`), never a chapter. Sessions receive an
   already-extracted, keys-scoped highlights file and are forbidden to widen it.
2. The governor runs BEFORE each unit. Weekly bucket past the soft line steps effort
   down (never the model); past the ceiling, the night stops and marks stay queued.
3. The ledger advances ONLY when cards verifiably landed in the deck (count delta),
   or the session credibly reported no_cards. Failed units re-queue tomorrow.
4. No new unit after `no_new_units_after` — the five-hour window slides.
5. Every note gets `night::<date>` and `night-unit::<stamp>` tags: a bad night is
   one Anki search away from block deletion.
6. The brief (HP: night-shift/briefs/, Mac: ~/Desktop/night-shift-brief.md) always
   ends with what the night REFUSED to do.

## Pause switch

While `<state_dir>/PAUSED` exists, `night_shift.py` exits immediately — before the
lock and before the preflight ping, so a paused night spends nothing. It blocks cron,
manual runs, and `--dry-run` alike; `--ignore-pause` is the deliberate override.

    # pause
    printf 'PAUSED <date> — <why>\n' > ~/night-shift/PAUSED
    crontab -e   # comment out the night-shift line

    # resume
    rm ~/night-shift/PAUSED
    crontab -e   # uncomment the night-shift line

Both halves matter: the cron line stops it being invoked, the file stops it running
if it is invoked anyway. **Currently PAUSED (2026-08-26)** at Parker's request while
he works through the EMT backlog himself.

Note: cron invokes the wrapper as `/bin/bash <path>` because Syncthing does not carry
the executable bit from the Mac.

## Running it by hand

    python3 automation/night_shift.py --dry-run   # everything except spend+write
    python3 automation/night_shift.py --once      # real, single unit
    python3 automation/usage_governor.py --show   # the buckets, live
    python3 automation/anki_gate.py --test        # tunnel + identity check
    python3 scripts/detect_pending.py             # the queue, human-readable

## Do-not

- Do not run Anki or Zotero apps on the HP. The mirror and the gate both refuse to
  proceed if they see them, but do not lean on that.
- Do not edit the ledger by hand; it must match what is actually in Anki.
- Do not run two orchestrators; the lock file prevents it.
