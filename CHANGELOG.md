# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Plugin versions are tracked independently in each plugin's
`.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. A repo
release tag (`vX.Y.Z`) marks the state of the whole library at a point in time.

## [Unreleased]

### Added

- **PSDOS gap-closure: mandatory security/performance gates, criteria-checked
  gates, front-half states, failure transitions, a Validation Orchestrator, and
  a pattern miner.** Brings the `feature-development` harness lifecycle closer to
  a faithful PSDOS implementation:
  - **Mandatory `G-security` + conditional `G-performance` verify gates**
    ([`workflows/feature-development.workflow.json`](workflows/feature-development.workflow.json))
    — a feature can no longer reach `release` without a recorded security review;
    high/critical findings are fixed or carry an approved risk-acceptance
    decision. Wired into `loops.verify` and the verify-report template.
  - **Criteria-checked gates** (`gateCriteria`) — HITL approval tokens
    (`approved-discovery`, `approved-product-definition`, `approved-spec`,
    `architecture-validated`, `release-candidate-ready`) now carry explicit,
    checkable criteria, so an approval is a checklist not a vibe.
    `architecture-validated` gives architecture its own pass/fail via
    [`plans/architecture-review.md`](projects/_template/specs/_template/plans/architecture-review.md).
  - **Front-half + back-half states** — `product-definition` (PO-owned MVP/scope/
    metrics) and `release-candidate` (proven-correct vs decided-to-ship) are now
    explicit states with their own artifacts.
  - **Failure protocol** (`transitions.onGateFailure`) — a failed gate routes
    back to its mapped rework state (root-cause → return → revalidate), never a
    bypass. Validated by `tools/validate_harness.py`.
  - **Validation Orchestrator** ([`.claude/skills/validation-orchestrator/`](.claude/skills/validation-orchestrator/SKILL.md),
    `/validation-orchestrator`) — the standing role with sole authority to halt
    progression; adjudicates each gate to a closed-set verdict
    (`advance | block | escalate`).
  - **Continuous-learning pattern miner** ([`tools/patterns.py`](tools/patterns.py),
    `make patterns`) — sweeps the ledger + run logs for recurring tags, sources,
    and stop conditions and surfaces them as human-gated promotion candidates.
- **Spec-driven verification spine + self-evolving doctrine.** A set of
  opt-in harness capabilities that make "iterate until it's actually correct"
  deterministic and bounded, and let the harness learn under a human gate:
  - **Never assume, always validate** ([`rules/never-assume.md`](rules/never-assume.md),
    `tools/assumptions.py`) — low-confidence guesses are logged to an assumptions
    ledger and replayed to the user as an A/B/C question-flow (`sweep`), then
    resolved into a decision.
  - **Loop control** ([`rules/loop-control.md`](rules/loop-control.md),
    `tools/loop.py`) — the `verify` step runs as a bounded convergence loop with a
    terminal predicate, budget, and no-progress guard; it meets the predicate
    (`done`) or escalates, never spins. Wired into every workflow's `verify` step
    via `loops.verify` (+ `onContinue` back-edge).
  - **Enumerated stop-conditions catalog** ([`rules/stop-conditions-catalog.md`](rules/stop-conditions-catalog.md),
    `schemas/stop-conditions.schema.json`) — `U-1…U-10` universal hard blockers
    with exact `STOP[...]` text and resolution gates, plus per-spec `P-*`/`S-*`
    additions and a run-log incident protocol; the deterministic counterpart to
    the assumptions ledger.
  - **Experience contracts** (`schemas/experience-contract.schema.json`) — an
    optional `experience` step between spec and plan that turns each declared
    surface into an executable, verifiable contract (markdown + validating JSON).
  - **Typed gate catalog + verify report** — a `gateCatalog` of `G-*` gates in the
    workflow schema, referenced by `loops.verify` and experience contracts; verify
    reports record a per-gate result with reviewer sign-off and forbid
    self-certification (`U-8`).
  - **Per-task anti-drift** — tasks carry `Forbidden / Gate / Output` + `files-owned`,
    linted by `tools/check_tasks.py` (`make check-tasks FILE=…`).
  - **Promotion executor** (`tools/promote.py`) — promotes a validated assumption
    into a `pending` rule/gate/eval/guardrail in the memory ledger, routed via
    `skill-learner` (promote on evidence; propose, never mutate; human-gated).
  - **Ambient validation hook** ([`integrations/hooks/validation.settings.example.json`](integrations/hooks/validation.settings.example.json))
    surfaces open assumptions and escalated loops at SessionStart and before a
    commit/push.

  Adds the `feature-development` `experience` step, expands `spec.schema.json`
  (optional `experienceInventory`), and extends `tools/validate_harness.py` with
  experience-contract, gate-catalog, and stop-condition checks (harness tests grow
  to 92). All opt-in; existing specs are unaffected. Bumps the `praxis` plugin to
  `1.8.0`.

- **`skill-learner` — the factory's learning loop** (Tier 3). Turns a knowledge
  gap discovered during expert work — a missing org convention, runbook, or rule
  (e.g. how *this team* builds infra in Terraform/Azure) — into durable,
  auditable skill knowledge. It detects the gap, decides where the knowledge
  belongs (a `references/` file inside the role expert by default; a new skill
  only on evidence per the promotion policy — role experts stay
  language-agnostic), delegates authoring to `skill-creator`, and **proposes**
  the result through the memory ledger as `pending` (never mutates a skill
  silently). Captures org-specific conventions, not public facts the model
  already knows. Ships three workflows (detect-gap, refine-existing, create-new),
  governing rules, worked examples, routing trigger-evals, and a `/learn`
  command.

### Changed

- **Merged the two plugins into one self-contained `praxis` plugin.** The
  separate `skill-factory` plugin is removed; `plugin-praxis` now also carries
  `skill-creator`, `skill-learner`, the `factory/` tooling, `/learn`, and
  `/validate-skills` (via symlinks). A single `/plugin install praxis@praxis`
  now brings the experts **and** the skill factory, so the learning loop
  (`skill-learner` delegates to `skill-creator`) always has its dependency and
  there is no second install to remember. Updates `marketplace.json`, the plugin
  manifest, AGENTS.md, README, USECASES, and the docs site. Bumps the `praxis`
  plugin to `1.6.0`.

- **Harness mode (phases 3, 5–8)** — completes the agent-harness layer on top of
  phase 1. Adds **durable spec artifacts** (`/new-feature`, in harness mode, now
  writes `spec.md` + `plans/` + `tasks/` + `decisions/` + `reports/` under
  `projects/<project>/specs/<spec>/` following a `spec → plan → tasks → verify`
  workflow, instead of leaving the plan only in chat; `schemas/spec.schema.json`,
  `systems/feature-development/`, and a `projects/_template/specs/_template/`
  scaffold). Adds **workflow gates** (`workflows/registry.json` + manifests,
  `schemas/workflow.schema.json`) validated mechanically. Adds **runtime state**
  (`runtime/`, `schemas/session-state.schema.json`, `tools/runtime.py`) as
  disposable, git-ignored session glue kept separate from durable memory. Adds
  **adapter wiring** (`tools/install_adapter.py` to scaffold a repo's
  `.praxis/config.json` + `.praxis/current-spec.md`, and a shared **read-order
  block** injected into the generated Cursor/Codex/IntelliJ entry docs). Hardens
  **`/review-changes`** to load project authority, accepted decisions, and the
  active spec, and to record outcomes only as `pending`. `tools/validate_harness.py`
  now also checks specs, workflow manifests, and runtime state; harness tool tests
  (`tools/test_harness_tools.py`) run in `make test` and CI. All command behavior
  is **opt-in** (activates only when a `.praxis/config.json` resolves a project),
  so non-harness repos are unaffected. Bumps the `praxis` plugin to `1.5.0`.

- **Harness mode (phase 1)** — the first step from a skill factory toward a fuller
  **agent harness**: an authority model that tells agents where to read first,
  what is canonical, where durable decisions go, and when to stop and ask. Adds a
  first-class **rules layer** (`rules/source-of-truth.md` — canonical vs generated
  vs runtime, and the authority order; `rules/stop-conditions.md` — when to stop
  and ask, plus hard blocks), **per-project memory** (`projects/projects-index.md`
  and `projects/_template/` with `PROJECT.md`, `linked-repos.md`, and
  `memory/current-state.md` + `open-questions.md`), two JSON **schemas**
  (`schemas/project.schema.json`, `schemas/praxis-config.schema.json`), and a
  **deterministic validator** (`tools/validate_harness.py`, no LLM) that checks
  the registry, project-memory shape, schemas, and a consuming repo's
  `.praxis/config.json`. Repos opt in with a small `.praxis/config.json` pointer
  ([`examples/praxis-config.example.json`](examples/praxis-config.example.json));
  the model is **hybrid with `local` (per-repo) as the default** and `central` as
  an opt-in for multi-repo teams. Wired into the Makefile (`make validate-harness`)
  and CI, documented in [`docs/harness-mode.md`](docs/harness-mode.md), surfaced
  in the README and the GitHub Pages site (a new "Harness mode" section + example
  card), and **changes no existing skill, command, or `/new-feature`**. Bumps the
  `praxis` plugin to `1.4.0`.

- `/new-feature` — **token-efficiency** controls. An optional **context digest**
  (Phase 0.5) gathers the relevant codebase/PRD context once on a cheap model
  (Haiku `Explore` subagent) and feeds that digest to every later phase, so
  experts stop re-reading the same material. Each phase now also runs at the
  **model tier its work needs** — Opus for deep design/build reasoning
  (architect, developer, domain experts), Sonnet for the artifact-transforming
  phases (BA, PO, QA, DevOps), Haiku for retrieval only. Bumps the `praxis`
  plugin to `1.2.0` and regenerates the Cursor/Codex/IntelliJ integrations.

- `memory` skill — a **bootstrap / `/memory init`** flow that primes an empty
  ledger from the repo's existing context so memory reflects the project from day
  one. Adds a deterministic `ledger.py bootstrap [--brief]` subcommand (init +
  a report of durable-context docs — `AGENTS.md`, ADRs, architecture docs — and a
  git-history summary; it never writes entries), a `workflows/bootstrap.md`
  procedure, `/memory init` routing, and a SessionStart hook line that suggests
  seeding when the ledger is empty (the closest thing to an on-install step).
- `ml-ai-engineer` skill (Tier 2) — an **ML/AI Engineer** SDLC expert covering the
  full model lifecycle: problem framing & metric selection, ML-ready features
  (leakage, train/serve skew, feature stores), training & selection, rigorous
  evaluation, experiment tracking & reproducibility, serving & deployment
  (batch/online, shadow/canary, A/B), MLOps, drift monitoring & retraining,
  responsible AI (bias, fairness, explainability, privacy), and modern LLM/GenAI
  engineering (RAG, prompting, fine-tuning, evals, guardrails, cost/latency).
  Ships `references/practices.md`, a model production-readiness
  `references/checklist.md`, an `/ml` slash command, plugin symlinks, and
  Cursor/IntelliJ/Codex integrations. This brings the roster to thirteen SDLC
  experts.
- `data-engineer` skill (Tier 2) — a **Data Engineer** SDLC expert covering the
  full data platform: batch & streaming pipelines (ETL/ELT, CDC), warehouse/lake/
  lakehouse and dimensional modeling, orchestration (dbt/Airflow/Dagster), data
  quality & contracts, lineage & governance, partitioning, and DataOps & cost.
  Ships `references/practices.md`, a data-product `references/checklist.md`, a
  `/data` slash command, plugin symlinks, and Cursor/IntelliJ/Codex integrations.
  This brings the roster to twelve SDLC experts.
- `memory` skill (Tier 4) — a versioned **memory ledger** that records plans,
  decisions, implementations, and artifacts under `.praxis/memory/` (committed
  to git), each with a `pending → accepted | rejected | rolled-back` lifecycle.
  Ships a deterministic `ledger.py` CLI (`log`, `snapshot`, `list`, `pending`,
  `show`, `accept`, `reject`, `rollback`, `status`), a `/memory` slash command,
  capture/review/rollback workflows, plugin symlinks, and an opt-in hook template
  (`integrations/hooks/memory.settings.example.json`) that surfaces pending
  entries at session start and snapshots changes on stop. `/new-feature` and
  `/review-changes` now record their artifacts to the ledger.
- Three frontend SDLC expert skills: `ux-ui-engineer`, `frontend-architect`,
  and `frontend-engineer` (Tier 2), each with `practices.md` and `checklist.md`
  references, a per-expert slash command (`/ux`, `/frontend-architect`,
  `/frontend`), plugin symlinks, and `/review-changes` routing.
- `LICENSE` (Apache-2.0) and `NOTICE`, making the project open source.
- `SECURITY.md` with a private vulnerability-reporting process.
- `CHANGELOG.md` (this file) and a documented versioning scheme.

### Changed

- **`memory` doctrine: decisions are cross-role, `pending` is not approval, and
  statuses are a closed set.** Decision entries are no longer framed as the
  architect's alone — the doctrine, provenance guidance, capture examples,
  `/new-feature`, and the global "leave a record" rule now record PO
  prioritization calls, QA test-strategy gates, DevOps deploy choices, and
  security risk acceptances under their own `--source`. A `pending` entry is
  stated explicitly to be a *proposal awaiting the user's call* — surface it and
  get an explicit `accept` before executing the work it authorizes; recording is
  not approval. The five statuses (`pending`, `accepted`, `rejected`,
  `superseded`, `rolled-back`) are documented as a closed, authoritative set the
  CLI enforces, with each one defined and inventing new statuses forbidden.
  Reconciles the `praxis` plugin manifest (`plugin.json`) to `1.1.0` to match the
  marketplace.
- **`/new-feature` now runs each SDLC phase in its own subagent** instead of
  loading all six expert skills into one growing conversation. Each expert's
  doctrine (`SKILL.md` + `references/`) loads in an isolated context and only
  its compact artifact returns to the main thread, so skill references no
  longer accumulate or get re-read phase after phase. Phases draw on
  `practices.md` to generate and self-check against `checklist.md` (instead of
  eagerly loading both up front, which contradicted each skill's own "do not
  load both" guidance). QA and DevOps — which depend only on the earlier
  phases, not on each other — are dispatched in parallel. The orchestrator now
  also **routes in the conditional domain experts a feature warrants** — adding
  `ml-ai-engineer`, `data-engineer`, `security-engineer`,
  `cybersecurity-architect`, `frontend-architect`, `frontend-engineer`, or
  `ux-ui-engineer` as an extra parallel phase after the Architect — so an ML- or
  security-heavy feature is no longer left to the core six alone. Net effect: far
  less main-thread context, lower latency, and the right specialist in the room
  — at the same quality. Ported Cursor / Codex / IntelliJ integrations keep the
  single-thread behaviour (those tools have no subagents). Bumps the `praxis`
  plugin to `1.1.0`.
- Hardened the `validate` GitHub Actions workflow with a least-privilege
  `permissions: contents: read` block.
- Updated the README License section to reflect the Apache-2.0 license.

## [1.0.0] - 2026-05-31

### Added

- Initial public release of the **praxis** skill factory.
- `skill-creator` meta-skill — the pattern for scaffolding, classifying,
  reviewing, and validating new Claude Code skills.
- Eight SDLC expert skills: business-analyst, product-owner,
  software-architect, developer, qa-engineer, devops-engineer,
  security-engineer, and cybersecurity-architect.
- Per-expert slash commands and the `/new-feature` orchestrator.
- `/review-changes` diff router plus opt-in CI and local-hook integrations.
- Two distributable plugins (`praxis` and `skill-factory`) at version `1.0.0`,
  published via `.claude-plugin/marketplace.json`.
- Deterministic skill generator, validators, catalog builder, and CI.

[Unreleased]: https://github.com/marcrabadan/praxis/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/marcrabadan/praxis/releases/tag/v1.0.0
