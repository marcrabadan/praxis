# AGENTS.md

This is the single source of truth for agent behavior in this repository. Claude Code (and any compatible agent) should read this file first, then follow the links below for specifics.

## What this repo is

`praxis` is a **skill factory** for your team or organization. Its only purpose is to **create, improve, evaluate, and ship Claude Code skills**. It centers on one meta-skill — the pattern for creating new skills — plus a set of SDLC expert skills built with that pattern.

It is **not**:

- a product repo;
- an application repo;
- a design-system implementation repo;
- a place to store production React or backend code.

Any code produced here is an example, a fixture, a generator script, or a packaged skill artifact. Production code belongs in product repositories.

## Required reading before acting

1. [.claude/factory/ai/operating-model.md](.claude/factory/ai/operating-model.md) — what the repo is, what it is not, and the global rules.
2. [.claude/factory/ai/skill-tiering.md](.claude/factory/ai/skill-tiering.md) — tier definitions and the classification decision tree.
3. [.claude/factory/ai/routing.md](.claude/factory/ai/routing.md) — how skills should be triggered and described.

When working on code-producing skills, also read [.claude/factory/ai/implementation-principles.md](.claude/factory/ai/implementation-principles.md).
When deciding whether to split a workflow into its own top-level skill, read [.claude/factory/ai/promotion-policy.md](.claude/factory/ai/promotion-policy.md). Default to keeping the workflow inside its parent until evidence justifies promotion.

## Canonical entry points

- **Create, improve, review, evaluate, or classify a skill** → use [.claude/skills/skill-creator/SKILL.md](.claude/skills/skill-creator/SKILL.md). This is the **pattern for creating new skills** — the primary meta-skill in the repo.
- **Learn from a gap discovered during work** (an expert lacks an org convention, runbook, or rule — e.g. how *this team* builds infra in Terraform/Azure) → use [.claude/skills/skill-learner/SKILL.md](.claude/skills/skill-learner/SKILL.md), or `/learn`. It detects the gap, decides where the knowledge belongs (a reference inside the role expert by default; a new skill only on evidence), delegates the authoring to `skill-creator`, and **proposes** the result through the memory ledger as `pending` — it never mutates a skill silently. Captures org-specific conventions, not public facts the model already knows.
- **Run a guided interview to capture an objective** → use [.claude/skills/skill-creator/workflows/interview.md](.claude/skills/skill-creator/workflows/interview.md).

Skills are **Claude Code native**: each lives at `.claude/skills/<name>/SKILL.md` and Claude Code discovers it automatically from its frontmatter (no `command.md`, no installers). Invoke a skill by describing the task or by typing `/<name>`.

Alongside the meta-skill, the repo ships thirteen **SDLC expert skills** — one per role in the software delivery lifecycle:

- [.claude/skills/business-analyst/](.claude/skills/business-analyst/) — requirements, user stories, acceptance criteria.
- [.claude/skills/product-owner/](.claude/skills/product-owner/) — backlog, prioritization, roadmap, OKRs.
- [.claude/skills/software-architect/](.claude/skills/software-architect/) — architecture, ADRs, NFRs, trade-offs.
- [.claude/skills/developer/](.claude/skills/developer/) — clean code, testing, PR hygiene, refactoring.
- [.claude/skills/qa-engineer/](.claude/skills/qa-engineer/) — test strategy, test design, bug reports.
- [.claude/skills/devops-engineer/](.claude/skills/devops-engineer/) — CI/CD, IaC, observability, releases.
- [.claude/skills/security-engineer/](.claude/skills/security-engineer/) — threat modeling, OWASP Top 10, authn/authz, secrets, crypto, SAST/DAST/SCA, CVSS triage.
- [.claude/skills/cybersecurity-architect/](.claude/skills/cybersecurity-architect/) — zero trust, IAM, segmentation, data protection, key management, control frameworks, compliance, risk.
- [.claude/skills/ux-ui-engineer/](.claude/skills/ux-ui-engineer/) — design systems, tokens, visual & interaction design, accessibility (WCAG), responsive layout, usability, UX writing, handoff.
- [.claude/skills/frontend-architect/](.claude/skills/frontend-architect/) — framework & rendering strategy, state/data/routing architecture, build & bundling, design-system architecture, Core Web Vitals.
- [.claude/skills/frontend-engineer/](.claude/skills/frontend-engineer/) — component implementation, state & data wiring, forms, styling, frontend TypeScript, performance, a11y implementation, testing.
- [.claude/skills/data-engineer/](.claude/skills/data-engineer/) — data pipelines (ETL/ELT, batch & streaming, CDC), warehouse/lake/lakehouse modeling, dimensional/star schemas, orchestration (dbt/Airflow/Dagster), data quality & contracts, lineage & governance, DataOps & cost.
- [.claude/skills/ml-ai-engineer/](.claude/skills/ml-ai-engineer/) — model lifecycle: problem framing & metrics, ML-ready features (leakage, train/serve skew, feature stores), training & evaluation, experiment tracking, serving & deployment (shadow/canary/A-B), MLOps, drift monitoring & retraining, responsible AI, and LLM/GenAI (RAG, prompting, fine-tuning, evals, guardrails).

