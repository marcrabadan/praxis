---
id: sse-reconnect-stale-marker
title: Live marker freezes after the SSE stream reconnects
project: helios
type: bug
severity: medium
status: in-progress
---

# Bug: Live marker freezes after the SSE stream reconnects

> **Example** `bug-fix` for Helios — a defect found in a feature still being built
> (`SPEC-live-tracking`). It links the owning spec for traceability.

## Summary

On the customer tracking page, if the network blips and the `EventSource`
reconnects, the driver marker stops updating even though new events arrive.

## Severity & impact

`medium` — the page looks broken until reload; no data is wrong, no money at risk.
Hits users on flaky mobile networks.

## Steps to reproduce

1. Open a delivery's tracking page (`helios-web`).
2. Toggle the network off for ~5s, then on (forces SSE reconnect).
3. Observe new location events in the network tab.

**Expected:** marker resumes moving.
**Actual:** marker stays at the last pre-disconnect position.

## Environment

`helios-web` tracking page (`TASK-007`), feature branch for `SPEC-live-tracking`.

## Reproduction status

`reproduced` — consistent with throttled network in the browser dev tools.

## Traceability

- This bug id: `BUG-sse-reconnect-stale-marker`
- Found in: `SPEC-live-tracking/REQ-001` (live driver location)
- Downstream: [`root-cause.md`](root-cause.md), [`plans/fix-plan.md`](plans/fix-plan.md)
