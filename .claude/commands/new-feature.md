---
description: Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer, DevOps Engineer — to produce one consolidated plan. Use to kick off a new feature end to end.
argument-hint: <the feature idea, PRD, or ticket>
---

Orchestrate the six SDLC expert skills over the feature below, in lifecycle order. Each phase **builds on the output of the previous one** — keep all phases in this single conversation so context carries forward. Do not spawn subagents; load each skill in the main thread.

The feature to work through:

$ARGUMENTS

## Phase 0 — Scope (gate)

If the feature is underspecified (the problem, the target user, or the desired outcome is unclear), ask **2–3** clarifying questions with `AskUserQuestion` before starting. If it is clear enough, state your one-line understanding and proceed.

## Phases

Work through these in order. For each: load the named skill, use its `references/practices.md` and `references/checklist.md`, and produce the listed artifact. Carry every prior artifact forward as input.

1. **Business Analyst** (`business-analyst`) — frame the problem and stakeholders; capture business/functional/non-functional requirements; write user stories (INVEST) with Gherkin acceptance criteria; flag ambiguities and open questions.
2. **Product Owner** (`product-owner`) — slice into thin vertical increments, prioritize them (pick and justify a framework), define the sprint goal and the Definition of Ready/Done, and state the value/outcome being targeted.
3. **Software Architect** (`software-architect`) — propose the design approach, record the key decisions as short ADR notes, call out the driving NFRs, the main trade-offs, and the top risks.
4. **Developer** (`developer`) — turn the top-priority slice into a concrete implementation plan: components/files to touch, the test approach, and an ordered task list. Note assumptions; do not write production code unless asked.
5. **QA Engineer** (`qa-engineer`) — derive a test strategy and the highest-value test cases (positive, negative, boundary) from the acceptance criteria; identify the riskiest areas and regression scope.
6. **DevOps Engineer** (`devops-engineer`) — outline delivery and rollout (pipeline gates, deployment strategy, rollback), the observability/SLOs to add, and run the production-readiness checklist.

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
- **Open questions / assumptions** gathered across all phases

Keep each section concrete and short. The deliverable is a plan, not code — implement only when the user asks.

## Record to memory

Before ending, record the consolidated plan and the key architectural decisions to the memory ledger so they survive the session (use the `memory` skill). Prefer one `plan` entry for the consolidated output plus a `decision` entry per significant architectural call, each `--source /new-feature` and left `pending` for the user to accept. If the repo has no ledger yet, `python .claude/skills/memory/scripts/ledger.py init` creates one. Skip only if the user opted out of memory.
