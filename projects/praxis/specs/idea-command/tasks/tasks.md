# Tasks — /idea intake & triage command

> Authorized once the plan is `accepted` (the `approved-plan` gate). Every task
> names its **Plan ref**, the **Decisions** in force, what is **Forbidden**
> (anti-drift), the **Gate** that proves it, and its allowed **Output** (the only
> files it may touch). Lint with `python tools/check_tasks.py
> projects/praxis/specs/idea-command/tasks/tasks.md`.

Plan: [`../plans/implementation-plan.md`](../plans/implementation-plan.md) ·
Decision: [`../decisions/ADR-001-idea-triage-design.md`](../decisions/ADR-001-idea-triage-design.md) ·
Spec: [`../spec.md`](../spec.md)

## Phase 1 — Author the command

### Surface: idea-command

Experience: the `/idea` slash command · Contract: spec AC-01…AC-15.

files-owned:
- `.claude/commands/idea.md`
- `plugin-praxis/commands/idea.md`
- `SKILLS.md`

- [ ] T001 [idea-command] Author `.claude/commands/idea.md` to the structure in the plan.
  - Plan ref: Approach / idea.md structure
  - Decisions in force: ADR-001 (all four decisions)
  - Forbidden: adding `allowed-tools`; any `Agent`/`Skill` tool invocation; auto-invoking `/new-feature`/`/fix-bug`/`/refine`; emitting plan/spec/problem-statement content after the output block; using a `--type` other than `note`; computing the class→route mapping at runtime instead of a static table
  - Gate: G-build
  - Output: `.claude/commands/idea.md`
- [ ] T002 [idea-command] Run the static AC checks on the authored file.
  - Plan ref: Test approach / static checks
  - Decisions in force: ADR-001
  - Forbidden: proceeding if any of AC-01…AC-06, AC-13, AC-15 fail; editing the file to game a check rather than fix the cause
  - Gate: G-build
  - Output: implementation note only (line count 31–41; no `allowed-tools`; description has "intake and triage", not "plan a feature"; no `Agent`/`Skill`; four classes statically mapped; ledger snippet uses `--type note` and `--source /idea`)

## Phase 2 — Port and catalog

### Surface: plugin-and-catalog

Experience: plugin port + regenerated index · Contract: DoD (plugin symlink, `make catalog`).

files-owned:
- `plugin-praxis/commands/idea.md`
- `SKILLS.md`

- [ ] T010 [plugin-and-catalog] Create the plugin symlink for the command.
  - Plan ref: Components & files to touch
  - Decisions in force: none
  - Forbidden: copying the file instead of symlinking; using an absolute symlink target (must be relative `../../.claude/commands/idea.md`, matching every existing entry)
  - Gate: G-build
  - Output: `plugin-praxis/commands/idea.md`
- [ ] T011 [plugin-and-catalog] Regenerate `SKILLS.md` and confirm no drift.
  - Plan ref: Components & files to touch (`make catalog`)
  - Decisions in force: none
  - Forbidden: hand-editing `SKILLS.md` instead of running `make catalog`; committing if `make catalog-check` reports stale
  - Gate: G-build
  - Output: `SKILLS.md`
- [ ] T012 [plugin-and-catalog] Confirm integrations show no drift (verify A-1).
  - Plan ref: Risks & assumptions / A-1
  - Decisions in force: none
  - Forbidden: assuming drift status without running `make integrations-check`; adding `/idea` to a codex/intellij prompt list as part of this slice (out of scope — it is not a single-persona or orchestration command)
  - Gate: G-build
  - Output: implementation note only (`make integrations-check` exits clean; `/idea` is intentionally absent from generated integrations)

## Phase 3 — Behavioural verify

### Surface: triage-behaviour

Experience: classification → route → capture · Contract: spec AC-07…AC-14.

files-owned:
- `reports/verify/idea-command.md`

- [ ] T020 [triage-behaviour] Dry-run one input per category plus a vague input.
  - Plan ref: Test approach / classification table
  - Decisions in force: ADR-001 (recommend-and-confirm; unconditional capture)
  - Forbidden: skipping the `not-worth-doing` or vague cases; accepting a run that asks a third clarifying question; accepting a run where `--title` differs from the `Next:` argument
  - Gate: G-runtime-clean
  - Output: `reports/verify/idea-command.md`
- [ ] T021 [triage-behaviour] Record the whole-feature verify verdict.
  - Plan ref: Sequencing / Phase 3
  - Decisions in force: none
  - Forbidden: declaring done before every AC (AC-01…AC-15) is shown to pass; advancing on a `pending` decision (ADR-001 is `proposed`, not accepted)
  - Gate: every required feature gate
  - Output: `reports/verify/idea-command.md`

## Definition of done

- every task names Plan ref, Decisions, Forbidden, Gate, and Output
- each surface group declares files-owned and the final phase ends in verify
- AC-01…AC-15 from `spec.md` all pass
- `make catalog-check` and `make integrations-check` are clean
- `python tools/check_tasks.py projects/praxis/specs/idea-command/tasks/tasks.md` passes
