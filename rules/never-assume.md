# Never Assume, Always Validate

This is a **harness rule**. It is short and behavior-changing. It is the spine of
deterministic, spec-driven work: an agent must not let a silent guess become an
unexamined fact the rest of the work is built on.

It works **with** [stop-conditions.md](stop-conditions.md), not instead of it.
Stop conditions cover ambiguity that is *material* — where guessing wrong would
change ownership, destination, behavior, architecture, security posture, or the
verification standard. Those still make the agent **stop and ask now**. This rule
covers the residue: the smaller, low-stakes, reversible choices an agent makes to
keep moving. Those must not vanish — they are **logged as assumptions and
validated later**.

## The rule

1. **High confidence → assert.** If you are certain, you are not assuming. Record
   it as a decision (memory ledger / project decisions) and proceed.
2. **Material ambiguity → stop.** If the choice meets any
   [stop condition](stop-conditions.md), stop and ask before acting. Do not log
   it and barrel ahead.
3. **Low-stakes, reversible, uncertain → log, then proceed.** Record the
   assumption in the assumptions ledger, keep working, and let the sweep validate
   it. Never guess silently.

If you cannot honestly place a choice in (1) or (3), treat it as (2) and stop.

## The assumptions ledger

Assumptions live in `.praxis/assumptions/` (committed, durable), managed only by
the CLI — never hand-edited:

```sh
python tools/assumptions.py add \
  --statement "the upstream API returns ISO-8601 timestamps" \
  --impact "date parsing in the ingest worker" \
  --confidence low --source /developer \
  --alt "epoch millis" --alt "RFC-2822" \
  --body "No schema was supplied; assumed ISO-8601 to keep the slice moving."
```

Each entry has a typed id (`ASSUME-…`), a confidence (`low | medium` — high is
not an assumption), the alternatives considered, and a status from one **closed
set**: `open → confirmed | corrected | withdrawn`. The shape is enforced by
[../schemas/assumption.schema.json](../schemas/assumption.schema.json).

## The sweep (validate, deterministically)

Before a workflow gate, before release, or whenever the user asks, **replay open
assumptions**:

```sh
python tools/assumptions.py sweep        # or --json for the agent to render
```

`sweep` is deterministic: it orders open assumptions lowest-confidence first and
shapes each into a question whose **recommended answer (option A) is exactly what
the agent assumed**, with the alternatives as options B, C, … and a free-form
answer always allowed. The agent renders these as real questions; the *asking* is
the agent's, the *selection and ordering* is the tool's.

## Resolution → decision → (proposed) promotion

Every answer is adjudicated and recorded — the answer never lives only in chat:

- **Confirmed** (`confirm <id>`): the user agreed. Record it as a decision.
- **Corrected** (`correct <id> --answer "…"`): the assumption was wrong. Record
  the correction as a decision, and check whether anything built on it must
  change — that may send the workflow **back a step** (implement → test → spec).
- **Withdrawn** (`withdraw <id>`): the assumption became moot.

When a confirmed or corrected answer **generalises** — it is not a one-off but a
rule the team should always follow — propose promoting it:

```sh
python tools/assumptions.py confirm <id> --decision <ledger-id> --promote rule
```

`--promote rule | guardrail | eval | gate` records the *intent*. The promotion
itself is **proposed through the memory ledger as `pending`** (route via
`skill-learner` / `/learn`) and **never applied silently** — a wrong promotion
poisons every future run. **Pending is not approval**: the user accepts before
any rule, guardrail, eval, or gate is actually added. This is how the workflow
*learns*: a human decision becomes durable governance, deterministically and
under review.

## Why this is deterministic

The judgement (was the assumption right?) is the user's. Everything around it is
deterministic and inspectable: the log shape, the lowest-confidence-first
ordering, the option layout, the closed status set, and the hard line that
promotion is always human-gated. The model never quietly upgrades a guess into a
fact, and never quietly upgrades a decision into a rule.
