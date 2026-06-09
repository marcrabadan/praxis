---
description: Review the current changes (diff) by routing to the right SDLC experts and returning didactic, severity-tagged findings. Use to catch bad practices before a PR merges — locally or in CI — with feedback a junior can learn from and a senior can skim.
argument-hint: "[optional: a git ref/range, path, or PR focus — defaults to the working diff vs the base branch]"
---

Review the code changes below as a team of SDLC experts. The goal is to **catch bad practices early and help the author improve**, not to gatekeep. Calibrate so a **junior learns** from each finding, a **senior can skim by severity**, and an **architect sees the team's standards being enforced**.

Scope of the review:

$ARGUMENTS

## Step 0 — Get the diff

Determine what changed. If `$ARGUMENTS` names a ref/range/path, use it; otherwise review the working diff against the base branch:

```bash
git fetch -q origin 2>/dev/null || true
base=$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD main 2>/dev/null || echo HEAD~1)
git diff --stat "$base"...HEAD
git diff "$base"...HEAD
```

Read the surrounding code of each change before judging it — a diff line is not enough context. If there is nothing to review, say so and stop.

## Step 1 — Route to the relevant experts

Pick **only** the experts the diff actually warrants (do not run all of them by reflex). Load each chosen skill and apply its `references/checklist.md`:

| If the change touches… | Consult |
| ---------------------- | ------- |
| Application/library code, logic, refactors, error handling | **`developer`** |
| Public interfaces, module boundaries, new dependencies, data models, cross-cutting/performance/security-significant decisions | **`software-architect`** |
| Tests, or code that lacks tests it should have | **`qa-engineer`** |
| CI/CD, IaC, Dockerfiles, deploy/release config, observability | **`devops-engineer`** |
| Authentication/authorization, input handling, crypto, secrets, dependencies, or any code with an abuse/vulnerability risk | **`security-engineer`** |
| Trust boundaries, identity/data-protection design, segmentation, encryption strategy, or compliance-significant architecture | **`cybersecurity-architect`** |
| Frontend framework/rendering/state/routing/build architecture, design-system structure, or Core Web Vitals budgets | **`frontend-architect`** |
| UI components, hooks, client/server state, forms, styling, frontend TypeScript, re-render/performance, accessibility implementation, or component/E2E tests | **`frontend-engineer`** |
| Design tokens, visual/interaction design, accessibility criteria (WCAG), responsive layout, usability, UX writing, or design fidelity | **`ux-ui-engineer`** |
| Requirements/acceptance behavior that the diff seems to contradict | **`business-analyst`** |

Always run the `developer` checklist on code changes as the baseline. Add others by the table above.

## Step 1.5 — Harness mode: review against project standards

Praxis **always runs in harness mode**. Ensure the harness is initialized with `python tools/ensure_harness.py` (idempotent; auto-bootstraps a project from the repo if none resolves), then load the project's context *before* judging the diff, so the review enforces **this team's** standards rather than only generic best practice:

- **Authority & rules.** Read the project's `PROJECT.md` authority notes and the harness `rules/source-of-truth.md` + `rules/stop-conditions.md`.
- **Accepted decisions.** Load the project's *accepted* decisions — `projects/<projectId>/memory/decisions/` and `accepted` entries in the memory ledger. A diff that contradicts an accepted decision is at least a **🟠 Should-fix**; cite the decision by id/title.
- **Active spec.** If `config.activeSpec` is set, load that spec and check the diff against its acceptance criteria; flag drift from the spec.
- **Stop condition:** if the diff plainly contradicts an accepted decision or the active spec, surface that explicitly in the verdict rather than quietly approving.

When recording any durable outcome from the review (an agreed standard, an accepted risk), record it **only as a `pending` memory entry** (`--source /review-changes`) — review proposes, it does not authorize. The user accepts it. Never auto-accept.

## Step 2 — Output: didactic, severity-tagged findings

Group findings by severity. For **each** finding use this shape:

- **[severity] file:line — short title**
  - **What:** the bad practice or risk, in one sentence.
  - **Why it matters:** the consequence and the principle behind the rule (this is the teaching part — never skip it; cite the expert checklist item, e.g. "Developer checklist: error handling").
  - **Fix:** a concrete, minimal change (a snippet or a precise instruction).

Severity scale:

- **🔴 Blocker** — correctness, security, or data-loss risk; must fix before merge.
- **🟠 Should-fix** — a real bad practice or maintainability problem; fix before merge unless explicitly deferred.
- **🟡 Nit** — style/clarity/learning point; optional, but valuable for a junior.

End with a short **Verdict**: `Approve`, `Approve with nits`, or `Changes requested`, plus a one-line summary and the list of experts consulted. If the diff is clean, say so plainly — do not invent findings to look thorough.

## Notes

- This is a **review**, not an implementation. Propose fixes; apply them only if the user asks.
- Stay within the diff and its immediate context; do not review or refactor unrelated code.
- This differs from a generic code review by routing to **your team's** SDLC expert checklists and explaining the *why* so it doubles as on-the-job teaching.
- **Memory:** if the review surfaces a durable decision (e.g. an agreed standard or an accepted risk), record it in the memory ledger via the `memory` skill (`--source /review-changes`). If you go on to apply fixes at the user's request, capture them with `snapshot` so they can be rolled back.
