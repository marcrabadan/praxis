"""Install a praxis adapter into a consuming repo.

Writes the small pointer files that put a product repo into harness mode:

    <target>/.praxis/config.json        which harness, which project, active spec
    <target>/.praxis/current-spec.md    human-readable pointer to the active spec

Deterministic: same arguments -> same files. No LLM. The generated config is
validated against schemas/praxis-config.schema.json shape before writing.

Usage:
    python tools/install_adapter.py --target ../checkout --project checkout
    python tools/install_adapter.py --target . --project checkout --mode central \
        --harness-root ../praxis --active-spec oauth

Exit codes:
    0: wrote (or, with --check, found up to date)
    1: refused (would overwrite without --force, or --check found drift)
    2: arguments wrong
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9-]{1,64}$")
SCHEMA_VERSION = "1.0.0"


def build_config(args) -> dict:
    config = {
        "schemaVersion": SCHEMA_VERSION,
        "harnessRoot": args.harness_root,
        "projectId": args.project,
        "mode": args.mode,
        "activeSpec": args.active_spec,
        "generatedBy": "tools/install_adapter.py",
    }
    return config


def current_spec_md(args) -> str:
    spec = args.active_spec or "_none_"
    return (
        "# Current spec\n\n"
        f"Active spec: **{spec}**\n\n"
        "This pointer is convenience, not authority. The spec's source of truth is\n"
        f"`projects/{args.project}/specs/<spec>/spec.md` in the harness "
        f"(`{args.harness_root}`).\n"
    )


def _validate_args(args) -> list[str]:
    errors: list[str] = []
    if not SLUG.match(args.project):
        errors.append(f"--project must be a slug (got: {args.project!r})")
    if args.mode not in {"local", "central"}:
        errors.append(f"--mode must be 'local' or 'central' (got: {args.mode!r})")
    if not args.harness_root:
        errors.append("--harness-root must be non-empty")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install a praxis adapter into a repo.")
    parser.add_argument("--target", required=True, help="Path to the consuming repo root.")
    parser.add_argument("--project", required=True, help="Project id (slug).")
    parser.add_argument("--harness-root", default="../praxis", help="Path from the repo to the harness.")
    parser.add_argument("--mode", default="local", choices=["local", "central"], help="Project-memory mode.")
    parser.add_argument("--active-spec", default=None, help="Active spec id, or omitted for none.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing config.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if files are missing or would change.")
    args = parser.parse_args(argv)

    arg_errors = _validate_args(args)
    if arg_errors:
        for e in arg_errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    target = Path(args.target)
    if not target.is_dir():
        print(f"error: target is not a directory: {target}", file=sys.stderr)
        return 2

    praxis_dir = target / ".praxis"
    config_path = praxis_dir / "config.json"
    spec_path = praxis_dir / "current-spec.md"

    config_text = json.dumps(build_config(args), indent=2) + "\n"
    spec_text = current_spec_md(args)

    if args.check:
        drift = []
        if not config_path.is_file() or config_path.read_text(encoding="utf-8") != config_text:
            drift.append(".praxis/config.json")
        if not spec_path.is_file() or spec_path.read_text(encoding="utf-8") != spec_text:
            drift.append(".praxis/current-spec.md")
        if drift:
            print("drift: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("adapter up to date")
        return 0

    if config_path.exists() and not args.force:
        print(
            f"refusing to overwrite existing {config_path} (pass --force)",
            file=sys.stderr,
        )
        return 1

    praxis_dir.mkdir(parents=True, exist_ok=True)
    config_path.write_text(config_text, encoding="utf-8")
    spec_path.write_text(spec_text, encoding="utf-8")
    print(f"wrote {config_path}")
    print(f"wrote {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
