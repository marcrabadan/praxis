# Feature development

The lifecycle that `/new-feature` drives. This doc is the **operating model**;
the machine-readable gates live in
[`../../workflows/feature-development.workflow.json`](../../workflows/feature-development.workflow.json)
and the artifact shapes in [`artifact-model.md`](artifact-model.md).

## Two modes

`/new-feature` adapts to the repo:

- **Plan mode (default, no harness):** runs the SDLC experts and returns a
  consolidated plan, writing `docs/` files and recording entries to the memory
  ledger. Behavior unchanged from before harness mode.
- **Harness mode (a `.praxis/config.json` resolves a project):** *additionally*
  writes durable, typed spec artifacts under
  `projects/<project>/specs/<spec>/`, following the `spec → plan → tasks → verify`
  workflow and respecting its gates. Chat output becomes a summary; the
  artifacts are the source of truth.

## The thin-command principle

The command routes; it does not own lifecycle doctrine forever:

```
commands/new-feature.md
  -> workflows/feature-development.workflow.json   (gates & transitions)
  -> systems/feature-development/                  (this doctrine + artifact model)
  -> skills/<SDLC expert>                          (the work)
```

## Stop conditions

In addition to [`../../rules/stop-conditions.md`](../../rules/stop-conditions.md),
this workflow stops when: the spec's scope or target user is ambiguous; the plan
would adopt an architecture the project has not used; or a gate's required
decision is still `pending`. Recording a proposal is allowed; acting on it before
acceptance is not.
