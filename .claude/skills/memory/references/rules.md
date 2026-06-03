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

- **decision** — mini-ADR, and **not the architect's alone**. Every SDLC role
  makes decisions worth recording: the PO commits to a prioritization call, the
  BA fixes a scope or process choice, QA sets the test strategy and entry/exit
  criteria, DevOps picks a deploy strategy or rollback trigger, Security accepts
  or defers a risk, Data fixes a modeling choice, ML picks the metric and
  threshold, the frontend/UX experts choose a rendering strategy or an
  accessibility trade-off. Whatever the source, write four short parts:
  **Context** (what forced the decision), **Decision** (what was chosen),
  **Rationale** (why, including alternatives rejected), **Consequences** (what
  this commits us to / trades away). This is the highest-value entry type — write
  it well, and set `--source` to the role that made the call so "what did QA /
  the PO / security decide?" gets a clean answer.
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
(`/new-feature`, `/architect`, `/product`, `/qa`, `/devops`, `/security`,
`/review-changes`, `auto` for hook snapshots, `manual` for ad-hoc). Provenance is
what lets someone later ask "what did the *PO* / *QA* / *the architect* decide?"
and get a clean answer — decisions come from every role, so the source must
identify which one.

## Statuses — the closed set

Every entry carries exactly one status from this **closed, authoritative set**.
These five are the *only* statuses — never invent another (no `in-progress`,
`approved`, `on-hold`, `draft`, `super-seeded`, …). The CLI enforces it
(`--status` is a fixed `choices=` list and the lifecycle transitions are
hard-coded), so the only way to get a bogus status into the ledger is to
hand-edit it — which you must not do.

| Status | Meaning |
|--------|---------|
| `pending` | Logged but not yet decided — a **proposal awaiting the user's call**. |
| `accepted` | The user approved it; the team may act on it. |
| `rejected` | The user declined it; do not act on it. |
| `superseded` | Replaced by a later entry — set **automatically** via `--supersedes`, never by hand. Kept for history. |
| `rolled-back` | An implementation that was actually reverted via `rollback`. |

## Status discipline

- New entries are `pending` unless the user already approved them.
- Only the **user** moves an entry to `accepted` or `rejected`. Don't presume.
- **Pending is not approval — don't execute on it.** A `pending` decision or plan
  is a proposal, not a green light. Surface it and get an explicit `accept` before
  carrying out the work it authorizes; recording a decision is not the same as
  being allowed to act on it. (Planning-only runs like `/new-feature` legitimately
  end with everything `pending` — they propose, they don't ship.)
- Use `--supersedes` when a new decision replaces an old one — the old entry flips
  to `superseded` automatically; keep the history, don't delete.
- `rolled-back` is reserved for implementations that were actually reverted via
  `rollback` (see [../workflows/rollback.md](../workflows/rollback.md)).

## Hygiene

- One rich entry per artifact beats many fragments.
- Never hand-edit `ledger.jsonl` — use the CLI so the index and files stay
  consistent.
- Don't record secrets, credentials, or tokens in an entry body or a snapshot.
- The ledger is committed to git; write entries as if a teammate will read them.
