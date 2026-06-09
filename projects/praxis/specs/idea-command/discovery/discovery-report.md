---
id: DISC-idea-command
title: "Discovery Report — /idea command"
status: draft
traces:
  feeds-research: "RES-idea-command"
  feeds-spec: "SPEC-idea-command"
---

# Discovery Report — /idea command

> Step 1 of `feature-development`. Produced before any spec exists. This is where
> understanding happens — no solutions yet. Routed to the **business-analyst**.
> Gate 1 (`approved-discovery`) accepts discovery **and** research together
> before the spec step opens.

---

## Problem statement

A praxis user who has a half-formed idea currently has no friction-free front door. Their only choices are to invoke a full-lifecycle command (`/new-feature`, `/fix-bug`, `/refine`) directly — which demands a well-articulated input — or to do nothing and lose the idea. The mismatch between the quality of input those commands expect and the quality of input the user actually holds in the moment means:

1. Vague ideas get forced into the wrong lifecycle (e.g., a potential refinement incorrectly routed as a new feature), producing misaligned artifacts and wasted lifecycle effort.
2. Ideas that would be classified "not worth doing" at triage still consume the full lifecycle cost of `/new-feature` before being abandoned.
3. The memory ledger never receives a raw capture of the idea, so ideas surfaced and then deferred leave no trace and cannot be mined by `/patterns`.
4. The cognitive burden on the user to pre-classify their own idea before invoking a command creates a drop-off point that suppresses intake.

The gap is the absence of a lightweight intake step that accepts raw, ambiguous input, disambiguates it minimally, classifies it, captures it durably, and routes it to the correct lifecycle entry point — without itself becoming a second planner or second spec writer.

---

## Business goals

| # | Desired outcome | Measurable indicator |
|---|----------------|----------------------|
| BG-1 | Reduce the cognitive cost of submitting an idea so that no idea is lost because the user could not phrase it correctly for a lifecycle command. | Subjective: users report fewer "I didn't know which command to use" moments. |
| BG-2 | Ensure every idea — including ones immediately classified "not worth doing" — is captured in the memory ledger before any routing decision, so the ledger becomes a complete intake record. | Every `/idea` invocation produces a `pending` ledger entry, regardless of classification outcome. |
| BG-3 | Reduce misrouted lifecycle invocations (e.g., a bug reported as `/new-feature`) by inserting a classification step before the user commits to a lifecycle. | Qualitative: fewer lifecycle artifacts abandoned after Phase 0. |
| BG-4 | Keep the command thin enough that it never becomes a parallel planner — its output is a routing decision, not a spec. | The command file stays under ~80 lines; it invokes existing lifecycle commands rather than duplicating their behavior. |

---

## Stakeholders

| Stakeholder | Role in this feature | RACI |
|-------------|---------------------|------|
| **Praxis end user** (developer/analyst using praxis on a repo) | Primary beneficiary; the person who types `/idea <raw thought>` | C — defines what "easy intake" means |
| **Praxis repo maintainer** (currently the user at marcrabadan@gmail.com) | Owns the command file; accountable for promotion-policy compliance; decides the routing rules | A, R |
| **Memory ledger subsystem** | Receives every intake capture; no human actor, but a dependency whose CLI contract must be respected | I |
| **/new-feature, /fix-bug, /refine commands** | Downstream consumers; their argument contracts constrain what `/idea` can hand off | I |
| **`/patterns` miner** | Downstream consumer of ledger entries tagged by `/idea`; richer intake improves pattern quality | I |

There is no external regulatory or security stakeholder for this feature. The RACI is simple: one Accountable (repo maintainer), one Responsible (same person as implementer), and the end user as the primary Consulted voice.

---

## Constraints

**Structural constraints (non-negotiable)**

