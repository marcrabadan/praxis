---
id: template
title: Bug Template
project: template
type: bug
severity: medium
status: triaged
---

# Bug: <short title>

> Copy this folder to `projects/<project>/bugs/<bug-id>/`. The `bug-fix`
> workflow is `triage → reproduce → diagnose → fix → verify` — lighter than a
> feature: no discovery/research/spec chain. See
> [`systems/bug-fix/artifact-model.md`](../../../../systems/bug-fix/artifact-model.md).

## Summary

What is wrong, in one sentence.

## Severity & impact

Who/what is affected, how badly, how often. Justify the `severity` frontmatter
(`critical | high | medium | low`).

## Steps to reproduce

1. …
2. …

**Expected:** what should happen.
**Actual:** what happens instead.

## Environment

Version/commit, platform, config — anything needed to reproduce.

## Reproduction status

`not-reproduced | reproduced`. The `diagnose` step is gated on `reproduced` —
a bug that cannot be reproduced and lacks detail to reproduce it is a stop
condition.

## Traceability

- This bug id: `BUG-<NNN>`
- Related spec (if the bug is in a shipped feature): `SPEC-<NNN>`
- Downstream: root cause (`root-cause.md`), fix plan (`plans/fix-plan.md`)
