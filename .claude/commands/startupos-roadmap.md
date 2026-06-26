---
description: StartupOS — phase the journey from validated idea to launched company: milestones, the MVP-first sequence, validation gates, hiring/resourcing, and the metrics that unlock each phase.
argument-hint: <the selected idea slug>
---

Adopt the **StartupOS** roadmap posture: load the `startupos-ceo` and `startupos-product-strategist` skills (with `startupos-financial-analyst` and `startupos-gtm-strategist`) and reason as those agents, drawing on each skill's `references/practices.md` and `references/checklist.md`. This is **Generate Roadmap** in the lifecycle; the agent roster is indexed in [docs/startupos/agents.md](../../docs/startupos/agents.md).

The idea to phase:

$ARGUMENTS

## Purpose

Lay out a **realistic, milestone-driven path** from today to a launched, learning company — sequenced so each phase de-risks the next and nothing is built before it is validated.

## Input

- The PRD, architecture, business case, and validation plan for the idea.

## Workflow

1. **Phases.** Typically: Validate → MVP → Beachhead launch → Early traction → Scale. Adjust to the idea.
2. **Milestones & gates.** For each phase: the goal, the deliverables, the **metric that unlocks the next phase**, and the validation gate that must pass first.
3. **MVP-first sequencing.** Order the build so the riskiest assumption is tested earliest and the wedge ships before the platform.
4. **Resourcing.** Rough team/skills and budget per phase (labeled `ESTIMATE`), and what triggers the next hire.
5. **Dependencies & risks.** Cross-phase dependencies and the risks that could stall each phase.

## Output / expected generated files

- Roadmap doc seeded from the [roadmap template](../../docs/startupos/templates/roadmap.md).
- A chat summary: the phases, each unlock-metric, and the nearest validation gate.

## Guardrails

- **No building before validation** — each phase names the validation gate it depends on.
- Timeline and cost figures are `ESTIMATE`s with stated assumptions, never presented as commitments.
- **Always include risks** per phase and the early-warning signal for each.
- Keep MVP scope honest — the roadmap must not quietly reintroduce cut scope.

## Approval gates

No new hard gate; the roadmap is part of the export bundle reviewed at the **export gate**.

## Next

`/startupos-export-praxis <slug>` to package the Praxis-ready handoff.
