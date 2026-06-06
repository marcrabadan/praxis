# Fix Plan — Order total is wrong after removing a coupon

> Step `fix`. Minimal change that restores expected behavior — nothing more.

## Approach

In `helios-api/pricing/cart.py`, have `removeCoupon()` call the shared
`recompute_total()` after clearing the coupon — the same call `applyCoupon()` and
the quantity/address mutations already use. No new behavior, just the missing
recompute.

## Regression test

`test_remove_coupon_restores_total`: apply `SAVE10` to a €40 cart, remove it,
assert total == €40.00. Fails before the fix, passes after.

## Risk & side effects

Low and localized — reuses the existing recompute path. No pricing rules change.

## Traceability

- Fixes: `BUG-coupon-total-mismatch`
- Verified by: [`../reports/verify/report.md`](../reports/verify/report.md)
