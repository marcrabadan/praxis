# ADR-002 — Compute ETA in helios-workers

> Spec-scoped decision (`ADR-002` within `SPEC-live-tracking`). **Example.**

## Context

ETA must update live (`SPEC-live-tracking/REQ-002`). Routing/ETA logic already
exists in `helios-workers`; the project authority note says ETAs are computed
there, not in the API.

## Decision

`helios-workers` computes ETA from driver pings and publishes it; `helios-api`
only relays the latest ETA over the SSE stream. The API does **not** re-implement
ETA.

## Consequences

- Single ETA implementation (no drift between API and workers).
- API stays thin; workers own the compute and the load.

## Status

accepted

## Traceability

- Decides: `SPEC-live-tracking/REQ-002`
- Source: `RES-live-tracking`
