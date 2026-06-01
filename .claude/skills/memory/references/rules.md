# Rules — what to record and how

## What is worth a ledger entry

Record durable outcomes, not conversation. A good rule: *would the next person to
open this repo want to know this?*

| Record | Skip |
|--------|------|
| An architectural decision and its rationale (ADR-style) | A passing thought or half-formed idea |
| A consolidated plan from `/new-feature` | Each individual sentence of that plan |
| A test strategy or rollout plan | Restating something already recorded |
| A shipped change (as a `snapshot`, so it can be rolled back) | Exploratory edits you immediately discarded |
| A trade-off the team chose between | Pure Q&A with no decision |

When unsure and the artifact is significant, record it as `pending` — pending is
cheap and the user can reject it.

## How to write each type

- **decision** — mini-ADR. Four short parts: **Context** (what forced the
  decision), **Decision** (what was chosen), **Rationale** (why, including
  alternatives rejected), **Consequences** (what this commits us to / trades
  away). This is the highest-value entry type — write it well.
- **plan** — the goal, the ordered increments, and the acceptance/Definition of
  Done. Link or name the deciding artifacts.
- **implementation** — prefer `snapshot`; the body lists touched files and points
  at the rollback patch. Add a sentence on *what* the change does.
- **test-strategy / rollout** — the QA or DevOps artifact: key cases & risks, or
  pipeline gates, deploy strategy, rollback, and observability.
- **artifact / note** — anything else durable (a diagram path, a research
  finding, an interface contract).

## Provenance

Always set `--source` to the command or skill that produced the entry
(`/new-feature`, `/architect`, `/review-changes`, `auto` for hook snapshots,
`manual` for ad-hoc). Provenance is what lets someone later ask "what did the
architect decide?" and get a clean answer.

## Status discipline

- New entries are `pending` unless the user already approved them.
- Only the **user** moves an entry to `accepted` or `rejected`. Don't presume.
- Use `--supersedes` when a new decision replaces an old one — keep the history,
  don't delete.
- `rolled-back` is reserved for implementations that were actually reverted via
  `rollback` (see [../workflows/rollback.md](../workflows/rollback.md)).

## Hygiene

- One rich entry per artifact beats many fragments.
- Never hand-edit `ledger.jsonl` — use the CLI so the index and files stay
  consistent.
- Don't record secrets, credentials, or tokens in an entry body or a snapshot.
- The ledger is committed to git; write entries as if a teammate will read them.
