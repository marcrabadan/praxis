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

A praxis user who has a half-formed idea currently has no friction-free front door. Their only choices are to invoke a full-lifecycle command (`/new-feature`, `/fix-bug`, `/refine`) directly — which demands a well-articulated input — or to do nothing and lose the idea. The mismatch between the quality of input those commands expect and the quality of input the user actually holds at that moment produces four concrete problems:

1. Vague ideas get forced into the wrong lifecycle (e.g., a potential refinement incorrectly routed as a new feature), producing misaligned artifacts and wasted lifecycle effort.
2. Ideas that would be classified "not worth doing" at triage still consume the full lifecycle cost of `/new-feature` before being abandoned.
3. The memory ledger never receives a raw capture of the idea, so ideas surfaced and then deferred leave no trace and cannot be mined later by `/patterns`.
4. The cognitive burden on the user to pre-classify their own idea before invoking a command creates a drop-off point that suppresses intake volume.

The gap is the absence of a lightweight intake step that accepts raw, ambiguous input, disambiguates it minimally, classifies it, captures it durably, and routes it to the correct lifecycle entry point — without itself becoming a second planner or second spec writer.

---

## Business goals

| # | Desired outcome | Measurable indicator |
|---|----------------|----------------------|
| BG-1 | Reduce the cognitive cost of submitting an idea so that no idea is lost because the user could not phrase it correctly for a lifecycle command. | Subjective: users report fewer "I didn't know which command to use" moments. |
| BG-2 | Ensure every idea — including ones immediately classified "not worth doing" — is captured in the memory ledger before any routing decision, so the ledger becomes a complete intake record. | Every `/idea` invocation produces a `pending` ledger entry, regardless of classification outcome. |
| BG-3 | Reduce misrouted lifecycle invocations (e.g., a bug reported as `/new-feature`) by inserting a classification step before the user commits to a lifecycle. | Qualitative: fewer lifecycle artifacts abandoned after Phase 0 because the user chose the wrong command. |
| BG-4 | Keep the command thin enough that it never becomes a parallel planner — its output is a routing decision, not a spec. | The command file stays under approximately 80 lines; it invokes existing lifecycle commands rather than duplicating their behavior. |

---

## Stakeholders

| Stakeholder | Role in this feature | RACI |
|-------------|---------------------|------|
| **Praxis end user** (developer or analyst using praxis on a repo) | Primary beneficiary; the person who types `/idea <raw thought>` | C — defines what "easy intake" means in practice |
| **Praxis repo maintainer** (marcrabadan@gmail.com) | Owns the command file; accountable for promotion-policy compliance; decides the routing rules and category set | A, R |
| **Memory ledger subsystem** (`python .claude/skills/memory/scripts/ledger.py`) | Receives every intake capture; no human actor, but a hard dependency whose CLI contract must be respected | I |
| **/new-feature, /fix-bug, /refine commands** | Downstream consumers; their Phase 0 argument contracts constrain what `/idea` can hand off | I |
| **`/patterns` miner** (`tools/patterns.py`) | Downstream consumer of ledger entries tagged by `/idea`; richer intake improves pattern-mining signal | I |

There is no external regulatory or security stakeholder for this feature. There is one Accountable (repo maintainer), one Responsible (same person as implementer), and the end user as the primary Consulted voice. No veto stakeholders are missing.

---

## Constraints

### Structural constraints (non-negotiable)

- **C-1** — `/idea` must be implemented as a command file (`.claude/commands/idea.md`) with YAML frontmatter (`description`, optional `argument-hint`, optional `allowed-tools`), a Markdown body, and a `$ARGUMENTS` placeholder. It must not be implemented as a new skill. The promotion-policy doctrine (`.claude/factory/ai/promotion-policy.md`) requires demonstrated independent invocation across at least five distinct sessions before a new top-level skill is warranted; no such evidence exists yet. A command is the correct artifact at this maturity level.
- **C-2** — The command must remain thin: triage and routing only. It must not replicate the Discovery, Research, or Spec phases that already live inside `/new-feature`. The rule: if logic belongs to a lifecycle, it belongs in the command that owns that lifecycle.
- **C-3** — The command must integrate with the existing ledger CLI (`python .claude/skills/memory/scripts/ledger.py log`) using its current `--type`, `--title`, and `--status` parameters. It must not propose changes to the ledger schema as part of this feature.
- **C-4** — The command must not introduce new `allowed-tools` entries beyond what the three target lifecycle commands already require. Tool permission sprawl is a maintenance cost without a corresponding benefit at the triage layer.
- **C-5** — Tone and structure must match the reference exemplars: `memory.md` (a thin routing command with a short numbered how-to body) and `patterns.md` (a single-action command with a constrained `allowed-tools` list).

