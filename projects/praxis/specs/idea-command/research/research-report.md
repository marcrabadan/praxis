---
id: RES-idea-command
title: "Research Report — /idea command"
status: draft
traces:
  sources-discovery: "DISC-idea-command"
  feeds-spec: "SPEC-idea-command"
---

# Research Report — /idea command

> Step 2 of `feature-development`. **Research must precede specification.**
> Routed to `deep-research` (and the relevant domain experts). Reuse > Extend >
> Build: prefer existing solutions and existing praxis skills before proposing
> something new.

---

## Questions

OQ-1 through OQ-7 from `DISC-idea-command`, with OQ-1 and OQ-2 marked [STOP].

---

## Findings

### OQ-1 — Routing model: recommend-and-confirm (not auto-route)

**Recommendation: recommend-and-confirm.**

Auto-routing fires the target lifecycle command immediately after classification. The inspection of `/new-feature` Phase 0 (`new-feature.md:14`) reveals it asks "2–3 clarifying questions" of the user if the feature is underspecified, *but those questions happen in the main conversation, not in a subagent*. If `/idea` auto-routes, the user goes from answering 1–2 `/idea` clarifying questions directly into answering 2–3 more Phase 0 questions from `/new-feature`. The round-trip cost is identical to recommend-and-confirm, but the user has no moment to confirm the classification before a heavy lifecycle starts. For the `not-worth-doing` path, auto-routing has no target to invoke — making the routing model inconsistent depending on classification outcome.

Recommend-and-confirm presents the classification, ledger-entry id, and a one-line route proposal (e.g. "Classified as `feature`. Run `/new-feature <clarified summary>` to proceed."), then stops. The user invokes the target command with whatever refinement they choose. This preserves control, keeps `/idea` demonstrably thin (it never touches the Agent tool), and avoids the double-questioning hazard.

Evidence: `new-feature.md:14`, `fix-bug.md:14`, `refine.md:13`. See also evidence EV-007 in the evidence log.

---

### OQ-2 — Four categories are sufficient with one clarification on scope

**Recommendation: retain the four categories; add explicit absorb rules for edge cases.**

Tested against ten representative real intake inputs drawn from the project's own ledger and command history:

1. "The ledger should auto-bootstrap when no config exists" → `feature` (new behavior)
2. "The `patterns` command output truncates at 250 lines" → `bug` (unexpected behavior)
3. "Refactor `ledger.py` snapshot diff to use a cleaner temp-index approach" → `refinement` (behavior-preserving quality)
4. "Update AGENTS.md to mention the new /patterns command" → `refinement` (doc update is behavior-preserving)
5. "Add a security gate to the feature-development verify loop" → `feature` (new gate = new behavior)
6. "Dependency bump: upgrade to a newer Python stdlib version requirement" → `refinement` (no behavior change, quality/maintenance)
7. "Why does `ledger.py bootstrap` not print the context docs when called with --brief?" → `bug` (unexpected gap in behavior)
8. "Consider adding a Tier-6 skill level for multi-agent systems" → classification: `feature` if pursued, `not-worth-doing` if the value is unclear; the command's 1–2 clarifying questions resolve this
9. "Process improvement: run `make validate-all` in CI before merge" → `feature` (new CI gate = new behavior)
10. "Idea: a `/review` alias for `/review-changes`" → `refinement` (convenience alias, preserves behavior)

All ten map cleanly to one of the four categories. The edge cases that initially appear ambiguous (doc updates, dependency bumps, process improvements) absorb into `refinement` because they are behavior-preserving changes. The command body should state this absorb rule explicitly: "doc updates, dependency bumps, and process improvements that do not alter user-observable behavior classify as `refinement`."

No fifth category (`question`, `spike`, `chore`) is needed at the triage layer — `/idea` is an intake front door, not a full project-management taxonomy.

Evidence: EV-001, EV-002, EV-008.

---

### OQ-3 — Inline classification is sufficient; no skill delegation needed

**Recommendation: inline classification (LLM reasoning at invocation time).**

