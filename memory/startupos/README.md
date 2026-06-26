# StartupOS memory

This is the working knowledge store for [StartupOS](../../docs/startupos/README.md) — the structured evidence and decisions the `/startupos:*` commands read from and write to as an idea moves through the lifecycle.

Full documentation: [docs/startupos/memory.md](../../docs/startupos/memory.md).

## Structure

```
memory/startupos/
  ideas/             one file per candidate opportunity
  observations/      raw signal logs behind candidates
  markets/           market theses, sizing, trends
  competitors/       competitive maps and threat assessments
  customers/         segments, ICPs, pains, current spend
  interviews/        customer interview notes & synthesis
  pricing/           pricing & willingness-to-pay evidence
  financials/        unit-economics models and scenarios
  hypotheses/        leap-of-faith assumptions, risk-ranked
  experiments/       experiment designs, thresholds, results
  decisions/         rankings, selections, challenge verdicts, arch calls
  risks/             risk registers and failure modes
  lessons/           post-hoc learnings
  praxis-handoffs/   export records
```

Files are named by idea slug (`<slug>.md`) or by event (`ranking-<date>.md`, `selection-<slug>.md`).

## The one rule that matters most

**Do not invent facts.** Every claim in every file must be labeled:

- `[FACT]` — observed/sourced (cite the source)
- `[ASSUMPTION]` — believed, unverified
- `[ESTIMATE]` — derived (show the method)
- `[HYPOTHESIS]` — testable, awaiting an experiment

See [docs/startupos/guardrails.md](../../docs/startupos/guardrails.md) for the complete rules.

> `.gitkeep` files preserve the empty subdirectories in a fresh clone. Generated content is committed as the lifecycle progresses.
