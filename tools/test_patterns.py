"""Unit tests for the continuous-learning pattern miner.

Deterministic, stdlib-only. Run via:
    python -m unittest discover -s tools -p 'test_*.py'
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import patterns as pt


def _entry(eid: str, **kw) -> dict:
    base = {"id": eid, "source": "/new-feature", "type": "decision", "tags": []}
    base.update(kw)
    return base


class MineTests(unittest.TestCase):
    def test_recurring_tag_at_threshold(self) -> None:
        entries = [_entry(f"e{i}", tags=["harness"]) for i in range(3)]
        out = pt.mine_patterns(entries, [], min_count=3)
        tags = {r["value"]: r["count"] for r in out["tag"]}
        self.assertEqual(tags.get("harness"), 3)

    def test_below_threshold_excluded(self) -> None:
        entries = [_entry("e1", tags=["rare"]), _entry("e2", tags=["rare"])]
        out = pt.mine_patterns(entries, [], min_count=3)
        self.assertEqual(out["tag"], [])

    def test_stop_conditions_counted(self) -> None:
        hits = [("U-2", "a.md"), ("U-2", "b.md"), ("U-2", "c.md"), ("U-7", "a.md")]
        out = pt.mine_patterns([], hits, min_count=3)
        vals = {r["value"]: r["count"] for r in out["stop-condition"]}
        self.assertEqual(vals.get("U-2"), 3)
        self.assertNotIn("U-7", vals)

    def test_examples_capped(self) -> None:
        entries = [_entry(f"e{i}", tags=["x"]) for i in range(10)]
        out = pt.mine_patterns(entries, [], min_count=1)
        row = next(r for r in out["tag"] if r["value"] == "x")
        self.assertLessEqual(len(row["examples"]), 5)

    def test_load_ledger_skips_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ledger.jsonl"
            p.write_text(
                json.dumps(_entry("ok")) + "\nnot-json\n" + json.dumps(_entry("ok2")) + "\n",
                encoding="utf-8",
            )
            entries = pt.load_ledger(p)
            self.assertEqual([e["id"] for e in entries], ["ok", "ok2"])

    def test_scan_run_logs_dedupes_per_file(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "r.md"
            log.write_text("STOP[U-2] ... and again U-2 here", encoding="utf-8")
            hits = pt.scan_run_logs([log])
            self.assertEqual(hits, [("U-2", str(log))])

    def test_run_on_full_root(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            mem = root / ".praxis" / "memory"
            mem.mkdir(parents=True)
            (mem / "ledger.jsonl").write_text(
                "\n".join(json.dumps(_entry(f"e{i}", tags=["harness"])) for i in range(3)),
                encoding="utf-8",
            )
            report = pt.run(root, min_count=3)
            self.assertEqual(report["n_entries"], 3)
            self.assertTrue(any(r["value"] == "harness" for r in report["patterns"]["tag"]))

    def test_format_report_handles_empty(self) -> None:
        text = pt.format_report({"tag": [], "source": [], "type": [], "stop-condition": []}, 0, 0, 3)
        self.assertIn("No recurring patterns", text)


if __name__ == "__main__":
    unittest.main()
