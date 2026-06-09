---
description: Run a bug through the corrective lifecycle — triage → reproduce → diagnose → fix → verify — consulting QA and the Developer (and Security if it's a vulnerability) to produce a minimal, regression-tested fix. Use to fix a defect end to end.
argument-hint: <the bug report, failing behavior, or issue link>
---

Drive the **`bug-fix`** lifecycle over the defect below: `triage → reproduce → diagnose → fix → verify`. This is **corrective** work — restore the expected behavior, nothing more. Do **not** run the feature discovery/research/spec chain; the behavior is already specified.

The bug to fix:

$ARGUMENTS

## Phase 0 — Triage (gate)

Handle this in the main conversation (subagents cannot talk to the user). Confirm severity and the expected-vs-actual behavior. If the report lacks enough detail to attempt a reproduction, ask **1–2** focused questions with `AskUserQuestion` before starting — an unreproducible bug with no repro detail is a stop condition.

## Phases

Each phase produces one concise artifact that feeds the next.

1. **Reproduce** (`qa-engineer`) — establish a reliable reproduction from the report's steps. If it cannot be reproduced, stop and report what is missing. Record the repro in `bug-report.md`.
2. **Diagnose** (`developer`) — trace the **root cause** to specific code (`file:line`); confirm it with evidence (failing test, trace, bisect). Note why it wasn't caught and the blast radius. Do not propose a fix until the cause is evidenced — **root-cause-accepted** gates the fix.
3. **Fix** (`developer`) — the **minimal** change that restores expected behavior, plus the **regression test** that fails before and passes after. Expanding behavior here is a stop condition (that's a feature).
4. **Verify** (`qa-engineer`) — confirm the regression test passes, the original repro no longer triggers the bug, and the wider suite is green.

If the bug is a **security** vulnerability, add **`security-engineer`** after triage and treat disclosure/severity as a stop condition.

## Execution

Run each phase in its **own subagent** (`Agent`, `subagent_type: general-purpose`): tell it to adopt the named skill, pass the bug plus all prior artifacts, have it self-check against the skill's `references/checklist.md`, and return only the compact artifact. Reproduce → Diagnose → Fix are serial; Verify follows Fix.

### Model tiers

- **Opus** — diagnosis and the fix (Developer): root-cause reasoning is where depth pays.
- **Sonnet** — reproduction and verification (QA): structured transformation of the report.

## Harness mode — durable artifacts

Praxis **always runs in harness mode**. At the start, **ensure the harness is initialized** with `python tools/ensure_harness.py` (idempotent; auto-bootstraps a project derived from the repo if none resolves). Then write the durable artifacts under the owning project, following the `bug-fix` workflow. Doctrine: the harness `systems/bug-fix/artifact-model.md`; gates: `workflows/bug-fix.workflow.json`. There is no non-harness fallback.

```
projects/<projectId>/bugs/<bug-id>/
  bug-report.md            # triage + reproduction
  root-cause.md            # diagnosis
  plans/fix-plan.md        # the minimal fix + regression test
  reports/verify/report.md # verification evidence
```

- Copy the harness's `projects/_template/bugs/_template/` as the starting shape. Assign a `BUG-<NNN>` id and link any owning `SPEC-` (see `rules/traceability.md`).
- **Respect the gates.** The fix is authorized by an accepted root cause, not a pending one — **pending is not approval**.
- **Stop condition:** auto-bootstrap covers a *missing* config. If a config is *present* but its `projectId` does not resolve, stop and ask — do not guess a destination, and do not overwrite it.

## Memory

Record the root-cause decision and the fix in the memory ledger (`log` the decision, `snapshot` the change so it can be rolled back). New entries are `pending` until the user accepts.
