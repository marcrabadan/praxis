"""Ensure the repo is in praxis harness mode — auto-bootstrap if it is not.

Harness mode is praxis's **default and only** operating mode. There is no
opt-in: any repo praxis runs in is a harness repo. This tool makes that true
deterministically. It is **idempotent** — safe to run at the start of every
command:

  - If `.praxis/config.json` already exists and resolves a project, it does
    nothing and reports "already initialized".
  - Otherwise it bootstraps the minimum a project needs and writes the config,
    deriving the project id from the repo folder name.

Two shapes, chosen automatically:

  - **The harness repo itself** (praxis — it carries `rules/source-of-truth.md`
    and `workflows/registry.json`): `mode: central`, `harnessRoot: "."`, the
    project lives under `projects/<id>/`, and a row is added to
    `projects/projects-index.md`.
  - **A consuming repo** (anything else): `mode: local`, project memory lives in
    the repo under `.praxis/project/`, and nothing is written into the harness.

Deterministic, stdlib-only. Same repo state -> same files.

Usage:
    python tools/ensure_harness.py                 # bootstrap ./ if needed
    python tools/ensure_harness.py --root ../app   # bootstrap another repo
    python tools/ensure_harness.py --check         # exit 1 if not initialized
    python tools/ensure_harness.py --harness-root ../praxis   # consumer override

Exit codes:
    0: harness is initialized (already, or just bootstrapped)
    1: --check found it uninitialized
    2: arguments / environment wrong
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9-]{1,64}$")
SCHEMA_VERSION = "1.0.0"


def slugify(name: str) -> str:
    """Turn a repo folder name into a valid project-id slug."""
    s = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return (s or "project")[:64]


def titleize(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-")) or "Project"


def git_root(start: Path) -> Path:
    """The git toplevel for `start`, or `start` itself if not a git repo."""
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return start.resolve()


def is_harness_repo(root: Path) -> bool:
    """A repo is the harness itself if it carries the harness spine."""
    return (root / "rules" / "source-of-truth.md").is_file() and (
        root / "workflows" / "registry.json"
    ).is_file()


def config_resolves(root: Path) -> bool:
    """True when .praxis/config.json exists, parses, and its project resolves."""
    config_path = root / ".praxis" / "config.json"
    if not config_path.is_file():
        return False
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    project_id = config.get("projectId")
    if not isinstance(project_id, str) or not SLUG.match(project_id):
        return False
    mode = config.get("mode", "local")
    if mode == "central":
        return (root / "projects" / project_id / "PROJECT.md").is_file()
    # local: memory lives in the repo
    return (root / ".praxis" / "project" / "PROJECT.md").is_file()


def _project_md(project_id: str) -> str:
    return (
        f"---\nid: {project_id}\nname: {titleize(project_id)}\nstatus: active\n---\n\n"
        f"# Project: {titleize(project_id)}\n\n"
        "Auto-bootstrapped by `tools/ensure_harness.py` because praxis runs in\n"
        "harness mode by default. Replace the placeholders below with the real\n"
        "purpose, authority notes, and linked repos.\n\n"
        "## Purpose\n\nWhat this project is and the outcome it exists to deliver.\n\n"
        "## Authority notes\n\nProject-specific authority that overrides general harness\n"
        "defaults. Authority order: [`../../rules/source-of-truth.md`](../../rules/source-of-truth.md).\n\n"
        "## Where specs live\n\n`specs/` under this project folder, one subfolder per spec.\n"
    )


def _linked_repos_md(project_id: str) -> str:
    return (
        "# Linked Repos\n\nThe product repositories this project spans.\n\n"
        "| Repo | Role | Path / URL | Notes |\n|------|------|-----------|-------|\n"
        f"| `{project_id}` | `service / web / infra` | `.` | auto-bootstrapped |\n"
    )


def _current_state_md() -> str:
    return (
        "# Current State\n\nA living snapshot of where this project is right now.\n\n"
        "## Now\n\n- Bootstrapping — replace this with what is in progress.\n\n"
        "## Recently landed\n\n- _none yet_\n\n"
        "## Active spec\n\n- _none_\n\n## Known constraints\n\n- _none recorded_\n"
    )


def _open_questions_md() -> str:
    return (
        "# Open Questions\n\nUnresolved questions that affect this project. An open\n"
        "question that gates the step in front of you is a stop condition.\n\n"
        "| # | Question | Blocks | Raised | Status |\n"
        "|---|----------|--------|--------|--------|\n"
    )


def _scaffold_project_memory(project_dir: Path, project_id: str) -> list[Path]:
    written: list[Path] = []
    files = {
        project_dir / "PROJECT.md": _project_md(project_id),
        project_dir / "linked-repos.md": _linked_repos_md(project_id),
        project_dir / "memory" / "current-state.md": _current_state_md(),
        project_dir / "memory" / "open-questions.md": _open_questions_md(),
    }
    for path, text in files.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            written.append(path)
    return written


def _add_index_row(root: Path, project_id: str) -> bool:
    """Add a row for project_id to projects-index.md if absent. Returns True if changed."""
    index = root / "projects" / "projects-index.md"
    if not index.is_file():
        return False
    text = index.read_text(encoding="utf-8")
    if f"| `{project_id}` |" in text:
        return False
    lines = text.splitlines()
    row = f"| `{project_id}` | {titleize(project_id)} | active | Auto-bootstrapped by ensure_harness. |"
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*-+", line):  # the table separator row
            lines.insert(i + 1, row)
            break
    else:
        return False
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def build_config(project_id: str, mode: str, harness_root: str) -> dict:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "harnessRoot": harness_root,
        "projectId": project_id,
        "mode": mode,
        "activeSpec": None,
        "generatedBy": "tools/ensure_harness.py",
    }


def ensure(root: Path, harness_root_override: str | None) -> int:
    root = root.resolve()
    if config_resolves(root):
        print(f"harness already initialized at {root}")
        return 0

    project_id = slugify(root.name)
    harness = is_harness_repo(root)
    mode = "central" if harness else "local"
    harness_root = harness_root_override or ("." if harness else "../praxis")

    written: list[Path] = []
    if harness:
        project_dir = root / "projects" / project_id
        written += _scaffold_project_memory(project_dir, project_id)
        if _add_index_row(root, project_id):
            written.append(root / "projects" / "projects-index.md")
    else:
        project_dir = root / ".praxis" / "project"
        written += _scaffold_project_memory(project_dir, project_id)

    config_path = root / ".praxis" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(build_config(project_id, mode, harness_root), indent=2) + "\n",
        encoding="utf-8",
    )
    written.append(config_path)

    print(f"bootstrapped harness for project '{project_id}' (mode: {mode})")
    for p in written:
        print(f"  wrote {p.relative_to(root)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ensure the repo is in harness mode.")
    parser.add_argument("--root", default=None, help="Repo root (default: git toplevel of cwd).")
    parser.add_argument("--harness-root", default=None, help="Override harnessRoot in the written config.")
    parser.add_argument("--check", action="store_true", help="Exit 1 if the harness is not initialized; write nothing.")
    args = parser.parse_args(argv)

    root = Path(args.root) if args.root else git_root(Path.cwd())
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    if args.check:
        if config_resolves(root):
            print(f"harness initialized at {root}")
            return 0
        print(f"harness NOT initialized at {root}", file=sys.stderr)
        return 1

    return ensure(root, args.harness_root)


if __name__ == "__main__":
    raise SystemExit(main())
