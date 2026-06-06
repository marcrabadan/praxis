# Alternatives Analysis — Live delivery tracking

> The transport options considered. The chosen one becomes `ADR-001`. **Example.**

## Options

### Option A — Server-Sent Events (SSE)  ← chosen
- **Summary:** Server streams location/ETA events over a long-lived HTTP response.
- **Pros:** Simple over existing HTTP stack; auto-reconnect; easy authz on the
  request; low ops overhead.
- **Cons:** Server→client only (fine here); one connection per stream.
- **Reuse posture:** extend (no new edge protocol).

### Option B — WebSocket
- **Summary:** Full-duplex socket between browser and a gateway.
- **Pros:** Bidirectional; mature libraries.
- **Cons:** New gateway/protocol to operate and secure; bidirectionality unused.
- **Reuse posture:** build.

### Option C — Client polling
- **Summary:** Browser polls `GET /track` every few seconds.
- **Pros:** Trivial.
- **Cons:** Latency vs load trade-off is poor at ≤5s freshness; wasteful.
- **Reuse posture:** reuse but doesn't meet the latency NFR.

## Recommendation

**Option A (SSE).** Meets the ≤5s freshness NFR with the least new infrastructure.
Recorded as [`../decisions/ADR-001-realtime-transport.md`](../decisions/ADR-001-realtime-transport.md).

## Traceability

- This artifact id: `ALT-live-tracking` (part of `RES-live-tracking`)
- Feeds: spec (`SPEC-live-tracking`), decision (`ADR-001`)
