"""Praxis loop controller — terminal predicate + guards for "loop until correct".

Spec-driven work iterates: build → verify → fix → verify, until the change
actually meets expectations. The danger is the *literal* never-ending loop — an
agent that spins, re-tries the same failing thing, or declares victory early.

This tool makes the loop deterministic and bounded. A loop has an explicit
**terminal predicate** — a set of acceptance criteria that must all be met — and
two guards so it can never spin forever:

  * a **budget** (max iterations), and
  * **no-progress detection** (patience): N consecutive ticks with no change in
    the progress signature (criteria-met count + a free-form state signal).

Each tick returns one verdict from a closed set: ``continue`` (predicate not yet
met, still making progress, budget remains), ``done`` (predicate satisfied), or
``escalate`` (a guard tripped — stop and bring the user in). Escalation is a real
stop: a loop must be ``resume``-d (with fresh human guidance, optionally a bigger
budget) before it can tick again. The agent never quietly keeps grinding.

Deterministic, stdlib-only. The *judgement* (is a criterion met?) is the caller's;
the *verdict* (continue / done / escalate) is computed here, the same way every
time.

Storage (committed to the consuming repo, under its git root):

    .praxis/loops/
      log.jsonl          the index, one loop per line (full structured state)
      entries/<id>.md     human-readable mirror of each loop
      README.md           explains the directory

Lifecycle:  running -> done | escalated | abandoned   (escalated -> running via resume)

Usage:
    python loop.py init
    python loop.py start --goal "OAuth slice passes verify" \
        --criterion "all unit tests green" \
        --criterion "lint clean" \
        --criterion "spec acceptance checks pass" \
        --max-iterations 8 --patience 3
    python loop.py tick <id> --met c1 --met c2 --signal "1 test failing: token refresh"
    python loop.py status <id>
    python loop.py resume <id> --max-iterations 12 --note "user widened budget"
    python loop.py resolve <id> --as abandoned --note "descoped"
    python loop.py list [--status running]
    python loop.py show <id>

Exit codes:
    0: success (any verdict — a verdict is not an error)
    1: not found / nothing to do (e.g. ticking a closed loop)
    2: arguments wrong
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ("running", "done", "escalated", "abandoned")
VERDICTS = ("continue", "done", "escalate")
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_PATIENCE = 3


# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def repo_root() -> Path:
    """Resolve the git toplevel. Falls back to PRAXIS_LOOPS_ROOT or cwd."""
    override = os.environ.get("PRAXIS_LOOPS_ROOT")
    if override:
        return Path(override).resolve()
    res = _git("rev-parse", "--show-toplevel")
    if res.returncode == 0 and res.stdout.strip():
        return Path(res.stdout.strip())
    return Path.cwd()


def loops_dir() -> Path:
    return repo_root() / ".praxis" / "loops"


def _paths() -> tuple[Path, Path, Path]:
    base = loops_dir()
    return base, base / "log.jsonl", base / "entries"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salt = hashlib.sha1(os.urandom(8)).hexdigest()[:4]
    return f"LOOP-{stamp}-{salt}"


# --------------------------------------------------------------------------- #
# Index (log.jsonl) — read all, rewrite all on mutation
# --------------------------------------------------------------------------- #
def _read_index() -> list[dict]:
    _, log, _ = _paths()
    if not log.is_file():
        return []
    rows: list[dict] = []
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _write_index(rows: list[dict]) -> None:
    _, log, _ = _paths()
    log.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows)
    log.write_text(body + ("\n" if body else ""), encoding="utf-8", newline="\n")


def _find(rows: list[dict], loop_id: str) -> dict | None:
    for r in rows:
        if r.get("id") == loop_id:
            return r
    matches = [r for r in rows if str(r.get("id", "")).startswith(loop_id)]
    if not matches:
        matches = [r for r in rows if loop_id in str(r.get("id", ""))]
    return matches[0] if len(matches) == 1 else None


def _save(loop: dict) -> None:
    """Upsert a loop into the index and rewrite its markdown mirror."""
    rows = _read_index()
    for i, r in enumerate(rows):
        if r.get("id") == loop["id"]:
            rows[i] = loop
            break
    else:
        rows.append(loop)
    _write_index(rows)
    _write_entry_md(loop)


# --------------------------------------------------------------------------- #
# Markdown mirror
# --------------------------------------------------------------------------- #
def _entry_path(loop_id: str) -> Path:
    _, _, entries = _paths()
    return entries / f"{loop_id}.md"


def _write_entry_md(loop: dict) -> None:
    path = _entry_path(loop["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    iters = loop.get("iterations", [])
    last_met = set(iters[-1]["met"]) if iters else set()
    crit_lines = []
    for c in loop.get("criteria", []):
        mark = "x" if c["id"] in last_met else " "
        crit_lines.append(f"- [{mark}] `{c['id']}` {c['text']}")
    iter_lines = ["| # | verdict | met | signal |", "|---|---|---|---|"]
    for it in iters:
        iter_lines.append(
            f"| {it['n']} | {it['verdict']} | {len(it['met'])}/{len(loop.get('criteria', []))}"
            f" | {it.get('signal', '') or '—'} |"
        )
    esc = loop.get("escalation")
    lines = [
        "---",
        f"id: {loop['id']}",
        f"created: {loop['created']}",
        f"updated: {loop['updated']}",
        f"status: {loop['status']}",
        f"verdict: {loop.get('verdict', '')}",
        f"max_iterations: {loop['max_iterations']}",
        f"patience: {loop['patience']}",
        "---",
        "",
        f"# Loop: {loop.get('goal', '')}",
        "",
        f"**Status:** {loop['status']}  ·  **Latest verdict:** {loop.get('verdict', '—')}"
        f"  ·  **Iterations:** {len(iters)}/{loop['max_iterations']}",
        "",
        "## Terminal predicate (all must be met)",
        "",
        *crit_lines,
        "",
        "## Iterations",
        "",
        *iter_lines,
    ]
    if esc:
        lines += ["", f"> **Escalated:** {esc}"]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


# --------------------------------------------------------------------------- #
# init
# --------------------------------------------------------------------------- #
README = """# Praxis loop controller

