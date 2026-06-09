# Product Definition — /idea intake & triage command

> Step 3 of `feature-development`, between research and spec. Routed to the
> **product-owner**. Bounds the *what* and *why* before the spec pins the
> *how-it-behaves*. Gate `approved-product-definition` opens the spec step.

## Problem & outcome

Praxis users holding a half-formed idea have no friction-free front door.
Invoking `/new-feature`, `/fix-bug`, or `/refine` directly demands a
well-articulated input most ideas do not yet meet — so ideas get misrouted into
the wrong lifecycle, or silently dropped before any ledger record exists.

**The bet:** a single thin `/idea` command that accepts raw input, classifies it
into one of four categories, captures a `pending` ledger entry unconditionally,
and recommends the exact downstream invocation (then stops) removes the
pre-classification burden and guarantees no idea is lost.

**Outcome targeted:** raw thought reaches the correct lifecycle entry point in one
low-friction step, and every intake leaves a durable, mineable ledger record.

## MVP scope

**In scope (the one MVP slice):**
- A thin `.claude/commands/idea.md` (31–41 lines) matching the
  `memory.md` / `learn.md` shape.
- 1–2 inline clarifying questions (`AskUserQuestion`), then 4-way inline
  classification: `feature` → `/new-feature`, `bug` → `/fix-bug`,
  `refinement` → `/refine`, `not-worth-doing` → no route.
- Unconditional `pending` ledger capture via
  `ledger.py log --type note --source /idea --tags "intake,<class>"`.
- Recommend-and-confirm output block, then stop.
- Plugin port (symlink) + regenerated `SKILLS.md`.

**Out of scope:**
- Auto-routing / invoking any downstream lifecycle command.
- Planning, problem-statement, or spec production (downstream owns these).
- Any `ledger.py` schema change (no new `idea` type).
- New `allowed-tools`; subagent / `Agent` / `Skill` dispatch.
- Making `/idea` a required gate for any other command.

## Prioritised requirements

Framework: **MoSCoW.** Chosen over RICE/WSJF because this is a single small
command with no competing-investment trade-offs to score — the only real decision
is in-vs-out of the one slice, which MoSCoW expresses directly. Every spec FR/NFR
is already a Must except the description-uniqueness Should.

| Req id | Requirement | Priority | Traces to | Rationale |
|--------|-------------|----------|-----------|-----------|
| REQ-001 | Thin `idea.md`, 31–41 lines, memory/learn shape | Must | FR-1, NFR-1 / RES-idea-command | Thinness is the feature's identity; over-budget = absorbed downstream logic |
| REQ-002 | ≤2 inline clarifying questions via `AskUserQuestion` | Must | FR-2 / RES OQ-6 | Resolves ambiguity without a full Phase 0 interrogation |
| REQ-003 | 4-way inline classification with absorb rules | Must | FR-3 / RES OQ-2,OQ-3 | The core triage value; four bins are exhaustive for intake |
| REQ-004 | Unconditional `pending` ledger capture (`note`) | Must | FR-4, NFR-5 / RES OQ-4 | No idea silently dropped; mineable by `/patterns` |
| REQ-005 | Recommend-and-confirm output, then stop | Must | FR-5 / RES OQ-1 | Preserves user confirmation; keeps command thin |
| REQ-006 | Clarified summary as title + downstream arg | Must | FR-6 / RES OQ-6 | Ledger record and proposed invocation stay consistent |
| REQ-007 | Input-specific rationale on `not-worth-doing` | Must | FR-7 / RES R-4 | Prevents dismissive feel; preserves intake for revisit |
| REQ-008 | `description` distinct from lifecycle commands | Should | NFR-6 | Stops the router ambiguously selecting `/idea` over a direct lifecycle call |

No follow-up slice is needed: every Must is in the single MVP slice. The only
plausible future increment (a dedicated `idea` ledger type) is explicitly
deferred (OQ-R1, out of scope).

## Sprint goal

Ship a thin, deterministic `/idea` front door that classifies any raw input into
one of four categories, always leaves a `pending` ledger record, and recommends
(never runs) the right lifecycle command.

## Definition of Ready

- [ ] Spec accepted with FRs/NFRs and AC table (done — `spec.md`).
- [ ] Routing model and ledger type decided (done — research/alternatives).
- [ ] Reference exemplars identified (`memory.md`, `learn.md`).
- [ ] No blocking open questions (OQ-R1 is non-blocking, logged).

## Definition of Done

- [ ] `idea.md` exists, 31–41 lines, no `allowed-tools`, no `Agent`/`Skill`.
- [ ] `description` contains "intake and triage", not "plan a feature".
- [ ] All four categories statically mapped to routes in the body.
- [ ] Ledger call uses `--type note --source /idea --tags "intake,<class>"`.
- [ ] Plugin symlink present; `make catalog` regenerated `SKILLS.md`.
- [ ] AC-01…AC-15 pass (the spec's QA targets).

## Success criteria

- 100% of `/idea` invocations produce a `pending` ledger entry (BG-2).
- Classification → route mapping is readable from the file with zero runtime
  inference (NFR-4).
- File length stays ≤41 lines (NFR-1) — the proxy metric for "stayed thin".

## Traceability

- This artifact id: `PROD-idea-command`
- Sources: discovery (`DISC-idea-command`), research (`RES-idea-command`)
- Feeds: spec (`SPEC-idea-command`)
