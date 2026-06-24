# Reference: Implementation Guardrails

Use these guardrails whenever a spec-driven phase reaches implementation or writes tasks that will drive implementation.

## Purpose

Reduce common AI coding mistakes during implementation: hidden assumptions, speculative abstractions, broad refactors, unverified changes, and messy scope drift.

This is a guardrail, not a replacement for the host workflow's implementation step. Apply it lightly for trivial changes and more explicitly for multi-file, risky, or ambiguous implementation work.

## Karpathy Guardrail Summary

1. **Think before coding**: do not assume, do not hide confusion, surface tradeoffs, state assumptions explicitly, and ask when multiple interpretations would create different code.
2. **Simplicity first**: write or specify the minimum code that solves the problem. Do not add features, single-use abstractions, speculative flexibility, unnecessary configurability, or error handling for impossible scenarios.
3. **Surgical changes**: touch only what the request requires. Do not improve adjacent code, refactor unrelated code, rename things, or reformat files as cleanup. Remove only unused code created by the current change.
4. **Goal-driven execution**: turn the task into verifiable goals before editing. For bug fixes, reproduce or define the failure; for validation, name the test, build, lint, manual route, screenshot, or inspection that proves the outcome.

For multi-step implementation, state a brief plan where each step has its own verification method. If the plan starts to exceed the obvious minimum, simplify before coding.

## Starter Checks

Ask or verify before proceeding:

1. What concrete behavior or artifact proves this implementation is done?
2. What assumptions could change the code path?
3. What is the smallest scoped change that satisfies the request?

Do not block on these questions when the answers are clear from the task and local context. State assumptions briefly and proceed.

## Decision Checkpoints

Pause and surface an explicit decision when:

- two plausible interpretations would produce incompatible implementations
- the simplest fix conflicts with an approved spec, governance principle, or design decision
- the requested change implies a new abstraction, migration, or broad refactor
- verification cannot be performed and the risk is material

If a durable direction changes, create or update the relevant decision artifact instead of leaving the rationale only in chat.

## Procedure

1. Restate the implementation goal as a verifiable outcome.
2. Name material assumptions. Ask only when an assumption would materially change the solution.
3. Inspect relevant code and existing local patterns before editing.
4. Choose the smallest implementation that satisfies the request and approved artifacts.
5. Avoid speculative flexibility, new configuration, or abstractions unless they remove real current complexity.
6. Edit surgically:
   - touch only files needed for the task
   - match existing style
   - avoid unrelated cleanup or formatting churn
   - remove only unused code created by this change
7. Validate with the narrowest reliable check first, then broaden when the blast radius warrants it.
8. Report what changed, what was verified, and any assumptions, deviations, or follow-up decisions.

## Quality Rules

- No hidden confusion: surface important uncertainty instead of coding around it.
- No speculative features: implement what was asked and approved.
- No abstraction for one-off code unless the local codebase already clearly uses that pattern.
- No drive-by refactors, unrelated formatting churn, or cleanup outside the task.
- Every changed line should trace back to the request, a required integration point, or validation.
- Prefer simple, readable code over clever flexibility.
- Verification should prove behavior, not merely show that files changed.

## Stop Conditions

Stop and ask for clarification when:

- required contracts, tokens, assets, or behavior are missing and guessing would shape the implementation
- the task would require mutating approved workflow, product, or design-system doctrine
- success criteria cannot be inferred and the change is not trivial
- validation is impossible and the risk is too high to proceed silently
