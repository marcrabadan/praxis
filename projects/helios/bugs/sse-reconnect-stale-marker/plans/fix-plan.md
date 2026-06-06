# Fix Plan — Live marker freezes after the SSE stream reconnects

> Step `fix`. Minimal change to restore updates after reconnect.

## Approach

In the `helios-web` tracking page, keep the latest marker-update callback in a ref
and have the single `onmessage` handler call `ref.current`, so reconnects always
dispatch to the current state setter. Subscribe/unsubscribe the `EventSource`
exactly once for the page's lifetime.

## Regression test

Component test that mounts the page, emits an event, simulates a reconnect, emits
another event, and asserts the marker position updates **after** the reconnect.
Fails before the fix.

## Risk & side effects

Localized to the tracking page subscription; no transport/contract change.

## Traceability

- Fixes: `BUG-sse-reconnect-stale-marker`
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
