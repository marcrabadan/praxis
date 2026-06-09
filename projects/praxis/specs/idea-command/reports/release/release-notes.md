# Release Notes (plan) — /idea intake & triage command

> **Planning run.** This is the *release plan*, not a shipped release. Gate 4
> (`release-approved`) requires the verify report to show every acceptance
> criterion met **after the build** before this is approved. `idea.md` is not
> written yet — the spec/plan are `draft`/`pending`.

## Summary (planned)

`/idea` — a thin intake & triage front door. Type `/idea <a raw thought>`; it
asks at most 1–2 clarifying questions, classifies the input into one of four
categories (`feature` → `/new-feature`, `bug` → `/fix-bug`, `refinement` →
`/refine`, `not-worth-doing` → no route), records a `pending` note in the memory
ledger (`--source /idea --tags intake,<class>`), and prints the recommended next
command for you to run. It never plans, specs, or auto-runs the lifecycle.

## Acceptance criteria to be met before release

All 15 acceptance criteria in [`../../spec.md`](../../spec.md) (AC-01…AC-15),
proven by the verify report ([`../verify/report.md`](../verify/report.md)) once
the build runs. Exit criteria are defined in [`docs/test-strategy.md`](../../../../../docs/test-strategy.md):
13 static cases + the primary behavioural suite pass, all 15 AC mapped, no open
Critical/High defects, `make catalog-check` + `make integrations-check` clean.

## Versioning (planned)

Adding a user-visible command is a **minor** bump: `plugin-praxis/.claude-plugin/plugin.json`
`1.9.0 → 1.10.0`, plus a `CHANGELOG.md` `[Unreleased] → Added` entry. Bump at
build time, not in this planning run.

## Risks & known limitations

- **Misclassification** at the refinement/feature and bug/refinement boundaries
  (mitigated by ≤2 clarifying questions + recommend-and-confirm: the user sees the
  class before any lifecycle starts).
- **Description collision** with `/new-feature` (mitigated by required wording
  "intake and triage", forbidden "plan a feature"; guarded by TC-S-04/05/10).
- `/idea` is intentionally **absent from the generated codex/intellij
  integrations** (the generator's command list is curated) — a separate product
  call, out of this slice.

## Rollback

Trivial (<5 min): `git revert`, `make catalog` to drop the `/idea` row, confirm
`make catalog-check && make integrations-check`. User-written ledger entries are
data, not code — left intact. Runbook: [`docs/technical-manual.md`](../../../../../docs/technical-manual.md).

## Traceability

- This artifact id: `REL-idea-command` (plan)
- Sources: spec (`SPEC-idea-command`), test-strategy, DevOps runbook
- Closes (on release): `IDEA-idea-command`
