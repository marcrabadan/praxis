"""Unit tests for the always-on harness bootstrap.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'

Every test runs against a throwaway directory so no real .praxis/ is touched.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import ensure_harness as eh


class _Tmp(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _config(self) -> dict:
        return json.loads((self.root / ".praxis" / "config.json").read_text())


class TestSlug(unittest.TestCase):
    def test_slugify_normalizes(self) -> None:
        self.assertEqual(eh.slugify("My App"), "my-app")
        self.assertEqual(eh.slugify("checkout_service"), "checkout-service")
        self.assertEqual(eh.slugify("--Weird__Name--"), "weird-name")
        self.assertEqual(eh.slugify(""), "project")


class TestConsumerBootstrap(_Tmp):
    """A plain repo (no harness spine) bootstraps a local project."""

    def test_bootstraps_local_project(self) -> None:
        rc = eh.ensure(self.root, harness_root_override=None)
        self.assertEqual(rc, 0)
        cfg = self._config()
        self.assertEqual(cfg["mode"], "local")
        self.assertEqual(cfg["projectId"], eh.slugify(self.root.name))
        self.assertEqual(cfg["generatedBy"], "tools/ensure_harness.py")
        # local memory lives in the repo, not in a harness projects/ dir
        self.assertTrue((self.root / ".praxis" / "project" / "PROJECT.md").is_file())
        self.assertTrue((self.root / ".praxis" / "project" / "memory" / "current-state.md").is_file())
        self.assertFalse((self.root / "projects").exists())

    def test_idempotent(self) -> None:
        eh.ensure(self.root, harness_root_override=None)
        before = (self.root / ".praxis" / "config.json").read_text()
        # mutate PROJECT.md to prove a second run does not clobber it
        proj = self.root / ".praxis" / "project" / "PROJECT.md"
        proj.write_text(proj.read_text() + "\nedited\n")
        rc = eh.ensure(self.root, harness_root_override=None)
        self.assertEqual(rc, 0)
        self.assertEqual((self.root / ".praxis" / "config.json").read_text(), before)
        self.assertIn("edited", proj.read_text())  # not overwritten

    def test_harness_root_override(self) -> None:
        eh.ensure(self.root, harness_root_override="../elsewhere")
        self.assertEqual(self._config()["harnessRoot"], "../elsewhere")


class TestHarnessRepoBootstrap(_Tmp):
    """A repo carrying the harness spine bootstraps a central project + index row."""

    def setUp(self) -> None:
        super().setUp()
        (self.root / "rules").mkdir()
        (self.root / "rules" / "source-of-truth.md").write_text("# sot\n")
        (self.root / "workflows").mkdir()
        (self.root / "workflows" / "registry.json").write_text("{}\n")
        (self.root / "projects").mkdir()
        (self.root / "projects" / "projects-index.md").write_text(
            "# Projects Index\n\n| Project id | Name | Status | Notes |\n"
            "|------------|------|--------|-------|\n"
            "| `helios` | Helios | active | example |\n"
        )

    def test_central_mode_and_index_row(self) -> None:
        rc = eh.ensure(self.root, harness_root_override=None)
        self.assertEqual(rc, 0)
        cfg = self._config()
        self.assertEqual(cfg["mode"], "central")
        self.assertEqual(cfg["harnessRoot"], ".")
        pid = cfg["projectId"]
        self.assertTrue((self.root / "projects" / pid / "PROJECT.md").is_file())
        index = (self.root / "projects" / "projects-index.md").read_text()
        self.assertIn(f"| `{pid}` |", index)
        self.assertIn("| `helios` |", index)  # existing row preserved

    def test_project_md_frontmatter_matches_folder(self) -> None:
        eh.ensure(self.root, harness_root_override=None)
        pid = self._config()["projectId"]
        body = (self.root / "projects" / pid / "PROJECT.md").read_text()
        self.assertIn(f"id: {pid}", body)
        self.assertIn("status: active", body)


class TestCheck(_Tmp):
    def test_config_resolves_false_then_true(self) -> None:
        self.assertFalse(eh.config_resolves(self.root))
        eh.ensure(self.root, harness_root_override=None)
        self.assertTrue(eh.config_resolves(self.root))

    def test_broken_config_does_not_resolve(self) -> None:
        praxis = self.root / ".praxis"
        praxis.mkdir()
        (praxis / "config.json").write_text("{ not json")
        self.assertFalse(eh.config_resolves(self.root))


if __name__ == "__main__":
    unittest.main()
