"""Praxis assumptions ledger — the deterministic spine of "never assume, always
validate".

When an agent must move forward without certainty, it does **not** guess
silently. It records the assumption here, keeps working (only when the choice is
low-stakes and reversible — a material ambiguity is a *stop condition*, see
``rules/stop-conditions.md``), and a later sweep replays every open assumption to
the user as a question-flow. The user's answer becomes a durable decision in the
memory ledger and, when it generalises, a *proposed* promotion to a rule,
guardrail, eval, or workflow gate — proposed, never applied silently.

Deterministic, stdlib-only. No LLM involvement and no third-party deps so it runs
on a vanilla Python install and inside hooks. This file decides *nothing*; it
only records what the agent assumed and surfaces it for the user to adjudicate.

Storage (committed to the consuming repo, under its git root):

    .praxis/assumptions/
      log.jsonl            the index, one JSON object per assumption
      entries/<id>.md      full content: frontmatter + reasoning body
      README.md            explains the directory

Lifecycle:  open -> confirmed | corrected | withdrawn

    open       recorded by the agent, awaiting the user's adjudication
    confirmed  the user agreed the assumption was right
    corrected  the user supplied a different answer (recorded as the resolution)
    withdrawn  the assumption became moot (the code path it covered is gone)

Usage:
    python assumptions.py init
    python assumptions.py add --statement "API returns ISO-8601 timestamps" \
        --impact "date parsing in the ingest worker" --confidence low \
        --source /developer --alt "epoch millis" --alt "RFC-2822" \
        --body "No schema was provided; assumed ISO-8601 to keep moving."
    python assumptions.py list [--status open]
    python assumptions.py open [--brief]
    python assumptions.py show <id>
    python assumptions.py sweep [--json]            # the question-flow material
    python assumptions.py confirm <id> [--decision <ledger-id>] [--promote rule] [--note ...]
    python assumptions.py correct <id> --answer "epoch millis" [--decision <id>] [--promote eval]
    python assumptions.py withdraw <id> [--note ...]
    python assumptions.py status

Exit codes:
    0: success
    1: not found / nothing to do
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

# Confidence is bounded on purpose: if you are *highly* confident you are not
# assuming, you are asserting — record that as a decision, not an assumption.
CONFIDENCE = ("low", "medium")
STATUSES = ("open", "confirmed", "corrected", "withdrawn")
OPEN_STATUSES = ("open",)
# Where a resolved assumption may be proposed for promotion. "none" means the
# answer is a one-off decision with no general rule behind it.
PROMOTE_TARGETS = ("none", "rule", "guardrail", "eval", "gate")
# lowest confidence first — the most fragile assumptions get adjudicated soonest
_CONFIDENCE_RANK = {"low": 0, "medium": 1}


# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def repo_root() -> Path:
    """Resolve the git toplevel. Falls back to PRAXIS_ASSUMPTIONS_ROOT or cwd."""
    override = os.environ.get("PRAXIS_ASSUMPTIONS_ROOT")
    if override:
        return Path(override).resolve()
    res = _git("rev-parse", "--show-toplevel")
    if res.returncode == 0 and res.stdout.strip():
        return Path(res.stdout.strip())
    return Path.cwd()


def assumptions_dir() -> Path:
    return repo_root() / ".praxis" / "assumptions"


def _paths() -> tuple[Path, Path, Path]:
    base = assumptions_dir()
    return base, base / "log.jsonl", base / "entries"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salt = hashlib.sha1(os.urandom(8)).hexdigest()[:4]
    return f"ASSUME-{stamp}-{salt}"


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


def _find(rows: list[dict], entry_id: str) -> dict | None:
    for r in rows:
        if r.get("id") == entry_id:
            return r
    # allow an unambiguous prefix match for convenience (e.g. the timestamp tail)
    matches = [r for r in rows if str(r.get("id", "")).startswith(entry_id)]
    if not matches:
        matches = [r for r in rows if entry_id in str(r.get("id", ""))]
    return matches[0] if len(matches) == 1 else None


# --------------------------------------------------------------------------- #
# Entry markdown files
# --------------------------------------------------------------------------- #
def _entry_path(entry_id: str) -> Path:
    _, _, entries = _paths()
    return entries / f"{entry_id}.md"


def _write_entry_md(meta: dict, body: str) -> None:
    path = _entry_path(meta["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    fm_keys = [
        "id", "created", "updated", "source", "status", "confidence",
        "statement", "impact", "alternatives", "promote", "decision_ref",
        "promotion_ref", "resolution",
    ]
    lines = ["---"]
    for k in fm_keys:
        v = meta.get(k)
        if v in (None, "", []):
            continue
        if k == "alternatives" and isinstance(v, list):
            v = "; ".join(v)
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append((body or "").rstrip() + "\n")
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def _read_entry_body(entry_id: str) -> str:
    path = _entry_path(entry_id)
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return parts[2].strip("\n") if len(parts) == 3 else text


# --------------------------------------------------------------------------- #
# init
# --------------------------------------------------------------------------- #
README = """# Praxis assumptions ledger

