# Verify Report — <bug title>

> Step `verify`. Evidence the bug is fixed and stays fixed. A bounded convergence
> loop (returns to `fix` until every gate passes). The fixer does not self-certify
> — only this report with real gate results closes the bug.

## Gate results

| Gate | Result | Evidence |
|------|--------|----------|
| G-repro-gone | pass \| fail | the documented repro no longer fails |
| G-regression-test | pass \| fail | new test fails before the fix, passes after |
| G-tests | pass \| fail | full suite green |
| G-build | pass \| fail | exit 0 |

## Result

`fixed | not-fixed`.

## Traceability

- Verifies fix for: `BUG-<NNN>`
