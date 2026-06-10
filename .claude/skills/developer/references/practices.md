# Developer Practices

Core engineering principles and techniques for writing, testing, refactoring, and reviewing code across the SDLC.

---

## 1. Clean code and readable naming

Readable code is the default; clever code is the exception that must justify itself.

### Naming
- Name variables, functions, and types after what they represent in the domain, not after their implementation mechanics. Prefer `invoiceTotal` over `val2`, `processPayment` over `doStuff`.
- Boolean names carry a positive predicate: `isActive`, `hasPermission`, `canRetry`. Avoid negations like `isNotDisabled`.
- Functions that return values are named as nouns or noun phrases (`userId()`). Functions with side effects are named as verbs (`saveOrder()`).
- Avoid abbreviations unless they are universally understood in the codebase (e.g. `id`, `url`). Expand the rest.
- If a name needs a comment to be understood, rename it instead.

### Function and method hygiene
- A function does one thing. If its name contains "and", split it.
- Keep functions short enough to read without scrolling. There is no hard rule; use judgment calibrated against readability, not line count.
- Prefer fewer parameters. Beyond three or four, group related parameters into a named struct or object.
- Avoid flag parameters (`process(order, true)`). Model the two behaviors as two named functions.

### Comments — team rule: no non-functional inline comments
- **Default: no inline comments.** Code self-explains through names, small functions, and structure. Needing a comment to explain *what* code does is a refactoring signal — rename or extract until the comment is unnecessary.
- **Functional comments are not commentary.** Directives the toolchain consumes — `# noqa`, `// eslint-disable`, `@ts-ignore`, pragmas, coverage markers — are code; use them when needed, each scoped as narrowly as possible and never to mute a warning that should be fixed.
- **The one permitted informative comment** states a constraint the code cannot express: a non-obvious invariant, an external or legal requirement, a deliberate trade-off, or a security warning. One line, stating the *why*.
- Design rationale lives in ADRs (`docs/decisions/`), never inline. Docstrings on public/exported APIs are interface documentation, not narrative comments — they stay.
- Delete commented-out code (source control preserves history) and inline `TODO`/`FIXME` markers (track them in tickets).
- Keep the rare permitted comment current. A stale comment is worse than none because it actively misleads.

---

## 2. SOLID, DRY, and YAGNI applied pragmatically

These principles are heuristics, not laws. Apply them when the benefit is clear; do not apply them speculatively.

### SOLID
- **Single Responsibility:** a module or class has one reason to change. When a file is pulled in opposite directions by two different teams or features, split it.
- **Open/Closed:** extend behavior by adding new code (subclasses, strategies, plugins) rather than by modifying existing code that already works and is tested.
- **Liskov Substitution:** a subtype must behave consistently with the contract of its parent. Violating LSP produces surprises at runtime that type checkers cannot catch.
- **Interface Segregation:** depend on the narrowest interface that satisfies the caller's needs. Fat interfaces create unnecessary coupling.
- **Dependency Inversion:** depend on abstractions, not concrete implementations. This makes components independently testable and swappable.

