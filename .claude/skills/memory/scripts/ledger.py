"""Praxis memory ledger — a versioned record of plans, decisions, implementations
and artifacts, with an accept / pending / rollback lifecycle.

Deterministic, stdlib-only. No LLM involvement and no third-party deps so it runs
on a vanilla Python install and inside hooks.

Storage (committed to the consuming repo, under its git root):

    .praxis/memory/
      ledger.jsonl        append-only-ish index, one JSON object per entry
      entries/<id>.md      full content: YAML-ish frontmatter + markdown body
      patches/<id>.patch   reverse-appliable diff (implementations only)
      README.md            explains the directory

Entry lifecycle:  pending -> accepted | rejected | rolled-back  (and superseded)

Usage:
    python ledger.py init
    python ledger.py log --type decision --title "Use hexagonal ports" \
        --source /architect --tags arch,adr --body "We chose ... because ..."
    python ledger.py snapshot --source /new-feature --title "Auth slice 1"
    python ledger.py list [--status pending] [--type decision] [--source /architect]
    python ledger.py pending [--brief]
    python ledger.py show <id>
    python ledger.py accept <id> [--note "shipped in PR #12"]
    python ledger.py reject <id> [--note "..."]
    python ledger.py rollback <id> [--dry-run]
    python ledger.py status

Exit codes:
    0: success
    1: not found / nothing to do / rollback could not apply cleanly
    2: arguments wrong or not inside a git repo
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TYPES = ("plan", "decision", "implementation", "artifact", "test-strategy", "rollout", "note")
STATUSES = ("pending", "accepted", "rejected", "rolled-back", "superseded")
OPEN_STATUSES = ("pending", "accepted")


# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
def _git(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )


def repo_root() -> Path:
    """Resolve the git toplevel. Falls back to PRAXIS_MEMORY_ROOT or cwd."""
    override = os.environ.get("PRAXIS_MEMORY_ROOT")
    if override:
        return Path(override).resolve()
    res = _git("rev-parse", "--show-toplevel")
    if res.returncode == 0 and res.stdout.strip():
        return Path(res.stdout.strip())
    return Path.cwd()


def memory_dir() -> Path:
    return repo_root() / ".praxis" / "memory"


def _paths() -> tuple[Path, Path, Path, Path]:
    base = memory_dir()
    return base, base / "ledger.jsonl", base / "entries", base / "patches"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _new_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salt = hashlib.sha1(os.urandom(8)).hexdigest()[:4]
    return f"{stamp}-{salt}"


# --------------------------------------------------------------------------- #
# Index (ledger.jsonl) — read all, rewrite all on mutation
# --------------------------------------------------------------------------- #
def _read_index() -> list[dict]:
    _, ledger, _, _ = _paths()
    if not ledger.is_file():
        return []
    rows: list[dict] = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _write_index(rows: list[dict]) -> None:
    _, ledger, _, _ = _paths()
    ledger.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows)
    ledger.write_text(body + ("\n" if body else ""), encoding="utf-8", newline="\n")


def _find(rows: list[dict], entry_id: str) -> dict | None:
    for r in rows:
        if r.get("id") == entry_id:
            return r
    # allow unambiguous prefix match for convenience
    matches = [r for r in rows if str(r.get("id", "")).startswith(entry_id)]
    return matches[0] if len(matches) == 1 else None


# --------------------------------------------------------------------------- #
# Entry markdown files
# --------------------------------------------------------------------------- #
def _entry_path(entry_id: str) -> Path:
    _, _, entries, _ = _paths()
    return entries / f"{entry_id}.md"


def _write_entry_md(meta: dict, body: str) -> None:
    path = _entry_path(meta["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    fm_keys = [
        "id", "created", "updated", "source", "type", "status",
        "title", "tags", "git_base", "git_ref", "patch", "diff_hash", "supersedes",
    ]
    lines = ["---"]
    for k in fm_keys:
        v = meta.get(k)
        if v in (None, "", []):
            continue
        if k == "tags" and isinstance(v, list):
            v = ", ".join(v)
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
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
README = """# Praxis memory ledger

This directory is the project's **memory** — a versioned record of the plans,
decisions, implementations and artifacts produced while working with the praxis
SDLC experts. It is committed to git on purpose, so the record survives across
sessions and machines.

