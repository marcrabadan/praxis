---
id: test-strategy-idea-command
feature: /idea — idea intake & triage command
spec: projects/praxis/specs/idea-command/spec.md
plan: projects/praxis/specs/idea-command/plans/implementation-plan.md
status: draft
---

# Test Strategy — /idea intake & triage command

## 1. Scope

The `/idea` command is a single markdown command file (`.claude/commands/idea.md`) plus its plugin symlink (`plugin-praxis/commands/idea.md`) and the resulting catalog entry in `SKILLS.md`. All testing is confined to these three artefacts plus the observable runtime behaviour of the command when invoked with representative inputs.

**In scope:**
- Static analysis of the authored file against structural and content requirements.
- Behavioural dry-runs confirming the four classification paths, the clarification gate, ledger capture, and output shape.
- Regression checks confirming the catalog and integrations surfaces are not disrupted.

**Out of scope:**
- Ledger CLI internals (`ledger.py`) — those are covered by the memory-skill's own tests.
- Downstream lifecycle commands (`/new-feature`, `/fix-bug`, `/refine`) — `/idea` stops before invoking them.
- LLM non-determinism beyond the stated classification categories; the test strategy acknowledges that exact phrasing of the rationale or clarification questions is LLM-generated and not byte-compared.

---

## 2. Test approach

### 2.1 Two test layers

This feature has no traditional unit/integration/E2E pyramid because the artefact is a markdown command, not a compiled module. The applicable layers are:

| Layer | What it checks | Method |
|-------|---------------|--------|
| **Static** | The authored file satisfies all structural, content, and constraint requirements independently of any LLM invocation. | Scripted file inspection (grep, wc -l, YAML parse). These are deterministic and runnable on every commit. |
| **Behavioural** | The command, when invoked, produces the correct classification, ledger entry, output block, and stop behaviour for each category and for boundary paths. | Manual dry-runs with documented inputs and expected observable outputs. Non-deterministic in phrasing; deterministic in structure. |

### 2.2 Design techniques applied

- **Equivalence partitioning (EP):** inputs are partitioned into four classification classes (feature, bug, refinement, not-worth-doing) and two clarity states (clear enough to classify / too vague). One representative per partition.
- **Boundary value analysis (BVA):** applied to the 31–41 line budget (test at 30, 31, 41, 42); applied to the ≤2 clarifying-question limit (test exactly 0, exactly 1, exactly 2, and confirm a third is never asked).
- **Decision table:** the four-class × three-output-shapes combination (Next line present or absent; Rationale line present or absent) yields a 4-row table; all rows must be verified.
- **Negative testing:** inputs that should NOT produce a given output — e.g. `not-worth-doing` path must have no `Next:` line; `allowed-tools` must not appear; `Agent` must not appear as a tool invocation.

### 2.3 AC classification: static vs behavioural

| AC ID | Type | Criterion summary |
|-------|------|-------------------|
| AC-01 | Static | File line count 31–41 inclusive |
| AC-02 | Static | No `allowed-tools` frontmatter key |
| AC-03 | Static | `description` contains "intake and triage" |
| AC-04 | Static | `description` does not contain "plan a feature" |
| AC-05 | Static | Body does not contain `Agent` as a tool invocation |
| AC-06 | Static | Explicit static 4-category route mapping present in body |
| AC-07 | Behavioural | Feature input → `intake,feature` ledger entry + `pending` |
| AC-08 | Behavioural | Bug input → `intake,bug` ledger entry + `Next: /fix-bug` |
| AC-09 | Behavioural | Doc-update input → `intake,refinement` ledger entry + `Next: /refine` |
| AC-10 | Behavioural | Not-worth-doing input → `intake,not-worth-doing` + `Rationale:` + no `Next:` |
| AC-11 | Behavioural | Vague input triggers ≤2 `AskUserQuestion` calls |
| AC-12 | Behavioural | `Next:` argument matches `--title` in ledger entry |
| AC-13 | Static | Ledger CLI call uses `--type note` |
| AC-14 | Behavioural | No content produced after output block |
| AC-15 | Static | Ledger CLI call uses `--source /idea` |

