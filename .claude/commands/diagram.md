---
description: Generate a Mermaid diagram from the memory ledger and the codebase. Just describe what you want to see — the system, a flow, the data model, a pipeline — and the right diagram type is chosen automatically.
argument-hint: "<describe what you want to see>"
---

Generate a diagram using the `diagram` skill.

$ARGUMENTS

## Pick the diagram type from the description

Read the request and infer the best type — do not ask the user for a type keyword:

| What the request is about | Diagram type |
|---------------------------|--------------|
| The overall system, services, how things connect, deployment | [architecture](../skills/diagram/workflows/architecture.md) |
| A flow of calls, a user journey, how X talks to Y, an API | [sequence](../skills/diagram/workflows/sequence.md) |
| The data model, entities, tables, schema, relationships | [er](../skills/diagram/workflows/er.md) |
| A pipeline, a process, CI/CD steps, a decision tree | [flow](../skills/diagram/workflows/flow.md) |

Only ask a clarifying question if the description genuinely fits two types equally well. One question maximum, with two concrete options.

## No arguments

If the request is empty, generate an L2 architecture diagram of the whole system — the most useful default.

## Output

- Deliver the diagram as a fenced `mermaid` code block, ready to paste into any Markdown file.
- One-line description above the fence (what it shows).
- Write to `docs/diagrams/<type>-<slug>.md` if the user asks for a file.
- Record the diagram as a `pending` artifact in the memory ledger before ending.