- `ledger.jsonl` — the index (one entry per line). Don't hand-edit; use the CLI.
- `entries/<id>.md` — the full content of each entry.
- `patches/<id>.patch` — a reverse-appliable diff for implementation entries,
  used by `rollback`.

Manage it with the `memory` skill or the `/memory` command, e.g.:

    /memory list pending
    /memory accept <id>
    /memory rollback <id>

Each entry moves through: **pending → accepted | rejected | rolled-back**.
"""


def _ensure_structure() -> Path:
    """Create the ledger directory structure if missing. Silent and idempotent."""
    base, ledger, entries, patches = _paths()
    base.mkdir(parents=True, exist_ok=True)
    entries.mkdir(parents=True, exist_ok=True)
    patches.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        ledger.write_text("", encoding="utf-8")
    readme = base / "README.md"
    if not readme.exists():
        readme.write_text(README, encoding="utf-8", newline="\n")
    return base


def cmd_init(_args) -> int:
    base = _ensure_structure()
    print(f"memory ledger ready at {base}")
    return 0


# --------------------------------------------------------------------------- #
# log
# --------------------------------------------------------------------------- #
def _read_body_arg(args) -> str:
    if getattr(args, "body_file", None):
        return Path(args.body_file).read_text(encoding="utf-8")
    if getattr(args, "body", None) == "-":
        return sys.stdin.read()
    return getattr(args, "body", None) or ""


def _add_entry(meta: dict, body: str) -> None:
    rows = _read_index()
    if meta.get("supersedes"):
        prev = _find(rows, meta["supersedes"])
        if prev and prev.get("status") in OPEN_STATUSES:
            prev["status"] = "superseded"
            prev["updated"] = _now()
    rows.append({k: meta.get(k) for k in (
        "id", "created", "updated", "source", "type", "status",
        "title", "tags", "diff_hash", "supersedes",
    ) if meta.get(k) not in (None, "", [])})
    _write_index(rows)
    _write_entry_md(meta, body)


def cmd_log(args) -> int:
    _ensure_structure()
    if args.type not in TYPES:
        print(f"error: --type must be one of {', '.join(TYPES)}", file=sys.stderr)
        return 2
    entry_id = _new_id()
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    meta = {
        "id": entry_id,
        "created": _now(),
        "updated": _now(),
        "source": args.source or "manual",
        "type": args.type,
        "status": args.status,
        "title": args.title,
        "tags": tags,
        "supersedes": args.supersedes,
    }
    _add_entry(meta, _read_body_arg(args))
    print(entry_id)
    return 0


# --------------------------------------------------------------------------- #
# snapshot — capture the current diff as a rollback-able implementation entry
# --------------------------------------------------------------------------- #
def cmd_snapshot(args) -> int:
    _ensure_structure()
    base_ref = args.since or "HEAD"
    diff = _git("diff", base_ref).stdout
    if not diff.strip():
        print("snapshot: no changes to capture")
        return 0
    diff_hash = hashlib.sha1(diff.encode("utf-8")).hexdigest()[:12]

    rows = _read_index()
    for r in rows:
        if r.get("diff_hash") == diff_hash and r.get("status") in OPEN_STATUSES:
            print(f"snapshot: already captured as {r['id']} (unchanged diff)")
            return 0

    names = _git("diff", "--name-only", base_ref).stdout.split()
    stat = _git("diff", "--stat", base_ref).stdout.strip()
    base_sha = _git("rev-parse", "--short", base_ref).stdout.strip()

    entry_id = _new_id()
    _, _, _, patches = _paths()
    patch_rel = f"patches/{entry_id}.patch"
    (patches / f"{entry_id}.patch").write_text(diff, encoding="utf-8", newline="\n")

    title = args.title or f"Working changes ({len(names)} file{'s' if len(names) != 1 else ''})"
    body = (
        f"Automatic snapshot of the diff against `{base_ref}` ({base_sha}).\n\n"
        f"**Files touched:**\n\n"
        + "\n".join(f"- `{n}`" for n in names)
        + f"\n\n```\n{stat}\n```\n\n"
        f"Roll back with `/memory rollback {entry_id}` "
        f"(applies `{patch_rel}` in reverse)."
    )
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    meta = {
        "id": entry_id,
        "created": _now(),
        "updated": _now(),
        "source": args.source or "auto",
        "type": "implementation",
        "status": args.status,
        "title": title,
        "tags": tags,
        "git_base": base_sha,
        "patch": patch_rel,
        "diff_hash": diff_hash,
    }
    _add_entry(meta, body)
    print(entry_id)
    return 0


# --------------------------------------------------------------------------- #
# list / pending / show / status
# --------------------------------------------------------------------------- #
_ICON = {
    "pending": "○", "accepted": "●", "rejected": "✗",
    "rolled-back": "↩", "superseded": "⊘",
}


def _filtered(args) -> list[dict]:
    rows = _read_index()
    if getattr(args, "status", None):
        rows = [r for r in rows if r.get("status") == args.status]
    if getattr(args, "type", None):
        rows = [r for r in rows if r.get("type") == args.type]
    if getattr(args, "source", None):
        rows = [r for r in rows if r.get("source") == args.source]
    return rows


def cmd_list(args) -> int:
    rows = _filtered(args)
    if not rows:
        print("(no matching entries)")
        return 0
    rows.sort(key=lambda r: r.get("created", ""), reverse=True)
    for r in rows:
        icon = _ICON.get(r.get("status", ""), "?")
        print(
            f"{icon} {r.get('id')}  [{r.get('status')}]  {r.get('type')}"
            f"  {r.get('source')}\n    {r.get('title', '')}"
        )
    return 0


def cmd_pending(args) -> int:
    rows = [r for r in _read_index() if r.get("status") == "pending"]
    rows.sort(key=lambda r: r.get("created", ""), reverse=True)
    if args.brief:
        if not rows:
            return 0
        print(f"[praxis memory] {len(rows)} pending entr"
              f"{'y' if len(rows) == 1 else 'ies'} awaiting accept/reject:")
        for r in rows[:10]:
            print(f"  - {r.get('id')} ({r.get('type')}): {r.get('title', '')}")
        print("  Review with `/memory` (accept, reject, or rollback).")
        return 0
    args.status = "pending"
    args.type = None
    args.source = None
    return cmd_list(args)


def cmd_show(args) -> int:
    rows = _read_index()
    entry = _find(rows, args.id)
    if not entry:
        print(f"error: no entry matching {args.id!r}", file=sys.stderr)
        return 1
    print(_read_entry_body(entry["id"]))
    return 0


def cmd_status(_args) -> int:
    rows = _read_index()
    if not rows:
        print("memory ledger is empty.")
        return 0
    by_status: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for r in rows:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
        by_type[r.get("type", "?")] = by_type.get(r.get("type", "?"), 0) + 1
    print(f"Praxis memory — {len(rows)} entries")
    print("  by status: " + ", ".join(f"{_ICON.get(k, '?')} {k}={v}"
                                       for k, v in sorted(by_status.items())))
    print("  by type:   " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    return 0


# --------------------------------------------------------------------------- #
# accept / reject / rollback
# --------------------------------------------------------------------------- #
def _set_status(entry_id: str, status: str, note: str | None) -> dict | None:
    rows = _read_index()
    entry = _find(rows, entry_id)
    if not entry:
        return None
    now = _now()
    entry["status"] = status
    entry["updated"] = now
    _write_index(rows)

    # rebuild the entry file: index row fields + frontmatter-only fields
    # (git_base / git_ref / patch) recovered from the existing file.
    meta = dict(entry)
    existing = (
        _entry_path(entry["id"]).read_text(encoding="utf-8")
        if _entry_path(entry["id"]).is_file()
        else ""
    )
    for key in ("git_base", "git_ref", "patch"):
        m = re.search(rf"^{key}: (.+)$", existing, re.MULTILINE)
        if m:
            meta[key] = m.group(1).strip()

    footer = f"_{status} on {now}_" + (f" — {note}" if note else "")
    body = _read_entry_body(entry["id"]).rstrip() + f"\n\n---\n\n{footer}\n"
    _write_entry_md(meta, body)
    return entry


def cmd_accept(args) -> int:
    entry = _set_status(args.id, "accepted", args.note)
    if not entry:
        print(f"error: no entry matching {args.id!r}", file=sys.stderr)
        return 1
    print(f"accepted {entry['id']}")
    return 0


def cmd_reject(args) -> int:
    entry = _set_status(args.id, "rejected", args.note)
    if not entry:
        print(f"error: no entry matching {args.id!r}", file=sys.stderr)
        return 1
    print(f"rejected {entry['id']}")
    return 0


def cmd_rollback(args) -> int:
    rows = _read_index()
    entry = _find(rows, args.id)
    if not entry:
        print(f"error: no entry matching {args.id!r}", file=sys.stderr)
        return 1
    existing = _entry_path(entry["id"]).read_text(encoding="utf-8") if _entry_path(entry["id"]).is_file() else ""
    m = re.search(r"^patch: (.+)$", existing, re.MULTILINE)
    if not m:
        print(f"error: {entry['id']} has no recorded patch — nothing to roll back.\n"
              f"Only implementation snapshots can be rolled back automatically.",
              file=sys.stderr)
        return 1
    patch_path = memory_dir() / m.group(1).strip()
    if not patch_path.is_file():
        print(f"error: patch file missing: {patch_path}", file=sys.stderr)
        return 1

    check = _git("apply", "--reverse", "--check", str(patch_path))
    if check.returncode != 0:
        print("error: the recorded diff does not apply cleanly in reverse "
              "(the code has moved on since the snapshot).", file=sys.stderr)
        print(check.stderr.strip(), file=sys.stderr)
        print("Resolve manually, or inspect with: "
              f"git apply --reverse --3way {patch_path}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"dry-run OK: {entry['id']} would roll back cleanly.")
        return 0

    applied = _git("apply", "--reverse", str(patch_path))
    if applied.returncode != 0:
        print("error: reverse apply failed:\n" + applied.stderr, file=sys.stderr)
        return 1
    _set_status(entry["id"], "rolled-back", args.note or "reverted via /memory rollback")
    print(f"rolled back {entry['id']} — the snapshotted changes were reverted in your "
          f"working tree. Review with `git diff` and commit.")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Praxis memory ledger.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create the ledger directory structure.").set_defaults(func=cmd_init)

    lg = sub.add_parser("log", help="Append an entry (plan/decision/artifact/...).")
    lg.add_argument("--type", required=True, help=f"one of: {', '.join(TYPES)}")
    lg.add_argument("--title", required=True)
    lg.add_argument("--source", default="manual", help="command/skill that produced it, e.g. /architect")
    lg.add_argument("--status", default="pending", choices=STATUSES)
    lg.add_argument("--tags", default="")
    lg.add_argument("--body", help="entry body, or '-' to read stdin")
    lg.add_argument("--body-file", help="read the body from a file")
    lg.add_argument("--supersedes", help="id of an entry this replaces")
    lg.set_defaults(func=cmd_log)

    sn = sub.add_parser("snapshot", help="Capture the current diff as a rollback-able implementation entry.")
    sn.add_argument("--source", default="auto")
    sn.add_argument("--title")
    sn.add_argument("--since", help="capture the diff against this ref (default: uncommitted vs HEAD)")
    sn.add_argument("--status", default="pending", choices=STATUSES)
    sn.add_argument("--tags", default="")
    sn.set_defaults(func=cmd_snapshot)

    ls = sub.add_parser("list", help="List entries.")
    ls.add_argument("--status", choices=STATUSES)
    ls.add_argument("--type", choices=TYPES)
    ls.add_argument("--source")
    ls.set_defaults(func=cmd_list)

    pn = sub.add_parser("pending", help="List pending entries.")
    pn.add_argument("--brief", action="store_true", help="compact output for hooks/context")
    pn.set_defaults(func=cmd_pending)

    sh = sub.add_parser("show", help="Print one entry's full content.")
    sh.add_argument("id")
    sh.set_defaults(func=cmd_show)

    sub.add_parser("status", help="Summary dashboard.").set_defaults(func=cmd_status)

    ac = sub.add_parser("accept", help="Mark an entry accepted.")
    ac.add_argument("id")
    ac.add_argument("--note")
    ac.set_defaults(func=cmd_accept)

    rj = sub.add_parser("reject", help="Mark an entry rejected.")
    rj.add_argument("id")
    rj.add_argument("--note")
    rj.set_defaults(func=cmd_reject)

    rb = sub.add_parser("rollback", help="Reverse-apply an implementation snapshot's patch.")
    rb.add_argument("id")
    rb.add_argument("--dry-run", action="store_true")
    rb.add_argument("--note")
    rb.set_defaults(func=cmd_rollback)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
