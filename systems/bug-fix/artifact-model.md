# Bug-fix artifact model

This is the **doctrine** behind the `bug-fix` workflow
([`../../workflows/bug-fix.workflow.json`](../../workflows/bug-fix.workflow.json)).
A bug fix is **corrective** work: it restores expected behavior. It deliberately
skips the discovery → research → spec chain a feature needs — the expected
behavior is already specified; what is missing is a working implementation of it.

## The lifecycle

```
Triage → Reproduce → Diagnose → Fix → Verify
```

The discipline that matters: **reproduce before you diagnose, diagnose before you
fix.** A fix without a confirmed reproduction and an evidenced root cause is a
guess.

## Where artifacts live

```
projects/<project>/bugs/<bug-id>/
  bug-report.md            # triage: summary, severity, repro steps, environment
  root-cause.md            # diagnose: the evidenced cause + why it wasn't caught
  plans/
    fix-plan.md            # fix: the minimal change + the regression test
  reports/
    verify/report.md       # verify: fixed, and stays fixed
```

A scaffold lives at
[`../../projects/_template/bugs/_template/`](../../projects/_template/bugs/_template/) —
copy it to `projects/<project>/bugs/<bug-id>/`.

## Steps and gates

| Step | Produces | Gate to enter |
|------|----------|---------------|
| `triage` | `bug-report.md` | — (entry point) |
| `reproduce` | reproduction (status in the report) | `triage` done |
| `diagnose` | `root-cause.md` | `reproduced` |
| `fix` | `plans/fix-plan.md` + the change | `root-cause-accepted` |
| `verify` | `reports/verify/report.md` | `fix` done **and** `regression-test` present |

**HITL:** bugs are usually low-ceremony — the only routine gate is verify/close.
Escalate to a human earlier when severity is high, when the fix changes behavior
beyond restoring the expected one, or when the bug is a **security** issue (then
loop in `security-engineer` and treat disclosure/severity as a stop condition).

## Routing

- `qa-engineer` — reproduction, regression test design, verify.
- `developer` — root-cause analysis and the minimal fix.
- `security-engineer` — when the bug is a vulnerability.

## Scope discipline

A bug fix restores expected behavior and nothing more. If fixing it requires new
behavior, it is a **feature** (use `feature-development`); if it is purely
internal quality with no behavior change, it is a **refinement**. Expanding scope
inside a bug fix is a stop condition.

## Traceability

`BUG-<NNN>` is the entry id. The root cause, fix plan, commit, and verify report
link back to it via `source:`/`traces:`; if the bug lives in a shipped feature,
link the owning `SPEC-`. See [`../../rules/traceability.md`](../../rules/traceability.md).
