---
id: template
title: Refinement Template
project: template
type: refinement
status: assessed
---

# Refinement: <short title>

> Copy this folder to `projects/<project>/refinements/<ref-id>/`. The
> `refinement` workflow is `assess → plan → change → verify`. A refinement
> **preserves observable behavior** (refactor, performance, tech-debt, internal
> quality). If behavior changes, it is a feature or a bug fix instead. See
> [`systems/refinement/artifact-model.md`](../../../../systems/refinement/artifact-model.md).

## Motivation

What is being improved and why (maintainability, performance, debt, clarity).
Tie to a cost being paid today.

## Scope

What code/area is in scope, and explicitly what is out.

## Baseline (behavior to preserve)

How current behavior is captured so it can be shown unchanged afterwards:
existing tests, characterization tests to add, benchmarks, golden outputs. The
`plan` step is gated on `baseline-captured`.

## Success measure

How we will know it worked (e.g. p95 latency ↓, complexity ↓, duplication
removed) **without** changing observable behavior.

## Traceability

- This refinement id: `REF-<NNN>`
- Related spec / code area: `SPEC-<NNN>` / `<path>`
- Decision (if structurally significant): `ADR-<NNN>`
