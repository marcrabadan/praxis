---
name: diagram
description: Generate versioned, text-based diagrams (Mermaid by default, PlantUML on request) from architecture decisions, memory ledger entries, system design, data models, or user/API flows. Produces C4 architecture maps, sequence diagrams, ER diagrams, and flow charts. Use when the user wants a visual representation of the system, a flow, or a data model.
tier: 3
version: 1.0.0
---

# Diagram

Produce versioned, text-based diagrams directly from the memory ledger and the codebase. Text-based diagrams (Mermaid, PlantUML) live in the repo, diff cleanly, and render natively on GitHub — no external tools required.

The memory ledger already holds the architectural decisions that shape the system. This skill reads those decisions alongside the code and renders them as visual artefacts a team can share, review, and update.

## When to use

- "Draw the system architecture."
- "Show the sequence for the auth flow."
- "Give me an ER diagram for the data model."
- "Map the deployment topology."
- "Show how data flows through the pipeline."
- "Generate a C4 diagram."

## When not to use

- The user wants prose documentation, not a diagram → use the `docs` skill instead.
- The user wants to *record* a decision → use the `memory` skill.
- The requested diagram type has no equivalent in Mermaid or PlantUML — confirm with the user before attempting.

## Workflows

Pick the type that best matches the request. When uncertain, ask: "Is this about components/structure (architecture), interactions over time (sequence), data entities (ER), or data movement (flow)?"

| Type | File | When |
|------|------|------|
| Architecture (C4) | [workflows/architecture.md](workflows/architecture.md) | System/container/component overview |
| Sequence | [workflows/sequence.md](workflows/sequence.md) | Step-by-step interactions, API calls, event flows |
| ER | [workflows/er.md](workflows/er.md) | Data model entities and relationships |
| Flow | [workflows/flow.md](workflows/flow.md) | Data pipelines, process flows, decision trees |

## References

- [references/mermaid.md](references/mermaid.md) — Mermaid syntax for each diagram type
- [references/diagram-types.md](references/diagram-types.md) — decision guide for choosing the right type

## Output format

Default: **Mermaid** (renders on GitHub, Notion, most wikis with no setup).  
Alternative: **PlantUML** — request it explicitly or use it when the diagram complexity exceeds Mermaid's limits (e.g. large class hierarchies, detailed deployment diagrams).

Each diagram is delivered as a fenced code block (````mermaid` or ````plantuml`) ready to paste into any Markdown file. If the user asks for a file, write it to `docs/diagrams/<type>-<slug>.md` by default.

## Output expectations

- Every diagram opens with a title comment (`%% Title`) and a one-line description below the fence.
- The diagram compiles without syntax errors — validate mentally against [references/mermaid.md](references/mermaid.md).
- Architecture diagrams include at least three levels of granularity (system, container, component) or clearly state which level they represent.
- Sequence diagrams include actor labels and numbered or labelled messages.
- ER diagrams label every relationship (verb phrase) and mark cardinality.
- Record each diagram to the memory ledger as an `artifact` entry (`pending`).

## Stop conditions

- The requested diagram is produced and free of syntax errors.
- A ledger `artifact` entry is recorded.
- If multiple diagram types are needed, all are produced before closing.
