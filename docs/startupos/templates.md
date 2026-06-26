# StartupOS — Templates

StartupOS ships 13 markdown templates under [`docs/startupos/templates/`](templates/). They are the structured skeletons the `/startupos:*` commands fill in, and together they form the **Praxis-ready `docs/` bundle** produced at handoff.

Each template carries a leading HTML comment stating which command fills it and the labeling rule. **Every claim must be labeled** one of:

- `[FACT]` — observed/sourced (include the source)
- `[ASSUMPTION]` — believed but unverified
- `[ESTIMATE]` — derived (include the derivation/method)
- `[HYPOTHESIS]` — testable, awaiting an experiment

This is the single most important convention: it is how StartupOS refuses to invent market data.

## The templates

| Template | Filled by | Purpose |
| -------- | --------- | ------- |
| [vision.md](templates/vision.md) | `/startupos:discover` | Problem, segment, why-now, signals, AI leverage, defensibility |
| [market-research.md](templates/market-research.md) | `/startupos:research` | Market thesis, sizing (ranges + method), demand evidence, evidence log |
| [business-case.md](templates/business-case.md) | `/startupos:business-case` | Value prop, model, unit-economics summary, the ask, make-or-break assumption |
| [competitive-analysis.md](templates/competitive-analysis.md) | `/startupos:research`, `/startupos:challenge` | Landscape map, substitutes, differentiation, moat, threat assessment |
| [pricing.md](templates/pricing.md) | `/startupos:business-case` | Value metric, packaging, willingness-to-pay evidence, risks |
| [financials.md](templates/financials.md) | `/startupos:business-case` | Assumptions ledger, unit economics with formulas, 3-scenario model, sensitivity |
| [product-requirements.md](templates/product-requirements.md) | `/startupos:prd` | MVP scope, personas, FR/NFR, INVEST user stories, success metrics |
| [architecture.md](templates/architecture.md) | `/startupos:architecture` | C4 L1/L2, AI strategy, build-vs-buy, data/privacy, NFRs/risks, feasibility |
| [roadmap.md](templates/roadmap.md) | `/startupos:roadmap` | Phases, unlock metrics, validation gates, resourcing, dependencies |
| [validation-plan.md](templates/validation-plan.md) | `/startupos:validate` | Leap-of-faith assumptions, falsifiable experiments, kill/continue thresholds |
| [gtm.md](templates/gtm.md) | `/startupos:business-case` | Beachhead, positioning, motion, channels, first-100-customers, funnel |
| [risk-analysis.md](templates/risk-analysis.md) | `/startupos:challenge` | Risk register, top failure modes, fatal assumptions, kill criteria |
| [praxis-handoff.md](templates/praxis-handoff.md) | `/startupos:export-praxis` | The handoff manifest: bundle contents, what's validated vs assumed, Praxis command sequence |

## How templates relate to memory

A template is the **document shape**; `memory/startupos/` is the **working store**. Commands typically:

1. Read prior evidence from `memory/startupos/*` (see [memory.md](memory.md)).
2. Write/update working artifacts in `memory/startupos/*`.
3. Render the relevant template for the human to review.
4. At export, assemble the templates into the Praxis-ready `docs/` bundle.

## Reuse over reinvention

These templates intentionally echo Praxis artifact shapes where they overlap:

- `product-requirements.md` uses **INVEST user stories + Gherkin acceptance criteria** — the same convention the Praxis `business-analyst` expects, so `/praxis:analyst` picks it up cleanly.
- `architecture.md` produces **C4 L1/L2** only; Praxis's `software-architect` owns ADRs and detailed design after handoff.
- `risk-analysis.md` and `validation-plan.md` feed Praxis discovery/research so nothing is re-derived.

When editing templates, keep them detailed but skeletal — they are scaffolds to fill, not finished documents.