- C-1: `/idea` must be implemented as a command (a `.claude/commands/idea.md` file with frontmatter `description` + optional `argument-hint`), not as a new skill. The promotion-policy doctrine in `.claude/factory/ai/promotion-policy.md` requires demonstrated independent invocation before a new skill is warranted. No such evidence exists yet.
- C-2: The command must remain thin — triage and routing only. It must not replicate the Discovery, Research, or Spec phases that already live inside `/new-feature`. The rule is: if the logic belongs to a lifecycle, it belongs in the lifecycle command that owns that lifecycle.
- C-3: The command must integrate with the existing ledger CLI (`python .claude/skills/memory/scripts/ledger.py log`) using its current `--type` and `--status` parameters. It must not propose ledger schema changes as part of this feature.
- C-4: The command must not add a new `allowed-tools` surface beyond what the three target lifecycle commands already require. Tool permission sprawl is a maintenance cost.
- C-5: The command file must follow the established shape of existing commands: YAML frontmatter (`description`, optional `argument-hint`, optional `allowed-tools`), then a Markdown body with `$ARGUMENTS`. Tone and structure must match `memory.md` and `patterns.md` as reference exemplars.

**Behavioral constraints**

- C-6: Classification output must be one of four named categories: `feature`, `bug`, `refinement`, `not-worth-doing`. Routing follows directly from classification: `feature → /new-feature`, `bug → /fix-bug`, `refinement → /refine`, `not-worth-doing → no routing, ledger capture only`.
- C-7: Clarification is limited to 1–2 questions. A command that asks three or more questions before doing anything will be perceived as slower than just using `/new-feature` directly — defeating the intake purpose.
- C-8: The command must respect the constraint that subagents cannot talk to the user; all clarifying questions must happen in the main conversation before any subagent dispatch.

---

## Assumptions

| # | Assumption | Why it needs validation |
|---|-----------|------------------------|
| A-1 | The four classification categories (`feature`, `bug`, `refinement`, `not-worth-doing`) are exhaustive for practical intake. Edge cases (e.g., "question", "doc update", "dependency upgrade") can be absorbed into one of the four without user confusion. | If there are common input types that do not map cleanly, the classification step will generate more friction than it removes. Research should probe this with examples. |
| A-2 | Classification can be performed inline by the command itself (i.e., the LLM reasoning at invocation time is sufficient), without delegating to the `business-analyst` or `product-owner` skills. | If classification accuracy for vague inputs is poor without a skill, the command will misroute. Research should test against real vague inputs. |
| A-3 | The user's intent when typing `/idea` is to get to the right lifecycle quickly, not to receive a polished artifact. The "output" of `/idea` is a routing action plus a ledger entry, not a report. | If users expect a richer output (e.g., a short problem framing before routing), the command's scope expands. |
| A-4 | The existing ledger `log` command with `--type note --status pending` is the correct mechanism for capturing a raw idea. No new ledger type is needed. | If "idea" as a ledger type is desirable for `/patterns` mining, a new type might be warranted — but that is a ledger change, not an `/idea` command change, and is out of scope for this feature. |
| A-5 | Auto-routing (actually invoking `/new-feature`, `/fix-bug`, or `/refine` on behalf of the user) is preferable to recommend-and-confirm routing (proposing the route and waiting for the user to invoke it). | The opposite assumption is equally defensible: the user may want to see the classification, confirm it, and then invoke the lifecycle command themselves. This is a significant behavioral fork that Research must resolve. |

---

## Risks

