# Verify Report — Live delivery tracking

> Step `verify`. Evidence the build meets the spec's acceptance criteria.
> **Example — in progress**, shown to illustrate where verification lands.

## Status

in progress (build underway — see [`../../tasks/tasks.md`](../../tasks/tasks.md))

## Acceptance checks (per requirement)

| Requirement | Check | Result |
|-------------|-------|--------|
| `REQ-001` | Customer sees live marker, updates ≤5s | ⏳ pending |
| `REQ-002` | ETA updates as driver moves | ⏳ pending |
| `REQ-003` | Ops dashboard lists in-flight + ETA | ⏳ pending |
| `REQ-004` | Updates over SSE (not polling) | ⏳ pending |
| `REQ-005` | p95 update latency ≤5s at peak (load test) | ⏳ pending |
| `REQ-006` | Authz enforced on the stream (security review) | ⏳ pending |

## Traceability

- Verifies: `SPEC-live-tracking`
- Gate 4 (Release) opens only when every check above passes.
