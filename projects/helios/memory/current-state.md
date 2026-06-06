# Current State

A living snapshot of where **Helios** is right now. First thing an agent reads
after `PROJECT.md`. Keep it short and current.

> This is **example** content to show the shape of a populated multi-repo
> project. Replace it with your product's real state.

## Now

- Standing up the harness for the four repos; no feature spec in flight yet.

## Recently landed

- 2026-06-06 — Adopted central-mode harness across `helios-api`, `helios-workers`,
  `helios-web`, `helios-console`.

## Active spec

- _none_

## Known constraints

- The API contract (`helios-api/openapi.yaml`) is canonical; frontend repos must
  not assume undocumented shapes.
- Design tokens are owned by `helios-web` and shared with `helios-console`.

## Pointers

- Accepted patterns: `accepted-patterns/` _(add when the first one exists)_
- Previous failures to avoid repeating: `previous-failures/` _(add when relevant)_
- Decisions: `decisions/` _(add when the first decision is recorded)_
