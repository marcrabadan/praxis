---
id: idea-command
project: praxis
title: "/idea — idea intake & triage command"
status: accepted
source: DISC-idea-command
traces: RES-idea-command
---

# Spec: /idea — idea intake & triage command

Sources: discovery ([`discovery/discovery-report.md`](discovery/discovery-report.md))
and research ([`research/research-report.md`](research/research-report.md)).

---

## Problem & scope

Praxis users who hold a half-formed idea have no friction-free front door. Invoking
`/new-feature`, `/fix-bug`, or `/refine` directly demands a well-articulated input
that most ideas do not yet meet. The result is misrouted lifecycles, ideas silently
dropped before any ledger record exists, and a cognitive barrier that suppresses
intake volume.

This spec defines a single thin command — `/idea` — that accepts raw, ambiguous
input; asks at most 1–2 clarifying questions; classifies the input into one of four
categories; captures a `pending` ledger entry unconditionally; and then prints the
classification, the ledger entry id, and the exact lifecycle invocation string for
the user to run. The command then stops. It does not plan, it does not spec, and it
does not invoke the downstream lifecycle command on the user's behalf.

### Out of scope

- Planning, problem-statement writing, or spec production (those belong to the
  downstream lifecycle commands).
- Auto-routing: the command never invokes `/new-feature`, `/fix-bug`, or `/refine`
  itself; it only recommends the invocation string.
- Any change to the ledger schema (`ledger.py` TYPES enum, new `idea` type).
- New `allowed-tools` entries beyond the default toolset.
- Converting `/idea` into a skill or adding a subagent dispatch.
- Making `/idea` a required prerequisite gate for any other command.

---

## Functional requirements

**FR-1 — Command file shape (Must)**
The command must be implemented as `.claude/commands/idea.md` with YAML frontmatter
containing `description` (value must include "intake and triage" and must NOT
include "plan a feature") and `argument-hint`. No `allowed-tools` frontmatter key.
The body must follow the `memory.md`/`learn.md` thin-command shape: purpose
paragraph, `$ARGUMENTS` placeholder, numbered routing section. Total file length:
31–41 lines.

**FR-2 — Clarification gate (Must)**
Before classifying, the command must determine whether the input is sufficiently
specific to classify. If not, it must ask at most two clarifying questions using
`AskUserQuestion` in the main conversation. It must not ask a third question; if
ambiguity remains after two rounds, it must classify on the available information
and note the residual uncertainty in the ledger entry body.

**FR-3 — Four-way inline classification (Must)**
The command must classify the clarified input into exactly one of four categories
using inline LLM reasoning (no skill delegation, no subagent, no `Agent` tool call):

| Category | Routing target | Absorb rule |
|----------|---------------|-------------|
| `feature` | `/new-feature` | New user-observable behavior that does not exist today |
| `bug` | `/fix-bug` | Existing behavior that deviates from documented or expected output |
| `refinement` | `/refine` | Behavior-preserving improvement; absorbs doc updates, dependency bumps, process changes that do not alter user-observable behavior |
| `not-worth-doing` | No route | Signal is insufficient to justify a lifecycle, or cost/value ratio is clearly unfavorable |

No fifth category is permitted. The four categories are exhaustive for practical
intake.

**FR-4 — Unconditional ledger capture (Must)**
Before printing any output, the command must record a `pending` ledger entry via:

```
python .claude/skills/memory/scripts/ledger.py log \
  --type note \
  --title "<clarified one-line summary>" \
  --source /idea \
  --status pending \
  --tags "intake,<classification>" \
  --body "<raw input + any clarification Q&A>"
```

The capture must occur for all four classification outcomes, including
`not-worth-doing`. It must not be skipped on any path.

**FR-5 — Recommend-and-confirm output (Must)**
After capture, the command must print a structured block and then stop:

For `feature`, `bug`, or `refinement`:
```
Classification: <category>
Captured: <ledger-entry-id> (pending)
Next: /<command> "<clarified summary>"
(Run the command above when ready, or adjust the summary first.)
```

For `not-worth-doing`:
```
Classification: not-worth-doing
Rationale: <one sentence — why the signal is insufficient or cost/value is unfavorable>
Captured: <ledger-entry-id> (pending — remains in the ledger if you want to revisit)
```

