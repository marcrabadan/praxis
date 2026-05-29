# Classify-Tier Workflow

Decide which tier (1–5) the new skill should be, using the answers captured during the interview.

## When to run

After [interview-intake.md](interview-intake.md) has produced a `skill-brief.md`. Before [create-skill.md](create-skill.md).

## Inputs

The brief's answers to:

- Q1 (purpose);
- Q5 (rules / preferences / constraints — implies whether reusable knowledge exists);
- Q7 (code production);
- Q8 (reuse expectation);
- the implied number of workflow steps from Q1 / Q3.

## Decision tree

Apply the questions in order. Stop at the first match.

1. **Does the skill produce, modify, or validate code or structured machine-readable output?** (Brief Q7 = "yes — code" or "yes — structured data".)
   - Yes → **Tier 4**. Check the Tier 5 promotion criteria below before finalizing.
2. **Does the skill have a repeatable multi-step procedure or multiple modes?** (Brief Q1 implies ≥3 distinct steps, or the skill has variant modes like create/review/evaluate.)
   - Yes → **Tier 3**.
3. **Does the skill need reusable domain knowledge that would not fit in `SKILL.md` under 500 lines?** (Brief Q5 includes substantial rules or Q6 includes a large set of examples.)
   - Yes → **Tier 2**.
4. Otherwise → **Tier 1**.

## Tier 5 promotion check

After the initial classification, ask whether the skill meets **all** of:

- High reuse expectation (Brief Q8 = "Frequently") **OR** high risk of regression (Brief Q5 contains safety/security/compliance rules);
- Specialist evaluation would provide real signal that a checklist cannot (e.g. blind A/B comparison, grading against multi-dimensional rubrics);
- The skill is critical enough that empty `agents/`, `assets/`, `reports/` folders would be filled over time, not left as scaffolding.

If all three are true, promote to **Tier 5**. Otherwise leave at the initial classification.

Do not jump straight to Tier 5 for new skills. Default to Tier 4 and promote only when the criteria are met.

## Tier downgrade check

After picking a tier, look at the folder shape it implies and ask:

- Will `evals/` be empty fixtures?
- Will `references/` have only one stub file?
- Will `workflows/` have only one file that could just be a section in `SKILL.md`?

If yes to any, **downgrade one tier**. It is cheaper to grow a Tier 2 into a Tier 3 later than to maintain empty folders.

## Confirm with the user

Present the chosen tier with a one-paragraph rationale. Use this format:

```
Suggested tier: <N>

Why: <one or two sentences referencing the brief's answers>

Folder shape this implies:
- SKILL.md
- references/ (rules.md, examples.md)
- workflows/ (default.md)
- ...

Override? (Type a different tier number, or 'yes' to confirm.)
```

If the user overrides, accept and record the override in the brief along with the user's reason.

## Output

After confirmation:

1. Set `tier: <N>` in the `skill-brief.md` frontmatter.
2. Add a "Tier rationale" section to the brief.
3. Hand off to [create-skill.md](create-skill.md).

## Examples

### Example 1 — Tier 1

Brief Q1: "Enforce branch naming conventions in code review."
Brief Q5: "Only one rule: branches must start with `feature/`, `fix/`, `chore/`, or `docs/`."
Brief Q7: "No code production."
Brief Q8: "Occasionally."

Classification: Tier 1. Single rule, no procedure, no knowledge body, no code. `SKILL.md` only.

### Example 2 — Tier 3

Brief Q1: "Guide a designer through a design-system review."
Brief Q5: "Apply the rules in `design-system-rules.md` (long document)."
Brief Q1 implies steps: yes — review structure, then tokens, then components, then accessibility.
Brief Q7: "No code production."

Classification: Tier 3. Multi-step procedure with reusable knowledge. `SKILL.md` + `references/` + `workflows/`.

### Example 3 — Tier 4

Brief Q1: "Generate a CSS file from a JSON token export."
Brief Q5: "Tokens follow the company naming convention; warn on unknown token types."
Brief Q7: "Yes — produces CSS."

Classification: Tier 4. Code production. `SKILL.md` + `references/` + `workflows/` + `scripts/generate.py` + `evals/`.

### Example 4 — Tier 5

The `skill-creator` itself. High reuse, high risk (a bad skill-creator produces many bad skills), needs measured improvement over time, benefits from specialist evaluator subagents.