### DRY (Don't Repeat Yourself)
- Extract duplication when three identical or structurally identical fragments exist and are clearly the same concept. Two copies can be a coincidence.
- DRY applies to *knowledge*, not just text. Two pieces of code that look similar but represent different concepts should stay separate.
- Over-applying DRY produces premature abstractions that are harder to change than the duplication they replaced.
- Default thresholds: keep duplicated lines under ~3% of a file and cyclomatic/cognitive complexity of a function under ~10/15 (see `rules/code-quality-metrics.md`, or the repo's configured quality gate). Treat repeated trips above either as a signal to extract or simplify, not just a number to track.

### YAGNI (You Aren't Gonna Need It)
- Do not build for requirements that do not yet exist. Speculative features add complexity, maintenance cost, and testing surface with no near-term payoff.
- If a future need is likely and cheap to accommodate, leave an extension point but do not implement the extension.
- Delete code that is no longer called. If it is needed later, source control retrieves it.

---

## 3. Test-first / TDD and the test pyramid

Tests are the safety net that makes change safe. Writing them before the code sharpens thinking about the interface before the implementation locks it in.

### Team rule: test-first for complex logic
- **Before implementing complex logic, write the unit tests first** (red → green → refactor). "Complex" is observable, not a feeling: non-trivial conditionals, calculations (money, dates, rounding), parsing/serialization, state machines, concurrency, and security-sensitive paths (authn/authz, input validation, crypto). Every bug fix starts with the failing regression test.
- Trivial glue, configuration, or passthrough code may be tested with or after the change — but **no complex logic merges without unit tests** covering positive, negative, and boundary cases.
- If the test is hard to write, the interface is wrong; discovering that before the implementation exists is the point of writing the test first.

### Test-first workflow
1. Write a failing test that expresses the desired behavior clearly.
2. Write the minimal code that makes it pass. Resist adding more than the test requires.
3. Refactor the implementation (and the test if needed) until both are clean.
4. Repeat.

The test is the specification. If the test is hard to write, the interface is usually wrong.

### Test pyramid

| Layer | What it tests | Speed | Count |
|-------|--------------|-------|-------|
| **Unit** | A single function, class, or module in isolation. Dependencies are replaced with fakes or stubs. | Milliseconds | Many (majority of the suite) |
| **Integration** | Two or more real components working together — a service and its database, an HTTP handler and its repository. | Seconds | Moderate |
| **End-to-end / contract** | The full system from an external boundary. Run less often; flag regressions not caught below. | Minutes | Few |

- Keep unit tests pure: no file I/O, no network, no clock unless specifically injecting them.
- Integration tests may hit real databases or services but should run against a local or ephemeral instance, not production.
- A test that is slow, flaky, or depends on global state is a maintenance liability; fix or delete it.

### Writing good tests
- Name the test after the behavior it verifies: `calculatesTaxOnInternationalOrders`, not `test1`.
- Structure tests as Arrange / Act / Assert (or Given / When / Then). One assertion per test is a guideline; group assertions that together constitute one behavioral claim.
- Test edge cases: empty input, boundary values, error paths. Happy-path-only suites give false confidence.
- Do not test implementation details. Test observable behavior (return values, side effects, emitted events). Tests that break when internals are refactored are the wrong tests.
- Prefer real objects to mocks where performance allows. Mocks that encode implementation assumptions make refactoring harder.

---

## 4. Small, focused commits and good commit messages

Commits are the audit trail. Each commit should express one coherent change that a reviewer can understand in isolation.

### Commit scope
- One logical change per commit. "Fix bug" and "add feature" are not one commit.
- A commit should pass all tests on its own. Bisecting a broken build is frustrating; broken-commit histories make it impossible.
- Separate refactoring commits from behavior-change commits. Mixed commits obscure what actually changed behavior.

### Commit message format
```
<subject line: imperative mood, under 72 characters>

<optional body: explain WHY, not WHAT; wrap at 72 characters>

<optional footer: references to tickets, issues, or breaking changes>
```

- Use the imperative mood: "Add retry logic" not "Added retry logic" or "Adds retry logic".
- The subject line completes the sentence "If applied, this commit will: ___."
- The body explains the motivation and any constraints the code alone cannot express.
- Reference the issue tracker ticket where relevant (e.g. `Closes #123`).

### What not to put in a commit
- Do not mix unrelated changes. "Fix payment bug and update README and reformat logger" is three commits.
- Do not commit half-finished work to a shared branch. Use a feature branch, stash, or draft commit.
- Do not commit secrets, credentials, generated build artifacts, or large binary blobs.

---

## 5. Branch and PR hygiene

Short-lived branches and small pull requests reduce merge conflicts and accelerate review.

### Branch naming
- Use a consistent convention: `type/short-description` (e.g. `feat/add-retry-logic`, `fix/null-pointer-on-empty-cart`, `chore/upgrade-deps`).
- Branch names are lowercase, hyphen-separated, and descriptive enough to understand without opening the PR.
- Delete branches after merging. Stale branches are noise.

### PR sizing
- A PR should express one coherent change. If the reviewer needs to understand two independent features to review it, split the PR.
- Target under 400 lines of meaningful change per PR as a rule of thumb. Larger PRs get shallower reviews.
- Prerequisite refactoring goes in its own PR ahead of the feature PR. Stack PRs when dependencies are unavoidable.

### PR descriptions
- Summarize what changed and why in one paragraph. Link to the relevant ticket or spec.
- List the non-obvious decisions made and why. Save reviewers from asking questions that already have answers.
- Note how the change was tested: which tests were added, which manual checks were performed.
- Highlight areas where feedback is especially wanted.

### Self-review before requesting a review
- Read the diff as a reviewer would before assigning anyone.
- Remove debug output, `console.log`, `TODO`s that belong in tickets, and commented-out code.
- Confirm that every file in the diff should be in this PR.
- Run the tests and linter locally before pushing.

---

## 6. Reading code before changing it

Understanding before acting prevents regressions and preserves intent.

- Read the function, module, or class being modified in full before writing any new code.
- Identify the invariants: what is the function expected to always be true about its inputs, outputs, and state?
- Note the existing style: indentation, naming conventions, error-handling patterns, logging conventions. Match them.
- Run the existing tests to confirm they pass before touching anything.
- Understand why the code is the way it is before judging it. There may be a constraint comment, a git blame entry, or a linked issue that explains the apparent oddity.

---

## 7. Refactoring safely behind tests

Refactoring is changing the structure of code without changing its observable behavior. The test suite is the proof.

### Refactoring discipline
- Do not refactor and change behavior in the same commit. These are separate concerns.
- Ensure test coverage is adequate for the code being refactored before starting. If it is not, add tests first.
- Make one refactoring move at a time (extract method, rename variable, inline variable, move module). Run tests after each move.
- Prefer small, mechanical transformations to large freehand rewrites. Mechanical steps have known failure modes; rewrites introduce new ones.

### Common safe refactoring moves
- **Extract function:** isolate a named block of code into its own function when it can be understood independently.
- **Rename:** rename to better express intent. Rely on tooling to rename across the codebase atomically.
- **Inline:** replace a function call with its body when the indirection adds no clarity.
- **Extract variable:** assign a complex expression to a descriptively named variable.
- **Move:** relocate a function or module to the package that conceptually owns it.

### When not to refactor
- Do not refactor code you do not have to touch to deliver the current task. Unsolicited refactoring creates review burden and merge conflicts.
- Do not refactor without tests unless the code is trivially simple and you are adding tests as part of the work.

---

## 8. Error handling and defensive boundaries

Errors are part of the contract, not an afterthought.

### Principles
- Fail fast and loudly at the point where invalid state is detected. Silent failures propagate and surface far from their cause.
- Every function that can fail should communicate its failure mode clearly: exception type, error code, or typed error return.
- Distinguish between expected errors (invalid input, network timeout) and unexpected errors (bugs, assertion failures). Handle them differently.
- Do not swallow exceptions with empty catch blocks. At minimum, log the cause.
- Validate inputs at the boundary of the system (HTTP request, CLI argument, file read) and at the boundary of each module that cannot trust its callers.

### Error message quality
- Name the specific input or condition that caused the failure.
- Suggest the likely fix if it is knowable without the user needing to dig.
- Include correlation IDs or trace context in logged errors so they can be found in production.

### Defensive boundaries
- External inputs are untrusted until validated. Model validation with typed objects or schema validators rather than ad-hoc if-chains.
- Avoid returning null or undefined as a sentinel when a typed Optional or Result type communicates the absence more clearly.
- When a function cannot proceed, fail immediately rather than returning a partial result the caller must inspect.

---

## 9. Performance awareness without premature optimization

Measure before optimizing. Optimize where the evidence points.

- Write correct code first. Optimize only after profiling shows that a specific path is a bottleneck.
- Understand the algorithmic complexity (O notation) of the chosen approach. A quadratic algorithm on a large input is almost always wrong, even before profiling.
- Avoid micro-optimizations that reduce readability without a measured payoff.
- Database access patterns are the most common performance bottleneck. Prefer indexed lookups over sequential scans; avoid N+1 query patterns.
- Cache only when profiling confirms the need; caching adds correctness complexity (invalidation, consistency) that must be maintained.
- If you take a performance shortcut, name it explicitly in a comment so the next engineer knows it is intentional and the conditions under which it is valid.

---

## 10. Security basics

Security failures are bugs with greater consequence. Apply these practices by default.

### Input validation and injection prevention
- Validate all external input at the system boundary: type, range, length, format, and character set.
- Use parameterized queries or ORMs for database access. Never concatenate user input into SQL.
- Encode output before rendering in HTML, XML, or other structured formats. Do not trust that stored data is safe.
- Validate and sanitize file paths and names before use. Reject path-traversal patterns (`..`).

### Secrets handling
- Never commit secrets, API keys, passwords, or tokens to source control. Use environment variables or a secrets manager.
- Rotate any secret that was accidentally committed immediately; a force-push does not erase it from forks and clones.
- Do not log secrets. Scrub credentials from log output before writing.
- Prefer short-lived credentials over long-lived ones. Prefer the principle of least privilege: grant only the permissions the code actually needs.

### Dependency and surface area
- Keep dependencies up to date. Outdated packages are the most common source of known vulnerabilities.
- Minimize the attack surface: disable unused endpoints, remove unused dependencies, close unused ports.
- Prefer well-maintained, audited libraries over custom implementations of cryptographic or authentication logic.

---

## 11. Code review etiquette

Code review is a collaborative quality activity, not a gatekeeping ceremony.

### Giving feedback
- Distinguish severity: **nit** (style preference, take or leave it), **suggestion** (improvement, author's call), **must-fix** (correctness bug, security risk, or architectural problem).
- Frame observations as questions or explanations, not commands: "Could this fail with an empty list?" rather than "Handle the empty list."
- Comment on the code, not the author. Avoid "you" statements.
- Acknowledge good work where it exists. Feedback that is exclusively negative creates a hostile review culture.
- Ask for clarification before flagging something as wrong. The author may know something you do not.

### Receiving feedback
- Read every comment before responding or making changes. Some comments address the same root cause.
- Do not take review comments personally. The reviewer is trying to improve the codebase.
- If you disagree with a must-fix comment, discuss the tradeoff explicitly. Do not silently ignore it.
- Respond to every comment — even if only with "Done" or "Discussed offline." Leaving comments unaddressed stalls the merge.
- Apply changes in a new commit during review; do not rewrite history mid-review unless the team has agreed to it.

### Scope of a review
- Reviewers should not redesign the PR from scratch. If a fundamental approach is wrong, raise it early and discuss before the implementation is done.
- Stay in scope: a review of a payment module is not the place to refactor the logging utilities it imports.
- Approve when the code is good enough to ship. Perfect is not the criterion; shippable and better than before is.
