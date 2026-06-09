# Product Definition — <Feature title>

> Step 3 of `feature-development`, between research and spec. Routed to the
> **product-owner**. This is where the *what* and *why* are bounded before the
> spec pins the *how-it-behaves*. Gate `approved-product-definition` opens the
> spec step, and it is **criteria-checked** (see the workflow manifest's
> `gateCriteria`): a human approves only when every criterion below holds.

## Problem & outcome

The discovery problem restated as the product bet, and the outcome it targets.

## MVP scope

Explicit **in scope** / **out of scope** lists. Out-of-scope is as important as
in-scope — it is what keeps the spec bounded.

## Prioritised requirements

Each requirement with a MoSCoW (or RICE/WSJF) rank and a one-line rationale.
Every requirement **traces to a discovery need** (cite the `DISC-`/`RES-` id).

| Req id | Requirement | Priority | Traces to | Rationale |
|--------|-------------|----------|-----------|-----------|
| `REQ-<NNN>` | … | Must \| Should \| Could \| Won't | `DISC-<NNN>` | … |

## Success criteria

Measurable target metrics / signals that tell us the bet paid off. These feed
the spec's acceptance criteria and the acceptance gate.

## Assumptions & open questions

Open product questions. One that gates the spec is a **stop condition** —
resolve it or log it as an assumption with an owner before advancing.

## Traceability

- This artifact id: `PROD-<NNN>`
- Sources: discovery (`DISC-<NNN>`), research (`RES-<NNN>`)
- Feeds: spec (`SPEC-<NNN>`)
