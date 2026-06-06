# Root Cause — Live marker freezes after the SSE stream reconnects

> Step `diagnose`. Evidenced.

## Root cause

The `EventSource` `onmessage` handler is registered inside a `useEffect` that
captures the *initial* marker-update closure. On reconnect the browser reuses the
same `EventSource`, but the component's effect re-runs and a **stale** handler
(closing over the first render's state setter target) keeps handling events, so
updates no longer reach the live marker state. `helios-web` tracking page.

## Evidence

Logging in the handler shows events still firing after reconnect, but the state
setter writes to a stale ref. Removing the stale closure (see fix plan) restores
updates.

## Why it was not caught

Tests covered the happy-path stream; no test simulated a reconnect.

## Blast radius

Only the tracking page's SSE subscription. The ops console (`TASK-008`) uses a
separate subscription and is unaffected.

## Traceability

- Root cause for: `BUG-sse-reconnect-stale-marker`
- Relates to: `SPEC-live-tracking/REQ-004` (SSE transport)
