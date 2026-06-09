---
type: run-log
condition: <U-*|P-*|S-*>
status: unresolved
step: <workflow step where it fired>
created: <yyyy-mm-dd>
---

# Run Log: <topic>

> Written when a [stop condition](../../../../../rules/stop-conditions-catalog.md)
> fires. The step stays **blocked** until this log is resolved and the workflow
> re-enters at the exact blocked point. Copy to `runs/<date>-stop-<condition>-<topic>.md`.

## Context

- What was being attempted, and the workflow step + scope.
- Active artifacts loaded (spec, experience contract, plan, tasks).
- The exact catalog row that fired.

## Expected vs actual

What the source of truth said should be true, and what was observed instead.

## Evidence

The command output, file/line, or failing check that makes this an observable
blocker — not a hunch.

## Options for resolution

List at least two. **"Keep going" is not a valid option.**

```
A. <option> — <cost, risk, downstream impact>
B. <option> — <cost, risk, downstream impact>
```

## Resolution

Until resolved, write `Unresolved.` When resolved:

- Chosen option:
- Why:
- Downstream updates required:
- **Re-entry point:** the exact step/task to resume.
- Decision trace (for strategic changes):

## Definition of done

Resolved only when: the trigger and evidence are clear, the chosen resolution is
recorded, downstream updates are done or tracked, and the workflow re-enters at
the exact blocked step. A recurring blocker is a candidate to promote into a new
`P-*` or a guardrail via `tools/promote.py` (pending, human-gated).
