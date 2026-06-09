# Praxis memory ledger

This directory is the project's **memory** — a versioned record of the plans,
decisions, implementations and artifacts produced while working with the praxis
SDLC experts. It is committed to git on purpose, so the record survives across
sessions and machines.

- `ledger.jsonl` — the index (one entry per line). Don't hand-edit; use the CLI.
- `entries/<id>.md` — the full content of each entry.
- `patches/<id>.patch` — a reverse-appliable diff for implementation entries,
  used by `rollback`.

Manage it with the `memory` skill or the `/memory` command, e.g.:

    /memory list pending
    /memory accept <id>
    /memory rollback <id>

Each entry moves through: **pending → accepted | rejected | rolled-back**.
