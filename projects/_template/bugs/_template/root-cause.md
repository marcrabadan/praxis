# Root Cause — <bug title>

> Step `diagnose`. An **evidenced** diagnosis, not a guess. The `fix` step is
> gated on `root-cause-accepted`.

## Root cause

The actual cause, traced to specific code/behavior (cite `file:line`).

## Evidence

How the cause was confirmed (failing test, trace, log, bisect, repro).

## Why it was not caught

The gap that let this through (missing test, unhandled case, bad assumption).
Feeds the regression test and any prevention follow-up.

## Blast radius

What else this cause could affect — related call sites, similar patterns.

## Traceability

- This artifact: root cause for `BUG-<NNN>`
- Decision (if the fix approach is significant): `ADR-<NNN>`
