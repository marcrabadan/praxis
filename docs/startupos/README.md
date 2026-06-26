# StartupOS

**StartupOS is an AI-native operating system for discovering, validating, designing, and preparing startup/business ideas — *before* they become engineering work in [Praxis](../../README.md).**

Where Praxis answers **"how do we build the product correctly?"**, StartupOS answers the question that comes before it:

> **What should we build, why, for whom, and how do we turn it into a real company?**

StartupOS is a **module/ecosystem layered on top of Praxis**, not a replacement for it. It uses the same conventions — Claude Code-native commands, markdown templates, a memory model, and human-in-the-loop gates — and ends by **handing a validated, Praxis-ready project** to the existing Praxis lifecycle (`/praxis:idea`, `/praxis:new-feature`, …).

## Why it exists

Praxis is excellent at turning a *defined* idea into a well-built product. But most ideas should never be built — they lack real pain, real spend, or any defensibility. StartupOS is the **front door**: it discovers many candidates, kills the weak ones, validates the survivors, designs the business around the winner, and only then exports to Praxis. It refuses to invent market data and forces a clean separation of **facts, assumptions, estimates, and hypotheses** at every step.

## Relationship with Praxis

| | StartupOS | Praxis |
| --- | --- | --- |
| Question | What/why/for-whom + how to make it a company | How to build it correctly |
| Output | A validated, Praxis-ready project bundle | Shipped, tested software |
| Altitude | Market, business, product, high-level architecture | Detailed design, code, delivery |
| Ends at | `/startupos-export-praxis` (human-approved gate) | `/praxis:new-feature` → release |

StartupOS **never builds product**. Its terminal action is the handoff. See [praxis-integration.md](praxis-integration.md).

## Documentation map

| Doc | What it covers |
| --- | --- |
| [vision.md](vision.md) | Vision and purpose of StartupOS |
| [lifecycle.md](lifecycle.md) | The 15-stage lifecycle (Observe → … → Export to Praxis) |
| [commands.md](commands.md) | The `/startupos-*` commands |
| [templates.md](templates.md) | The 13 templates and where they're filled |
| [agents.md](agents.md) | The 12 StartupOS agent personas |
| [memory.md](memory.md) | The `memory/startupos/` model and rules |
| [guardrails.md](guardrails.md) | The rules every command must obey |
| [praxis-integration.md](praxis-integration.md) | The StartupOS → Praxis handoff |
| [integrations.md](integrations.md) | Using StartupOS with Cursor, Claude Code, and Codex |

## Lifecycle at a glance

```
Observe → Discover → Research → Cluster → Score → Validate → Challenge → Improve
  → Rank → [Select ✋] → Business Case → Product Requirements → Architecture
  → Roadmap → [Export to Praxis ✋]
```

`✋` = mandatory human-in-the-loop approval gate. Full detail in [lifecycle.md](lifecycle.md).

## Commands

```
/startupos-discover        find & frame candidate opportunities
/startupos-research        market / customer / competitor research
/startupos-validate        design falsifiable validation experiments
/startupos-challenge       red-team the idea, expose failure modes
/startupos-rank            score & order the candidate shortlist
/startupos-select          ✋ human selects the idea to take forward
/startupos-business-case   model, pricing, unit economics, GTM
/startupos-prd             product requirements / MVP scope
/startupos-architecture    high-level AI-native architecture
/startupos-roadmap         phased path to launch
/startupos-export-praxis   ✋ human-approved handoff to Praxis
```

Full reference in [commands.md](commands.md).

## Quick start

```text
# 1. Discover candidates in a domain you understand
/startupos-discover "ops teams drowning in manual vendor-security reviews"

# 2. Research, validate, and challenge the strongest candidates
/startupos-research <slug>
/startupos-validate <slug>
/startupos-challenge <slug>

# 3. Rank, then YOU select (human gate)
/startupos-rank
/startupos-select <slug>

# 4. Design the business and the product
/startupos-business-case <slug>
/startupos-prd <slug>
/startupos-architecture <slug>
/startupos-roadmap <slug>

# 5. Export to Praxis (human gate), then build with Praxis
/startupos-export-praxis <slug>
/praxis:idea ...        # ownership passes to Praxis
/praxis:new-feature ...
```

## Core principles (guardrails)

- **Never invent market data** — label every claim `FACT` / `ASSUMPTION` / `ESTIMATE` / `HYPOTHESIS`.
- **Reject weak ideas** — prefer real pain, existing spend, recurring revenue, AI leverage, and defensibility.
- **Validate before building** — every idea needs falsifiable experiments before selection.
- **Human approval is mandatory** before *selecting the idea* and before *exporting to Praxis*.
- **Always include risks and failure modes.**

See [guardrails.md](guardrails.md) for the complete set.
