# Feature-development artifact model

This is the **doctrine** behind the `feature-development` workflow
([`../../workflows/feature-development.workflow.json`](../../workflows/feature-development.workflow.json)).
It answers: which artifacts exist, which are required, which status values are
allowed, and which artifact authorizes the next step.

A feature plan is **not** the final source of truth. It becomes a set of durable,
typed artifacts that future agents can load selectively.

## Where artifacts live

In harness mode, a feature's durable artifacts live under the owning project:

```
projects/<project>/specs/<spec>/
  spec.md                       # what & why (frontmatter: id, title, project, status)
  decisions/                    # typed decisions (mini-ADRs) for this spec
  plans/
    implementation-plan.md      # how: components, files, ordered tasks
  tasks/
    tasks.md                    # the checklist the build follows
  reports/
    verify/report.md            # evidence the work meets the spec
```

A scaffold lives at
[`../../projects/_template/specs/_template/`](../../projects/_template/specs/_template/) —
copy it to `projects/<project>/specs/<spec>/`.

## The steps and what authorizes the next one

The workflow is `spec → plan → tasks → verify`. Each step is **gated** by an
artifact from the previous step reaching an authorizing status:

| Step | Produces | Gate to enter (from the manifest) |
|------|----------|-----------------------------------|
| `spec` | `spec.md` | — (entry point) |
| `plan` | `plans/implementation-plan.md` | `approved-spec` — `spec.md` status is `accepted` |
| `tasks` | `tasks/tasks.md` | `approved-plan` — the plan decision is `accepted` |
| `verify` | `reports/verify/report.md` | `tasks` exist **and** `test-evidence` is present |

**Pending is not approval.** A `spec.md` left at `draft`, or a plan recorded as a
`pending` ledger decision, does **not** open the next gate. Advance only after the
user accepts (see [`../../rules/source-of-truth.md`](../../rules/source-of-truth.md)
and [`../../rules/stop-conditions.md`](../../rules/stop-conditions.md)).

## Status values (closed sets)

- **spec.md** status: `draft | accepted | superseded | done` (schema:
  [`../../schemas/spec.schema.json`](../../schemas/spec.schema.json)).
- **decisions** recorded in the memory ledger use the ledger's closed set:
  `pending | accepted | rejected | superseded | rolled-back`.

Never invent a status. If the lifecycle needs another state, change the schema
and this doc together.

## Required vs optional

- **Required to call a spec real:** `spec.md`.
- **Required before building:** `plans/implementation-plan.md` (once the spec is
  accepted).
- **Required before verify:** `tasks/tasks.md` + test evidence.
- **Optional but encouraged:** `decisions/` (one file per significant call) and
  `reports/` (verify output, run logs).

Keep it light. Do not force a full artifact chain on a one-line change — a tiny
fix may need only a spec note or nothing at all. The chain earns its keep on
features with real ambiguity or risk.
