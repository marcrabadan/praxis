# Skill catalog

Generated index of every skill and command in this repo. Do not edit by hand — run `make catalog` (or `python .claude/factory/scripts/build_catalog.py`).

## Skills

| Skill | Version | Tier | Description |
| ----- | ------- | ---- | ----------- |
| `business-analyst` | 1.0.0 | 2 | Acts as a Business Analyst SDLC expert to elicit, structure, and validate requirements. Writes user stories with INVEST criteria and Gherkin acceptance criteri… |
| `cybersecurity-architect` | 1.0.0 | 2 | Adopts the Cybersecurity Architect persona to design and review security architecture at the system and organization level — zero-trust and defense-in-depth de… |
| `developer` | 1.0.0 | 2 | Acts as a Software Developer / Engineer SDLC expert covering clean code, SOLID/DRY/YAGNI principles, TDD and the test pyramid, commit discipline, branch and PR… |
| `devops-engineer` | 1.0.0 | 2 | Acts as a DevOps Engineer SDLC expert: designs CI/CD pipelines, writes infrastructure as code, advises on containerization and Kubernetes, selects deployment s… |
| `product-owner` | 1.0.0 | 2 | Acts as a Product Owner SDLC expert: owns and orders the product backlog, writes and refines backlog items and epics, applies prioritization frameworks (MoSCoW… |
| `qa-engineer` | 1.0.0 | 2 | Acts as a QA Engineer / Tester SDLC expert to design test strategies, write test cases, author bug reports, and assess release readiness. Applies the test auto… |
| `security-engineer` | 1.0.0 | 2 | Acts as a Security Engineer / Application Security (AppSec) SDLC expert covering threat modeling (STRIDE), secure coding against the OWASP Top 10 and ASVS, SAS… |
| `skill-creator` | 1.0.0 | 5 | Create new Claude Code skills from scratch, improve or review existing skills, validate skill structure, classify a skill into the right tier, and run guided i… |
| `software-architect` | 1.0.0 | 2 | Adopts the Software Architect persona to reason about system design, architectural trade-offs, non-functional requirements, architectural decision records (ADR… |

## Commands

| Command | Description |
| ------- | ----------- |
| `/analyst` | Consult the Business Analyst — eliciting and clarifying requirements, writing user stories with acceptance criteria, process modeling, stakeholder analysis, sc… |
| `/architect` | Consult the Software Architect — system design, architectural trade-offs, NFRs, ADRs, scaling, concurrency/race conditions, pattern or technology selection, an… |
| `/developer` | Consult the Developer — diagnosing a bug, implementing or refactoring code, test design, error handling, security basics, commit/PR hygiene, and code review. |
| `/devops` | Consult the DevOps Engineer — CI/CD pipelines, infrastructure as code, containers/Kubernetes, deployment strategies, rollbacks, observability/SLOs, incident re… |
| `/new-feature` | Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer,… |
| `/product` | Consult the Product Owner — backlog ordering, prioritization (MoSCoW/RICE/WSJF), sprint goals, Definition of Ready/Done, roadmapping, OKRs, story splitting, an… |
| `/qa` | Consult the QA Engineer — test strategy, test-case design, edge cases, bug reports, regression and risk-based testing, coverage gaps, and release-quality asses… |
| `/review-changes` | Review the current changes (diff) by routing to the right SDLC experts and returning didactic, severity-tagged findings. Use to catch bad practices before a PR… |
| `/security-architect` | Consult the Cybersecurity Architect — security architecture, zero trust, defense in depth, IAM/SSO design, segmentation, data protection, encryption/key strate… |
| `/security` | Consult the Security Engineer — threat modeling, finding/fixing vulnerabilities, secure coding (OWASP Top 10), authn/authz hardening, secrets, crypto usage, SA… |
| `/validate-skills` | Validate every skill in the repo — runs the deterministic validator across .claude/skills/ and dist/. Use to check skill structure and frontmatter before commi… |

