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
GATE_ID = re.compile(r"^G-[a-z0-9-]{1,48}$")
PROJECT_STATUSES = {"active", "paused", "archived"}
SPEC_STATUSES = {"draft", "accepted", "superseded", "done"}
EXPERIENCE_TYPES = {"screen", "flow", "api", "job", "cli", "data", "integration"}
EXPERIENCE_STATUSES = {"draft", "accepted", "superseded"}
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
    "workflow.schema.json",
    "session-state.schema.json",
    "spec.schema.json",
    "experience-contract.schema.json",
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


def _check_project_specs(project_dir: Path, project_id: str, errors: list[str]) -> None:
    """Validate spec folders under a project. Each real spec needs a spec.md with
    valid frontmatter; underscore-prefixed folders (templates) are skipped."""
    specs_dir = project_dir / "specs"
    if not specs_dir.is_dir():
        return
    for spec in sorted(specs_dir.iterdir()):
        if not spec.is_dir() or spec.name.startswith("_") or spec.name.startswith("."):
            continue
        spec_id = spec.name
        label = f"{project_id}/specs/{spec_id}"
        if not SLUG.match(spec_id):
            errors.append(f"{label}: spec folder name is not a valid slug")
        spec_md = spec / "spec.md"
        if not spec_md.is_file():
            errors.append(f"{label}: missing spec.md")
            continue
        data, read_errors = _read_frontmatter(spec_md)
        for err in read_errors:
            errors.append(f"{label}/spec.md: {err}")
        if read_errors:
            continue
        sid = data.get("id")
        if not isinstance(sid, str) or not SLUG.match(sid):
            errors.append(f"{label}/spec.md: 'id' must be a slug (got: {sid!r})")
        elif sid != spec_id:
            errors.append(
                f"{label}/spec.md: frontmatter id {sid!r} does not match folder {spec_id!r}"
            )
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            errors.append(f"{label}/spec.md: missing 'title'")
        proj = data.get("project")
        if proj != project_id:
            errors.append(
                f"{label}/spec.md: 'project' {proj!r} does not match owning project {project_id!r}"
            )
        status = data.get("status")
        if status not in SPEC_STATUSES:
            errors.append(
                f"{label}/spec.md: 'status' must be one of {sorted(SPEC_STATUSES)} (got: {status!r})"
            )

        _check_experience_contracts(spec, spec_id, data, label, errors)