This directory is the project's **assumptions log** — the record behind the
harness rule *never assume, always validate* (see `rules/never-assume.md`).

When an agent has to move forward without certainty on a low-stakes, reversible
choice, it records the assumption here instead of guessing silently. A material
ambiguity is **not** logged here — it is a stop condition, and the agent stops
and asks (see `rules/stop-conditions.md`).

- `log.jsonl` — the index (one assumption per line). Don't hand-edit; use the CLI.
- `entries/<id>.md` — the full reasoning for each assumption.

Lifecycle: **open → confirmed | corrected | withdrawn**.

A later **sweep** replays every open assumption to the user as a question-flow:

    python tools/assumptions.py sweep

The user's answer is recorded as a durable decision in the memory ledger and,
when it generalises, *proposed* for promotion to a rule, guardrail, eval, or
workflow gate — proposed via the ledger as `pending`, never applied silently.
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
    print(f"assumptions ledger ready at {base}")
    return 0


# --------------------------------------------------------------------------- #
# add — record an assumption
# --------------------------------------------------------------------------- #
def _read_body_arg(args) -> str:
    if getattr(args, "body_file", None):
        return Path(args.body_file).read_text(encoding="utf-8")
    if getattr(args, "body", None) == "-":
        return sys.stdin.read()
    return getattr(args, "body", None) or ""


def cmd_add(args) -> int:
    _ensure_structure()
    if args.confidence not in CONFIDENCE:
        print(f"error: --confidence must be one of {', '.join(CONFIDENCE)} "
              f"(high confidence is not an assumption — record a decision instead)",
              file=sys.stderr)
        return 2
    entry_id = _new_id()
    alternatives = [a.strip() for a in (args.alt or []) if a and a.strip()]
    meta = {
        "id": entry_id,
        "created": _now(),
        "updated": _now(),
        "source": args.source or "manual",
        "status": "open",
        "confidence": args.confidence,
        "statement": args.statement,
        "impact": args.impact or "",
        "alternatives": alternatives,
        "promote": "none",
        "decision_ref": "",
        "promotion_ref": "",
        "resolution": "",
    }
    rows = _read_index()
    rows.append({k: meta[k] for k in (
        "id", "created", "updated", "source", "status", "confidence",
        "statement", "impact", "alternatives", "promote", "decision_ref",
        "promotion_ref", "resolution",
    ) if meta[k] not in (None, "", [])})
    _write_index(rows)
    _write_entry_md(meta, _read_body_arg(args))
    print(entry_id)
    return 0


# --------------------------------------------------------------------------- #
# list / open / show / status
# --------------------------------------------------------------------------- #
_ICON = {"open": "○", "confirmed": "●", "corrected": "✎", "withdrawn": "⊘"}


def _sorted_open(rows: list[dict]) -> list[dict]:
    """Open assumptions, lowest confidence first, then oldest first."""
    opens = [r for r in rows if r.get("status") == "open"]
    opens.sort(key=lambda r: (_CONFIDENCE_RANK.get(r.get("confidence"), 9),
                              r.get("created", "")))
    return opens


def cmd_list(args) -> int:
    rows = _read_index()
    if getattr(args, "status", None):
        rows = [r for r in rows if r.get("status") == args.status]
    if not rows:
        print("(no matching assumptions)")
        return 0
    rows.sort(key=lambda r: r.get("created", ""), reverse=True)
    for r in rows:
        icon = _ICON.get(r.get("status", ""), "?")
        print(f"{icon} {r.get('id')}  [{r.get('status')}]  conf={r.get('confidence')}"
              f"  {r.get('source')}\n    {r.get('statement', '')}")
    return 0


