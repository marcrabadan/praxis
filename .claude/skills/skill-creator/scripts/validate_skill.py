"""Validate a skill folder.

Deterministic checks only. No LLM involvement. Runs the frontmatter validator
and additionally checks folder shape against the declared tier (or against
basic requirements if no tier is declared).

Usage:
    python validate_skill.py path/to/skill-folder
    python validate_skill.py path/to/skill-folder --tier 3
    python validate_skill.py path/to/skill-folder --json

Exit codes:
    0: skill is valid
    1: skill is invalid
    2: arguments wrong or path unreadable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from validate_frontmatter import validate as validate_frontmatter  # noqa: E402


TIER_EXPECTATIONS: dict[int, dict[str, list[str]]] = {
    1: {
        "required_files": ["SKILL.md"],
        "allowed_dirs": [],
    },
    2: {
        "required_files": ["SKILL.md"],
        "allowed_dirs": ["references"],
    },
    3: {
        "required_files": ["SKILL.md"],
        "allowed_dirs": ["references", "workflows"],
    },
    4: {
        "required_files": ["SKILL.md"],
        "allowed_dirs": ["references", "workflows", "scripts", "evals"],
    },
    5: {
        "required_files": ["SKILL.md"],
        "allowed_dirs": [
            "references",
            "workflows",
            "scripts",
            "evals",
            "agents",
            "assets",
            "reports",
        ],
    },
}


def _strip_inline_code(line: str) -> str:
    """Remove backtick-delimited inline code spans so anti-pattern examples in
    documentation don't trip the link checker."""
    result_parts: list[str] = []
    i = 0
    in_code = False
    while i < len(line):
        ch = line[i]
        if ch == "`":
            in_code = not in_code
            i += 1
            continue
        if not in_code:
            result_parts.append(ch)
        i += 1
    return "".join(result_parts)


def _check_windows_paths(skill_dir: Path) -> list[str]:
    """Flag markdown files that use backslash-style paths inside links.

    Inline code spans (anything between backticks on the same line) are
    ignored so that anti-pattern examples like `[x](path\\file.md)` do not
    trigger the check.
    """
    findings: list[str] = []
    for md_path in skill_dir.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        in_fenced_block = False
        for line_num, raw_line in enumerate(text.splitlines(), start=1):
            stripped = raw_line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fenced_block = not in_fenced_block
                continue
            if in_fenced_block:
                continue
            line = _strip_inline_code(raw_line)
            if "](" not in line:
                continue
            link_target = line.split("](", 1)[1].split(")", 1)[0]
            if "\\" in link_target:
                findings.append(
                    f"{md_path.relative_to(skill_dir)}:{line_num} uses Windows-style backslash in a markdown link"
                )
    return findings


def _validate_eval_files(skill_dir: Path) -> tuple[list[str], list[str]]:
    """Parse any *.json files under evals/ and report parse errors."""
    errors: list[str] = []
    warnings: list[str] = []
    evals_dir = skill_dir / "evals"
    if not evals_dir.is_dir():
        return errors, warnings
    for json_path in evals_dir.glob("*.json"):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"evals/{json_path.name} is not valid JSON: {exc}")
            continue
        if json_path.name == "trigger-evals.json":
            if not isinstance(data, list):
                errors.append(
                    "evals/trigger-evals.json must be a JSON array of {query, should_trigger} objects"
                )
                continue
            has_positive = False
            has_negative = False
            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    errors.append(
                        f"evals/trigger-evals.json[{idx}] is not an object"
                    )
                    continue
                if "query" not in item or "should_trigger" not in item:
                    errors.append(
                        f"evals/trigger-evals.json[{idx}] missing 'query' or 'should_trigger'"
                    )
                    continue
                if item["should_trigger"] is True:
                    has_positive = True
                elif item["should_trigger"] is False:
                    has_negative = True
            if not has_positive or not has_negative:
                warnings.append(
                    "trigger-evals.json should contain both positive and negative cases"
                )
        elif json_path.name == "output-evals.json":
            if not isinstance(data, dict) or "evals" not in data:
                errors.append(
                    "evals/output-evals.json must be an object with an 'evals' array"
                )
    return errors, warnings


def _infer_tier_from_dirs(skill_dir: Path) -> int | None:
    has = {
        "references": (skill_dir / "references").is_dir(),
        "workflows": (skill_dir / "workflows").is_dir(),
        "scripts": (skill_dir / "scripts").is_dir(),
        "evals": (skill_dir / "evals").is_dir(),
        "agents": (skill_dir / "agents").is_dir(),
    }
    if has["agents"]:
        return 5
    if has["scripts"] or has["evals"]:
        return 4
    if has["workflows"]:
        return 3
    if has["references"]:
        return 2
    return 1


def _validate_folder_shape(skill_dir: Path, tier: int) -> list[str]:
    errors: list[str] = []
    expectations = TIER_EXPECTATIONS[tier]
    for required in expectations["required_files"]:
        if not (skill_dir / required).is_file():
            errors.append(f"missing required file: {required}")
    return errors


def validate(skill_dir: Path, declared_tier: int | None = None) -> tuple[bool, dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.is_dir():
        return False, {
            "path": str(skill_dir),
            "errors": [f"not a directory: {skill_dir}"],
            "warnings": [],
            "ok": False,
        }

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, {
            "path": str(skill_dir),
            "errors": ["SKILL.md is missing"],
            "warnings": [],
            "ok": False,
        }

    ok_fm, fm_report = validate_frontmatter(skill_md)
    errors.extend(f"frontmatter: {err}" for err in fm_report["errors"])
    warnings.extend(f"frontmatter: {warn}" for warn in fm_report["warnings"])

    frontmatter = fm_report.get("frontmatter") or {}
    fm_tier = frontmatter.get("tier") if isinstance(frontmatter, dict) else None

    tier = declared_tier or (fm_tier if isinstance(fm_tier, int) else None)
    if tier is None:
        tier = _infer_tier_from_dirs(skill_dir)
    if tier not in TIER_EXPECTATIONS:
        errors.append(f"could not determine tier; got {tier!r}")
        tier = 1

    errors.extend(_validate_folder_shape(skill_dir, tier))

    eval_errors, eval_warnings = _validate_eval_files(skill_dir)
    errors.extend(eval_errors)
    warnings.extend(eval_warnings)

    windows_findings = _check_windows_paths(skill_dir)
    errors.extend(windows_findings)

    report = {
        "path": str(skill_dir),
        "tier": tier,
        "frontmatter": frontmatter,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }
    return not errors, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a skill folder structure and frontmatter."
    )
    parser.add_argument("path", help="Path to the skill directory.")
    parser.add_argument(
        "--tier", type=int, choices=[1, 2, 3, 4, 5], help="Declared tier (overrides inferred)."
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report on stdout.")
    args = parser.parse_args()

    skill_dir = Path(args.path)
    ok, report = validate(skill_dir, declared_tier=args.tier)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "OK" if ok else "FAIL"
        print(f"{status}: {skill_dir} (tier {report.get('tier')})")
        for err in report["errors"]:
            print(f"  error: {err}", file=sys.stderr)
        for warn in report["warnings"]:
            print(f"  warn:  {warn}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
