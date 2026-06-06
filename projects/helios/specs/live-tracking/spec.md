---
id: live-tracking
title: Live delivery tracking
project: helios
status: accepted
---

# Spec: Live delivery tracking

> **Example** cross-repo spec for the Helios product. It is the **single source of
> truth** for these requirements — every repo's tasks reference these `REQ-` ids;
> none copy the text. `status: accepted` means Gate 1 (Discovery & Research) and
> Gate 2 (Specification) passed, so the plan and tasks are authorized.
>
> Distilled from [`discovery/discovery-report.md`](discovery/discovery-report.md)
> and [`research/research-report.md`](research/research-report.md).

## Problem & scope

Let customers see their delivery's live location and ETA, and let ops monitor all
in-flight deliveries, so support contacts drop and lateness is caught early.
Spans all four repos. Driver-side location capture is **out of scope** (already
exists).

## Requirements

Functional and non-functional requirements. **Defined once, here.** Reference them
by id from anywhere (`SPEC-live-tracking/REQ-00n`).

### REQ-001 — Live driver location (customer)
The customer sees the driver's position on a map for their active delivery,
updated within 5 seconds of a new driver ping.

### REQ-002 — Live ETA (customer)
The customer sees an ETA that updates as the driver moves. ETA is computed by
`helios-workers` (see `ADR-002`).

### REQ-003 — Ops monitoring (console)
Ops see all in-flight deliveries with status and current ETA, sortable by
lateness risk.

### REQ-004 — Real-time transport
Location and ETA updates are pushed to the browser over **SSE** (see `ADR-001`),
not polling.

### REQ-005 — Latency (NFR)
p95 end-to-end update latency (driver ping → visible to customer) ≤ 5s at peak
load.

### REQ-006 — Authorization (NFR / security)
A delivery's location is visible only to the customer who owns the order and to
authorized ops users. Authz is enforced on the stream, not just the first request.

## Out of scope

- Driver-app location capture and routing source data.
- Historical playback of past deliveries.

## Open questions

- Project open-question **#1** (shared component library for `helios-web` /
  `helios-console`) is still open and gates only the shared-UI parts of `TASK-006`;
  see [`../../memory/open-questions.md`](../../memory/open-questions.md). #2
  (transport) is **resolved** by `ADR-001`.

## Traceability

- This spec id: `SPEC-live-tracking`
- Sources: discovery (`DISC-live-tracking`), research (`RES-live-tracking`),
  idea (`IDEA-HELIOS-42`)
- See [`../../../../rules/traceability.md`](../../../../rules/traceability.md).

## Upstream artifacts

- Discovery: [`discovery/discovery-report.md`](discovery/discovery-report.md)
- Research: [`research/research-report.md`](research/research-report.md), [`research/evidence-log.md`](research/evidence-log.md), [`research/alternatives.md`](research/alternatives.md)

## Downstream artifacts

- Decisions: [`decisions/ADR-001-realtime-transport.md`](decisions/ADR-001-realtime-transport.md), [`decisions/ADR-002-eta-in-workers.md`](decisions/ADR-002-eta-in-workers.md)
- Plan: [`plans/implementation-plan.md`](plans/implementation-plan.md)
- Tasks: [`tasks/tasks.md`](tasks/tasks.md)
- Verify report: [`reports/verify/report.md`](reports/verify/report.md)
- Release notes: [`reports/release/release-notes.md`](reports/release/release-notes.md)
