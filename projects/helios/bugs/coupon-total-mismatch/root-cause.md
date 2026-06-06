# Root Cause — Order total is wrong after removing a coupon

> Step `diagnose`. Evidenced, not guessed.

## Root cause

`removeCoupon()` in `helios-api/pricing/cart.py:88` clears the coupon reference but
never recomputes the cart total — it leaves the previously discounted `total`
field in place. Only `applyCoupon()` recomputes; removal does not.

## Evidence

A unit test that applies then removes `SAVE10` asserts `total == 40.00` and fails
(returns `36.00`) before the fix. Confirmed by stepping through `removeCoupon()`.

## Why it was not caught

Tests covered *applying* coupons but never *removing* one — a missing case, not a
regression.

## Blast radius

Any mutation that should trigger a recompute. Checked sibling paths: quantity
change and address change both recompute correctly; only removal was missed.

## Traceability

- Root cause for: `BUG-coupon-total-mismatch`
