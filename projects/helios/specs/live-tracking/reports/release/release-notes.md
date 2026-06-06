# Release Notes — Live delivery tracking

> Final step. **Example — not yet released.** Gate 4 (Release approval, owner:
> tech lead + product owner) requires the verify report to show every acceptance
> check passing.

## Status

not released (awaiting verify completion)

## Summary (planned)

Customers can follow their delivery's live location and ETA; ops can monitor all
in-flight deliveries. Delivered across `helios-api`, `helios-workers`,
`helios-web`, and `helios-console`.

## Acceptance criteria met

To be confirmed against [`../verify/report.md`](../verify/report.md) before release.

## Rollback

Feature-flag the customer tracking page and the SSE endpoint; disabling the flag
reverts to the prior order-status view. ETA publishing in workers is additive and
safe to leave running.

## Traceability

- This artifact id: `REL-live-tracking`
- Sources: `SPEC-live-tracking`, verify report
- Closes: `IDEA-HELIOS-42`
