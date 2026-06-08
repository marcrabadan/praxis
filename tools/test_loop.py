"""Unit tests for the loop controller.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'

Every test points the ledger at a throwaway dir via PRAXIS_LOOPS_ROOT.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest

import loop as L


class _TmpRoot(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._prev = os.environ.get("PRAXIS_LOOPS_ROOT")
        os.environ["PRAXIS_LOOPS_ROOT"] = self._tmp.name

    def tearDown(self) -> None:
        if self._prev is None:
            os.environ.pop("PRAXIS_LOOPS_ROOT", None)
        else:
            os.environ["PRAXIS_LOOPS_ROOT"] = self._prev
        self._tmp.cleanup()

    def _run(self, argv: list[str]) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            try:
                rc = L.main(argv)
            except SystemExit as exc:  # argparse exits on bad/missing args
                rc = exc.code if isinstance(exc.code, int) else 2
        return rc, buf.getvalue()

    def _start(self, criteria=("c", "d"), max_iter=10, patience=3) -> str:
        argv = ["start", "--goal", "g", "--max-iterations", str(max_iter),
                "--patience", str(patience)]
        for c in criteria:
            argv += ["--criterion", c]
        rc, out = self._run(argv)
        self.assertEqual(rc, 0)
        return out.splitlines()[0].strip()

    def _loop(self, loop_id):
        return L._find(L._read_index(), loop_id)


class StartTests(_TmpRoot):
    def test_start_requires_a_criterion(self) -> None:
        rc, _ = self._run(["start", "--goal", "g"])
        # argparse rejects a missing required --criterion with its own exit code 2
        self.assertEqual(rc, 2)

    def test_start_assigns_stable_ids(self) -> None:
        loop_id = self._start(criteria=("tests green", "lint clean"))
        loop = self._loop(loop_id)
        self.assertEqual([c["id"] for c in loop["criteria"]], ["c1", "c2"])
        self.assertEqual(loop["status"], "running")


class VerdictTests(_TmpRoot):
    def test_all_criteria_met_is_done(self) -> None:
        loop_id = self._start()
        rc, out = self._run(["tick", loop_id, "--met", "all"])
        self.assertEqual(rc, 0)
        self.assertIn("VERDICT: done", out)
        self.assertEqual(self._loop(loop_id)["status"], "done")

    def test_partial_progress_is_continue(self) -> None:
        loop_id = self._start()
        rc, out = self._run(["tick", loop_id, "--met", "c1", "--signal", "one left"])
        self.assertEqual(rc, 0)
        self.assertIn("VERDICT: continue", out)
        self.assertEqual(self._loop(loop_id)["status"], "running")

    def test_budget_exhaustion_escalates(self) -> None:
        loop_id = self._start(max_iter=2, patience=99)
        # vary the signal each tick so the no-progress guard never fires first
        self._run(["tick", loop_id, "--met", "c1", "--signal", "s1"])
        rc, out = self._run(["tick", loop_id, "--met", "c1", "--signal", "s2"])
        self.assertIn("VERDICT: escalate", out)
        loop = self._loop(loop_id)
        self.assertEqual(loop["status"], "escalated")
        self.assertIn("budget exhausted", loop["escalation"])

    def test_no_progress_escalates(self) -> None:
        loop_id = self._start(max_iter=99, patience=3)
        self._run(["tick", loop_id, "--signal", "stuck"])
        self._run(["tick", loop_id, "--signal", "stuck"])
        rc, out = self._run(["tick", loop_id, "--signal", "stuck"])
        self.assertIn("VERDICT: escalate", out)
        self.assertIn("no progress", self._loop(loop_id)["escalation"])

    def test_changing_signal_avoids_no_progress(self) -> None:
        loop_id = self._start(max_iter=99, patience=2)
        self._run(["tick", loop_id, "--signal", "a"])
        rc, out = self._run(["tick", loop_id, "--signal", "b"])
        self.assertIn("VERDICT: continue", out)

    def test_done_takes_priority_over_budget(self) -> None:
        # on the final allowed iteration, meeting the predicate wins over escalate
        loop_id = self._start(max_iter=1, patience=99)
        rc, out = self._run(["tick", loop_id, "--met", "all"])
        self.assertIn("VERDICT: done", out)


class GuardTests(_TmpRoot):
    def test_unknown_criterion_rejected(self) -> None:
        loop_id = self._start()
        rc, _ = self._run(["tick", loop_id, "--met", "c9"])
        self.assertEqual(rc, 2)

    def test_numeric_met_token_maps_to_id(self) -> None:
        loop_id = self._start()
        self._run(["tick", loop_id, "--met", "1", "--signal", "x"])
        self.assertEqual(self._loop(loop_id)["iterations"][-1]["met"], ["c1"])

    def test_cannot_tick_escalated_loop(self) -> None:
        loop_id = self._start(max_iter=1, patience=99)
        self._run(["tick", loop_id, "--signal", "x"])  # escalates
        rc, _ = self._run(["tick", loop_id, "--signal", "y"])
        self.assertEqual(rc, 1)

    def test_resume_reopens_and_can_raise_budget(self) -> None:
        loop_id = self._start(max_iter=1, patience=99)
        self._run(["tick", loop_id, "--signal", "x"])  # escalates at budget
        rc, _ = self._run(["resume", loop_id, "--max-iterations", "5"])
        self.assertEqual(rc, 0)
        loop = self._loop(loop_id)
        self.assertEqual(loop["status"], "running")
        self.assertEqual(loop["max_iterations"], 5)
        # and it can tick again
        rc, out = self._run(["tick", loop_id, "--signal", "y"])
        self.assertIn("VERDICT: continue", out)

    def test_resume_budget_must_exceed_iterations_run(self) -> None:
        loop_id = self._start(max_iter=1, patience=99)
        self._run(["tick", loop_id, "--signal", "x"])
        rc, _ = self._run(["resume", loop_id, "--max-iterations", "1"])
        self.assertEqual(rc, 2)


class CloseTests(_TmpRoot):
    def test_resolve_abandoned(self) -> None:
        loop_id = self._start()
        rc, _ = self._run(["resolve", loop_id, "--as", "abandoned", "--note", "descoped"])
        self.assertEqual(rc, 0)
        self.assertEqual(self._loop(loop_id)["status"], "abandoned")

    def test_resolve_bad_target_rejected(self) -> None:
        loop_id = self._start()
        rc, _ = self._run(["resolve", loop_id, "--as", "nonsense"])
        self.assertEqual(rc, 2)

    def test_unknown_loop_returns_1(self) -> None:
        rc, _ = self._run(["status", "LOOP-nope"])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
