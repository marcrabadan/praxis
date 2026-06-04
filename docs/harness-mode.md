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

systems/
  feature-development/   # artifact-model.md + operating model (doctrine)

workflows/
  registry.json          # the workflow registry
  *.workflow.json        # machine-readable steps + gates + stop conditions

schemas/
  project.schema.json        # PROJECT.md frontmatter shape
  praxis-config.schema.json  # .praxis/config.json shape
  spec.schema.json           # spec.md frontmatter shape
  workflow.schema.json       # workflow manifest shape
  session-state.schema.json  # runtime session-state shape

runtime/
  README.md              # disposable session glue (state files are git-ignored)

tools/
  validate_harness.py    # deterministic harness-state validator
  install_adapter.py     # scaffold .praxis/config.json into a consuming repo
  runtime.py             # read/update runtime session state
```

It does **not** add production application code or a full SDD Kit clone. The
skill factory is unchanged; `/new-feature` and `/review-changes` gain **opt-in**
harness behavior that only activates when a `.praxis/config.json` resolves a
project (otherwise they behave exactly as before). See [`../AGENTS.md`](../AGENTS.md)
for the skill-factory doctrine.

## Per-repo vs central (the authority choice)

The critical design choice is whether Praxis is a **per-repo plugin** or a
**central team harness**. Harness mode is **hybrid, with per-repo (`local`) as
the default and well-paved road**, and central as an opt-in for teams that
outgrow it:

1. **`local` (default).** Project memory lives in the product repo under
   `.praxis/project/`, versioned alongside the code it describes. Zero new
   infrastructure — this matches how Praxis is already installed per repo. Use it
   unless you have a concrete cross-repo need.
2. **`central` (opt-in).** Project memory lives in the harness under
   `projects/<projectId>/`, shared across many repos. Choose it when several
   repos must share decisions, specs, and patterns — and you can run a central
   harness repo.

Each consuming repo declares its choice in `.praxis/config.json` via
`mode: "local"` or `mode: "central"`. **An omitted `mode` is treated as
`local`.** Pick `local` first; move to `central` only when shared cross-repo
memory actually pays for the extra repo to maintain.

## Opting a repo in

Add a `.praxis/config.json` to the consuming repo (see
[`../examples/praxis-config.example.json`](../examples/praxis-config.example.json)
and [`../schemas/praxis-config.schema.json`](../schemas/praxis-config.schema.json)):

```json
{
  "schemaVersion": "1.0.0",
  "harnessRoot": "../praxis",
  "projectId": "example-project",
  "mode": "local",
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
- Every real spec has a `spec.md` with valid frontmatter (slug `id` matching the
  folder, a `title`, `project` matching the owner, a `status` from
  `draft | accepted | superseded | done`).
- Workflow manifests are well-formed and agree with `workflows/registry.json`
  (gates/artifacts reference real steps; ids match file names).
- `runtime/session-state.json`, if present, has a valid shape.
- A `.praxis/config.json` has a valid `schemaVersion`, `harnessRoot`, and a
  well-formed `projectId`. In `central` mode it also checks the project exists in
  the harness; `local` mode (the default) keeps memory in the product repo, so
  there is nothing to resolve against the harness.

CI runs `make validate-harness` and the harness tool tests alongside the skill
validators.

## Workflows, specs, and runtime

- **Workflows** (`workflows/`) are machine-readable lifecycles — steps, gates,
  stop conditions, and validation commands. `feature-development` is
  `spec → plan → tasks → verify`, where each gate is opened by the previous
  artifact reaching an authorizing status. See
  [`../systems/feature-development/artifact-model.md`](../systems/feature-development/artifact-model.md).
- **Specs** are the durable, typed artifacts `/new-feature` writes in harness mode
  under `projects/<project>/specs/<spec>/` (`spec.md`, `plans/`, `tasks/`,
  `decisions/`, `reports/`) — instead of leaving the plan only in chat.
- **Runtime** (`runtime/`) is disposable session glue (last active
  project/repo/spec/command), managed by `tools/runtime.py` and **git-ignored**.
  Durable decisions never live only here — see [`../runtime/README.md`](../runtime/README.md).

## Installing the adapter into a consuming repo

`tools/install_adapter.py` scaffolds the pointer files deterministically:

```sh
python tools/install_adapter.py --target ../checkout --project checkout --mode local
# writes ../checkout/.praxis/config.json + ../checkout/.praxis/current-spec.md
```

The generated Cursor / Codex / IntelliJ entry docs include the same harness
**read order**, so every agent resolves project context the same way.

## Status

Phases 1–8 of the harness conversion are in place: the authority model, project
memory, adapter config + read-order wiring, the harness validator, durable spec
artifacts for `/new-feature`, workflow gates, runtime state, and a project-aware
`/review-changes`. All harness behavior in commands is **opt-in** — it activates
only when a `.praxis/config.json` resolves a project, so non-harness repos are
unaffected.

Deliberately still out of scope (add on evidence, not anticipation): a full SDD
Kit, an `experience` workflow step, and central-mode sync tooling.
