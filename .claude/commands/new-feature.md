---
description: Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer, DevOps Engineer — to produce one consolidated plan. Use to kick off a new feature end to end.
argument-hint: <the feature idea, PRD, or ticket>
---

Orchestrate the six SDLC expert skills over the feature below, in lifecycle order. Each phase **builds on the output of the previous one**: every expert receives the artifacts produced before it.

The feature to work through:

$ARGUMENTS

## Phase 0 — Scope (gate)

Handle this yourself in the main conversation (subagents cannot talk to the user). If the feature is underspecified (the problem, the target user, or the desired outcome is unclear), ask **2–3** clarifying questions with `AskUserQuestion` before starting. If it is clear enough, state your one-line understanding and proceed.

## Phases

Each phase produces **one concise, structured artifact** that becomes the input to the phases after it and to the final summary.

1. **Business Analyst** (`business-analyst`) — frame the problem and stakeholders; capture business/functional/non-functional requirements; write user stories (INVEST) with Gherkin acceptance criteria; flag ambiguities and open questions.
2. **Product Owner** (`product-owner`) — slice into thin vertical increments, prioritize them (pick and justify a framework), define the sprint goal and the Definition of Ready/Done, and state the value/outcome being targeted.
3. **Software Architect** (`software-architect`) — propose the design approach, record the key decisions as short ADR notes, call out the driving NFRs, the main trade-offs, and the top risks.
4. **Developer** (`developer`) — turn the top-priority slice into a concrete implementation plan: components/files to touch, the test approach, and an ordered task list. Note assumptions; do not write production code unless asked.
5. **QA Engineer** (`qa-engineer`) — derive a test strategy and the highest-value test cases (positive, negative, boundary) from the acceptance criteria; identify the riskiest areas and regression scope.
6. **DevOps Engineer** (`devops-engineer`) — outline delivery and rollout (pipeline gates, deployment strategy, rollback), the observability/SLOs to add, and run the production-readiness checklist.

### Domain experts (conditional)

The core six are not enough when a feature has a strong specialist dimension. **After the Architect phase, judge from the feature and the design which — if any — of the domain experts below it warrants, and add each as an extra phase.** Do not run these by reflex; add an expert only when its column clearly applies.

| If the feature involves… | Add |
| ------------------------ | --- |
| ML/AI, models, LLMs, inference, training, evaluation, RAG, prompting, guardrails | **`ml-ai-engineer`** |
| Data pipelines (ETL/ELT, CDC, streaming), warehouse/lake modeling, dbt/orchestration, data quality | **`data-engineer`** |
| Authentication/authorization, untrusted input, crypto, secrets, or any abuse/vulnerability surface | **`security-engineer`** |
| Trust boundaries, identity/data-protection design, segmentation, encryption strategy, compliance-significant architecture | **`cybersecurity-architect`** |
| Frontend framework/rendering/state/routing/build architecture, design-system structure, Core Web Vitals | **`frontend-architect`** |
| UI components, client/server state, forms, styling, frontend TypeScript, performance, accessibility implementation | **`frontend-engineer`** |
| Design tokens, visual/interaction design, WCAG criteria, responsive layout, usability, UX writing | **`ux-ui-engineer`** |

Each added expert produces its own artifact (e.g. the ML/AI expert: metric & evaluation design, model/serving plan, guardrails, drift/retraining; the security expert: a STRIDE threat model + the top controls) that folds into the consolidated summary under its own heading.

## Execution

Run each phase in its **own subagent** (the `Agent` tool, `subagent_type: general-purpose`) so each expert's doctrine loads in an isolated context and only its compact artifact returns to the main thread — the skill references never pile up here, and no phase re-reads another expert's full skill. In every subagent prompt:

- tell it to **adopt the named skill** (e.g. invoke the `business-analyst` skill) and reason in that persona;
- pass the feature plus **all prior artifacts** verbatim as its input;
- have it draw on the skill's `references/practices.md` to produce the artifact, then **self-check against `references/checklist.md`** before returning (that checklist read stays inside the subagent, not here);
- ask it to return **only** the structured artifact — no preamble — and to surface any blocking ambiguity as an explicit open question rather than guessing.

Schedule by dependency, not by reflex:

- Phases **1 → 2 → 3 → 4** are serial — each needs the previous artifact, so run them one subagent at a time.
- After Phase 3, pick the **conditional domain experts** the feature warrants (table above).
- Phases **5 (QA)**, **6 (DevOps)**, and **any warranted domain experts** depend only on phases 1–4, not on each other — dispatch **all of those subagents in a single message** so they run in parallel.

If a subagent returns a blocking open question, surface it to the user (or resolve it from context) before continuing.

## Checkpoint

After Phase 3 (Architect), if the feature is large or the direction is uncertain, **pause** and confirm the framing + design direction with the user before continuing into the build/test/delivery phases. For small, clear features, continue straight through.

## Output

Close with a consolidated summary the user can act on:

- **Problem & scope** (BA)
- **Prioritized increments + sprint goal** (PO)
- **Design decisions, NFRs, risks** (Architect)
- **Implementation plan** (Developer)
- **Test strategy & key cases** (QA)
- **Rollout & production-readiness** (DevOps)
- **Domain-expert findings** (ML/AI, security, data, frontend, or UX) — only the experts the feature warranted
- **Open questions / assumptions** gathered across all phases

Keep each section concrete and short. The deliverable is a plan, not code — implement only when the user asks.

## Record to memory

Before ending, record the consolidated plan and the key architectural decisions to the memory ledger so they survive the session (use the `memory` skill). Prefer one `plan` entry for the consolidated output plus a `decision` entry per significant architectural call, each `--source /new-feature` and left `pending` for the user to accept. If the repo has no ledger yet, `python .claude/skills/memory/scripts/ledger.py init` creates one. Skip only if the user opted out of memory.