def cmd_open(args) -> int:
    opens = _sorted_open(_read_index())
    if args.brief:
        if not opens:
            return 0
        print(f"[praxis assumptions] {len(opens)} open assumption"
              f"{'' if len(opens) == 1 else 's'} awaiting validation:")
        for r in opens[:10]:
            print(f"  - {r.get('id')} (conf={r.get('confidence')}): {r.get('statement', '')}")
        print("  Replay them with `python tools/assumptions.py sweep`.")
        return 0
    if not opens:
        print("(no open assumptions)")
        return 0
    for r in opens:
        print(f"○ {r.get('id')}  conf={r.get('confidence')}  {r.get('source')}\n"
              f"    {r.get('statement', '')}\n    impact: {r.get('impact', '') or '—'}")
    return 0


def cmd_show(args) -> int:
    entry = _find(_read_index(), args.id)
    if not entry:
        print(f"error: no assumption matching {args.id!r}", file=sys.stderr)
        return 1
    print(_read_entry_body(entry["id"]))
    return 0


def cmd_status(_args) -> int:
    rows = _read_index()
    if not rows:
        print("assumptions ledger is empty.")
        return 0
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
    print(f"Praxis assumptions — {len(rows)} recorded")
    print("  by status: " + ", ".join(f"{_ICON.get(k, '?')} {k}={v}"
                                       for k, v in sorted(by_status.items())))
    n_open = by_status.get("open", 0)
    if n_open:
        print(f"  {n_open} open — run `sweep` to validate with the user.")
    return 0


# --------------------------------------------------------------------------- #
# sweep — turn open assumptions into question-flow material
# --------------------------------------------------------------------------- #
def _question(entry: dict) -> dict:
    """Shape one open assumption into a question with A/B/C options.

    Deterministic: the recorded assumption is always option A and the AI's
    recommendation; the alternatives follow. The caller (agent) renders this as
    a real prompt and always allows a free-form answer on top.
    """
    options = [{"key": "A", "text": entry.get("statement", ""), "recommended": True}]
    for i, alt in enumerate(entry.get("alternatives", []) or []):
        options.append({"key": chr(ord("B") + i), "text": alt, "recommended": False})
    impact = entry.get("impact", "") or "(impact not recorded)"
    return {
        "id": entry.get("id"),
        "confidence": entry.get("confidence"),
        "question": f"I assumed: {entry.get('statement', '')}. This affects {impact}. "
                    f"Is that right?",
        "options": options,
        "free_answer": True,
    }


def cmd_sweep(args) -> int:
    opens = _sorted_open(_read_index())
    questions = [_question(r) for r in opens]
    if args.json:
        print(json.dumps({"questions": questions}, ensure_ascii=False, indent=2))
        return 0
    if not questions:
        print("No open assumptions — nothing to validate.")
        return 0
    print(f"{len(questions)} assumption(s) to validate with the user "
          f"(lowest confidence first):\n")
    for q in questions:
        print(f"[{q['id']}]  (confidence: {q['confidence']})")
        print(f"  {q['question']}")
        for opt in q["options"]:
            rec = "  ← recommended (what I assumed)" if opt["recommended"] else ""
            print(f"    {opt['key']}. {opt['text']}{rec}")
        print("    Or give a free-form answer.\n")
    print("Resolve each with `confirm <id>` or `correct <id> --answer \"...\"`, "
          "recording the decision in the memory ledger.")
    return 0


# --------------------------------------------------------------------------- #
# confirm / correct / withdraw
# --------------------------------------------------------------------------- #
def _resolve(entry_id: str, status: str, *, resolution: str | None,
             decision_ref: str | None, promote: str | None,
             note: str | None) -> dict | None:
    rows = _read_index()
    entry = _find(rows, entry_id)
    if not entry:
        return None
    now = _now()
    entry["status"] = status
    entry["updated"] = now
    if resolution is not None:
        entry["resolution"] = resolution
    if decision_ref:
        entry["decision_ref"] = decision_ref
    if promote:
        entry["promote"] = promote
    _write_index(rows)

    footer = f"_{status} on {now}_"
    if resolution:
        footer += f" — resolution: {resolution}"
    if decision_ref:
        footer += f" — decision: {decision_ref}"
    if promote and promote != "none":
        footer += f" — promote → {promote} (propose via the memory ledger as pending)"
    if note:
        footer += f" — {note}"
    body = _read_entry_body(entry["id"]).rstrip() + f"\n\n---\n\n{footer}\n"
    _write_entry_md(dict(entry), body)
    return entry


def _check_promote(value: str | None) -> bool:
    return value is None or value in PROMOTE_TARGETS


