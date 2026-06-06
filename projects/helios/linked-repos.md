# Linked Repos

The four repositories the **Helios** product spans. They sit side by side under a
common parent folder, with the harness (`praxis`) as a sibling:

```
workspace/
  praxis/          # this harness (central) — shared memory, specs, rules, workflows
  helios-api/      # backend  · core REST/GraphQL API (owns openapi.yaml — canonical)
  helios-workers/  # backend  · async jobs: dispatch, ETA, notifications
  helios-web/      # frontend · customer-facing delivery tracking app (owns design tokens)
  helios-console/  # frontend · internal ops/admin console
```

| Repo | Role | Path (from harness) | Notes |
|------|------|---------------------|-------|
| `helios-api` | backend / service | `../helios-api` | Owns `openapi.yaml` — the canonical API contract. |
| `helios-workers` | backend / workers | `../helios-workers` | Consumes the API contract + the event schema. |
| `helios-web` | frontend / web | `../helios-web` | Owns the design tokens; consumes the API contract. |
| `helios-console` | frontend / admin | `../helios-console` | Consumes tokens + API contract. |

## How each repo opts in (central mode)

Every repo carries the **same** `.praxis/config.json` except its own identity is
irrelevant — what matters is they all resolve the **same** harness and project:

```jsonc
// helios-api/.praxis/config.json  (identical in all four repos)
{
  "schemaVersion": "1.0.0",
  "harnessRoot": "../praxis",   // path from this repo to the harness
  "projectId": "helios",         // must equal this project's id
  "mode": "central",             // memory lives in the harness, shared by all repos
  "activeSpec": null              // set to the active spec slug while working one
}
```

Ready-to-copy configs and a walkthrough live at
[`../../examples/multi-repo/`](../../examples/multi-repo/README.md).

## How linking works

- `projectId` in each repo's config equals this project's `id` (`helios`).
- `harnessRoot` is the relative path from that repo to this harness (`../praxis`).
- `mode: central` keeps specs/decisions/memory **here**, so a feature that crosses
  `helios-api` + `helios-web` is specified once and stays consistent.
- The harness validator checks that paths declared here are recorded; it does not
  reach into the external repos.

Keep this list current — an undeclared linked repo is a stop condition for work
that crosses repo boundaries (see
[`../../rules/stop-conditions.md`](../../rules/stop-conditions.md)).
