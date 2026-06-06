# Fix Plan — <bug title>

> Step `fix`. The minimal change that restores expected behavior — nothing more.
> Expanding behavior here is a stop condition (that would be a feature).

## Approach

The fix, in terms of files/functions to change. Keep it minimal and targeted.

## Regression test

The test that fails before the fix and passes after. Required: `verify` is gated
on `regression-test`.

## Risk & side effects

What this change could affect; how the blast radius from the root cause is
covered.

## Traceability

- Fixes: `BUG-<NNN>`
- Implements decision: `ADR-<NNN>` (if any)
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
