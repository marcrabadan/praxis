# Implementation Plan — Live delivery tracking

> How the accepted spec is built across the four repos. **Example.** Tasks (with
> owners and per-repo grouping) live in [`../tasks/tasks.md`](../tasks/tasks.md).

## Approach

One feature, four repos, **one** spec. Data flows:

```
driver pings → helios-workers (ingest + ETA) → helios-api (SSE relay, authz)
                                                   ├──► helios-web      (customer map + ETA)
                                                   └──► helios-console  (ops dashboard)
```

The API contract (`helios-api/openapi.yaml`) is updated first; frontend repos
build against it. SSE per `ADR-001`; ETA in workers per `ADR-002`.

## Components / files to touch

| Repo | Area | Notes |
|------|------|-------|
| `helios-api` | `openapi.yaml`, tracking route, authz middleware | Canonical contract + SSE endpoint (`REQ-001/004/006`) |
| `helios-workers` | `routing/eta.py`, ping ingestion, publisher | Extend existing ETA module (`REQ-002/005`) |
| `helios-web` | `components/Map`, tracking page, `EventSource` client | Reuse map + design tokens (`REQ-001/002/004`) |
| `helios-console` | ops deliveries dashboard | All in-flight + lateness (`REQ-003`) |

## Build order

1. `helios-api` contract + SSE endpoint stub (unblocks both frontends).
2. `helios-workers` ETA publish + ping ingestion.
3. `helios-web` customer tracking page; `helios-console` ops dashboard (parallel).
4. Authz hardening across the stream; load test against the latency NFR.

## Risks / assumptions

- Fan-out load (`REQ-005`) — load-test before release.
- Authz on the stream (`REQ-006`) — security review required (project authority note).

## Traceability

- Plan for: `SPEC-live-tracking`
- Source: `SPEC-live-tracking`; decisions `ADR-001`, `ADR-002`
- Traces: `tasks/tasks.md`
