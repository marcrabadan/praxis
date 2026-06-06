# Open Questions

Unresolved questions that affect **Helios**. An open question that gates the step
in front of you is a **stop condition** — resolve it (ask the user) before
proceeding on the work it blocks. See
[`../../../rules/stop-conditions.md`](../../../rules/stop-conditions.md).

| # | Question | Blocks | Raised | Status |
|---|----------|--------|--------|--------|
| 1 | Do `helios-web` and `helios-console` share one component library, or two? | `TASK-008` shared-UI parts | 2026-06-06 | open |
| 2 | Is real-time tracking delivered over WebSocket or SSE? | Tracking feature spec | 2026-06-06 | resolved → SSE (`specs/live-tracking/decisions/ADR-001-realtime-transport.md`) |

## Conventions

- **Status** is `open` or `resolved`. When resolved, record the answer where it
  belongs (a project decision in `decisions/`, or the memory ledger) and link it
  here, then mark the row `resolved` — don't delete it.
- **Blocks** names what cannot proceed while the question is open. If nothing is
  blocked, it is a note, not a stop condition.
