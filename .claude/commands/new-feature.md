---
description: Run a feature idea or PRD through the full SDLC, consulting each expert in order — Business Analyst, Product Owner, Software Architect, Developer, QA Engineer, DevOps Engineer — to produce one consolidated plan. Use to kick off a new feature end to end.
argument-hint: <the feature idea, PRD, or ticket>
---

Orchestrate the SDLC expert skills over the feature below, following the full lifecycle — **Discovery → Research → Spec → Plan → Tasks → Build → Verify → Release** — driven by the **core six** (Business Analyst → Product Owner → Software Architect → Developer → QA → DevOps) plus any specialist experts the feature warrants (see *Domain experts* below). Each phase **builds on the output of the previous one**: every expert receives the artifacts produced before it. **Understand before specifying, research before specifying, specify before building, validate before releasing.**

The feature to work through:

$ARGUMENTS

## Phase 0 — Scope (gate)

Handle this yourself in the main conversation (subagents cannot talk to the user). If the feature is underspecified (the problem, the target user, or the desired outcome is unclear), ask **2–3** clarifying questions with `AskUserQuestion` before starting. If it is clear enough, state your one-line understanding and proceed.

## Phase 0.5 — Context digest (cheap, optional)

If the feature touches an existing codebase or a long PRD, **gather the shared context once on a cheap model** instead of making every expert re-discover it. Dispatch a single `Agent` (`subagent_type: Explore`, `model: haiku`) to find the relevant files/conventions and condense the PRD into a **short factual digest** — paths, current behavior, key constraints, no opinions. Pass that digest into every later phase alongside the prior artifacts. This is retrieval, not reasoning, so the cheap tier costs little and the experts stop paying to re-read the same material. Skip for greenfield or trivial features.

## Phase D — Discovery (understand before proposing)

