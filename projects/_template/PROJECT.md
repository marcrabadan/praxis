---
id: template
name: Project Template
status: active
---

# Project: <Project Name>

> Copy this folder to `projects/<your-project-id>/`, replace every placeholder,
> then add the project to [`../projects-index.md`](../projects-index.md). The
> frontmatter `id` must match the folder name and the `projectId` in the
> consuming repo's `.praxis/config.json`.

## Purpose

What this project is and the outcome it exists to deliver. One short paragraph.

## Linked repos

See [`linked-repos.md`](linked-repos.md) for the product repositories this
project spans and how they map to `.praxis/config.json`.

## Authority notes

Project-specific authority that overrides general harness defaults — e.g. "this
project's API contract in `repo-x/openapi.yaml` is canonical", "security review is
required before any auth change". Keep to durable, behavior-changing notes.
Authority order is defined in [`../../rules/source-of-truth.md`](../../rules/source-of-truth.md).

## Current workflow

Which workflow this project follows and where it is. Until the workflow layer
lands, name the lifecycle in prose (e.g. "spec → plan → tasks → verify").

## Where specs live

`specs/` under this project folder. Each spec gets its own subfolder. (Not
created by the template — add `specs/<spec>/` when the first spec exists.)

## Where decisions live

Durable project decisions: `memory/decisions/`. Cross-cutting or snapshot-able
changes also go to the memory ledger (`.praxis/memory/`). Status is always from
the closed set `pending | accepted | rejected | superseded | rolled-back`, and
**pending is not approval**.
