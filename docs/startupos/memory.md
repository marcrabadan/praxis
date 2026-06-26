# StartupOS — Memory model

StartupOS keeps its working knowledge under [`memory/startupos/`](../../memory/startupos/) at the repo root. It is a **structured store of evidence and decisions** — the substrate the commands read from and write to as an idea moves through the lifecycle.

> This complements, and is distinct from, the Praxis **memory ledger** (`.praxis/memory/ledger.jsonl`, managed by `/memory`). Praxis's ledger tracks *build-time* plans/decisions/implementations with an accept/reject lifecycle. StartupOS memory tracks *pre-build* market and business evidence. When StartupOS records a durable decision (e.g. a selection), it may also log a `pending` entry in the Praxis ledger so the decision is traceable in the same place as everything else.

## Structure

```
memory/startupos/
  ideas/             one file per candidate opportunity
  markets/           market theses, sizing, trends (per idea/market)
  competitors/       competitive maps and threat assessments
  customers/         segments, ICPs, pains, current spend
  interviews/        customer interview notes & synthesis
  pricing/           pricing & willingness-to-pay evidence
  financials/        unit-economics models and scenarios
  hypotheses/        leap-of-faith assumptions, risk-ranked
  experiments/       experiment designs, thresholds, and results
  decisions/         rankings, selections, challenge verdicts, arch calls
  risks/             risk registers and failure modes
  lessons/           post-hoc learnings (what we got right/wrong)
  praxis-handoffs/   export records (date, approver, target, what was validated)
```

Each subdirectory carries a `.gitkeep` so the structure exists in a fresh clone. Files are named by idea slug (`<slug>.md`) or by event (`ranking-<date>.md`, `selection-<slug>.md`).

## How memory is used

1. **Read before deriving.** Every command checks the relevant subdirectory first — *reuse > extend > build*. Research already done is not redone.
2. **Write working artifacts.** Commands persist evidence and decisions as they go, so the next stage has context and the chain stays traceable.
3. **Render templates from memory.** The `docs/startupos/templates/` documents are rendered/updated from what's in memory.
4. **Assemble at export.** `/startupos-export-praxis` reads the full trail to build the Praxis-ready bundle and writes a record to `praxis-handoffs/`.

## Rules for using memory (do not invent facts)

These rules are non-negotiable — they are what make StartupOS trustworthy:

- **Never fabricate.** Do not write a number, quote, or "fact" into memory that you did not observe or source. If you don't have it, write the gap.
- **Label everything.** Every claim in every memory file is `[FACT]` (with source), `[ASSUMPTION]`, `[ESTIMATE]` (with method), or `[HYPOTHESIS]`.
- **Sources are mandatory for facts.** A `[FACT]` without a source is an `[ASSUMPTION]` in disguise.
- **Promote honestly.** An assumption becomes a fact *only* after an experiment or source confirms it — and the confirming evidence is recorded alongside.
- **Decisions are traceable.** A decision file records *what* was decided, *who* approved it (human, for gated decisions), *when*, and the evidence it rests on.
- **Memory is append-friendly.** Prefer adding dated entries over silently overwriting prior evidence; superseded findings stay visible with a note.
- **No build artifacts here.** Code, designs, and implementation belong to Praxis after handoff — not in StartupOS memory.

## Traceability chain

```
observation → idea → market/customer/competitor evidence
   → hypothesis → experiment → result
   → ranking → selection → business-case/pricing/financials
   → prd → architecture → roadmap → praxis-handoff
```

Keeping each link in its subdirectory means any claim in the final handoff can be traced back to the evidence (or the labeled assumption) it came from — the same bidirectional traceability discipline Praxis applies to its spec chain.
