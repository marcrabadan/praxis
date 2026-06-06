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

Each artifact gets a stable, typed id. Two id shapes, chosen so concurrent work
**cannot collide**:

- **Top-level work items use a slug, not a global counter** — `SPEC-<slug>`,
  `BUG-<slug>`, `REF-<slug>` (e.g. `SPEC-live-tracking`). The slug is the folder
  name, so the filesystem/git already guarantees uniqueness. Two people creating
  two specs never race for a number.
- **Sub-ids are numbered, but scoped to their parent spec** — `REQ-001`,
  `TASK-003`, `ADR-002` are unique *within* their spec folder, not globally.
  `REQ-001` in `SPEC-live-tracking` and `REQ-001` in `SPEC-merchant-onboarding`
  are different requirements and never conflict. Reference one from elsewhere with
  the qualified form `SPEC-live-tracking/REQ-001`.

| Type | Id | Produced in |
|------|-----------|-------------|
| Idea / request | `IDEA-<ticket>` | the originating ticket or request |
| Discovery report | `DISC-<slug>` | `feature-development` discovery step |
| Research report | `RES-<slug>` | `feature-development` research step |
| Specification | `SPEC-<slug>` (= the spec folder name) | `feature-development` spec step |
| Requirement | `REQ-<nnn>` (scoped to its spec) | inside the spec |
| Epic / Story / Task | `EPIC-`/`STORY-`/`TASK-<nnn>` (scoped to its spec) | PO + tasks |
| Architecture decision | `ADR-<nnn>` (scoped to its spec) | any role's significant decision |
| Bug | `BUG-<slug>` | `bug-fix` triage step |
| Refinement | `REF-<slug>` | `refinement` assess step |
| Verify report | `VER-<slug>` | verify step |
| Release | `REL-<slug>` | `feature-development` release step |

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

- **One canonical home — never duplicate.** A SPEC and its REQs exist in exactly
  one place: `projects/<project>/specs/<slug>/spec.md`. Other artifacts — tasks in
  any repo, commits, plans, sibling specs — **reference** a requirement by id;
  they never copy its text. A cross-repo feature is **one** spec whose `tasks.md`
  groups tasks by repo, each task carrying `source:REQ-<nnn>`. If you find
  yourself pasting requirement text into a second file, link the id instead.
- **Collision-safe ids (see above).** Top-level items are slug-keyed; sub-ids are
  spec-scoped. Never hand out a global running number that two people could grab
  at once.
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
