# Glossary

Definitions used consistently across this repo. If you find yourself using a synonym for one of these, stop and use the canonical term instead.

## Skill

A folder containing a `SKILL.md` file with YAML frontmatter (`name`, `description`, sometimes `disable-model-invocation`) and a markdown body. May include `references/`, `workflows/`, `scripts/`, `evals/`, `agents/`, `assets/`, and `reports/` depending on tier. Claude Code discovers a skill from its frontmatter and exposes it via the Skill tool / `/<name>`.

## SKILL.md

The required entry-point file of a skill. Contains frontmatter and instructions for the agent. Stays under 500 lines; longer content lives in `references/`.

## Frontmatter

The YAML block at the top of `SKILL.md`, delimited by `---` lines. Contains at minimum `name` and `description`.

## Description

The third-person, trigger-rich string in frontmatter that the agent reads to decide whether to invoke the skill. Max 1024 characters. See [routing.md](routing.md).

## Tier

One of five complexity levels (1–5) that determines a skill's folder structure. See [skill-tiering.md](skill-tiering.md). Classified **before** scaffolding.

## Skill brief

A markdown file (`skill-brief.md`) produced by the interview workflow. Captures the user's purpose, audience, trigger context, output format, rules, examples, and tier choice. Lives at the root of the produced skill folder. Inputs to the generator script.

## Skill factory

This repo (`praxis`). The system that creates, improves, evaluates, and packages skills.

## Factory-owned skill

A skill that lives inside `.claude/skills/` in this repo and supports the factory itself or is a shared org asset. Currently: `skill-creator` (the meta-skill, includes interview workflows) and the eight SDLC expert skills (`business-analyst`, `product-owner`, `software-architect`, `developer`, `qa-engineer`, `devops-engineer`, `security-engineer`, `cybersecurity-architect`).

## Produced skill

A skill created by the factory. Defaults to scratch at `dist/<skill-name>/` during creation; promote to `.claude/skills/<skill-name>/` when it becomes a shared asset that Claude Code discovers automatically.

## Generator

The script `.claude/skills/skill-creator/scripts/create_skill.py`. Consumes a `skill-brief.md` plus a tier and emits the scaffold deterministically. Same input → same output.

## Validator

A Python script that performs deterministic checks on a skill (existence of files, frontmatter shape, JSON validity). Lives in `.claude/factory/validators/` and in `.claude/skills/skill-creator/scripts/`. Never delegates to an LLM.

## Trigger eval

A JSON file (`evals/trigger-evals.json`) containing positive and negative cases — user queries paired with `should_trigger: true|false`. Used to verify that a skill's description routes correctly.

## Output eval

A JSON file (`evals/output-evals.json`) containing prompts paired with expected outputs or assertions. Used to verify that a skill produces correct output when triggered.

## Workflow

A markdown file in `workflows/` describing a procedural sub-routine of a skill. Skills with multiple modes (create, review, evaluate, package) split each mode into its own workflow file.

## Reference

A markdown file in `references/` containing stable knowledge — rules, examples, anti-patterns, glossaries. Read by the agent only when relevant, not always.

## Interview

A guided one-question-at-a-time conversation used to capture objectives or a skill brief when user intent is incomplete. Implemented by [.claude/skills/skill-creator/workflows/interview.md](../../skills/skill-creator/workflows/interview.md) (general) and [interview-intake.md](../../skills/skill-creator/workflows/interview-intake.md) (skill creation).

## Routing

The mechanism by which an agent decides which skill to invoke based on `description` content. See [routing.md](routing.md).

## Implementation principles

The rules in [implementation-principles.md](implementation-principles.md) that apply to skills producing or modifying code (Tier 4 and Tier 5).
