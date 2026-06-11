---
description: Turn a knowledge gap discovered during work into durable skill knowledge — capture an org convention, runbook, or rule, or refine an existing skill, via the skill-creator and the memory ledger. Use for "learn this", "capture how we do X", or "update the skill with what you just learned".
argument-hint: <what to learn / capture, or which skill to refine>
---

Use the **skill-learner** skill to capture or refine org knowledge from a gap
discovered during work.

The user wants to teach the factory:

$ARGUMENTS

## How to handle it

Load `skill-learner` and run its workflows in order:

1. [detect-gap](../skills/skill-learner/workflows/detect-gap.md) — confirm the
   gap is **org-specific** (not public knowledge the model already has; see
   `references/rules.md`, Rule 2), search existing coverage under
   `.claude/skills/`, and decide the route.
2. Then [refine-existing](../skills/skill-learner/workflows/refine-existing.md)
   (coverage exists but is wrong/incomplete) **or**
   [create-new](../skills/skill-learner/workflows/create-new.md) (no coverage).

Hold to the four rules: **propose, never silently mutate**; capture conventions,
not public facts; **smallest home first** (a reference inside the role expert
before a new `lang-*`/`iac-*` skill — promote on evidence per the promotion
policy); and **delegate** scaffolding/refinement to the `skill-creator`, then run
the validator.

End by logging a `pending` entry to the memory ledger describing what will be
learned, and tell the user it awaits their accept before becoming canonical.
