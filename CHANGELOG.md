# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Plugin versions are tracked independently in each plugin's
`.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. A repo
release tag (`vX.Y.Z`) marks the state of the whole library at a point in time.

## [Unreleased]

### Added

- **StartupOS module** — an optional, AI-native front door layered on top of
  Praxis that answers *what to build, why, for whom, and how to turn it into a
  company* before Praxis answers *how to build it correctly*. It discovers,
  validates, and designs startup/business ideas, then hands a Praxis-ready
  project to the existing lifecycle. Nothing in existing Praxis behavior changes.
  - **Commands** as flat files `.claude/commands/startupos-<name>.md` (invoked
    `/startupos-<name>` — Claude Code names a command by its file name, so a flat
    `startupos-` prefix keeps the grouping and registers on CLI/desktop/web alike):
    `discover`, `research`, `validate`, `challenge`, `rank`, `select`,
    `business-case`, `prd`, `architecture`, `roadmap`, `export-praxis`. Each
    documents purpose, input, output, workflow, guardrails, approval gates, and
    expected generated files. Symlinked into `plugin-praxis/commands/` like the
    other commands.
  - **Agent skills** under `.claude/skills/startupos-*` (12, Tier 2, each with
    `references/practices.md` + `references/checklist.md`): `startupos-ceo`,
    `startupos-vc-partner`, `startupos-market-analyst`,
    `startupos-customer-researcher`, `startupos-business-designer`,
    `startupos-product-strategist`, `startupos-financial-analyst`,
    `startupos-gtm-strategist`, `startupos-cto`, `startupos-ai-architect`,
    `startupos-security-officer`, `startupos-legal-compliance`. Each agent
    persona is a real, validated Claude Code skill (like the SDLC experts);
    every `/startupos-*` command loads the relevant agent skill(s) and reasons
    in-persona. Symlinked into `plugin-praxis/skills/` and catalogued in
    `SKILLS.md` (now 31 skills).
  - **Documentation** under `docs/startupos/`: `README`, `vision`, `lifecycle`
    (15 stages), `commands`, `templates`, `agents` (12 personas), `memory`,
    `guardrails`, `praxis-integration`, and `integrations` (Cursor / Claude Code
    / Codex).
  - **Templates** under `docs/startupos/templates/` (13): vision, market-research,
    business-case, competitive-analysis, pricing, financials,
    product-requirements, architecture, roadmap, validation-plan, gtm,
    risk-analysis, praxis-handoff.
  - **Memory model** under `memory/startupos/` (ideas, markets, competitors,
    customers, interviews, pricing, financials, hypotheses, experiments,
    decisions, risks, lessons, praxis-handoffs, observations) with a README and
    the *never invent facts* labeling discipline.
  - **Guardrails**: never invent market data; separate facts/assumptions/
    estimates/hypotheses; mandatory human approval before selecting the idea and
    before exporting to Praxis; reject weak ideas; always include risks and
    validation experiments.
  - **Cursor / Codex / IntelliJ integrations** now include StartupOS, generated
    by `build_integrations.py` as a parallel, namespaced set (the SDLC-expert
    outputs are unchanged): twelve `praxis-startupos-*` persona guides per tool,
    the eleven lifecycle commands as `/startupos-*` (Cursor) and
    `/praxis-startupos-*` (Codex) prompts, plus a StartupOS roster per tool (the
    `praxis-startupos` Cursor rule, a StartupOS section of Codex's
    `AGENTS.praxis.md`, and IntelliJ's `.junie/praxis-startupos.md`). For Codex
    the roster is merged into `AGENTS.praxis.md` so the single documented append
    wires it (no separate file to forget). Each tool's always-read entry doc —
    Cursor's always-on `praxis` rule, Codex's `AGENTS.praxis.md`, IntelliJ's
    `guidelines.md` — points to StartupOS so it is discoverable, not merely
    description-gated. Integration file count: 99 → 170.
  - **README and GitHub Pages** updated with a StartupOS section (without
    overstating it as the purpose of Praxis).

## [1.16.0] - 2026-06-24

### Added

- **Spec-driven experience-grounding workflows** in the `ux-ui-engineer` skill
  (now tier 3, v1.1.0) — a non-owning layer that injects UX, UI, accessibility,
  and design-system discipline into any spec-driven / SDD / PRD-to-build
  process without owning its specs, plans, tasks, or code. Five workflows under
  `.claude/skills/ux-ui-engineer/workflows/`: `experience-grounding` (guided
  run: process detection, artifact map, upfront idea interview, per-phase
  routing), `experience-governance-seed`, `experience-phase-contributions`,
  `experience-design-system-grounding`, and `experience-design-checklist`.
- **New UX references** backing the grounding gates: `ux-comprehension-and-friction`
  (`G-ux`), `imagery-visuals-and-taste` (`G-imagery`), `landing-conversion`
  (`G-landing`), plus `gate-phase-map`, `interview-protocol`,
  `implementation-guardrails`, `governance-design-articles`, and
  `design-rationale-snippet`. Duplicate gate references were dropped and their
  gates repointed to the existing `practices.md` and `checklist.md`.
- **Portable experience-grounding guide** in the generated Cursor/Codex/IntelliJ
  integrations, so the grounding workflow set and its references travel to other
  IDEs as a self-contained doc rather than dangling links.

## [1.15.0] - 2026-06-18

### Added

- **Optional `deploy` phase** for the `feature-development` lifecycle — a
  terminal, config-gated step that provisions/updates infrastructure with
  Terraform and ships to a declared cloud target (generic Kubernetes, AWS/EKS,
  GCP/GKE, Azure/AKS), driven through an **MCP server** when one is configured,
  with a plan-only fallback otherwise. It mirrors the optional `experience`
  step: it enters on `release-approved` and, when no `deploy` target is declared
  in `.praxis/config.json`, records a skip and advances — a cloud target is
  never assumed. Doctrine in
  `.claude/skills/devops-engineer/references/deploy.md` (devops-engineer →
  v1.2.0); wired into `workflows/feature-development.workflow.json` and the
  `/new-feature` orchestration, with a `reports/release/deploy-report.md`
  artifact and scaffold template.
- **Enforceable deploy gates**, each backed by a deterministic tool:
  `deploy-plan-guardrails` (Infracost cost budget, OPA/Conftest policy-as-code,
  tfsec/Checkov IaC scan over the terraform plan — fail-closed on production),
  `deploy-supply-chain` (SBOM via Syft, cosign signature, SLSA provenance,
  admission control), and `deploy-healthy` (SLO error-budget burn-rate plus
  DORA capture).
- **`deploy` config block** in `schemas/praxis-config.schema.json`
  (`targets`, `mcpServers`, `guardrails`, `supplyChain`, per-target `slo`),
  including a conditional rule that a `production` target must set
  `promotion: "manual"`. MCP servers carry pinned sources and a mandatory
  digest-pinning note (supply-chain control).

### Changed

- README, GitHub Pages (`docs/index.html`), `docs/harness-mode.md`, and the
  **Software Developer Life Cycle diagram** (`.mmd` + infographic + re-rendered
  PNG) updated to show the optional deploy phase end to end.

## [1.13.0] - 2026-06-11

### Added

- **Semantic model tiers** (`rules/model-tiers.md`) — lifecycle commands now
  name `light` / `standard` / `deep` tiers instead of hardcoded vendor models,
  so the doctrine ports across runtimes (Claude Code, Codex, Cursor, Junie) and
  model generations. Tiers resolve through a new optional `models` map in
  `.praxis/config.json` (added to `schemas/praxis-config.schema.json`); when
  absent, runtimes fall back to their own defaults (Claude Code:
  `haiku`/`sonnet`/`opus`, with `deep` remappable higher — e.g. `fable`).

### Changed

- **Cheap-by-default model policy** — `/new-feature`, `/fix-bug`, and `/refine`
  now default *every* phase to the `standard` tier; a phase must *earn* `deep`
  (a genuinely hard design, a complex root cause, a high-stakes domain
  analysis), and the orchestrator reports which phases it escalated and why.
  Previously the design/build phases ran on the frontier tier by reflex.
- **Shorter skill and command descriptions** — all 19 skill frontmatter
  descriptions, the most verbose command descriptions (`/idea`, `/learn`,
  `/patterns`, `/ml`), and the plugin manifest were tightened (~45% smaller on
  average) to cut the fixed per-request context cost the plugin adds to every
  session, while keeping the triggering keywords intact. `SKILLS.md` and the
  cursor/codex/intellij integrations regenerated to match.

## [1.12.0] - 2026-06-11

### Added

- **SonarQube-aligned code-quality metrics rule** (`rules/code-quality-metrics.md`)
  — a new harness rule giving `developer`, `qa-engineer`, `software-architect`,
  and `security-engineer` a shared vocabulary and default min/max thresholds
  (Coverage on new code >= 80%, Duplicated Lines on new code <= 3%,
  Maintainability/Reliability/Security Rating = A, Security Hotspots Reviewed
  = 100%, Cyclomatic Complexity <= 10, Cognitive Complexity <= 15, with the
  Technical Debt Ratio bands behind the Maintainability Rating), aligned to
  SonarQube's default "Sonar way" Quality Gate. The rule is explicit that a
  repo's own configured quality gate is binding when one exists — these are
  defaults and a shared vocabulary, not a new mandatory gate. Wired into
  `developer` (DRY/complexity practices and pre-merge checklist),
  `qa-engineer` (test-readiness coverage item), `software-architect`
  (checklist item 8.7, alongside the 8.6 hotspot signal), and
  `security-engineer` (pipeline-gates checklist, ahead of `G-security`).

- **Systemic-complexity hotspot detection in `/patterns`** — the pattern miner
  (`tools/patterns.py`) now also reads `implementation` ledger entries' "Files
  touched" lists and surfaces a file/module recurring across 3+ *distinct*
  specs/refinements as a **hotspot**: a candidate for `/refine`. Touched files
  are deduplicated by the originating spec/refinement (the `source:<id>` tag
  on the implementation entry, falling back to the entry's own id), so several
  iterative implementation snapshots of one spec collapse to a single hit
  instead of inflating the count once per snapshot. `CHANGELOG.md` and the
  generated `SKILLS.md` / `integrations/**` bundles are excluded from the
  signal — they are touched by nearly every change and would otherwise
  dominate the list without indicating anything. The software-architect's
  "Avoiding over-engineering and accidental complexity" practice gains a new
  "Systemic complexity" subsection covering this evidence-based, no-new-gate
  signal, and the architecture review checklist gains item 8.6 to act on it.

## [1.11.0] - 2026-06-10

### Added

- **Team conventions captured into four role experts** (via `/learn`, accepted
  ledger decision `20260610-181128-01db`, refined by `20260610-181909-202f`):
  **no non-functional inline comments** — code self-explains; functional tool
  directives (`noqa`, `eslint-disable`, pragmas) are code, not commentary; the
  one permitted informative comment states a constraint the code cannot
  express (invariant, external requirement, deliberate trade-off, security
  warning); no commented-out code or inline TODO/FIXME; docstrings on public
  APIs and ADRs remain the documented homes for interface docs and design
  rationale — and **test-first for complex logic** — unit tests are written
  before implementing observably complex logic (non-trivial conditionals,
  calculations, parsing, state machines, concurrency, security-sensitive
  paths); bug fixes start with the failing regression test; trivial glue may
  be test-after, but no complex logic merges untested. Landed in the
  `developer` practices + checklist, the `qa-engineer`, `security-engineer`,
  and `software-architect` checklists, and the architect's testability NFR
  and ADR discipline.

- **`U-11` — executing on a pending authorization is now a catalogued hard stop**
  ([`rules/stop-conditions-catalog.md`](rules/stop-conditions-catalog.md)) —
  work whose only authorization is a still-`pending` artifact (a memory-ledger
  decision/plan, a `spec.md` at `status: draft`, an ungiven HITL gate approval)
  halts with `STOP[U-11]` until the user explicitly accepts or rejects it.
  "Pending is not approval" was already doctrine throughout; it now also has a
  deterministic catalog id, cited by the validation-orchestrator and by the
  judgement half in [`rules/stop-conditions.md`](rules/stop-conditions.md).
- **Memory hook: pre-ship pending nudge**
  ([`integrations/hooks/memory.settings.example.json`](integrations/hooks/memory.settings.example.json))
  — a `PreToolUse` hook on `git commit` / `git push` re-surfaces the ledger
  entries still awaiting accept/reject (`ledger.py pending --brief`), so work
  built on an unaccepted proposal is caught before it ships. A stderr nudge,
  never a block (exit 0 always) — planning runs legitimately commit with
  everything pending.

### Changed

- **Accept is the trigger — accepting an entry now drives execution.** The
  mirror of "pending is not approval": when the user accepts a `plan`,
  `decision`, `test-strategy`, or `rollout` whose work has not been done yet,
  that acceptance is the green light and the work is carried out in the same
  turn — the user does not have to ask twice. Codified in the memory skill's
  rules and review workflow, the `/memory` command's accept route, and the
  eight consult-command reminders; `ledger.py accept` now prints an explicit
  "acceptance is the green light — carry it out now" nudge for actionable
  entry types (with tests).
- **Consult commands now restate the acceptance gate.** The eight expert
  commands that record `pending` artifacts (`/analyst`, `/architect`,
  `/developer`, `/devops`, `/product`, `/qa`, `/security`, `/ux`) now close
  their *Always-on docs* section with the rule that a recorded ADR / plan /
  strategy is a proposal, not authorization: do not implement it until the user
  explicitly accepts it (`/memory accept <id>`) — pending is not approval
  (`U-11`). Previously the rule lived only in the memory skill,
  `rules/stop-conditions.md`, and the lifecycle commands, so a consult command
  followed by "ok, do it" had no in-command guard.

## [1.10.0] - 2026-06-09

### Added

- **`/idea` — intake & triage front door** ([`.claude/commands/idea.md`](.claude/commands/idea.md))
  — a thin command that takes a raw idea, clarifies it (≤2 questions), classifies
  it (`feature` → `/new-feature`, `bug` → `/fix-bug`, `refinement` → `/refine`,
  `not-worth-doing` → no route), captures a `pending` note in the memory ledger
  (`--source /idea --tags intake,<class>`), and recommends the next command. It
  classifies, captures, and recommends — it never plans, specs, or runs the
  lifecycle. A command, not a skill (per promotion-policy). Designed end-to-end
  through the harness lifecycle under
  [`projects/praxis/specs/idea-command/`](projects/praxis/specs/idea-command/).

### Changed

- **Harness mode is now always on (was opt-in).** Harness behavior is praxis's
  default and only operating mode — the `if not in harness mode, behave as before`
  fallback is gone from `/new-feature`, `/fix-bug`, `/refine`, and
  `/review-changes`. A missing `.praxis/config.json` is no longer treated as
  "no harness"; it is **auto-bootstrapped**.
  - New [`tools/ensure_harness.py`](tools/ensure_harness.py) (`make harness-init`)
    — idempotent, stdlib-only. On the first lifecycle command it derives a project
    id from the repo name and writes the config + project memory: `central` mode
    under `projects/<id>/` for the harness repo itself, `local` mode under
    `.praxis/project/` for a consuming repo. A no-op once initialized.
  - **Stop conditions narrowed:** a *missing* config is not a hard block (it is
    bootstrapped); only a config that is *present but broken* (malformed, or a
    `projectId` that does not resolve) stops the agent — it asks rather than
    overwriting. Updated [`rules/stop-conditions.md`](rules/stop-conditions.md)
    and [`rules/source-of-truth.md`](rules/source-of-truth.md).
  - Doctrine + docs updated throughout (AGENTS.md, README, `docs/harness-mode.md`,
    the GitHub page) from "opt-in / experimental" to "always on".

## [1.9.0] - 2026-06-09

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
    `make patterns`, and the `/patterns` command) — sweeps the ledger + run logs
    for recurring tags, sources, and stop conditions and surfaces them as
    human-gated promotion candidates, routed into `/learn`.
  - **`G-performance` now has an owning expert** — `software-architect` gains
    [`references/performance-review.md`](.claude/skills/software-architect/references/performance-review.md)
    (build-time budgets, review method, regression threshold), with
    `devops-engineer` owning the runtime/SLO side, so the gate routes to a named
    role like `G-security` does. No new skill (per promotion-policy).
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

[Unreleased]: https://github.com/marcrabadan/praxis/compare/v1.9.0...HEAD
[1.9.0]: https://github.com/marcrabadan/praxis/compare/v1.0.0...v1.9.0
[1.0.0]: https://github.com/marcrabadan/praxis/releases/tag/v1.0.0
