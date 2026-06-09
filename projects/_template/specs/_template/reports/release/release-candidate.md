# Release Candidate — <Feature title>

> Step 10 of `feature-development`, between verify and release. The candidate is
> assembled once `verify` passes; the `release-candidate-ready` gate (criteria-
> checked) must hold before the final `release-approved` gate can be sought.
> This separates "the change is proven correct" from "we have decided to ship
> it".

## Candidate

What is being proposed for release (build / artifact / commit range).

## Verify result

Link the [verify report](../verify/report.md). Its `overall-result` must be
`pass` with accepted sign-off.

## Security posture

Confirm no open high or critical security finding remains (or link the approved
risk-acceptance decision under [`../../decisions/`](../../decisions/)).

## Release notes (draft)

Draft of the user-facing notes / changelog entry that the `release` step will
finalise.

## Go / no-go checklist (must all hold to pass `release-candidate-ready`)

- [ ] verify report `overall-result: pass` with accepted sign-off
- [ ] release notes / changelog entry drafted
- [ ] no open high or critical security finding

## Traceability

- This artifact id: `RC-<NNN>`
- Sources: verify report, spec (`SPEC-<NNN>`)
- Feeds: release (`REL-<NNN>`)
