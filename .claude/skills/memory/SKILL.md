---
name: memory
description: Persist and manage the project's working memory — a versioned ledger of plans, decisions, implementations, and artifacts produced across the praxis SDLC experts and commands, each with an accept / pending / rollback lifecycle. Use when the user wants to remember, record, save, or log what was decided or built; review or accept/reject pending decisions; roll back a change; or ask "what did we decide / build / plan". Also triggers automatically (via the opt-in hook) so every command and skill leaves a durable record.
tier: 4
version: 1.0.0
---

# Memory

The project's **working memory**. A versioned ledger that captures what the team
plans, decides, builds, and ships while working with the praxis experts — so the
record survives across sessions, machines, and the next person to open the repo.

It answers three recurring needs:

1. **Remember** — record plans, decisions (ADR-style, from *any* SDLC role — not
   just the architect), implementations, and artifacts as durable, git-committed
   entries.
2. **Decide** — every entry carries one status from a closed set
   (`pending → accepted | rejected`, plus `superseded` and `rolled-back`). You can
   see at a glance what is still awaiting a call. **Pending is a proposal awaiting
   the user — not a licence to act on it.**
3. **Undo** — implementation entries store a reverse-appliable patch, so a change
   can be **rolled back** even sessions later.

The bookkeeping is deterministic — done by `scripts/ledger.py`, never by guesswork.
Your job is to decide *what is worth remembering* and to write the entry body well.

## Where memory lives

Committed to the consuming repo under `.praxis/memory/` (git root):

```
.praxis/memory/
  ledger.jsonl        index — one entry per line (managed by the CLI)
  entries/<id>.md      full content: frontmatter + markdown body
  patches/<id>.patch   reverse-appliable diff (implementation entries)
  README.md            explains the directory
```

Entry types: `plan`, `decision`, `implementation`, `artifact`, `test-strategy`,
`rollout`, `note`. Statuses: `pending`, `accepted`, `rejected`, `rolled-back`,
`superseded` — this is the **complete, closed set**; the CLI enforces it, so
never invent a new status. See [references/rules.md](references/rules.md) for what
each one means.

## When to use

- "Remember / save / log this decision (plan, design, result)."
- "Initialize / bootstrap / seed memory" → prime an empty ledger from the repo's
  existing context (`/memory init`). Do this once when adopting praxis in a repo.
- "What did we decide / build / plan for X?" → read the ledger.
- "Show me what's pending." / "Accept this." / "Reject that."
- "Roll back that change / undo what we just did."
- Implicitly at the **end of a command** (`/new-feature`, `/review-changes`, an
  expert consult) — record the artifact it produced. See the always-on rule below.

## When not to use

- Throwaway exploration or chit-chat with no durable outcome — don't clutter the
  ledger. Record decisions and artifacts, not every message.
- Configuring *automatic* behavior — that's a hook, not memory. See
  [references/automation.md](references/automation.md).
- The user wants the change itself, not a record of it — just do the work
  (a snapshot can capture it afterward).

## Workflows

| Mode | File | When |
|------|------|------|
| Bootstrap | [workflows/bootstrap.md](workflows/bootstrap.md) | Prime an empty ledger from the repo's existing context (`/memory init`) |
| Capture | [workflows/capture.md](workflows/capture.md) | Record a plan, decision, implementation, or artifact |
| Review | [workflows/review.md](workflows/review.md) | List, inspect, and accept/reject pending entries |
| Rollback | [workflows/rollback.md](workflows/rollback.md) | Undo a snapshotted implementation |

## Always-on rule — leave a record

After any command or skill produces a **durable artifact** — a plan, an
architectural decision, a test strategy, a rollout plan, or a shipped change —
record it before ending the turn, unless the user opted out. Prefer one rich
entry per artifact over many thin ones. Follow [workflows/capture.md](workflows/capture.md).

This is reinforced automatically by the opt-in hook (see
[references/automation.md](references/automation.md)), which surfaces pending
entries at session start and snapshots uncommitted changes when you stop.

## The CLI

All state changes go through the script — do not hand-edit `ledger.jsonl`:

```bash
python .claude/skills/memory/scripts/ledger.py <command>
```

| Command | Purpose |
|---------|---------|
| `init` | Create the ledger directory (idempotent) |
| `bootstrap [--brief]` | Init, then report the repo's existing context (docs + git history) to seed an empty ledger from — see [workflows/bootstrap.md](workflows/bootstrap.md) |
| `log --type T --title "..." --source /cmd [--tags a,b] [--body "..."]` | Append an entry |
| `snapshot [--source /cmd] [--title "..."] [--since REF]` | Capture the current diff as a rollback-able implementation |
| `list [--status pending] [--type decision] [--source /architect]` | List entries |
| `pending [--brief]` | Show pending entries (brief = hook/context form) |
| `show <id>` | Print an entry's full body |
| `accept <id> [--note "..."]` / `reject <id> [--note "..."]` | Advance the lifecycle |
| `rollback <id> [--dry-run]` | Reverse-apply an implementation's patch |
| `status` | Counts by status and type |

See [references/ledger-format.md](references/ledger-format.md) for the entry
schema and [references/rules.md](references/rules.md) for what to record and how
to write a good entry.

## Output expectations

- A capture ends with the new entry id and a one-line confirmation of what was
  recorded and its status.
- A review presents pending entries clearly and only changes status on explicit
  user intent.
- A rollback reverts the working tree, marks the entry `rolled-back`, and tells
  the user to review `git diff` and commit.

## Stop conditions

- The artifact is recorded (or the user declined) and the new id is reported.
- The requested entries have been listed / shown / re-statused.
- The rollback applied (or was reported as not cleanly appliable) and the user
  knows the next step.