---

## 3. Test cases

### Group S — Static checks

---

**TC-S-01**
AC ref: AC-01
Type: Boundary — lower bound (below)
Precondition: `idea.md` exists.
Steps:
  1. Run `wc -l .claude/commands/idea.md`.
  2. Check the reported line count.
Expected: Value is ≥ 31. If 30 or fewer, the file is too short — intent is underspecified.
Pass/Fail: —

---

**TC-S-02**
AC ref: AC-01
Type: Boundary — upper bound (at limit)
Precondition: `idea.md` exists.
Steps:
  1. Run `wc -l .claude/commands/idea.md`.
  2. Check the reported line count.
Expected: Value is ≤ 41. If 42 or more, the file has absorbed downstream logic (planning, spec-writing) that violates NFR-1.
Pass/Fail: —

> Note: TC-S-01 and TC-S-02 together enforce the closed interval [31, 41]. The boundary values 30 and 42 are the fail thresholds; 31 and 41 are the inclusive pass thresholds. A single assertion `31 ≤ count ≤ 41` covers both.

---

**TC-S-03**
AC ref: AC-02
Type: Negative — prohibited key
Precondition: `idea.md` exists.
Steps:
  1. Parse the YAML frontmatter of `idea.md`.
  2. Inspect the set of top-level frontmatter keys.
Expected: The key `allowed-tools` is absent. Any presence is a fail.
Pass/Fail: —

---

**TC-S-04**
AC ref: AC-03
Type: Positive — required substring
Precondition: `idea.md` exists.
Steps:
  1. Read the `description` value from frontmatter.
  2. Check for the substring "intake and triage" (case-sensitive as authored).
Expected: Substring is present. Absence is a fail (the routing layer cannot distinguish `/idea` from lifecycle commands without this anchor).
Pass/Fail: —

---

**TC-S-05**
AC ref: AC-04
Type: Negative — prohibited substring
Precondition: `idea.md` exists.
Steps:
  1. Read the `description` value from frontmatter.
  2. Check for the substring "plan a feature".
Expected: Substring is absent. Presence is a fail (description collision with `/new-feature` intent).
Pass/Fail: —

---

**TC-S-06**
AC ref: AC-05
Type: Negative — prohibited tool invocation
Precondition: `idea.md` exists.
Steps:
  1. Read the full body of `idea.md` (below the frontmatter delimiter).
  2. Search for the pattern `Agent` appearing as a tool invocation (e.g. `Agent tool`, `invoke Agent`, or `use the Agent`). A plain occurrence of the word "agent" in prose is acceptable; the constraint is against `Agent` as a tool call instruction.
  3. Also search for any `Skill` tool reference.
Expected: No `Agent` tool invocation and no `Skill` tool reference appear. Any such reference is a fail (NFR-3 — all reasoning must be inline).
Pass/Fail: —

> Exploratory note: The word "Agent" may appear in prose (e.g. "no Agent tool"). The check is for tool-invocation patterns (`use the Agent tool`, `Agent(`, `invoke Agent`), not the word in isolation. The reviewer must apply judgment; a scripted grep for `Agent tool` or `Skill tool` covers the clear cases.

---

**TC-S-07**
AC ref: AC-06
Type: Positive — static route table completeness
Precondition: `idea.md` exists.
Steps:
  1. Read the body of `idea.md`.
  2. Confirm a static table or labeled list mapping all four categories is present: `feature`, `bug`, `refinement`, `not-worth-doing`.
  3. Confirm each of the three routable categories has an explicit downstream command (`/new-feature`, `/fix-bug`, `/refine`).
  4. Confirm `not-worth-doing` has no downstream route (only a rationale instruction).
Expected: All four categories appear with correct routing; the table is static (no conditional logic, no runtime computation).
Pass/Fail: —

---

