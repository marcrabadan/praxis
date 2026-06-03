# Workflow — Functional Manual

Generate the functional manual by routing each section to the right expert: Business Analyst, Product Owner, and UX/UI Engineer.

## When you reach here

The user wants documentation that describes *what* the system does and *how users interact with it* — not how it is built. Audience: product stakeholders, QA testers, support teams, new users.

## Steps

### 1. Gather shared context (once, cheap)

Run in parallel:

```bash
# Memory ledger — all accepted entries
python .claude/skills/memory/scripts/ledger.py list --status accepted

# Codebase top-level orientation
find . -maxdepth 2 -name "README*" -o -name "*.md" -path "*/docs/*" | head -20
ls -la
```

Condense into a short **context digest**: product name, target users, main features, key constraints. This digest goes into every expert subagent.

### 2. Dispatch expert subagents in order

Each phase builds on the previous artifact. Run serially unless phases are truly independent.

---

#### Phase 1 — Business Analyst

Subagent prompt (pass the context digest and all accepted ledger entries):

> Adopt the `business-analyst` skill. Write the **Requirements and Feature Catalogue** section of a functional manual.
>
> Include:
> - Product purpose and target users (one paragraph)
> - Functional requirements as a numbered list
> - Feature catalogue: for each feature, one row in a table (Feature | Description | User benefit | Acceptance criteria summary)
> - Business rules and constraints (numbered list)
> - Open questions / known gaps
>
> Source everything from the ledger entries and codebase provided. Do not invent requirements. Return only the Markdown section — no preamble.

---

#### Phase 2 — Product Owner

Subagent prompt (pass context digest + BA artifact):

> Adopt the `product-owner` skill. Write the **User Journeys and Workflows** section of a functional manual.
>
> Include:
> - The 3–5 most important user journeys as numbered step lists (trigger → steps → outcome)
> - A prioritised feature table (MoSCoW or WSJF) if the ledger contains prioritisation decisions
> - Definition of Done for the current scope
>
> Ground every journey in the BA feature catalogue above. Return only the Markdown section.

---

#### Phase 3 — UX/UI Engineer (conditional)

Add this phase only if the product has a user interface. Subagent prompt (pass context digest + BA + PO artifacts):

> Adopt the `ux-ui-engineer` skill. Write the **User Interface Guide** section of a functional manual.
>
> Include:
> - Key screens / pages and their purpose (table: Screen | Purpose | Key actions)
> - Navigation model (how users move between screens)
> - Accessibility notes (keyboard navigation, ARIA, colour contrast requirements)
> - Any UX constraints or design principles established in the ledger
>
> Return only the Markdown section.

---

### 3. Stitch into the manual

Assemble the sections into one file:

```markdown
# <Product Name> — Functional Manual

> Generated: <date> | Source: memory ledger + codebase

## Table of Contents

1. [Purpose and Users](#1-purpose-and-users)
2. [Feature Catalogue](#2-feature-catalogue)
3. [Business Rules](#3-business-rules)
4. [User Journeys](#4-user-journeys)
5. [User Interface Guide](#5-user-interface-guide) ← if applicable
6. [Glossary](#6-glossary)
7. [Open Questions](#7-open-questions)

---

<!-- paste BA artifact here -->
<!-- paste PO artifact here -->
<!-- paste UX artifact here -->

---

## 6. Glossary

<!-- Extract domain terms from BA artifact and define them -->

## 7. Open Questions

<!-- Collect open questions flagged by each expert -->
```

Write the assembled file to `docs/functional-manual.md` (or user-specified path).

### 4. Record to the ledger

```bash
python .claude/skills/memory/scripts/ledger.py log \
  --type artifact \
  --title "Functional Manual: <product name>" \
  --source /docs \
  --tags docs,manual,functional \
  --body "Functional manual written by BA + PO + UX subagents. Sources: ledger entries <ids>. Path: docs/functional-manual.md."
```

### 5. Report

State the file path, the sections produced, which experts were used, and any sections skipped (with the reason).
