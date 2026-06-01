---
description: Manage the project's working-memory ledger — record plans/decisions/implementations, review what's pending, accept or reject entries, and roll back a snapshotted change. Use to remember what was decided or built, or to undo a change.
argument-hint: "[init|list|pending|show|accept|reject|rollback|status|log|snapshot] [id or details] — omit to see status + pending"
---

Manage the praxis **memory ledger** for this repo using the `memory` skill. The
ledger is the versioned record of plans, decisions, implementations, and
artifacts, each with a `pending → accepted | rejected | rolled-back` lifecycle.

Request:

$ARGUMENTS

## How to handle it

Load the `memory` skill and route on the request above. The skill's CLI is
`python .claude/skills/memory/scripts/ledger.py`.

- **"init" / "bootstrap" / "seed memory"** → prime the ledger from the repo's
  existing context. Follow [.claude/skills/memory/workflows/bootstrap.md](../skills/memory/workflows/bootstrap.md):
  run `bootstrap`, then record the project's already-made decisions as `pending`
  entries. If the ledger already has entries, surface them instead of re-seeding.
- **No arguments, or "status" / "what's pending"** → show `status` then
  `pending`, and give a one-line human summary.
- **"list ..."** → `list` with the matching `--status` / `--type` / `--source`
  filter. Follow [.claude/skills/memory/workflows/review.md](../skills/memory/workflows/review.md).
- **"show <id>"** → print the entry's full body.
- **"accept <id>" / "reject <id>"** → advance the lifecycle. Only on explicit
  user intent; confirm the new status.
- **"rollback <id>"** → follow
  [.claude/skills/memory/workflows/rollback.md](../skills/memory/workflows/rollback.md):
  dry-run first, revert the working tree only, never commit, then tell the user to
  review `git diff`.
- **"log ..." / "remember ..." / "snapshot ..."** → record a new entry per
  [.claude/skills/memory/workflows/capture.md](../skills/memory/workflows/capture.md).
  Default new entries to `pending`.

Never hand-edit `.praxis/memory/ledger.jsonl` — always go through the CLI so the
index and entry files stay consistent. Report the entry id(s) you touched.
