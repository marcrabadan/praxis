"""Unit tests for the tasks anti-drift linter.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_tasks as ct

_GOOD = """# Tasks

### Surface: checkout

files-owned:
- src/checkout.tsx

- [ ] T010 [checkout] Implement the surface.
  - Plan ref: Per-surface plan / checkout
  - Decisions in force: none
  - Forbidden: renaming the route
  - Gate: G-build, G-typecheck
  - Output: src/checkout.tsx
"""

_MISSING_FIELDS = """# Tasks

- [ ] T001 [scaffold] Do a thing.
  - Plan ref: Phase 1
  - Output: foo.py
"""

_MISSING_FILES_OWNED = """# Tasks

### Surface: cart

- [ ] T010 [cart] Implement.
  - Forbidden: none
  - Gate: G-build
  - Output: cart.ts
"""


class LintTests(unittest.TestCase):
    def _write(self, text: str) -> Path:
        d = tempfile.mkdtemp()
        p = Path(d) / "tasks.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_well_formed_passes(self) -> None:
        code, _ = ct.lint(self._write(_GOOD), ct.DEFAULT_REQUIRED)
        self.assertEqual(code, 0)

    def test_missing_forbidden_and_gate_flagged(self) -> None:
        code, report = ct.lint(self._write(_MISSING_FIELDS), ct.DEFAULT_REQUIRED)
        self.assertEqual(code, 1)
        joined = "\n".join(report)
        self.assertIn("T001", joined)
        self.assertIn("Forbidden", joined)
        self.assertIn("Gate", joined)

    def test_missing_files_owned_flagged(self) -> None:
        code, report = ct.lint(self._write(_MISSING_FILES_OWNED), ct.DEFAULT_REQUIRED)
        self.assertEqual(code, 1)
        self.assertTrue(any("files-owned" in r and "cart" in r for r in report))

    def test_no_tasks_is_arg_error(self) -> None:
        code, _ = ct.lint(self._write("# Tasks\n\njust prose, no tasks\n"), ct.DEFAULT_REQUIRED)
        self.assertEqual(code, 2)

    def test_missing_file_is_arg_error(self) -> None:
        code, _ = ct.lint(Path("/no/such/tasks.md"), ct.DEFAULT_REQUIRED)
        self.assertEqual(code, 2)

    def test_custom_required_fields(self) -> None:
        # only require Output; the missing-fields fixture has Output, so it passes
        code, _ = ct.lint(self._write(_MISSING_FIELDS), ("output",))
        self.assertEqual(code, 0)

    def test_parallel_marker_task_parsed(self) -> None:
        text = ("# Tasks\n\n- [ ] T020 [P] [cart] Thing.\n"
                "  - Forbidden: none\n  - Gate: G-build\n  - Output: x.ts\n")
        tasks = ct._parse_tasks(text.splitlines())
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], "T020")
        self.assertEqual(tasks[0]["fields"], {"forbidden", "gate", "output"})

    def test_main_returns_exit_code(self) -> None:
        self.assertEqual(ct.main([str(self._write(_GOOD))]), 0)
        self.assertEqual(ct.main([str(self._write(_MISSING_FIELDS))]), 1)


if __name__ == "__main__":
    unittest.main()
