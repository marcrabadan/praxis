# Source of Truth

This is a **harness rule**. It is short and behavior-changing. It defines what is
canonical, what is generated, what is runtime state, and where durable decisions
and production code live. Procedures belong in skills and workflows; authority
lives here.

Read this before editing anything. Praxis **always runs in harness mode** — if a
repo has no `.praxis/config.json`, the harness auto-bootstraps one
(`tools/ensure_harness.py`) rather than running without it. See
[../docs/harness-mode.md](../docs/harness-mode.md) for the read order and how
bootstrap works.

## What praxis (the harness) owns

The harness owns **durable agent context and doctrine**, not product code:

- `AGENTS.md` — the root operating instructions.
- `rules/` — durable, behavior-changing constraints (this file, stop-conditions,
  and any future rule). Constraints, not procedures.
- `.claude/skills/` — reusable execution methods (the meta-skill + SDLC experts +
  memory ledger).
- `.claude/commands/` — thin, user-facing entry points that route into skills.
- `.claude/factory/` — skill-authoring doctrine, templates, schemas, validators.
- `schemas/` — JSON shapes for harness artifacts (project, praxis-config, …).
- `tools/` — deterministic harness validators and scripts.
- `projects/` — **project memory**: durable per-project state, decisions,
  accepted patterns, previous failures, and specs (see harness-mode doc).

The harness may contain examples, fixtures, generators, validators, patches, and
reports. It must **not** contain production application code.

## What product repos own

Product (consuming) repos own their **source code, tests, build config, and
runtime assets**. They opt into the harness with a small pointer:

- `.praxis/config.json` — adapter config (which harness, which project, active
  spec). Validated by [../schemas/praxis-config.schema.json](../schemas/praxis-config.schema.json).
- `.praxis/current-spec.md` — optional human-readable pointer to the active spec.
- Optionally `.praxis/project/` — project memory kept *in the product repo* when a
  team runs per-repo rather than central mode.

A product repo never duplicates the full harness. The harness never owns the
product's code.

## What generated integrations own

Generated files (`integrations/cursor/`, `integrations/codex/`,
`integrations/intellij/`, `SKILLS.md`) own **nothing canonical**. They are
reproducible projections of `.claude/`. They point to authority; they never
become authority. Every generated file declares its source and the command that
regenerates it, and CI fails when they are stale (`make integrations-check`,
`make catalog-check`).

## What is runtime state

Runtime state (last active project, last active repo, recent command runs,
adapter install events) is **disposable session glue**, never durable doctrine.
Major decisions are never stored only in runtime. (The runtime layer is a later
phase; today, durable decisions live in the memory ledger and in `projects/`.)

## Where product decisions live

Durable decisions live in **project memory** with a lifecycle status:

- Per-project decisions: `projects/<project>/memory/decisions/` and the project's
  `current-state.md` / `open-questions.md`.
- Cross-cutting and snapshot-able changes: the **memory ledger** under
  `.praxis/memory/` (see [../.claude/skills/memory/](../.claude/skills/memory/)).

Decision status comes from one **closed set** — `pending`, `accepted`,
`rejected`, `superseded`, `rolled-back` — and is never invented. **Pending means
recorded, not authorized**: an agent may record a proposed decision but must not
execute the work it authorizes until the user accepts it.

## Where production code lives

In product repos. Never here.

## Authority order

When sources conflict, follow this order (highest first):

1. Explicit user instruction (in the current session).
2. Project constitution (`projects/<project>/PROJECT.md` authority notes).
3. Accepted project decisions (status `accepted`).
4. The active spec or plan.
5. Harness rules (`rules/`) and skill doctrine (`.claude/factory/ai/`).
6. Repo-local governance in the product repo.
7. Existing code.

Convenience files — generated adapters, local prompts, command wrappers — point
to authority. They are never themselves authority.
