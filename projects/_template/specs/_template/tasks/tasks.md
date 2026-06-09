# Tasks

> Authorized once the plan is `accepted` (the `approved-plan` gate). The build
> follows this checklist. Every task is scoped tightly enough to run without
> guessing: it names its **Plan ref**, the **Decisions** in force, what is
> **Forbidden** (anti-drift), the **Gate** that proves it, and its allowed
> **Output** (the only files it may touch). Lint with
> `python tools/check_tasks.py tasks/tasks.md` (or `make check-tasks FILE=...`).

## Format

```
- [ ] T001 [scope] <description>
  - Plan ref: <plan section>
  - Decisions in force: <decision ids or none>
  - Forbidden: <explicit anti-drift constraints>
  - Gate: <G-* gate ids from the workflow gate catalog>
  - Output: <the only files/artifacts this task may create or edit>
```

Use `[P]` only for tasks that touch disjoint files with no ordering dependency.

## Phase 1 — Scaffold

Prove the toolchain and app shell; do not implement a feature surface.

- [ ] T001 [scaffold] Confirm repo, package manager, and dev/build/test commands.
  - Plan ref: Sequencing / Phase 1
  - Decisions in force: none
  - Forbidden: guessing the package manager; installing deps without checking repo conventions
  - Gate: G-build
  - Output: implementation note only

## Phase 2 — Per surface

One contiguous group per surface; each group ends with a verify task. Declare the
group's `files-owned` (mirror the surface's experience-contract `filesOwned` — the
verifier scopes checks to these).

### Surface: <surface-slug>

Experience: `experience/<surface-slug>.md` · Contract: `experience/<surface-slug>.contract.json`

files-owned:
- `<path/owned/by/this/surface>`

- [ ] T010 [<surface-slug>] Implement the surface contract.
  - Plan ref: Per-surface plan / <surface-slug>
  - Decisions in force: <ids or none>
  - Forbidden: hardcoding values the contract names as tokens; renaming the route/invocation; substituting a named dependency (U-9)
  - Gate: G-build, G-typecheck, G-runtime-clean
  - Output: `<allowed files under files-owned>`
- [ ] T011 [<surface-slug>] Run verify for this surface.
  - Plan ref: Sequencing / Phase 2
  - Decisions in force: none
  - Forbidden: advancing to the next surface if the verify report is not `pass`
  - Gate: every gate required for this scope
  - Output: `reports/verify/<date>-<surface-slug>.md`

## Phase 3 — Cross-cutting & whole-feature verify

Cross-cutting runs only after every surface verify report passes.

- [ ] T090 [cross-cutting] Complete cross-surface integration.
  - Plan ref: Sequencing / Phase 3
  - Decisions in force: <ids or none>
  - Forbidden: changing a previously verified surface without re-running its verify scope
  - Gate: G-runtime-clean
  - Output: `<allowed files>`
- [ ] T091 [cross-cutting] Run whole-feature verify.
  - Plan ref: Sequencing / Phase 3
  - Decisions in force: none
  - Forbidden: declaring the feature done before this report is `pass`
  - Gate: every required feature gate
  - Output: `reports/verify/<date>-feature.md`

## Definition of done

- every task names Plan ref, Decisions, Forbidden, Gate, and Output
- every surface group declares files-owned and ends with a verify task
- the final task is whole-feature verify
- `python tools/check_tasks.py tasks/tasks.md` passes
