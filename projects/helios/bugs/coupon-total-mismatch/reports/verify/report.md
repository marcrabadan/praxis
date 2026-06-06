# Verify Report — Order total is wrong after removing a coupon

> Step `verify`. Evidence the bug is fixed and stays fixed.

## Result

`fixed`

## Evidence

- Regression test `test_remove_coupon_restores_total` now passes (failed before
  the fix).
- The original repro (apply then remove `SAVE10` on a €40 cart) returns €40.00.
- Full `helios-api` pricing suite green; coupon apply/quantity/address paths
  unaffected.

## Traceability

- Verifies fix for: `BUG-coupon-total-mismatch`
