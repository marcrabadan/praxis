"""Generate SKILLS.md — a catalog of every skill and command in the repo.

Deterministic: reads frontmatter from each .claude/skills/<name>/SKILL.md and
each .claude/commands/<name>.md and renders a stable markdown index. No LLM.

Usage:
    python scripts/build_catalog.py            # write SKILLS.md
    python scripts/build_catalog.py --check     # exit 1 if SKILLS.md is stale

Exit codes:
    0: wrote the catalog, or --check found it up to date
    1: --check found the catalog stale (regenerate and commit)
    2: IO / arguments error
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

FACTORY_DIR = Path(__file__).resolve().parents[1]
CLAUDE_DIR = FACTORY_DIR.parent
REPO_ROOT = CLAUDE_DIR.parent
SKILLS_DIR = CLAUDE_DIR / "skills"
COMMANDS_DIR = CLAUDE_DIR / "commands"
CATALOG_PATH = REPO_ROOT / "SKILLS.md"

sys.path.insert(0, str(FACTORY_DIR / "validators"))
from validate_frontmatter import _read_frontmatter  # noqa: E402


def _truncate(text: str, limit: int = 160) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _skill_rows() -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    if not SKILLS_DIR.is_dir():
        return rows
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm, _ = _read_frontmatter(skill_md)
        name = str(fm.get("name") or skill_md.parent.name)
        version = str(fm.get("version") or "—")
        tier = str(fm.get("tier") or "—")
        description = _truncate(str(fm.get("description") or ""))
        rows.append((name, version, tier, description))
    return rows


def _command_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if not COMMANDS_DIR.is_dir():
        return rows
    for cmd_md in sorted(COMMANDS_DIR.glob("*.md")):
        fm, _ = _read_frontmatter(cmd_md)
        name = "/" + cmd_md.stem
        description = _truncate(str(fm.get("description") or ""))
        rows.append((name, description))
    return rows


def render() -> str:
    lines: list[str] = []
    lines.append("# Skill catalog")
    lines.append("")
    lines.append(
        "Generated index of every skill and command in this repo. "
        "Do not edit by hand — run `make catalog` (or `python .claude/factory/scripts/build_catalog.py`)."
    )
    lines.append("")

    lines.append("## Skills")
    lines.append("")
    lines.append("| Skill | Version | Tier | Description |")
    lines.append("| ----- | ------- | ---- | ----------- |")
    for name, version, tier, description in _skill_rows():
        lines.append(f"| `{name}` | {version} | {tier} | {description} |")
    lines.append("")

    command_rows = _command_rows()
    if command_rows:
        lines.append("## Commands")
        lines.append("")
        lines.append("| Command | Description |")
        lines.append("| ------- | ----------- |")
        for name, description in command_rows:
            lines.append(f"| `{name}` | {description} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the skill catalog (SKILLS.md).")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if SKILLS.md is out of date instead of writing it.",
    )
    args = parser.parse_args()

    content = render()

    if args.check:
        existing = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.is_file() else ""
        if existing != content:
            print("SKILLS.md is stale. Run `make catalog` and commit the result.", file=sys.stderr)
            return 1
        print("SKILLS.md is up to date.")
        return 0

    CATALOG_PATH.write_text(content, encoding="utf-8", newline="\n")
    print(f"Wrote {CATALOG_PATH.relative_to(REPO_ROOT)} ({len(_skill_rows())} skills).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
