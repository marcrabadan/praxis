---
description: StartupOS — discover and frame candidate startup/business opportunities from observed pains, trends, and signals, separating facts from assumptions. The intake front door of the StartupOS lifecycle.
argument-hint: <a domain, market, audience, trend, or raw observation>
---

Adopt the **StartupOS** discovery posture: load the `startupos-ceo`, `startupos-market-analyst`, and `startupos-customer-researcher` skills and reason as those agents, drawing on each skill's `references/practices.md` and self-checking against its `references/checklist.md`. This is the **Observe → Discover** entry of the StartupOS lifecycle ([docs/startupos/lifecycle.md](../../../docs/startupos/lifecycle.md)); the agent roster is indexed in [docs/startupos/agents.md](../../../docs/startupos/agents.md).

StartupOS answers *"what should we build, why, for whom, and how do we turn it into a real company?"* — it never builds product. Building is Praxis's job.

The discovery input:

$ARGUMENTS

## Purpose

Turn a vague domain, trend, or observation into a **structured set of candidate opportunities**, each framed as a real problem worth money, with the evidence (or lack of it) made explicit. No solutions yet, no scoring yet.

## Input

- A domain, market, audience, trend, or raw observation (`$ARGUMENTS`).
- Optional: prior StartupOS memory under [`memory/startupos/`](../../../memory/startupos/) (observations, markets, customers) — read it; do not invent it.

## Workflow

1. **Frame the question.** If the input is too thin to act on (no audience, no domain, no pain signal), ask **1–2** focused questions with `AskUserQuestion` before proceeding. Otherwise state a one-line understanding and continue.
2. **Observe.** List the signals: pains, workarounds, complaints, spending, regulatory shifts, technology unlocks (especially AI leverage). For each, label it **FACT** (sourced/observed), **ASSUMPTION**, **ESTIMATE**, or **HYPOTHESIS** — never blur them (guardrail).
3. **Discover candidates.** Derive 5–12 candidate opportunities. For each: the problem (in the sufferer's words), who has it, why now, and the earliest pain/spending signal.
4. **First-pass filter.** Drop candidates with no real pain, no existing spend, or no plausible AI leverage / defensibility (guardrail: *reject weak ideas* — but only filter here, do not rank).
5. **Record.** Write each surviving candidate to `memory/startupos/ideas/<slug>.md` using the [vision template](../../../docs/startupos/templates/vision.md) skeleton (problem + segment + signals only — the rest is filled later).

## Output / expected generated files

- `memory/startupos/ideas/<slug>.md` — one file per candidate (problem, segment, why-now, signals, source labels).
- `memory/startupos/observations/<topic>.md` — the raw signal log behind the candidates (optional).
- A chat summary table: candidate | problem | segment | strongest signal | FACT/ASSUMPTION mix.

## Guardrails

- **Never invent market data.** Any number without a source is marked `ASSUMPTION` or `ESTIMATE`.
- Separate **facts, assumptions, estimates, hypotheses** on every claim.
- Prefer opportunities with **real pain, existing spending, recurring revenue, AI leverage, and defensibility**.
- No solutions, no architecture, no go-to-market here — discovery only.

## Approval gates

None block here — discovery is divergent. The first human gate is at **`/startupos:select`** (idea selection) and the second at **`/startupos:export-praxis`** (handoff). Record candidates as proposals only.

## Next

`/startupos:research <candidate>` to deepen the strongest candidates.
