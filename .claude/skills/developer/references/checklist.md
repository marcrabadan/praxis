# Pre-Merge Developer Checklist

A self-review checklist a developer runs before opening or merging a pull request. Work through every section. Flag outstanding items in the PR description rather than ignoring them.

---

## 1. Scope

- [ ] The PR addresses exactly the intended change — no more, no less.
- [ ] No unrelated refactoring, formatting changes, or dependency upgrades are mixed in.
- [ ] Every file in the diff belongs in this PR.
- [ ] The branch is up to date with the target branch; merge conflicts are resolved.

---

## 2. Tests pass

- [ ] All existing tests pass locally (`make test`, `npm test`, `pytest`, or the project equivalent).
- [ ] New code is covered by at least one test that exercises the changed behavior.
- [ ] **Team rule — test-first:** complex logic (non-trivial conditionals, calculations, parsing/serialization, state machines, concurrency, security-sensitive paths) had its unit tests written *before* the implementation, and a bug fix includes the regression test that failed before it.
- [ ] Edge cases are covered: empty inputs, boundary values, error paths, and unexpected inputs.
- [ ] No tests have been skipped or disabled to make the suite green.
- [ ] Integration or end-to-end tests that touch the changed path have been run (or a reason is noted why they were not).

---

## 3. Code quality

- [ ] No dead code: unused variables, unreachable branches, or commented-out code are removed.
- [ ] **Team rule — no non-functional inline comments:** no narrative comments; every non-functional comment that remains states a constraint the code cannot express (invariant, external requirement, deliberate trade-off, security warning). Tool directives (`noqa`, `eslint-disable`, pragmas) are fine, scoped as narrowly as possible.
- [ ] No debug output (`console.log`, `print`, `fmt.Println`, breakpoints) left in the code.
- [ ] Names are clear and consistent with surrounding code.
- [ ] Functions do one thing; any function that grew during this change is still within reason.
- [ ] No obvious duplication that violates DRY without a stated reason.
- [ ] Code matches the surrounding style (indentation, naming conventions, error-handling patterns).

---

## 4. Error handling

- [ ] Every failure path either surfaces an informative error to the caller or logs with enough context to diagnose in production.
- [ ] No empty catch blocks or silently swallowed exceptions.
- [ ] External inputs (HTTP request bodies, CLI arguments, file content) are validated at the boundary before use.
- [ ] Functions return typed errors or typed optionals where the language supports it; `null` or `undefined` is not used as a hidden failure signal.

---

## 5. Security

- [ ] No secrets, API keys, passwords, or tokens are committed to source control.
- [ ] All user-controlled or external input is validated before use in a query, filesystem path, or template.
- [ ] Database queries use parameterized statements or an ORM — no string concatenation with user input.
- [ ] Output rendered in HTML, XML, or other structured formats is encoded correctly.
- [ ] File paths and names from external sources are sanitized; path-traversal patterns are rejected.
- [ ] New dependencies added in this PR are intentional, known to be maintained, and not carrying known vulnerabilities.

---

## 6. Performance

- [ ] No N+1 query patterns introduced (loading a collection then issuing one query per item).
- [ ] Loops over large collections do not contain expensive nested operations without a stated rationale.
- [ ] Any caching added includes a note on the invalidation strategy.
- [ ] Any performance trade-off taken is named in a comment.

---

## 7. Commit hygiene

- [ ] Each commit is a single logical change that passes tests on its own.
- [ ] Commit messages use the imperative mood and explain the why, not just the what.
- [ ] No merge commits from the base branch in the middle of the feature branch (rebase or squash as team convention dictates).
- [ ] No temporary commits ("wip", "fix", "asdf") are visible in the final history.

---

## 8. Documentation

- [ ] Public APIs and exported functions have up-to-date docstrings (interface documentation — the comment-free rule does not apply to them).
- [ ] Any user-facing behavior change is reflected in the relevant README, changelog, or docs page.
- [ ] Architecture decision records (ADRs) are updated if a significant architectural decision was made — design rationale lives there, not in inline comments.
- [ ] No inline `TODO` or `FIXME` comments remain; outstanding work is tracked in tickets.

---

## 9. PR description

- [ ] The description explains what changed and why, not just a list of file names.
- [ ] The related ticket or issue is linked.
- [ ] The test or verification approach is described (automated test, manual step, screenshot, or log snippet).
- [ ] Non-obvious design decisions are explained so reviewers do not need to ask.
- [ ] Known limitations or follow-up items are listed if they will not be addressed in this PR.

---

## 10. Final gate

- [ ] The CI pipeline is green (or failures are understood and unrelated to this change).
- [ ] At least one reviewer has been assigned (or the PR is explicitly draft / not-for-review).
- [ ] The author has read the entire diff one more time as a reviewer would, top to bottom.
