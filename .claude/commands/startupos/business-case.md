---
description: StartupOS — build the business case for the selected idea: value proposition, business model, pricing, unit economics, financials, and go-to-market — with every number labeled fact, estimate, or assumption.
argument-hint: <the selected idea slug>
---

Adopt the **StartupOS** business-design posture: load the `startupos-business-designer`, `startupos-financial-analyst`, and `startupos-gtm-strategist` skills (reviewed by `startupos-vc-partner` and `startupos-legal-compliance`) and reason as those agents, drawing on each skill's `references/practices.md` and `references/checklist.md`. This is **Generate Business Case** in the lifecycle; the agent roster is indexed in [docs/startupos/agents.md](../../../docs/startupos/agents.md).

The selected idea:

$ARGUMENTS

## Purpose

Turn a selected idea into a coherent **business**: how it creates value, who pays, how much, how it reaches them, and whether the unit economics can work. This is the commercial backbone the PRD and architecture serve.

## Input

- The selection decision (`memory/startupos/decisions/selection-<slug>.md`) and the full research/validation trail.

## Workflow

1. **Value proposition & business model.** Job-to-be-done, the wedge, the model (SaaS, marketplace, usage-based, etc.), and why it is defensible.
2. **Pricing.** Packaging, price metric, tiers, and the willingness-to-pay evidence behind them (label evidence vs assumption). Use the [pricing template](../../../docs/startupos/templates/pricing.md).
3. **Unit economics & financials.** CAC, LTV, gross margin, payback, and a simple 3-scenario (low/base/high) model. **Every figure is `FACT`, `ESTIMATE` (with derivation), or `ASSUMPTION`.** Use the [financials template](../../../docs/startupos/templates/financials.md).
4. **Go-to-market.** Beachhead segment, channels, motion (PLG/sales-led), and the first-100-customers plan. Use the [gtm template](../../../docs/startupos/templates/gtm.md).
5. **Risks.** Pull forward the challenge risks; tie each to a mitigation or a validation experiment.
6. **Assemble** the business case and confirm it stays consistent with the recorded evidence.

## Output / expected generated files

- `memory/startupos/financials/<slug>.md` — the unit-economics model and scenarios.
- `memory/startupos/pricing/<slug>.md` — pricing & packaging.
- Business-case doc seeded from the [business-case template](../../../docs/startupos/templates/business-case.md), plus `gtm.md` from the [gtm template](../../../docs/startupos/templates/gtm.md).
- A chat summary: model, price metric, key unit economics (labeled), and the make-or-break assumption.

## Guardrails

- **Do not invent market or financial data** — derive estimates transparently or label them assumptions.
- Separate facts/assumptions/estimates/hypotheses in every financial claim.
- Prefer recurring revenue, existing spend, and AI leverage; flag if the model lacks them.
- **Always include risks and failure modes** and the validation experiments that de-risk the numbers.

## Approval gates

No new hard gate, but the business case is reviewed at the **export gate**. A business case built on unvalidated numbers should not reach Praxis without the human knowingly accepting that.

## Next

`/startupos:prd <slug>` to define the product, or `/startupos:architecture <slug>`.
