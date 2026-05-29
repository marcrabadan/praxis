# Routing

How agents decide which skill to invoke is determined almost entirely by the **`description`** field in `SKILL.md` frontmatter. This document defines the rules for writing descriptions that route correctly.

## Why descriptions matter

Skills appear in the agent's available-skills list with only their `name` and `description`. The body of `SKILL.md` is not visible at routing time. If the description is vague, the agent will undertrigger or misroute.

## Description requirements

Every skill description in this repo must:

1. **Be third-person.** It is injected into the system prompt.
   - Good: "Extract text and tables from PDF files."
   - Bad: "I help you extract text from PDFs."

2. **Include both WHAT and WHEN.**
   - WHAT: the specific capabilities of the skill.
   - WHEN: realistic user contexts and phrases that should activate it.

3. **Be trigger-rich.** List concrete phrases the user is likely to say. Modern agents tend to undertrigger skills; bias slightly toward inclusion.

4. **Stay under 1024 characters.** This is a hard limit enforced by the validator.

5. **Use one consistent term per concept.** Do not mix "endpoint" / "route" / "URL" for the same thing.

6. **Avoid vague glue words.** "Helps with", "deals with", "assists" — replace with the specific verb.

## Good vs bad descriptions

### Good

```yaml
description: Extract text, tables, and form fields from PDF files; fill PDF forms; merge or split PDF documents. Use when the user mentions PDFs, PDF forms, document extraction, or asks to read, search, fill, merge, or split a .pdf file.
```

```yaml
description: Create new Claude Code skills from scratch, improve or review existing skills, validate skill structure, and classify a skill into the right tier. Use when the user says they want to make a skill, build a skill, design a skill, turn a workflow into a skill, document a repeatable process as a skill, improve an existing SKILL.md, validate a skill, or decide which tier a skill should be.
```

### Bad

```yaml
description: Helps with PDF files.
```

```yaml
description: A skill for creating skills.
```

The bad versions either lack trigger phrases or use "helps with" — neither helps the agent decide.

## Trigger-eval pattern

For skills important enough to verify, add `evals/trigger-evals.json` with both positive and negative cases:

```json
[
  { "query": "i need to turn this checklist into a skill", "should_trigger": true },
  { "query": "make a skill for naming branches", "should_trigger": true },
  { "query": "what's a skill?", "should_trigger": false },
  { "query": "review my code", "should_trigger": false }
]
```

The negative cases should be **near-misses** — queries that share keywords with the skill but actually need something different. Easy negatives (totally unrelated queries) do not test routing.

## Avoiding trigger collisions

Two skills with overlapping trigger phrases will compete. Resolve collisions by:

1. **Narrowing each description** to the part of the space the skill actually owns.
2. **Cross-referencing.** If skill A says "for PDFs only," skill B can say "for spreadsheets only — not PDFs."
3. **Collapsing** if the skills truly do the same thing. Splitting prematurely is the most common routing failure.

## Controlling auto-trigger

The `disable-model-invocation` frontmatter field controls whether the skill can auto-trigger:

- `disable-model-invocation: true` → skill only loads when explicitly named (`/skill-name` or read by tool).
- omitted → skill auto-triggers from ambient context.

For factory-owned skills in this repo, default to **omitted** (auto-trigger) because we want the skill-creator and the SDLC expert skills to activate from natural-language user requests. Reserve `disable-model-invocation: true` for skills that are risky or expensive to fire unprompted. Capture the choice in the skill-brief during the interview.

## Routing self-check

Before declaring a skill done, ask yourself:

- Could a user who has never seen this skill describe a task that would and would not trigger it from the description alone?
- Are the trigger phrases concrete enough to discriminate from adjacent skills?
- Would the description still be accurate in six months, or does it depend on time-sensitive context?
