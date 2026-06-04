"""Runtime session state — disposable glue, not durable doctrine.

Tracks the last active project / repo / spec / command and an append-only
activity log. This is deliberately separate from durable memory (project
decisions, the ledger): major decisions are NEVER stored only here.

Files (under runtime/, gitignored — they are session-local):
    runtime/session-state.json   the current pointers (see schemas/session-state.schema.json)
    runtime/activity-log.jsonl   append-only events, one JSON object per line

Usage:
    python tools/runtime.py show
    python tools/runtime.py set --project checkout --spec oauth --command /new-feature
    python tools/runtime.py log --type adapter-install --note "codex"
    python tools/runtime.py init

Exit codes:
    0: ok
    1: error reading/writing state
    2: arguments wrong
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

STATE_FIELDS = ("lastActiveProject", "lastActiveRepo", "lastActiveSpec", "lastCommand")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _runtime_dir(root: Path) -> Path:
    return root / "runtime"


def _state_path(root: Path) -> Path:
    return _runtime_dir(root) / "session-state.json"


def _log_path(root: Path) -> Path:
    return _runtime_dir(root) / "activity-log.jsonl"


def _default_state() -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "lastActiveProject": None,
        "lastActiveRepo": None,
        "lastActiveSpec": None,
        "lastCommand": None,
        "updated": None,
    }


def load_state(root: Path) -> dict[str, Any]:
    path = _state_path(root)
    if not path.is_file():
        return _default_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _default_state()
    state = _default_state()
    if isinstance(data, dict):
        state.update({k: v for k, v in data.items() if k in state})
    return state


def write_state(root: Path, state: dict[str, Any]) -> None:
    _runtime_dir(root).mkdir(parents=True, exist_ok=True)
    _state_path(root).write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )


def append_event(root: Path, event: dict[str, Any]) -> None:
    _runtime_dir(root).mkdir(parents=True, exist_ok=True)
    event = {"ts": _now(), **event}
    with _log_path(root).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, separators=(",", ":")) + "\n")


def cmd_init(root: Path, _args) -> int:
    if not _state_path(root).is_file():
        write_state(root, _default_state())
    _log_path(root).touch()
    print(f"runtime initialized at {_runtime_dir(root)}")
    return 0


def cmd_show(root: Path, _args) -> int:
    print(json.dumps(load_state(root), indent=2))
    return 0


def cmd_set(root: Path, args) -> int:
    state = load_state(root)
    mapping = {
        "lastActiveProject": args.project,
        "lastActiveRepo": args.repo,
        "lastActiveSpec": args.spec,
        "lastCommand": args.command,
    }
    changed = {}
    for field, value in mapping.items():
        if value is not None:
            state[field] = value
            changed[field] = value
    state["updated"] = _now()
    write_state(root, state)
    append_event(root, {"type": "set", "changed": changed})
    print(json.dumps(state, indent=2))
    return 0


def cmd_log(root: Path, args) -> int:
    event: dict[str, Any] = {"type": args.type}
    if args.note is not None:
        event["note"] = args.note
    append_event(root, event)
    print(f"logged: {event['type']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Read/update runtime session state.")
    p.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Harness root (default: repo root containing this tool).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create runtime/ with an empty state.").set_defaults(func=cmd_init)
    sub.add_parser("show", help="Print the current session state.").set_defaults(func=cmd_show)

    st = sub.add_parser("set", help="Update one or more state pointers.")
    st.add_argument("--project")
    st.add_argument("--repo")
    st.add_argument("--spec")
    st.add_argument("--command")
    st.set_defaults(func=cmd_set)

    lg = sub.add_parser("log", help="Append an activity-log event.")
    lg.add_argument("--type", required=True, help="Event type, e.g. adapter-install.")
    lg.add_argument("--note", help="Optional free-text note.")
    lg.set_defaults(func=cmd_log)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root)
    try:
        return args.func(root, args)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
