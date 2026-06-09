---
id: ALT-idea-command
title: "Alternatives Analysis — /idea command"
status: draft
traces:
  part-of: "RES-idea-command"
  feeds-spec: "SPEC-idea-command"
---

# Alternatives Analysis — /idea command

> Options considered during research, weighed against each other. The chosen
> direction becomes the spec's baseline; significant rejected options are
> recorded here so the "why not" is traceable.

---

## OQ-1: Routing model — auto-route vs recommend-and-confirm

### Option A — Auto-route (invoke target lifecycle immediately after classification)

- **Summary:** After classifying the input, `/idea` immediately dispatches the target lifecycle command (e.g. calls `/new-feature <clarified summary>` as an inline continuation), passing the clarified summary as its argument.
- **Pros:** Lowest user action count — one invocation produces a running lifecycle. Feels fast for users who trust the classification.
- **Cons:**
  - `/new-feature` Phase 0 asks 2–3 more clarifying questions immediately after `/idea`'s 1–2 questions — the user experiences back-to-back interrogation with no moment to verify the classification before a heavy lifecycle starts (`new-feature.md:14`).
  - The `not-worth-doing` path has no target command — auto-routing is logically inconsistent across all four outcomes. The command would need a branch that does not route for one case.
  - Invoking a lifecycle command from within another command creates an implicit dependency between command files; a change to `/new-feature`'s argument contract would silently break `/idea`.
  - The `Agent` tool or inline continuation would be needed, making `/idea` no longer a "thin command" under C-2 and BG-4.
- **Reuse posture:** build (no existing pattern for command-invokes-command in this repo)

### Option B — Recommend-and-confirm (present classification + route proposal, stop) [CHOSEN]

- **Summary:** After classifying, `/idea` presents the classification, writes the ledger entry, proposes the exact invocation string (e.g. `/new-feature "<clarified summary>"`), and stops. The user invokes the target command themselves.
- **Pros:**
  - Preserves the user's confirmation step between classification and lifecycle start — they can adjust the summary or choose a different command.
  - Consistent across all four outcomes: `feature`/`bug`/`refinement` get a route proposal; `not-worth-doing` gets a rationale and ledger capture only. No branching needed.
  - `/idea` never calls `Agent` or another command — it stays under 80 lines and uses only `Bash` (ledger CLI) and `AskUserQuestion`.
  - Matches the established shape of every thin routing command in this repo (`memory.md`, `patterns.md`, `learn.md`, `diagram.md` — none auto-dispatch a lifecycle).
  - The two Phase 0 gates (`/idea` classification + `/new-feature` scoping) remain separable and complementary rather than back-to-back.
- **Cons:** One more user action (copy-paste or re-type the proposed invocation). For users who trust the classification, this is a small friction cost.
- **Reuse posture:** reuse (direct match of the thin-command shape used by all four reference commands)

**Decision: Option B.** The friction cost of one extra user action is lower than the risks of double-questioning, logical inconsistency on the `not-worth-doing` path, and cross-command coupling. Evidence: EV-007, EV-008, EV-003.

---

## OQ-3: Classification approach — inline LLM reasoning vs skill delegation

### Option A — Inline LLM reasoning (no subagent dispatch) [CHOSEN]

- **Summary:** The command body states the four categories with their absorb rules. The LLM running `/idea` classifies the input directly, using its own reasoning on the user's raw input plus 1–2 clarifying answers.
- **Pros:**
  - No latency from subagent dispatch; no `Agent` tool call required.
  - Keeps `/idea` thin (C-2, BG-4) — the command file stays under 80 lines.
  - Does not require `allowed-tools` beyond defaults.
  - The four categories have clear, non-overlapping definitions when absorb rules are stated (EV-001, EV-002). LLM reasoning on a 1–3 sentence input with clear rules is adequate for triage accuracy.
  - Misclassification is low-cost under recommend-and-confirm: the user sees the classification before any lifecycle starts and can correct it.
- **Cons:** Accuracy is lower than a purpose-built BA/PO skill for genuinely ambiguous inputs. An input like "the authentication feels slow — is that a bug or a refinement?" may require more context than the 1–2 clarifying questions provide.
- **Reuse posture:** reuse (all four reference thin commands use inline routing)

### Option B — Delegate to `business-analyst` or `product-owner` skill

- **Summary:** Dispatch a subagent loaded with the `business-analyst` or `product-owner` skill to classify the input. The subagent returns a classification with rationale.
- **Pros:** Higher classification accuracy for genuinely ambiguous inputs; the BA skill's domain knowledge would catch edge cases.
- **Cons:**
  - Requires the `Agent` tool — `/idea` is no longer thin (violates C-2, C-4).
  - The `business-analyst` skill focuses on specification (user stories, Gherkin AC, stakeholders) — not triage. Using it for a binary classification is over-engineering for the task.
  - Adds subagent latency and token cost disproportionate to triage value.
  - No existing command delegates to a skill subagent just for routing — would be a new pattern with no precedent in this repo.
