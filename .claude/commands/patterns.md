---
description: Mine the memory ledger and stop-condition run logs for recurring patterns — repeated tags, sources, artifact types, stop conditions, and complexity hotspots (files/areas touched by many specs) — and surface them as human-gated promotion candidates. The proactive half of continuous learning. Use to ask "what keeps happening?" or "what should we codify?".
argument-hint: "[MIN=<n>] — recurrence threshold (default 3); omit to run with defaults"
allowed-tools: Bash(make patterns), Bash(make patterns MIN=:*), Bash(python tools/patterns.py:*)
---

Run the continuous-learning **pattern miner** over this repo's durable record:

```bash
make patterns
```

(Pass a threshold with `make patterns MIN=<n>`; default is 3.) It is read-only —
it sweeps `.praxis/memory/ledger.jsonl`, the "Files touched" lists of
`implementation` entries, and the stop-condition run logs under
`projects/*/specs/*/runs/`, and reports recurring **tags**, **sources**,
**artifact types**, **stop conditions**, and **hotspots** (files/areas touched
across many entries). It never mutates the ledger.

Request:

$ARGUMENTS

## How to handle it

1. Run the miner and read its report.
2. Summarise what recurs, highest-signal first. A repeated **stop condition** is
   the strongest signal (a blocker that keeps firing); a repeated **hotspot**
   means the same file/module has absorbed change across several
   specs/refinements — a systemic-complexity signal; repeated **tags/sources**
   suggest a theme worth a rule or skill.
3. For each candidate worth acting on, **propose** — do not auto-create:
   - a recurring blocker → a new `P-*` stop condition, gate, or guardrail;
   - a recurring hotspot → a `/refine` to extract a boundary or reduce coupling
     (route to `software-architect` to confirm scope first);
   - a recurring theme → a rule or a dedicated skill.
   Route the proposal through **`/learn`** (skill-learner → skill-creator) or
   `tools/promote.py`, landing it as a `pending` entry in the memory ledger.
4. **Nothing here is a rule yet.** Promotion is human-gated; surface the
   candidates and let the user choose. If nothing clears the threshold, say so
   plainly rather than inventing a pattern.