The command must not produce additional output: no problem statement, no spec
fragment, no additional plan content.

**FR-6 — Clarified summary as downstream argument (Must)**
The string passed as the argument in the `Next:` line must be the clarified
one-line summary (the version produced after any clarification Q&A), not the
raw unedited user input. The same string must be used as the `--title` in the
ledger entry, ensuring the ledger record and the proposed downstream invocation
are consistent.

**FR-7 — Not-worth-doing rationale (Must)**
When the classification is `not-worth-doing`, the command must emit one sentence of
rationale before the `Captured:` line. The rationale must reference the specific
deficiency in the input (e.g., insufficient signal, unclear value, known duplicate,
explicitly out of scope) rather than a generic dismissal.

---

## Non-functional requirements

**NFR-1 — File line budget (Must)**
The finished `idea.md` command file must not exceed 41 lines (matching the
`memory.md`/`learn.md` reference exemplars). Exceeding this budget is evidence
the command has absorbed planning or spec-writing logic that belongs downstream.

**NFR-2 — No new allowed-tools (Must)**
The command file must not introduce an `allowed-tools` frontmatter key. The command
relies only on `Bash` (for the ledger CLI call) and `AskUserQuestion` (for
clarification), both of which are in the default toolset. Adding `allowed-tools`
would introduce a visible maintenance surface with no corresponding benefit at the
triage layer.

**NFR-3 — No subagent dispatch (Must)**
The command must not invoke the `Agent` tool, instantiate a subagent, or load a
skill. All reasoning (classification, rationale) must execute inline in the main
conversation. This constraint is observable: if the command body contains the word
`Agent` as a tool invocation, or any `Skill` tool reference, it fails this NFR.

**NFR-4 — Deterministic classification-to-route mapping (Must)**
The mapping between the four classification labels and the three downstream
commands must be static and explicit in the command body (a table or labeled list).
It must not be computed or inferred at runtime. A reader of the command file must
be able to determine the routing outcome for any classification without running the
command.

**NFR-5 — No ledger schema change (Must)**
The command must use `--type note` with the existing ledger CLI. It must not
introduce a new `--type idea` or any other value outside the existing TYPES enum
(`plan`, `decision`, `implementation`, `artifact`, `test-strategy`, `rollout`,
`note`). Any future ledger-type change is a separate workstream.

**NFR-6 — Description uniqueness (Should)**
The `description` frontmatter value must be distinct from the descriptions of
`/new-feature`, `/fix-bug`, and `/refine` so that the routing layer does not
ambiguously select `/idea` when the user intends to invoke a lifecycle command
directly. The phrase "intake and triage" must appear; the phrase "plan a feature"
must not appear.

---

## User stories and acceptance criteria

### US-1 — Feature intake

**As a** praxis developer,
**I want** to type `/idea add a caching layer to the fetch function` and have the
command classify it, capture it, and tell me the exact `/new-feature` invocation to
run,
**so that** I can move my idea from raw thought to the correct lifecycle entry point
without having to decide upfront which lifecycle command to use.

**INVEST notes:** Independent (no dependency on an incomplete story). Negotiable
(classification mechanism is LLM reasoning, not prescribed algorithm). Valuable
(removes the pre-classification burden from the user). Estimable (command file of
known shape and size). Small (single command file change). Testable (Gherkin below).

```gherkin
Scenario: Clear feature input classifies as feature and prints invocation
  Given the user invokes /idea with "add a caching layer to the fetch function"
  And the input unambiguously describes new user-observable behavior
  When the command runs
  Then the classification printed is "feature"
  And a ledger entry with status "pending" and tags "intake,feature" is created
  And the output contains a "Next:" line of the form: /new-feature "<clarified summary>"
  And the command stops without invoking /new-feature

Scenario: Feature input already in the ledger with a different route
  Given a prior ledger entry exists for a similar idea classified as "refinement"
  And the user invokes /idea with a new variation that adds new observable behavior
  When the command runs
  Then a new separate ledger entry is created with classification "feature"
  And the prior entry is not modified
```

---

### US-2 — Bug intake

**As a** praxis developer,
**I want** to type `/idea the patterns output truncates at 250 lines` and receive
a `bug` classification with the `/fix-bug` invocation string,
**so that** unexpected behavior reaches the fix lifecycle without me first having
to determine that it is a bug and not a refinement.