Before any specification, **frame the problem**. Dispatch the `business-analyst` to produce a **Discovery Report**: problem statement (in the user's terms, not a solution), business goals, stakeholders, constraints, assumptions, risks, and open questions. No solutions yet. In harness mode this is `discovery/discovery-report.md`.

## Phase R — Research (research before specifying)

**Research must precede the specification.** Dispatch `deep-research` (and any domain expert the questions need) to investigate the open questions from discovery and produce a **Research Report** + **Evidence Log** + **Alternatives Analysis**. Apply **Reuse > Extend > Build**: surface what already exists in this codebase, the org, the ecosystem, and the praxis skills before proposing something new. In harness mode these are `research/research-report.md`, `research/evidence-log.md`, `research/alternatives.md`.

### Gate 1 — Discovery & Research approval (HITL)

Present the consolidated discovery + research to the user with **Recommendation, Evidence, Risks, Alternatives**, and request `ACCEPT | REFINE | REJECT`. **Do not write the spec until this is accepted** — research informs the spec, the spec is not guessed. Pending is not approval.

## Phases

Each phase produces **one concise, structured artifact** that becomes the input to the phases after it and to the final summary.

1. **Business Analyst** (`business-analyst`) — building on the accepted Discovery + Research, turn understanding into the **specification**: capture business/functional/non-functional requirements; write user stories (INVEST) with Gherkin acceptance criteria; resolve the discovery open questions or flag the ones that still block. This produces the `spec.md` in harness mode.
2. **Product Owner** (`product-owner`) — slice into thin vertical increments, prioritize them (pick and justify a framework), define the sprint goal and the Definition of Ready/Done, and state the value/outcome being targeted.
3. **Software Architect** (`software-architect`) — propose the design approach, record the key decisions as short ADR notes, call out the driving NFRs, the main trade-offs, and the top risks.
4. **Developer** (`developer`) — turn the top-priority slice into a concrete implementation plan: components/files to touch, the test approach, and an ordered task list. Note assumptions; do not write production code unless asked.
5. **QA Engineer** (`qa-engineer`) — derive a test strategy and the highest-value test cases (positive, negative, boundary) from the acceptance criteria; identify the riskiest areas and regression scope.
6. **DevOps Engineer** (`devops-engineer`) — outline delivery and rollout (pipeline gates, deployment strategy, rollback), the observability/SLOs to add, and run the production-readiness checklist.
7. **Release** (`devops-engineer` + `product-owner`) — only after the work is built and verified: confirm the acceptance criteria are met against the verify report, write the **release notes** (what shipped, residual risks, rollback), and present **Gate 4 (Release approval)** for `ACCEPT | REFINE | REJECT`. In a planning-only run, produce the release/readiness plan rather than releasing. In harness mode this is `reports/release/release-notes.md`.

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

## Docs and diagrams — inline with each phase

Each expert writes its documentation file **before** returning its planning artifact to this thread — no separate `/docs` or `/diagram` step needed. The file is the durable record; the artifact is the compact summary for the next phase.

| Phase | File to write | Diagram to generate |
|-------|--------------|---------------------|
| BA | `docs/functional-manual.md` — Purpose, Feature Catalogue, User Journeys, Business Rules | — |
| PO | append Priorities + Sprint Goal sections to `docs/functional-manual.md` | — |
| Architect | `docs/decisions/ADR-<NNN>-<slug>.md` per significant decision | `docs/diagrams/architecture-<slug>.md` (L2, if design is non-trivial) |
| Security | append Security Architecture section to `docs/technical-manual.md` | — |
| UX | append UI Guide section to `docs/functional-manual.md` | — |
| Developer | `docs/technical-manual.md` — Module Map, Implementation Notes, Configuration | — |
| QA | `docs/test-strategy.md` | — |
| DevOps | append Operations + Runbook sections to `docs/technical-manual.md` | `docs/diagrams/flow-deploy-<slug>.md` (if pipeline is non-trivial) |

Rules for subagents:
- Write the file first, **then** return the artifact text to this thread.
- If the file already exists, append or update the relevant section — do not overwrite.
- Skip a file only when the artifact is trivially thin (e.g. a one-liner BA scope on a tiny feature).
- Tag each ledger artifact entry with `source:<planning-entry-id>` so rollback can mark it stale.
- ADR numbering: check the existing count in `docs/decisions/` and increment.

## Harness mode — durable spec artifacts (conditional)

If the repo is in **harness mode** — a `.praxis/config.json` exists and resolves a `projectId` — then *in addition* to the `docs/` files above, write the feature's durable, typed artifacts under the owning project, following the `feature-development` workflow (`spec → plan → tasks → verify`). The doctrine is in the harness at `systems/feature-development/artifact-model.md`; the gates are in `workflows/feature-development.workflow.json` (resolve the harness via the config's `harnessRoot`).

```
projects/<projectId>/specs/<spec-slug>/
  discovery/discovery-report.md # Discovery: problem, stakeholders, assumptions, open questions
  research/research-report.md   # Research: findings, recommendation (research precedes spec)
  research/evidence-log.md      # one row per source
  research/alternatives.md      # options weighed; chosen direction
  spec.md                       # BA + PO: problem, scope, requirements (frontmatter status: draft)
  decisions/                    # one mini-ADR per significant call (architect/PO/QA/devops/security)
  plans/implementation-plan.md  # Developer: approach, files, ordered tasks
  tasks/tasks.md                # the ordered checklist
  reports/verify/report.md      # verify evidence, once the work is built
  reports/release/release-notes.md # Release: what shipped, acceptance met, rollback (Gate 4)
```

