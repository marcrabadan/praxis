# Reference: Interview Protocol

Use this local protocol whenever the skill needs missing context. It is bundled so the skill can run without another interview skill.

## Purpose

Run a structured, adaptive interview that starts from the user's objective and proceeds one useful question at a time until the objective is complete.

The interview does not replace the domain method. It collects the answers this skill needs for the artifact map, idea brief, governance principles, spec, clarification, plan, tasking, or implementation grounding.

## Starting Protocol

At the start, identify:

1. **Objective**: what final understanding, decision, artifact, or saved knowledge is needed.
2. **Output**: whether the result is conversational only or should be saved.
3. **Scope**: which product, workflow, feature, repo, or decision space the interview concerns.
4. **Completion signal**: what must be answered before the interview is done.

If the user already provided any of these, do not ask again. Ask only for missing information that affects the next useful question.

## Question Format

Ask exactly one question at a time.

Use this format by default:

```text
Question: <specific question>

Suggested answers:
- A. <realistic option with consequence> (recommended)
- B. <realistic option with different consequence>
- C. <realistic option with different consequence>
- Or answer in your own words.
```

For every question with suggested answers, mark the single option you would recommend by appending " (recommended)" to it. Recommend exactly one option per question. If you genuinely cannot recommend one, briefly say why instead of marking any.

Do not force false choices. Make clear that the user can edit, combine, reject, or answer freely.

## Interview Loop

Repeat:

1. Ask the highest-leverage next question.
2. Wait for the user's answer.
3. Interpret the answer into concrete facts, decisions, preferences, rules, constraints, examples, or open questions.
4. Register the interpreted answer before asking the next question.
5. Keep a running interview state.
6. Briefly reflect the captured point when useful.
7. Ask a follow-up if it materially improves the objective.
8. Move to the next main question when the current branch is sufficiently understood.

## Answer Registration Rule

Do not ask the next question until the previous answer has been registered.

Registration means:

- In chat, state the captured answer briefly before the next question.
- In the running interview state, update confirmed facts, decisions, preferences, constraints, examples, and open questions.
- If the interview has a clear artifact target, persist the answer to that artifact before asking the next question.

When persisting answers:

- keep entries concise
- preserve the user's raw intent when wording matters
- translate vague or risky language into safer working language only as a separate interpretation
- mark unresolved ambiguity as open
- avoid turning tentative answers into final decisions unless the user clearly committed

## Follow-Up Rules

Ask follow-up questions when they would improve the outcome:

- broad answers that need a concrete example
- strong preferences without rationale
- contradictions or tradeoffs
- threshold, exception, or consequence
- claims that should become a principle or decision

Good follow-ups ask why it matters, what happens if it is wrong, when the rule stops applying, what proves it, what the opposite case looks like, or how the user would explain it to someone else.

Do not over-interrogate. If a follow-up is only curiosity, skip it.

## Challenge Behavior

Do not agree automatically.

Challenge politely when:

- the answer conflicts with an earlier answer
- the user is choosing a vague direction where the artifact needs precision
- a claim is too strong for the evidence
- the answer creates downstream implementation or communication problems

When challenging, state the conflict or risk briefly and ask which direction should win.

## Ending The Interview

End when the objective is genuinely satisfied.

Before finalizing, provide:

- what was decided or learned
- what remains open
- what was saved, if anything
- recommended next host workflow step, if obvious

## Quality Rules

- Ask one question at a time.
- Register every answer before asking the next question.
- Keep questions high-leverage.
- Offer suggested answers by default.
- Recommend exactly one option per question, or say why you cannot.
- Adapt follow-ups to the user's latest answer.
- Track decisions and open questions.
- Preserve ambiguity instead of pretending it is resolved.
- Do not turn the interview into a form unless the user asks for a fixed questionnaire.
