# Skill catalog

Generated index of every skill and command in this repo. Do not edit by hand — run `make catalog` (or `python .claude/factory/scripts/build_catalog.py`).

## Skills

| Skill | Version | Tier | Description |
| ----- | ------- | ---- | ----------- |
| `business-analyst` | 1.0.0 | 2 | Acts as a Business Analyst SDLC expert to elicit, structure, and validate requirements. Writes user stories with INVEST criteria and Gherkin acceptance criteri… |
| `cybersecurity-architect` | 1.0.0 | 2 | Adopts the Cybersecurity Architect persona to design and review security architecture at the system and organization level — zero-trust and defense-in-depth de… |
| `data-engineer` | 1.0.0 | 2 | Acts as a Data Engineer SDLC expert covering the full data platform — batch and streaming pipelines (ETL/ELT, CDC, Kafka/Flink/Spark), data modeling (dimension… |
| `developer` | 1.0.0 | 2 | Acts as a Software Developer / Engineer SDLC expert covering clean code, SOLID/DRY/YAGNI principles, TDD and the test pyramid, commit discipline, branch and PR… |
| `devops-engineer` | 1.0.0 | 2 | Acts as a DevOps Engineer SDLC expert: designs CI/CD pipelines, writes infrastructure as code, advises on containerization and Kubernetes, selects deployment s… |
| `diagram` | 1.0.0 | 3 | Generate versioned, text-based diagrams (Mermaid by default, PlantUML on request) from architecture decisions, memory ledger entries, system design, data model… |
| `docs` | 1.0.0 | 3 | Generate functional and technical manuals by routing each section to the right SDLC expert. The functional manual is written by the Business Analyst, Product O… |
| `frontend-architect` | 1.0.0 | 2 | Adopts the Frontend Architect persona to make system-level frontend design decisions — framework and meta-framework selection (React/Vue/Svelte/Angular, Next/N… |
| `frontend-engineer` | 1.0.0 | 2 | Acts as a Frontend Engineer SDLC expert covering component implementation and composition (presentational/container, compound components, custom hooks), state-… |
| `memory` | 1.0.0 | 4 | Persist and manage the project's working memory — a versioned ledger of plans, decisions, implementations, and artifacts produced across the praxis SDLC expert… |
| `ml-ai-engineer` | 1.0.0 | 2 | Acts as an ML/AI Engineer SDLC expert covering the full model lifecycle — problem framing and metric selection, ML-ready features (feature stores, leakage, tra… |
| `product-owner` | 1.0.0 | 2 | Acts as a Product Owner SDLC expert: owns and orders the product backlog, writes and refines backlog items and epics, applies prioritization frameworks (MoSCoW… |
| `qa-engineer` | 1.0.0 | 2 | Acts as a QA Engineer / Tester SDLC expert to design test strategies, write test cases, author bug reports, and assess release readiness. Applies the test auto… |
| `security-engineer` | 1.0.0 | 2 | Acts as a Security Engineer / Application Security (AppSec) SDLC expert covering threat modeling (STRIDE), secure coding against the OWASP Top 10 and ASVS, SAS… |
| `skill-creator` | 1.0.0 | 5 | Create new Claude Code skills from scratch, improve or review existing skills, validate skill structure, classify a skill into the right tier, and run guided i… |
| `skill-learner` | 1.0.0 | 3 | Detects when a praxis SDLC expert hits a knowledge gap mid-task — missing team conventions, runbooks, or domain rules it should have applied — and turns it int… |
| `software-architect` | 1.0.0 | 2 | Adopts the Software Architect persona to reason about system design, architectural trade-offs, non-functional requirements, architectural decision records (ADR… |
| `ux-ui-engineer` | 1.0.0 | 2 | Acts as a UX/UI Engineer SDLC expert bridging design and code — design systems and component libraries, design tokens and theming, visual design (type scale, c… |

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
| `/learn` | Turn a knowledge gap discovered during work into durable skill knowledge — capture an org convention, runbook, or rule, or refine an existing skill, by routing… |
| `/memory` | Manage the project's working-memory ledger — record plans/decisions/implementations, review what's pending, accept or reject entries, and roll back a snapshott… |
| `/ml` | Consult the ML/AI Engineer — problem framing & metric selection, ML-ready features (leakage, train/serve skew, feature stores), training & model selection, rig… |
| `/new-feature` | Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer,… |
| `/product` | Consult the Product Owner — backlog ordering, prioritization (MoSCoW/RICE/WSJF), sprint goals, Definition of Ready/Done, roadmapping, OKRs, story splitting, an… |
| `/qa` | Consult the QA Engineer — test strategy, test-case design, edge cases, bug reports, regression and risk-based testing, coverage gaps, and release-quality asses… |
| `/refine` | Run a quality-only improvement through the refinement lifecycle — assess → plan → change → verify — preserving observable behavior. Use to refactor, pay down t… |
| `/review-changes` | Review the current changes (diff) by routing to the right SDLC experts and returning didactic, severity-tagged findings. Use to catch bad practices before a PR… |
| `/security-architect` | Consult the Cybersecurity Architect — security architecture, zero trust, defense in depth, IAM/SSO design, segmentation, data protection, encryption/key strate… |
| `/security` | Consult the Security Engineer — threat modeling, finding/fixing vulnerabilities, secure coding (OWASP Top 10), authn/authz hardening, secrets, crypto usage, SA… |
| `/ux` | Consult the UX/UI Engineer — design systems and tokens, visual design (type/color/spacing/grid), interaction and motion, accessibility (WCAG 2.2 AA), responsiv… |
| `/validate-skills` | Validate every skill in the repo — runs the deterministic validator across .claude/skills/ and dist/. Use to check skill structure and frontmatter before commi… |

