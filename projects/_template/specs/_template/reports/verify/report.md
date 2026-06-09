---
type: verify-report
scope: <scaffold|surface-slug|feature>
overall-result: draft
---

# Verify report

> The **authoritative** completion record for one verify run, authorized once
> tasks are done and test evidence exists (the `verify` gate). The `verify` step
> is a bounded convergence loop (see [`../../../../../rules/loop-control.md`](../../../../../rules/loop-control.md)):
> it iterates until every gate below passes (`done`) or a guard trips (`escalate`).

## No self-certification

The implementer does **not** declare their own work done. An implementation note
describes what happened; only this report — with real gate results and reviewer
sign-off — can mark a scope complete. Recording a gate `pass` without the
evidence that ran it is forbidden (it is a hard stop, `U-8`).

## Gate results

One row per gate in the workflow's `gateCatalog` that applies to this scope.

| Gate | Result | Evidence |
|------|--------|----------|
| G-build | pass \| fail \| skipped \| n/a | `<command + exit code, or link>` |
| G-lint | pass \| fail \| skipped \| n/a | |
| G-typecheck | pass \| fail \| skipped \| n/a | |
| G-tests | pass \| fail \| skipped \| n/a | |
| G-runtime-clean | pass \| fail \| skipped \| n/a | |
| G-acceptance | pass \| fail \| skipped \| n/a | |
| G-security | pass \| fail \| skipped \| n/a | `<security review ref; high/critical findings + dispositions>` |
| G-performance | pass \| fail \| skipped \| n/a | `<budget + measured result, or why n/a>` |

Conditional gates (e.g. `G-visual`, `G-routes-200`) that are skipped must say why
here. A skipped required gate without justification fails the report.

## Stop conditions hit during this run

| ID | Surfaced as | Run log | Status |
|----|-------------|---------|--------|
| `<U/P/S-*>` | `STOP[...]` | `<path>` | resolved \| unresolved |

Any unresolved stop condition forces `overall-result: fail`.

## Verdict

`overall-result`: `pass` / `fail` / `partial`. Failures are paired with evidence
and the next action; the loop returns to `build` (`onContinue`) on anything but
`pass`.

## Reviewer sign-off

The verifier emits the report; the reviewer decides whether the verdict is
accepted for advancement. Only `pass` with accepted sign-off opens `release`.

- Verifier:
- Reviewed by:
- Decision: `accepted-as-authoritative` / `rejected-rerun-required` / `accepted-with-documented-exceptions`
- Notes (exceptions require a decision trace):
