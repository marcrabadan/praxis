---
name: {{NAME}}
description: {{DESCRIPTION}}
---

# {{TITLE}}

{{PURPOSE}}

## When to use

Use this skill when:

- (concrete user phrases / contexts)

## When not to use

Skip this skill when:

- (near-miss situations)

## Why Tier 5

This skill is Tier 5 because:

- (high reuse / high risk / needs measured improvement / has specialist evaluator roles)

Promotion to Tier 5 should be justified explicitly. If the justification weakens over time, demote to Tier 4.

## Implementation discipline

Applies [ai/implementation-principles.md](../../ai/implementation-principles.md).

## Workflows

| Mode | File |
|------|------|
| Default | [workflows/default.md](workflows/default.md) |
| Review | [workflows/review.md](workflows/review.md) |
| Evaluate | [workflows/evaluate.md](workflows/evaluate.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate.py` | (describe) |
| `scripts/validate.py` | (describe) |

## Agents

Specialist evaluator roles invoked as subagents:

- [agents/grader.md](agents/grader.md) — grades outputs against assertions.
- [agents/comparator.md](agents/comparator.md) — blind A/B comparison between two outputs.
- [agents/analyzer.md](agents/analyzer.md) — analyzes why one version beat another.

Do not invoke these for every run. Use them when specialist judgment is required.

## References

- [references/rules.md](references/rules.md)
- [references/examples.md](references/examples.md)

## Evals

- [evals/trigger-evals.json](evals/trigger-evals.json)
- [evals/output-evals.json](evals/output-evals.json)

## Assets

Static reusable resources in [assets/](assets/) — templates, examples, fixtures.

## Reports

Generated reports land in [reports/](reports/). Reports are outputs, not source instructions.

## Output expectations

(Concrete success criteria.)

## Stop conditions

(Concrete done signals.)
