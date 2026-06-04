# Linked Repos

The product repositories this project spans. Each linked repo should declare a
`.praxis/config.json` whose `projectId` matches this project's `id`, and whose
`harnessRoot` points back to this harness.

| Repo | Role | Path / URL | Notes |
|------|------|-----------|-------|
| `<repo-name>` | `<service / web / infra / …>` | `<relative path or git URL>` | |

## How linking works

- A consuming repo opts in by adding `.praxis/config.json` (see
  [`../../schemas/praxis-config.schema.json`](../../schemas/praxis-config.schema.json)).
- `projectId` in that config must equal this project's `id`.
- `harnessRoot` is the path (or pointer) from the product repo to this harness.
- The harness validator checks that every path declared here is recorded; it does
  not reach into external repos.

Keep this list current — an undeclared linked repo is a stop condition for work
that crosses repo boundaries (see [`../../rules/stop-conditions.md`](../../rules/stop-conditions.md)).
