---
id: web-map-perf
title: Reduce re-renders on the live map
project: helios
type: refinement
status: in-progress
---

# Refinement: Reduce re-renders on the live map

> **Example** `refinement` for Helios — quality-only, **behavior-preserving**.

## Motivation

The `helios-web` map re-renders the whole layer on every location event, causing
jank on low-end phones during live tracking. Pure rendering cost; the displayed
result is already correct.

## Scope

In: memoize marker rendering and update only the changed marker on each event
(`components/Map`). Out: any change to what is shown, the data, or the SSE contract.

## Baseline (behavior to preserve)

- Existing `helios-web` map component tests (green).
- A visual snapshot of the tracking page for a scripted sequence of 50 location
  events; the final rendered DOM/markers must match before and after.
- A render-count probe and an FPS measurement on a throttled-CPU profile as the
  before/after numbers.

## Success measure

- Re-renders per location event drop from O(all markers) to O(1).
- Snapshot identical (behavior unchanged); FPS on the throttled profile improves.

## Traceability

- This refinement id: `REF-web-map-perf`
- Related: `SPEC-live-tracking/REQ-001` (the live map it speeds up)
