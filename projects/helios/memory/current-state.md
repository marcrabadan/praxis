# Current State

A living snapshot of where **Helios** is right now. First thing an agent reads
after `PROJECT.md`. Keep it short and current.

> This is **example** content to show the shape of a populated multi-repo
> project. Replace it with your product's real state.

## Now

- **`SPEC-live-tracking`** is the active spec (status: accepted) — build underway
  across all four repos. Team Tracking owns api/workers/web; Team Ops owns the
  console dashboard. See `specs/live-tracking/tasks/tasks.md`.
- Also in flight: `BUG-sse-reconnect-stale-marker` (fix under review) and
  `REF-web-map-perf` (in progress). Recently closed:
  `BUG-coupon-total-mismatch`, `REF-extract-pricing-calculator`.

## Recently landed

- 2026-06-06 — Accepted `SPEC-live-tracking` (Gate 1 + Gate 2 passed).
- 2026-06-06 — Adopted central-mode harness across `helios-api`, `helios-workers`,
  `helios-web`, `helios-console`.

## Active spec

- `specs/live-tracking/` — Live delivery tracking (accepted, building)

## Known constraints

- The API contract (`helios-api/openapi.yaml`) is canonical; frontend repos must
  not assume undocumented shapes.
- Design tokens are owned by `helios-web` and shared with `helios-console`.

## Pointers

- Accepted patterns: `accepted-patterns/` _(add when the first one exists)_
- Previous failures to avoid repeating: `previous-failures/` _(add when relevant)_
- Decisions: `decisions/` _(add when the first decision is recorded)_
