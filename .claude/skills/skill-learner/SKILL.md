---
name: skill-learner
description: Detects when a praxis SDLC expert hits a knowledge gap mid-task — missing team conventions, runbooks, or domain rules it should have applied — and turns it into durable skill knowledge by routing to the skill-creator to create a new skill or refine an existing one, always proposed via the memory ledger and never mutated silently. Use when the user says you didn't know our setup, learn this, capture or remember how we do X, teach the system our Terraform/Azure/deployment convention, update or refine a skill with what you just learned, or an expert is missing our runbook. For making a skill from scratch or validating a SKILL.md, use the skill-creator instead.
tier: 3
version: 1.0.0
---

# Skill Learner

The **learning loop** of the factory. When an SDLC expert is working and hits a
gap — it lacks *this team's* conventions, a runbook, or domain rules it should
have applied (e.g. the `devops-engineer` is asked how the org builds
infrastructure in Terraform or Azure and no convention is captured) —
`skill-learner` turns that gap into durable, auditable skill knowledge.

It is a **thin orchestration layer**, not a second skill factory. It does three
things and delegates the rest:

1. **Detect** that the gap is real and worth capturing.
2. **Decide** where the knowledge belongs (new skill, existing skill, or a
   reference inside a role expert) and at what tier/granularity.
3. **Delegate** the actual authoring to the [`skill-creator`](../skill-creator/SKILL.md),
   then **propose** the result through the [memory ledger](../memory/SKILL.md) as
   `pending` for the user to accept.

It never edits a skill silently. **Propose, don't mutate.**

## Required reading

Before acting, read [references/rules.md](references/rules.md) — the four rules
that keep this loop safe. The new-skill-vs-reference granularity call is governed
by [../../factory/ai/promotion-policy.md](../../factory/ai/promotion-policy.md)
(*promote on evidence, never on anticipation*).

## When to use

Trigger this skill when:

- An expert was asked for org-specific knowledge it does not have — "how do *we*
  build infra in Terraform/Azure", "what's our deployment runbook" — and the
  answer should be remembered for next time.
- The user says "learn this", "capture how we do X", "remember our convention",
  "teach the system", "you didn't know our setup".
- An existing skill gave an answer that was wrong or incomplete for this org and
  should be **refined** with what was just learned.

## When not to use

- The user wants to **build a skill from scratch** or **validate a SKILL.md** —
  that is the [`skill-creator`](../skill-creator/SKILL.md) directly. `skill-learner`
  is for gaps *discovered during work*, and it hands off to the skill-creator.
- The gap is **public knowledge the model already has** (plain Terraform syntax,
  what Azure is). A skill captures org-specific conventions and procedures, not
  facts the model can already produce. See `references/rules.md`, Rule 2.
- The user just wants the answer once, with no intent to make it durable.

## Workflows

Pick the mode that matches the situation and follow its file.

| Mode | File | When |
|------|------|------|
| Detect & route | [workflows/detect-gap.md](workflows/detect-gap.md) | Entry point — confirm the gap is real and org-specific, search existing coverage, decide the route. |
| Refine existing | [workflows/refine-existing.md](workflows/refine-existing.md) | Coverage exists but is wrong/incomplete — hand to skill-creator's review flow. |
| Create new | [workflows/create-new.md](workflows/create-new.md) | No coverage — decide reference-vs-new-skill and tier, hand to skill-creator's create flow. |
| Promote governance | [workflows/promote-governance.md](workflows/promote-governance.md) | The insight is a standing *constraint*, not skill knowledge — turn a validated assumption or evidenced gap into a `pending` rule / gate / eval / guardrail via `tools/promote.py`. |

Default path: **detect-gap → (refine-existing | create-new)**. When the learning
is a harness constraint rather than skill knowledge, use **promote-governance**.

## References

- [references/rules.md](references/rules.md) — the four governing rules.
- [references/examples.md](references/examples.md) — worked examples (the Terraform/Azure gap, the language-granularity call).

## Evals

- [evals/trigger-evals.json](evals/trigger-evals.json) — positive and negative
  routing cases, with the near-misses centred on the boundary against
  `skill-creator` (build-from-scratch / review a SKILL.md) and against public
  knowledge that should be answered, not captured.

This skill carries `evals/` purely as a routing safety net — it has a real
collision risk with `skill-creator` and benefits from explicit negative cases.
It stays **Tier 3**: it orchestrates and delegates, it does not generate,
modify, or validate code, so the Tier 4 trigger in
[../../factory/ai/skill-tiering.md](../../factory/ai/skill-tiering.md) does not
apply.

## Output expectations

- A one-line statement of the **gap** and evidence it is org-specific, not public.
- A **routing decision**: create new / refine existing / add reference, with the
  exact destination (which skill, which reference file).
- A **tier and granularity** call, justified against the promotion policy.
- A **handoff** to the skill-creator (which workflow, with what brief).
- A **memory-ledger entry** logged as `pending` describing what will be learned.
- Validator result for any touched skill.

## Stop conditions

The skill is done when:

- The gap has been classified as capturable (org-specific) or declined (public
  knowledge / one-off), with the reason stated.
- A routing decision and destination exist.
- The skill-creator handoff has been made (or explicitly deferred to the user).
- A `pending` ledger entry records the proposed learning.
- The validator passes on any skill that was created or refined.
- Nothing was mutated without a corresponding `pending` proposal.
