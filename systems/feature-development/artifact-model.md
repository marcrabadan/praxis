# Feature-development artifact model

This is the **doctrine** behind the `feature-development` workflow
([`../../workflows/feature-development.workflow.json`](../../workflows/feature-development.workflow.json)).
It answers: which artifacts exist, which are required, which status values are
allowed, and which artifact authorizes the next step.

A feature plan is **not** the final source of truth. It becomes a set of durable,
typed artifacts that future agents can load selectively. The spec is the single
source of truth once written; discovery and research are what earn it.

## The full lifecycle

```
Idea → Discovery → Research → Spec → Experience → Plan → Tasks → Build → Verify → Release
```

No spec is written before research; no research happens before discovery frames
the problem; no build happens before an accepted spec and plan. This encodes the
operating philosophy: understand → research → specify → contract the surfaces →
plan → build → validate → release.

The **`experience` step is optional**: for each surface the spec declares (its
experience inventory) it produces an executable per-surface contract
(`experience/<surface>.md` + a validating `experience/<surface>.contract.json`,
see [`../../schemas/experience-contract.schema.json`](../../schemas/experience-contract.schema.json))
that plan, tasks, build, and verify enforce. A pure logic/refactor spec that
declares no surfaces skips it (record that it was skipped).

The **`deploy` step is also optional** and terminal: after `release` is approved,
it provisions or updates infrastructure with Terraform and ships to a declared
cloud target (Kubernetes, AWS/EKS, GCP/GKE, Azure/AKS), driven through an MCP
server when one is configured. It runs **only when `.praxis/config.json` declares
a `deploy` target**; with no target it is skipped and that skip is recorded —
never assume a cloud. It is owned by the **devops-engineer** expert; the doctrine
is in [`../../.claude/skills/devops-engineer/references/deploy.md`](../../.claude/skills/devops-engineer/references/deploy.md).

## Where artifacts live

In harness mode, a feature's durable artifacts live under the owning project:

```
projects/<project>/specs/<spec>/
  discovery/
    discovery-report.md         # understand: problem, stakeholders, assumptions
  research/
    research-report.md          # investigate: findings, recommendation
    evidence-log.md             # one row per source backing a finding
    alternatives.md             # options weighed; the chosen direction
  spec.md                       # what & why (frontmatter: id, title, project, status, experienceInventory?)
  experience/                   # optional: one executable contract per surface
    <surface>.md                #   the contract (behaviour, files-owned, gates)
    <surface>.contract.json     #   companion, validates against experience-contract.schema.json
  decisions/                    # typed decisions (mini-ADRs) for this spec
  plans/
    implementation-plan.md      # how: components, files, ordered tasks
  tasks/
    tasks.md                    # the checklist the build follows
  reports/
    verify/report.md            # evidence the work meets the spec
    release/release-notes.md    # what shipped; acceptance met; rollback
    release/deploy-report.md    # optional: target, plan, promotion, health, rollback
```

A scaffold lives at
[`../../projects/_template/specs/_template/`](../../projects/_template/specs/_template/) —
copy it to `projects/<project>/specs/<spec>/`.

## The steps and what authorizes the next one

The workflow is `discovery → research → spec → experience → plan → tasks → build
→ verify → release`. Each step is **gated** by an artifact from a previous step
reaching an authorizing status:

| Step | Produces | Gate to enter | HITL gate |
|------|----------|---------------|-----------|
| `discovery` | `discovery/discovery-report.md` | — (entry point) | — |
| `research` | `research/*` | discovery report exists | — |
| `spec` | `spec.md` | `approved-discovery` — discovery + research accepted | **Gate 1** |
| `experience` | `experience/<surface>.{md,contract.json}` | `approved-spec` | — (per-surface `accepted`) |
| `plan` | `plans/implementation-plan.md` | `approved-spec` **and** `experience-complete` | **Gate 2** |
| `tasks` | `tasks/tasks.md` | `approved-plan` — the plan decision is `accepted` | (Gate 3 if architecture) |
| `build` | code (in the product repo) | `tasks` exist | — |
| `verify` | `reports/verify/report.md` | build done **and** `test-evidence` present | — |
| `release` | `reports/release/release-notes.md` | `verify-passed` **and** `release-approved` | **Gate 4** |
| `deploy` *(optional)* | `reports/release/deploy-report.md` | `release-approved` **and** `deploy-target-configured` | promotion decision (manual for prod) |

The four HITL gates mirror the operating model: **Gate 1** (Discovery & Research
approval) opens the spec; **Gate 2** (Specification approval) opens planning;
**Gate 3** (Architecture approval) is required only when a structurally
significant decision exists — it does not block every feature; **Gate 4**
(Release approval) opens release. At each gate provide Recommendation, Evidence,
Risks, Alternatives, and pause for `ACCEPT | REFINE | REJECT`.

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

## Traceability

Every artifact carries a typed id (`DISC-`, `RES-`, `SPEC-`, `ADR-`, `TASK-`,
`VER-`, `REL-`) and links to its `source:` and `traces:` neighbours, so the chain
`IDEA → DISC → RES → SPEC → … → REL` is navigable both ways. See
[`../../rules/traceability.md`](../../rules/traceability.md).

## Required vs optional

- **Required to start:** `discovery/discovery-report.md`.
- **Required before a spec:** research findings recorded (research precedes spec).
- **Required to call a spec real:** `spec.md`.
- **Required before building:** `plans/implementation-plan.md` (once the spec is
  accepted).
- **Required before verify:** `tasks/tasks.md` + test evidence.
- **Required before release:** a verify report showing acceptance criteria met.
- **Optional but encouraged:** `decisions/` (one file per significant call).
- **Optional, config-gated:** `reports/release/deploy-report.md` — only when a
  `deploy` target is declared in `.praxis/config.json`; skipped and recorded
  otherwise.

Keep it light. Do not force the full chain on a one-line change — a tiny tweak
may be a `refinement` or a `bug-fix` instead, or need only a spec note. The chain
earns its keep on features with real ambiguity or risk. For corrective or
quality-only work, use the lighter
[`../bug-fix/artifact-model.md`](../bug-fix/artifact-model.md) and
[`../refinement/artifact-model.md`](../refinement/artifact-model.md) lifecycles.
