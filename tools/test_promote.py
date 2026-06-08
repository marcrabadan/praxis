"""Unit tests for the promotion executor.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'

Both the assumptions ledger and the memory ledger are pointed at one throwaway
dir (via their env overrides) so a promotion links them exactly as it would in a
real repo, without touching any real .praxis/.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest

import assumptions as A
import promote as P
import ledger as L


class _TmpRoot(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._env = {}
        for var in ("PRAXIS_ASSUMPTIONS_ROOT", "PRAXIS_MEMORY_ROOT"):
            self._env[var] = os.environ.get(var)
            os.environ[var] = self._tmp.name

    def tearDown(self) -> None:
        for var, prev in self._env.items():
            if prev is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = prev
        self._tmp.cleanup()

    def _run(self, mod, argv) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            try:
                rc = mod.main(argv)
            except SystemExit as exc:
                rc = exc.code if isinstance(exc.code, int) else 2
        return rc, buf.getvalue()

    def _resolved_assumption(self, promote=None) -> str:
        argv = ["add", "--statement", "API returns ISO-8601", "--confidence", "low",
                "--impact", "ingest", "--source", "/developer", "--alt", "epoch"]
        _, out = self._run(A, argv)
        aid = out.strip()
        conf = ["confirm", aid]
        if promote:
            conf += ["--promote", promote]
        self._run(A, conf)
        return aid


class FromAssumptionTests(_TmpRoot):
    def test_open_assumption_is_refused(self) -> None:
        _, out = self._run(A, ["add", "--statement", "x", "--confidence", "low"])
        aid = out.strip()
        rc, _ = self._run(P, ["from-assumption", aid, "--target", "rule"])
        self.assertEqual(rc, 1)  # evidence rule: must be resolved first

    def test_promotes_resolved_assumption_to_pending_decision(self) -> None:
        aid = self._resolved_assumption(promote="rule")
        rc, out = self._run(P, ["from-assumption", aid])  # target from --promote
        self.assertEqual(rc, 0)
        lid = out.splitlines()[0].strip()
        entry = L._find(L._read_index(), lid)
        self.assertEqual(entry["status"], "pending")
        self.assertEqual(entry["type"], "decision")
        self.assertIn("promotion", entry["tags"])
        self.assertIn("promote:rule", entry["tags"])
        self.assertIn(f"source:{aid}", entry["tags"])

    def test_links_decision_ref_back_to_assumption(self) -> None:
        aid = self._resolved_assumption(promote="gate")
        _, out = self._run(P, ["from-assumption", aid])
        lid = out.splitlines()[0].strip()
        arow = A._find(A._read_index(), aid)
        self.assertEqual(arow["decision_ref"], lid)
        self.assertEqual(arow["promote"], "gate")

    def test_target_required_when_none_recorded(self) -> None:
        aid = self._resolved_assumption()  # no --promote
        rc, _ = self._run(P, ["from-assumption", aid])
        self.assertEqual(rc, 2)

    def test_explicit_target_overrides(self) -> None:
        aid = self._resolved_assumption(promote="rule")
        _, out = self._run(P, ["from-assumption", aid, "--target", "eval"])
        lid = out.splitlines()[0].strip()
        entry = L._find(L._read_index(), lid)
        self.assertIn("promote:eval", entry["tags"])

    def test_body_carries_evidence_and_routing(self) -> None:
        aid = self._resolved_assumption(promote="rule")
        _, out = self._run(P, ["from-assumption", aid])
        lid = out.splitlines()[0].strip()
        body = L._read_entry_body(lid)
        self.assertIn("## Evidence", body)
        self.assertIn(aid, body)
        self.assertIn("Routing", body)
        self.assertIn("pending", body.lower())


class ProposeTests(_TmpRoot):
    def test_propose_requires_evidence(self) -> None:
        rc, _ = self._run(P, ["propose", "--target", "rule", "--title", "t"])
        self.assertEqual(rc, 2)  # argparse: --evidence required

    def test_propose_creates_pending_decision(self) -> None:
        rc, out = self._run(P, ["propose", "--target", "gate", "--title",
                                "perf budget at verify", "--evidence",
                                "3 latency incidents", "--rationale", "make it a gate"])
        self.assertEqual(rc, 0)
        lid = out.splitlines()[0].strip()
        entry = L._find(L._read_index(), lid)
        self.assertEqual(entry["status"], "pending")
        self.assertIn("promote:gate", entry["tags"])
        self.assertIn("3 latency incidents", L._read_entry_body(lid))

    def test_bad_target_rejected(self) -> None:
        rc, _ = self._run(P, ["propose", "--target", "nope", "--title", "t",
                              "--evidence", "e"])
        self.assertEqual(rc, 2)


class ListAndRoutingTests(_TmpRoot):
    def test_list_filters_to_promotions(self) -> None:
        # a non-promotion ledger entry should not show up
        self._run(L, ["log", "--type", "note", "--title", "unrelated"])
        self._run(P, ["propose", "--target", "rule", "--title", "r",
                      "--evidence", "e"])
        rc, out = self._run(P, ["list"])
        self.assertEqual(rc, 0)
        self.assertIn("rule", out)
        self.assertNotIn("unrelated", out)

    def test_list_target_filter(self) -> None:
        self._run(P, ["propose", "--target", "rule", "--title", "r", "--evidence", "e"])
        self._run(P, ["propose", "--target", "eval", "--title", "v", "--evidence", "e"])
        _, out = self._run(P, ["list", "--target", "eval"])
        self.assertIn("v", out)
        self.assertNotIn("[pending]  rule", out)

    def test_routing_prints_target_guidance(self) -> None:
        rc, out = self._run(P, ["routing", "rule"])
        self.assertEqual(rc, 0)
        self.assertIn("rules/", out)

    def test_routing_bad_target(self) -> None:
        rc, _ = self._run(P, ["routing", "nonsense"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
