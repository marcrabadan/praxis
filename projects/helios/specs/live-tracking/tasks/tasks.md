# Tasks — Live delivery tracking

> **Grouped by repo**, so each team works its own repo's list. Every task
> **references** a requirement by id (`SPEC-live-tracking/REQ-00n`) — the
> requirement text is **never copied here**; it lives once in
> [`../spec.md`](../spec.md). Task ids (`TASK-00n`) are scoped to this spec.
> **Example** content.
>
> Ownership shows how concurrent teams divide one spec without touching each
> other's files. Status: `[ ]` todo · `[~]` in progress · `[x]` done.

## helios-api  · owner: Team Tracking
- [x] **TASK-001** — Define the tracking endpoint in `openapi.yaml` (canonical contract first). _implements_ `SPEC-live-tracking/REQ-004`
- [~] **TASK-002** — Implement the SSE endpoint `GET /deliveries/{id}/track`, relaying ETA from workers. _implements_ `SPEC-live-tracking/REQ-001`, `SPEC-live-tracking/REQ-002`
- [ ] **TASK-003** — Enforce per-order authz on the stream (customer-owns-order + ops role). _implements_ `SPEC-live-tracking/REQ-006`

## helios-workers  · owner: Team Tracking
- [~] **TASK-004** — Ingest driver location pings into the tracking pipeline. _implements_ `SPEC-live-tracking/REQ-001`
- [ ] **TASK-005** — Compute and publish live ETA from pings (extend `routing/eta.py`). _implements_ `SPEC-live-tracking/REQ-002` · _per_ `ADR-002`
- [ ] **TASK-006** — Load test the pipeline to the latency NFR. _implements_ `SPEC-live-tracking/REQ-005`

## helios-web  · owner: Team Tracking
- [ ] **TASK-007** — Customer tracking page: reuse `components/Map`, render live marker + ETA via `EventSource`. _implements_ `SPEC-live-tracking/REQ-001`, `SPEC-live-tracking/REQ-002`, `SPEC-live-tracking/REQ-004`

## helios-console  · owner: Team Ops
- [ ] **TASK-008** — Ops dashboard: list all in-flight deliveries with status + ETA, sort by lateness. _implements_ `SPEC-live-tracking/REQ-003`
  - ⛔ Blocked on project open-question **#1** (shared component library) for the shared UI parts only — see [`../../../memory/open-questions.md`](../../../memory/open-questions.md).

## Traceability

- Tasks for: `SPEC-live-tracking`
- Each task traces to its `SPEC-live-tracking/REQ-00n`; commits cite their `TASK-00n`.
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