**TC-S-08**
AC ref: AC-13
Type: Positive — ledger type value
Precondition: `idea.md` exists.
Steps:
  1. Read the body of `idea.md`.
  2. Locate the ledger CLI invocation snippet.
  3. Check the `--type` argument value.
Expected: Value is exactly `note`. Any other value (e.g. `idea`, `plan`) is a fail (NFR-5).
Pass/Fail: —

---

**TC-S-09**
AC ref: AC-15
Type: Positive — ledger source value
Precondition: `idea.md` exists.
Steps:
  1. Read the body of `idea.md`.
  2. Locate the ledger CLI invocation snippet.
  3. Check the `--source` argument value.
Expected: Value is exactly `/idea`. Any other value is a fail.
Pass/Fail: —

---

**TC-S-10**
AC ref: AC-03, AC-04 (description uniqueness — NFR-6)
Type: Negative — catalog collision check
Precondition: `SKILLS.md` has been regenerated via `make catalog` after `idea.md` is installed.
Steps:
  1. Read the `/idea` row in the `## Commands` table of `SKILLS.md`.
  2. Confirm the description contains "intake and triage".
  3. Read the `/new-feature`, `/fix-bug`, and `/refine` rows.
  4. Confirm none of those three descriptions contains "intake and triage".
  5. Confirm the `/idea` description does not contain "plan a feature", "corrective lifecycle", or "quality-only improvement" (the distinguishing phrases of the lifecycle commands).
Expected: `/idea` description is unique and unambiguous relative to the three lifecycle commands. Any description overlap is a fail.
Pass/Fail: —

---

**TC-S-11**
AC ref: AC-02, AC-06 (symlink and plugin integrity)
Type: Positive — plugin symlink
Precondition: `plugin-praxis/commands/idea.md` has been created.
Steps:
  1. Run `ls -la plugin-praxis/commands/idea.md`.
  2. Confirm the entry is a symbolic link (lrwxrwxrwx).
  3. Confirm the target resolves to `../../.claude/commands/idea.md` (relative, matching the pattern of every other command symlink in the directory).
Expected: Symlink exists and resolves correctly. A plain file or a broken symlink is a fail.
Pass/Fail: —

---

**TC-S-12**
AC ref: AC-01, AC-06 (catalog drift — assumption A-2)
Type: Positive — catalog check
Precondition: `idea.md` and its symlink are installed.
Steps:
  1. Run `make catalog-check`.
Expected: Exit code 0, no drift reported. Non-zero exit or drift message is a fail; run `make catalog` to regenerate and investigate the delta.
Pass/Fail: —

---

**TC-S-13**
AC ref: AC-02 (integrations drift — assumption A-1)
Type: Positive — integrations check
Precondition: `idea.md` and its symlink are installed.
Steps:
  1. Run `make integrations-check`.
Expected: Exit code 0, no drift reported. Non-zero exit is a fail; run `make integrations` and investigate.
Pass/Fail: —

---

### Group B — Behavioural dry-runs

Precondition for all B tests: `idea.md` is installed and functional; the ledger is initialised (`ledger.py init` has been run if the ledger is absent); the working directory is the repo root.

Observable outputs: the printed output block, the ledger entry written to disk (verify via `python .claude/skills/memory/scripts/ledger.py list --status pending --tags intake` or `show <id>`).

---

**TC-B-01**
AC ref: AC-07, AC-12, AC-14
Type: Positive — feature classification (happy path)
Input: `/idea add a caching layer to the fetch function`
Steps:
  1. Invoke the command with the input above.
  2. Observe the printed output block.
  3. Retrieve the ledger entry created during the run (`ledger.py list --status pending --tags intake`).
Expected:
  - Output block contains `Classification: feature`.
  - Output block contains a `Next:` line of the form `Next: /new-feature "<clarified summary>"`.
  - The `<clarified summary>` string in the `Next:` line matches the `--title` value in the ledger entry exactly (AC-12).
  - Ledger entry has `--status pending`, `--tags "intake,feature"`, `--type note`, `--source /idea`.
  - No plan, problem statement, or spec fragment appears after the output block (AC-14).
  - The command stops; `/new-feature` is not invoked.
