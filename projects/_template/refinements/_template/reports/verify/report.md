# Verify Report — <refinement title>

> Step `verify`. Evidence behavior is unchanged and the goal was met. A bounded
> convergence loop (returns to `change` until every gate passes). The author does
> not self-certify — only this report with real gate results closes the work.

## Gate results

| Gate | Result | Evidence |
|------|--------|----------|
| G-behavior-preserved | pass \| fail | behavior matches the recorded baseline |
| G-no-api-change | pass \| fail | public surface unchanged |
| G-tests | pass \| fail | suite green before and after |
| G-build | pass \| fail | exit 0 |

## Result

`done | reverted`.

## Improvement achieved

The success measure from the assessment, before vs after (numbers where
possible).

## Traceability

- Verifies: `REF-<NNN>`
