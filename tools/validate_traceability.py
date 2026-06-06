"""Validate traceability links across a project's lifecycle artifacts.

Deterministic, dependency-free, and **advisory** by default. It implements the
convention in rules/traceability.md: every artifact carries a typed id
(e.g. SPEC-001, BUG-003) and links to its neighbours via `source:` / `traces:`.
This tool collects the ids a project declares and checks that the ids referenced
by `source:` / `traces:` actually resolve to a declared id.

It scans real projects only (folders under projects/ that are not underscore- or
dot-prefixed). Template folders are skipped, so the `<NNN>` placeholders in the
scaffolds are never flagged.

Usage:
    python tools/validate_traceability.py            # advisory: always exit 0
    python tools/validate_traceability.py --strict   # exit 1 on dangling refs
    python tools/validate_traceability.py --json

Exit codes:
    0: ok (or advisory mode with only warnings)
    1: dangling references found (only in --strict)
    2: arguments wrong or path unreadable
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Typed id, e.g. SPEC-001, BUG-12, ADR-003. Numbers are 1+ digits.
ID_RE = re.compile(r"\b([A-Z]{2,6}-\d{1,6})\b")
# A declaration line, e.g. "This spec id: `SPEC-001`" or "id: SPEC-001".
DECL_RE = re.compile(r"id[^\n:]*:\s*`?([A-Z]{2,6}-\d{1,6})`?", re.IGNORECASE)
# A link token, e.g. "source:SPEC-001" or "traces: BUG-003".
LINK_RE = re.compile(r"\b(source|traces)\s*:\s*`?([A-Z]{2,6}-\d{1,6})`?", re.IGNORECASE)


def _scan_project(project_dir: Path) -> tuple[set[str], list[tuple[str, str, str]]]:
    """Return (declared ids, [(file, kind, referenced id)])."""
    declared: set[str] = set()
    links: list[tuple[str, str, str]] = []
    for md in project_dir.rglob("*.md"):
        # Skip template scaffolds anywhere in the path.
        if any(part.startswith("_") or part.startswith(".") for part in md.parts):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in DECL_RE.finditer(text):
            declared.add(m.group(1).upper())
        for m in LINK_RE.finditer(text):
            links.append((str(md), m.group(1).lower(), m.group(2).upper()))
    return declared, links


def validate(root: Path) -> tuple[bool, dict]:
    projects_dir = root / "projects"
    warnings: list[str] = []
    dangling: list[str] = []
    scanned = 0
    if not projects_dir.is_dir():
        return True, {"scanned": 0, "dangling": [], "warnings": ["no projects/ directory"]}

    for child in sorted(projects_dir.iterdir()):
        if not child.is_dir() or child.name.startswith(("_", ".")):
            continue
        scanned += 1
        declared, links = _scan_project(child)
        for fpath, kind, ref in links:
            if ref not in declared:
                dangling.append(f"{fpath}: {kind}:{ref} does not resolve to a declared id in {child.name}")

    if scanned == 0:
        warnings.append("no real projects yet — nothing to trace (only _template/).")

    ok = not dangling
    return ok, {"scanned": scanned, "dangling": dangling, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate traceability links (advisory).")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--strict", action="store_true", help="Exit 1 on dangling references.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    ok, report = validate(root)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "OK" if ok else ("FAIL" if args.strict else "WARN")
        print(f"{status}: traceability scan of {report['scanned']} project(s) at {root}")
        for d in report["dangling"]:
            print(f"  dangling: {d}", file=sys.stderr)
        for w in report["warnings"]:
            print(f"  note:  {w}", file=sys.stderr)

    if not ok and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
