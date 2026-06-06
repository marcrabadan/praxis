# Harness Mode (experimental)

Praxis began as a **skill factory + SDLC expert pack + memory ledger + generated
integrations**. Harness mode is the first step toward a fuller **agent harness**:
a reliable operating environment that tells an agent where to read first, where
source of truth lives, where durable decisions go, how project context is
resolved, and when to stop and ask.

It carries two layers. The *authority model* — projects, source-of-truth rules,
stop conditions, adapter config, and a deterministic validator — and the
*delivery lifecycle* on top of it: machine-readable workflows with human-in-the-loop
gates, durable typed artifacts, bidirectional traceability, and runtime state.
The feature lifecycle runs `discovery → research → spec → plan → tasks → build →
verify → release`; lighter `bug-fix` and `refinement` lifecycles handle corrective
and quality-only work. All of it is **opt-in** — it activates only when a
`.praxis/config.json` resolves a project, so non-harness repos are unaffected.

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

rules/
  traceability.md        # typed ids + source:/traces: links (the chain)

systems/
  feature-development/   # full lifecycle doctrine (discovery → … → release)
  bug-fix/               # corrective lifecycle doctrine
  refinement/            # behavior-preserving lifecycle doctrine

workflows/
  registry.json          # the workflow registry
  feature-development.workflow.json   # discovery → research → spec → plan → tasks → build → verify → release
  bug-fix.workflow.json               # triage → reproduce → diagnose → fix → verify
  refinement.workflow.json            # assess → plan → change → verify
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
skill factory is unchanged; `/new-feature`, `/fix-bug`, `/refine`, and
`/review-changes` gain **opt-in** harness behavior that only activates when a
`.praxis/config.json` resolves a project (otherwise they behave exactly as
before). See [`../AGENTS.md`](../AGENTS.md) for the skill factory doctrine.

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

**Multiple repos for one product → one project, central mode.** A product split
across several repos (e.g. two backend + two frontend) is **one** project whose
specs, decisions, and memory live centrally in the harness, with each repo
carrying the same `projectId` and `mode: central`. A worked example —
the fictional **Helios** product across four repos — lives at
[`../projects/helios/`](../projects/helios/PROJECT.md) with copy-ready configs and
a walkthrough at [`../examples/multi-repo/`](../examples/multi-repo/README.md).
Split into multiple projects only when the repos are genuinely independent
products.

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
  stop conditions, and validation commands. Each gate is opened by the previous
  artifact reaching an authorizing status, and **pending is not approval**.
  - `feature-development`: `discovery → research → spec → plan → tasks → build →
    verify → release`, with four human-in-the-loop gates — **Discovery &
    Research**, **Specification**, **Architecture** (only when a significant
    decision exists), and **Release**. Research must precede the spec. Doctrine:
    [`../systems/feature-development/artifact-model.md`](../systems/feature-development/artifact-model.md).
  - `bug-fix`: `triage → reproduce → diagnose → fix → verify` — corrective work,
    no discovery/research/spec chain. Doctrine:
    [`../systems/bug-fix/artifact-model.md`](../systems/bug-fix/artifact-model.md).
  - `refinement`: `assess → plan → change → verify` — quality-only,
    behavior-preserving. Doctrine:
    [`../systems/refinement/artifact-model.md`](../systems/refinement/artifact-model.md).
- **Specs** are the durable, typed artifacts `/new-feature` writes in harness mode
  under `projects/<project>/specs/<spec>/` (`discovery/`, `research/`, `spec.md`,
  `plans/`, `tasks/`, `decisions/`, `reports/verify/`, `reports/release/`) —
  instead of leaving the plan only in chat. `/fix-bug` writes under
  `projects/<project>/bugs/<id>/` and `/refine` under
  `projects/<project>/refinements/<id>/`.
- **Traceability** (`rules/traceability.md`) gives every artifact a typed id
  (`DISC-`, `RES-`, `SPEC-`, `ADR-`, `BUG-`, `REF-`, `VER-`, `REL-`, …) and
  `source:` / `traces:` links, so the chain `IDEA → DISC → RES → SPEC → … → REL`
  is navigable both ways. Check it with `make validate-traceability` (advisory).
- **Runtime** (`runtime/`) is disposable session glue (last active
  project/repo/spec/command), managed by `tools/runtime.py` and **git-ignored**.
  Durable decisions never live only here — see [`../runtime/README.md`](../runtime/README.md).

## Trying harness mode end to end

You can exercise the whole loop in a few minutes. Two ways to run it:

**A. Inside praxis itself (quickest — no second repo).**

```sh
# 1. Scaffold a project under the harness
cp -r projects/_template projects/checkout
#    edit projects/checkout/PROJECT.md  → frontmatter id: checkout, set name + status: active
#    add a row for `checkout` to projects/projects-index.md
make validate-harness                  # must pass

# 2. Add a repo-root .praxis/config.json pointing at this harness
cat > .praxis/config.json <<'JSON'
{ "schemaVersion": "1.0.0", "harnessRoot": ".", "projectId": "checkout", "mode": "central", "activeSpec": null }
JSON

# 3. Drive a lifecycle from your agent
#    /new-feature "saved payment methods at checkout"
#      → writes projects/checkout/specs/<slug>/ : discovery/ → research/ → spec.md → plans/ → tasks/ → reports/
#    /fix-bug "totals wrong when a coupon is removed"
#      → writes projects/checkout/bugs/<id>/
#    /refine "extract the pricing calculator, no behavior change"
#      → writes projects/checkout/refinements/<id>/
```

**B. From a product repo (the realistic setup).**

```sh
python tools/install_adapter.py --target ../checkout --project checkout --mode local
#    writes ../checkout/.praxis/config.json + .praxis/current-spec.md
#    open ../checkout in your agent and run /new-feature, /fix-bug, or /refine
```

**What to watch for** (this is the methodology working):

- **Discovery and research come first.** `/new-feature` writes `discovery/` and
  `research/` and pauses at **Gate 1** before writing `spec.md`. It will not
  guess a spec.
- **Gates hold.** The spec stays `status: draft` and the plan stays a `pending`
  ledger decision until *you* accept them. Pending never opens the next gate.
- **Stop conditions fire.** If `projectId` doesn't resolve, or an open question
  gates the step, the agent stops and asks instead of guessing.
- **Everything is traceable.** Run `make validate-traceability` to confirm the
  `source:`/`traces:` ids resolve, and `make validate-harness` to confirm the
  project/spec/workflow shapes are well-formed.

## Installing the adapter into a consuming repo

`tools/install_adapter.py` scaffolds the pointer files deterministically:

```sh
python tools/install_adapter.py --target ../checkout --project checkout --mode local
# writes ../checkout/.praxis/config.json + ../checkout/.praxis/current-spec.md
```

The generated Cursor / Codex / IntelliJ entry docs include the same harness
**read order**, so every agent resolves project context the same way.

## Status

The harness conversion is in place: the authority model, project memory, adapter
config + read-order wiring, the harness validator, the full `feature-development`
lifecycle (discovery → research → spec → plan → tasks → build → verify → release)
with four HITL gates, the lighter `bug-fix` and `refinement` lifecycles
(`/fix-bug`, `/refine`), bidirectional traceability, runtime state, and a
project-aware `/review-changes`. All harness behavior in commands is **opt-in** —
it activates only when a `.praxis/config.json` resolves a project, so non-harness
repos are unaffected.

Deliberately still out of scope (add on evidence, not anticipation): a full SDD
Kit, an `experience` workflow step, and central-mode sync tooling.