The four categories have clear, non-overlapping definitions when the absorb rules from OQ-2 are stated. LLM reasoning on a vague 1–2 sentence input with 1–2 clarifying answers is sufficient to place the input in one of four bins. The `business-analyst` and `product-owner` skills add value at the specification layer (writing user stories, INVEST criteria, Gherkin acceptance criteria) — not at the triage layer. Delegating to either skill would launch a subagent, requiring the `Agent` tool, which would disqualify `/idea` as a thin command under C-2 and C-4. Every existing thin router command (`memory.md`, `patterns.md`, `learn.md`, `diagram.md`) uses inline routing logic, not subagent dispatch.

A misclassification at triage is low-cost: the user sees the classification before any lifecycle starts (under recommend-and-confirm), can correct it, and the ledger entry records the original intake regardless. The ledger entry is the canonical record; the routing decision is advisory.

Evidence: EV-003, EV-006.

---

### OQ-4 — `--type note` is the correct ledger type; no schema change needed

**Recommendation: `--type note --source /idea --tags intake,<classification>`.**

The valid `--type` set in `ledger.py:60` is:
```
("plan", "decision", "implementation", "artifact", "test-strategy", "rollout", "note")
```
There is no `idea` type. Adding one would require modifying `ledger.py`, violating C-3. The `note` type is the correct catch-all for a raw intake record. It is already used by other commands for informal captures.

`tools/patterns.py` mines four dimensions from the ledger: `tag`, `source`, `type`, and `stop-condition` (`patterns.py:98-104`). The `source` field (`/idea`) provides a distinct pattern-mining signal without a new type. The `tags` field (e.g., `intake,feature` or `intake,bug`) provides secondary signal for `/patterns` to surface. No schema change is in scope for this feature.

Evidence: EV-004, EV-005.

---

### OQ-5 — Memory hook does NOT double-capture on `/idea`; no suppression needed

**Recommendation: no suppression required; the Stop hook is safe.**

`integrations/hooks/memory.settings.example.json:19-27` shows the `Stop` hook calls `ledger.py snapshot --source auto`. The `snapshot` command (`ledger.py:398-445`) captures the *diff against HEAD* — it records working-tree changes, not the invocation itself. A pure `/idea` run that does not write files produces an empty diff (`"snapshot: no changes to capture"` at line 404). Even if the command writes a ledger entry (via `log`), the `MEMORY_EXCLUDE` glob (`ledger.py:58`) explicitly excludes `.praxis/memory/**` from the snapshot diff, so the ledger entry itself is not re-snapshotted.

The `SessionStart` hook runs `bootstrap --brief` and `pending --brief` — orientation commands that do not write entries. Neither hook creates a duplicate `log` entry for an explicit `log` call made by a command.

Conclusion: the explicit `log` call in `/idea` and the `Stop` snapshot hook capture different things (a text record vs a diff) and do not collide. No suppression is needed.

Evidence: EV-009.

---

### OQ-6 — Pass the clarified one-line summary; Phase 0 gates are complementary, not redundant

**Recommendation: pass the clarified summary (not raw input); the two Phase 0 gates are complementary.**

`/idea` asks 1–2 questions to resolve ambiguity at the classification level ("is this a new behavior or a quality improvement?"). `/new-feature` Phase 0 (`new-feature.md:14`) asks 2–3 questions to resolve scope at the planning level ("who is the target user? what is the desired outcome?"). These are different questions at different levels of specificity. `/idea`'s clarification produces a classification-grade summary; `/new-feature`'s Phase 0 produces a planning-grade framing. They are complementary, not redundant.

The argument to pass is the *clarified one-line summary* (not the raw input). The raw input may be ambiguous or misspelled; the clarified summary is what `/idea` understood and what was captured in the ledger. Passing the clarified summary also makes the ledger entry and the downstream command argument consistent, closing a traceability gap.

`/fix-bug` Phase 0 (`fix-bug.md:14`) asks 1–2 focused questions about severity and expected-vs-actual behavior — again, a different level than `/idea`'s classification questions. `/refine` Phase 0 (`refine.md:13`) confirms the improvement goal and behavior-preservation constraint — also complementary.