def _check_experience_contracts(
    spec_dir: Path, spec_id: str, frontmatter: dict, label: str, errors: list[str]
) -> None:
    """Validate per-surface experience contracts (schemas/experience-contract.schema.json).

    Two deterministic checks:
      * every experience/*.contract.json present is structurally well-formed; and
      * when the spec frontmatter declares an `experienceInventory`, each listed
        surface has both its markdown and its companion contract (coverage).
    Both are inert for specs that declare no surfaces, so existing specs are
    unaffected.
    """
    exp_dir = spec_dir / "experience"

    # 1. structural validation of any contract present
    if exp_dir.is_dir():
        for contract in sorted(exp_dir.glob("*.contract.json")):
            clabel = f"{label}/experience/{contract.name}"
            try:
                data = json.loads(contract.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{clabel} is not valid JSON: {exc}")
                continue
            if not isinstance(data, dict):
                errors.append(f"{clabel} must be a JSON object")
                continue
            if data.get("contractType") != "experience-contract":
                errors.append(f"{clabel}: 'contractType' must be 'experience-contract'")
            if data.get("spec") != spec_id:
                errors.append(f"{clabel}: 'spec' {data.get('spec')!r} does not match the owning spec {spec_id!r}")
            if not (isinstance(data.get("surface"), str) and SLUG.match(data.get("surface", ""))):
                errors.append(f"{clabel}: 'surface' must be a slug")
            if data.get("experienceType") not in EXPERIENCE_TYPES:
                errors.append(f"{clabel}: 'experienceType' must be one of {sorted(EXPERIENCE_TYPES)}")
            if data.get("status") not in EXPERIENCE_STATUSES:
                errors.append(f"{clabel}: 'status' must be one of {sorted(EXPERIENCE_STATUSES)}")
            files_owned = data.get("filesOwned")
            if not (isinstance(files_owned, list) and files_owned):
                errors.append(f"{clabel}: 'filesOwned' must be a non-empty array (it scopes verification)")
            verification = data.get("verification")
            if not (isinstance(verification, list) and verification):
                errors.append(f"{clabel}: 'verification' must be a non-empty array (an unverifiable surface must not be built)")
            else:
                for v in verification:
                    if not (isinstance(v, dict) and GATE_ID.match(str(v.get("gate", "")))):
                        errors.append(f"{clabel}: each verification entry needs a gate id matching ^G-* (got {v.get('gate') if isinstance(v, dict) else v!r})")

    # 2. coverage when the spec declares its surfaces
    inventory = frontmatter.get("experienceInventory")
    if isinstance(inventory, list):
        for entry in inventory:
            if not isinstance(entry, dict):
                continue
            surface = entry.get("surface")
            if not (isinstance(surface, str) and SLUG.match(surface)):
                errors.append(f"{label}: experienceInventory surface {surface!r} is not a slug")
                continue
            md = exp_dir / f"{surface}.md"
            contract = exp_dir / f"{surface}.contract.json"
            if not md.is_file():
                errors.append(f"{label}: experienceInventory declares surface {surface!r} but experience/{surface}.md is missing")
            if not contract.is_file():
                errors.append(f"{label}: experienceInventory declares surface {surface!r} but experience/{surface}.contract.json is missing")


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
        _check_project_specs(child, project_id, errors)

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


def _check_runtime(root: Path, errors: list[str]) -> None:
    """Validate runtime/session-state.json shape if it is present. Runtime files
    are disposable and usually git-ignored, so absence is fine."""
    state_path = root / "runtime" / "session-state.json"
    if not state_path.is_file():
        return
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"runtime/session-state.json is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append("runtime/session-state.json must be a JSON object")
        return
    sv = data.get("schemaVersion")
    if not isinstance(sv, str) or not SEMVER.match(sv):
        errors.append(
            f"runtime/session-state.json: 'schemaVersion' must be semver (got: {sv!r})"
        )


def _check_workflows(root: Path, errors: list[str], warnings: list[str]) -> None:
    """Validate workflow manifests: the registry, each manifest's shape, and
    registry<->disk agreement. Workflows are optional; absence is fine."""
    workflows_dir = root / "workflows"
    if not workflows_dir.is_dir():
        return

    registry_path = workflows_dir / "registry.json"
    registry_ids: dict[str, str] = {}  # id -> file
    if not registry_path.is_file():
        errors.append("workflows/ exists but workflows/registry.json is missing")
    else:
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"workflows/registry.json is not valid JSON: {exc}")
            registry = None
        if isinstance(registry, dict):
            entries = registry.get("workflows")
            if not isinstance(entries, list):
                errors.append("workflows/registry.json: 'workflows' must be an array")
            else:
                for idx, entry in enumerate(entries):
                    if not isinstance(entry, dict) or "id" not in entry or "file" not in entry:
                        errors.append(
                            f"workflows/registry.json[{idx}] must have 'id' and 'file'"
                        )
                        continue
                    wid, wfile = entry["id"], entry["file"]
                    registry_ids[wid] = wfile
                    if not isinstance(wid, str) or not SLUG.match(wid):
                        errors.append(
                            f"workflows/registry.json: id {wid!r} is not a valid slug"
                        )
                    if not (workflows_dir / str(wfile)).is_file():
                        errors.append(
                            f"workflows/registry.json: file {wfile!r} for {wid!r} does not exist"
                        )
        elif registry is not None:
            errors.append("workflows/registry.json must be a JSON object")

    # Validate each manifest and check it is registered.
    disk_files = sorted(p.name for p in workflows_dir.glob("*.workflow.json"))
    registered_files = set(registry_ids.values())
    for fname in disk_files:
        if fname not in registered_files:
            errors.append(f"workflows/{fname} is not listed in registry.json")
        _check_workflow_manifest(workflows_dir / fname, errors)

    for wid, wfile in registry_ids.items():
        stem = str(wfile).removesuffix(".workflow.json")
        if stem != wid:
            warnings.append(
                f"workflows/registry.json: file {wfile!r} stem does not match id {wid!r}"
            )


def _check_workflow_manifest(path: Path, errors: list[str]) -> None:
    label = f"workflows/{path.name}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{label} must be a JSON object")
        return

    wid = data.get("id")
    if not isinstance(wid, str) or not SLUG.match(wid):
        errors.append(f"{label}: 'id' must be a slug (got: {wid!r})")
    elif path.name != f"{wid}.workflow.json":
        errors.append(f"{label}: id {wid!r} does not match file name")

    if not isinstance(data.get("name"), str) or not data["name"].strip():
        errors.append(f"{label}: missing 'name'")

    steps = data.get("steps")
    if not isinstance(steps, list) or not steps or not all(isinstance(s, str) for s in steps):
        errors.append(f"{label}: 'steps' must be a non-empty array of strings")
        return
    if len(set(steps)) != len(steps):
        errors.append(f"{label}: 'steps' contains duplicates")
    step_set = set(steps)

    for section in ("gates", "artifacts", "validation", "loops"):
        block = data.get(section)
        if block is None:
            continue
        if not isinstance(block, dict):
            errors.append(f"{label}: '{section}' must be an object")
            continue
        for key in block:
            if key not in step_set:
                errors.append(
                    f"{label}: '{section}' references unknown step {key!r}"
                )

    catalog_ids = _check_gate_catalog(label, data.get("gateCatalog"), errors)
    _check_workflow_loops(label, data.get("loops"), step_set, catalog_ids, errors)


