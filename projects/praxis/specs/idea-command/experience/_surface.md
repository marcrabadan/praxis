# Experience: <Surface name>

> One contract per user- or system-facing surface, written **after** the spec is
> accepted and **before** the plan (the optional `experience` step). It turns a
> surface into an executable contract that plan, tasks, build, and verify enforce.
> Copy this to `experience/<surface-slug>.md` and fill its companion
> `experience/<surface-slug>.contract.json` (see `_surface.contract.json`).
>
> Skip the experience step only when the spec declares no surfaces (pure
> logic/refactor) — record that the step was skipped and why.

## Why this surface exists

The user/system need this surface serves, traced to a spec requirement.

## Source of truth

The authoritative references (Figma node, API doc, schema, fixture, screenshot).
Each must be reachable or committed before build — an unreadable source is a
hard stop (`U-1`). Mirror these in the contract's `sourceOfTruth`.

## Contract

Lock the behavior in verifiable detail:
- **UI:** layout, hierarchy, copy, tokens, responsive + accessibility behavior, states, motion.
- **api/job/cli/data/integration:** inputs, outputs, side effects, error states, idempotency, retries/scheduling, security, observability.

## Dependency mapping

Every named primitive/module/endpoint/dependency resolves to an existing source
or a planned local artifact (mirror in the contract's `components`). A named
substitution at build time is `U-9`.

## Files owned by this surface

The verifier scopes checks to these. Cross-cutting files belong to scaffold /
cross-cutting, not here. Mirror in the contract's `filesOwned`.

## Verification contract

The gates that prove this surface, drawn from the workflow gate catalog
(`G-*`). Mirror in the contract's `verification`. An unverifiable surface must
not be built (`U-7`).

## Open questions

Anything unresolved gates the surface — it cannot be `accepted` until cleared or
explicitly deferred by a decision.

## Definition of done

Accepted only when: the markdown is approved, the companion JSON validates, every
source of truth is reachable/committed, every named dependency resolves, every
file owned is listed, and every verification gate has pass criteria.
