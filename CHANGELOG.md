# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Plugin versions are tracked independently in each plugin's
`.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. A repo
release tag (`vX.Y.Z`) marks the state of the whole library at a point in time.

## [Unreleased]

### Added

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