- **Reuse posture:** extend (would require new pattern)

**Decision: Option A.** The four categories with stated absorb rules are sufficient for LLM-level triage. A misclassification under recommend-and-confirm is low-cost and user-correctable. Skill delegation would violate the thinness constraint and introduce a pattern inconsistent with all existing thin commands. Evidence: EV-003, EV-006.

---

## OQ-4: Ledger type — `note` vs `decision` vs new `idea` type

### Option A — `--type note` [CHOSEN]

- **Summary:** Use the existing `note` type, differentiated from other notes by `--source /idea` and `--tags intake,<classification>`.
- **Pros:**
  - No schema change to `ledger.py` — respects C-3.
  - `patterns.py` mines `source` and `tags` fields independently (`patterns.py:115–120`), giving clean filterable signal for `/patterns` without a new type.
  - `note` is semantically correct: a raw intake record is an informal note, not a plan, decision, or implementation.
  - Idiomatic: the memory skill's own `learn.md` uses `note` type for capturing informal knowledge.
- **Cons:** `note` entries are not distinguished from other notes by type alone — `/patterns` would need to filter by `source=/idea` or `tag=intake` to isolate idea-level captures. Minor inconvenience, not a functional gap.
- **Reuse posture:** reuse (no new code; existing type)

### Option B — `--type decision`

- **Summary:** Record the intake as a `decision` (the user decided to pursue this idea).
- **Pros:** `decision` type is already used for significant calls; surfacing a classification as a decision has semantic precedent.
- **Cons:** A raw intake is not a decision — it is a captured observation. Promoting raw intake to `decision` type inflates the `decision` count in `/patterns` output and blurs the distinction between "we decided X" and "we had an idea about X". Misleading type.
- **Reuse posture:** reuse (but semantically incorrect)

### Option C — New `--type idea`

- **Summary:** Add `idea` to the `TYPES` tuple in `ledger.py:60`.
- **Pros:** Cleanest semantic signal for `/patterns` — a dedicated type would allow `list --type idea` directly.
- **Cons:**
  - Requires modifying `ledger.py` — violates C-3 ("must not propose changes to the ledger schema as part of this feature").
  - Pattern-mining signal is already achievable via `--source /idea` without a schema change.
  - Premature: if intake volume never materially exceeds a handful of entries, a dedicated type adds schema complexity with no payoff.
- **Reuse posture:** build (schema change)

**Decision: Option A.** No schema change needed; `source=/idea` and `tag=intake` provide sufficient mining signal. Evidence: EV-004, EV-005, EV-014.

---

## OQ-1 (not-worth-doing path): ledger-only vs silent drop

### Option A — Capture to ledger + surface rationale [CHOSEN]

- **Summary:** For `not-worth-doing`, write the ledger entry (same as other outcomes), emit a one-sentence rationale, and stop.
- **Pros:** Every invocation produces a ledger entry (BG-2). A rationale prevents the response from feeling dismissive (R-4). The captured entry is revisitable later.
- **Cons:** One extra sentence of output. Negligible.
- **Reuse posture:** reuse (same ledger `log` call as all other outcomes)

### Option B — Silent drop (no ledger entry, no output)

- **Summary:** If classified `not-worth-doing`, simply say so and stop — no ledger capture.
- **Pros:** Minimalist.
- **Cons:** Violates BG-2 (every invocation produces a ledger entry). User has no record of having evaluated the idea. Undermines the "intake front door" value proposition — if ideas silently disappear, `/idea` is no better than doing nothing. Directly contradicts discovery finding BG-2.
- **Reuse posture:** n/a

**Decision: Option A.** BG-2 is explicit: every invocation must produce a `pending` ledger entry regardless of classification outcome. Evidence: EV-011.

---

## Summary of chosen directions

| Question | Chosen option | Key evidence |
|----------|--------------|--------------|
| OQ-1 routing model | Recommend-and-confirm (Option B) | EV-007, EV-008, EV-003 |
| OQ-2 category set | Four categories + absorb rules; no fifth category | EV-001, EV-002 |
| OQ-3 classification | Inline LLM reasoning (Option A) | EV-003, EV-006 |
| OQ-4 ledger type | `--type note` + `--source /idea` + `--tags intake,<class>` | EV-004, EV-005, EV-014 |
| Not-worth-doing path | Capture + rationale (Option A) | EV-011 |

## Traceability

- This artifact id: `ALT-idea-command` (part of `RES-idea-command`)
- Feeds: spec (`SPEC-idea-command`), decisions (`decisions/` directory for any significant ADR)
