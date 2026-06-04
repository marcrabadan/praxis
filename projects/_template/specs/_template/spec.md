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

## Problem & scope

What outcome this delivers and for whom. The one or two sentences that fix scope.

## Requirements

Functional and non-functional requirements; user stories with acceptance
criteria. Link the BA/PO artifacts rather than duplicating them.

## Out of scope

What this spec explicitly does not cover.

## Open questions

Anything unresolved that gates the work. An open question that blocks a step is a
stop condition — resolve it before advancing.

## Downstream artifacts

- Plan: [`plans/implementation-plan.md`](plans/implementation-plan.md)
- Tasks: [`tasks/tasks.md`](tasks/tasks.md)
- Decisions: `decisions/`
- Verify report: `reports/verify/report.md`
