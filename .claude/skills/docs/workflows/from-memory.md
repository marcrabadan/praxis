# Workflow — Docs from Memory

Generate documentation by rendering memory ledger entries into structured Markdown files.

## When you reach here

The user wants documentation derived from what the team has already decided and planned — not from raw code. Typical triggers: "document our decisions", "write ADRs from the ledger", "generate the architecture doc", "what have we built so far".

## Steps

### 1. Read the ledger

```bash
python .claude/skills/memory/scripts/ledger.py list --status accepted
python .claude/skills/memory/scripts/ledger.py list --status pending
```

If the ledger does not exist, tell the user and suggest running `/memory init` first.

### 2. Determine scope

From the user's request and the ledger contents, decide which entries to render:

| User asks for… | Pull these entry types |
|----------------|------------------------|
| Architecture doc | `plan`, `decision` (arch/design tags) |
| ADRs | `decision` entries, especially those tagged `arch` or `adr` |
| What we've built | `implementation`, `snapshot` |
| Test strategy | `test-strategy` |
| Runbook / deploy guide | `rollout`, `decision` (deploy/infra tags) |
| Everything | all accepted entries, grouped by type |

If the scope is still ambiguous after reading the ledger, ask one clarifying question.

### 3. Group and order entries

- **Decisions** → one ADR per entry (or one consolidated architecture doc if entries are closely related).
- **Plans** → one architecture or design doc per feature/system.
- **Implementations** → changelog-style or per-module reference.
- **Test strategies** → test plan doc.
- **Rollouts** → runbook or release-notes doc.

### 4. Select the format

Use [references/formats.md](../references/formats.md) to pick the right document shape for each group. Run the [references/checklist.md](../references/checklist.md) before writing.

### 5. Write the documents

For each document:

1. Use `ledger.py show <id>` to read the full entry body.
2. Synthesise into the chosen format — do not copy-paste raw ledger text; rewrite for a reader who was not in the room.
3. Set the output path (default from [references/formats.md](../references/formats.md) unless the user specified one).
4. Write the file.

### 6. Record to the ledger

For each file written, include a `source:<id>` tag for every ledger entry that
contributed to the document. This enables rollback to find and mark this artifact
stale automatically when any source entry is rolled back.

```bash
python .claude/skills/memory/scripts/ledger.py log \
  --type artifact \
  --title "<doc type>: <slug>" \
  --source /docs \
  --tags "docs,generated,source:<id1>,source:<id2>,..." \
  --body "Generated <type> from ledger entries <ids>. Path: <path>."
```

Leave the entry `pending` for the user to accept.

### 7. Report

List each file written with its path and the ledger entry IDs it was derived from. Note any entries that were skipped and why (e.g. still `pending`, too thin to render).
