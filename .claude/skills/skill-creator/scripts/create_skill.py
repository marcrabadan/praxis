"""Deterministic skill scaffolder.

Reads a `skill-brief.md` plus a tier (1-5) and copies the matching template
from `templates/tier-N-*/` into the output directory, substituting placeholders.

Determinism contract: given the same brief + tier + name + out, the script
produces byte-identical output on every run. No timestamps, no random IDs.

Usage:
    python create_skill.py \
        --brief dist/my-skill/skill-brief.md \
        --tier 3 \
        --name my-skill \
        --out dist/my-skill

Exit codes:
    0: success
    1: validation failure (e.g. tier mismatch, invalid name)
    2: argument / IO error
    3: target directory exists and is non-empty (use --force to override)
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

CLAUDE_DIR = Path(__file__).resolve().parents[3]
TEMPLATES_DIR = CLAUDE_DIR / "factory" / "templates"

NAME_PATTERN = re.compile(r"^[a-z0-9-]{1,64}$")

TIER_FOLDERS = {
    1: "tier-1-basic-skill",
    2: "tier-2-knowledge-skill",
    3: "tier-3-workflow-skill",
    4: "tier-4-implementation-skill",
    5: "tier-5-core-skill",
}


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:64]


def _title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def _parse_brief(brief_path: Path) -> dict[str, str]:
    """Read a skill-brief.md and extract simple fields.

    The brief uses YAML-like frontmatter followed by `## Section` blocks. This
    parser is intentionally minimal: it pulls the frontmatter scalars and the
    first non-empty paragraph after the `## Purpose` section as the purpose.
    """
    result: dict[str, str] = {}
    if not brief_path.is_file():
        return result

    text = brief_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                for fm_line in lines[1:idx]:
                    if ":" in fm_line:
                        key, _, value = fm_line.partition(":")
                        result[key.strip()] = value.strip()
                break

    purpose_lines: list[str] = []
    in_purpose = False
    for line in lines:
        if line.strip().lower().startswith("## purpose"):
            in_purpose = True
            continue
        if in_purpose:
            if line.startswith("## "):
                break
            if line.strip():
                purpose_lines.append(line.strip())
    if purpose_lines:
        result["purpose"] = " ".join(purpose_lines)

    return result


def _substitute(text: str, substitutions: dict[str, str]) -> str:
    for key, value in substitutions.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def _copy_template(src: Path, dst: Path, substitutions: dict[str, str]) -> list[Path]:
    """Copy the template tree into dst, substituting placeholders in text files.

    Returns the list of files written (relative to dst).
    """
    written: list[Path] = []
    text_suffixes = {".md", ".json", ".py", ".yaml", ".yml", ".txt"}

    for source_path in sorted(src.rglob("*")):
        if source_path.is_dir():
            continue
        rel = source_path.relative_to(src)
        target_path = dst / rel
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if source_path.suffix.lower() in text_suffixes:
            content = source_path.read_text(encoding="utf-8")
            content = _substitute(content, substitutions)
            target_path.write_text(content, encoding="utf-8", newline="\n")
        else:
            shutil.copy2(source_path, target_path)
        written.append(rel)
    return written


def _is_dir_non_empty(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_file():
        return True
    return any(path.iterdir())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministically scaffold a skill from a brief + tier."
    )
    parser.add_argument(
        "--brief",
        type=Path,
        help="Path to the skill-brief.md. Optional; values from the brief override CLI flags.",
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Tier (1-5). Required if not present in brief frontmatter.",
    )
    parser.add_argument(
        "--name",
        help="Skill slug, lowercase hyphenated. Required if not in brief frontmatter.",
    )
    parser.add_argument(
        "--description",
        help="Initial description. Defaults to a placeholder if omitted.",
    )
    parser.add_argument(
        "--purpose",
        help="One-line purpose. Defaults to value from the brief or a placeholder.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory for the produced skill folder.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output directory if it is non-empty.",
    )
    args = parser.parse_args()

    brief_data = _parse_brief(args.brief) if args.brief else {}

    name = args.name or brief_data.get("name")
    if not name:
        print("error: --name is required (and not in brief frontmatter)", file=sys.stderr)
        return 2
    if not NAME_PATTERN.match(name):
        print(
            f"error: name {name!r} must match ^[a-z0-9-]{{1,64}}$",
            file=sys.stderr,
        )
        return 1

    tier_value = args.tier
    if tier_value is None and "tier" in brief_data:
        try:
            tier_value = int(brief_data["tier"])
        except ValueError:
            print(
                f"error: brief tier value {brief_data['tier']!r} is not an integer",
                file=sys.stderr,
            )
            return 1
    if tier_value not in TIER_FOLDERS:
        print(
            f"error: --tier must be 1-5 (got {tier_value!r})",
            file=sys.stderr,
        )
        return 1

    template_dir = TEMPLATES_DIR / TIER_FOLDERS[tier_value]
    if not template_dir.is_dir():
        print(f"error: template not found: {template_dir}", file=sys.stderr)
        return 2

    out_dir = args.out
    if _is_dir_non_empty(out_dir) and not args.force:
        print(
            f"error: {out_dir} exists and is non-empty (use --force to overwrite)",
            file=sys.stderr,
        )
        return 3

    out_dir.mkdir(parents=True, exist_ok=True)

    title = brief_data.get("title") or _title_from_slug(name)
    description = args.description or (
        f"TODO: write a trigger-rich description for {name}. "
        "See .claude/skills/skill-creator/references/description-writing.md."
    )
    purpose = args.purpose or brief_data.get("purpose") or (
        f"{title}: TODO replace this with the one-line purpose from the brief."
    )

    substitutions = {
        "NAME": name,
        "TITLE": title,
        "DESCRIPTION": description,
        "PURPOSE": purpose,
        "TIER": str(tier_value),
    }

    written = _copy_template(template_dir, out_dir, substitutions)

    if args.brief and args.brief.is_file() and args.brief.resolve() != (out_dir / "skill-brief.md").resolve():
        target_brief = out_dir / "skill-brief.md"
        target_brief.write_text(
            args.brief.read_text(encoding="utf-8"),
            encoding="utf-8",
            newline="\n",
        )

    print(f"Scaffolded {name} (tier {tier_value}) at {out_dir}")
    for rel in written:
        print(f"  + {rel}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
