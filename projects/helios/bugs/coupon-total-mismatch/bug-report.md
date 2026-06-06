---
id: coupon-total-mismatch
title: Order total is wrong after removing a coupon
project: helios
type: bug
severity: high
status: fixed
---

# Bug: Order total is wrong after removing a coupon

> **Example** `bug-fix` for Helios (`triage → reproduce → diagnose → fix →
> verify`). Corrective work — no discovery/research/spec chain.

## Summary

Removing an applied coupon does not restore the original total; the discount stays
subtracted, so customers are charged too little (or shown the wrong total).

## Severity & impact

`high` — direct revenue impact and customer trust. Affects any order where a
coupon is applied and then removed before checkout. Seen in production.

## Steps to reproduce

1. Add items to a cart (subtotal €40.00).
2. Apply coupon `SAVE10` → total €36.00.
3. Remove the coupon.

**Expected:** total returns to €40.00.
**Actual:** total stays €36.00.

## Environment

`helios-api` pricing service, commit `a1b2c3d`; reproducible in staging.

## Reproduction status

`reproduced` — captured as a failing test in `helios-api`.

## Traceability

- This bug id: `BUG-coupon-total-mismatch`
- Code area: `helios-api` pricing service (no owning feature spec)
- Downstream: [`root-cause.md`](root-cause.md), [`plans/fix-plan.md`](plans/fix-plan.md)
