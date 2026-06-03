# Documentation Formats

Reference for the document types this skill can produce, the source each draws from, and the shape to follow.

---

## Document types

### Architecture Document

**Source:** memory ledger (`decision`, `plan` entries) + codebase exploration  
**When:** broad system overview; onboarding; stakeholder communication  
**Shape:**
```
# <System or Feature> Architecture
> One-line purpose statement

## Overview
## Components / Modules
## Key Decisions (links or inline ADRs)
## Data Flow
## NFRs and Trade-offs
## Open Questions
```

---

### ADR (Architecture Decision Record)

**Source:** a single `decision` entry from the memory ledger  
**When:** formalising an accepted decision that deserves a permanent record  
**Shape:**
```
# ADR-<NNN>: <Short title>

**Status:** Accepted | Proposed | Deprecated | Superseded by ADR-<NNN>  
**Date:** YYYY-MM-DD  
**Deciders:** (roles or names)

## Context
## Decision
## Consequences
## Alternatives Considered
```

Number ADRs sequentially from the existing count in `docs/decisions/`.

---

### API Reference

**Source:** codebase (routes, controllers, handlers, OpenAPI schemas, function signatures)  
**When:** public-facing or internal API documentation  
**Shape (REST):**
```
# <Resource> API

## Endpoints
### GET /resource
**Description:** ...  
**Parameters:** ...  
**Response:** ...  
**Example:** ...
```
**Shape (function/library):**
```
## `functionName(param1, param2)`
**Purpose:** ...  
**Parameters:** ...  
**Returns:** ...  
**Example:** ...
```

---

### Component / Module Guide

**Source:** codebase (directory structure, exports, tests)  
**When:** frontend components, library modules, internal packages  
**Shape:**
```
# <Component / Module>

> One-line purpose

## Usage
## Props / Parameters
## Variants / Modes
## Accessibility notes (if UI)
## Examples
```

---

### Runbook

**Source:** memory ledger (`rollout`, `decision` entries) + codebase (deploy config, scripts)  
**When:** operational procedures — deploy, rollback, on-call response  
**Shape:**
```
# Runbook: <Operation>

**Owner:** ...  
**Last updated:** ...

## When to use this runbook
## Prerequisites
## Steps
## Verification
## Rollback
## Escalation
```

---

### Data Dictionary

**Source:** codebase (schemas, models, migrations, type definitions)  
**When:** documenting entities, fields, and relationships  
**Shape:**
```
# Data Dictionary: <Domain>

## <Entity>
| Field | Type | Required | Description |
|-------|------|----------|-------------|
```

---

### Project README Section

**Source:** memory ledger + codebase  
**When:** updating or generating a README overview, quickstart, or contributing section  
**Shape:** standard Markdown; keep each section scannable and under 20 lines.

---

## Output paths (defaults)

| Type | Default path |
|------|-------------|
| Architecture doc | `docs/architecture/<slug>.md` |
| ADR | `docs/decisions/ADR-<NNN>-<slug>.md` |
| API reference | `docs/api/<resource>.md` |
| Component guide | `docs/components/<name>.md` |
| Runbook | `docs/runbooks/<operation>.md` |
| Data dictionary | `docs/data/<domain>.md` |
| README section | inline or `README.md` |

Always confirm the path with the user if it differs from the default.
