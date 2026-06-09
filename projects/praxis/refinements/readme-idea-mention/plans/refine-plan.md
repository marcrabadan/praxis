# Refine Plan — mention /idea in the README

One small, reversible step. Behavior-preserving (docs only).

## Steps

1. Add one paragraph to `README.md` after the `/fix-bug` / `/refine` lifecycle
   paragraph (the "Not every change is a greenfield feature." block), introducing
   `/idea` as the intake & triage front door: clarify ≤2 questions → classify
   (feature/bug/refinement/not-worth-doing) → capture a `pending` ledger note →
   recommend the next command; triages and routes, does not plan.

## Behavior-preserving evidence

- The README is not consumed by any validator, generator, or test, so the
  deterministic suite must be **unchanged** after the edit. Confirm:
  `make catalog-check`, `make integrations-check`, `make validate-harness`,
  `make test` all still pass.

## Rollback

Single-hunk `git revert` of the README edit; nothing else is touched.
