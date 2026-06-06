# Research Report — Live delivery tracking

> Step 2 of `feature-development`. **Research precedes the spec.** Reuse > Extend
> > Build. **Example** artifact.

## Questions

1. WebSocket or SSE for pushing location/ETA updates to the browser?
2. Where should ETA be computed, and how fresh must updates be?

## Findings

- **SSE fits this use case.** Updates are server→client only (location, ETA); SSE
  is simpler to operate behind the existing HTTP stack, auto-reconnects, and needs
  no new protocol on the API edge. WebSocket's bidirectionality buys nothing here.
  Backed by EV-001/EV-002.
- **ETA already has a home.** `helios-workers` consumes driver pings and runs the
  routing/ETA logic today for internal metrics; exposing it is *extend*, not
  *build*. Backed by EV-003.
- **Map component is reusable.** `helios-web` already renders a map for address
  selection; the live marker is an extension. Backed by EV-004.

## Existing solutions & reusable assets

- `helios-workers` routing/ETA module (extend).
- `helios-web` map component + design tokens (reuse).
- Existing auth middleware in `helios-api` for per-order ownership checks (reuse).

## Technical constraints discovered

- p95 end-to-end update latency target ≤ 5s to feel "live".
- Authz must be enforced on the stream, not just the initial request.

## Recommendation

Deliver tracking over **SSE**, ETA computed in `helios-workers` and published via
the API, map reused in `helios-web`, ops view in `helios-console`. Alternatives
weighed in [`alternatives.md`](alternatives.md); transport choice recorded as
`ADR-001`.

## Traceability

- This artifact id: `RES-live-tracking`
- Sources: discovery (`DISC-live-tracking`)
- Feeds: spec (`SPEC-live-tracking`)
