"""Unit tests for ledger.py — stdlib only, no third-party deps.

Covers both pre-existing commands and the new ones added in this PR:
  - list --tag filter
  - supersede
  - dependents
  - stale
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Make ledger importable from this directory
sys.path.insert(0, str(Path(__file__).parent))
import ledger


def _run(*args, env_root=None):
    """Run a ledger CLI command, returning (exit_code, stdout)."""
    import io
    from contextlib import redirect_stdout

    if env_root:
        os.environ["PRAXIS_MEMORY_ROOT"] = str(env_root)

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            code = ledger.main(list(args))
    except SystemExit as e:
        code = int(e.code) if e.code is not None else 0
    finally:
        if env_root:
            os.environ.pop("PRAXIS_MEMORY_ROOT", None)

    return code, out.getvalue()


class LedgerTestCase(unittest.TestCase):
    """Base: each test gets a fresh temp directory as the ledger root."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        os.environ["PRAXIS_MEMORY_ROOT"] = str(self.root)
        ledger.main(["init"])

    def tearDown(self):
        os.environ.pop("PRAXIS_MEMORY_ROOT", None)
        self._tmpdir.cleanup()

    def run_cmd(self, *args):
        return _run(*args)

    def log_entry(self, type_="decision", title="Test entry", tags="", status="pending", body="body text"):
        code, out = self.run_cmd(
            "log", "--type", type_, "--title", title,
            "--source", "/test", "--status", status,
            *(["--tags", tags] if tags else []),
            "--body", body,
        )
        self.assertEqual(code, 0)
        return out.strip()

    def read_index(self):
        ledger_path = self.root / ".praxis" / "memory" / "ledger.jsonl"
        rows = []
        for line in ledger_path.read_text().splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------
class TestInit(LedgerTestCase):
    def test_creates_directory_structure(self):
        base = self.root / ".praxis" / "memory"
        self.assertTrue(base.is_dir())
        self.assertTrue((base / "entries").is_dir())
        self.assertTrue((base / "patches").is_dir())
        self.assertTrue((base / "ledger.jsonl").is_file())
        self.assertTrue((base / "README.md").is_file())

    def test_idempotent(self):
        code, _ = self.run_cmd("init")
        self.assertEqual(code, 0)


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------
class TestLog(LedgerTestCase):
    def test_creates_entry(self):
        entry_id = self.log_entry(title="My decision")
        rows = self.read_index()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "My decision")
        self.assertEqual(rows[0]["status"], "pending")

    def test_tags_stored_as_list(self):
        entry_id = self.log_entry(tags="arch,adr,payments")
        rows = self.read_index()
        self.assertEqual(rows[0]["tags"], ["arch", "adr", "payments"])

    def test_entry_file_created(self):
        entry_id = self.log_entry()
        path = self.root / ".praxis" / "memory" / "entries" / f"{entry_id}.md"
        self.assertTrue(path.is_file())
        self.assertIn("body text", path.read_text())

    def test_invalid_type_returns_error(self):
        code, _ = self.run_cmd("log", "--type", "invalid", "--title", "x")
        self.assertEqual(code, 2)


# ---------------------------------------------------------------------------
# list + --tag filter
# ---------------------------------------------------------------------------
class TestList(LedgerTestCase):
    def setUp(self):
        super().setUp()
        self.id1 = self.log_entry(type_="decision", title="Decision A", tags="arch", status="pending")
        self.id2 = self.log_entry(type_="artifact", title="Artifact B", tags="docs,source:20240101-abcd", status="accepted")
        self.id3 = self.log_entry(type_="plan", title="Plan C", tags="docs,source:20240101-abcd", status="pending")

    def test_list_all(self):
        code, out = self.run_cmd("list")
        self.assertEqual(code, 0)
        self.assertIn("Decision A", out)
        self.assertIn("Artifact B", out)
        self.assertIn("Plan C", out)

    def test_filter_by_status(self):
        code, out = self.run_cmd("list", "--status", "accepted")
        self.assertEqual(code, 0)
        self.assertIn("Artifact B", out)
        self.assertNotIn("Decision A", out)

    def test_filter_by_type(self):
        code, out = self.run_cmd("list", "--type", "plan")
        self.assertEqual(code, 0)
        self.assertIn("Plan C", out)
        self.assertNotIn("Decision A", out)

    def test_filter_by_source(self):
        code, out = self.run_cmd("list", "--source", "/test")
        self.assertEqual(code, 0)
        self.assertIn("Decision A", out)

    def test_filter_by_tag_matches(self):
        code, out = self.run_cmd("list", "--tag", "source:20240101-abcd")
        self.assertEqual(code, 0)
        self.assertIn("Artifact B", out)
        self.assertIn("Plan C", out)
        self.assertNotIn("Decision A", out)

    def test_filter_by_tag_no_match(self):
        code, out = self.run_cmd("list", "--tag", "source:does-not-exist")
        self.assertEqual(code, 0)
        self.assertIn("no matching", out)

    def test_filter_by_tag_exact(self):
        # "arch" matches but "ar" does not (exact tag value, not substring)
        code, out = self.run_cmd("list", "--tag", "ar")
        self.assertEqual(code, 0)
        self.assertIn("no matching", out)


