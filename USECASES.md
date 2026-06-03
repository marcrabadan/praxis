# Use Cases

Practical scenarios for every command in this repo. Organized by what you are trying to do, not by command name.

---

## Table of Contents

0. [Bring praxis to an existing project](#0-bring-praxis-to-an-existing-project)
1. [Kick off a new feature end-to-end](#1-kick-off-a-new-feature-end-to-end)
2. [Ask a specific expert](#2-ask-a-specific-expert)
3. [Review code before merging](#3-review-code-before-merging)
4. [Generate documentation](#4-generate-documentation)
5. [Generate diagrams](#5-generate-diagrams)
6. [Manage decisions and memory](#6-manage-decisions-and-memory)
7. [Work on data and AI features](#7-work-on-data-and-ai-features)
8. [Work on the frontend](#8-work-on-the-frontend)
9. [Harden security](#9-harden-security)
10. [Maintain skills in this repo](#10-maintain-skills-in-this-repo)
11. [Combined workflows](#11-combined-workflows)

---

## 0. Bring praxis to an existing project

You do not need a greenfield project. Every command reads the codebase and the memory ledger at runtime — it discovers what exists, documents it, reviews it, and builds on it.

### Step 1 — Install the plugin (one command)

From inside your existing project, with Claude Code open:

```
/plugin marketplace add marcrabadan/praxis
/plugin install praxis@praxis
```

That gives you all 19 commands immediately — `/new-feature`, `/review-changes`, `/docs`, `/diagram`, every expert, and `/memory`.

Want the skill-authoring tooling too?

```
/plugin install skill-factory@praxis
```

### Step 2 — Seed the memory ledger from what already exists

The ledger is empty on first install. Bootstrap it from your existing ADRs, README, git history, and architecture docs:

```
/memory init
```

This reads `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `docs/adr/`, and the recent git log, then records the project's already-made decisions as `pending` entries. Review and accept the ones that are still current:

```
/memory list pending
/memory accept <id>
```

Once the ledger is seeded, every subsequent command inherits institutional context — the architect knows your past decisions, the security engineer knows your risk posture, the QA engineer knows your test strategy.

### Step 3 — Document what you already have

Generate documentation from the existing codebase in one command:

```
/docs
```

The experts read your code, your ADRs, and the ledger and produce:
- `docs/functional-manual.md` — what the system does (BA + PO + UX)
- `docs/technical-manual.md` — how it is built and operated (Architect + Developer + DevOps)

Or just the part you need:

```
/docs the API reference for the payments module
/docs the onboarding runbook
/docs our architecture decisions
```

### Step 4 — Diagram what you already have

```
/diagram                              → L2 architecture of the whole system
/diagram the auth flow                → sequence diagram from existing code
/diagram the database schema          → ER diagram from existing models
/diagram our CI/CD pipeline           → flow diagram from the workflow files
```

The diagram skill reads your `docker-compose`, `Dockerfile`, `*.tf`, ORM models, and CI config — it does not need descriptions written in advance.

### Step 5 — Review any existing PR or branch

```
/review-changes
/review-changes main..feature/my-branch
```

Works on any diff, any repo. Routes to the relevant experts based on what changed.

### Step 6 (optional) — Wire it into your team's workflow

#### Automatic PR reviews in CI

Copy the GitHub Actions workflow into your project:

```bash
cp .claude/skills/../integrations/github-actions/praxis-pr-review.yml \
   <your-repo>/.github/workflows/praxis-pr-review.yml
```

Add an `ANTHROPIC_API_KEY` repository secret. Every PR now gets a review posted automatically.

#### Pre-push review nudge (local)

Merge the hooks block from `integrations/hooks/settings.example.json` into your project's `.claude/settings.json`. Claude Code will remind you to run `/review-changes` before committing.

#### Automatic memory capture (local)

Merge the hooks block from `integrations/hooks/memory.settings.example.json` into `.claude/settings.json`. On every session start, pending decisions surface automatically. On every stop, uncommitted changes are snapshotted as a rollback-able entry.

#### Cursor, IntelliJ, or OpenAI Codex

The same expert personas are available for other agents via the generated integrations:

| Agent | What to copy |
|-------|-------------|
| **Cursor** | `integrations/cursor/` → `.cursor/rules/` and `.cursor/commands/` in your project |
| **IntelliJ** (AI Assistant / Junie) | `integrations/intellij/` → `.junie/` in your project |
| **OpenAI Codex** | `integrations/codex/` → `AGENTS.praxis.md` + `.praxis/` |

### Day-one checklist for an existing project

```
/plugin install praxis@praxis          # 1. install
/memory init                           # 2. seed ledger from existing context
/memory list pending                   # 3. review and accept what's current
/docs                                  # 4. generate manuals from existing code
/diagram                               # 5. generate architecture overview
/review-changes main..HEAD             # 6. review any open work
```

After that, every subsequent expert command knows your project's history and contributes to its documentation automatically.

---

## 1. Kick off a new feature end-to-end

Run a feature idea through every SDLC role in lifecycle order. Each expert builds on the previous one's output. Documentation and diagrams are generated inline — no extra step needed.

```
/new-feature add multi-tenant support to the billing module
/new-feature user wants to export their data as CSV
/new-feature replace our polling mechanism with WebSockets
```

**What you get:**
- Requirements and acceptance criteria (BA)
- Prioritized increments and sprint goal (PO)
- Architecture decisions as ADR files (Architect)
- Architecture diagram if the design is non-trivial (Architect)
- Implementation plan (Developer)
- Test strategy document (QA)
- Rollout plan and runbook (DevOps)
- CI/CD flow diagram if the pipeline is non-trivial (DevOps)
- Domain experts added automatically when the feature warrants them — security for auth, ML/AI for models, data for pipelines, UX for interfaces

**Checkpoint:** After the architect phase, the command pauses on complex features so you can confirm direction before continuing.

---

## 2. Ask a specific expert

Quick single-turn consultations. Each expert writes a documentation or diagram file automatically when the answer contains a substantial artifact.

### Business Analyst — requirements, user stories, acceptance criteria

```
/analyst the checkout flow needs to support 3D Secure — what are the requirements?
/analyst write user stories for the password reset feature
/analyst map the as-is onboarding process and find the pain points
```

→ Writes or updates `docs/functional-manual.md` when requirements are substantial.

### Product Owner — prioritization, roadmap, sprint planning

```
/product which of these three features should we build first?
/product split this epic into vertical slices we can ship independently
/product define the Definition of Done for the auth module
```

→ Appends Priorities and Sprint Goal to `docs/functional-manual.md`.

### Software Architect — design, ADRs, trade-offs, NFRs

```
/architect should we use an event-driven or request-response design for order processing?
/architect review the current module boundaries — are there hidden dependencies?
/architect we need to handle 10k concurrent users — what changes?
```

→ Writes `docs/decisions/ADR-NNN-<slug>.md` + architecture diagram when a significant decision is made.

### Developer — implementation, refactoring, code review, bugs

```
/developer how should I structure the repository layer for this feature?
/developer this function is 200 lines — help me refactor it
/developer why is this test flaky and how do I fix it?
```

→ Writes or updates `docs/technical-manual.md` when an implementation plan is produced.

### QA Engineer — test strategy, test cases, coverage gaps

```
/qa write a test strategy for the payments module
/qa what are the highest-risk areas in the auth flow to test first?
/qa this bug report is incomplete — help me write a proper one
```

→ Writes `docs/test-strategy.md` when a full strategy is produced.

### DevOps Engineer — pipelines, infra, deploy, observability

```
/devops design a zero-downtime deployment strategy for the API
/devops what SLOs should we track for the checkout service?
/devops is this service production-ready? run the checklist
```

→ Writes Operations + Runbook sections in `docs/technical-manual.md` + deploy flow diagram.

### UX/UI Engineer — design, accessibility, user journeys, components

```
/ux review the login form for WCAG 2.2 AA compliance
/ux the onboarding flow has too many steps — how do we simplify it?
/ux what spacing and type scale should the new dashboard use?
```

→ Writes or updates the UI Guide section of `docs/functional-manual.md`.

### Security Engineer — vulnerabilities, threat modeling, AppSec

```
/security review this authentication code for vulnerabilities
/security what are the top risks in our file upload feature?
/security this dependency has a CVE — how severe is it and what do we do?
```

→ Appends Security Findings to `docs/technical-manual.md` when a threat model or significant finding is produced.

### Cybersecurity Architect — security design, zero trust, IAM, compliance

```
/security-architect design an IAM strategy for our multi-tenant SaaS
/security-architect we need SOC 2 Type II — what controls are missing?
/security-architect review our network segmentation for zero-trust gaps
```

---

## 3. Review code before merging

Routes the current diff to the relevant experts and returns severity-tagged findings. Always includes the Developer checklist as baseline; adds others based on what changed.

```
/review-changes
/review-changes focus on the auth module
/review-changes HEAD~3..HEAD
```

**Severity tags:**
- 🔴 Blocker — correctness, security, data-loss risk
- 🟠 Should-fix — bad practice or maintainability problem
- 🟡 Nit — style or learning point

**Experts invoked automatically based on the diff:**
- Developer — always, for any code change
- Architect — for module boundaries, new dependencies, cross-cutting changes
- Security — for auth, input handling, crypto, secrets
- QA — for code missing tests or testing logic
- DevOps — for CI/CD, Dockerfiles, infra config
- Frontend — for UI components, hooks, styling
- UX — for design tokens, WCAG, accessibility

---

## 4. Generate documentation

Documentation generated inline during expert work lands in `docs/`. Use `/docs` when you want to generate or regenerate manuals explicitly.

```
/docs                               → generates both manuals (functional + technical)
/docs for the new stakeholder demo  → functional manual
/docs how the system is built       → technical manual
/docs just the API reference        → API reference section only
/docs the runbook for the payments service
```

**Functional manual** (`docs/functional-manual.md`) — written by BA + PO + UX:
- Purpose and target users
- Feature catalogue with acceptance criteria
- User journeys and workflows
- Business rules
- UI guide

**Technical manual** (`docs/technical-manual.md`) — written by Architect + Developer + DevOps (+ Security, Data, ML when applicable):
- Architecture overview and ADRs
- Module/component map
- API reference
- Data model
- Configuration reference
- Local setup
- Deployment, observability, runbook

---

## 5. Generate diagrams

Describe what you want to see — type is inferred automatically.

```
/diagram                                   → L2 architecture overview of the whole system
/diagram how services connect              → architecture diagram
/diagram the login flow                    → sequence diagram
/diagram how payment and order talk to each other → sequence diagram
/diagram the user and order data model     → ER diagram
/diagram our CI/CD pipeline                → flow diagram
/diagram how data flows from ingestion to the warehouse → flow diagram
```

**Types generated automatically:**
- Architecture (C4 L2) — services, datastores, external actors, boundaries
- Sequence — step-by-step interactions, API calls, user journeys
- ER — data entities, fields, relationships
- Flow — pipelines, CI/CD stages, decision trees

All diagrams are Mermaid — they render natively on GitHub, Notion, and most wikis with no setup.

---

## 6. Manage decisions and memory

The memory ledger is a versioned record of plans, decisions, and artifacts. Every command records its significant outputs here automatically.

```
/memory                         → show status and what's pending
/memory list pending            → see everything awaiting a call
/memory accept <id>             → approve a pending decision or plan
/memory reject <id>             → reject it with a note
/memory rollback <id>           → revert a snapshotted implementation
/memory show <id>               → read a full entry
/memory init                    → bootstrap the ledger for a new repo
```

**When a rollback happens:**
The memory command automatically finds all docs and diagrams that were generated from the rolled-back entry (via `source:` tags) and marks them `superseded`. It then tells you exactly which files to regenerate with `/docs` or `/diagram`.

**Statuses:** `pending → accepted | rejected | rolled-back` (plus `superseded`)

A `pending` entry is a proposal — it does not authorize action. Get an explicit `accept` before executing the work it describes.

---

## 7. Work on data and AI features

### Data Engineer — pipelines, modeling, orchestration, quality

```
/data design an idempotent ETL pipeline for Stripe events
/data our dbt model is slow — what's wrong and how do we optimize it?
/data is this dataset ready to expose as a data product?
/data what partitioning strategy should we use for this 1TB table?
```

### ML/AI Engineer — framing, features, training, evals, serving, LLMs

```
/ml frame the churn prediction problem and define the right metric
/ml check this feature set for data leakage
/ml design an evaluation suite for our RAG chatbot
/ml our model is drifting — what monitoring and retraining strategy do we need?
/ml compare RAG vs fine-tuning for this use case
/ml is this model production-ready? run the checklist
```

**`/new-feature` automatically adds these experts** when the feature involves data pipelines or ML/AI — no flag needed.

---

## 8. Work on the frontend

### Frontend Architect — framework, rendering, state, build, design system

```
/frontend-architect should we use Next.js SSR or a SPA for this product?
/frontend-architect our bundle is 2MB — what's the splitting strategy?
/frontend-architect design the state architecture for the dashboard
/frontend-architect how should we structure the design system tokens?
```

### Frontend Engineer — components, hooks, state, styling, a11y

```
/frontend this component re-renders on every keystroke — why?
/frontend implement an accessible modal with focus trap
/frontend the form validation logic is duplicated everywhere — refactor it
/frontend write an E2E test for the checkout flow
```

---

## 9. Harden security

### For application-level vulnerabilities (OWASP, AppSec, CVEs)

```
/security review the file upload handler
/security is this JWT implementation correct?
/security triage CVE-2024-XXXX for our dependency
```

### For architectural security (IAM, zero trust, compliance)

```
/security-architect design the auth and SSO topology for multi-tenant
/security-architect map our controls to NIST CSF and find the gaps
/security-architect what encryption and key-management strategy do we need?
```

**`/review-changes` always runs the security checklist** on diffs that touch auth, input handling, crypto, or secrets — automatically, no flag needed.

---

## 10. Maintain skills in this repo

### Validate all skills

```
/validate-skills
```

Runs the deterministic validator across every skill under `.claude/skills/` and `dist/`. Reports failing skills with exact error lines.

### Create, improve, or evaluate a skill

Use the `skill-creator` meta-skill (the pattern for creating new skills):

```
/new-feature I need a skill that does X    ← for simple, well-scoped skills
```

Or invoke `skill-creator` directly for full interview-driven skill authoring.

---

## 11. Combined workflows

### Design → document → diagram in one shot

```
/new-feature add OAuth2 login with Google
```
→ BA writes requirements → PO slices increments → Architect writes ADR + architecture diagram → Security adds threat model → Developer writes implementation notes → QA writes test strategy → DevOps writes runbook + deploy diagram. All files land in `docs/` automatically.

### After merging: refresh docs

```
/docs                   → regenerates manuals from updated ledger + code
/diagram                → regenerates architecture diagram
```

### After a rollback: see what's stale and regenerate

```
/memory rollback <id>   → reverts code, marks dependent docs/diagrams superseded, lists what to regenerate
/docs                   → regenerates from the current state
/diagram                → regenerates diagrams
```

### Before a release: full review + docs

```
/review-changes         → catch issues in the diff
/docs                   → ensure manuals are up to date
/diagram                → ensure architecture diagram reflects current state
/memory list pending    → check nothing is waiting for a decision
```

### On-call: find the runbook

```
/memory list --type artifact --tag docs   → find all generated docs
/memory show <id>                         → read the runbook entry
```

---

## Quick reference

| Command | One-line purpose |
|---------|-----------------|
| `/new-feature` | Full SDLC from idea to rollout plan, docs and diagrams inline |
| `/analyst` | Requirements, user stories, acceptance criteria |
| `/product` | Backlog prioritization, sprint goals, roadmap |
| `/architect` | Design decisions, ADRs, trade-offs, scaling |
| `/developer` | Implementation, refactoring, bugs, code review |
| `/qa` | Test strategy, test cases, coverage, defect reports |
| `/devops` | CI/CD, infra, deploy strategy, observability, runbooks |
| `/ux` | Design, accessibility, user journeys, component specs |
| `/security` | Vulnerabilities, threat modeling, CVE triage, AppSec |
| `/security-architect` | IAM, zero trust, segmentation, compliance, risk |
| `/frontend` | Components, hooks, state, styling, a11y implementation |
| `/frontend-architect` | Framework, rendering, build, design-system architecture |
| `/data` | Pipelines, modeling, orchestration, data quality |
| `/ml` | Model lifecycle, LLMs, RAG, evals, drift, responsible AI |
| `/review-changes` | Diff review routed to the relevant experts |
| `/docs` | Generate functional and/or technical manuals |
| `/diagram` | Generate Mermaid diagram from a natural language description |
| `/memory` | Record, review, accept/reject, and roll back decisions |
| `/validate-skills` | Validate skill structure across the repo |