This directory tracks bounded **work loops** — build → verify → fix → verify
runs that iterate until a change actually meets expectations, without ever
spinning forever (see `rules/loop-control.md`).

Each loop carries a **terminal predicate** (acceptance criteria that must all be
met) and two guards: a max-iteration **budget** and **no-progress** detection.
Every tick yields one verdict — `continue`, `done`, or `escalate`.

- `log.jsonl` — the index (one loop per line). Don't hand-edit; use the CLI.
- `entries/<id>.md` — a human-readable mirror of each loop.

Lifecycle: **running → done | escalated | abandoned** (an escalated loop must be
`resume`-d with fresh guidance before it can continue). Drive it with:

    python tools/loop.py start --goal "..." --criterion "..." --criterion "..."
    python tools/loop.py tick <id> --met c1 --signal "2 tests failing"
"""


def _ensure_structure() -> Path:
    base, log, entries = _paths()
    base.mkdir(parents=True, exist_ok=True)
    entries.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("", encoding="utf-8")
    readme = base / "README.md"
    if not readme.exists():
        readme.write_text(README, encoding="utf-8", newline="\n")
    return base


def cmd_init(_args) -> int:
    base = _ensure_structure()
    print(f"loop ledger ready at {base}")
    return 0


# --------------------------------------------------------------------------- #
# start
# --------------------------------------------------------------------------- #
def cmd_start(args) -> int:
    _ensure_structure()
    criteria_text = [c.strip() for c in (args.criterion or []) if c and c.strip()]
    if not criteria_text:
        print("error: at least one --criterion is required (the terminal predicate "
              "cannot be empty — that is how loops spin forever)", file=sys.stderr)
        return 2
    if args.max_iterations < 1:
        print("error: --max-iterations must be >= 1", file=sys.stderr)
        return 2
    if args.patience < 1:
        print("error: --patience must be >= 1", file=sys.stderr)
        return 2
    loop_id = _new_id()
    criteria = [{"id": f"c{i + 1}", "text": t} for i, t in enumerate(criteria_text)]
    loop = {
        "id": loop_id,
        "created": _now(),
        "updated": _now(),
        "status": "running",
        "goal": args.goal or "",
        "criteria": criteria,
        "max_iterations": args.max_iterations,
        "patience": args.patience,
        "iterations": [],
        "verdict": "",
        "escalation": "",
    }
    _save(loop)
    print(loop_id)
    print(f"  goal: {loop['goal'] or '(none)'}")
    print(f"  predicate: {len(criteria)} criteria; budget {args.max_iterations} "
          f"iterations; patience {args.patience}")
    for c in criteria:
        print(f"    {c['id']}: {c['text']}")
    return 0


# --------------------------------------------------------------------------- #
# tick — record an iteration and compute the verdict
# --------------------------------------------------------------------------- #
def _normalize_met(tokens: list[str], criteria: list[dict]) -> tuple[list[str], str | None]:
    """Map --met tokens to known criterion ids. Returns (ids, error_or_None)."""
    known = {c["id"] for c in criteria}
    if tokens and any(t.strip().lower() == "all" for t in tokens):
        return [c["id"] for c in criteria], None
    out: list[str] = []
    for t in tokens or []:
        t = t.strip()
        if not t:
            continue
        if t.isdigit():
            t = f"c{t}"
        if t not in known:
            return [], f"unknown criterion {t!r}; known: {', '.join(sorted(known))}"
        if t not in out:
            out.append(t)
    return out, None


def _signature(met_ids: list[str], signal: str) -> str:
    return f"{len(met_ids)}|{signal.strip()}"


def _no_progress_streak(iterations: list[dict]) -> int:
    """How many trailing iterations share the latest progress signature."""
    if not iterations:
        return 0
    sigs = [_signature(it["met"], it.get("signal", "")) for it in iterations]
    latest = sigs[-1]
    streak = 0
    for s in reversed(sigs):
        if s == latest:
            streak += 1
        else:
            break
    return streak


def cmd_tick(args) -> int:
    rows = _read_index()
    loop = _find(rows, args.id)
    if not loop:
        print(f"error: no loop matching {args.id!r}", file=sys.stderr)
        return 1
    if loop["status"] != "running":
        print(f"error: loop {loop['id']} is {loop['status']}, not running — "
              f"{'resume it first' if loop['status'] == 'escalated' else 'it is closed'}.",
              file=sys.stderr)
        return 1

    met_ids, err = _normalize_met(args.met or [], loop["criteria"])
    if err:
        print(f"error: {err}", file=sys.stderr)
        return 2

    n = len(loop["iterations"]) + 1
    signal = args.signal or ""
    iteration = {
        "n": n,
        "ts": _now(),
        "met": met_ids,
        "signal": signal,
        "note": args.note or "",
        "verdict": "",  # filled below
    }
    loop["iterations"].append(iteration)

    all_met = len(met_ids) == len(loop["criteria"]) and len(loop["criteria"]) > 0
    streak = _no_progress_streak(loop["iterations"])

    # Verdict, in priority order: predicate met > budget exhausted > stuck > go on.
    escalation = ""
    if all_met:
        verdict = "done"
    elif n >= loop["max_iterations"]:
        verdict = "escalate"
        escalation = (f"budget exhausted: {n}/{loop['max_iterations']} iterations with "
                      f"{len(met_ids)}/{len(loop['criteria'])} criteria met")
    elif streak >= loop["patience"]:
        verdict = "escalate"
        escalation = (f"no progress for {streak} consecutive iterations "
                      f"(signal unchanged: {signal or '∅'})")
    else:
        verdict = "continue"

    iteration["verdict"] = verdict
    loop["verdict"] = verdict
    loop["updated"] = _now()
    if verdict == "done":
        loop["status"] = "done"
    elif verdict == "escalate":
        loop["status"] = "escalated"
        loop["escalation"] = escalation
    _save(loop)

    unmet = [c for c in loop["criteria"] if c["id"] not in met_ids]
    print(f"VERDICT: {verdict}  (iteration {n}/{loop['max_iterations']}, "
          f"{len(met_ids)}/{len(loop['criteria'])} criteria met)")
    if verdict == "done":
        print("  Terminal predicate satisfied — the loop is complete. Record the "
              "result in the memory ledger.")
    elif verdict == "continue":
        print("  Keep iterating. Still unmet:")
        for c in unmet:
            print(f"    {c['id']}: {c['text']}")
    else:  # escalate
        print(f"  STOP — escalate to the user. Reason: {escalation}")
        print("  Do not keep grinding. Bring the user the state, the blocker, and "
              "options; `resume` only after they give guidance (and maybe a bigger "
              "budget).")
    return 0


# --------------------------------------------------------------------------- #
# resume / resolve
# --------------------------------------------------------------------------- #
def cmd_resume(args) -> int:
    rows = _read_index()
    loop = _find(rows, args.id)
    if not loop:
        print(f"error: no loop matching {args.id!r}", file=sys.stderr)
        return 1
    if loop["status"] not in ("escalated", "running"):
        print(f"error: loop {loop['id']} is {loop['status']} and cannot be resumed.",
              file=sys.stderr)
        return 1
    if args.max_iterations is not None:
        if args.max_iterations <= len(loop["iterations"]):
            print(f"error: --max-iterations must exceed iterations already run "
                  f"({len(loop['iterations'])})", file=sys.stderr)
            return 2
        loop["max_iterations"] = args.max_iterations
    if args.patience is not None:
        if args.patience < 1:
            print("error: --patience must be >= 1", file=sys.stderr)
            return 2
        loop["patience"] = args.patience
    loop["status"] = "running"
    loop["verdict"] = ""
    loop["escalation"] = ""
    loop["updated"] = _now()
    _save(loop)
    print(f"resumed {loop['id']} — budget {loop['max_iterations']}, "
          f"patience {loop['patience']}"
          + (f" — {args.note}" if args.note else ""))
    return 0


def cmd_resolve(args) -> int:
    if args.as_ not in ("done", "abandoned"):
        print("error: --as must be 'done' or 'abandoned'", file=sys.stderr)
        return 2
    rows = _read_index()
    loop = _find(rows, args.id)
    if not loop:
        print(f"error: no loop matching {args.id!r}", file=sys.stderr)
        return 1
    loop["status"] = args.as_
    loop["verdict"] = args.as_ if args.as_ == "done" else loop.get("verdict", "")
    loop["updated"] = _now()
    if args.note:
        loop["escalation"] = args.note
    _save(loop)
    print(f"{args.as_} {loop['id']}" + (f" — {args.note}" if args.note else ""))
    return 0


# --------------------------------------------------------------------------- #
# list / show / status
# --------------------------------------------------------------------------- #
_ICON = {"running": "▶", "done": "●", "escalated": "⚠", "abandoned": "⊘"}


def cmd_list(args) -> int:
    rows = _read_index()
    if getattr(args, "status", None):
        rows = [r for r in rows if r.get("status") == args.status]
    if not rows:
        print("(no matching loops)")
        return 0
    rows.sort(key=lambda r: r.get("created", ""), reverse=True)
    for r in rows:
        icon = _ICON.get(r.get("status", ""), "?")
        met = len(r["iterations"][-1]["met"]) if r.get("iterations") else 0
        print(f"{icon} {r.get('id')}  [{r.get('status')}]  "
              f"{met}/{len(r.get('criteria', []))} met  "
              f"iter {len(r.get('iterations', []))}/{r.get('max_iterations')}\n"
              f"    {r.get('goal', '')}")
    return 0


def cmd_show(args) -> int:
    loop = _find(_read_index(), args.id)
    if not loop:
        print(f"error: no loop matching {args.id!r}", file=sys.stderr)
        return 1
    path = _entry_path(loop["id"])
    if path.is_file():
        print(path.read_text(encoding="utf-8"))
    else:
        print(json.dumps(loop, indent=2, ensure_ascii=False))
    return 0


def cmd_status(args) -> int:
    loop = _find(_read_index(), args.id)
    if not loop:
        print(f"error: no loop matching {args.id!r}", file=sys.stderr)
        return 1
    iters = loop.get("iterations", [])
    last_met = set(iters[-1]["met"]) if iters else set()
    print(f"{_ICON.get(loop['status'], '?')} {loop['id']}  [{loop['status']}]")
    print(f"  goal: {loop.get('goal', '') or '(none)'}")
    print(f"  iterations: {len(iters)}/{loop['max_iterations']}  "
          f"patience: {loop['patience']}  latest verdict: {loop.get('verdict', '—') or '—'}")
    print("  terminal predicate:")
    for c in loop["criteria"]:
        mark = "✓" if c["id"] in last_met else "·"
        print(f"    [{mark}] {c['id']}: {c['text']}")
    if loop.get("escalation"):
        print(f"  escalation: {loop['escalation']}")
    return 0


# --------------------------------------------------------------------------- #
# brief — compact context line for hooks (SessionStart / pre-gate)
# --------------------------------------------------------------------------- #
def cmd_brief(_args) -> int:
    rows = _read_index()
    escalated = [r for r in rows if r.get("status") == "escalated"]
    running = [r for r in rows if r.get("status") == "running"]
    if not escalated and not running:
        return 0
    if escalated:
        print(f"[praxis loops] {len(escalated)} loop"
              f"{'' if len(escalated) == 1 else 's'} ESCALATED — need your guidance "
              f"before work continues:")
        for r in escalated[:10]:
            print(f"  - {r.get('id')}: {r.get('goal', '') or '(no goal)'}"
                  f" — {r.get('escalation', '') or 'a guard tripped'}")
        print("  Give guidance, then `python tools/loop.py resume <id>`.")
    if running:
        print(f"[praxis loops] {len(running)} loop"
              f"{'' if len(running) == 1 else 's'} in progress.")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Praxis loop controller.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create the loop directory structure.").set_defaults(func=cmd_init)

    st = sub.add_parser("start", help="Start a bounded loop with a terminal predicate.")
    st.add_argument("--goal", default="", help="what the loop is trying to achieve")
    st.add_argument("--criterion", action="append", required=True,
                    help="an acceptance criterion (repeatable; all must be met to finish)")
    st.add_argument("--max-iterations", type=int, default=DEFAULT_MAX_ITERATIONS,
                    help=f"budget guard (default {DEFAULT_MAX_ITERATIONS})")
    st.add_argument("--patience", type=int, default=DEFAULT_PATIENCE,
                    help=f"no-progress guard: escalate after this many unchanging ticks "
                         f"(default {DEFAULT_PATIENCE})")
    st.set_defaults(func=cmd_start)

    tk = sub.add_parser("tick", help="Record an iteration; prints the verdict.")
    tk.add_argument("id")
    tk.add_argument("--met", action="append",
                    help="criterion id now met (e.g. c1), a number, or 'all' (repeatable)")
    tk.add_argument("--signal", help="free-form state fingerprint, e.g. '2 tests failing'")
    tk.add_argument("--note")
    tk.set_defaults(func=cmd_tick)

    rs = sub.add_parser("resume", help="Re-open an escalated loop after the user gives guidance.")
    rs.add_argument("id")
    rs.add_argument("--max-iterations", type=int, help="raise the budget")
    rs.add_argument("--patience", type=int, help="adjust the no-progress guard")
    rs.add_argument("--note")
    rs.set_defaults(func=cmd_resume)

    rv = sub.add_parser("resolve", help="Manually close a loop as done or abandoned.")
    rv.add_argument("id")
    rv.add_argument("--as", dest="as_", required=True, help="done | abandoned")
    rv.add_argument("--note")
    rv.set_defaults(func=cmd_resolve)

    ls = sub.add_parser("list", help="List loops.")
    ls.add_argument("--status", choices=STATUSES)
    ls.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help="Print one loop's full mirror.")
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    stt = sub.add_parser("status", help="Show one loop's predicate and progress.")
    stt.add_argument("id")
    stt.set_defaults(func=cmd_status)

    sub.add_parser("brief", help="Compact summary of escalated/running loops (for hooks).").set_defaults(func=cmd_brief)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
