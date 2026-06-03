---
description: Generate a versioned Mermaid diagram (architecture, sequence, ER, or flow) from the memory ledger and the codebase. Use to visualise the system structure, a user/API flow, the data model, or a pipeline.
argument-hint: "<what to diagram> [architecture|sequence|er|flow]"
---

Generate a diagram using the `diagram` skill.

Request:

$ARGUMENTS

## How to handle it

Load the `diagram` skill and pick the right workflow from [.claude/skills/diagram/SKILL.md](../skills/diagram/SKILL.md):

| If the request mentions… | Use workflow |
|--------------------------|--------------|
| "architecture", "system", "services", "containers", "C4", "topology", "deployment" | [architecture](../skills/diagram/workflows/architecture.md) |
| "sequence", "flow of calls", "API", "auth flow", "journey", "interactions" | [sequence](../skills/diagram/workflows/sequence.md) |
| "ER", "data model", "entities", "schema", "tables", "relationships" | [er](../skills/diagram/workflows/er.md) |
| "pipeline", "CI", "process", "steps", "decision tree", "data flow", "ETL" | [flow](../skills/diagram/workflows/flow.md) |

If the request is ambiguous, ask one clarifying question using the guide in [references/diagram-types.md](../skills/diagram/references/diagram-types.md) before drawing.

## Output

- Deliver the diagram as a fenced `mermaid` code block.
- Include a one-line description above the fence (what it shows and when it was generated).
- If the user asks for a file, write to `docs/diagrams/<type>-<slug>.md`.
- Record the diagram to the memory ledger as an `artifact` entry (`pending`) before ending.
