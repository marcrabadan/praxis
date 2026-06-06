# Working as a team with praxis

How praxis stays viable from **one developer** up to **several teams of 3+**
working the same repo or several repos at once — without mixing or duplicating
specs and requirements.

It builds on [harness mode](harness-mode.md) and the
[multi-repo example](../examples/multi-repo/README.md). The short version:

> **git coordinates the code. praxis coordinates the intent.** The spec is the
> single source of truth; the spec *folder* is the unit of parallel work; ids are
> collision-safe; durable decisions land as one-file-per-decision so concurrent
> work rarely conflicts.

## Layout (option A) — repos side by side, harness shared

```
workspace/                 # just a folder convention — NOT a git repo
  praxis/          # shared central harness — one clone per machine, kept in git
  helios-api/  helios-workers/  helios-web/  helios-console/   # 4 product repos
```

- Each repo is its **own** git repo; everyone clones them side by side so the
  relative `harnessRoot: ../praxis` resolves the same for all.
- **The harness `praxis` is the shared repo.** Pushing/pulling it is how the team
  syncs specs, decisions, and project memory. Treat it like any shared repo:
  branch, PR, review, merge.
- Don't make `workspace/` itself a git repo (that nests repos). If you ever need
  one-clone reproducibility, switch to submodules — but option A doesn't need it.

## One source of truth — never duplicate SPEC or REQ

This is the rule that makes multi-person work sane (see
[`../rules/traceability.md`](../rules/traceability.md)):

- A spec and its requirements live in **exactly one place**:
  `projects/helios/specs/<slug>/spec.md`. `REQ-001` is defined there, once.
- A **cross-repo feature is one spec**, not one per repo. Its `tasks.md` groups
  tasks by repo; every task references the requirement by id
  (`source:SPEC-live-tracking/REQ-001`) — it never copies the requirement text.
- `helios-api` and `helios-web` both implement parts of the same `REQ-001` by
  **pointing at it**, so the requirement can't drift between repos.
- If you're about to paste requirement text into a second file, **link the id
  instead.**

## The spec folder is the unit of parallel work

Two people on **different** specs touch **different** folders
(`specs/live-tracking/` vs `specs/merchant-onboarding/`) → no merge conflict by
construction. So the basic rule of concurrency is: **one spec → one owner (or
pair) at a time.** Assign specs, not files.

- **Collision-safe ids.** Top-level items are slug-keyed (`SPEC-live-tracking`),
  so two people never race for "SPEC-007". Sub-ids (`REQ-`, `TASK-`, `ADR-`) are
  numbered **within** their spec, so two specs can both have `REQ-001` with no
  conflict.
- **Decisions are one file each.** Record a decision as
  `specs/<slug>/decisions/ADR-002-...md` (or a project decision under
  `memory/decisions/`), not as an edit to a shared file. Per-file decisions from
  different specs merge cleanly.
- **Keep `current-state.md` short and additive.** It's the one shared file that
  several people touch. Use the "Now" list to show *who owns what in flight*;
  prune aggressively. If it causes conflicts often, it's too detailed — move
  detail into the per-spec artifacts.
- **The ledger is append-only JSONL.** Concurrent appends can collide on the last
  line; resolve by keeping **both** lines (union). Prefer per-spec
  `decisions/` files for most records so the shared ledger stays for genuinely
  cross-cutting entries.

## `activeSpec` is per session, not committed

If three people share `helios-api`, they're each working a different spec — so the
committed `.praxis/config.json` must **not** pin one person's spec.

- Leave `activeSpec: null` in the **committed** config.
- Each developer sets their own active spec in **runtime** (git-ignored,
  per-machine):

  ```sh
  python tools/runtime.py set --project helios --repo helios-api --spec live-tracking
  ```

That way the shared config never churns and each session still knows its context.

## Who approves a gate?

With more than one person, "the human accepts" is ambiguous. Name the approver in
the project's `PROJECT.md` **authority notes**, per gate — e.g. *"Spec gate:
product owner; Architecture gate: tech lead; Release gate: tech lead + PO."* The
agent presents the gate (Recommendation / Evidence / Risks / Alternatives); the
named owner records `ACCEPT` by moving the spec to `status: accepted` (or
accepting the ledger decision). **Pending is not approval** still holds — and now
it's clear *whose* approval.

## Several teams, same or different repos

The unit of isolation scales up cleanly:

- **Different teams → different specs.** Team A owns `SPEC-live-tracking`, team B
  owns `SPEC-merchant-onboarding`. Their spec folders don't overlap; their code
  lands through normal per-repo PRs.
- **When two specs would change the same module**, that's surfaced, not silent:
  an accepted architecture decision (`ADR-`) records the contract, and
  `/review-changes` flags a diff that contradicts an accepted decision or the
  active spec (it loads them in harness mode). Resolve at the contract, not in two
  diverging implementations.
- **Canonical contracts prevent cross-team drift.** Helios declares
  `helios-api/openapi.yaml` and the design tokens as canonical (in `PROJECT.md`).
  A change there is a decision other teams can see, not a local assumption.
- **Cadence:** push the harness often (specs/decisions are small and merge well),
  review spec PRs like code, and keep `open-questions.md` current — a blocker
  there is a stop condition for everyone touching that area.

## From one dev to many — nothing changes shape

Solo, you still write the spec once, work it through the gates, and let git carry
the harness. Adding people just means: assign specs as the unit of work, name gate
approvers, keep `activeSpec` in runtime, and record decisions one-file-each. The
methodology is the same; the coordination is in git + the spec model, not in a new
tool.
