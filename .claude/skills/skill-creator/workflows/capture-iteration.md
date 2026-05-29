# Capture-Iteration Workflow

When the user iterates on a skill the agent just produced — "fix this", "change that", "actually no...", "next time always do X" — pause and ask whether the change should be captured **as a durable rule** for the skill (or for the skill-creator itself), not just applied silently.

This workflow turns one-shot corrections into accumulated knowledge. Without it, the same correction gets re-applied every time, and the skill never improves.

## When to run

Run this workflow inline, **after any output from another workflow** in this skill (create / review / evaluate), whenever the user's next message is corrective rather than additive. Examples that trigger this workflow:

- "fix the description, it should mention Excel too"
- "the rules.md is too strict — remove the part about X"
- "actually the trigger phrases should include casual phrasings"
- "no, the output should be JSON, not YAML"
- "from now on, every skill you create should have a section called Y"
- "I don't like that — try again"

Do **not** run this workflow when:

- the user is asking a clarifying question;
- the user is approving the output ("looks good", "ship it");
- the user is adding a new requirement that did not exist before (that goes back into the create / review flow, not into rule capture).

## The two destinations

Iteration feedback can be captured in one of two places. Decide which before asking.

### A. Rules for THIS skill

The feedback applies only to the specific skill the agent just produced. Examples:

- "the description should mention Excel" → captured in this skill's `SKILL.md` description and in `references/rules.md`.
- "remove the part about MUST in rules.md" → captured by editing this skill's `references/rules.md`.
- "the trigger phrases should include 'spreadsheet review'" → captured in this skill's `description` and `evals/trigger-evals.json`.

This is the **common case**. The destination is a file inside the produced skill folder.

### B. Meta-rules for the SKILL-CREATOR

The feedback is about how the skill-creator itself should behave — applicable to every skill it produces from now on. Examples:

- "from now on, always include a 'Stop conditions' section even for Tier 1 skills"
- "stop suggesting 'TODO' placeholders in descriptions; ask me to write the real text instead"
- "every produced skill should have an evals/trigger-evals.json by default, even Tier 2"
- "always ask the user about packaging target before classifying tier"

This is the **rarer but higher-leverage** case. The destination is a file inside `.claude/skills/skill-creator/references/` (typically `learned-rules.md`, created on first such capture) or a workflow file in `.claude/skills/skill-creator/workflows/`.

Meta-rules become part of the factory permanently and affect future runs. Be conservative about accepting them.

## Detection heuristics

The agent should treat the user's message as iteration feedback when it contains any of:

- corrective verbs: "fix", "change", "rewrite", "remove", "drop", "shorten", "lengthen", "make it more...", "make it less...";
- negation: "no,", "actually", "wait,", "that's wrong", "I don't want";
- "next time" / "from now on" / "always" / "never" phrasing (strong signal of meta-rule);
- a contradiction of a decision captured earlier in the same session;
- a request to re-do the previous step.

A purely additive message ("also add support for Excel files") is not iteration — it is a new requirement, and goes through the normal create/review flow.

If the signal is ambiguous, ask one clarifying question before proceeding.

## Procedure

### 1. Pause and acknowledge

Do not silently apply the change. Read it back briefly so the user can confirm you understood:

```
You'd like me to <restate the change>. Before I make it, one question:
```

### 2. Ask the capture question

