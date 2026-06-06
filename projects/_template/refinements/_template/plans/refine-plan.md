# Refine Plan — <refinement title>

> Step `plan`. The ordered, behavior-preserving steps. Each step should keep the
> baseline green.

## Approach

The refactor/optimization strategy: what changes, in what order, kept small and
reversible.

## Steps

1. … (baseline stays green after each)
2. …

## Behavior-preserving evidence

How each step proves behavior is unchanged (tests still pass, benchmark within
tolerance, golden output identical). `verify` is gated on
`behavior-preserving-evidence`.

## Rollback

How to back out if a step regresses behavior.

## Traceability

- Refines: `REF-<NNN>`
- Implements decision: `ADR-<NNN>` (if any)
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
