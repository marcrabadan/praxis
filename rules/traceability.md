# Traceability

This is a **harness rule**. It is short and behavior-changing. It defines how
every artifact in a lifecycle stays linked to its origin and its consequences,
so any artifact can answer "where did this come from?" and "what did it lead
to?".

Traceability is layered on the **memory ledger and the artifact files that
already exist** — it is not a separate database. The mechanism is two things: a
typed id in an artifact's frontmatter or header, and `source:` / `traces:` links
recorded on the ledger entry and in the artifact's *Traceability* section.

## Typed ids

Each artifact gets a stable, typed id. Ids are uppercase type + zero-padded
number; the number is unique within its type per project.

| Type | Id prefix | Produced in |
|------|-----------|-------------|
| Idea / request | `IDEA-` | the originating ticket or request |
| Discovery report | `DISC-` | `feature-development` discovery step |
| Research report | `RES-` | `feature-development` research step |
| Specification | `SPEC-` | `feature-development` spec step (the spec folder slug) |
| Requirement | `REQ-` | inside the spec |
| Epic / Story / Task | `EPIC-` / `STORY-` / `TASK-` | PO + tasks |
| Architecture decision | `ADR-` | any role's significant decision |
| Bug | `BUG-` | `bug-fix` triage step |
| Refinement | `REF-` | `refinement` assess step |
| Verify report | `VER-` | verify step |
| Release | `REL-` | `feature-development` release step |

The full feature chain is bidirectional:

```
IDEA → DISC → RES → SPEC → REQ → EPIC → STORY → TASK → ADR → COMMIT → VER → REL
```

`bug-fix` and `refinement` use short chains:

```
BUG  → root-cause → fix-plan (ADR?) → COMMIT → VER
REF  → assessment → refine-plan (ADR?) → COMMIT → VER
```

## The two links

Every artifact records, in its *Traceability* section and on its ledger entry:

- **`source:<id>`** — the artifact(s) it derives from (its upstream). The memory
  ledger already supports `source:` tags; use the typed id.
- **`traces:<id>`** — the artifact(s) it feeds or implements (its downstream).

Together these make the chain navigable in both directions. A commit message
references the `TASK-`/`BUG-`/`REF-` id; a `VER-` report references what it
verifies; a `REL-` closes the `IDEA-`.

## Rules

- **No orphans.** Every artifact past discovery/triage/assess must name at least
  one `source:`. The entry point (idea/bug/refinement) names the originating
  request instead.
- **Ids are stable.** Once assigned, an id never changes. A superseded artifact
  keeps its id and is marked `superseded`, with the successor linking back.
- **Closed status set only.** Artifact/ledger status is drawn from the ledger's
  closed set — `pending | accepted | rejected | superseded | rolled-back` — and
  is never invented (see [source-of-truth.md](source-of-truth.md)).
- **Check it deterministically, don't eyeball it.** Run
  `make validate-traceability` (`tools/validate_traceability.py`) to confirm
  declared links resolve. It is advisory, not a hard CI gate.

## What this is *not*

Not a ticketing system and not a replacement for the ledger or `projects/`
memory. It is the thin id + link convention that turns the existing artifacts
into a navigable chain.