Pass/Fail: —

---

**TC-B-02**
AC ref: AC-08, AC-12, AC-14
Type: Positive — bug classification (happy path)
Input: `/idea the patterns output truncates at 250 lines`
Steps:
  1. Invoke the command with the input above.
  2. Observe the printed output block.
  3. Retrieve the ledger entry.
Expected:
  - Output block contains `Classification: bug`.
  - Output block contains `Next: /fix-bug "<clarified summary>"`.
  - `Next:` argument matches ledger `--title` (AC-12).
  - Ledger entry has `--tags "intake,bug"`, `--status pending`, `--type note`, `--source /idea`.
  - No additional output after the block (AC-14).
  - `/fix-bug` is not invoked.
Pass/Fail: —

---

**TC-B-03**
AC ref: AC-09, AC-12, AC-14
Type: Positive — refinement classification via absorb rule (doc update)
Input: `/idea Update AGENTS.md to mention the /patterns command`
Steps:
  1. Invoke the command with the input above.
  2. Observe the printed output block.
  3. Retrieve the ledger entry.
Expected:
  - Output block contains `Classification: refinement`.
  - Output block contains `Next: /refine "<clarified summary>"`.
  - `Next:` argument matches ledger `--title` (AC-12).
  - Ledger entry has `--tags "intake,refinement"`, `--status pending`, `--type note`, `--source /idea`.
  - No additional output after the block (AC-14).
Pass/Fail: —

---

**TC-B-04**
AC ref: AC-09
Type: Positive — refinement classification (dependency bump variant)
Input: `/idea upgrade to a newer Python stdlib version requirement`
Steps:
  1. Invoke the command with the input above.
  2. Observe the printed output block.
Expected:
  - Output block contains `Classification: refinement`.
  - Output block contains `Next: /refine "<clarified summary>"`.
  - Ledger entry has `--tags "intake,refinement"`.
Pass/Fail: —

---

**TC-B-05**
AC ref: AC-09
Type: Positive — refinement classification (CI process variant)
Input: `/idea run make validate-all in CI before merge`
Steps:
  1. Invoke the command with the input above.
  2. Observe the printed output block.
Expected:
  - Output block contains `Classification: refinement`.
  - No new user-observable behavior is claimed; the absorb rule applies.
  - `Next: /refine` line is present.
Pass/Fail: —

---

**TC-B-06**
AC ref: AC-10, AC-14
Type: Positive — not-worth-doing classification (insufficient signal)
Input: `/idea maybe do something with the config`
Steps:
  1. Invoke the command. If the input is too vague to classify immediately, allow up to two clarifying questions with responses that do not clarify meaningfully (e.g. "I'm not sure", "just some config changes").
  2. Observe the printed output block.
  3. Retrieve the ledger entry.
Expected:
  - Output block contains `Classification: not-worth-doing`.
  - Output block contains a `Rationale:` line with a non-generic, input-specific sentence (must reference the specific deficiency: insufficient signal, unclear value, unclear scope — not a generic "this is not actionable").
  - Output block does NOT contain a `Next:` line.
  - Ledger entry has `--tags "intake,not-worth-doing"`, `--status pending`, `--type note`, `--source /idea`.
  - No additional output after the block (AC-14).
Pass/Fail: —

---

**TC-B-07**
AC ref: AC-11
Type: Boundary — clarification question count (exactly 0, clear input)
Input: `/idea add OAuth support to the login endpoint`
Steps:
  1. Invoke the command with the input above.
  2. Count the number of `AskUserQuestion` calls made before output is produced.
Expected: Zero clarifying questions are asked. The input is unambiguous; the command classifies directly.
Pass/Fail: —

---

**TC-B-08**
AC ref: AC-11
Type: Boundary — clarification question count (exactly 1, moderately vague)
Input: `/idea the output looks wrong`
Steps:
  1. Invoke the command.
  2. Answer the first clarifying question with: "The patterns output shows headers but no body rows, which contradicts what the docs say."
  3. Count total `AskUserQuestion` calls before classification output is produced.
