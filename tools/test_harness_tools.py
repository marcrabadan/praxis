"""Unit tests for the harness tools: validate_harness and runtime.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