| # | Risk | Likelihood | Impact | Notes |
|---|------|-----------|--------|-------|
| R-1 | **Scope creep into a planner.** Once the command classifies an idea as a feature, there is pressure to also produce a one-line problem statement, a suggested title, or a brief framing — which is the first step of `/new-feature`'s Discovery phase. Each such addition moves the command toward being a thin planner. | Medium | High | The constraint "routing only, not planning" must be held explicitly. Any framing output should be limited to what is passed as the argument to the target lifecycle command. |
| R-2 | **Overlap and routing confusion with `/new-feature`.** If `/idea` is described broadly, the LLM router may trigger it when the user intends `/new-feature` directly (or vice versa). Two commands with similar descriptions compete for trigger surface — the exact anti-pattern the promotion policy warns against. | Medium | Medium | The `description` frontmatter of `/idea` must be narrow and distinct: "intake and triage", not "start a feature". Research should propose a wording that clearly distinguishes the two. |
| R-3 | **Misclassification sends the user down the wrong lifecycle.** A bug described ambiguously as "the output is wrong" may be classified as a refinement. The cost is the user discovers the wrong lifecycle after partial progress. | Medium | Medium | The 1–2 clarifying questions are the primary mitigation. The ledger entry also provides a rollback point. |
| R-4 | **"Not worth doing" feels dismissive.** The user types an idea and receives a negative classification with no further action. If the rationale is not surfaced, this erodes trust in the command. | Low | Medium | The command must surface the rationale for a "not-worth-doing" classification (even a one-sentence reason) before closing. |
| R-5 | **Memory hook double-capture.** If the repo's opt-in memory hook fires on every command invocation, it may produce a second ledger entry for the same idea in addition to the one `/idea` explicitly logs. | Low | Low | Research should check the hook behavior and confirm whether the hook should be suppressed or whether the explicit log entry is idempotent with the hook's entry. |
| R-6 | **Command becomes a dependency for other commands.** If `/new-feature`, `/fix-bug`, or `/refine` are updated to suggest "use `/idea` first", the thin intake command acquires a support burden and a surface it was not designed to carry. | Low | Low | The downstream commands should remain self-sufficient. `/idea` is a convenience front-door, not a required gate. |

---

## Open questions

Questions marked **[STOP]** are stop conditions — Research must resolve them before the spec is written.

| # | Question | Why it blocks | Owner |
|---|---------|--------------|-------|
| OQ-1 **[STOP]** | Does `/idea` auto-route (invoke the target lifecycle command immediately after classification) or recommend-and-confirm (present the classification and proposed route, then wait for the user to act)? | This is the primary behavioral fork. Auto-routing is faster but removes the user's confirmation step. Recommend-and-confirm preserves user control but adds a round trip. The answer drives the entire command body. | Research |
| OQ-2 **[STOP]** | Are the four classification categories (`feature`, `bug`, `refinement`, `not-worth-doing`) sufficient, or do common input types (doc updates, questions, dependency bumps, process improvements) require additional categories or a fallback? | If the category set is incomplete, the classification logic will misroute a material percentage of real inputs. | Research (test against example inputs) |
| OQ-3 | Is inline classification (LLM reasoning at invocation) accurate enough for vague inputs, or does classification require the `business-analyst` or `product-owner` skill? | If skill delegation is needed, the command is no longer thin — it must dispatch a subagent, which changes the latency and complexity profile significantly. | Research |
| OQ-4 | What is the correct `ledger.py log --type` value for the intake entry: `note`, `plan`, or a new `idea` type? Does the `/patterns` miner treat a `note` entry tagged `source:/idea` as a distinct signal, or does it need a new type to surface idea-level patterns distinctly? | Determines whether ledger schema changes are in scope. If a new type is needed, that is a separate workstream. | Research (check patterns.py behavior) |
| OQ-5 | Does the repo's opt-in memory hook (if active) fire on `/idea` invocations and produce a duplicate ledger entry? If so, should the hook be suppressed for this command or should the explicit log call be made idempotent? | Avoids ledger pollution with duplicate entries for the same idea. | Research (inspect hook configuration) |
| OQ-6 | When `/idea` routes to `/new-feature`, what is the correct argument to pass? Is it the raw user input, the clarified+classified input, or a structured summary? The `/new-feature` Phase 0 gate will ask clarifying questions if the input is underspecified — does that mean `/idea`'s clarification is redundant, or is it intentionally a pre-filter? | Determines what `/idea` actually hands off, and whether the two commands' Phase 0 gates are additive (wasteful) or complementary. | Research |
| OQ-7 | Should `/idea` produce any user-visible output before routing, beyond the ledger capture confirmation and the route announcement? For example: a one-line problem restatement, a classification rationale, or a summary of what the target lifecycle will do next? | Affects the tone and length of the command body. Too much output contradicts "thin"; too little output feels opaque. | Research |

---

## Traceability

- Idea / request id: `IDEA-idea-command`
- This artifact id: `DISC-idea-command`
- Feeds: research (`RES-idea-command`) → spec (`SPEC-idea-command`)