Expected: Exactly one clarifying question is asked. The answer is sufficient to classify as `bug`. Classification and output follow.
Pass/Fail: —

---

**TC-B-09**
AC ref: AC-11
Type: Boundary — clarification question count (exactly 2, persistently vague)
Input: `/idea improve the ledger`
Steps:
  1. Invoke the command.
  2. Answer Q1 with: "Make it better somehow."
  3. If a second question is asked, answer Q2 with: "I don't know, just a general feeling."
  4. Confirm no third question is asked; observe that the command classifies on available information and produces output.
Expected:
  - No more than two `AskUserQuestion` calls occur.
  - After the second answer, the command classifies (likely `refinement` or `not-worth-doing`) on the available information.
  - The ledger entry body records the raw input and both Q&A exchanges.
  - A third question is never asked under any circumstance.
Pass/Fail: —

> Boundary note: The constraint is ≤2 questions. Testing exactly 2 (TC-B-09) and confirming the third is blocked is the critical boundary. Testing 0 (TC-B-07) and 1 (TC-B-08) covers the interior and lower boundary. A scenario where even two questions leave residual ambiguity and the command still stops is the highest-risk boundary to verify.

---

**TC-B-10**
AC ref: AC-10, AC-07 (not-worth-doing path — ledger persistence)
Type: Positive — not-worth-doing entry survives in ledger
Precondition: TC-B-06 has been executed and a `not-worth-doing` ledger entry was created.
Steps:
  1. Run `python .claude/skills/memory/scripts/ledger.py list --status pending --tags intake`.
  2. Locate the entry created in TC-B-06.
  3. Run `python .claude/skills/memory/scripts/ledger.py show <id>`.
Expected:
  - The entry appears in the list.
  - The entry body contains the original raw input ("maybe do something with the config") and the rationale.
  - Status remains `pending` (it is not auto-accepted or auto-rejected).
Pass/Fail: —

---

**TC-B-11**
AC ref: AC-07, AC-12 (independent ledger entries — no collision)
Type: Negative — prior similar entry does not suppress new entry
Precondition: A ledger entry already exists for a similar idea classified as `refinement`.
Input: `/idea add a real-time caching layer to the fetch function with observable cache-hit metrics`
Steps:
  1. Invoke the command.
  2. Confirm a new, separate ledger entry is created.
  3. Confirm the prior entry is not modified.
Expected:
  - A second, distinct ledger entry is created with `--tags "intake,feature"`.
  - The prior `refinement` entry is unchanged.
  - Classification is `feature` (new user-observable behavior: cache-hit metrics).
Pass/Fail: —

---

**TC-B-12**
AC ref: AC-14 (no trailing content — boundary)
Type: Negative — output terminates after the block
Input: `/idea add a caching layer to the fetch function` (same as TC-B-01)
Steps:
  1. Invoke the command.
  2. After the output block (the 4-line `Classification / Captured / Next / parenthetical` structure), check whether any additional text is printed.
Expected: Nothing appears after the closing parenthetical of the output block. No problem statement, no spec fragment, no plan content, no additional questions.
Pass/Fail: —

---

**TC-B-13**
AC ref: AC-07, AC-10 (misclassification boundary — refinement vs feature)
Type: Exploratory — absorb-rule boundary
Charter: Probe the boundary between `refinement` and `feature`. An improvement that adds new user-observable behavior (e.g. a new metric, a new output format) should classify as `feature`; one that preserves behavior while improving quality should classify as `refinement`.
Input A: `/idea add a --verbose flag to the ledger list command`
Input B: `/idea improve the readability of the ledger list output`
Steps:
  1. Invoke the command separately for each input.
  2. Observe the classification for each.
Expected:
  - Input A → `feature` (new user-observable behavior: a new flag).
  - Input B → `refinement` (behavior-preserving improvement).
  - Neither is misclassified as `bug` or `not-worth-doing`.