**INVEST notes:** Independent. Negotiable. Valuable (correct lifecycle routing
avoids abandoned `/new-feature` artifacts created for bugs). Estimable. Small.
Testable.

```gherkin
Scenario: Unexpected-behavior input classifies as bug
  Given the user invokes /idea with "the patterns output truncates at 250 lines"
  And the input describes behavior deviating from expected or documented output
  When the command runs
  Then the classification printed is "bug"
  And a ledger entry with status "pending" and tags "intake,bug" is created
  And the output contains a "Next:" line of the form: /fix-bug "<clarified summary>"
  And the command stops without invoking /fix-bug

Scenario: Ambiguous symptom input resolves to bug after one clarifying question
  Given the user invokes /idea with "the output looks wrong"
  When the command asks at most one clarifying question
  And the user confirms the output deviates from documented behavior
  Then the classification printed is "bug"
  And the ledger entry body records the raw input and the clarification exchange
```

---

### US-3 — Refinement intake (including absorb rule)

**As a** praxis developer,
**I want** doc updates, dependency bumps, and process improvements to be classified
as `refinement` automatically,
**so that** I do not accidentally start a `/new-feature` lifecycle for a
behavior-preserving change.

**INVEST notes:** Independent. Negotiable. Valuable (prevents lifecycle mismatch
for the most common maintenance inputs). Estimable. Small. Testable.

```gherkin
Scenario: Doc update classifies as refinement via absorb rule
  Given the user invokes /idea with "Update AGENTS.md to mention the /patterns command"
  When the command runs
  Then the classification printed is "refinement"
  And a ledger entry with status "pending" and tags "intake,refinement" is created
  And the output contains a "Next:" line of the form: /refine "<clarified summary>"

Scenario: Dependency bump classifies as refinement
  Given the user invokes /idea with "upgrade to a newer Python stdlib version requirement"
  When the command runs
  Then the classification printed is "refinement"
  And the output contains a "Next:" line of the form: /refine "<clarified summary>"

Scenario: Behavior-preserving process change classifies as refinement
  Given the user invokes /idea with "run make validate-all in CI before merge"
  And the change does not alter any user-observable output
  When the command runs
  Then the classification printed is "refinement"
```

---

### US-4 — Not-worth-doing intake

**As a** praxis developer,
**I want** an idea with insufficient signal or unfavorable cost/value to be captured
in the ledger with a one-sentence rationale rather than silently dropped,
**so that** I can revisit it later without having to remember I had the idea.

**INVEST notes:** Independent. Negotiable. Valuable (prevents trust erosion from
silent dismissal; preserves the intake record for future pattern mining). Estimable.
Small. Testable.

```gherkin
Scenario: Insufficient-signal input classifies as not-worth-doing with rationale
  Given the user invokes /idea with "maybe do something with the config"
  And the input cannot be clarified into a concrete outcome after two clarifying questions
  When the command runs
  Then the classification printed is "not-worth-doing"
  And the output contains a "Rationale:" line with a non-generic, input-specific sentence
  And a ledger entry with status "pending" and tags "intake,not-worth-doing" is created
  And the output contains no "Next:" line

Scenario: Not-worth-doing entry persists in ledger for future retrieval
  Given the command has classified an idea as "not-worth-doing" and created a ledger entry
  When the user later runs /memory list --status pending --tags intake
  Then the not-worth-doing entry appears in the results
  And it retains the original raw input and rationale in its body
```

---

### US-5 — Vague input clarification path

**As a** praxis developer,
**I want** the command to ask me at most two focused clarifying questions when my
input is too vague to classify,
**so that** I get a correct classification without the overhead of answering a full
Phase 0 interrogation.

**INVEST notes:** Independent (clarification path is internal to the command).
Negotiable (the exact questions are LLM-generated, not prescribed). Valuable
(prevents misclassification of vague inputs; reduces lifecycle abandonment).
Estimable. Small. Testable.

