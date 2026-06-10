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

    def test_hotspot_recurring_file_at_threshold(self) -> None:
        hits = [
            ("src/foo.py", "e1"),
            ("src/foo.py", "e2"),
            ("src/foo.py", "e3"),
            ("src/bar.py", "e1"),
        ]
        out = pt.mine_patterns([], [], hits, min_count=3)
        vals = {r["value"]: r["count"] for r in out["hotspot"]}
        self.assertEqual(vals.get("src/foo.py"), 3)
        self.assertNotIn("src/bar.py", vals)

    def test_scan_touched_files_parses_files_touched_section(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            entries_dir = Path(d)
            (entries_dir / "e1.md").write_text(
                "---\nid: e1\ntype: implementation\n---\n\n"
                "Automatic snapshot.\n\n"
                "**Files touched:**\n\n"
                "- `src/foo.py`\n"
                "- `src/bar.py`\n\n"
                "```\n src/foo.py | 2 +-\n```\n",
                encoding="utf-8",
            )
            entries = [_entry("e1", type="implementation")]
            hits = pt.scan_touched_files(entries, entries_dir)
            self.assertEqual(hits, [("src/foo.py", "e1"), ("src/bar.py", "e1")])

    def test_scan_touched_files_dedupes_snapshots_from_same_spec(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            entries_dir = Path(d)
            for i in range(1, 4):
                (entries_dir / f"e{i}.md").write_text(
                    "**Files touched:**\n\n- `src/foo.py`\n", encoding="utf-8"
                )
            entries = [
                _entry(f"e{i}", type="implementation", tags=["source:D1"])
                for i in range(1, 4)
            ]
            hits = pt.scan_touched_files(entries, entries_dir)
            # Three iterative snapshots of the same spec (shared `source:`
            # tag) collapse to a single (file, spec) pair, so they don't
            # look like 3+ distinct specs touching the file.
            self.assertEqual(hits, [("src/foo.py", "D1")])

    def test_scan_touched_files_distinct_specs_without_source_tag(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            entries_dir = Path(d)
            for i in range(1, 4):
                (entries_dir / f"e{i}.md").write_text(
                    "**Files touched:**\n\n- `src/foo.py`\n", encoding="utf-8"
                )
            entries = [_entry(f"e{i}", type="implementation") for i in range(1, 4)]
            hits = pt.scan_touched_files(entries, entries_dir)
            # No `source:` tag to group by: each entry is its own spec, so
            # all three count as distinct specs touching the file.
            self.assertEqual(
                hits,
                [("src/foo.py", "e1"), ("src/foo.py", "e2"), ("src/foo.py", "e3")],
            )

    def test_scan_touched_files_skips_non_implementation_entries(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            entries_dir = Path(d)
            (entries_dir / "e1.md").write_text(
                "**Files touched:**\n\n- `src/foo.py`\n", encoding="utf-8"
            )
            entries = [_entry("e1", type="decision")]
            hits = pt.scan_touched_files(entries, entries_dir)
            self.assertEqual(hits, [])

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
        text = pt.format_report(
            {"tag": [], "source": [], "type": [], "stop-condition": [], "hotspot": []}, 0, 0, 3
        )
        self.assertIn("No recurring patterns", text)


if __name__ == "__main__":
    unittest.main()