# ---------------------------------------------------------------------------
# accept / reject
# ---------------------------------------------------------------------------
class TestAcceptReject(LedgerTestCase):
    def test_accept(self):
        entry_id = self.log_entry()
        code, out = self.run_cmd("accept", entry_id)
        self.assertEqual(code, 0)
        rows = self.read_index()
        self.assertEqual(rows[0]["status"], "accepted")

    def test_reject(self):
        entry_id = self.log_entry()
        code, out = self.run_cmd("reject", entry_id, "--note", "not needed")
        self.assertEqual(code, 0)
        rows = self.read_index()
        self.assertEqual(rows[0]["status"], "rejected")

    def test_accept_nonexistent(self):
        code, _ = self.run_cmd("accept", "does-not-exist")
        self.assertEqual(code, 1)

    def test_accept_actionable_type_prints_execute_nudge(self):
        entry_id = self.log_entry(type_="plan")
        code, out = self.run_cmd("accept", entry_id)
        self.assertEqual(code, 0)
        self.assertIn("green light", out)

    def test_accept_non_actionable_type_prints_no_execute_nudge(self):
        entry_id = self.log_entry(type_="note")
        code, out = self.run_cmd("accept", entry_id)
        self.assertEqual(code, 0)
        self.assertNotIn("green light", out)


# ---------------------------------------------------------------------------
# supersede
# ---------------------------------------------------------------------------
class TestSupersede(LedgerTestCase):
    def test_supersede_marks_entry(self):
        entry_id = self.log_entry(title="Old decision", status="accepted")
        code, out = self.run_cmd("supersede", entry_id, "--note", "replaced")
        self.assertEqual(code, 0)
        self.assertIn("superseded", out)
        rows = self.read_index()
        self.assertEqual(rows[0]["status"], "superseded")

    def test_supersede_pending_entry(self):
        entry_id = self.log_entry(title="Pending decision", status="pending")
        code, out = self.run_cmd("supersede", entry_id)
        self.assertEqual(code, 0)
        rows = self.read_index()
        self.assertEqual(rows[0]["status"], "superseded")

    def test_supersede_nonexistent(self):
        code, _ = self.run_cmd("supersede", "does-not-exist")
        self.assertEqual(code, 1)


# ---------------------------------------------------------------------------
# dependents
# ---------------------------------------------------------------------------
class TestDependents(LedgerTestCase):
    def setUp(self):
        super().setUp()
        self.source_id = self.log_entry(type_="decision", title="Source decision", status="accepted")
        self.artifact1 = self.log_entry(
            type_="artifact", title="Functional manual",
            tags=f"docs,source:{self.source_id}", status="accepted",
        )
        self.artifact2 = self.log_entry(
            type_="artifact", title="Architecture diagram",
            tags=f"diagram,source:{self.source_id}", status="pending",
        )
        self.unrelated = self.log_entry(
            type_="artifact", title="Unrelated doc",
            tags="docs,source:other-id", status="accepted",
        )

    def test_finds_dependent_artifacts(self):
        code, out = self.run_cmd("dependents", self.source_id)
        self.assertEqual(code, 0)
        self.assertIn("Functional manual", out)
        self.assertIn("Architecture diagram", out)

    def test_excludes_unrelated_artifacts(self):
        code, out = self.run_cmd("dependents", self.source_id)
        self.assertNotIn("Unrelated doc", out)

    def test_excludes_non_artifact_entries(self):
        # source_id itself is a decision, not an artifact — should not appear
        code, out = self.run_cmd("dependents", self.source_id)
        self.assertNotIn("Source decision", out)

    def test_no_dependents(self):
        code, out = self.run_cmd("dependents", "no-such-id")
        self.assertEqual(code, 0)
        self.assertIn("no artifact entries", out)


