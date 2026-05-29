# Description Writing

The `description` field in a skill's frontmatter is the **only** thing the agent sees at routing time. If the description is vague, the skill will not trigger when it should — or it will trigger when it shouldn't.

This reference is the operational checklist for writing descriptions. The doctrine is in [ai/routing.md](../../../factory/ai/routing.md).

## The contract

A good description:

1. Is written in third person (it is injected into the system prompt).
2. States **what** the skill does in concrete verbs.
3. States **when** to use it with realistic phrases the user would actually say.
4. Stays under 1024 characters.
5. Uses one consistent term per concept.
6. Avoids "helps with", "deals with", "assists" — replace with the specific verb.

## The template

```
<What it does — specific verbs and nouns>. Use when the user <trigger phrase 1>, <trigger phrase 2>, <trigger phrase 3>, or <near-miss situation>.
```

Trigger phrases should be lowercase, realistic, and varied (some formal, some casual). The list should include at least one phrase that does **not** explicitly name the skill's keyword — agents commonly undertrigger when the user is talking around the topic.

## Worked examples

### Good

```yaml
description: Create new Claude Code skills from scratch, improve or review existing skills, validate skill structure, and classify a skill into the right tier. Use when the user says they want to make a skill, build a skill, design a skill, turn a workflow into a skill, document a repeatable process as a skill, improve an existing SKILL.md, validate a skill, or decide which tier a skill should be.
```

Why it works: concrete verbs, multiple realistic phrasings, names adjacent operations (review, validate, classify) that should also route here.

### Good

```yaml
description: Extract text, tables, and form fields from PDF files; fill PDF forms; merge or split PDF documents. Use when the user mentions PDFs, PDF forms, document extraction, or asks to read, search, fill, merge, or split a .pdf file.
```

Why it works: enumerates capabilities, names the file extension, covers both "PDF" and ".pdf" phrasings.

### Bad

```yaml
description: Helps with PDF files.
```

Failures: vague verb ("helps with"), no trigger phrases, no scope.

### Bad

```yaml
description: A skill for creating skills. It can also improve them, review them, and do other related things.
```

Failures: meta-vague ("other related things"), no trigger phrases, no concrete user phrasings.

## Pushy vs honest

Modern agents tend to **undertrigger** skills. To compensate, lean toward inclusion:

- list more trigger phrases than you think you need;
- name near-adjacent operations the skill can handle;
- name common synonyms.

Do not, however, lie about capabilities. If the skill does not actually package, do not say "and package" in the description.

## Trigger collisions

When two skills compete for similar phrases:

1. **Narrow each description** to the part of the space the skill actually owns.
2. **Add a disambiguator** to each: "for PDFs — not spreadsheets" / "for spreadsheets — not PDFs".
3. **Consider collapsing** if the skills genuinely overlap. Premature splitting is the most common routing failure in this repo.

## Self-check

Before declaring a description done:

- Could a user who has never seen the skill predict from the description alone which queries would and would not trigger it?
- Are there at least four trigger phrases?
- Is there at least one negative-coverage phrase (something it does **not** do, if confusion is likely)?
- Is the description under 1024 characters?
- Does `validators/validate_frontmatter.py` pass?

For high-value skills, capture both positive and negative trigger cases in `evals/trigger-evals.json` and verify they route as expected.