Evidence: EV-007, EV-010.

---

### OQ-7 — Minimum viable output per classification outcome

**Recommendation: four-line output shape; one sentence of rationale for `not-worth-doing`.**

The minimum viable output per outcome:

**`feature` / `bug` / `refinement`:**
```
Classification: <category>
Captured: <ledger-entry-id> (pending)
Next: /new-feature "<clarified summary>"   ← or /fix-bug / /refine
(Run the command above when ready, or adjust the summary first.)
```

**`not-worth-doing`:**
```
Classification: not-worth-doing
Rationale: <one sentence — why the signal is insufficient or the cost/value ratio is unfavorable>
Captured: <ledger-entry-id> (pending — remains in the ledger if you want to revisit)
```

This satisfies BG-2 (every invocation produces a ledger entry), mitigates R-4 (rationale prevents dismissiveness), and stays under the "thin" constraint of BG-4 and C-2. The command produces no report, no problem statement, no spec fragment.

Evidence: EV-006, EV-011.

---

## Existing solutions and reusable assets

### Shape: thin routing commands

`memory.md`, `patterns.md`, `learn.md`, and `diagram.md` each follow the same shape:
- YAML frontmatter: `description`, `argument-hint`, optional `allowed-tools`
- A one-paragraph statement of purpose
- `$ARGUMENTS` placeholder
- A `## How to handle it` section with a numbered or bulleted routing table
- No subagent dispatch
- Ledger record at the end

`/idea` must match this shape exactly (C-5).

### Ledger CLI

`python .claude/skills/memory/scripts/ledger.py log --type note --title "<clarified summary>" --source /idea --status pending --tags "intake,<classification>" --body "<raw input + clarification Q&A>"` is the complete invocation. No new subcommand or flag is needed.

### No `allowed-tools` needed

`memory.md` has no `allowed-tools` entry. `patterns.md` has a tightly scoped one for the `make patterns` commands. `/idea` needs only `Bash` for the ledger CLI call and `AskUserQuestion` for clarification — both are default tools. No `allowed-tools` entry is required (matching A-6).

---

## Technical constraints discovered

- **T-1** — The `--type` argument to `ledger.py log` must be one of the seven TYPES enum values (line 60). `note` is the correct choice. A new `idea` type would require a `ledger.py` change, violating C-3.
- **T-2** — Clarification questions must be asked in the main conversation, not in a subagent (`new-feature.md:14`, `fix-bug.md:14`). This is already stated in C-8 but is confirmed by inspecting how all three lifecycle commands handle Phase 0.
- **T-3** — The `Stop` hook captures working-tree diffs, not log entries. The `.praxis/memory/**` exclude glob prevents re-capture. No idempotency logic is needed in `/idea`.
- **T-4** — `patterns.py` mines `source` and `tags` fields, not entry titles. The `--source /idea` and `--tags intake,<classification>` arguments give the miner clean, filterable signal without a new ledger type.

---

## Recommendation

**Design direction: thin inline-classification command, recommend-and-confirm routing, `note` ledger type.**

1. Implement `/idea` as `.claude/commands/idea.md` matching the `memory.md` / `learn.md` shape.
2. Ask 1–2 clarifying questions inline (main conversation, `AskUserQuestion`), then classify into one of four categories using inline LLM reasoning.
3. Call `ledger.py log --type note --source /idea --status pending --tags "intake,<classification>"` with the clarified summary as the title and the full exchange (raw input + Q&A) as the body.
4. Emit the four-line output block (three lines for routable outcomes; three lines with rationale for `not-worth-doing`).
5. Stop. Do not invoke the target lifecycle command. Present the invocation string and let the user run it.
6. No `allowed-tools` frontmatter entry. No subagent. No `Agent` tool call.

---

## Traceability

- This artifact id: `RES-idea-command`
- Sources: discovery (`DISC-idea-command`)
- Feeds: spec (`SPEC-idea-command`), alternatives (`ALT-idea-command`)
