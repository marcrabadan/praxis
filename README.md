# praxis

**A shared library of Claude Code skills.** A repo where a team captures *how it does things* — processes, conventions, roles, taste — once, in a format Claude Code reads and applies consistently across every project.

It has three parts:

1. **`skill-creator`** — the meta-skill that *is the pattern for creating new skills*. Use it to scaffold, review, classify, and validate any new skill.
2. **Thirteen SDLC expert skills** — one per role in the software delivery lifecycle (Business Analyst, Product Owner, Software Architect, Developer, QA Engineer, DevOps Engineer, Security Engineer, Cybersecurity Architect, UX/UI Engineer, Frontend Architect, Frontend Engineer, Data Engineer, ML/AI Engineer), each built with that pattern.
3. **`memory`** — a versioned *memory ledger* that records the plans, decisions, implementations, and artifacts the experts produce, each with a `pending → accepted | rejected | rolled-back` lifecycle, so the record survives across sessions and changes can be rolled back.

**Just want to use it?** Jump to [Install & integrate](#install--integrate) for Claude Code, Cursor, IntelliJ, and Codex. **Want to see the output first?** Browse [`examples/`](examples/README.md) for sample transcripts. Otherwise: **PMs, designers, stakeholders** read from the top; **developers writing or shipping a skill** skip to the [Developer guide](#developer-guide).

---

## What is this repo?

`praxis` is a **factory for Claude Code skills**. A "skill" is a small package of instructions that teaches Claude Code how to do one specific thing your team's way — act as a particular SDLC expert, follow a review checklist, write requirements, design an architecture, and so on.

Every time someone teaches Claude a useful pattern, that knowledge is captured **once** here and becomes available to everyone. It is **not** a product repo — it holds the instructions Claude uses *when working on* product repos, not the products themselves.

## Install & integrate

Pick the path that matches how you work. The experts are **Claude Code native**; the same personas are also generated for **Cursor**, **IntelliJ**, and **OpenAI Codex** so you can use them from those tools too.

**Prerequisites:** [Claude Code](https://docs.claude.com/en/docs/claude-code) for the primary path. Python 3 is only needed if you want to *author* skills with the factory tooling (the validators use the standard library — no extra packages to install).

### Claude Code — install into another project (plugin marketplace)

To pull the experts into a *different* repo, `praxis` ships as a Claude Code **plugin marketplace** with two plugins. Run this from inside the target project:

```text
/plugin marketplace add marcrabadan/praxis
/plugin install praxis@praxis          # the twelve SDLC experts + /new-feature + /review-changes
/plugin install skill-factory@praxis   # optional: author your own skills (skill-creator + /validate-skills)
```

As plugins, commands are namespaced under the plugin name — `/praxis:architect`, `/praxis:new-feature`, `/skill-factory:validate-skills`, and so on.

Want just **one** skill, with no plugin? Copy the folder, or use the export target from inside this repo:

```bash
make export SKILL=software-architect TO=../my-product-repo   # → ../my-product-repo/.claude/skills/software-architect
# or by hand, including for user-wide scope:
cp -R .claude/skills/software-architect ~/.claude/skills/
```

### Cursor

The twelve experts ship as Cursor **project rules** (auto-attaching) plus **commands**. Copy the generated `.cursor/` directory into your project root:

```bash
cp -R integrations/cursor/.cursor <your-repo>/
cp AGENTS.md <your-repo>/        # optional: Cursor reads AGENTS.md natively
```

Personas auto-attach when your request matches them; invoke one explicitly with `/architect`, `/developer`, `/security`, `/frontend`, … or run `/new-feature` and `/review-changes`. Details: [`integrations/cursor/`](integrations/cursor/README.md).

### IntelliJ (JetBrains AI Assistant & Junie)

Ships as Junie guidelines + persona guides + ready-to-paste prompts. Copy the generated `.junie/` directory into your project root:

```bash
cp -R integrations/intellij/.junie <your-repo>/
cp AGENTS.md <your-repo>/        # JetBrains AI Assistant reads AGENTS.md natively
```

Then ask Junie or the AI Assistant to *act as the praxis Software Architect* (or any role). IntelliJ has no repo-level slash commands, so the snippets in [`integrations/intellij/prompts/`](integrations/intellij/prompts/) are one-per-persona prompts you can save to the AI Assistant prompt library. Details: [`integrations/intellij/`](integrations/intellij/README.md).

### OpenAI Codex

```bash
# 1. Codex reads AGENTS.md natively — append the roster (or copy praxis's AGENTS.md):
cat integrations/codex/AGENTS.praxis.md >> <your-repo>/AGENTS.md
# 2. ship the persona guides with your code:
cp -R integrations/codex/.praxis <your-repo>/
# 3. install the slash commands:
cp integrations/codex/prompts/*.md ~/.codex/prompts/
```

Then type `/praxis-architect`, `/praxis-security`, `/praxis-new-feature`, … Details: [`integrations/codex/`](integrations/codex/README.md).

> The `cursor/`, `intellij/`, and `codex/` files are **generated** from the canonical Claude Code skills (`make integrations`) so they never drift — don't edit them by hand. See [`integrations/`](integrations/README.md) for the full wiring, including automatic PR review (CI) and a local pre-push nudge.

## What is a "skill"?

A skill is a **folder** under `.claude/skills/<name>/` containing a `SKILL.md` that Claude Code reads when it decides the skill is relevant. Claude decides in one of two ways:

- **You type a slash command** — e.g. `/software-architect`. This explicitly loads the skill.
- **You describe what you want** — e.g. "review this architecture and write an ADR". Claude matches your request against the skill's `description` and loads it on its own.

Once loaded, Claude follows the skill's instructions — which may include reading reference files, walking workflows step by step, or running scripts.

## What's inside a skill?

| File or folder   | What it is                                                                                             | Who reads it                |
| ---------------- | ------------------------------------------------------------------------------------------------------ | --------------------------- |
| `SKILL.md`       | **The entry point.** Frontmatter (`name`, `description`) + a short page telling Claude what the skill does, when to use it, and which reference/workflow to consult. | Claude, automatically.      |
| `references/`    | **Knowledge files.** Rules, examples, checklists — looked up when relevant. One topic per file.        | Claude, when relevant.      |
| `workflows/`     | **Step-by-step procedures** for multi-step skills.                                                     | Claude, in order.           |
| `scripts/`       | **Deterministic Python helpers** for things best not left to a guess.                                  | Claude, by running them.    |
| `evals/`         | **Test cases** — trigger cases (`should_trigger`) and expected-output expectations.                    | Validators / a future runner. |
| `skill-brief.md` | **Internal design doc** — purpose, decisions, iteration log. Stays in the factory.                     | Maintainers.                |

A small skill is just `SKILL.md`. A complex one has all of the above. How much structure a skill needs is set by its **tier**.

> **On evals today:** CI validates the *shape* of eval files (valid JSON, at least one positive and one negative trigger case). It does **not yet execute** them against a model — running trigger/output evals automatically is on the [roadmap](#roadmap). So evals currently document intended behavior; they don't prove it.

## Tiers — how complex is the skill?

| Tier | What it's for | Folders |
| ---- | ------------- | ------- |
| **1 — Basic** | A single rule or short guidance. | `SKILL.md` |
| **2 — Knowledge** | Reusable domain knowledge that would clutter `SKILL.md`. | `+ references/` |
| **3 — Workflow** | A multi-step procedure or multiple modes. | `+ workflows/` |
| **4 — Implementation** | Generates, modifies, or validates code/structured output. | `+ scripts/ + evals/` |
| **5 — Core** | Central, frequent, or high-risk skill needing extra harness. | `+ agents/ + reports/` |

The point of tiering is to **not overbuild**. Full criteria: [.claude/factory/ai/skill-tiering.md](.claude/factory/ai/skill-tiering.md).

## Talking to an expert

Each SDLC expert has a short slash command so you can address it directly with a question, instead of describing the role each time:

| Command | Expert | Example |
| ------- | ------ | ------- |
| `/architect` | Software Architect | `/architect how do I avoid this race condition under load?` |
| `/developer` | Developer | `/developer why does this function intermittently return null?` |
| `/qa` | QA Engineer | `/qa what edge cases am I missing for this checkout flow?` |
| `/analyst` | Business Analyst | `/analyst turn this idea into user stories with acceptance criteria` |
| `/product` | Product Owner | `/product how should I prioritize these five backlog items?` |
| `/devops` | DevOps Engineer | `/devops is this service ready to ship to production?` |
| `/security` | Security Engineer | `/security threat-model this upload endpoint and find the vulns` |
| `/security-architect` | Cybersecurity Architect | `/security-architect design the IAM and segmentation for this platform` |
| `/ux` | UX/UI Engineer | `/ux check the contrast and focus states on this form` |
| `/frontend-architect` | Frontend Architect | `/frontend-architect SSR or SSG for this catalog, and where should state live?` |
| `/frontend` | Frontend Engineer | `/frontend why does this list re-render on every keystroke?` |
| `/data` | Data Engineer | `/data design an idempotent incremental load for this orders pipeline` |
| `/ml` | ML/AI Engineer | `/ml is there leakage in these features, and what metric should I optimize?` |

Each command loads its matching skill and answers in that persona. You can also just describe what you want and Claude will load the right expert on its own. Command definitions live in [.claude/commands/](.claude/commands/).

To run a feature through the **core six experts** in lifecycle order — BA → PO → architect → developer → QA → devops, each building on the last — use `/new-feature <idea or PRD>`. It produces one consolidated plan (requirements, prioritized increments, design decisions, implementation plan, test strategy, rollout). Each phase runs in its own subagent, so an expert's doctrine loads in an isolated context and only its compact artifact returns to the main thread; prior artifacts are carried forward so context still flows across phases. After the architect phase it also **routes in the specialist experts a feature warrants** — ML/AI, data, security, frontend, or UX — as extra parallel phases, so an ML- or security-heavy feature gets its specialist automatically. Those experts also sit alongside the lifecycle for direct use (`/ml`, `/data`, `/security`, …), and `/review-changes` brings them in when a diff warrants it.

### See it in action

Sample transcripts — the prompt you type and a representative response — live in [`examples/`](examples/README.md). Most follow one running feature (saved payment methods at checkout) so you can watch it move through requirements, architecture, build, and review:

| Sample | Shows |
| ------ | ----- |
| [new-feature.md](examples/new-feature.md) | `/new-feature` → the core six's consolidated plan |
| [architect-adr.md](examples/architect-adr.md) | `/architect` → a decision captured as an ADR |
| [analyst-user-stories.md](examples/analyst-user-stories.md) | `/analyst` → INVEST stories + Gherkin acceptance criteria |
| [review-changes.md](examples/review-changes.md) | `/review-changes` → severity-tagged, didactic findings |
| [security-threat-model.md](examples/security-threat-model.md) | `/security` → a STRIDE threat model with mitigations |
| [ml-evaluation.md](examples/ml-evaluation.md) | `/ml` → leakage check, the right metric, and a safe rollout |

## Wiring the experts into your workflow

Consulting an expert is *pull* — you have to remember to ask. To **catch bad practices at the moment they happen**, wire the experts into your dev flow so they show up on their own:

- **`/review-changes`** reviews the current diff, routes to only the relevant experts (developer / qa / architect / devops / security / security-architect), and returns **severity-tagged, didactic** findings — each says *what* the bad practice is, *why* it matters, and *how* to fix it. A junior learns from it; a senior skims by severity; an architect sees the team's standards enforced.
- Make it **automatic**: a GitHub Action runs it on every PR, and a local hook nudges you before you push. Both are opt-in templates in [`integrations/`](integrations/README.md).
- **Remember what you decided and built.** The `memory` ledger (`/memory`) records plans, decisions, and changes as durable, git-committed entries you can accept, reject, or roll back. An opt-in hook surfaces what's still pending at session start and snapshots changes when you stop — see [The memory ledger](#memory-tier-4--the-working-memory-ledger).
- **Use the same experts in other agents.** The personas and workflows are also generated for **Cursor**, **IntelliJ** (JetBrains AI Assistant & Junie), and **OpenAI Codex**, each in that tool's native format — see [`integrations/`](integrations/README.md#4-other-agents-cursor-intellij-openai-codex). All three read `AGENTS.md` natively for repo-wide doctrine.

## The skills in this factory today

### `skill-creator` (Tier 5 — the meta-skill / the pattern)

The pattern for creating new skills. You describe what you want; it runs a guided interview (one question at a time), picks the right tier, scaffolds the folder deterministically, and validates the result. Two capabilities worth calling out:

- **General-purpose interview** — the one-question-at-a-time workflow works for scoping *any* objective, not only skills.
- **Iteration capture (a learning loop)** — when you correct its output ("actually, always do X"), it asks whether to record that as a durable rule for the skill or a meta-rule for the factory (`learned-rules.md`), so the same correction is never needed twice.

### The twelve SDLC expert skills (Tier 2)

Each makes Claude act as that role's expert, with practices and a review checklist:

| Skill | Role | Covers |
| ----- | ---- | ------ |
| `business-analyst` | Business Analyst | Requirements elicitation, user stories (INVEST + Gherkin), process modeling, traceability, MoSCoW. |
| `product-owner` | Product Owner | Backlog ordering, prioritization (RICE/WSJF/Kano), Definition of Ready/Done, OKRs, story splitting. |
| `software-architect` | Software Architect | NFRs, ADRs, trade-offs, C4 model, pattern selection, risk, avoiding over-engineering. |
| `developer` | Developer | Clean code, TDD/test pyramid, commit & PR hygiene, safe refactoring, security basics, review etiquette. |
| `qa-engineer` | QA Engineer | Test strategy, test-design techniques, bug reports, risk-based & regression testing, release readiness. |
| `devops-engineer` | DevOps Engineer | CI/CD, IaC, containers/K8s, deployment strategies, observability/SLOs, incident response, DORA. |
| `security-engineer` | Security Engineer | Threat modeling (STRIDE), OWASP Top 10, authn/authz, secrets, crypto, SAST/DAST/SCA, supply chain, CVSS triage. |
| `cybersecurity-architect` | Cybersecurity Architect | Zero trust, defense in depth, IAM/identity, segmentation, data protection, key management, NIST/ISO/CIS, compliance, risk. |
| `ux-ui-engineer` | UX/UI Engineer | Design systems & tokens, visual & interaction design, accessibility (WCAG 2.2 AA), responsive layout, usability heuristics, UX writing, design handoff. |
| `frontend-architect` | Frontend Architect | Framework & rendering strategy (SSR/SSG/ISR/RSC), state/data/routing architecture, build & bundling, micro-frontends, design-system architecture, Core Web Vitals. |
| `frontend-engineer` | Frontend Engineer | Component implementation, state & data wiring, forms, styling, frontend TypeScript, re-render/performance, accessibility implementation, component/E2E testing. |
| `data-engineer` | Data Engineer | Batch & streaming pipelines (ETL/ELT, CDC), warehouse/lake/lakehouse & dimensional modeling, orchestration (dbt/Airflow/Dagster), data quality & contracts, lineage & governance, partitioning, DataOps & cost. |
| `ml-ai-engineer` | ML/AI Engineer | Problem framing & metrics, ML-ready features (leakage, train/serve skew, feature stores), training & evaluation, experiment tracking, serving & deployment (shadow/canary/A-B), MLOps, drift monitoring & retraining, responsible AI, LLM/GenAI (RAG, prompting, fine-tuning, evals, guardrails). |

### `memory` (Tier 4 — the working-memory ledger)

The experts produce plans, decisions, and code — `memory` makes that output **stick**. It's a versioned ledger, committed to git under `.praxis/memory/`, so the record survives across sessions, machines, and the next person to open the repo.

- **What it stores:** `plan`, `decision` (mini-ADRs), `implementation`, `artifact`, `test-strategy`, `rollout`, and `note` entries — each with provenance (which command/skill produced it) and a lifecycle: **`pending → accepted | rejected | rolled-back`** (plus `superseded`).
- **Seed it once with `/memory init`:** the bootstrap flow primes an empty ledger from the repo's existing context — `AGENTS.md`, ADRs, architecture docs, and git history — so memory reflects the project from day one instead of only what happens after adoption. (Claude Code has no on-install hook; this is the explicit one-time seed, and the SessionStart hook nudges you to run it whenever the ledger is empty.)
- **Rollback:** implementation entries are captured as a `snapshot` that stores a reverse-appliable patch, so a change can be undone — with a safe dry-run — even sessions later.
- **Drive it with `/memory`:** `init`, `list`, `pending`, `show <id>`, `accept <id>`, `reject <id>`, `rollback <id>`, `status`. Everything goes through a deterministic, stdlib-only CLI (`.claude/skills/memory/scripts/ledger.py`) — never hand-edit the ledger.
- **Make it automatic:** an opt-in hook ([`integrations/hooks/memory.settings.example.json`](integrations/hooks/memory.settings.example.json)) ensures the ledger exists, nudges you to seed it when empty, surfaces pending entries at **SessionStart**, and snapshots uncommitted changes on **Stop**. Paired with the *“leave a record”* rule in [`AGENTS.md`](AGENTS.md), the hook captures *what* changed while the experts record *why*. `/new-feature` and `/review-changes` already log their artifacts.

```text
/memory init                 # seed the ledger from the repo's existing context
/memory                      # status + what's still pending
/memory accept 20260601-153012-9af3
/memory rollback 20260601-153012-9af3   # dry-run first, reverts the working tree
```

---

## Developer guide

### Quick start

1. Read [AGENTS.md](AGENTS.md) — the single source of truth for agent behavior in this repo.
2. To create a new skill, invoke the meta-skill: type `/skill-creator` (or just "I want a skill for X"). It loads [.claude/skills/skill-creator/SKILL.md](.claude/skills/skill-creator/SKILL.md).
3. The skill-creator runs the interview, classifies the tier, scaffolds via `create_skill.py`, and validates.
4. Promote finished skills from `dist/<name>/` to `.claude/skills/<name>/` when they become shared assets — Claude Code then discovers them automatically.

### Using these skills in another project

See [Install & integrate](#install--integrate) above for the plugin, single-skill copy, and Cursor / IntelliJ / Codex paths. A few notes for maintainers:

- **`praxis`** — the on-demand SDLC team: the twelve expert skills, their per-expert commands, and the `/new-feature` orchestrator. Fully self-contained, so it works anywhere.
- **`skill-factory`** — the `skill-creator` meta-skill, `/validate-skills`, and the factory tooling, for teams that want to author their own skills. (One doctrine file links back to this repo's `AGENTS.md`, which only resolves with `praxis` open as a workspace — harmless when installed elsewhere.)
- Every skill carries a `version` (semver) in its frontmatter, so a consuming repo can tell when its copy is behind. Keep authoring and iteration inside `praxis`, since the factory depends on `.claude/factory/ai/`, `.claude/factory/templates/`, and `.claude/factory/validators/`.

### The catalog

`SKILLS.md` is a generated index of every skill (name, version, tier, description) and command. Regenerate it with `make catalog`; CI fails if it is stale, so it always reflects what is actually in the repo.

### Shortcuts

| Tool | How to invoke |
| ---- | ------------- |
| `make` | `make help` |
| VS Code Tasks | Cmd/Ctrl+Shift+P → "Run Task" → pick a `skills: ...` task ([.vscode/tasks.json](.vscode/tasks.json)) |
| Raw Python | see below |

### Run the validator directly

```bash
python .claude/factory/validators/validate_skill.py .claude/skills/skill-creator
make validate-all          # validate every skill in .claude/skills/ and dist/
```

Or, inside Claude Code, run `/validate-skills` — it wraps `make validate-all` and reports failures with the exact error lines.

### Run the generator directly (skip the interview)

```bash
python .claude/skills/skill-creator/scripts/create_skill.py \
  --brief dist/my-skill/skill-brief.md \
  --tier 3 \
  --name my-skill \
  --out dist/my-skill
```

### Continuous integration

Pushes and PRs against `main` run [.github/workflows/validate.yml](.github/workflows/validate.yml): it validates every skill in `.claude/skills/` and `dist/`, runs a generator determinism check (and asserts no `command.md` is emitted), verifies `SKILLS.md` is up to date, and sanity-checks the JSON schemas.

### Key concepts

- **Tiers (1–5).** Every skill is classified by complexity before scaffolding. See [.claude/factory/ai/skill-tiering.md](.claude/factory/ai/skill-tiering.md).
- **Interview-first.** When intent is incomplete, an interview captures purpose, triggers, output format, and rules. See [.claude/skills/skill-creator/workflows/interview.md](.claude/skills/skill-creator/workflows/interview.md).
- **Deterministic scaffolding.** `create_skill.py` consumes a `skill-brief.md` + tier and emits the folder. Same input → same output.
- **Validators run before done.** No skill is shipped until [.claude/factory/validators/validate_skill.py](.claude/factory/validators/validate_skill.py) passes.

### Repo layout

```
praxis/
├─ AGENTS.md              # global doctrine (read first)
├─ CLAUDE.md              # pointer to AGENTS.md
├─ README.md              # this file
├─ Makefile               # `make help` for short commands
├─ .vscode/tasks.json     # equivalent tasks for VS Code
├─ .github/workflows/     # CI: validates every skill on push / PR
├─ SKILLS.md              # generated catalog of skills + commands (make catalog)
├─ examples/              # sample transcripts — what each expert/command produces
├─ .claude-plugin/        # marketplace.json (lists the praxis + skill-factory plugins)
├─ plugin-praxis/         # plugin: symlinks to the 11 experts + memory + their commands
├─ plugin-skill-factory/  # plugin: symlinks to skill-creator + factory + /validate-skills
├─ .claude/               # the real source of truth (used when this repo is the workspace)
│  ├─ skills/             # skill-creator (meta) + the twelve SDLC experts + memory
│  ├─ commands/           # /architect, /developer, …, /new-feature, /memory, /validate-skills
│  └─ factory/            # all skill-authoring tooling + doctrine
│     ├─ ai/              # operating model, tiering, routing, principles, promotion policy, glossary
│     ├─ templates/       # tier-1..5 scaffolds + eval template
│     ├─ schemas/         # JSON Schema for skill + eval shapes
│     ├─ scripts/         # repo-level tooling (catalog generator)
│     └─ validators/      # deterministic Python validators
└─ dist/                  # scratch for new skills (gitignored)
```

The `plugin-*/` folders are thin shells of symlinks into `.claude/` — the real files live once under `.claude/`, and the plugin cache dereferences the symlinks at install time.

### Conventions

- Use forward slashes in markdown links and skill paths, not backslashes.
- Skill `name` is lowercase, hyphens only, max 64 chars (regex `^[a-z0-9-]{1,64}$`).
- Skill `description` is trigger-rich, third-person, max 1024 chars, and includes both **what** the skill does and **when** to use it.
- `SKILL.md` body stays under 500 lines. Long knowledge moves to `references/`, multi-step procedures move to `workflows/`.

## Roadmap

What exists today is strong at **creating** skills. The gaps below are what stand between this repo and a product other teams could adopt — listed so contributors know where the edges are. Per [.claude/factory/ai/promotion-policy.md](.claude/factory/ai/promotion-policy.md), build these on evidence of need, not anticipation.

- **Eval runner.** Execute `trigger-evals.json` and `output-evals.json` against a model and report pass/fail, so a skill's behavior is *measured*, not just asserted. Today CI only checks eval shape.
- **Usage telemetry.** Capture which skills trigger, how often, and with what outcome — the evidence the promotion policy already assumes exists.
- **Versioned distribution.** Build on the `version` frontmatter and `make export`/`SKILLS.md` toward a real publish/update flow (changelog, update detection in consuming repos).
- **Multi-environment support.** This library is Claude Code native. Re-introducing exporters for other agent tools would widen the addressable audience.
- **Generalization & governance.** The SDLC skills are generic best practices; differentiation comes from team-specific IP and integrations, plus a contribution/ownership process for shared skills.

## License

Licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for
attribution and [CHANGELOG.md](CHANGELOG.md) for the release history.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). The two
distributable plugins each carry a `version` in their
`.claude-plugin/plugin.json` (mirrored in `.claude-plugin/marketplace.json`),
and the repository as a whole is tagged `vX.Y.Z` at each release. Changes are
recorded in [CHANGELOG.md](CHANGELOG.md).
