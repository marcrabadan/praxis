# Refine Plan — Extract the pricing calculator

> Step `plan`. Ordered, behavior-preserving steps; baseline stays green after each.

## Approach

Introduce a `pricing_core` module with pure functions for subtotal, discount, tax,
and total. Move the math out of `helios-api/pricing/cart.py` and
`helios-workers/billing/*` to call it, deleting the duplicates. No rule changes.

## Steps

1. Add `pricing_core` with the functions; cover with the golden fixtures.
2. Point `helios-api` at `pricing_core`; delete its local math. Suite stays green.
3. Point `helios-workers` at `pricing_core`; delete its local math. Suite stays green.
4. Remove now-dead helpers.

## Behavior-preserving evidence

After each step: both repos' suites pass and the 20 golden carts produce identical
totals (diff is empty).

## Rollback

Each step is an isolated commit; revert the offending commit — the prior duplicated
path is restored untouched until the final delete.

## Traceability

- Refines: `REF-extract-pricing-calculator`
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
