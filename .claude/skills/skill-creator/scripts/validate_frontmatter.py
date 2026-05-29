"""Validate the YAML frontmatter of a SKILL.md file.

Deterministic checks only. No LLM involvement.

Usage:
    python validate_frontmatter.py path/to/SKILL.md

Exit codes:
    0: frontmatter is valid
    1: frontmatter is invalid
    2: file unreadable or arguments wrong
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

NAME_PATTERN = re.compile(r"^[a-z0-9-]{1,64}$")
DESCRIPTION_MAX = 1024


def _read_frontmatter(skill_md_path: Path) -> tuple[dict[str, Any], list[str]]:
    """Return (frontmatter_dict, errors). Uses a minimal YAML parser tailored
    to the simple key: value frontmatter we use in this repo. Avoids the
    PyYAML dependency so the validator can run on a vanilla Python install."""
    errors: list[str] = []
    try:
        text = skill_md_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"could not read {skill_md_path}: {exc}"]

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["frontmatter is missing: file does not start with '---'"]

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, ["frontmatter is not closed: no second '---' line found"]

    data: dict[str, Any] = {}
    current_key: str | None = None
    current_buffer: list[str] = []

    def _commit() -> None:
        nonlocal current_key, current_buffer
        if current_key is not None:
            value = "\n".join(current_buffer).strip()
            data[current_key] = _coerce(value)
        current_key = None
        current_buffer = []

    for raw in lines[1:end_idx]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith(" ") and ":" in raw:
            _commit()
            key, _, value = raw.partition(":")
            current_key = key.strip()
            value = value.strip()
            if value == ">-" or value == ">" or value == "|":
                current_buffer = []
            elif value:
                current_buffer = [value]
            else:
                current_buffer = []
        else:
            current_buffer.append(raw.strip())
    _commit()

    return data, errors


def _coerce(value: str) -> Any:
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.isdigit():
        try:
            return int(value)
        except ValueError:
            return value
    if (value.startswith("\"") and value.endswith("\"")) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def validate(skill_md_path: Path) -> tuple[bool, dict[str, Any]]:
    data, read_errors = _read_frontmatter(skill_md_path)
    errors = list(read_errors)
    warnings: list[str] = []

    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append("frontmatter is missing 'name'")
    elif not NAME_PATTERN.match(name):
        errors.append(
            f"'name' must match ^[a-z0-9-]{{1,64}}$ (got: {name!r})"
        )

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("frontmatter is missing 'description'")
    else:
        if len(description) > DESCRIPTION_MAX:
            errors.append(
                f"'description' is {len(description)} chars (max {DESCRIPTION_MAX})"
            )
        lowered = description.lower()
        if "use when" not in lowered and "trigger" not in lowered:
            warnings.append(
                "'description' does not mention 'use when' or 'trigger'; "
                "consider making the triggering context explicit"
            )

    tier = data.get("tier")
    if tier is not None:
        if not isinstance(tier, int) or not (1 <= tier <= 5):
            errors.append(f"'tier' must be an integer 1-5 (got: {tier!r})")

    report = {
        "path": str(skill_md_path),
        "frontmatter": data,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }
    return not errors, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a SKILL.md frontmatter block."
    )
    parser.add_argument("path", help="Path to SKILL.md")
    parser.add_argument(
        "--json", action="store_true", help="Emit report as JSON on stdout."
    )
    args = parser.parse_args()

    skill_md = Path(args.path)
    if not skill_md.is_file():
        print(f"error: file not found: {skill_md}", file=sys.stderr)
        return 2

    ok, report = validate(skill_md)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if ok:
            print(f"OK: {skill_md}")
        else:
            print(f"FAIL: {skill_md}", file=sys.stderr)
        for err in report["errors"]:
            print(f"  error: {err}", file=sys.stderr)
        for warn in report["warnings"]:
            print(f"  warn:  {warn}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
