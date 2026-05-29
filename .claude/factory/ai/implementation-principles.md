# Implementation Principles

Apply these rules when a skill **generates, modifies, reviews, or proposes code** (Tier 4 and Tier 5 skills). The principles are inspired by widely-shared engineering discipline, especially as articulated by Andrej Karpathy. This document is the local source of truth; do not treat any external repo as unquestioned authority.

These principles are not about the factory itself — they are about the code that produced skills emit, and about how skill-creator-generated scripts should behave.

## 1. Think before coding

Before generating or changing code:

- **Restate the objective** in one sentence. What is the user actually trying to achieve?
- **Identify constraints.** Language, framework, runtime, target environment, performance budget.
- **Identify affected files.** Which exist? Which need to be created? Which should not be touched?
- **Define success criteria.** What test, validator, or visual check confirms it works?
- **Note assumptions.** Anything not stated explicitly that the code depends on.

If any of these are unknown, **ask the user** before writing code. Guessing wastes more time than asking.

## 2. Simplicity first

Prefer:

- the smallest working solution;
- existing project patterns over new ones;
- obvious code over clever code;
- fewer abstractions;
- fewer moving parts.

Avoid:

- speculative architecture (building for needs that do not yet exist);
- unnecessary frameworks;
- premature generalization;
- broad rewrites when a targeted change would do.

If a solution requires explaining a clever abstraction, the abstraction is probably wrong for this stage.

## 3. Surgical changes

Change only what is necessary to meet the objective. Do not:

- refactor unrelated files;
- rename things without reason;
- reformat entire files;
- introduce new patterns when existing ones already work;
- "while I'm here, let me also fix..." — separate concerns into separate changes.

Unsolicited refactors create review burden and merge conflicts. They are not free.

## 4. Goal-driven execution

Before declaring done:

- check whether the original objective is satisfied (re-read the brief if needed);
- run available tests or validators;
- report exactly what changed;
- report what remains unverified;
- expose risks (assumptions that might be wrong, edge cases not tested).

If a test or validator does not exist, write a minimal one. "I ran it once and it looked OK" is not goal-driven execution.

## 5. Explain the why

When a skill generates code, the produced code should carry intent. Prefer:

- a one-line comment explaining a non-obvious trade-off;
- a docstring on a function that captures the invariant;
- clear variable names that encode meaning.

Avoid:

- comments that narrate what the code obviously does ("// increment counter");
- redundant docstrings;
- ASCII-art banners.

The goal is that a reader six months later (human or agent) understands why this code exists, not what each line does mechanically.

## 6. Failure should be informative

When code can fail, it should fail with:

- a clear error message naming the input or condition that caused it;
- a hint at the likely fix;
- an exit code or exception type that callers can branch on.

Silent failure (returning empty data, swallowing exceptions) is forbidden in produced skills.

## 7. Determinism where possible

If a check can be done by a script, do not delegate it to an LLM. Examples that belong in scripts, not in `SKILL.md` instructions:

- "does this file exist?";
- "is this JSON valid?";
- "does the frontmatter have a `name` field?";
- "does this folder contain at least one `.md` file?";
- "are all references one level deep?".

LLMs are for judgment calls, not bookkeeping.

## 8. Output expectations

Every code-producing skill must state in its `SKILL.md`:

- **what files** it produces (path patterns);
- **what format** they are in;
- **what validation** must pass before declaring done;
- **what to do** if validation fails (retry? ask the user?).

Output that the agent cannot inspect or validate is output the agent cannot ship.

## 9. Stop conditions

Every workflow in a code-producing skill must have an explicit stop condition. Common patterns:

- "Stop when `validate.py` exits 0."
- "Stop when the user confirms the diff."
- "Stop when N iterations have passed and the metric did not improve."

Loops without stop conditions are how skills end up rewriting the same file forever.

## 10. Acknowledged trade-offs

If you take a shortcut, name it. Examples:

- "Used a regex here instead of a proper parser because the input format is fixed and small. Revisit if the input grows."
- "Skipped the migration validator because the produced SQL is reviewed manually before running."

Acknowledged trade-offs are fine. Hidden ones rot.
