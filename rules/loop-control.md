# Loop Control

This is a **harness rule**. It is short and behavior-changing. It governs the
*keep going* lane of agent work — the build → verify → fix → verify loop that
runs until a change actually meets expectations. Its single job is to make that
loop **converge or escalate**, never spin.

It completes the trio that decides what an agent does at each step:

- [stop-conditions.md](stop-conditions.md) — *stop and ask* on material ambiguity.
- [never-assume.md](never-assume.md) — *log and validate* a low-stakes guess.
- **loop-control.md** (this rule) — *keep iterating, but bounded*.

## The rule

A loop that retries work toward a goal must, before its first iteration, declare
a **terminal predicate** and a **budget**. Without them, "loop until correct"
degenerates into "loop forever".

1. **Terminal predicate.** An explicit, checkable set of acceptance criteria —
   all of which must be met for the loop to be `done`. No empty predicates: a
   loop with nothing to satisfy can never legitimately finish. Criteria come from
   the spec / Definition of Done, not invented mid-loop.
2. **Budget guard.** A maximum number of iterations. Hitting it is not failure —
   it is a checkpoint that forces the agent to surface state to the user.
3. **No-progress guard.** If the progress signature (criteria-met count + a
   free-form state signal, e.g. test output) is unchanged for *patience*
   consecutive iterations, the loop is stuck. Retrying the same failing action
   is not iteration.

## Every iteration yields one verdict

From a **closed set** — never invented:

- `continue` — predicate not yet met, progress is being made, budget remains.
- `done` — every criterion is met. The terminal predicate wins even on the last
  allowed iteration.
- `escalate` — a guard tripped (budget exhausted or no progress). **Stop.**

## Escalate, don't grind

`escalate` is a real stop, not a log line. When a guard trips the agent **does
not keep going**. It brings the user the current state, the specific blocker, and
options — exactly as a [stop condition](stop-conditions.md) would. The loop can
only continue after the user gives guidance (and, if warranted, a larger budget):
that is what `resume` is for. Silently widening your own budget to keep grinding
defeats the rule.

## The loop controller

Loops are tracked deterministically in `.praxis/loops/` via the CLI — never
hand-edited. The *judgement* (is criterion `c2` met?) is the agent's; the
*verdict* is computed the same way every time:

```sh
python tools/loop.py start --goal "OAuth slice passes verify" \
  --criterion "all unit tests green" \
  --criterion "lint clean" \
  --criterion "spec acceptance checks pass" \
  --max-iterations 8 --patience 3

python tools/loop.py tick <id> --met c1 --met c2 --signal "1 failing: token refresh"
# -> VERDICT: continue  (c3 still unmet)
python tools/loop.py tick <id> --met all
# -> VERDICT: done
```

Status set: `running → done | escalated | abandoned` (an `escalated` loop returns
to `running` only via `resume`). The shape is enforced by
[../schemas/loop.schema.json](../schemas/loop.schema.json).

## Where this fits the workflow

A workflow step that iterates (notably `verify`, and corrective `fix → verify`)
opens a loop whose predicate is that step's acceptance criteria. `done` clears
the step; `escalate` is a local stop condition that hands control back to the
user. When a `correct`ed [assumption](never-assume.md) invalidates work already
done, the loop's predicate is what tells you how far back to re-run. This is how
"never-ending until expectations are met" stays honest: it ends — by meeting the
predicate, or by escalating to a human — and never just spins.
