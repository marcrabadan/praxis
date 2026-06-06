# Verify Report — <bug title>

> Step `verify`. Evidence the bug is fixed and stays fixed.

## Result

`fixed | not-fixed`.

## Evidence

- Regression test: name + that it now passes (and failed before the fix).
- Manual/automated reproduction: the original repro steps no longer trigger the
  bug.
- Wider regression: relevant suite is green.

## Traceability

- Verifies fix for: `BUG-<NNN>`
