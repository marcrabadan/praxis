# Validation Orchestrator — gate checklist & escalation

This reference makes the role deterministic. For each gate in
`feature-development`, the criteria source, the evidence to demand, and where a
failure routes. Criteria text is owned by the **workflow manifest's
`gateCriteria`** — this file points at it; it does not fork it.

## Gate-by-gate

| Gate (token) | Criteria source | Evidence to demand | On failure → |
|--------------|-----------------|--------------------|--------------|
| `approved-discovery` | `gateCriteria.approved-discovery` | discovery report + research; problem/user/outcome stated | `discovery` |
| `approved-product-definition` | `gateCriteria.approved-product-definition` | product-definition.md; MVP bounded, requirements prioritised & traced | `product-definition` |
| `approved-spec` | `gateCriteria.approved-spec` | spec.md; testable acceptance criteria; no contradiction with product def | `spec` |
| `experience-complete` | manifest `gates.plan` | each declared surface has a contract | `experience` |
| `architecture-validated` | `gateCriteria.architecture-validated` | architecture-review.md; NFRs met, ADR for unfamiliar arch | `plan` |
| `approved-plan` | manifest `gates.tasks` | implementation plan accepted | `plan` |
| `verify-passed` | `loops.verify.predicate` + `G-*` | verify report `overall-result: pass`, accepted sign-off | `build` |
| `release-candidate-ready` | `gateCriteria.release-candidate-ready` | release candidate; pass sign-off; no open high/critical security finding | `verify` |
| `release-approved` | human decision | explicit release approval (not pending) | — |

The verify gate is proven by the typed catalog — `G-build`, `G-lint`,
`G-typecheck`, `G-tests`, `G-runtime-clean`, `G-acceptance`, the mandatory
`G-security`, and the conditional `G-performance`/`G-routes-200`/`G-visual`.
A skipped **required** gate without justification fails the report. A conditional
gate that does not apply records *why* (wrong surface type).

## The block protocol

1. State the gate and the **specific** unmet criterion (quote it).
2. Cite the missing or red evidence.
3. Name the return state from `transitions.onGateFailure`.
4. Record a `decision` (verdict: block) in the memory ledger, `pending`.
5. Do not allow the guarded step to start.

## The escalate protocol

Escalate (do not decide) when:

- a convergence-loop guard tripped — `tools/loop.py` returned `escalate`
  (budget exhausted or no progress);
- two authoritative artifacts contradict (stop condition `U-6`);
- a required gate **cannot run** (`U-7`) and no approved waiver exists;
- the call is genuinely the user's (a risk acceptance, a scope trade-off).

Bring: the current state, the blocker, the evidence, and **at least two**
options. "Keep going anyway" is never one of them.

## Promotion

A recurring block of the same class is evidence to **promote** a new stop
condition (`P-*`), gate, or guardrail via `tools/promote.py` — pending and
human-gated, routed through `skill-learner`. The Validation Orchestrator
proposes; it does not silently add rules.
