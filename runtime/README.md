# Runtime state

**Disposable session glue — not durable doctrine.** This directory holds the
agent's *runtime* state: which project/repo/spec was last active, the most
recent command, and an append-only activity log. It is the harness equivalent of
a scratchpad.

| File | What it holds |
|------|---------------|
| `session-state.json` | Current pointers — last active project, repo, spec, command. Shape: [`../schemas/session-state.schema.json`](../schemas/session-state.schema.json). |
| `activity-log.jsonl` | Append-only events (set, adapter-install, command runs), one JSON object per line. |

Both files are **git-ignored** — they are session-local and reconstructable, so
they are never committed. Only this README and the schema are tracked.

## Durable vs runtime — the line

| Durable (committed) | Runtime (disposable) |
|---------------------|----------------------|
| Project decisions (`projects/<p>/memory/decisions/`) | Last active project/repo/spec |
| The memory ledger (`.praxis/memory/`) | Recent command runs |
| Specs, accepted patterns, current state | Adapter install events |

**Never store a major decision only in runtime.** If it matters past this
session, it belongs in project memory or the ledger.

## CLI

Managed deterministically by [`../tools/runtime.py`](../tools/runtime.py):

```sh
python tools/runtime.py init
python tools/runtime.py set --project checkout --spec oauth --command /new-feature
python tools/runtime.py log --type adapter-install --note "codex"
python tools/runtime.py show
```