### Behavioral constraints

- **C-6** — Classification output must be one of four named categories: `feature`, `bug`, `refinement`, `not-worth-doing`. Routing follows directly: `feature → /new-feature`, `bug → /fix-bug`, `refinement → /refine`, `not-worth-doing → ledger capture only, no routing`.
- **C-7** — Clarification is capped at 1–2 questions. A command that asks three or more questions before acting will feel slower than using `/new-feature` directly, defeating the intake purpose. The `/new-feature` Phase 0 gate itself asks 2–3 questions; `/idea` must not double that cost.
- **C-8** — All clarifying questions must occur in the main conversation before any subagent dispatch. Subagents in this repo cannot address the user interactively (established pattern in `/new-feature` Phase 0 and `/fix-bug` Phase 0).

---

## Assumptions

| # | Assumption | Risk if wrong |
|---|-----------|---------------|
| A-1 | The four classification categories (`feature`, `bug`, `refinement`, `not-worth-doing`) are exhaustive for practical intake. Common edge cases (doc updates, questions, dependency bumps, process improvements) can be absorbed into one of the four without causing user confusion. | If common inputs do not map cleanly, the classification step generates more friction than it removes. Research must probe this with representative real inputs. |
| A-2 | Classification can be performed inline by the command itself (LLM reasoning at invocation time is sufficient), without delegating to the `business-analyst` or `product-owner` skills. | If classification accuracy for vague inputs is poor without skill delegation, the command will misroute a material percentage of intake. |
| A-3 | The user's intent when typing `/idea` is to get to the right lifecycle quickly, not to receive a polished artifact. The observable output of `/idea` is a routing action plus a ledger entry, not a report. | If users expect richer output (e.g., a brief problem framing before routing), the command's scope expands materially. |
| A-4 | The existing ledger `log` command with `--type note --status pending` is the correct mechanism for capturing a raw idea. No new ledger type (`idea`) is needed. | If a distinct `idea` type is desirable for `/patterns` mining (to surface idea-level patterns separately from general notes), that is a ledger change — a separate workstream outside this feature. |
| A-5 | Auto-routing (actually invoking the target lifecycle command on behalf of the user after classification) is preferable to recommend-and-confirm routing (proposing the classification and waiting for the user to invoke the lifecycle command manually). | The opposite assumption is equally defensible: the user may want to confirm the classification before committing to a lifecycle. This is a significant behavioral fork. Research must resolve it. See OQ-1. |
| A-6 | The command can be written without an `allowed-tools` frontmatter entry (i.e., it relies solely on the tools the agent has by default) because its only tool actions are invoking the ledger CLI and passing control to a lifecycle command. | If the ledger CLI invocation or lifecycle routing requires an explicit tool permission, an `allowed-tools` entry must be added — which is a visible surface change. |

---

## Risks

| # | Risk | Likelihood | Impact | Mitigation direction |
|---|------|-----------|--------|----------------------|
| R-1 | **Scope creep into a planner.** Once the command classifies an idea as a feature, there is immediate pressure to also produce a one-line problem statement or a suggested title to pass to `/new-feature` — which is the first action of `/new-feature`'s own Phase 0. Each such addition moves `/idea` toward being a thin planner. | Medium | High | The constraint "routing only, not planning" must be held explicitly in the command body and in any future review. Any framing must be limited strictly to what is already in the user's raw input. |
| R-2 | **Description collision with `/new-feature`.** If the `description` frontmatter of `/idea` is worded broadly ("start a feature" or "submit an idea for a feature"), the routing layer will select it when the user intends `/new-feature` directly, and vice versa. Two commands with similar descriptions compete for the same trigger surface — the exact anti-pattern the promotion-policy warns against. | Medium | Medium | The `description` must be narrow and distinct: the phrase "intake and triage" must appear, not "plan a feature" or "start development". Research should propose candidate wording. |
| R-3 | **Misclassification sends the user down the wrong lifecycle.** A bug described ambiguously as "the output looks wrong" may be classified as a refinement. The cost is discovering the wrong lifecycle after partial progress. | Medium | Medium | The 1–2 clarifying questions are the primary mitigation. The ledger entry also provides a canonical rollback point: the user can see what was captured and re-invoke the correct lifecycle command. |
| R-4 | **"Not worth doing" classification feels dismissive without rationale.** The user types an idea and receives a negative classification with no further action. If no rationale is surfaced, this erodes trust in the command and suppresses future intake. | Low | Medium | The command must surface a brief (one-sentence) rationale for a "not-worth-doing" classification before closing. |
| R-5 | **Memory hook double-capture.** If the repo's opt-in memory hook (`integrations/hooks/memory.settings.example.json`) is active in a consuming repo, it may produce a second ledger entry for the same idea in addition to the one `/idea` explicitly writes. | Low | Low | Research must check the hook behavior and confirm whether the hook fires on command invocations and whether the explicit ledger log call is idempotent with any hook-generated entry. |
| R-6 | **`/idea` becomes a soft prerequisite for other commands.** If `/new-feature`, `/fix-bug`, or `/refine` are later updated to suggest "run `/idea` first", the thin front-door command acquires a support burden it was not designed to carry. | Low | Low | The downstream commands must remain self-sufficient. `/idea` is a convenience front door, not a required gate. The feature spec must state this explicitly. |