Pass/Fail: —

---

**TC-B-14**
AC ref: AC-07 (misclassification risk — bug vs refinement)
Type: Exploratory — bug vs refinement boundary
Charter: Probe the boundary between `bug` and `refinement`. Performance degradation observed by users (slower response times) should classify as `bug`; a refactor to improve internal code quality without user-observable change should classify as `refinement`.
Input A: `/idea the ledger list command takes 10 seconds when there are 50 entries; it used to take under 1 second`
Input B: `/idea refactor the ledger list output formatter to reduce cyclomatic complexity`
Steps:
  1. Invoke the command separately for each input.
  2. Observe the classification for each.
Expected:
  - Input A → `bug` (documented/expected performance regressed; user-observable deviation).
  - Input B → `refinement` (behavior-preserving internal change).
Pass/Fail: —

---

**TC-B-15**
AC ref: AC-10 (not-worth-doing path — rationale specificity)
Type: Negative — generic rationale is a fail
Input: `/idea make things better`
Steps:
  1. Invoke the command; answer any clarifying questions with equally non-specific responses.
  2. Observe the `Rationale:` line in the output.
Expected:
  - The `Rationale:` sentence references the specific deficiency of this input (e.g. "The input does not name a specific system, behavior, or outcome, providing insufficient signal to justify a lifecycle.").
  - The sentence is NOT a generic phrase such as "This idea does not have enough information." or "The cost/value ratio is unfavorable." without referencing what is specifically missing.
Pass/Fail: —

> This test is deliberately hard to automate. The reviewer must apply judgment: the rationale must be input-specific, not a template.

---

## 4. Coverage matrix

| AC ID | TC IDs | Coverage |
|-------|--------|----------|
| AC-01 | TC-S-01, TC-S-02 | Covered (BVA lower + upper) |
| AC-02 | TC-S-03, TC-S-11 | Covered |
| AC-03 | TC-S-04, TC-S-10 | Covered |
| AC-04 | TC-S-05, TC-S-10 | Covered |
| AC-05 | TC-S-06 | Covered |
| AC-06 | TC-S-07 | Covered |
| AC-07 | TC-B-01, TC-B-11, TC-B-13 | Covered (happy path + collision + boundary) |
| AC-08 | TC-B-02 | Covered |
| AC-09 | TC-B-03, TC-B-04, TC-B-05 | Covered (3 absorb-rule variants) |
| AC-10 | TC-B-06, TC-B-10, TC-B-15 | Covered (happy path + persistence + rationale specificity) |
| AC-11 | TC-B-07, TC-B-08, TC-B-09 | Covered (0, 1, 2 questions — BVA across full range) |
| AC-12 | TC-B-01, TC-B-02, TC-B-03 | Covered |
| AC-13 | TC-S-08 | Covered |
| AC-14 | TC-B-01, TC-B-06, TC-B-12 | Covered (positive path + not-worth-doing + dedicated boundary) |
| AC-15 | TC-S-09 | Covered |

All 15 ACs are covered. No gaps.

---

## 5. Risk assessment

