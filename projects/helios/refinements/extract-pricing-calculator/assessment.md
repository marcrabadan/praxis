---
id: extract-pricing-calculator
title: Extract the pricing calculator into a single module
project: helios
type: refinement
status: done
---

# Refinement: Extract the pricing calculator into a single module

> **Example** `refinement` for Helios (`assess → plan → change → verify`).
> Quality-only — **observable behavior must not change**.

## Motivation

Pricing math is duplicated across `helios-api/pricing/cart.py` and
`helios-workers/billing/*` with subtle drift (the `BUG-coupon-total-mismatch`
class of defect thrives here). Consolidating into one calculator removes the
duplication and the drift risk.

## Scope

In: extract subtotal/discount/tax/total math into a shared `pricing_core` module
used by both repos. Out: any change to pricing rules or rounding behavior.

## Baseline (behavior to preserve)

- Existing `helios-api` pricing suite (green) as the characterization baseline.
- Golden fixtures: 20 representative carts with expected totals, captured before
  the change; outputs must be byte-identical after.

## Success measure

- Zero duplicated pricing functions across the two repos.
- Golden outputs identical; full suites green.

## Traceability

- This refinement id: `REF-extract-pricing-calculator`
- Related code area: `helios-api` + `helios-workers` pricing
- Decision (structural): [`#`](plans/refine-plan.md) (kept inline — single new module)
