"""Praxis task linter — deterministic anti-drift for a tasks.md.

A task that does not name what it may **not** do, what **proves** it, and the
**only files** it may touch is an invitation to drift. This linter enforces that
every task in a feature's `tasks/tasks.md` carries the anti-drift fields:

    - Forbidden:  explicit constraints (don't rename routes, don't substitute a
                  named dependency, don't hardcode contract tokens, ...)
    - Gate:       the G-* gate id(s) from the workflow gate catalog that prove it
    - Output:     the only files/artifacts this task may create or edit

It also checks that each per-surface group declares `files-owned` (the verifier's
scope, mirroring the surface's experience contract).

Deterministic, stdlib-only. Advisory — like validate_traceability, it is a lint
you run on demand (`make check-tasks FILE=...`), not a blocking harness gate, so
specs that predate the structured format are not broken by it.

Usage:
    python check_tasks.py <path/to/tasks.md> [--require Forbidden,Gate,Output]

Exit codes:
    0: every task carries the required fields (and groups declare files-owned)
    1: one or more tasks are missing required fields
    2: arguments wrong / file unreadable
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A task line: "- [ ] T001 [scope] description" (optionally "[P]" before scope).
TASK_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*(T\d+)\b(.*)$")
# A field sub-bullet: "  - Forbidden: ..." -> captures the label.
FIELD_RE = re.compile(r"^\s+[-*]\s*([A-Za-z][A-Za-z /-]*?)\s*:")
# A surface group heading: "### Surface: <slug>"
SURFACE_RE = re.compile(r"^#{2,6}\s+Surface:\s*(\S+)", re.IGNORECASE)
# A "files-owned" declaration anywhere in a group (label form or heading form).
FILES_OWNED_RE = re.compile(r"^\s*[-*#> ]*\s*files-owned\b", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s")

DEFAULT_REQUIRED = ("forbidden", "gate", "output")


def _parse_tasks(lines: list[str]) -> list[dict]:
    """Return one record per task: {id, line_no, desc, fields:set[str]}."""
    tasks: list[dict] = []
    current: dict | None = None
    for i, raw in enumerate(lines, start=1):
        m = TASK_RE.match(raw)
        if m:
            current = {"id": m.group(1), "line_no": i,
                       "desc": m.group(2).strip(), "fields": set()}
            tasks.append(current)
            continue
        if current is not None:
            if TASK_RE.match(raw) or HEADING_RE.match(raw):
                current = None
                continue
            fm = FIELD_RE.match(raw)
            if fm:
                current["fields"].add(fm.group(1).strip().lower())
    return tasks


def _surface_groups_missing_files_owned(lines: list[str]) -> list[str]:
    """Surface group slugs that never declare files-owned before the next group."""
    missing: list[str] = []
    current_slug: str | None = None
    has_files_owned = False

    def _close() -> None:
        nonlocal current_slug, has_files_owned
        if current_slug is not None and not has_files_owned:
            missing.append(current_slug)

    for raw in lines:
        sm = SURFACE_RE.match(raw)
        if sm:
            _close()
            current_slug = sm.group(1).strip("`")
            has_files_owned = False
            continue
        if current_slug is not None and FILES_OWNED_RE.match(raw):
            has_files_owned = True
    _close()
    return missing


def lint(path: Path, required: tuple[str, ...]) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines)."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return 2, [f"error: cannot read {path}: {exc}"]

    tasks = _parse_tasks(lines)
    report: list[str] = []
    if not tasks:
        return 2, [f"error: no tasks (lines like '- [ ] T001 [scope] ...') found in {path}"]

    offenders = 0
    for t in tasks:
        missing = [r for r in required if r not in t["fields"]]
        if missing:
            offenders += 1
            pretty = ", ".join(m.capitalize() for m in missing)
            report.append(f"  {path}:{t['line_no']}  {t['id']} — missing: {pretty}")

    group_misses = _surface_groups_missing_files_owned(lines)
    for slug in group_misses:
        report.append(f"  surface group '{slug}' does not declare files-owned")

    n = len(tasks)
    if offenders or group_misses:
        head = (f"{offenders}/{n} task(s) missing required fields"
                + (f"; {len(group_misses)} surface group(s) missing files-owned"
                   if group_misses else "")
                + f" (required per task: {', '.join(r.capitalize() for r in required)}):")
        return 1, [head, *report]
    return 0, [f"OK: {n} task(s), each carries {', '.join(r.capitalize() for r in required)}."]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lint a tasks.md for per-task anti-drift fields.")
    p.add_argument("path", help="path to tasks.md")
    p.add_argument("--require", default=",".join(DEFAULT_REQUIRED),
                   help=f"comma-separated required field labels (default: {','.join(DEFAULT_REQUIRED)})")
    args = p.parse_args(argv)
    required = tuple(r.strip().lower() for r in args.require.split(",") if r.strip())
    code, report = lint(Path(args.path), required)
    for line in report:
        print(line, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
