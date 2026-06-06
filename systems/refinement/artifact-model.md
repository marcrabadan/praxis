# Refinement artifact model

This is the **doctrine** behind the `refinement` workflow
([`../../workflows/refinement.workflow.json`](../../workflows/refinement.workflow.json)).
A refinement is **quality-only** work: refactoring, performance, tech-debt
paydown, readability — improvements that **preserve observable behavior**. The
defining constraint is the inverse of a feature: nothing the user can observe may
change.

## The lifecycle

```
Assess → Plan → Change → Verify
```

The discipline that matters: **capture a baseline first.** You cannot prove
behavior was preserved if you never recorded what it was.

## Where artifacts live

```
projects/<project>/refinements/<ref-id>/
  assessment.md            # assess: motivation, scope, baseline, success measure
  plans/
    refine-plan.md         # plan: ordered, behavior-preserving steps + rollback
  reports/
    verify/report.md       # verify: behavior preserved + improvement achieved
```

A scaffold lives at
[`../../projects/_template/refinements/_template/`](../../projects/_template/refinements/_template/) —
copy it to `projects/<project>/refinements/<ref-id>/`.

## Steps and gates

| Step | Produces | Gate to enter |
|------|----------|---------------|
| `assess` | `assessment.md` | — (entry point) |
| `plan` | `plans/refine-plan.md` | `assessed` **and** `baseline-captured` |
| `change` | the change (in the product repo) | `approved-plan` |
| `verify` | `reports/verify/report.md` | `change` done **and** `behavior-preserving-evidence` |

**HITL:** routine refinements need only the verify/close gate. Escalate to
**Gate 3 (Architecture)** when the refinement is structurally significant (moves
a boundary, changes a pattern) — then record an `ADR-` and get architecture
approval before the change.

## Routing

- `developer` — the refactor/optimization and its tests.
- `software-architect` — when the refinement is structurally significant.
- the relevant domain expert (`frontend-engineer`, `data-engineer`, …) when the
  area is specialized.

## Scope discipline

If the change alters observable behavior, it is **not** a refinement — it is a
feature (`feature-development`) or a bug fix (`bug-fix`). Behavior change inside a
refinement is a stop condition. The baseline (tests, benchmarks, golden outputs)
is what keeps this honest.

## Traceability

`REF-<NNN>` is the entry id. The plan, commit, and verify report link back via
`source:`/`traces:`; link the affected `SPEC-` or code area, and any `ADR-`. See
[`../../rules/traceability.md`](../../rules/traceability.md).
