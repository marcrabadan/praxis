# Architecture Review — <Feature title>

> Produced in the `plan` step alongside the implementation plan, routed to the
> **software-architect**. Its acceptance is the `architecture-validated` gate
> that opens `tasks` — a **criteria-checked** gate (see the workflow manifest's
> `gateCriteria`). Architecture is no longer an implicit sub-activity of the
> plan; it has its own pass/fail.

## Design summary

The chosen design in a few sentences, with a C4-level sketch or link.

## Non-functional requirements

How the design meets the spec's NFRs, each with evidence or rationale.

| NFR | Target | How the design meets it |
|-----|--------|-------------------------|
| Scalability | … | … |
| Availability | … | … |
| Latency | … | … |

## Maintainability & modularity

Boundaries, coupling, and cohesion. Why the seams are where they are.

## Architecture decisions (ADRs)

Link the ADRs under [`../decisions/`](../decisions/). **Any architecture new to
this project must be justified by an ADR** — otherwise the
"unfamiliar architecture" stop condition fires.

## Security-relevant design

Trust boundaries, authn/authz placement, and data handling that the **security
gate** (`G-security`) will scrutinise. Naming them here hands the security
review a map.

## Risks

Architectural risks and their mitigations.

## Gate criteria (must all hold to pass `architecture-validated`)

- [ ] NFRs met with stated evidence or rationale
- [ ] maintainable and modular — clear boundaries, no needless coupling
- [ ] any unfamiliar architecture is justified by an ADR
- [ ] security-relevant design choices are identified for the security gate

## Traceability

- This artifact id: `ARCH-<NNN>`
- Sources: spec (`SPEC-<NNN>`)
- Feeds: tasks (`TASK-<NNN>`)
