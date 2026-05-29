# Skill Tiering

Every skill in this repo (and every skill it produces) must be classified into one of five tiers **before** any files are scaffolded. The tier determines the folder shape and the level of harness around the skill.

## Why tier first

Skipping classification leads to two failure modes:

1. **Underbuilding** — a workflow skill gets only `SKILL.md` and loses its procedural structure.
2. **Overbuilding** — a simple guidance skill gets evals, scripts, agents, and reports it does not need.

Both failures waste tokens at trigger time and slow iteration. The tier system forces a deliberate choice.

## The five tiers

### Tier 1 — Basic Skill

A small guidance skill with no reusable knowledge, no procedure, no scripts.

```
.claude/skills/<skill-name>/
└─ SKILL.md
```

Use for: tone/style guidance, naming conventions, short review checklists, lightweight behavior patterns.

Do **not** add `references/`, `workflows/`, `scripts/`, `evals/`, or `agents/`.

### Tier 2 — Knowledge Skill

The skill needs reusable domain knowledge that would bloat `SKILL.md` if kept inline.

```
.claude/skills/<skill-name>/
├─ SKILL.md
└─ references/
   ├─ rules.md
   ├─ examples.md
   └─ anti-patterns.md
```

Use for: UX writing rules, design principles, accessibility guidance, domain knowledge, glossaries.

`SKILL.md` stays short and points the agent at the right reference file for the situation at hand.

### Tier 3 — Workflow Skill

The skill has a repeatable multi-step procedure or multiple modes.

```
.claude/skills/<skill-name>/
├─ SKILL.md
├─ references/
└─ workflows/
   ├─ default.md
   ├─ review.md
   └─ finalize.md
```

Use for: guided interviews, spec generation, research workflows, design reviews, multi-mode skills.

### Tier 4 — Implementation Skill

The skill generates, modifies, reviews, or validates code or structured machine-readable output.

```
.claude/skills/<skill-name>/
├─ SKILL.md
├─ references/
├─ workflows/
├─ scripts/
└─ evals/
```

Use for: code generation, token validation, design-system component generation, schema generation, markdown-to-JSON conversion, packaging workflows.

Tier 4 skills must apply the rules in [implementation-principles.md](implementation-principles.md).

### Tier 5 — Core Skill

A central, frequently reused, high-risk, or measurably improved skill. Adds specialist evaluator subagents and a place for generated reports.

```
.claude/skills/<skill-name>/
├─ SKILL.md
├─ references/
├─ workflows/
├─ scripts/
├─ evals/
├─ agents/
├─ assets/
└─ reports/
```

Use for: the skill-creator itself, skill-evaluator, skill-packager, critical team workflows, high-risk codegen skills, skills intended for repeated distribution to many users.

Do not jump straight to Tier 5. Promote a skill from Tier 4 to Tier 5 only when at least one of the following is true:

- the skill is triggered often enough that quality regressions are costly;
- the skill has produced incorrect output in the past and needs measured improvement;
- specialist evaluators (grader, comparator, analyzer) provide real signal that a checklist cannot.

## Classification decision tree

Apply these questions in order. Stop at the first match.

1. Does the skill **generate, modify, or validate code or structured machine-readable output**?
   - Yes → **Tier 4** (or Tier 5 if it also meets the promotion criteria above).
2. Does the skill have a **repeatable multi-step procedure** or multiple modes?
   - Yes → **Tier 3**.
3. Does the skill need **reusable domain knowledge** that would not fit in `SKILL.md` under 500 lines?
   - Yes → **Tier 2**.
4. Otherwise → **Tier 1**.

After the initial classification, re-check the Tier 5 promotion criteria. If the skill clearly meets them, promote it explicitly and state why.

## Tier inputs from the interview

The interview captures the inputs the decision tree needs:

| Question (from interview) | Feeds                  |
| ------------------------- | ---------------------- |
| Does it produce or modify code? | Tier 4 vs lower    |
| How many steps does its main workflow have? | Tier 3 trigger |
| Is there reusable domain knowledge? | Tier 2 trigger     |
| How often will this trigger? | Tier 5 promotion check |
| Has it failed before / does it need measured improvement? | Tier 5 promotion check |

## Tier downgrades

If during scaffolding a tier looks too heavy (e.g. `evals/` would be empty fixtures), drop down a tier. It is cheaper to grow a Tier 2 into a Tier 3 later than to maintain empty folders.

## State the tier explicitly

The chosen tier is recorded in two places:

1. The skill's `skill-brief.md` (under a `tier:` field in frontmatter).
2. The summary the agent returns at the end of skill creation.

This makes the choice auditable and easy to revisit on review.