def _check_gate_catalog(label: str, catalog: Any, errors: list[str]) -> set[str]:
    """Validate the optional 'gateCatalog' (typed verification gates). Returns the
    set of valid gate ids so callers can check references resolve."""
    if catalog is None:
        return set()
    if not isinstance(catalog, dict):
        errors.append(f"{label}: 'gateCatalog' must be an object")
        return set()
    ids: set[str] = set()
    for gid, spec in catalog.items():
        where = f"{label}: gateCatalog[{gid!r}]"
        if not GATE_ID.match(str(gid)):
            errors.append(f"{where}: gate id must match ^G-[a-z0-9-]+")
            continue
        if not isinstance(spec, dict):
            errors.append(f"{where} must be an object")
            continue
        if not (isinstance(spec.get("description"), str) and spec["description"].strip()):
            errors.append(f"{where}: 'description' is required")
        if not (isinstance(spec.get("passCriteria"), str) and spec["passCriteria"].strip()):
            errors.append(f"{where}: 'passCriteria' is required")
        if "conditional" in spec and not isinstance(spec["conditional"], bool):
            errors.append(f"{where}: 'conditional' must be a boolean")
        ids.add(gid)
    return ids


def _check_workflow_loops(
    label: str, loops: Any, step_set: set[str], catalog_ids: set[str], errors: list[str]
) -> None:
    """Validate the optional 'loops' block (rules/loop-control.md).

    Each looped step must carry a non-empty terminal predicate; the budget and
    patience guards must be positive integers; onContinue must name a real step;
    and any referenced gates must resolve to the gate catalog — a loop with no
    predicate, a dangling back-edge, or a phantom gate defeats the rule.
    """
    if loops is None:
        return
    if not isinstance(loops, dict):
        return  # already reported as "must be an object" above
    for step, spec in loops.items():
        where = f"{label}: loops[{step!r}]"
        if not isinstance(spec, dict):
            errors.append(f"{where} must be an object")
            continue
        predicate = spec.get("predicate")
        if (
            not isinstance(predicate, list)
            or not predicate
            or not all(isinstance(c, str) and c.strip() for c in predicate)
        ):
            errors.append(
                f"{where}: 'predicate' must be a non-empty array of strings "
                "(a step with no predicate could loop forever)"
            )
        for guard in ("maxIterations", "patience"):
            if guard in spec and (not isinstance(spec[guard], int) or isinstance(spec[guard], bool) or spec[guard] < 1):
                errors.append(f"{where}: '{guard}' must be an integer >= 1")
        cont = spec.get("onContinue")
        if cont is not None and cont not in step_set:
            errors.append(f"{where}: 'onContinue' references unknown step {cont!r}")
        for g in spec.get("gates", []) or []:
            if catalog_ids and g not in catalog_ids:
                errors.append(f"{where}: gate {g!r} is not defined in gateCatalog")


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


def _looks_like_harness(path: Path) -> bool:
    """A directory is a harness if it carries the canonical harness layers."""
    return (
        path.is_dir()
        and (path / "rules").is_dir()
        and (path / "projects").is_dir()
        and (path / "schemas").is_dir()
    )


def _check_config(config_path: Path, fallback_harness_root: Path | None, errors: list[str]) -> None:
    if not config_path.is_file():
        errors.append(f"config not found: {config_path}")
        return
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{config_path} is not valid JSON: {exc}")
        return

    # When the config lives at a real <repo>/.praxis/config.json, resolve the
    # harnessRoot it declares (relative to the consuming repo) and verify it
    # points at an actual harness — an unknown harness root is a hard block.
    # Use that resolved harness for the central-mode project check; fall back to
    # the invocation root for configs not located in a .praxis/ directory.
    harness_root = fallback_harness_root
    if isinstance(data, dict) and config_path.resolve().parent.name == ".praxis":
        hr = data.get("harnessRoot")
        if isinstance(hr, str) and hr:
            repo_root = config_path.resolve().parent.parent
            candidate = (repo_root / hr).resolve()
            if _looks_like_harness(candidate):
                harness_root = candidate
            else:
                errors.append(
                    f"{config_path}: harnessRoot {hr!r} does not resolve to an existing "
                    f"harness (looked at {candidate}) — unknown harness root is a hard block"
                )
                harness_root = None

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
    _check_workflows(root, errors, warnings)
    _check_runtime(root, errors)
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
