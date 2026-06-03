---
description: Generate documentation — a functional manual (for users/stakeholders) and/or a technical manual (for engineers). Just describe what you need, or type /docs with no arguments to generate both.
argument-hint: "[what to document, or leave blank for full docs]"
---

Generate documentation using the `docs` skill.

$ARGUMENTS

## Default behaviour (no arguments)

Generate both the functional and technical manuals. Follow [full](../skills/docs/workflows/full.md).

## Routing from natural language

Read the request above and pick the right scope — no need for exact keywords:

| If the request sounds like… | Use workflow |
|-----------------------------|--------------|
| Users, features, stakeholders, "what it does", user guide, product | [functional](../skills/docs/workflows/functional.md) — BA + PO + UX |
| Engineers, architecture, API, code, ops, deploy, runbook, "how it works" | [technical](../skills/docs/workflows/technical.md) — Architect + Developer + DevOps |
| Both, everything, or unclear | [full](../skills/docs/workflows/full.md) — all experts |

When the scope mentions a specific section ("just the API reference", "only the ADRs"), generate that section only and write it to the appropriate file.

## Domain experts (added automatically when warranted)

The technical workflow adds security, data, or ML/AI experts when the system clearly needs them — no flag required.

## Output

- Files land at `docs/functional-manual.md` and/or `docs/technical-manual.md` unless the user specifies a path.
- Each manual opens with a table of contents.
- Record each file as a `pending` artifact in the memory ledger before ending.
