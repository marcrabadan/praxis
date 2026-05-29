# Promotion Policy

When and how to promote a workflow inside `skill-creator` into its own top-level skill (or to promote a Tier 2 → Tier 3, Tier 4 → Tier 5, etc.). The rule of thumb: **promote on evidence, never on anticipation**.

This policy exists because the most common failure in skill factories is premature splitting — too many skills that share trigger phrases compete for routing and end up undertriggering. Keeping behavior consolidated until it earns its own trigger surface is the safer default.

## Why this matters

A workflow inside `skill-creator` (e.g. `workflows/review-skill.md`) is invoked by the parent skill's routing. The user does not need to know it exists — they say "review my SKILL.md", the skill-creator triggers on its description, and routes to the right workflow internally.

A top-level skill (e.g. a hypothetical `skill-reviewer/`) has its own `description` competing for trigger surface. If the description overlaps with `skill-creator`'s description (which it inevitably does — "review a skill" is in both), the routing will collide, and the agent will sometimes pick the wrong one.

Therefore: promote only when the evidence shows the workflow is being used independently enough that its own trigger surface is justified.

## Promotion criteria

Promote a workflow into its own top-level skill **only when all of these are true**:

1. **Demonstrated independent invocation.** The user has triggered this workflow without going through the parent skill's main flow at least N times (suggested threshold: **5+ distinct sessions** for medium-cost promotions, **20+ for high-cost promotions like splitting skill-creator**).

2. **Distinct trigger surface.** The user phrases that lead to this workflow are meaningfully different from the parent's phrases. If both the parent and the candidate promotion would trigger on "make a skill for X", do not promote.

3. **Stable interface.** The workflow's inputs and outputs have not changed substantially in the last two delivery cycles. Promoting an unstable workflow forces you to maintain a public surface that is still in flux.

4. **Earned harness.** If the promotion is to a higher tier (e.g. Tier 2 → 3, Tier 4 → 5), the new folders the promotion adds (`workflows/`, `evals/`, `agents/`) will be used, not left as empty scaffolding. Empty harness is worse than no harness — it lies about the skill's maturity.

If any of these is false, **keep the workflow inside its parent**. It is cheaper to grow a Tier 2 into a Tier 3 later than to maintain empty folders or trigger collisions now.

## Demotion criteria

The inverse also applies. Demote a skill (move it back into a workflow of another skill, or drop a tier) **when all of these are true**:

1. The skill has not been triggered in a meaningful window (suggested: **60+ days**) and there is no scheduled use coming.
2. Its trigger phrases are consistently being routed to a different skill — the agent has effectively voted to consolidate.
3. The current folder shape contains directories that are mostly empty stubs.

Demotion is not failure. A skill that did its job during a project and is now quiet is a candidate for archival or merging.

## Specific deferred promotions for v1

The v1 of this repo intentionally collapses several spec-listed skills into workflows under `skill-creator`:

| Spec name | location | Promotion criteria |
|-----------|----------|--------------------|
| `skill-reviewer` | [.claude/skills/skill-creator/workflows/review-skill.md](../../skills/skill-creator/workflows/review-skill.md) | Promote if "review my skill" is invoked 5+ times without an accompanying create/improve task, and the review surface diverges from create (e.g. needs different evaluators). |
| `skill-evaluator` | [.claude/skills/skill-creator/workflows/evaluate-skill.md](../../skills/skill-creator/workflows/evaluate-skill.md) | Promote when an automated eval runner exists and the user runs evals independently of creating skills. Likely tied to the v2 autoresearch loop. |
| `implementation-skill` | [ai/implementation-principles.md](implementation-principles.md) + skill-creator's awareness | Promote when several Tier-4/5 produced skills consistently need shared code-review/refactor logic that does not fit in a doctrine file. |

Each row's promotion criteria are concrete. Hold to them.

## Process for promoting

When you decide a promotion is warranted:

1. Record the evidence. Cite the sessions, dates, or metrics that triggered the decision. A one-line entry in `reports/promotion-log.md` is enough (create the file at first promotion).
2. Run the skill-creator on the new skill. The promotion itself is a skill creation task — interview, classify, scaffold, validate.
3. Update the parent skill: remove or shorten the workflow that has been promoted, and add a one-line pointer ("for X, use the dedicated `<new-skill>` skill").
4. Adjust the parent skill's `description` to narrow its trigger surface so it does not compete with the promoted skill.
5. Add cross-references in the promoted skill back to the parent for any shared references or workflows.
6. Run the validator on both the parent and the new skill.

## Process for demoting

1. Record the rationale alongside the promotion log.
2. Move the demoted skill's contents back into its target workflow under the parent.
3. Archive the demoted skill folder (`dist/_archive/<slug>/` or delete it if it was only ever in `skills/`).
4. Update doctrine and any cross-references.
5. Validate.

## Anti-patterns

- **Pre-emptive splitting.** Creating six skills "because the spec says so" before any of them have evidence of independent use. Avoid.
- **Sentimental retention.** Keeping a skill alive because someone made it, even though nothing triggers it. Demote or archive.
- **Description widening to justify a skill.** If you find yourself adding trigger phrases to a skill's description just so it "earns its place", that is evidence the skill should not exist as its own surface — fold it back.
- **Cross-skill duplication.** Two skills with mostly-identical descriptions, kept distinct because of internal differences. Either merge or sharpen each description to make the difference visible to the router.
