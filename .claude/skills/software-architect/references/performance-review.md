# Performance Review (owns the `G-performance` gate)

The software-architect is the **owning expert for the `G-performance` verify
gate** on the build-time side — performance budgets, the review method, and the
regression threshold a change must not cross. The runtime/operations side (SLOs,
error budgets, production load behaviour, alerting) is owned by the
**devops-engineer** (`references/practices.md`). Together they answer the gate's
pass criterion: *performance-sensitive surfaces meet their stated budget with
evidence; none regress beyond threshold.*

Use this when adjudicating `G-performance`, when a spec/architecture-review names
a latency/throughput/resource requirement, or when the Validation Orchestrator
routes a performance question.

## When the gate applies

`G-performance` is **conditional** — it applies to runtime-bearing surfaces
(`screen`, `flow`, `api`, `job`, `data`, `integration`). A pure CLI/library
change records `n/a` with a one-line reason. If a surface *has* a performance
budget in its spec or experience contract, the gate is **not** optional for it.

## Set the budget before you measure

A gate with no budget proves nothing. Each performance-sensitive surface needs an
explicit, falsifiable target captured in the spec or architecture review:

| Dimension | Example target |
|-----------|----------------|
| Latency | p95 < 200 ms, p99 < 500 ms at expected concurrency |
| Throughput | ≥ 500 req/s sustained; ≥ N rows/s for a job/pipeline |
| Resource | peak memory < X MB; CPU < Y cores; cold start < Z ms |
| Frontend | LCP < 2.5 s, INP < 200 ms, CLS < 0.1 (defer CWV detail to frontend-architect) |
| Data | batch SLA window; partition scan bounded; no full-table scan on hot path |

Pick the dimensions the surface actually exercises — do not invent budgets for
dimensions that do not matter.

## Review method

1. **Identify the hot path** — the operation under the budget, at the stated
   concurrency/data volume. Performance off the hot path is usually noise.
2. **Establish a baseline** — measure the current/main version under the same
   conditions, so "regression" has a reference. No baseline ⇒ the gate cannot
   prove "no regression"; that is stop condition `U-4` (dynamic behaviour without
   a measurable reference).
3. **Measure under representative load** — realistic data sizes and concurrency,
   warm and cold. A single happy-path call is not evidence.
4. **Compare to budget and baseline** — pass only if the surface meets its budget
   **and** does not regress beyond the threshold (e.g. > 10% p95 latency, or any
   new full-table scan / N+1 / unbounded allocation on the hot path).
5. **Watch the usual regressions** — N+1 queries, missing indexes, unbounded
   result sets, synchronous calls in a loop, chatty network hops, large bundles,
   memory growth, and accidental O(n²).

## Evidence the gate records

The verify report's `G-performance` row must cite **the budget and the measured
result** (or why it is `n/a`) — not a claim. Acceptable evidence: a benchmark
command + numbers, a load-test summary, a profiler flame graph reference, or a
query plan. "Looks fast" is not evidence (`U-8` self-certification).

## Verdict

- **pass** — every performance-sensitive surface meets its budget with evidence,
  none regress beyond threshold.
- **fail** — a budget is unmet or a regression exceeds threshold. Route back to
  `build` (the failure transition) with the specific surface, number, and target.
- **escalate** — the budget itself is wrong/absent or the trade-off (cost vs
  latency) is the user's call. Bring the numbers and at least two options.
