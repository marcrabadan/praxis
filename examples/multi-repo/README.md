# Working across multiple repos (central mode)

This example shows how to run praxis as a **central harness** for a product split
across several repositories — here the fictional **Helios** product: two backend
repos and two frontend repos that share one project memory.

The matching project lives at [`../../projects/helios/`](../../projects/helios/PROJECT.md).

## When to use central mode

| You have… | Use |
|-----------|-----|
| One repo, memory versioned next to its code | **`local`** (default) |
| Several repos that share specs, decisions, and patterns (one product) | **`central`** ← this example |

Multiple repos for **one product** → one **project**, central mode. Multiple
**independent** products → one project each (still can be central).

## Folder layout

Put the harness and the product repos side by side under a common parent:

```
workspace/
  praxis/          # the harness (this repo), cloned once
  helios-api/      # backend  · core API (owns openapi.yaml)
  helios-workers/  # backend  · async jobs
  helios-web/      # frontend · customer app (owns design tokens)
  helios-console/  # frontend · admin console
```

## 1. Create the project in the harness (once)

```sh
cd praxis
cp -r projects/_template projects/helios
#  edit projects/helios/PROJECT.md       → id: helios, name, status: active
#  edit projects/helios/linked-repos.md  → list the 4 repos
#  add a row for `helios` to projects/projects-index.md
make validate-harness
```

(Already done for you in this repo — `projects/helios/` is the worked example.)

## 2. Point each repo at the harness (once per repo)

Drop the **same** `.praxis/config.json` into each repo. The four files in this
folder are ready to copy:

- [`helios-api.config.json`](helios-api.config.json)
- [`helios-workers.config.json`](helios-workers.config.json)
- [`helios-web.config.json`](helios-web.config.json)
- [`helios-console.config.json`](helios-console.config.json)

```sh
cp examples/multi-repo/helios-api.config.json     ../helios-api/.praxis/config.json
cp examples/multi-repo/helios-workers.config.json ../helios-workers/.praxis/config.json
cp examples/multi-repo/helios-web.config.json     ../helios-web/.praxis/config.json
cp examples/multi-repo/helios-console.config.json ../helios-console/.praxis/config.json
```

Or scaffold each deterministically:

```sh
python tools/install_adapter.py --target ../helios-api     --project helios --mode central
python tools/install_adapter.py --target ../helios-workers --project helios --mode central
python tools/install_adapter.py --target ../helios-web     --project helios --mode central
python tools/install_adapter.py --target ../helios-console --project helios --mode central
```

Validate any repo's config against the harness:

```sh
python tools/validate_harness.py --config ../helios-api/.praxis/config.json
```

## 3. Work day to day

Open **any** of the four repos in your agent. Because each carries
`.praxis/config.json`, the agent resolves the same harness + project and reads
the shared context first (PROJECT.md → current-state.md → open-questions.md → the
active spec).

- **A cross-repo feature** (e.g. "live delivery tracking" touches `helios-api`,
  `helios-workers`, and `helios-web`): run `/new-feature` from any repo. It writes
  **one** spec under `projects/helios/specs/<slug>/`, and the implementation plan
  + `tasks.md` group tasks **by repo**. You then implement each group in its repo,
  all tracing back to the one spec.
- **A bug** in a single repo: run `/fix-bug` from that repo → `projects/helios/bugs/<id>/`.
- **A refinement**: run `/refine` → `projects/helios/refinements/<id>/`.

Because memory is central, a decision recorded while working `helios-api` (say,
"ETAs are computed in `helios-workers`, not the API") is visible when you next
open `helios-web`. The API contract stays canonical, so frontend and backend
agents agree on shapes.

## Syncing across machines & team (option A)

Keep it simple: **don't version the `workspace/` parent.** Each of the five repos
(the harness + the four products) is its own git repo, cloned side by side.

- **Standardize the layout** so the relative `harnessRoot: ../praxis` resolves the
  same for everyone. (Don't put absolute paths in the committed config — they
  differ per machine.)
- **The harness `praxis` is the shared repo.** It carries the central project
  memory (`projects/helios/`: specs, decisions, current-state). Syncing the team
  = pushing/pulling `praxis`. Branch and PR it like any shared repo.
- **Don't nest git repos.** A parent that is itself a git repo and merely contains
  child `.git` repos causes "embedded repository" problems. Option A avoids this
  by leaving the parent unversioned. (If you ever need one-clone reproducibility,
  switch to submodules — not needed here.)
- `runtime/` (last active project/repo/spec) is **git-ignored** — per-machine,
  never synced. Durable memory is in `projects/`, which **is** committed.

For working **concurrently** — several people on one repo, or several teams across
repos, without mixing or duplicating SPEC/REQ — see
[**Working as a team**](../../docs/teamwork.md). The essentials:

- **One canonical spec.** A cross-repo feature is **one** spec under
  `projects/helios/specs/<slug>/`; tasks reference `REQ-` ids, never copy them.
- **The spec folder is the unit of parallelism** — one spec, one owner at a time;
  different specs = different folders = no conflict.
- **`activeSpec` stays per-session** (in git-ignored runtime), so people sharing a
  repo don't churn the committed config:
  `python tools/runtime.py set --project helios --repo helios-api --spec <slug>`.

## Why one project, not four

Four projects would fragment the memory the repos must share — the API contract,
the design tokens, cross-cutting decisions, the "don't repeat this failure"
notes. One project in central mode keeps a cross-repo feature consistent and lets
any repo's agent see the whole picture. Split into multiple projects only when the
repos are genuinely independent products.
