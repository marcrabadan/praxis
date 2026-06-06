---
id: helios
name: Helios
status: active
---

# Project: Helios

> **Example project** shipped with the harness to demonstrate **central mode**
> across multiple repositories. Helios is a fictional last-mile logistics
> platform. It spans four repos — two backend, two frontend — that share one
> project memory here in the harness. Copy this shape for a real product (and
> rename `helios` to your product id).

## Purpose

Helios is a last-mile delivery platform: merchants create shipments, drivers are
dispatched and tracked, and customers follow deliveries in real time. The product
is delivered across four repositories that must stay coordinated, so their specs,
decisions, and memory live **centrally** here rather than fragmented per repo.

## Linked repos

See [`linked-repos.md`](linked-repos.md) for the four repositories this project
spans and the `.praxis/config.json` each one carries. In short: two backend repos
(`helios-api`, `helios-workers`) and two frontend repos (`helios-web`,
`helios-console`), all pointing `harnessRoot` at this harness with
`projectId: helios` and `mode: central`.

## Authority notes

Project-specific authority that overrides general defaults (authority order:
[`../../rules/source-of-truth.md`](../../rules/source-of-truth.md)):

- **The API contract is canonical.** `helios-api/openapi.yaml` is the source of
  truth for request/response shapes. `helios-web` and `helios-console` follow it;
  a frontend change that assumes a shape the contract does not define is a stop
  condition — change the contract (and this note's owning decision) first.
- **Design tokens are canonical in `helios-web`.** `helios-console` consumes the
  same tokens; do not fork them.
- **Cross-repo features are specified once, here.** A feature that touches more
  than one repo gets a single spec under `specs/`, with tasks grouped by repo —
  not a separate plan per repo.
- **Auth changes require a security review** before merge (any repo).
- **Gate approvers (who can ACCEPT).** Spec gate → product owner; Architecture
  gate → tech lead; Release gate → tech lead + product owner. The agent presents
  each gate; only the named owner accepts it. **Pending is not approval.** (See
  [`../../docs/teamwork.md`](../../docs/teamwork.md) for how concurrent teams
  coordinate.)

## Current workflow

`feature-development` (`discovery → research → spec → plan → tasks → build →
verify → release`) for new capabilities; `bug-fix` and `refinement` for
corrective and quality-only work. Manifests live in
[`../../workflows/`](../../workflows/registry.json).

## Where specs live

`specs/` under this project folder — one subfolder per spec, shared by all four
repos. `bugs/` and `refinements/` follow the same pattern. (Folders are created
when the first artifact exists.)

## Where decisions live

Durable project decisions: `memory/decisions/`. Cross-cutting or snapshot-able
changes also go to the memory ledger (`.praxis/memory/`). Status is always from
the closed set `pending | accepted | rejected | superseded | rolled-back`, and
**pending is not approval**.
