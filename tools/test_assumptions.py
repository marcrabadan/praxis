"""Unit tests for the assumptions ledger.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'

Every test points the ledger at a throwaway dir via PRAXIS_ASSUMPTIONS_ROOT so
no real .praxis/ is touched.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import assumptions as a


class _TmpRoot(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._prev = os.environ.get("PRAXIS_ASSUMPTIONS_ROOT")
        os.environ["PRAXIS_ASSUMPTIONS_ROOT"] = self._tmp.name

    def tearDown(self) -> None:
        if self._prev is None:
            os.environ.pop("PRAXIS_ASSUMPTIONS_ROOT", None)
        else:
            os.environ["PRAXIS_ASSUMPTIONS_ROOT"] = self._prev
        self._tmp.cleanup()

    def _add(self, **over) -> str:
        argv = ["add",
                "--statement", over.get("statement", "API returns ISO-8601"),
                "--confidence", over.get("confidence", "low"),
                "--impact", over.get("impact", "date parsing"),
                "--source", over.get("source", "/developer")]
        for alt in over.get("alts", ["epoch millis"]):
            argv += ["--alt", alt]
        if "body" in over:
            argv += ["--body", over["body"]]
        # capture the printed id
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = a.main(argv)
        self.assertEqual(rc, 0)
        return buf.getvalue().strip()


class AddAndReadTests(_TmpRoot):
    def test_add_writes_index_and_entry(self) -> None:
        entry_id = self._add(body="No schema; assumed ISO-8601 to keep moving.")
        self.assertTrue(entry_id.startswith("ASSUME-"))
        rows = a._read_index()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "open")
        self.assertEqual(rows[0]["confidence"], "low")
        self.assertIn("ISO-8601", rows[0]["statement"])
        # the markdown entry exists and carries the reasoning body
        body = a._read_entry_body(entry_id)
        self.assertIn("keep moving", body)

    def test_high_confidence_is_rejected(self) -> None:
        rc = a.main(["add", "--statement", "x", "--confidence", "high"])
        self.assertEqual(rc, 2)

    def test_alternatives_recorded(self) -> None:
        self._add(alts=["epoch millis", "RFC-2822"])
        rows = a._read_index()
        self.assertEqual(rows[0]["alternatives"], ["epoch millis", "RFC-2822"])


class SweepTests(_TmpRoot):
    def test_sweep_orders_low_confidence_first(self) -> None:
        self._add(statement="medium one", confidence="medium", alts=[])
        self._add(statement="low one", confidence="low", alts=[])
        opens = a._sorted_open(a._read_index())
        self.assertEqual(opens[0]["statement"], "low one")

    def test_sweep_json_shapes_question_with_recommended_first(self) -> None:
        self._add(statement="ISO-8601", alts=["epoch millis", "RFC-2822"])
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            a.main(["sweep", "--json"])
        data = json.loads(buf.getvalue())
        q = data["questions"][0]
        self.assertTrue(q["free_answer"])
        self.assertEqual(q["options"][0]["text"], "ISO-8601")
        self.assertTrue(q["options"][0]["recommended"])
        # alternatives become B, C
        self.assertEqual([o["key"] for o in q["options"]], ["A", "B", "C"])

    def test_resolved_assumptions_drop_out_of_sweep(self) -> None:
        entry_id = self._add()
        a.main(["confirm", entry_id])
        self.assertEqual(a._sorted_open(a._read_index()), [])


class ResolveTests(_TmpRoot):
    def test_confirm_sets_status_and_decision_ref(self) -> None:
        entry_id = self._add()
        rc = a.main(["confirm", entry_id, "--decision", "20260608-x", "--promote", "rule"])
        self.assertEqual(rc, 0)
        row = a._find(a._read_index(), entry_id)
        self.assertEqual(row["status"], "confirmed")
        self.assertEqual(row["decision_ref"], "20260608-x")
        self.assertEqual(row["promote"], "rule")

    def test_correct_records_resolution(self) -> None:
        entry_id = self._add()
        rc = a.main(["correct", entry_id, "--answer", "epoch millis"])
        self.assertEqual(rc, 0)
        row = a._find(a._read_index(), entry_id)
        self.assertEqual(row["status"], "corrected")
        self.assertEqual(row["resolution"], "epoch millis")

    def test_bad_promote_target_rejected(self) -> None:
        entry_id = self._add()
        rc = a.main(["confirm", entry_id, "--promote", "nonsense"])
        self.assertEqual(rc, 2)

    def test_withdraw(self) -> None:
        entry_id = self._add()
        rc = a.main(["withdraw", entry_id, "--note", "code path removed"])
        self.assertEqual(rc, 0)
        self.assertEqual(a._find(a._read_index(), entry_id)["status"], "withdrawn")

    def test_prefix_match_resolves_id(self) -> None:
        entry_id = self._add()
        tail = entry_id.split("-", 1)[1]  # drop the ASSUME- prefix
        rc = a.main(["confirm", tail])
        self.assertEqual(rc, 0)
        self.assertEqual(a._find(a._read_index(), entry_id)["status"], "confirmed")

    def test_unknown_id_returns_1(self) -> None:
        self.assertEqual(a.main(["confirm", "ASSUME-nope"]), 1)


if __name__ == "__main__":
    unittest.main()
