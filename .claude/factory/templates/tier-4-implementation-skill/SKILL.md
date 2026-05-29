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

## Implementation discipline

This skill generates or modifies code. Apply the rules in [ai/implementation-principles.md](../../ai/implementation-principles.md):

- think before coding;
- prefer simple solutions;
- make surgical changes;
- define verifiable success criteria;
- run validators before declaring done.

## Workflows

| Mode | File |
|------|------|
| Generate | [workflows/generate.md](workflows/generate.md) |
| Validate | [workflows/validate.md](workflows/validate.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate.py` | (describe) |
| `scripts/validate.py` | (describe) |

Use scripts for deterministic work (parsing, validation, file emission). Do not duplicate script logic in prose.

## References

- [references/rules.md](references/rules.md)
- [references/examples.md](references/examples.md)

## Evals

- [evals/trigger-evals.json](evals/trigger-evals.json) — positive and negative routing cases.
- [evals/output-evals.json](evals/output-evals.json) — expected outputs and assertions.

## Output expectations

(File paths, formats, validation that must pass.)

## Stop conditions

The skill is done when:

- `scripts/validate.py` exits 0;
- the user confirms the diff;
- (other concrete signals).
