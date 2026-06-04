# Harness Mode (experimental)

Praxis began as a **skill factory + SDLC expert pack + memory ledger + generated
integrations**. Harness mode is the first step toward a fuller **agent harness**:
a reliable operating environment that tells an agent where to read first, where
source of truth lives, where durable decisions go, how project context is
resolved, and when to stop and ask.

This is intentionally a **small first layer**. It adds the *authority model* —
projects, source-of-truth rules, stop conditions, adapter config, and a
deterministic validator — without changing any existing skill, command, or
`/new-feature`. Everything else (workflow gates, durable spec artifacts, runtime
state) builds on this and lands later.

## What harness mode adds

```
rules/
  source-of-truth.md     # what is canonical / generated / runtime; authority order
  stop-conditions.md     # when the agent must stop and ask

projects/
  projects-index.md      # the project registry
  _template/             # copy this to start a project
    PROJECT.md
    linked-repos.md
    memory/current-state.md
    memory/open-questions.md

schemas/
  project.schema.json        # PROJECT.md frontmatter shape
  praxis-config.schema.json  # .praxis/config.json shape

tools/
  validate_harness.py    # deterministic harness-state validator
```

It does **not** add production code, a full SDD Kit, or any change to the skill
factory. See [`../AGENTS.md`](../AGENTS.md) for the skill-factory doctrine, which
is unchanged.

## Per-repo vs central (the authority choice)

The critical design choice is whether Praxis is a **per-repo plugin** or a
**central team harness**. Harness mode supports a **hybrid**:

1. Praxis stays installable per repo (as today).
2. Teams can optionally run a central harness that governs many repos.
3. Each consuming repo declares a `.praxis/config.json` that points at either
   local or central project memory (`mode: "local"` or `mode: "central"`).

Project memory (`projects/<project>/`) lives in the harness in central mode, or
in the product repo under `.praxis/project/` in local mode.

## Opting a repo in

Add a `.praxis/config.json` to the consuming repo (see
[`../examples/praxis-config.example.json`](../examples/praxis-config.example.json)
and [`../schemas/praxis-config.schema.json`](../schemas/praxis-config.schema.json)):

```json
{
  "schemaVersion": "1.0.0",
  "harnessRoot": "../praxis",
  "projectId": "example-project",
  "mode": "central",
  "activeSpec": null
}
```

If `projectId` cannot be resolved to a project, the agent **stops** (see
[`../rules/stop-conditions.md`](../rules/stop-conditions.md)).

## Read order (harness mode)

When a repo is in harness mode, read in this order before editing:

1. Repo `AGENTS.md`
2. `.praxis/config.json`
3. Praxis harness `AGENTS.md`
4. `rules/source-of-truth.md`
5. `projects/<project>/PROJECT.md`
6. `projects/<project>/memory/current-state.md`
7. `projects/<project>/memory/open-questions.md`
8. Active spec artifacts (when the spec layer lands)
9. Relevant skills or workflows

A later phase generates this block into each adapter (Codex/Cursor/IntelliJ/Claude)
so the order is enforced, not just documented.

## Starting a project

```sh
cp -r projects/_template projects/<your-project-id>
# edit PROJECT.md (set id = folder name), linked-repos.md, memory/*
# add a row to projects/projects-index.md
make validate-harness
```

## Validating

The validator is deterministic — no LLM. It checks the project registry, the
required project-memory files, the schemas, and (optionally) a consuming repo's
config:

```sh
make validate-harness                                  # this harness
python tools/validate_harness.py --config path/.praxis/config.json
```

It enforces:

- `schemas/` exist and are valid JSON.
- `projects/projects-index.md` and `projects/_template/` exist with the required
  files.
- Every real project has `PROJECT.md` (valid frontmatter: slug `id` matching the
  folder name, a `name`, a `status` from the closed set `active | paused |
  archived`), `linked-repos.md`, and `memory/current-state.md` +
  `open-questions.md`.
- Disk projects and `projects-index.md` agree (no ghosts, no unlisted folders).
- A `.praxis/config.json` has a valid `schemaVersion`, `harnessRoot`, and a
  resolvable `projectId` (central mode checks the project exists in the harness).

CI runs `make validate-harness` alongside the skill validators.

## Status

This is **phase 1** of the harness conversion. Deliberately out of scope for now:

- Migrating `/new-feature` to write durable spec artifacts.
- Workflow manifests and gates.
- Runtime/session state.
- Any change to existing skills.

Those phases build on this authority model. Make the authority model real first.
