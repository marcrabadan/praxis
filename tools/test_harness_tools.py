"""Unit tests for the harness tools: validate_harness and runtime.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import install_adapter
import runtime
import validate_harness as vh


class WorkflowManifestTests(unittest.TestCase):
    def _write(self, tmp: Path, name: str, data: dict) -> Path:
        path = tmp / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_valid_manifest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "feature-development.workflow.json",
                {
                    "id": "feature-development",
                    "name": "Feature development",
                    "steps": ["spec", "plan", "tasks", "verify"],
                    "gates": {"plan": ["approved-spec"]},
                },
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertEqual(errors, [])

    def test_gate_referencing_unknown_step_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "bad.workflow.json",
                {
                    "id": "bad",
                    "name": "Bad",
                    "steps": ["spec", "plan"],
                    "gates": {"nope": ["x"]},
                },
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertTrue(any("unknown step" in e for e in errors), errors)

    def test_id_must_match_filename(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "feature-development.workflow.json",
                {"id": "mismatch", "name": "X", "steps": ["a"]},
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertTrue(any("does not match file name" in e for e in errors), errors)

    def test_duplicate_steps_fail(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "dup.workflow.json",
                {"id": "dup", "name": "Dup", "steps": ["a", "a"]},
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertTrue(any("duplicate" in e for e in errors), errors)

    def test_valid_loops_block_passes(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "feature-development.workflow.json",
                {
                    "id": "feature-development",
                    "name": "F",
                    "steps": ["build", "verify"],
                    "loops": {
                        "verify": {
                            "predicate": ["tests green", "lint clean"],
                            "maxIterations": 8,
                            "patience": 3,
                            "onContinue": "build",
                        }
                    },
                },
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertEqual(errors, [])

    def test_loop_empty_predicate_fails(self) -> None:
        errors: list[str] = []
        vh._check_workflow_loops("wf", {"verify": {"predicate": []}}, {"verify"}, errors)
        self.assertTrue(any("predicate" in e for e in errors), errors)

    def test_loop_on_unknown_step_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            path = self._write(
                tmp,
                "wf.workflow.json",
                {
                    "id": "wf",
                    "name": "W",
                    "steps": ["build", "verify"],
                    "loops": {"nope": {"predicate": ["x"]}},
                },
            )
            errors: list[str] = []
            vh._check_workflow_manifest(path, errors)
            self.assertTrue(any("unknown step" in e for e in errors), errors)

    def test_loop_bad_max_iterations_fails(self) -> None:
        errors: list[str] = []
        vh._check_workflow_loops(
            "wf", {"verify": {"predicate": ["x"], "maxIterations": 0}}, {"verify"}, errors
        )
        self.assertTrue(any("maxIterations" in e for e in errors), errors)

    def test_loop_dangling_on_continue_fails(self) -> None:
        errors: list[str] = []
        vh._check_workflow_loops(
            "wf", {"verify": {"predicate": ["x"], "onContinue": "ghost"}}, {"verify"}, errors
        )
        self.assertTrue(any("onContinue" in e for e in errors), errors)


class ConfigValidationTests(unittest.TestCase):
    def test_missing_project_id_fails(self) -> None:
        errors: list[str] = []
        vh._validate_config_data(
            {"schemaVersion": "1.0.0", "harnessRoot": "../praxis"},
            "cfg",
            None,
            errors,
        )
        self.assertTrue(any("projectId" in e for e in errors), errors)

    def test_local_mode_skips_harness_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            errors: list[str] = []
            vh._validate_config_data(
                {
                    "schemaVersion": "1.0.0",
                    "harnessRoot": "../praxis",
                    "projectId": "ghost",
                    "mode": "local",
                },
                "cfg",
                Path(d),
                errors,
            )
            self.assertEqual(errors, [])

    def test_central_mode_requires_existing_project(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            errors: list[str] = []
            vh._validate_config_data(
                {
                    "schemaVersion": "1.0.0",
                    "harnessRoot": "../praxis",
                    "projectId": "ghost",
                    "mode": "central",
                },
                "cfg",
                Path(d),
                errors,
            )
            self.assertTrue(any("does not resolve" in e for e in errors), errors)


class HarnessRootResolutionTests(unittest.TestCase):
    """A real .praxis/config.json must point harnessRoot at an actual harness."""

    def _write_adapter(self, repo: Path, harness_root: str) -> Path:
        praxis = repo / ".praxis"
        praxis.mkdir(parents=True)
        cfg = praxis / "config.json"
        cfg.write_text(
            json.dumps(
                {
                    "schemaVersion": "1.0.0",
                    "harnessRoot": harness_root,
                    "projectId": "checkout",
                    "mode": "local",
                }
            ),
            encoding="utf-8",
        )
        return cfg

    def test_typo_harness_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            cfg = self._write_adapter(Path(d), "../praxiz")
            errors: list[str] = []
            vh._check_config(cfg, None, errors)
            self.assertTrue(any("unknown harness root" in e for e in errors), errors)

    def test_valid_harness_root_passes(self) -> None:
        import os

        real_harness = Path(vh.__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            rel = os.path.relpath(real_harness, repo)
            cfg = self._write_adapter(repo, rel)
            errors: list[str] = []
            vh._check_config(cfg, None, errors)
            self.assertEqual(errors, [])

    def test_non_dot_praxis_config_skips_resolution(self) -> None:
        # A config not located in a .praxis/ dir (e.g. the shipped example) is
        # not resolved against a consuming-repo root, so a relative harnessRoot
        # is not treated as a hard block.
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d) / "example.json"
            cfg.write_text(
                json.dumps(
                    {
                        "schemaVersion": "1.0.0",
                        "harnessRoot": "../praxis",
                        "projectId": "checkout",
                        "mode": "local",
                    }
                ),
                encoding="utf-8",
            )
            errors: list[str] = []
            vh._check_config(cfg, None, errors)
            self.assertEqual(errors, [])


class RuntimeTests(unittest.TestCase):
    def test_default_state_when_absent(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            state = runtime.load_state(Path(d))
            self.assertEqual(state["schemaVersion"], runtime.SCHEMA_VERSION)
            self.assertIsNone(state["lastActiveProject"])

    def test_set_and_reload_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            runtime.main(["--root", str(root), "set", "--project", "checkout", "--spec", "oauth"])
            state = runtime.load_state(root)
            self.assertEqual(state["lastActiveProject"], "checkout")
            self.assertEqual(state["lastActiveSpec"], "oauth")
            self.assertIsNotNone(state["updated"])

    def test_log_appends_event(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            runtime.main(["--root", str(root), "log", "--type", "adapter-install", "--note", "codex"])
            lines = (root / "runtime" / "activity-log.jsonl").read_text().splitlines()
            self.assertEqual(len(lines), 1)
            event = json.loads(lines[0])
            self.assertEqual(event["type"], "adapter-install")
            self.assertEqual(event["note"], "codex")


class InstallAdapterTests(unittest.TestCase):
    def test_writes_then_idempotent_check(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            rc = install_adapter.main(
                ["--target", d, "--project", "checkout", "--mode", "local"]
            )
            self.assertEqual(rc, 0)
            cfg = Path(d) / ".praxis" / "config.json"
            self.assertTrue(cfg.is_file())
            # --check on the just-written adapter reports up to date
            rc = install_adapter.main(
                ["--target", d, "--project", "checkout", "--mode", "local", "--check"]
            )
            self.assertEqual(rc, 0)

    def test_generated_config_passes_validator(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            install_adapter.main(["--target", d, "--project", "checkout", "--mode", "local"])
            data = json.loads((Path(d) / ".praxis" / "config.json").read_text())
            errors: list[str] = []
            vh._validate_config_data(data, "cfg", None, errors)
            self.assertEqual(errors, [])

    def test_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            install_adapter.main(["--target", d, "--project", "checkout"])
            rc = install_adapter.main(["--target", d, "--project", "other"])
            self.assertEqual(rc, 1)

    def test_rejects_bad_project_slug(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            rc = install_adapter.main(["--target", d, "--project", "Bad_Slug"])
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
