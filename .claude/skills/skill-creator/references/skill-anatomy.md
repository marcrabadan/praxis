# Skill Anatomy

What each folder in a skill is for, and when to include it. See [ai/skill-tiering.md](../../../factory/ai/skill-tiering.md) for which folders belong in which tier.

## `SKILL.md` (required)

The entry point. Loaded into context whenever the skill triggers. Contains:

- YAML frontmatter (`name`, `description`, optional `disable-model-invocation`, `tier`);
- a one-line purpose statement;
- "when to use" and "when not to use" sections;
- routing to the appropriate workflow / reference;
- output expectations;
- stop conditions.

Keep `SKILL.md` under 500 lines. If you are approaching that limit, move material into `references/` and link to it.

## `references/`

Stable knowledge that the agent reads only when the situation calls for it.

Typical files:

- `rules.md` — core rules of the domain.
- `examples.md` — input/output examples the agent should mimic.
- `anti-patterns.md` — common failures and the correct alternatives.
- `glossary.md` — terms with one canonical meaning.

Keep references one level deep. Deeply nested references cause partial reads.

## `workflows/`

Procedural sub-routines. Use when the skill has multiple modes or a multi-step procedure that would crowd `SKILL.md`.

Typical files:

- `default.md` — the primary path.
- `review.md`, `evaluate.md`, `package.md` — variant modes.

Each workflow is a numbered procedure with explicit inputs, outputs, and a stop condition.

## `scripts/`

Deterministic automation. Use scripts for things that can be checked or done mechanically: parsing, validation, file emission, packaging.

Rules:

- Each script accepts inputs via `argparse`.
- Each script exits 0 on success, non-zero with a clear message on failure.
- Each script is documented in `SKILL.md` with a one-line purpose.
- Do not duplicate script logic in prose. Tell the agent to run the script.

## `evals/`

Test cases.

Files:

- `trigger-evals.json` — array of `{query, should_trigger}` cases. At least one positive and one negative.
- `output-evals.json` — object with `skill_name` and `evals` array. Each eval has `id`, `prompt`, and optional `expected_output` / `files` / `assertions`.
- `fixtures/` — optional sample inputs the evals reference.

Negative cases should be near-misses, not obviously irrelevant queries. Easy negatives test nothing.

## `agents/` (Tier 5 only)

Specialist evaluator roles invoked as subagents:

- `grader.md` — evaluates outputs against assertions.
- `comparator.md` — blind A/B between two outputs.
- `analyzer.md` — explains why one version beat another.

Use these only when specialist judgment is required. A checklist often suffices.

## `assets/` (Tier 5)

Static reusable resources — templates, fixtures, example outputs.

## `reports/` (Tier 5)

Generated reports (benchmark summaries, reviews, comparisons). Reports are **outputs**, not source instructions.

## `skill-brief.md`

Produced by the interview workflow. Lives at the root of the skill folder. Documents:

- the user's stated purpose;
- the answers given during the interview;
- the assumptions the agent made;
- the chosen tier and why.

`skill-brief.md` makes creation auditable. Keep it for at least the first review pass.
