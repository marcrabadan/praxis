# Refine Plan — Reduce re-renders on the live map

> Step `plan`. Ordered, behavior-preserving steps.

## Approach

Split the marker layer so each marker is a memoized component keyed by driver id;
on a location event, update only that marker's props instead of rebuilding the
layer. No change to map appearance or data.

## Steps

1. Capture the 50-event snapshot + render-count/FPS baseline.
2. Memoize the marker component; key by driver id. Snapshot stays identical.
3. Switch the event handler to update a single marker. Snapshot stays identical.
4. Re-measure render count + FPS.

## Behavior-preserving evidence

After each step: component tests pass and the 50-event snapshot is identical. Only
the render-count/FPS numbers change.

## Rollback

Each step is its own commit; revert to restore the prior rendering path.

## Traceability

- Refines: `REF-web-map-perf`
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
