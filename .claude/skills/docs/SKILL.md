---
name: docs
description: Generate functional and technical manuals by routing each section to the right SDLC expert — BA, Product Owner, and UX for the functional manual; Architect, Developer, and DevOps for the technical one — drawing on the memory ledger and the codebase. Use when the user wants a complete, well-ordered manual, not a one-off answer.
tier: 3
version: 1.0.0
---

# Docs

Generate **well-ordered manuals** — functional and/or technical — by dispatching each section to the SDLC expert who owns that domain. Every expert reads the memory ledger and the codebase before writing, so the manual reflects what was actually decided and built.

The result is a document a team can hand to a new engineer, a QA tester, or a stakeholder — not a dump of raw notes.

## Manual types

### Functional Manual

> *What the system does and how users interact with it.*

Written by: **Business Analyst**, **Product Owner**, **UX/UI Engineer**

Covers:
- Purpose and target users
- Feature catalogue with acceptance criteria
- User journeys and workflows
- Business rules and constraints
- Glossary of domain terms

### Technical Manual

> *How the system is built and how engineers operate it.*

Written by: **Software Architect**, **Developer**, **DevOps Engineer**

Covers:
- System architecture and key design decisions (ADRs)
- Module/component breakdown and their responsibilities
- API reference
- Data model
- Configuration and environment variables
- Deployment, observability, and operational runbooks

### Full Manual

Both manuals combined, with a shared table of contents and cross-links between functional and technical sections.

## When to use

- "Generate the functional manual."
- "Write the technical manual for this service."
- "Document everything — functional and technical."
- "Give me something to hand to a new engineer."
- "Write the user guide / the ops runbook / the API reference."

## When not to use

- The user wants a diagram → use the `diagram` skill.
- The user wants to *record* a new decision → use the `memory` skill.
- The user wants a quick in-chat answer — just answer; don't write a file.

## Workflows

| Mode | File | When |
|------|------|------|
| Functional | [workflows/functional.md](workflows/functional.md) | BA + PO + UX write the user-facing manual |
| Technical | [workflows/technical.md](workflows/technical.md) | Architect + Developer + DevOps write the engineering manual |
| Full | [workflows/full.md](workflows/full.md) | Both manuals in one pass (default when scope is broad) |

## References

- [references/formats.md](references/formats.md) — document types and output shapes
- [references/checklist.md](references/checklist.md) — quality gate before writing any file

## Execution model

Each section is written by the owning expert in its own subagent so doctrine stays isolated and the output is authoritative. The main thread stitches sections into a table of contents and cross-links them.

Every expert receives:
1. The user's request and the manual scope.
2. All accepted ledger entries relevant to their domain.
3. The codebase paths relevant to their section.
4. The outputs of preceding sections (so the technical manual can reference the functional one).

## Output expectations

- One Markdown file per manual (or per section if the user prefers split files).
- Opens with a table of contents linking every section.
- Each section has a clear heading, a one-line purpose, and substantive content sourced from the ledger or code.
- No invented details — every claim is traceable to a ledger entry or a code file.
- A ledger `artifact` entry is recorded for each file produced (`pending`).

## Stop conditions

- The requested manual(s) are written and file paths reported.
- Ledger artifact entries recorded.
- If scope is ambiguous, one clarifying question asked before starting.
