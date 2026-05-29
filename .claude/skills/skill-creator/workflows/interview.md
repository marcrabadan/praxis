# Interview Workflow

General-purpose, goal-directed interview for any objective — not only skill creation. Use when the user knows the **outcome** they want but not the starting structure.

For **creating a new skill**, prefer [interview-intake.md](interview-intake.md) after reading this protocol — it adds the skill-specific question set on top of the behavior here.

## When to run

- The user asks to run `/interview` or wants a guided Q&A to clarify an objective.
- The user has a goal but missing structure: requirements, rules, strategy, content, decisions.
- Before any substantial authoring when intent is incomplete and the task is **not** already covered by interview-intake.

## When not to run

- The user is creating a skill and has not yet been through interview-intake — use [interview-intake.md](interview-intake.md) instead (it embeds this protocol plus the skill brief questions).
- The user asked a single factual question with a clear answer.

## Core behavior

Run a structured interview that starts from the user's objective and proceeds through focused questions until the objective is complete.

The user may provide only an objective. If a target output path, format, audience, or scope is missing, ask before assuming. Keep the interview moving by offering suggested answers the user can accept, reject, or edit.

## Starting protocol

At the start, identify:

1. **Objective** — what final understanding, decision, artifact, or saved knowledge the user wants.
2. **Output** — conversational only, or saved to a file/folder.
3. **Scope** — domain, project, product, person, design system, or decision space.
4. **Completion signal** — what "done" means for this objective.

If the user already provided any of these, do not ask again. Ask only for missing details that affect the next step.

## Question style

Ask exactly **one question at a time**. Wait for the user's answer before asking the next question.

For each question, include suggested answers unless the answer must be free-form. Suggested answers should be realistic and mutually distinct.

```text
Question: <specific question>

Suggested answers:
- A. <reasonable option>
- B. <reasonable option>
- C. <reasonable option>
- Or answer in your own words.
```

Do not make the user choose from false options. Make it clear they can edit, combine, or reject suggestions.

If the agent host supports a structured-question UI (e.g. Claude Code's AskUserQuestion tool), prefer it over plain-text suggested answers.

## Interview loop

Repeat:

1. Ask the highest-leverage next question.
2. Interpret the answer into a concrete decision, fact, preference, rule, or open question.
3. Register the captured data in running interview state.
4. Briefly reflect the captured point when useful.
5. Ask a follow-up when the answer is interesting but still incomplete.
6. Ask the next main question when the current branch is sufficiently understood.

Keep a running model of: confirmed facts, explicit preferences, unresolved ambiguity, decisions still needed, target artifact shape.

When there is a saved-output target, update the draft artifact after meaningful answers instead of waiting until the end, unless the user asks to defer. Preserve uncertainty as open questions.

When the user pushes back, engage directly. If an answer conflicts with a prior decision, call out the conflict and ask which should win.

## Follow-up questions

Ask follow-ups when they would deepen understanding or improve the final output:

- broad answer needs a concrete example;
- strong preference without the reason;
- contradiction, tension, or tradeoff;
- mention of a person, product, workflow, or rule that seems important;
- answer would be more useful as a principle, constraint, or story;
- answer affects what should be saved, omitted, or emphasized.

Good follow-ups ask for: why it matters, a concrete example, the opposite case, the consequence of getting it wrong, the threshold where the rule stops applying, how the user would explain it to another person.

Do not over-interrogate. Skip follow-ups that only satisfy curiosity.

## Saving outputs

If the user asks to save the outcome, create or update the target file only after enough decisions are confirmed.

Before editing files, state what you are about to write and where. If the target path is ambiguous, ask. If the target file already exists, read it first and preserve unrelated content.

Use the repo's existing content style and folder conventions.

## Ending the interview

End when the objective is genuinely satisfied, not merely when many questions have been asked.

Before finalizing, provide a short synthesis:

- what was decided or learned;
- what was saved, if anything;
- what remains open, if anything.

If the interview produced a file, include the file path in the final response.

## Common uses

- deriving design-system rules from token files and user preferences;
- documenting professional profile information;
- turning vague goals into requirements;
- clarifying product strategy or UX direction;
- extracting personal preferences or working principles;
- preparing structured Markdown knowledge for a knowledge repo;
- capturing inputs before skill creation (then hand off to [interview-intake.md](interview-intake.md) if the outcome is a new skill).