Each SDLC expert also has a short **slash command** under [.claude/commands/](.claude/commands/) for addressing it directly — `/architect`, `/developer`, `/qa`, `/analyst`, `/product`, `/devops`, `/security`, `/security-architect`, `/ux`, `/frontend-architect`, `/frontend`, `/data`, `/ml` — e.g. `/architect how do I avoid this race condition?`. Each command loads its matching skill and answers in that persona. `/new-feature <idea>` orchestrates the core six (BA → PO → architect → developer → QA → devops) in lifecycle order — each phase in its own subagent so doctrine stays out of the main thread — and automatically routes in the specialist experts (security, frontend, data, ML/AI, UX) a feature warrants, to produce a consolidated plan; those same specialists are also available on demand and via `/review-changes`. `/review-changes` routes the current diff to the relevant experts (including the security experts) and returns severity-tagged, didactic findings; opt-in CI and local-hook templates in [integrations/](integrations/README.md) trigger it automatically on PRs and before pushing.

Beyond the SDLC roster, the repo ships one **utility skill**: [.claude/skills/memory/](.claude/skills/memory/) — the **memory ledger**. It records the plans, decisions, implementations, and artifacts the experts produce as durable, git-committed entries under `.praxis/memory/`, each with a status from one closed set — `pending → accepted | rejected | rolled-back` (plus `superseded`). Manage it with `/memory` (list, accept/reject, roll back) or let it run automatically via the opt-in hook in [integrations/hooks/memory.settings.example.json](integrations/hooks/memory.settings.example.json).

Do not invent a new top-level skill when an existing workflow in `skill-creator` covers the use case.

## Harness mode (experimental)

Beyond the skill factory, praxis has an **agent-harness** layer that gives agents
a reliable operating environment — source-of-truth authority, project memory,
durable spec artifacts, workflow gates, runtime state, and deterministic
validators. All harness behavior in commands is **opt-in**: it activates only
when a repo has a `.praxis/config.json` that resolves a project, so non-harness
repos are unaffected. Start at [docs/harness-mode.md](docs/harness-mode.md).

- [rules/source-of-truth.md](rules/source-of-truth.md) — what is canonical vs
  generated vs runtime, and the authority order to follow on conflict.
- [rules/stop-conditions.md](rules/stop-conditions.md) — when an agent must stop
  and ask instead of guessing.
- [projects/](projects/projects-index.md) — per-project memory (current state,
  open questions, decisions) and `specs/`; copy `projects/_template/` to start one.
- [systems/feature-development/](systems/feature-development/artifact-model.md) —
  the lifecycle doctrine + artifact model behind `/new-feature` in harness mode.
- [workflows/](workflows/registry.json) — machine-readable lifecycles (steps,
  gates, stop conditions). `feature-development` is `spec → plan → tasks → verify`.
- [schemas/](schemas/) — `project`, `praxis-config`, `spec`, `workflow`, and
  `session-state` JSON shapes.
- [runtime/](runtime/README.md) — disposable session state (git-ignored), via
  `tools/runtime.py`. Durable decisions never live only here.
- [tools/](tools/validate_harness.py) — `validate_harness.py` (run
  `make validate-harness`; CI enforces it), `install_adapter.py`, `runtime.py`.

A repo opts in by adding `.praxis/config.json` pointing at this harness and a
project id (scaffold it with `tools/install_adapter.py`). If the project id can't
be resolved, **stop** (see stop-conditions). **Pending is not approval** — don't
advance a workflow gate on a pending decision.

## Global rules

