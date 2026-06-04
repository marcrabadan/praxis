"""Validate harness state — project memory and adapter config shape.

Deterministic checks only. No LLM involvement. This is separate from
validate_skill.py (which checks skill folders); this validator checks the
harness-mode layer: the project registry, project-memory folders, the harness
schemas, and (optionally) a consuming repo's .praxis/config.json.

Usage:
    python tools/validate_harness.py                 # validate this harness
    python tools/validate_harness.py --root .        # explicit harness root
    python tools/validate_harness.py --config path/to/.praxis/config.json
    python tools/validate_harness.py --json

Exit codes:
    0: harness state is valid
    1: harness state is invalid
    2: arguments wrong or path unreadable
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Reuse the repo's dependency-free frontmatter parser.
_FACTORY_VALIDATORS = (
    Path(__file__).resolve().parent.parent / ".claude" / "factory" / "validators"
)
sys.path.insert(0, str(_FACTORY_VALIDATORS))
from validate_frontmatter import _read_frontmatter  # noqa: E402

SLUG = re.compile(r"^[a-z0-9-]{1,64}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
PROJECT_STATUSES = {"active", "paused", "archived"}
CONFIG_MODES = {"local", "central"}

# Files every project folder (and the template) must contain.
REQUIRED_PROJECT_FILES = [
    "PROJECT.md",
    "linked-repos.md",
    "memory/current-state.md",
    "memory/open-questions.md",
]

REQUIRED_SCHEMAS = [
    "project.schema.json",
    "praxis-config.schema.json",
]


def _check_schemas(root: Path, errors: list[str]) -> None:
    schemas_dir = root / "schemas"
    if not schemas_dir.is_dir():
        errors.append("missing schemas/ directory")
        return
    for name in REQUIRED_SCHEMAS:
        path = schemas_dir / name
        if not path.is_file():
            errors.append(f"missing schema: schemas/{name}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"schemas/{name} is not valid JSON: {exc}")


def _project_required_files(project_dir: Path, label: str, errors: list[str]) -> None:
    for rel in REQUIRED_PROJECT_FILES:
        if not (project_dir / rel).is_file():
            errors.append(f"{label}: missing required file: {rel}")


def _check_project_frontmatter(
    project_dir: Path, project_id: str, errors: list[str]
) -> None:
    project_md = project_dir / "PROJECT.md"
    if not project_md.is_file():
        return  # already reported by required-files check
    data, read_errors = _read_frontmatter(project_md)
    for err in read_errors:
        errors.append(f"{project_id}/PROJECT.md: {err}")
    if read_errors:
        return

    fid = data.get("id")
    if not isinstance(fid, str) or not SLUG.match(fid):
        errors.append(
            f"{project_id}/PROJECT.md: 'id' must match ^[a-z0-9-]{{1,64}}$ (got: {fid!r})"
        )
    elif fid != project_id:
        errors.append(
            f"{project_id}/PROJECT.md: frontmatter id {fid!r} does not match folder name {project_id!r}"
        )

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{project_id}/PROJECT.md: missing 'name'")

    status = data.get("status")
    if status not in PROJECT_STATUSES:
        errors.append(
            f"{project_id}/PROJECT.md: 'status' must be one of {sorted(PROJECT_STATUSES)} (got: {status!r})"
        )


def _parse_index_ids(index_path: Path) -> set[str]:
    """Extract project ids from the project-registry table in projects-index.md.

    Reads the first column of each row in the table whose header starts with
    "Project id", and keeps tokens that look like a project id (slug, optionally
    wrapped in backticks). Placeholder rows like `_(none yet)_` and other tables
    (e.g. the status legend) are ignored.
    """
    ids: set[str] = set()
    try:
        text = index_path.read_text(encoding="utf-8")
    except OSError:
        return ids
    in_registry = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_registry = False  # left the table
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0].strip().strip("`")
        if first.lower() == "project id":
            in_registry = True
            continue
        if set(first) <= {"-", ":"} or first == "":  # separator / empty
            continue
        if in_registry and SLUG.match(first):
            ids.add(first)
    return ids


def _check_projects(root: Path, errors: list[str], warnings: list[str]) -> None:
    projects_dir = root / "projects"
    if not projects_dir.is_dir():
        errors.append("missing projects/ directory")
        return

    index_path = projects_dir / "projects-index.md"
    if not index_path.is_file():
        errors.append("missing projects/projects-index.md")

    template_dir = projects_dir / "_template"
    if not template_dir.is_dir():
        errors.append("missing projects/_template/ scaffold")
    else:
        _project_required_files(template_dir, "_template", errors)

    # Real projects: every non-underscore subdirectory.
    disk_ids: set[str] = set()
    for child in sorted(projects_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("_") or child.name.startswith("."):
            continue
        project_id = child.name
        disk_ids.add(project_id)
        if not SLUG.match(project_id):
            errors.append(
                f"project folder {project_id!r} is not a valid id (^[a-z0-9-]{{1,64}}$)"
            )
        _project_required_files(child, project_id, errors)
        _check_project_frontmatter(child, project_id, errors)

    if index_path.is_file():
        index_ids = _parse_index_ids(index_path)
        for missing in sorted(disk_ids - index_ids):
            errors.append(
                f"project {missing!r} exists on disk but is not listed in projects-index.md"
            )
        for ghost in sorted(index_ids - disk_ids):
            errors.append(
                f"project {ghost!r} is listed in projects-index.md but has no folder under projects/"
            )

    if not disk_ids:
        warnings.append(
            "no projects defined yet (only _template/). Pilot one project to exercise harness mode."
        )


def _validate_config_data(
    data: Any, label: str, harness_root: Path | None, errors: list[str]
) -> None:
    if not isinstance(data, dict):
        errors.append(f"{label}: config must be a JSON object")
        return

    sv = data.get("schemaVersion")
    if not isinstance(sv, str) or not SEMVER.match(sv):
        errors.append(f"{label}: 'schemaVersion' must be semver (got: {sv!r})")

    harness = data.get("harnessRoot")
    if not isinstance(harness, str) or not harness:
        errors.append(f"{label}: 'harnessRoot' is required and must be a non-empty string")

    project_id = data.get("projectId")
    if not isinstance(project_id, str) or not SLUG.match(project_id):
        errors.append(
            f"{label}: 'projectId' must match ^[a-z0-9-]{{1,64}}$ (got: {project_id!r}) — "
            "unresolvable project id is a stop condition"
        )

    mode = data.get("mode")
    if mode is not None and mode not in CONFIG_MODES:
        errors.append(
            f"{label}: 'mode' must be one of {sorted(CONFIG_MODES)} (got: {mode!r})"
        )

    # If we know the harness root, check the project actually resolves there —
    # but only in explicit central mode. Local mode (the default, including an
    # omitted mode) keeps memory in the product repo, so there is nothing to
    # resolve against the harness.
    if (
        harness_root is not None
        and isinstance(project_id, str)
        and SLUG.match(project_id)
        and mode == "central"
    ):
        project_dir = harness_root / "projects" / project_id
        if not project_dir.is_dir():
            errors.append(
                f"{label}: projectId {project_id!r} does not resolve to projects/{project_id}/ in the harness"
            )


def _check_config(config_path: Path, harness_root: Path | None, errors: list[str]) -> None:
    if not config_path.is_file():
        errors.append(f"config not found: {config_path}")
        return
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{config_path} is not valid JSON: {exc}")
        return
    _validate_config_data(data, str(config_path), harness_root, errors)


def validate(root: Path, config: Path | None = None) -> tuple[bool, dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        return False, {
            "root": str(root),
            "errors": [f"not a directory: {root}"],
            "warnings": [],
            "ok": False,
        }

    _check_schemas(root, errors)
    _check_projects(root, errors, warnings)
    if config is not None:
        _check_config(config, root, errors)

    report = {
        "root": str(root),
        "config": str(config) if config else None,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }
    return not errors, report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate harness state (project memory + adapter config)."
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Path to the harness root (default: repo root containing this tool).",
    )
    parser.add_argument(
        "--config",
        help="Optional path to a consuming repo's .praxis/config.json to validate.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report on stdout.")
    args = parser.parse_args()

    root = Path(args.root)
    config = Path(args.config) if args.config else None
    ok, report = validate(root, config=config)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "OK" if ok else "FAIL"
        print(f"{status}: harness at {root}")
        for err in report["errors"]:
            print(f"  error: {err}", file=sys.stderr)
        for warn in report["warnings"]:
            print(f"  warn:  {warn}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
