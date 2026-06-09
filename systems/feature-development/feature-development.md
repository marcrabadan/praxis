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

## Lifecycle states, criteria-checked gates, and the failure protocol

The full chain is:

```
discovery → research → product-definition → spec → experience → plan
  → tasks → build → verify → release-candidate → release
```

Two states make the front and back halves explicit rather than folded away:

- **product-definition** (routed to the **product-owner**) bounds the *what/why*
  — MVP scope, prioritised requirements, success metrics — before the spec pins
  behaviour. Its artifact is [`product/product-definition.md`](../../projects/_template/specs/_template/product/product-definition.md).
- **release-candidate** separates "proven correct" (`verify` passed) from
  "decided to ship" (`release-approved`). Its artifact is
  [`reports/release/release-candidate.md`](../../projects/_template/specs/_template/reports/release/release-candidate.md).

### Gates are criteria-checked, not vibes

A gate token in the manifest's `gates` (e.g. `approved-spec`, `architecture-validated`)
is no longer a bare human thumbs-up. The manifest's **`gateCriteria`** block lists
the explicit, checkable criteria each gate proves; a human approves *only when
every criterion holds*. This closes the difference between an HITL approval and a
validator — the criteria are the validator, the human runs them. Notably,
**`architecture-validated`** gives architecture its own pass/fail (NFRs met,
maintainable/modular, unfamiliar architecture justified by an ADR,
security-relevant design identified) via
[`plans/architecture-review.md`](../../projects/_template/specs/_template/plans/architecture-review.md),
instead of leaving it implicit inside the plan. **Pending is not approved** — a
gate whose decision is still pending is a stop condition.

### The failure protocol: return to the failing state

When a gate fails, the workflow does not limp forward or silently retry in place.
The manifest's **`transitions.onGateFailure`** map says exactly which state to
return to for rework: a failed `architecture-validated` routes back to `plan`, a
failed `approved-spec` back to `spec`, a failed `verify-passed` back to `build`
(the same back-edge the verify loop's `onContinue` uses), and so on. The protocol
is: **stop → root-cause → return to the mapped state → fix → revalidate.** Letting
a failed gate be bypassed instead of routed back is itself a stop condition.

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

### The gate catalog and the verify report

The predicate is proven by **typed gates** declared in the manifest's
`gateCatalog` — `G-build`, `G-lint`, `G-typecheck`, `G-tests`, `G-runtime-clean`,
`G-acceptance`, the mandatory `G-security` (every feature records a security
review; high/critical findings are fixed or carry an approved risk-acceptance
decision — a feature never reaches `release` on an unaddressed one), and
conditional ones like `G-performance` (runtime-bearing surfaces meet their stated
budget), `G-routes-200`, and `G-visual` (which apply only to certain experience
types). `loops.verify.gates` lists the gates that
prove this step, and each gate id resolves to a catalog entry (the harness
validator enforces this). An experience contract's `verification` list references
the same gate ids, so a surface declares exactly which gates prove it.

The [verify report](../../projects/_template/specs/_template/reports/verify/report.md)
records a **pass/fail/skipped/n-a result per gate**, the stop conditions hit, the
verdict, and **reviewer sign-off**. Two rules make it authoritative:

- **No self-certification.** The implementer does not declare their own work done.
  An implementation note says what happened; only the verify report, with real
  gate results and an accepting sign-off, marks a scope complete. Recording a gate
  `pass` without the evidence that ran it is the hard stop `U-8`.
- **A skipped required gate must be justified** in the report, or the report
  fails. Conditional gates record *why* they don't apply (wrong surface type).

Only `overall-result: pass` with accepted sign-off satisfies the `release` gate.

### Tasks carry their own anti-drift constraints

The `tasks` step doesn't just list work — each task names its **Plan ref**,
**Decisions** in force, what is **Forbidden** (don't rename the route, don't
substitute a named dependency `U-9`, don't hardcode contract tokens), the
**Gate** that proves it, and its allowed **Output** (the only files it may
touch). Each per-surface group declares `files-owned`, mirroring the surface's
experience-contract `filesOwned`, so the verifier and the build agree on scope.
[`../../tools/check_tasks.py`](../../tools/check_tasks.py) lints this
deterministically (`make check-tasks FILE=…`) — a task with no Forbidden/Gate/
Output is drift waiting to happen.

## Stop conditions

In addition to [`../../rules/stop-conditions.md`](../../rules/stop-conditions.md),
this workflow stops when: the spec's scope or target user is ambiguous; the plan
would adopt an architecture the project has not used; a gate's required
decision is still `pending`; or `release` is reached with an unaddressed high or
critical security finding and no approved risk-acceptance decision. A tripped convergence-loop guard (above) is also a
stop. Recording a proposal is allowed; acting on it before acceptance is not.