```gherkin
Scenario: Vague input triggers at most two clarifying questions
  Given the user invokes /idea with "improve the ledger"
  When the command determines the input is too vague to classify
  Then it asks exactly one clarifying question using AskUserQuestion
  And if still ambiguous, it asks at most one more question
  And it does not ask a third question under any circumstance

Scenario: Classification proceeds after max questions even with residual ambiguity
  Given the user invokes /idea with a vague input
  And the command has asked two clarifying questions
  And the input remains ambiguous
  When the command classifies on the available information
  Then it selects the most probable category from the four options
  And the ledger entry body notes the residual ambiguity
  And the output is produced (it does not loop or ask a third question)

Scenario: Clear input skips clarification entirely
  Given the user invokes /idea with "add OAuth support to the login endpoint"
  And the input unambiguously describes new user-observable behavior
  When the command runs
  Then no clarifying question is asked
  And the classification is produced directly
```

---

## Acceptance criteria (QA test targets)

The following criteria are written for a QA engineer to turn into executable tests.
Each maps to at least one FR or NFR above.

| AC ID | Criterion | Maps to |
|-------|-----------|---------|
| AC-01 | `idea.md` file length is between 31 and 41 lines inclusive. | NFR-1 |
| AC-02 | `idea.md` frontmatter does not contain an `allowed-tools` key. | NFR-2, FR-1 |
| AC-03 | `idea.md` frontmatter `description` contains the substring "intake and triage". | FR-1, NFR-6 |
| AC-04 | `idea.md` frontmatter `description` does not contain "plan a feature". | FR-1, NFR-6 |
| AC-05 | `idea.md` body does not contain the string "Agent" as a tool invocation. | NFR-3 |
| AC-06 | `idea.md` contains an explicit static mapping of all four categories to their routes. | NFR-4 |
| AC-07 | Invoking `/idea` with a clear feature input produces a ledger entry with `--tags "intake,feature"` and `--status pending`. | FR-4, FR-3 |
| AC-08 | Invoking `/idea` with a clear bug input produces a ledger entry with `--tags "intake,bug"` and a `Next: /fix-bug` line. | FR-4, FR-5 |
| AC-09 | Invoking `/idea` with a doc-update input produces a ledger entry with `--tags "intake,refinement"` and a `Next: /refine` line (absorb rule). | FR-3, FR-4 |
| AC-10 | Invoking `/idea` with a `not-worth-doing` input produces a ledger entry with `--tags "intake,not-worth-doing"`, a `Rationale:` line, and no `Next:` line. | FR-5, FR-7 |
| AC-11 | When input is vague, the command asks no more than two `AskUserQuestion` calls before producing output. | FR-2 |
| AC-12 | The string in the `Next:` line matches the `--title` value in the ledger entry (clarified summary, not raw input). | FR-6 |
| AC-13 | The `--type` argument in the ledger CLI call is `note`. No other type value is used. | NFR-5, FR-4 |
| AC-14 | The command does not print any content after the output block (no plan, no problem statement, no spec fragment). | FR-5 |
| AC-15 | The `--source` argument in the ledger CLI call is `/idea`. | FR-4 |

---

## Open questions

No blocking open questions remain. All seven OQs from `DISC-idea-command` were
resolved in `RES-idea-command`.

One non-blocking residual item for implementation awareness:

**OQ-R1 (non-blocking)** — If a future version of `patterns.py` introduces a
dedicated `idea` ledger type for richer pattern-mining signal, the `--type note`
decision made here (per C-3 and OQ-4) will require a migration of existing
`intake`-tagged entries. The implementer should note this forward-compatibility
consideration in the command file's comments if it helps future maintainers.
Owner: repo maintainer. No action required before implementation.

---

## Traceability

- This spec id: `SPEC-idea-command` (frontmatter `id: idea-command`)
- Sources: discovery (`DISC-idea-command`), research (`RES-idea-command`)
- Upstream artifacts:
  - Discovery: [`discovery/discovery-report.md`](discovery/discovery-report.md)
  - Research: [`research/research-report.md`](research/research-report.md)
- Downstream artifacts:
  - Plan: [`plans/implementation-plan.md`](plans/implementation-plan.md)
  - Tasks: [`tasks/tasks.md`](tasks/tasks.md)
  - Decisions: `decisions/`
  - Verify report: [`reports/verify/report.md`](reports/verify/report.md)
  - Release notes: [`reports/release/release-notes.md`](reports/release/release-notes.md)