# ---------------------------------------------------------------------------
# stale
# ---------------------------------------------------------------------------
class TestStale(LedgerTestCase):
    def setUp(self):
        super().setUp()
        self.source_id = self.log_entry(type_="decision", title="Core decision", status="accepted")
        self.art1 = self.log_entry(
            type_="artifact", title="Technical manual",
            tags=f"docs,source:{self.source_id}", status="accepted",
        )
        self.art2 = self.log_entry(
            type_="artifact", title="Sequence diagram",
            tags=f"diagram,source:{self.source_id}", status="pending",
        )
        self.unrelated = self.log_entry(
            type_="artifact", title="Unrelated artifact",
            tags="docs,source:other-id", status="accepted",
        )

    def test_marks_all_dependents_superseded(self):
        code, out = self.run_cmd("stale", self.source_id)
        self.assertEqual(code, 0)
        rows = {r["id"]: r for r in self.read_index()}
        self.assertEqual(rows[self.art1]["status"], "superseded")
        self.assertEqual(rows[self.art2]["status"], "superseded")

    def test_does_not_touch_unrelated_artifacts(self):
        self.run_cmd("stale", self.source_id)
        rows = {r["id"]: r for r in self.read_index()}
        self.assertEqual(rows[self.unrelated]["status"], "accepted")

    def test_reports_what_was_marked(self):
        code, out = self.run_cmd("stale", self.source_id)
        self.assertEqual(code, 0)
        self.assertIn("Technical manual", out)
        self.assertIn("Sequence diagram", out)
        self.assertIn("Regenerate", out)

    def test_no_dependents_reports_nothing_found(self):
        code, out = self.run_cmd("stale", "no-such-id")
        self.assertEqual(code, 0)
        self.assertIn("no dependent artifacts", out)

    def test_already_closed_entries_skipped(self):
        # Close art1 first, then stale — only art2 should be marked
        self.run_cmd("reject", self.art1)
        code, out = self.run_cmd("stale", self.source_id)
        self.assertEqual(code, 0)
        rows = {r["id"]: r for r in self.read_index()}
        self.assertEqual(rows[self.art1]["status"], "rejected")   # untouched
        self.assertEqual(rows[self.art2]["status"], "superseded")  # marked

    def test_all_already_closed_reports_nothing_changed(self):
        self.run_cmd("reject", self.art1)
        self.run_cmd("reject", self.art2)
        code, out = self.run_cmd("stale", self.source_id)
        self.assertEqual(code, 0)
        self.assertIn("nothing changed", out)


# ---------------------------------------------------------------------------
# status + pending
# ---------------------------------------------------------------------------
class TestStatusAndPending(LedgerTestCase):
    def test_status_empty(self):
        code, out = self.run_cmd("status")
        self.assertEqual(code, 0)
        self.assertIn("empty", out)

    def test_status_with_entries(self):
        self.log_entry(status="pending")
        self.log_entry(status="accepted")
        code, out = self.run_cmd("status")
        self.assertEqual(code, 0)
        self.assertIn("pending=1", out)
        self.assertIn("accepted=1", out)

    def test_pending_lists_pending_only(self):
        self.log_entry(title="Pending one", status="pending")
        self.log_entry(title="Accepted one", status="accepted")
        code, out = self.run_cmd("pending")
        self.assertEqual(code, 0)
        self.assertIn("Pending one", out)
        self.assertNotIn("Accepted one", out)


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------
class TestShow(LedgerTestCase):
    def test_show_prints_body(self):
        entry_id = self.log_entry(body="This is the body content.")
        code, out = self.run_cmd("show", entry_id)
        self.assertEqual(code, 0)
        self.assertIn("This is the body content.", out)

    def test_show_prefix_match(self):
        entry_id = self.log_entry()
        code, out = self.run_cmd("show", entry_id[:8])
        self.assertEqual(code, 0)

    def test_show_missing(self):
        code, _ = self.run_cmd("show", "does-not-exist")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