---

## Open questions

Questions marked **[STOP]** are blocking — Research must resolve them before the spec is written.

| # | Question | Why it blocks | Owner |
|---|---------|--------------|-------|
| OQ-1 **[STOP]** | Does `/idea` auto-route (invoke the target lifecycle command immediately after classification, passing the user's input as the argument) or recommend-and-confirm (present the classification and proposed route, then wait for the user to act)? | This is the primary behavioral fork. Auto-routing is lower friction but removes the user's confirmation step. Recommend-and-confirm preserves user control but adds a round trip. The answer drives the entire command body structure. | Research |
| OQ-2 **[STOP]** | Are the four classification categories (`feature`, `bug`, `refinement`, `not-worth-doing`) sufficient, or do common real input types — doc updates, questions, dependency bumps, process improvements, ambiguous observations — require additional categories or a structured fallback? | If the category set is incomplete, a material percentage of real inputs will be misrouted or awkwardly forced into the wrong bucket. | Research — test against at least ten representative real inputs from project history |
| OQ-3 | Is inline classification (LLM reasoning at invocation time, no skill delegation) accurate enough for vague inputs, or does classification require the `business-analyst` or `product-owner` skill to achieve acceptable accuracy? | If skill delegation is needed, the command dispatches a subagent, changing the latency, complexity, and tool-permission profile substantially. A command that launches a subagent may no longer qualify as "thin" under C-2. | Research |
| OQ-4 | What is the correct `ledger.py log --type` value for the intake entry: `note`, `plan`, or `decision`? Does `tools/patterns.py` treat a `note` entry tagged `--source /idea` as a meaningfully distinct signal, or does capturing idea-level intake patterns require a dedicated ledger type? | Determines whether ledger schema changes are in scope. If a new type (`idea`) is needed, that is a separate workstream. If `note` with a source tag is sufficient, no schema change is required. | Research — inspect `tools/patterns.py` sweep logic |
| OQ-5 | Does the opt-in memory hook fire on `/idea` invocations in consuming repos and produce a duplicate ledger entry alongside the one the command explicitly writes? If so, should the hook be suppressed for this command, or should the explicit `log` call be made idempotent with the hook's entry? | Avoids ledger pollution with duplicate entries for the same idea, which would distort `/patterns` output. | Research — inspect `integrations/hooks/memory.settings.example.json` and the hook trigger conditions |
| OQ-6 | When `/idea` routes to `/new-feature`, `/fix-bug`, or `/refine`, what is the exact argument to pass? Is it the raw user input, the clarified input, or a structured one-line summary? Additionally: `/new-feature` Phase 0 itself asks 2–3 clarifying questions — if `/idea` has already asked 1–2, are the two Phase 0 gates additive (wasteful double-questioning) or intentionally complementary (coarser triage then finer scoping)? | Determines both the argument shape and whether `/idea`'s clarification step makes `/new-feature`'s Phase 0 redundant for routed inputs. A wasteful double-pass may make auto-routing feel worse than going direct. | Research |
| OQ-7 | Should `/idea` produce any user-visible output before routing beyond the ledger-capture confirmation and the route announcement? For example: a one-line restatement of the idea as understood, a brief classification rationale, or a summary of what the target lifecycle will do next? | Affects the tone and verbosity of the command body. Too much output contradicts "thin" (C-2 and BG-4); too little output feels opaque, especially for the "not-worth-doing" path (R-4). | Research — propose minimum viable output per classification outcome |

---

## Traceability

- Idea / request id: `IDEA-idea-command`
- This artifact id: `DISC-idea-command`
- Feeds: research (`RES-idea-command`) → spec (`SPEC-idea-command`)
