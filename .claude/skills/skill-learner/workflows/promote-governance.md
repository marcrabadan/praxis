# Promote governance

The companion to gap-driven learning: turn a **validated insight** into durable
governance — a new rule, workflow gate, eval, or guardrail — when it generalises
beyond a single skill. Where `detect-gap → create-new | refine-existing` captures
*org knowledge* into skills, this mode captures *behavioural constraints* into the
harness itself.

It runs on the same two rules as the rest of this skill ([references/rules.md](../references/rules.md)):
**propose, never mutate** and **promote on evidence, never on anticipation**. The
deterministic spine is [`tools/promote.py`](../../../../tools/promote.py); this
workflow is the human judgement around it.

## When to use

- A [resolved assumption](../../../../rules/never-assume.md) was confirmed or
  corrected and it is clearly a *standing* rule, not a one-off (e.g. "all
  timestamps are UTC ISO-8601, org-wide").
- A gap you detected is best expressed as a constraint the harness should enforce
  (a gate, a guardrail) rather than knowledge inside one skill.

If the insight is *org knowledge a skill should hold* (a runbook, a convention),
use `detect-gap` instead — that routes to skill-creator. This mode is for
constraints that belong in `rules/`, `workflows/`, or a deterministic check.

## Steps

1. **Confirm the evidence exists.** A promotion from an assumption requires the
   assumption to be `confirmed` or `corrected`. A direct proposal requires
   explicit evidence (incidents, repeated corrections, a decision). No evidence →
   do not promote; record the open question instead.
2. **Pick the target and the smallest home.** `rule` (behaviour-changing
   doctrine), `gate` (a workflow precondition), `eval` (a skill's regression
   case), or `guardrail` (a deterministic check in `tools/`/CI). Prefer the
   smallest, most enforceable home — a checkable guardrail or gate beats a rule
   the model is merely asked to remember.
3. **Record the proposal (pending).** Run the executor — it writes a `pending`
   `decision` to the memory ledger and never touches `rules/`/`workflows/`:

   ```sh
   # from a resolved assumption (target defaults to its --promote intent):
   python tools/promote.py from-assumption ASSUME-… --target rule --draft "…"

   # or directly, with evidence:
   python tools/promote.py propose --target gate --title "verify needs a perf budget" \
     --evidence "3 incidents traced to unbudgeted latency" --draft "…"
   ```
4. **Surface it to the user.** Report the ledger id and the routing the executor
   printed. Acceptance is the user's: `/memory accept <id>`. **Pending is not
   approval.**
5. **Author only after acceptance**, following the printed routing:
   - `rule` → write `rules/<name>.md`, add it to the AGENTS.md rules list, add a
     deterministic check + test if it is mechanically checkable.
   - `gate` → add the condition to `workflows/<id>.workflow.json` (`gates`,
     `loops`, or `stopConditions`); `make validate-harness`; document in `systems/`.
   - `eval` → hand to [skill-creator](../../skill-creator/SKILL.md)'s evaluate
     flow to add cases to the owning skill's `evals/`.
   - `guardrail` → add a validator under `tools/` and wire it into `make`/CI.
6. **Validate.** Run the relevant validator (`make validate-harness`,
   `validate_skill.py`) on whatever was authored.

## Stop conditions

- The evidence rule is not met (the assumption is still open, or no evidence for a
  direct proposal) — stop; do not promote.
- The target is ambiguous between "skill knowledge" and "harness constraint" —
  ask, or default to `detect-gap` (skill) which is the more reversible choice.
- Anything was authored in `rules/`/`workflows/` before the `pending` proposal was
  accepted — that violates *propose, never mutate*. Back it out.

## Output expectations

- A target + destination call, justified (smallest enforceable home).
- A `pending` promotion entry in the memory ledger (via `promote.py`), linked to
  its evidence.
- The routing surfaced to the user, with acceptance left to them.
- Validator result for anything authored after acceptance.
