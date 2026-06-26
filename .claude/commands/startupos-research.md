---
description: StartupOS — research a candidate opportunity (market, customers, competitors, willingness to pay) and cluster findings into a defensible market thesis, marking every claim as fact, assumption, estimate, or hypothesis.
argument-hint: <a candidate idea slug or description>
---

Adopt the **StartupOS** research posture: load the `startupos-market-analyst` and `startupos-customer-researcher` skills (reviewed by `startupos-vc-partner`) and reason as those agents, drawing on each skill's `references/practices.md` and `references/checklist.md`. This is the **Research → Cluster** stage of the lifecycle; the agent roster is indexed in [docs/startupos/agents.md](../../docs/startupos/agents.md).

The candidate to research:

$ARGUMENTS

## Purpose

Replace assumptions with evidence. Produce a market-research dossier for a candidate so that scoring, validation, and the business case rest on something defensible — not vibes.

## Input

- A candidate idea slug (from `memory/startupos/ideas/`) or a description.
- Existing StartupOS memory (`markets/`, `competitors/`, `customers/`, `interviews/`) — reuse before re-deriving.

## Workflow

1. **Scope the questions.** From the candidate's open questions, list what must be true for this to be a business (demand, segment size, willingness to pay, incumbents, distribution).
2. **Gather evidence.** Use available research tools (web search, prior memory, user-supplied sources). Apply **Reuse > Extend > Build**: check existing memory first. Log each source with what it supports.
3. **Cluster.** Group findings into a coherent **market thesis**: who the buyer is, the job-to-be-done, the size band (TAM/SAM/SOM as ranges, each labeled `ESTIMATE` with its derivation), and the competitive landscape.
4. **Label rigorously.** Every claim is `FACT` (with source), `ASSUMPTION`, `ESTIMATE` (with method), or `HYPOTHESIS` (testable). Unsupported numbers are never presented as facts (guardrail).
5. **Surface gaps.** Name what you could not verify and what a validation experiment would need to test.

## Output / expected generated files

- `memory/startupos/markets/<slug>.md` — market thesis, sizing (ranges + derivation), trends, why-now.
- `memory/startupos/competitors/<slug>.md` — competitive map (incumbents, substitutes, gaps), seeded from the [competitive-analysis template](../../docs/startupos/templates/competitive-analysis.md).
- `memory/startupos/customers/<slug>.md` — segments, ICP, pains, current spend.
- Updated `memory/startupos/ideas/<slug>.md` with the market-research section ([market-research template](../../docs/startupos/templates/market-research.md)).
- A chat summary: thesis, top 3 evidenced facts, top 3 open assumptions, biggest unknown.

## Guardrails

- **Do not invent market data.** No fabricated TAM, growth rates, or quotes. Cite or label.
- Keep facts/assumptions/estimates/hypotheses visibly separated in every file.
- Note failure modes and disconfirming evidence honestly — research that only confirms is a red flag.

## Approval gates

None block here, but research quality gates the later **idea selection** gate. Thin research → the idea cannot pass `/startupos-select`.

## Next

`/startupos-validate <slug>` to design experiments, or `/startupos-challenge <slug>` for a red-team pass.
