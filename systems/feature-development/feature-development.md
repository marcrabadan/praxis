# Feature development

The lifecycle that `/new-feature` drives. This doc is the **operating model**;
the machine-readable gates live in
[`../../workflows/feature-development.workflow.json`](../../workflows/feature-development.workflow.json)
and the artifact shapes in [`artifact-model.md`](artifact-model.md).

## Two modes

`/new-feature` adapts to the repo:

- **Plan mode (default, no harness):** runs the SDLC experts and returns a
  consolidated plan, writing `docs/` files and recording entries to the memory
  ledger. Behavior unchanged from before harness mode.
- **Harness mode (a `.praxis/config.json` resolves a project):** *additionally*
  writes durable, typed spec artifacts under
  `projects/<project>/specs/<spec>/`, following the `spec → plan → tasks → verify`
  workflow and respecting its gates. Chat output becomes a summary; the
  artifacts are the source of truth.

## The thin-command principle

The command routes; it does not own lifecycle doctrine forever:

```
commands/new-feature.md
  -> workflows/feature-development.workflow.json   (gates & transitions)
  -> systems/feature-development/                  (this doctrine + artifact model)
  -> skills/<SDLC expert>                          (the work)
```

## The verify step is a convergence loop

`verify` does not run once — it iterates until the change actually meets its
acceptance criteria, under [`../../rules/loop-control.md`](../../rules/loop-control.md).
The manifest's `loops.verify` block is its **terminal predicate** (every spec
acceptance criterion met, the suite green with no regressions, the step
validation command passing) plus the budget and no-progress guards. Drive it with
[`../../tools/loop.py`](../../tools/loop.py):

```
loop.py start --goal "verify <spec>" --criterion "<each predicate entry>" \
        --max-iterations 8 --patience 3
loop.py tick <id> --met c1 --signal "<state, e.g. 2 tests failing>"
```

Each tick yields one verdict:

- **continue** — criteria unmet, progress is being made: return to `build`
  (`onContinue`), fix, and tick again.
- **done** — the predicate holds: `verify` is complete; the `release` gate's
  `verify-passed` condition is now satisfied. Record the result in the ledger.
- **escalate** — a guard tripped (budget exhausted or no progress). **Stop** and
  bring the user the state, the blocker, and options — exactly like a stop
  condition. Resume only after they give guidance (and maybe a larger budget).

This is what makes "iterate until it's correct" terminate: it ends by meeting the
predicate or by escalating to a human, and never just spins. The bug-fix
(`verify → fix`) and refinement (`verify → change`) lifecycles use the same
mechanism with their own predicates.

## Stop conditions

In addition to [`../../rules/stop-conditions.md`](../../rules/stop-conditions.md),
this workflow stops when: the spec's scope or target user is ambiguous; the plan
would adopt an architecture the project has not used; or a gate's required
decision is still `pending`. A tripped convergence-loop guard (above) is also a
stop. Recording a proposal is allowed; acting on it before acceptance is not.
