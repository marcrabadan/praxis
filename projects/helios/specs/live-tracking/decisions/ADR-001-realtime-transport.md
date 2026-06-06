# ADR-001 — Real-time transport: SSE

> Spec-scoped decision (`ADR-001` within `SPEC-live-tracking`). Resolves project
> open-question #2. **Example.**

## Context

We need to push location and ETA updates to the browser with p95 ≤ 5s freshness
(`SPEC-live-tracking/REQ-004`, `SPEC-live-tracking/REQ-005`), without standing up
new edge infrastructure if we can avoid it.

## Options

See [`../research/alternatives.md`](../research/alternatives.md): SSE, WebSocket,
polling.

## Decision

Use **Server-Sent Events (SSE)** over the existing HTTP stack. Authz is enforced
on the stream per `SPEC-live-tracking/REQ-006`.

## Consequences

- `helios-api` exposes an SSE endpoint; no new gateway to operate.
- Browser clients use the native `EventSource` with auto-reconnect.
- If true bidirectional needs appear later, revisit (this ADR would be superseded).

## Status

accepted

## Traceability

- Decides: `SPEC-live-tracking/REQ-004`
- Source: `RES-live-tracking`, `ALT-live-tracking`
