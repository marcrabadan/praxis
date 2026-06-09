---
id: template
title: Spec Template
project: template
status: draft
---

# Spec: <Feature title>

> Copy this folder to `projects/<project>/specs/<spec-id>/`. Set frontmatter
> `id` = folder name and `project` = the owning project id. Keep `status: draft`
> until the user accepts it — `accepted` is what opens the `plan` gate.
>
> A spec is written **after** discovery and research, not before. It distils
> [`discovery/discovery-report.md`](discovery/discovery-report.md) and
> [`research/research-report.md`](research/research-report.md) into the agreed
> scope. The spec is the single source of truth from here on.

## Problem & scope

What outcome this delivers and for whom. The one or two sentences that fix scope.

## Requirements

Functional and non-functional requirements; user stories with acceptance
criteria. Link the BA/PO artifacts rather than duplicating them.

## Out of scope

What this spec explicitly does not cover.

## Experience inventory

Every user- or system-facing surface this spec delivers. Each gets an
[experience contract](experience/_surface.md) in the optional `experience` step
(after the spec is accepted, before the plan). Pure logic/refactor specs with no
surfaces leave this empty and skip the step.

| ID | Type | Surface (slug) | Priority |
|----|------|----------------|----------|
| EXP-001 | screen | `<surface-slug>` | P1 |

For machine-checkable coverage, mirror this list in the frontmatter:

```yaml
experienceInventory:
  - id: EXP-001
    type: screen
    surface: <surface-slug>
    priority: P1
```

When present, the harness validator requires an `experience/<surface>.md` and a
validating `experience/<surface>.contract.json` for each entry.

## Open questions

Anything unresolved that gates the work. An open question that blocks a step is a
stop condition — resolve it before advancing.

## Traceability

- This spec id: `SPEC-<NNN>`
- Sources: discovery (`DISC-<NNN>`), research (`RES-<NNN>`)
- See [`../../../../rules/traceability.md`](../../../../rules/traceability.md).

## Upstream artifacts

- Discovery: [`discovery/discovery-report.md`](discovery/discovery-report.md)
- Research: [`research/research-report.md`](research/research-report.md), [`research/evidence-log.md`](research/evidence-log.md), [`research/alternatives.md`](research/alternatives.md)

## Downstream artifacts

- Plan: [`plans/implementation-plan.md`](plans/implementation-plan.md)
- Tasks: [`tasks/tasks.md`](tasks/tasks.md)
- Decisions: `decisions/`
- Verify report: [`reports/verify/report.md`](reports/verify/report.md)
- Release notes: [`reports/release/release-notes.md`](reports/release/release-notes.md)
