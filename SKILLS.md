# Skill catalog

Generated index of every skill and command in this repo. Do not edit by hand — run `make catalog` (or `python .claude/factory/scripts/build_catalog.py`).

## Skills

| Skill | Version | Tier | Description |
| ----- | ------- | ---- | ----------- |
| `business-analyst` | 1.0.0 | 2 | Acts as a Business Analyst SDLC expert: elicits and structures requirements, writes INVEST user stories with Gherkin acceptance criteria, models processes, ana… |
| `cybersecurity-architect` | 1.0.0 | 2 | Adopts the Cybersecurity Architect persona for system-level security architecture: zero trust, defense in depth, IAM/SSO/identity design, network segmentation,… |
| `data-engineer` | 1.0.0 | 2 | Acts as a Data Engineer SDLC expert: batch/streaming pipelines (ETL/ELT, CDC, Kafka/Spark/Flink), dimensional and lakehouse modeling (star schemas, Data Vault,… |
| `developer` | 1.0.0 | 2 | Acts as a Software Developer SDLC expert: clean code, SOLID/DRY/YAGNI, TDD and the test pyramid, commit/branch/PR hygiene, safe refactoring, error handling, in… |
| `devops-engineer` | 1.1.0 | 2 | Acts as a DevOps Engineer SDLC expert: CI/CD pipelines, infrastructure as code (Terraform), containers and Kubernetes, deployment strategies (blue/green, canar… |
| `diagram` | 1.0.0 | 3 | Generate versioned, text-based diagrams (Mermaid by default, PlantUML on request) — C4 architecture maps, sequence diagrams, ER diagrams, flow charts — from ar… |
| `docs` | 1.0.0 | 3 | Generate functional and technical manuals by routing each section to the right SDLC expert — BA, Product Owner, and UX for the functional manual; Architect, De… |
| `frontend-architect` | 1.0.0 | 2 | Adopts the Frontend Architect persona for system-level frontend decisions: framework/meta-framework selection, rendering strategy (CSR/SSR/SSG/ISR, RSC, island… |
| `frontend-engineer` | 1.0.0 | 2 | Acts as a Frontend Engineer SDLC expert: component implementation and composition, hooks, state management (useState/Context, Redux Toolkit/Zustand, React Quer… |
| `memory` | 1.0.0 | 4 | Persist and manage the project's working memory — a versioned ledger of plans, decisions, implementations, and artifacts from the praxis experts and commands,… |
| `ml-ai-engineer` | 1.0.0 | 2 | Acts as an ML/AI Engineer SDLC expert across the model lifecycle: problem framing and metric selection, ML-ready features (leakage, train/serve skew, feature s… |
| `product-owner` | 1.0.0 | 2 | Acts as a Product Owner SDLC expert: owns and orders the backlog, writes and refines items and epics, prioritizes (MoSCoW, RICE, WSJF, Kano), defines sprint go… |
| `qa-engineer` | 1.0.0 | 2 | Acts as a QA Engineer / Tester SDLC expert: test strategies, test-case design (equivalence partitioning, boundary values, decision tables, state transition, pa… |
| `security-engineer` | 1.0.0 | 2 | Acts as a Security Engineer / AppSec SDLC expert: STRIDE threat modeling, secure coding (OWASP Top 10, ASVS), SAST/DAST/SCA and dependency scanning, secrets ma… |
| `skill-creator` | 1.0.0 | 5 | Create new Claude Code skills, improve or review existing SKILL.md files, validate skill structure, classify a skill into the right tier, and run guided interv… |
| `skill-learner` | 1.0.0 | 3 | Turns a knowledge gap a praxis expert hits mid-task — a missing team convention, runbook, or domain rule — into durable skill knowledge via the skill-creator,… |
| `software-architect` | 1.0.0 | 2 | Adopts the Software Architect persona for system design: architectural trade-offs, NFRs (scalability, availability, latency, security, cost), ADRs, pattern and… |
| `ux-ui-engineer` | 1.0.0 | 2 | Acts as a UX/UI Engineer SDLC expert bridging design and code: design systems and component libraries, design tokens and theming, visual design (type scale, co… |
| `validation-orchestrator` | 1.0.0 | 2 | The standing validation authority for harness-mode workflows: decides whether a workflow may advance past a gate, runs the gate criteria, the typed verify cata… |

## Commands

| Command | Description |
| ------- | ----------- |
| `/analyst` | Consult the Business Analyst — eliciting and clarifying requirements, writing user stories with acceptance criteria, process modeling, stakeholder analysis, sc… |
| `/architect` | Consult the Software Architect — system design, architectural trade-offs, NFRs, ADRs, scaling, concurrency/race conditions, pattern or technology selection, an… |
| `/data` | Consult the Data Engineer — data pipelines (ETL/ELT, batch & streaming, CDC), warehouse/lake/lakehouse modeling, dimensional/star schemas, dbt and orchestratio… |
| `/developer` | Consult the Developer — diagnosing a bug, implementing or refactoring code, test design, error handling, security basics, commit/PR hygiene, and code review. |
| `/devops` | Consult the DevOps Engineer — CI/CD pipelines, infrastructure as code, containers/Kubernetes, deployment strategies, rollbacks, observability/SLOs, incident re… |
| `/diagram` | Generate a Mermaid diagram from the memory ledger and the codebase. Just describe what you want to see — the system, a flow, the data model, a pipeline — and t… |
| `/docs` | Generate documentation — a functional manual (for users/stakeholders) and/or a technical manual (for engineers). Just describe what you need, or type /docs wit… |
| `/fix-bug` | Run a bug through the corrective lifecycle — triage → reproduce → diagnose → fix → verify — consulting QA and the Developer (and Security if it's a vulnerabili… |
| `/frontend-architect` | Consult the Frontend Architect — framework/meta-framework choice, rendering strategy (CSR/SSR/SSG/ISR/RSC), state and data architecture, routing and code-split… |
| `/frontend` | Consult the Frontend Engineer — building and composing components, client/server state, data fetching, forms, styling, frontend TypeScript, re-render/performan… |
| `/idea` | Triage a raw idea — clarify it, classify it as a feature, bug, or refinement (or not worth doing), record it as a pending ledger note, and recommend the next l… |
| `/learn` | Turn a knowledge gap discovered during work into durable skill knowledge — capture an org convention, runbook, or rule, or refine an existing skill, via the sk… |
| `/memory` | Manage the project's working-memory ledger — record plans/decisions/implementations, review what's pending, accept or reject entries, and roll back a snapshott… |
| `/ml` | Consult the ML/AI Engineer — problem framing and metrics, ML-ready features (leakage, train/serve skew), training and evaluation, experiment tracking, serving… |
| `/new-feature` | Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer,… |
| `/patterns` | Mine the memory ledger and stop-condition run logs for recurring patterns — repeated tags, sources, stop conditions, complexity hotspots — and surface them as… |
| `/product` | Consult the Product Owner — backlog ordering, prioritization (MoSCoW/RICE/WSJF), sprint goals, Definition of Ready/Done, roadmapping, OKRs, story splitting, an… |
| `/qa` | Consult the QA Engineer — test strategy, test-case design, edge cases, bug reports, regression and risk-based testing, coverage gaps, and release-quality asses… |
| `/refine` | Run a quality-only improvement through the refinement lifecycle — assess → plan → change → verify — preserving observable behavior. Use to refactor, pay down t… |
| `/review-changes` | Review the current changes (diff) by routing to the right SDLC experts and returning didactic, severity-tagged findings. Use to catch bad practices before a PR… |
| `/security-architect` | Consult the Cybersecurity Architect — security architecture, zero trust, defense in depth, IAM/SSO design, segmentation, data protection, encryption/key strate… |
| `/security` | Consult the Security Engineer — threat modeling, finding/fixing vulnerabilities, secure coding (OWASP Top 10), authn/authz hardening, secrets, crypto usage, SA… |
| `/ux` | Consult the UX/UI Engineer — design systems and tokens, visual design (type/color/spacing/grid), interaction and motion, accessibility (WCAG 2.2 AA), responsiv… |
| `/validate-skills` | Validate every skill in the repo — runs the deterministic validator across .claude/skills/ and dist/. Use to check skill structure and frontmatter before commi… |
| `/validation-orchestrator` | Consult the Validation Orchestrator — the standing authority that decides whether a harness workflow may advance past a gate, runs the gate's criteria and the… |

