# Operating Model

This document defines what `praxis` is, what it is not, and the global rules every agent must follow when working inside it. Read this before scaffolding any skill.

## Purpose

`praxis` is a **skill factory**. It exists to:

- create new skills from a user's stated purpose;
- run a guided interview when the purpose is incomplete;
- decide the right skill tier;
- generate the correct folder/file structure deterministically;
- add scripts only when a check is mechanical;
- add evals when the skill is important enough to test;
- apply implementation discipline when a skill produces or modifies code;
- ship skills as Claude Code skills under `.claude/skills/`, discovered automatically from their frontmatter.

## What this repo is not

This repo is not:

- a product repo;
- an application repo;
- a design-system implementation repo;
- a place to store production React components;
- a place to store production backend code;
- a replacement for project repos;
- a generic Obsidian vault;
- a dumping ground for ideas without a skill purpose.

If a skill creates code, treat the code as an example, a fixture, a generator output, a patch, or a packaged artifact. Production code belongs in the relevant product repository.

## Core principle

> A skill should be as simple as possible, but no simpler.

Do not wrap every skill in a large harness. Instead, classify the skill into a tier (see [skill-tiering.md](skill-tiering.md)) based on its purpose, risk, and expected reuse. The tier determines which folders and files are appropriate.

## Global rules for agents

1. **Read first, write second.**
   - [AGENTS.md](../../../AGENTS.md) for entry points.
   - [skill-tiering.md](skill-tiering.md) before deciding folder structure.
   - [routing.md](routing.md) before writing a `description` field.
   - [implementation-principles.md](implementation-principles.md) when the skill produces or modifies code.

2. **Classify the tier before scaffolding.**
   Use the decision tree in [skill-tiering.md](skill-tiering.md). Do not invent an ad-hoc folder shape.

3. **Use the interview workflow when intent is incomplete.**
   If purpose, output format, trigger context, or audience is missing, run the interview. Ask one question at a time with realistic suggested answers. Do not assume.

4. **Prefer the generator over hand-authored scaffolding.**
   `.claude/skills/skill-creator/scripts/create_skill.py` consumes a `skill-brief.md` plus a tier and emits the scaffold. Use it. Hand-edit afterward.

5. **Use deterministic validators where possible.**
   Mechanical checks (file existence, frontmatter shape, JSON validity) are done by `.claude/factory/validators/validate_skill.py`. Do not ask an LLM to do what a script can do.

6. **Where skills land.**
   - New / experimental / single-team skills default to `dist/<skill-name>/` (scratch, gitignored).
   - Skills that the org keeps and iterates on as shared assets get promoted to `.claude/skills/<skill-name>/` (tracked), where Claude Code discovers them automatically. `.claude/skills/` holds the **meta-skill** (`skill-creator`, which includes the interview workflow) and the **SDLC expert skills** (`business-analyst`, `product-owner`, `software-architect`, `developer`, `qa-engineer`, `devops-engineer`).
   - `dist/` remains **scratch space** for one-off skill scaffolding before promotion to `.claude/skills/` or discard. Gitignored. Still used as the default output of `create_skill.py`.

7. **No production app code.**
   If a skill needs to demonstrate code, the code is an example or fixture, not a real implementation. Production code belongs in product repos.

8. **Document assumptions and unresolved questions** in the produced skill's `skill-brief.md`. Preserve uncertainty rather than guessing.

9. **Surgical changes.**
   Do not refactor unrelated files. Do not rename without reason. Do not reformat entire files.

10. **Stop when the objective is satisfied, not when many steps have been taken.**
    Report what changed, what assumptions were made, what was validated, and what remains unverified.

## Workflow shape (canonical)

```
user purpose
  -> interview (one question at a time)
  -> skill-brief.md
  -> tier classification (1-5)
  -> generator script (create_skill.py)
  -> hand-author SKILL.md body and references
  -> validator
  -> optional: review / evaluate
  -> promote to .claude/skills/<slug>/ when shared
  -> summary
```

Every step is small and inspectable. If a step is being skipped, state why.

## Anti-overbuild constraint

Do not:

- create complex runners before the schemas are stable;
- create fake benchmarks with no useful assertions;
- add production code;
- create many subagents when a checklist would do;
- add dependencies without justification.

Start with documentation, structure, and simple validators. Earn complexity through repeated need, not anticipation.