def cmd_confirm(args) -> int:
    if not _check_promote(args.promote):
        print(f"error: --promote must be one of {', '.join(PROMOTE_TARGETS)}", file=sys.stderr)
        return 2
    entry = _resolve(args.id, "confirmed", resolution=None,
                     decision_ref=args.decision, promote=args.promote, note=args.note)
    if not entry:
        print(f"error: no assumption matching {args.id!r}", file=sys.stderr)
        return 1
    print(f"confirmed {entry['id']}")
    if args.promote and args.promote != "none":
        print(f"  → propose a {args.promote} via `/memory log` (pending) — never apply it silently.")
    elif not args.decision:
        print("  reminder: record the confirmed answer as a decision in the memory ledger.")
    return 0


def cmd_correct(args) -> int:
    if not _check_promote(args.promote):
        print(f"error: --promote must be one of {', '.join(PROMOTE_TARGETS)}", file=sys.stderr)
        return 2
    entry = _resolve(args.id, "corrected", resolution=args.answer,
                     decision_ref=args.decision, promote=args.promote, note=args.note)
    if not entry:
        print(f"error: no assumption matching {args.id!r}", file=sys.stderr)
        return 1
    print(f"corrected {entry['id']} → {args.answer}")
    print("  the assumption was wrong: record the correction as a decision, and "
          "check whether anything built on it needs to change.")
    if args.promote and args.promote != "none":
        print(f"  → propose a {args.promote} via `/memory log` (pending) so this class "
              f"of mistake is caught next time.")
    return 0


def cmd_withdraw(args) -> int:
    entry = _resolve(args.id, "withdrawn", resolution=None,
                     decision_ref=None, promote=None, note=args.note)
    if not entry:
        print(f"error: no assumption matching {args.id!r}", file=sys.stderr)
        return 1
    print(f"withdrawn {entry['id']}")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Praxis assumptions ledger.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create the assumptions directory structure.").set_defaults(func=cmd_init)

    ad = sub.add_parser("add", help="Record an assumption the agent is proceeding on.")
    ad.add_argument("--statement", required=True, help="what is being assumed")
    ad.add_argument("--impact", default="", help="what this assumption affects")
    ad.add_argument("--confidence", required=True, help=f"one of: {', '.join(CONFIDENCE)}")
    ad.add_argument("--source", default="manual", help="step/agent/command, e.g. /developer")
    ad.add_argument("--alt", action="append", help="an alternative (repeatable)")
    ad.add_argument("--body", help="full reasoning, or '-' to read stdin")
    ad.add_argument("--body-file", help="read the body from a file")
    ad.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="List assumptions.")
    ls.add_argument("--status", choices=STATUSES)
    ls.set_defaults(func=cmd_list)

    op = sub.add_parser("open", help="List open assumptions (lowest confidence first).")
    op.add_argument("--brief", action="store_true", help="compact output for hooks/context")
    op.set_defaults(func=cmd_open)

    sh = sub.add_parser("show", help="Print one assumption's full content.")
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    sw = sub.add_parser("sweep", help="Render open assumptions as question-flow material.")
    sw.add_argument("--json", action="store_true", help="machine-readable output for the agent")
    sw.set_defaults(func=cmd_sweep)

    cf = sub.add_parser("confirm", help="Mark an assumption confirmed (the user agreed).")
    cf.add_argument("id")
    cf.add_argument("--decision", help="memory-ledger entry id recording the decision")
    cf.add_argument("--promote", help=f"propose promotion: {', '.join(PROMOTE_TARGETS)}")
    cf.add_argument("--note")
    cf.set_defaults(func=cmd_confirm)

    co = sub.add_parser("correct", help="Mark an assumption corrected (the user gave a different answer).")
    co.add_argument("id")
    co.add_argument("--answer", required=True, help="the correct value the user supplied")
    co.add_argument("--decision", help="memory-ledger entry id recording the decision")
    co.add_argument("--promote", help=f"propose promotion: {', '.join(PROMOTE_TARGETS)}")
    co.add_argument("--note")
    co.set_defaults(func=cmd_correct)

    wd = sub.add_parser("withdraw", help="Mark an assumption withdrawn (no longer relevant).")
    wd.add_argument("id")
    wd.add_argument("--note")
    wd.set_defaults(func=cmd_withdraw)

    sub.add_parser("status", help="Summary dashboard.").set_defaults(func=cmd_status)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