- Copy the harness's `projects/_template/specs/_template/` as the starting shape; set `spec.md` frontmatter `id` = the spec folder slug and `project` = the resolved `projectId`. Assign typed ids and link `source:`/`traces:` per [`rules/traceability.md`](../../rules/traceability.md) so the chain `IDEA → DISC → RES → SPEC → … → REL` stays navigable.
- **Discovery and Research come first.** Write `discovery/` then `research/` before `spec.md`, and hold **Gate 1** (Discovery & Research approval) before the spec is written. Research must precede the spec.
- **Respect the gates.** A planning run *proposes*: leave `spec.md` at `status: draft` and the plan/decisions as `pending`. **Pending is not approval** — do not advance a gate on a pending artifact. The user accepts the spec (`status: accepted`) before the plan authorizes a build, and accepts the plan before tasks drive implementation.
- The chat summary (next section) becomes a **pointer** to these artifacts, not the source of truth.
- Tag the memory-ledger entries with the spec path so they are traceable to the spec.
- **Stop condition:** if a `projectId` is declared but does not resolve to `projects/<projectId>/`, stop and ask — do not guess a destination.
- If the repo is **not** in harness mode, skip this section and behave as before (`docs/` + ledger only).

## Execution

Run each phase in its **own subagent** (the `Agent` tool, `subagent_type: general-purpose`) so each expert's doctrine loads in an isolated context and only its compact artifact returns to the main thread — the skill references never pile up here, and no phase re-reads another expert's full skill. In every subagent prompt:

- tell it to **adopt the named skill** (e.g. invoke the `business-analyst` skill) and reason in that persona;
- pass the feature plus **all prior artifacts** verbatim as its input;
- have it draw on the skill's `references/practices.md` to produce the artifact, then **self-check against `references/checklist.md`** before returning (that checklist read stays inside the subagent, not here);
- instruct it to **write its documentation file and diagram** (from the table above) before returning — the file is written inside the subagent; only the compact artifact text comes back here;
- ask it to return the structured artifact — no preamble — and to surface any blocking ambiguity as an explicit open question rather than guessing.

Schedule by dependency, not by reflex:

- Phases **1 → 2 → 3** (BA → PO → Architect) are serial — each needs the previous artifact.
- **After Phase 3, pick the warranted domain experts** (table above) and dispatch them — in parallel with each other — **before the Developer phase**. Their findings (ML evaluation/serving constraints, security controls, frontend architecture, …) are exactly what the implementation plan must build on, so the Developer must see them.
- **Phase 4 (Developer)** runs once the domain-expert artifacts are back, with all prior artifacts as input.
- **Phases 5 (QA)** and **6 (DevOps)** depend only on phases 1–4 (plus the domain experts), not on each other — dispatch **both subagents in a single message** so they run in parallel.

If a subagent returns a blocking open question, surface it to the user (or resolve it from context) before continuing.

### Model tiers (cost vs. depth)

Match the model to the work, not to reflex — token price is the lever, reasoning quality is the constraint:

- **Opus** — the design/build reasoning where depth pays off: Software Architect, Developer, and the domain experts (security, ML/AI, frontend/data architecture). Cheapening these trades quality for little saving, since their outputs are small.
- **Sonnet** — the structured-but-shallower phases that mostly transform prior artifacts: Business Analyst, Product Owner, QA Engineer, DevOps Engineer.
- **Haiku** — pure retrieval/summarization only (the Phase 0.5 digest). Never the reasoning phases.

Pass `model` to the `Agent` tool per phase. These are sensible defaults — keep a phase on Opus if the feature makes it genuinely hard (e.g. a compliance-heavy BA framing), and tell the user which tiers you chose.

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

Before ending, record the consolidated plan and the key decisions to the memory ledger so they survive the session (use the `memory` skill). Prefer one `plan` entry for the consolidated output plus a `decision` entry per significant call — and those calls come from across the roster, not just the architect: a prioritization decision (PO), a test-strategy gate (QA), a deploy/rollback choice (DevOps), or a risk acceptance (security) each deserve their own `decision` entry. Use `--source /new-feature` and leave them `pending` for the user to accept — this is a planning run, so it proposes, it does not ship: don't act on a pending decision without an explicit accept. If the repo has no ledger yet, `python .claude/skills/memory/scripts/ledger.py init` creates one. Skip only if the user opted out of memory.
