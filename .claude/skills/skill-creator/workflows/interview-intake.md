# Interview Intake Workflow

Capture everything the generator and the rest of the skill-creator need before writing any files. This workflow is the **entry point** for any new-skill request and is also used when an existing skill is being substantially rewritten.

## When to run

- The user says "I want a skill for X" or anything similar.
- The user provides a skill request but is missing purpose, trigger context, output format, audience, or rules.
- An existing skill review reveals the original brief is missing.

## When to skip

- The user has already provided a complete `skill-brief.md` and explicitly asks to skip the interview.
- The user is asking a one-off question about skills, not creating one.

If in doubt, run the interview. It is cheap; guessing is expensive.

## Protocol

This workflow uses the **interview protocol** in [interview.md](interview.md):

- **One question at a time.** Do not batch.
- **Suggested answers** with each question (A / B / C / Or in your own words), unless the answer must be free-form.
- **Follow-ups** when an answer reveals a strong preference, contradiction, or interesting detail. Use the follow-up triggers in interview.md.
- **Running state.** Update `skill-brief.md` after each meaningful answer. Do not wait until the end.
- **Challenge contradictions.** Do not agree automatically. If an answer conflicts with a prior one, name the conflict.

If the agent host supports a structured-question UI (e.g. Claude Code's AskUserQuestion tool), prefer it over plain-text suggested answers — one question at a time, with realistic suggested answers.

## The question set

Ask these questions in order. Skip any the user has already answered. After each meaningful answer, append the captured fact to `skill-brief.md`.

### Q1 — Purpose

> What should this skill enable the agent to do? Describe it in one sentence.

Suggested answers (offered as examples; user will likely answer in their own words):

- A. "Generate X from Y."
- B. "Apply rules A, B, C to Z."
- C. "Run a guided procedure that produces W."
- D. Free-form.

Follow-up if the answer is broad: ask for a concrete example of input and expected output.

### Q2 — Trigger context

> When should the agent automatically invoke this skill? Give me the user phrases or situations that should activate it.

Suggested answers:

- A. The user mentions specific keywords (provide them).
- B. The user is in a specific file/folder or working with a specific file type.
- C. The user explicitly invokes the skill by name.
- D. Free-form.

Follow-up: ask for one near-miss situation where the skill should **not** trigger.

### Q3 — Output format

> What does the skill produce?

Suggested answers:

- A. A markdown file or section.
- B. Source code in a specific language.
- C. Structured machine-readable data (JSON, YAML, CSV).
- D. A diff or patch against existing files.
- E. Conversational guidance only (no file output).
- F. Free-form / combination.

Follow-up: if files, ask where they should land (a specific folder or a configurable path).

### Q4 — Invocation

> Should this skill auto-trigger from natural-language requests, or only when explicitly named?

Suggested answers:

- A. Auto-trigger (default) — Claude Code loads it whenever the description matches the request.
- B. Explicit only — set `disable-model-invocation: true` so it loads only when named or read by tool.

Most skills want A. Reserve B for skills that are risky to fire unprompted.

### Q5 — Rules, preferences, constraints

> Are there specific rules, conventions, or constraints the skill must enforce? Things like naming, file structure, accessibility, tone, security, formatting.

Suggested answers:

- A. Yes — let me list them.
- B. No specific rules; just follow general best practices.
- C. Use rules from an existing document (provide path).

Follow-up: ask for one example where the rule applies and one near-miss where it does not.

### Q6 — Examples to mimic

> Are there existing examples — files, snippets, past outputs — the agent should learn from?

Suggested answers:

- A. Yes, here are paths.
- B. Yes, I'll paste them.
- C. No, the skill is novel.

Follow-up: if examples are provided, ask which aspects matter (structure? wording? both?).

### Q7 — Code production

> Does this skill generate, modify, or validate code or structured machine-readable output?

Suggested answers:

- A. Yes — it produces code.
- B. Yes — it produces structured data (JSON/YAML/CSV).
- C. No — it produces prose or guidance.

This answer **gates Tier 4 vs lower**. If yes, the produced skill will need `scripts/` and `evals/`, and must follow [`ai/implementation-principles.md`](../../../factory/ai/implementation-principles.md).

### Q8 — Reuse expectation

> How often do you expect this skill to be triggered?

Suggested answers:

- A. Frequently — every day or every session.
- B. Occasionally — a few times per week.
- C. Rarely — once or twice.
- D. Unknown.

This answer **feeds the Tier 5 promotion check**. Frequent triggers + risk of regression = Tier 5 candidate.

### Q9 — Packaging target

> Where will this skill live?

Suggested answers:

- A. Project Claude Code skill (`.claude/skills/<name>/` in this repo) — the default for a shared, factory-owned skill.
- B. Personal Claude Code skill (`~/.claude/skills/<name>/`) — available across all your projects.
- C. Just experimenting; scaffold under `dist/<name>/` and decide later.

## The brief artifact

Maintain a running `skill-brief.md` in the target output directory (default `dist/<slug>/skill-brief.md`). Use this format:

```markdown
---
name: <slug>
title: <Title Case>
tier: <1-5, or "pending">
invocation: <auto-trigger / explicit-only>
created: <YYYY-MM-DD>
---

# Skill Brief: <Title Case>

## Purpose
<one sentence>

## Trigger context
- <phrases / situations>
- <negative trigger>

## Output format
<file types, paths, structure>

## Audience
<which agents>

## Rules and constraints
- <rule>
- <rule>

## Examples to mimic
- <path or pasted snippet>

## Produces code?
<yes / no — implications for tier>

## Reuse expectation
<frequency>

## Packaging target
<location>

## Open questions
- <anything still unresolved>

## Assumptions
- <any the agent made because the user did not specify>

## Iterations
<!--
Appended by workflows/capture-iteration.md when the user iterates on a previous
output and chooses to register the change as a rule for THIS skill. Each entry:

- YYYY-MM-DD — <imperative restatement of the rule>. Reason: <one-line context>.
-->
```

Update this file after each meaningful answer. Preserve uncertainty as "Open questions" rather than guessing.

## Completion

The intake is complete when the brief has answers (or explicit "skipped" / "not applicable") for Q1–Q9, and any open questions either have answers or are explicitly deferred.

When done, hand off to [classify-tier.md](classify-tier.md).

## Naming convention

Derive the skill `name` (slug) from the purpose:

- lowercase;
- hyphens between words;
- 2–4 words is ideal;
- max 64 characters;
- matches `^[a-z0-9-]{1,64}$`.

If the user provides a slug, validate it against the pattern. If not, propose one and confirm with the user before writing files.
