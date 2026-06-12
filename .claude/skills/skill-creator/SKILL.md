---
name: skill-creator
description: Create new Claude Code skills, improve or review existing SKILL.md files, validate skill structure, classify a skill into the right tier, and run guided interviews to scope an objective. Use when the user wants to make, build, improve, rewrite, validate, or tier a skill, or turn a workflow, checklist, or domain rules into one.
tier: 5
version: 1.0.0
---

# Skill Creator

The meta-skill of this repo: **the pattern for creating new skills.** Use it whenever the user wants to **create, improve, review, evaluate, or classify** a Claude Code skill.

The job has two halves:

1. **Gather** the inputs you need through an interview. Do not guess.
2. **Generate** the scaffold deterministically, then refine the body and validate.

## Required reading

Before scaffolding anything, read:

- [../../factory/ai/operating-model.md](../../factory/ai/operating-model.md)
- [../../factory/ai/skill-tiering.md](../../factory/ai/skill-tiering.md)
- [../../factory/ai/routing.md](../../factory/ai/routing.md)

If the skill will produce or modify code, also read [../../factory/ai/implementation-principles.md](../../factory/ai/implementation-principles.md).

## When to use

- "I want to make a skill for X"
- "Turn this workflow into a skill"
- "Capture these rules as a skill"
- "Improve the description of my X skill"
- "Review my SKILL.md"
- "Validate this skill folder"
- "Classify this skill — what tier should it be?"

## When not to use

- The user wants to **run** a skill, not create one — let the relevant skill trigger directly.
- The user is asking conceptual questions about skills with no intent to author one — answer from [../../factory/ai/glossary.md](../../factory/ai/glossary.md) and the other doctrine files instead.

## Routing inside this skill

Pick the workflow that matches the user's request:

| Request | Workflow |
|---------|----------|
| Run a guided interview (any objective, not only skills) | [workflows/interview.md](workflows/interview.md) |
| Create a new skill from scratch or from a vague purpose | [workflows/interview-intake.md](workflows/interview-intake.md) then [workflows/create-skill.md](workflows/create-skill.md) |
| Improve or rewrite an existing skill | [workflows/review-skill.md](workflows/review-skill.md) then [workflows/create-skill.md](workflows/create-skill.md) |
| Classify a skill into a tier | [workflows/classify-tier.md](workflows/classify-tier.md) |
| Add or review evals for a skill | [workflows/evaluate-skill.md](workflows/evaluate-skill.md) |
| User is correcting / iterating on a previous output ("fix this", "actually no...", "next time always...") | [workflows/capture-iteration.md](workflows/capture-iteration.md) |

Default path for "make me a skill for X": interview-intake → classify-tier → create-skill → review-skill → optional evaluate-skill.

**Always-on behavior — iteration capture.** Whenever the user's next message after any of the above workflows is **corrective** (asks to fix, change, rewrite, or "next time do X"), do not silently apply the change. Run [workflows/capture-iteration.md](workflows/capture-iteration.md) first to ask whether the change should be registered as a durable rule for the produced skill, a meta-rule for the skill-creator, or applied one-off. See the workflow for detection heuristics and the exact prompt.

## Canonical flow

```
user states purpose
  -> workflows/interview-intake.md           (one question at a time, follow-ups when warranted)
  -> writes dist/<slug>/skill-brief.md
  -> workflows/classify-tier.md              (decision tree, user confirms)
  -> scripts/create_skill.py                 (deterministic scaffold from template)
  -> hand-author SKILL.md body + references  (push long knowledge out of SKILL.md)
  -> scripts/validate_skill.py               (deterministic validation)
  -> (optional) workflows/evaluate-skill.md  (add trigger + output evals)
  -> promote the finished skill to .claude/skills/<slug>/ when it is a shared asset
  -> summary of created files, assumptions, validation results, next steps
```

## Inputs and outputs

**Inputs from the user.** Purpose, trigger context, output format, audience, rules/preferences, examples, whether it produces code, reuse expectation. The interview workflow captures these one at a time.

**Outputs.** A skill folder at `dist/<slug>/` (or a user-specified path) containing:

- `SKILL.md` with valid frontmatter (`name`, `description`, optional `tier`) and a routing-ready description;
- a `skill-brief.md` documenting the answers and assumptions;
- additional folders (`references/`, `workflows/`, `scripts/`, `evals/`, etc.) as the tier requires.

A Claude Code skill needs no `command.md`: Claude Code discovers a skill from its `SKILL.md` frontmatter and exposes it via the Skill tool / `/<name>` automatically.

## References

- [references/skill-anatomy.md](references/skill-anatomy.md) — what each folder is for.
- [references/description-writing.md](references/description-writing.md) — how to write trigger-rich descriptions.
- [references/prompting-best-practices.md](references/prompting-best-practices.md) — how to write the instruction body for current Claude models. Read when authoring or reviewing a skill body.
- [references/anti-patterns.md](references/anti-patterns.md) — common failures to avoid.

Read only the references relevant to the current task. Do not load all of them up front.

## Learned rules

If `references/learned-rules.md` exists, **read it at the start of every create / review / evaluate session** and apply the rules it contains. These are meta-rules captured from prior user iteration feedback. Conflicts between learned rules and a current user request go to the user — name the conflict explicitly and ask which should win.

If the file does not yet exist, no meta-rules have been captured. Do not invent any.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create_skill.py` | Deterministic scaffolder. Consumes a `skill-brief.md` + tier and emits the folder. |
| `scripts/validate_skill.py` | Same logic as the top-level `.claude/factory/validators/validate_skill.py`; bundled here so the skill is self-contained. |

Always run `scripts/validate_skill.py` before declaring a skill done.

## Evals

- [evals/trigger-evals.json](evals/trigger-evals.json) — positive and negative routing cases for this skill itself.
- [evals/output-evals.json](evals/output-evals.json) — expected outputs for a few sample briefs.

## Stop conditions

The skill-creator's job is done when:

- the produced skill's folder exists and is non-empty;
- `scripts/validate_skill.py` exits 0 on it;
- the user has confirmed (or declined) the optional review / evaluate steps;
- a summary has been returned listing created files, assumptions, validation outcome, and next steps.

## Output expectations (summary the agent must return)

At the end of a session, return:

```
Summary:
- Purpose captured: ...
- Tier chosen and why: ...
- Folder created: dist/<slug>/
- Files written: <list>
- Assumptions: <list, or "none">
- Validation: validate_skill.py returned <ok/fail with details>
- Next steps: <e.g. "add output evals", "promote to .claude/skills/">
```
</invoke>
