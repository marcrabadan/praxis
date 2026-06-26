# StartupOS — Lifecycle

StartupOS runs a **15-stage lifecycle** from raw observation to a Praxis-ready handoff. It mirrors the spirit of Praxis's harness lifecycle (understand → validate → specify → build) but at **business/market altitude**, ending exactly where Praxis begins.

```
Observe → Discover → Research → Cluster → Score → Validate → Challenge → Improve
  → Rank → [Select ✋] → Generate Business Case → Generate Product Requirements
  → Generate Architecture → Generate Roadmap → [Export to Praxis ✋]
```

`✋` = mandatory human-in-the-loop approval gate.

## Stages

| # | Stage | Command | Primary agents | Output |
| - | ----- | ------- | -------------- | ------ |
| 1 | **Observe** | `/startupos:discover` | Market Analyst, Customer Researcher | Raw signal log |
| 2 | **Discover** | `/startupos:discover` | CEO, Market Analyst | Candidate ideas |
| 3 | **Research** | `/startupos:research` | Market Analyst, Customer Researcher | Market thesis, sizing |
| 4 | **Cluster** | `/startupos:research` | Market Analyst | Grouped findings → thesis |
| 5 | **Score** | `/startupos:rank` | VC Partner, Financial Analyst | Per-criterion scores |
| 6 | **Validate** | `/startupos:validate` | Customer Researcher, Business Designer | Hypotheses + experiments |
| 7 | **Challenge** | `/startupos:challenge` | VC Partner, Financial Analyst, Security Officer | Risk register, verdict |
| 8 | **Improve** | `/startupos:challenge` | Business Designer, Product Strategist | Concrete improvements |
| 9 | **Rank** | `/startupos:rank` | VC Partner, CEO | Ordered shortlist |
| 10 | **Select** ✋ | `/startupos:select` | **Human** (CEO facilitates) | Selection decision |
| 11 | **Business Case** | `/startupos:business-case` | Business Designer, Financial Analyst, GTM Strategist | Model, pricing, financials, GTM |
| 12 | **Product Requirements** | `/startupos:prd` | Product Strategist | PRD / MVP scope |
| 13 | **Architecture** | `/startupos:architecture` | CTO, AI Architect, Security Officer | High-level architecture |
| 14 | **Roadmap** | `/startupos:roadmap` | CEO, Product Strategist | Phased roadmap |
| 15 | **Export to Praxis** ✋ | `/startupos:export-praxis` | **Human** (CEO/CTO assemble) | Praxis-ready bundle |

## The three phases

**Phase A — Divergence (1–9): find and pressure-test optionality.**
Cast wide, gather evidence, run experiments, red-team hard, and rank. The goal is *many* candidates and an honest, evidence-weighted shortlist. Weak ideas are killed here, not carried forward.

**Phase B — Convergence (10–14): design the winner.**
After the human selects one idea, design the *company* around it: business model, pricing, unit economics, GTM, product requirements, high-level architecture, and roadmap.

**Phase C — Handoff (15): cross the boundary.**
Package everything into a Praxis-ready project and, with human approval, hand off. Ownership passes to Praxis.

## Human-in-the-loop checkpoints

StartupOS deliberately keeps two **hard gates** — the two decisions where being wrong is most expensive:

1. **Select (stage 10)** — `/startupos:select` will not commit to an idea without explicit human approval. Ranking is advisory; the human chooses.
2. **Export to Praxis (stage 15)** — `/startupos:export-praxis` will not hand off without explicit human approval. The human confirms the evidence is strong enough to justify engineering spend.

Everything else is advisory and reversible. Discovery is divergent on purpose; the gates exist precisely so divergence is safe.

> **Pending is not approval.** As in Praxis, a recorded recommendation is a proposal, not a green light. Selection and export require an explicit human *accept*.

## Loop-backs

The lifecycle is not strictly linear. Common loops:

- **Challenge → Research/Validate.** A red-team pass that exposes a gap routes back to gather more evidence.
- **Rank → Discover.** A thin shortlist sends you back to discover more candidates.
- **Select → Rank.** "Pick another" returns to the shortlist.
- **Export → any convergence stage.** "Revise" at the export gate sends you back to fix the weak artifact.

## Traceability

Each stage writes to `memory/startupos/` (see [memory.md](memory.md)) so the chain
`observation → idea → research → hypothesis → experiment → decision → handoff`
stays navigable — the same traceability discipline Praxis applies to `IDEA → DISC → RES → SPEC → … → REL`.