- **Classify the tier before scaffolding.** Every skill request must be matched to a tier (1–5) using the criteria in [.claude/factory/ai/skill-tiering.md](.claude/factory/ai/skill-tiering.md).
- **Run the interview when intent is incomplete.** Do not guess scope, output format, or trigger conditions. Ask one question at a time with suggested answers.
- **Skills are Claude Code native.** A skill is a `SKILL.md` with `name` + `description` frontmatter under `.claude/skills/<name>/`. There is no `command.md` and no installer — Claude Code discovers the skill from its frontmatter.
- **Use deterministic validators where possible.** Do not ask an LLM to count files or check JSON shape — call [.claude/factory/validators/validate_skill.py](.claude/factory/validators/validate_skill.py) instead.
- **Prefer existing templates** in [.claude/factory/templates/](.claude/factory/templates/) over inventing folder structure. The generator script at `.claude/skills/skill-creator/scripts/create_skill.py` is the canonical way to produce a scaffold; it emits `SKILL.md` plus the tier-appropriate folders.
- **Where new skills land:** by default at `dist/<skill-name>/` (scratch). Promote to `.claude/skills/<skill-name>/` once the skill is intended as a shared, factory-owned asset that the org keeps and iterates on (the meta-skill `skill-creator` and the thirteen SDLC expert skills already live there).
- **Document assumptions and unresolved questions** in the produced skill's `skill-brief.md`.
- **Do not overbuild.** Avoid speculative complexity, fake evals, or subagents where a checklist would do.
- **No production app code** in this repo. Code-producing skills should emit examples, fixtures, scripts, or patches.
- **Leave a record.** When a command or skill produces a durable artifact — a plan, a **decision from any SDLC role** (not just the architect's ADRs: PO prioritization calls, QA test-strategy gates, DevOps deploy choices, security risk acceptances all count), a test strategy, a rollout plan, or a shipped change — record it in the [memory ledger](.claude/skills/memory/) before ending the turn (one rich entry per artifact), unless the user opted out. Decisions and plans go through `log`; on-disk changes through `snapshot` (so they can be rolled back). New entries are `pending` — a proposal awaiting the user's call, **not** approval to act; get an explicit accept before executing the work a pending decision authorizes. Entry status is drawn from one **closed set** — `pending`, `accepted`, `rejected`, `superseded`, `rolled-back` — and never invented. Never hand-edit `.praxis/memory/ledger.jsonl`; always use the CLI.

## Repo layout (high-level)

```
praxis/
├─ AGENTS.md, CLAUDE.md, README.md, SKILLS.md
├─ .claude-plugin/     # marketplace.json (lists the praxis + skill-factory plugins)
├─ plugin-praxis/      # plugin shell: symlinks to the 11 experts + their commands
├─ plugin-skill-factory/ # plugin shell: symlinks to skill-creator + factory + /validate-skills
├─ .claude/            # the real files (source of truth; used when this repo is the workspace)
│  ├─ skills/          # factory-owned Claude Code skills (discovered automatically)
│  │  ├─ skill-creator/   # the meta-skill — the pattern for creating new skills
│  │  ├─ skill-learner/    # the learning loop — turns discovered gaps into skills
│  │  ├─ business-analyst/   product-owner/   software-architect/
│  │  ├─ developer/          qa-engineer/     devops-engineer/
│  │  ├─ security-engineer/  cybersecurity-architect/
│  │  ├─ ux-ui-engineer/     frontend-architect/   frontend-engineer/
│  │  ├─ data-engineer/      ml-ai-engineer/
│  │  └─ memory/          # utility skill — the versioned memory ledger
│  ├─ commands/        # slash commands (/architect, /new-feature, …)
│  └─ factory/         # all skill-authoring tooling + doctrine
│     ├─ ai/           # global doctrine (operating model, tiering, routing, principles)
│     ├─ templates/    # tier 1-5 scaffolds + eval template
│     ├─ schemas/      # JSON Schema for skill + eval shapes
│     ├─ scripts/      # repo-level tooling (catalog generator)
│     └─ validators/   # deterministic Python validators
├─ integrations/       # opt-in, copy-in wiring for consuming repos
│  ├─ github-actions/, hooks/   # CI + local-hook templates for /review-changes
│  ├─ cursor/, codex/, intellij/  # the experts re-expressed for other agents (generated)
│  └─ scripts/         # build_integrations.py — regenerates the three above from .claude/
└─ dist/               # scratch space for one-off produced output (gitignored)
```

The `cursor/`, `codex/`, and `intellij/` integrations are **generated** — never edit them by hand. After changing any skill or command, run `make integrations` (CI enforces freshness via `make integrations-check`).

## Distribution

Skills are **Claude Code native**. Any skill under `.claude/skills/<name>/` is discovered automatically when this repo is open as the workspace — no install step.

To load everything into a **different** project, the repo is a Claude Code **plugin marketplace** ([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)) with two plugins. From inside the target project:

```text
/plugin marketplace add marcrabadan/praxis
/plugin install praxis@praxis          # the twelve SDLC experts + /new-feature
/plugin install skill-factory@praxis   # optional: author your own skills
```

Each plugin lives in a thin shell dir (`plugin-praxis/`, `plugin-skill-factory/`) made of **symlinks** into `.claude/`; the plugin cache dereferences them at install time, so the real files stay in one place. `praxis` is fully self-contained; `skill-factory` carries the `factory/` tooling via a symlink. Plugin commands are namespaced (`/praxis:<command>`, `/skill-factory:<command>`).

For a single skill without the plugin, copy its folder into the target's `.claude/skills/` (or `~/.claude/skills/` for user scope), or run `make export SKILL=<name> TO=<dir>`. The factory itself (`.claude/factory/ai/`, `templates/`, `validators/`) is needed only when authoring skills with `praxis` open as the workspace.

## Open questions / next work

- Whether `dist/` is still useful, or whether produced output should always be promoted to `.claude/skills/` immediately. Tentative answer: keep `dist/` as scratch, but soft-discourage it in the create flow.
- Whether any SDLC expert skill should grow into a Tier 3+ skill (workflows/scripts) once a repeatable multi-step procedure emerges — promote on evidence per [.claude/factory/ai/promotion-policy.md](.claude/factory/ai/promotion-policy.md).

## When you finish

Return a summary that includes:

- what was created or changed (file paths);
- what assumptions you made;
- which validators were run and what they returned;
- what remains unverified and what the next pass should improve.