| Risk area | Likelihood | Impact | Priority | Mitigation |
|-----------|-----------|--------|----------|-----------|
| **Misclassification: refinement vs feature** — the absorb rule boundary is fuzzy; the LLM may over-absorb new-behavior inputs into `refinement` | Medium | High | P1 | TC-B-13 (exploratory); the static route table in the command body anchors the rule |
| **Misclassification: bug vs refinement** — performance regressions are bugs, internal refactors are refinements; the LLM may conflate them | Medium | High | P1 | TC-B-14 (exploratory) |
| **Not-worth-doing rationale is dismissive/generic** — a generic rationale erodes trust and makes the ledger entry worthless for future pattern mining | Medium | High | P1 | TC-B-15 (negative); FR-7 requires input-specific rationale |
| **Third clarifying question asked** — violates FR-2 hard stop; user receives a Phase-0-style interrogation rather than triage | Low | High | P1 | TC-B-09 (BVA at exactly 2) |
| **Description collision with /new-feature** — the routing layer selects `/idea` when user intends a lifecycle command, or vice versa | Low | High | P1 | TC-S-04, TC-S-05, TC-S-10 |
| **Ledger capture skipped on not-worth-doing path** — silent drop violates FR-4; the entry is lost | Low | High | P1 | TC-B-06, TC-B-10 |
| **`Next:` argument diverges from ledger `--title`** — downstream invocation uses a different summary than the ledger record | Low | Medium | P2 | TC-B-01, TC-B-02, TC-B-03 (AC-12) |
| **Line budget exceeded** — file absorbs downstream logic; future maintainers mistake `/idea` for a planning command | Low | Medium | P2 | TC-S-01, TC-S-02 |
| **Catalog/integrations drift** — `SKILLS.md` not regenerated or integrations manifest drifts after new command is added | Low | Medium | P2 | TC-S-12, TC-S-13 |
| **`allowed-tools` key introduced** — creates a maintenance surface; violates NFR-2 | Low | Low | P3 | TC-S-03 |

### Regression scope

Adding `.claude/commands/idea.md` and its plugin symlink touches three surfaces that must not regress:

1. **Command catalog (`SKILLS.md`)**: regenerated by `make catalog`. Risk: if frontmatter is malformed, the build fails or the catalog row is wrong. Covered by TC-S-10 and TC-S-12.
2. **Plugin symlink directory (`plugin-praxis/commands/`)**: adding a new symlink must not break any existing symlink. Risk: naming collision with an existing command slug. There is no existing `idea.md`; risk is low. Covered by TC-S-11.
3. **Existing commands (`/new-feature`, `/fix-bug`, `/refine`, `/memory`)**: these are not modified. Regression risk is limited to the routing layer potentially selecting `/idea` ambiguously when the user types a lifecycle-command-like phrase. Covered by TC-S-04, TC-S-05, TC-S-10 (description uniqueness).

The ledger CLI (`ledger.py`) is not modified. No regression suite for it is required in this cycle.

---

## 6. Entry and exit criteria

### Entry criteria (testing may begin when)

1. `idea.md` exists at `.claude/commands/idea.md`.
2. The plugin symlink exists at `plugin-praxis/commands/idea.md` and resolves.
3. `make catalog` has been run and `SKILLS.md` reflects the `/idea` row.
4. The ledger is initialised in the target environment (`ledger.py status` exits 0).
5. All acceptance criteria are written, agreed, and unchanged from `spec.md`.

### Exit criteria (testing is complete and the verify gate may be passed when)

1. All static test cases (TC-S-01 through TC-S-13) have been executed with a pass verdict.
2. All behavioural dry-runs (TC-B-01 through TC-B-09) — the primary positive, negative, and boundary paths — have been executed with a pass verdict.
3. Exploratory charters TC-B-13, TC-B-14, and TC-B-15 have been completed with no Critical or High findings unresolved.
4. TC-B-10 and TC-B-11 (ledger persistence and independence) have been executed with a pass verdict.
5. Coverage matrix confirms all 15 ACs are mapped to at least one passing test case.
6. No open Critical or High severity defects are linked to this feature.
7. Any open Medium severity defect has a documented resolution plan and is risk-accepted by the product owner in writing before the gate is passed.
8. `make catalog-check` and `make integrations-check` both exit 0 on the target environment.

### Definition of "done / tested"

The `/idea` command is tested when all exit criteria above are met, the coverage matrix is attached to the verify report, and no unresolved Critical or High findings remain.

---

## 7. Test data notes

- All dry-run inputs are deterministic natural-language strings. No special test data setup is required beyond a functioning ledger.
- Each behavioural test case creates its own ledger entry. Run `ledger.py list --status pending --tags intake` before and after each TC-B run to isolate the entry created by that test.
- TC-B-10 depends on TC-B-06 having run. All other test cases are independent.
- The ledger entries created during testing are `pending` and can be rejected post-test with `ledger.py reject <id>` to keep the ledger clean.
