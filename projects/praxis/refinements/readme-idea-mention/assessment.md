---
id: readme-idea-mention
title: Mention /idea in the README command list
project: praxis
type: refinement
status: assessed
---

# Refinement: mention /idea in the README

## Motivation

The `/idea` command shipped (v1.10.0) but the README prose did not list it, so a
reader of the README would not discover the intake front door. Docs-vs-reality
drift. Source: ledger intake note `20260609-174557-742c` (raised by `/idea` itself).

## Scope

- **In:** one prose paragraph in `README.md`, next to the `/fix-bug` / `/refine`
  lifecycle description, introducing `/idea` as the intake & triage front door.
- **Out:** the generated `SKILLS.md` (already lists `/idea`), the integrations,
  any behavior of the command itself, any other doc.

## Baseline (behavior to preserve)

This is documentation only — there is **no runtime behavior** to preserve. The
"baseline" is the deterministic toolchain: `make catalog-check`,
`make integrations-check`, `make validate-harness`, and the test suite must stay
green (the README is not an input to any of them, so they must be unaffected).

## Success measure

The README's lifecycle-commands prose mentions `/idea` and accurately describes
it (intake → clarify → classify → capture → recommend, not a planner), and every
deterministic check stays green.
