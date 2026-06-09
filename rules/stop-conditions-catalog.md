# Stop Conditions Catalog (universal)

This is a **harness rule**. It is the *deterministic, hard-blocker* half of
[stop-conditions.md](stop-conditions.md): an enumerated catalog of observable
triggers that **halt implementation immediately**, each with the exact text to
surface and the gate that must be satisfied to resume.

It sits beside two siblings, and the three cover the whole spectrum of "should I
keep going?":

| Mechanism | For | What happens |
|-----------|-----|--------------|
| [never-assume.md](never-assume.md) + assumptions ledger | a **soft**, low-confidence guess on a reversible choice | log it, keep moving, sweep later |
| [stop-conditions.md](stop-conditions.md) (categories) | **material ambiguity** of judgement (ownership, architecture, security…) | stop and ask |
| **this catalog** (`U/P/S-*`) | a **hard, observable blocker** | halt, write a run log, resume only on the resolution gate |

A stop condition here is **not a feeling of uncertainty** — it is an observable
signal (a value that isn't defined, an asset that doesn't resolve, a gate that
can't run). When one fires, do not substitute a default, skip it, or mark it as
follow-up. Halt, surface the exact `STOP[...]` text, write a
[run log](../projects/_template/specs/_template/runs/_run-log.md), and wait.

## Universal stop conditions

These apply to every spec. A spec's own catalog inherits them
(`inheritsUniversal: true`) and adds project (`P-*`) and spec (`S-*`) entries.

| ID | Trigger (observable) | Surfaced as | Resolution gate |
|----|----------------------|-------------|-----------------|
| U-1 | Required source access is unavailable: a named authority (doc, API, repo, schema, dataset, credential, design source) cannot be read. | `STOP[U-1]: Source access unavailable for <source>. Cannot verify the contract.` | Source becomes readable, or the contract is amended with an approved alternate source. |
| U-2 | A referenced token, variable, config key, schema field, env var, or contract value is undefined. | `STOP[U-2]: Undefined value <name> referenced at <file>:<line>.` | Value is defined in its proper source, removed, or replaced by an approved decision. |
| U-3 | A referenced asset, fixture, data file, script, endpoint, or path does not resolve. | `STOP[U-3]: Path or reference not found: <path>.` | Reference exists, is removed, or is replaced by an approved decision. |
| U-4 | Dynamic behavior (timing, motion, API response, data transform) is specified without a committed reference or measurable criteria. | `STOP[U-4]: Dynamic behavior specified for <surface> without reference or measurable criteria.` | Reference or measurable criteria are committed and linked from the experience contract. |
| U-5 | A named primitive, module, command, endpoint, schema, provider, or dependency is missing. | `STOP[U-5]: Named dependency <name> is referenced but unavailable.` | Dependency is added, the contract is amended, or an approved local substitute is recorded. |
| U-6 | Two active artifacts contradict each other (spec, experience contract, plan, tasks, decision, or source). | `STOP[U-6]: Contradiction between <doc-a> and <doc-b>.` | Resolved by artifact amendment plus a decision trace when non-trivial. |
| U-7 | A required verification gate cannot run. | `STOP[U-7]: Gate <G-name> cannot run: <reason>.` | Gate runs to a definitive pass/fail, or an approved waiver decision changes the requirement. |
| U-8 | An implementation note would claim a gate is green without a verify-report result (self-certification). | `STOP[U-8]: Cannot self-mark gate <G-name> green.` | The gate runs and the verify report records the result, or the note is rewritten to state the gate is unrun. |
| U-9 | A named entity (asset, primitive, route, endpoint, provider, module) is substituted for a differently named one. | `STOP[U-9]: Named substitution detected: contract names <X>, implementation uses <Y>.` | Implementation uses the named entity, or the contract is amended with a decision trace. |
| U-10 | A block marked locked/verbatim is rewritten. | `STOP[U-10]: Locked block <name> rewritten at <file>:<line>.` | Implementation matches the lock exactly, or the lock is removed by an approved amendment. |

## Project- and spec-specific conditions

A spec may add recurring project failure modes (`P-*`) and feature-local hazards
(`S-*`) in its own catalog. Each entry needs the same four parts: a deterministic
**trigger**, the exact **surfaced** `STOP[...]` text, and a **resolution gate**.
The per-spec catalog is `projects/<project>/specs/<spec>/stop-conditions.json`,
validated against [../schemas/stop-conditions.schema.json](../schemas/stop-conditions.schema.json).

## When one fires

1. **Halt** the active step — do not work around it.
2. **Surface** the exact `STOP[...]` text.
3. **Write a run log** ([template](../projects/_template/specs/_template/runs/_run-log.md))
   with evidence and at least two resolution options ("keep going" is never one).
4. **Resume** at the exact blocked step only once the resolution gate is met.

If the blocker is really a *recurring* class worth preventing next time, a
resolved run log is good evidence to **promote a new `P-*` (or a guardrail/gate)**
via [`tools/promote.py`](../tools/promote.py) — pending, human-gated.
