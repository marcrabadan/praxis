# ADR-001 — /idea triage command design

> Spec-scoped decision (`ADR-001` within `SPEC-idea-command`). Records the four
> design calls already settled in research so the "why" is traceable. Mini-ADR:
> the feature is one ~40-line markdown command, so no C4 diagram is warranted.

## Context

`/idea` is an intake front door for raw, half-formed ideas. The driving NFRs are
**thinness** (NFR-1: 31–41 lines, the proxy for "no downstream logic absorbed")
and **determinism** (NFR-4: classification → route mapping must be statically
readable from the file, not inferred at runtime). The command must match the
established thin-router shape of `memory.md` / `learn.md` and touch the ledger
without a schema change. Four interlocking decisions shape it.

## Decision

1. **Recommend-and-confirm, not auto-route.** `/idea` classifies, captures, prints
   the exact downstream invocation string, and stops. It never invokes
   `/new-feature` / `/fix-bug` / `/refine`.
2. **Command, not skill.** Implemented as `.claude/commands/idea.md` with inline
   reasoning — no `Agent`/`Skill` dispatch, no subagent. Per the promotion policy,
   a skill is unjustified for a four-bin triage that all existing thin routers do
   inline.
3. **Inline 4-way classification.** `feature`/`bug`/`refinement`/`not-worth-doing`,
   with explicit absorb rules (doc updates, dependency bumps, behavior-preserving
   process changes → `refinement`). Mapping stated as a static table in the body.
4. **`--type note` ledger capture.** `ledger.py log --type note --source /idea
   --status pending --tags "intake,<class>"`, unconditional across all four
   outcomes. No new `idea` type; `source` + `tags` give `/patterns` clean signal.

## Status

proposed

## Consequences

- `/idea` stays thin (only `Bash` + `AskUserQuestion`, both default tools); no
  `allowed-tools`, no cross-command coupling, no subagent latency.
- The user gets a confirmation moment before any heavy lifecycle starts, and one
  extra action (running the recommended command) — an accepted, small friction.
- Every invocation, including `not-worth-doing`, leaves a `pending` ledger record;
  nothing is silently dropped.
- A misclassification is low-cost and user-correctable (advisory, pre-lifecycle).
- Forward debt: if a dedicated `idea` ledger type is later introduced, existing
  `intake`-tagged `note` entries need a migration (OQ-R1, non-blocking).

## Top risk

**Description collision with `/new-feature`** — if `/idea`'s `description`
overlaps lifecycle commands, the router may ambiguously select `/idea` when the
user means a direct lifecycle call (NFR-6). Mitigation: `description` must contain
"intake and triage" and must not contain "plan a feature".

## Alternatives considered

(from [`../research/alternatives.md`](../research/alternatives.md))

- **Auto-route (OQ-1, Option A):** rejected — double-questioning hazard, no target
  for `not-worth-doing`, cross-command coupling, needs `Agent` (breaks thinness).
- **Skill delegation to `business-analyst`/`product-owner` (OQ-3, Option B):**
  rejected — over-engineered for binary-style triage, requires `Agent`, no
  precedent among thin commands.
- **`--type decision` / new `--type idea` (OQ-4, B/C):** rejected — `decision`
  inflates and misleads `/patterns`; a new type means a `ledger.py` schema change
  (out of scope, C-3).
- **Silent drop for `not-worth-doing`:** rejected — violates BG-2 (every
  invocation must record), undermines the "front door" value.

## Traceability

- Decides: design of `SPEC-idea-command` (FR-1…FR-7, NFR-1…NFR-6)
- Source: `RES-idea-command`, `ALT-idea-command`
