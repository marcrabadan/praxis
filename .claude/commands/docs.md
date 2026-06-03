---
description: Generate a functional manual (what the system does, for users and stakeholders) or a technical manual (how it is built and operated, for engineers) by routing each section to the right SDLC expert. Both manuals draw from the memory ledger and the codebase.
argument-hint: "[functional|technical|full] [optional scope or topic]"
---

Generate documentation using the `docs` skill.

Request:

$ARGUMENTS

## How to handle it

Load the `docs` skill and pick the workflow based on the request:

| If the user asks for… | Use workflow |
|-----------------------|--------------|
| "functional", "user guide", "feature docs", "what it does", "stakeholder doc" | [functional](../skills/docs/workflows/functional.md) — BA + PO + UX |
| "technical", "architecture", "API reference", "ops", "runbook", "engineering manual" | [technical](../skills/docs/workflows/technical.md) — Architect + Developer + DevOps |
| "everything", "full", "all docs", no qualifier given | [full](../skills/docs/workflows/full.md) — all experts, both manuals |

If the request names a specific expert or section (e.g. "have the architect write the ADRs", "QA section of the technical manual"), call that expert directly and fold the output into the appropriate manual section.

## Specialist routing

Add domain experts to the technical manual when the system warrants them:

| System has… | Add |
|-------------|-----|
| Auth, crypto, untrusted input, secrets | `security-engineer` |
| Data pipelines, warehouse, ETL | `data-engineer` |
| ML models, LLMs, RAG | `ml-ai-engineer` |

## Output

- Write files to `docs/functional-manual.md` and/or `docs/technical-manual.md` (or user-specified paths).
- Each manual opens with a table of contents.
- Record each file as an `artifact` entry in the memory ledger (`pending`) before ending.
- Report file paths, experts used, and ledger entries recorded.