Ask exactly one question, with structured options. If the agent host has a structured-question UI (Claude Code's AskUserQuestion tool), use it. Otherwise present the options in prose.

**Default form when the destination looks like THIS skill:**

> Should I register this as a durable rule for the **<skill-name>** skill, so future regenerations and reviews carry it forward — or apply it only this once?
>
> Options:
> - A. Register as a rule (update `dist/<skill-name>/references/rules.md` or `SKILL.md`).
> - B. Apply this once. Do not record it.
> - C. Register as a meta-rule for the skill-creator (applies to every skill from now on).
> - D. Let me phrase it differently first.

**Default form when the destination clearly looks like the SKILL-CREATOR (e.g. user says "from now on always..."):**

> That sounds like a rule for the skill-creator itself, not just for **<skill-name>**. Should I:
>
> - A. Add it as a meta-rule (skill-creator's `references/learned-rules.md`).
> - B. Add it to **<skill-name>** only.
> - C. Apply once, do not record.

### 3. Capture (only after the user confirms)

Based on the answer:

- **A — rule for this skill.** Append the rule to the produced skill's `references/rules.md` (creating the file and the folder if the skill is Tier 1; the act of capturing one rule may justify promoting from Tier 1 → Tier 2). Phrase the rule in imperative tense ("Description must mention Excel.") and include a short why ("So Excel users find the skill via trigger search."). Then apply the change.

- **B — apply once.** Edit the relevant file(s) to apply the change. Do not write a rule. Note in the session summary that the change was applied without being durable.

- **C — meta-rule for skill-creator.** Append the rule to `.claude/skills/skill-creator/references/learned-rules.md` (create the file on first capture). Phrase as imperative. Include the date and a one-line context so a future reader knows where it came from. Then apply the current change.

- **D — let me rephrase.** Wait. Do not edit anything until the user gives the final wording.

### 4. Validate

Run `validators/validate_skill.py` on the affected skill after the change. If anything fails (frontmatter length, structure), surface the failure and ask whether to fix or revert.

### 5. Update the brief

If the affected skill has a `skill-brief.md`, append a one-line entry under an "Iterations" section:

```markdown
## Iterations

- 2026-05-26 — Added rule: description must mention Excel. Reason: Excel users find the skill via trigger search.
```

This makes the skill's evolution auditable and feeds future review passes.

### 6. Re-summarize

After applying, return a compact summary:

```
Captured as: <rule for this skill | meta-rule for skill-creator | applied once>
Files updated:
- <list>
Validation: OK (or details)
```

## Skipping the prompt

A short-circuit is OK if **all** of these hold:

- the user explicitly said in the same session "don't ask me about iteration capture, just apply changes";
- the change is small (one line in `SKILL.md` or one rule);
- the destination is unambiguously the current skill, not the skill-creator.

In that case, log a one-line note in `skill-brief.md`'s Iterations section so the trail still exists.

If at any point the user says "always ask me first" again, re-enable the prompt.

## Format of `references/learned-rules.md` (skill-creator's meta-rules)

When the first meta-rule is captured, create `.claude/skills/skill-creator/references/learned-rules.md` with this header:

```markdown
# Learned Rules

Meta-rules captured from user iteration feedback. Each rule applies to every skill the skill-creator produces from the date it was captured onward, unless explicitly overridden.

Format: one bullet per rule, with a date and a one-line context.
```

Each entry:

```markdown
- 2026-05-26 — Every produced skill must include a "Stop conditions" section, even Tier 1.
  Context: User found a Tier 1 skill ambiguous about when to declare done.
```

The skill-creator reads this file at the start of every create / review session and applies the rules.

## Why this workflow exists

Without iteration capture, three things happen, none good:

1. The same correction is re-applied to every new skill the user makes (wasted effort, frustrated user).
2. The skill-creator silently drifts from the user's actual preferences without recording why.
3. The factory cannot improve. Every session starts from the same defaults.

With iteration capture:

- the user feels in control (they explicitly chose to make the change durable);
- the skill or the factory accumulates real signal over time;
- a future review pass can re-read the `learned-rules.md` and the `Iterations` sections to audit the history.

## Stop conditions

The workflow is complete when:

- the user's iteration feedback has been classified (rule for this skill / meta-rule / one-off / rephrase);
- the corresponding file has been updated (or explicitly not updated);
- the change itself has been applied;
- the validator has been re-run on the affected skill;
- a one-line entry exists in the `skill-brief.md` Iterations section (when applicable).
