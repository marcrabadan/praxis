# Validate Workflow

(Replace with the validation procedure. Should be runnable as a script with no LLM in the loop.)

1. Run `scripts/validate.py <path>`.
2. If exit code is 0, declare done.
3. If non-zero, report the error and decide whether to retry or ask the user.

## Stop condition

`scripts/validate.py` exits 0 on the target output.
