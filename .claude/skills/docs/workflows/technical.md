# Workflow — Technical Manual

Generate the technical manual by routing each section to the right expert: Software Architect, Developer, and DevOps Engineer. Domain experts (Security, Data, ML/AI) are added when the feature warrants them.

## When you reach here

The user wants documentation for engineers — how the system is built, why key decisions were made, and how to operate it. Audience: engineers onboarding, on-call responders, code reviewers, architects.

## Steps

### 1. Gather shared context (once, cheap)

Run in parallel:

```bash
# Memory ledger — all accepted entries
python .claude/skills/memory/scripts/ledger.py list --status accepted

# Codebase orientation
find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.py" -o -name "*.go" \) | head -60
find . -name "docker-compose*" -o -name "Dockerfile" -o -name "*.tf" | head -20
cat README.md 2>/dev/null || true
```

Condense into a **context digest**: repo structure, main modules, tech stack, deployment environment. This goes into every expert subagent.

### 2. Dispatch expert subagents

Run Phase 1 first (it feeds Phases 2 and 3). Then run Phases 2 and 3 in parallel. Add domain experts between Phases 1 and 2 if warranted.

---

#### Phase 1 — Software Architect

Subagent prompt (pass context digest + all accepted ledger decisions and plans):

> Adopt the `software-architect` skill. Write the **Architecture** section of a technical manual.
>
> Include:
> - System overview: what problem it solves and the main architectural style (monolith, microservices, event-driven, etc.)
> - Component / service breakdown: table of components with their responsibility and technology
> - Key architectural decisions: render each accepted `decision` ledger entry as a short ADR block (Status, Context, Decision, Consequences)
> - Driving NFRs: performance, scalability, security, reliability targets
> - Known trade-offs and risks
>
> Source everything from the ledger entries and codebase. Return only the Markdown section.

---

#### Domain experts (conditional — add after Phase 1)

| If the system has… | Add expert | Section title |
|--------------------|-----------|---------------|
| Auth, crypto, untrusted input, secrets | `security-engineer` | Security Architecture |
| Data pipelines, warehouse, ETL | `data-engineer` | Data Architecture |
| ML models, LLMs, RAG, inference | `ml-ai-engineer` | AI/ML Architecture |

Each domain expert subagent receives: context digest + architect artifact + relevant ledger entries.

---

#### Phase 2 — Developer (parallel with Phase 3)

Subagent prompt (pass context digest + architect artifact + domain expert artifacts):

> Adopt the `developer` skill. Write the **Implementation Reference** section of a technical manual.
>
> Include:
> - Module / package map: table of top-level directories with their purpose
> - API reference: for each public endpoint or exported function, document signature, parameters, response, and one example
> - Data model: entity table (name, type, nullable, description) per entity in the codebase
> - Configuration reference: environment variables table (name, type, default, required, description)
> - Local development setup: step-by-step commands to get the project running
>
> Read the actual code — do not invent signatures or field names. Return only the Markdown section.

---

#### Phase 3 — DevOps Engineer (parallel with Phase 2)

Subagent prompt (pass context digest + architect artifact):

> Adopt the `devops-engineer` skill. Write the **Operations** section of a technical manual.
>
> Include:
> - Deployment topology: environments (dev / staging / prod) and how code flows through them
> - CI/CD pipeline: stages, gates, and promotion criteria
> - Observability: metrics, logs, traces, dashboards, and alerting thresholds
> - SLOs: availability, latency, error-rate targets
> - Runbook: step-by-step for the most critical operational procedures (deploy, rollback, incident triage)
> - On-call escalation path
>
> Source from ledger `rollout` entries and the CI/deploy config in the codebase. Return only the Markdown section.

---

### 3. Stitch into the manual

Assemble the sections into one file:

```markdown
# <System Name> — Technical Manual

> Generated: <date> | Source: memory ledger + codebase

## Table of Contents

1. [Architecture](#1-architecture)
2. [Security Architecture](#2-security-architecture) ← if applicable
3. [Data Architecture](#3-data-architecture) ← if applicable
4. [AI/ML Architecture](#4-aiml-architecture) ← if applicable
5. [Implementation Reference](#5-implementation-reference)
   - [Module Map](#module-map)
   - [API Reference](#api-reference)
   - [Data Model](#data-model)
   - [Configuration](#configuration)
   - [Local Setup](#local-setup)
6. [Operations](#6-operations)
   - [Deployment](#deployment)
   - [CI/CD](#cicd)
   - [Observability & SLOs](#observability--slos)
   - [Runbook](#runbook)

---

<!-- paste Architect artifact -->
<!-- paste domain expert artifacts -->
<!-- paste Developer artifact -->
<!-- paste DevOps artifact -->
```

Write to `docs/technical-manual.md` (or user-specified path).

### 4. Record to the ledger

```bash
python .claude/skills/memory/scripts/ledger.py log \
  --type artifact \
  --title "Technical Manual: <system name>" \
  --source /docs \
  --tags docs,manual,technical \
  --body "Technical manual written by Architect + Developer + DevOps subagents. Domain experts included: <list>. Sources: ledger entries <ids>. Path: docs/technical-manual.md."
```

### 5. Report

State the file path, sections produced, which experts were used, and any sections skipped with the reason.
