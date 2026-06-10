# Software Architect Practices

Core architecture practices covering non-functional requirements capture, ADR authoring, pattern selection, trade-off analysis, C4 documentation, data and integration design, technology selection, and risk identification.

---

## 1. Non-functional requirements (quality attributes)

Non-functional requirements (NFRs) constrain *how well* a system performs rather than what it does. They are architecturally significant because they eliminate solution options early.

### Canonical quality attributes

| Attribute | Key questions to ask |
|-----------|---------------------|
| **Scalability** | What is the expected peak load? What is the growth horizon (6 months, 2 years, 5 years)? Must scaling be horizontal, vertical, or both? |
| **Availability** | What is the acceptable downtime per month? Is an SLO already defined (e.g. 99.9% = ~44 min/month)? What are the consequences of an outage? |
| **Latency** | What are the p50/p95/p99 targets at the API boundary? Are there synchronous user-facing interactions with hard latency ceilings? |
| **Security** | What data classification applies (PII, PCI, PHI)? What are the authentication and authorization boundaries? What compliance mandates apply (GDPR, PCI-DSS, SOC 2)? |
| **Maintainability** | What is the team size and tenure? What is the expected change rate? Is the codebase shared across teams? |
| **Testability** | Can complex domain logic be unit-tested in isolation (clear boundaries, ports/adapters, injected dependencies)? The team's test-first rule depends on it: a design whose complex logic cannot have its tests written first is not an acceptable design. |
| **Cost** | What is the infrastructure budget? Are there burst-cost risks (traffic spikes, large batch jobs)? Is vendor lock-in a cost risk? |

### Capturing NFRs concretely

Vague NFRs ("the system should be fast") are not architecturally actionable. Every NFR must include:
- A measurable threshold ("p99 latency < 200 ms").
- A measurement condition ("under a sustained load of 1,000 concurrent users").
- A priority relative to other NFRs (latency vs cost, consistency vs availability).

Treat unquantified NFRs as open risks. Escalate to the stakeholder or product owner before committing to an architectural approach that depends on them.

---

## 2. Architecturally significant requirements (ASRs)

Not every requirement drives architecture. ASRs are the subset that constrain or shape the overall structure.

An ASR is architecturally significant if it:
- Affects more than one component or service boundary.
- Forces a choice between mutually exclusive structural options.
- Introduces risk that, if unaddressed, could cause the system to fail its quality targets.
- Cannot be satisfied by a local code change — it requires a cross-cutting decision.

To identify ASRs: walk through each NFR and functional requirement and ask "If we got this wrong, would the architecture need to change fundamentally?" If yes, it is an ASR.

---

## 3. Architectural decision records (ADRs)

An ADR is a short document that captures one significant architectural decision, the context that made it necessary, the options considered, and the consequences of the chosen option.

### When to write an ADR

Write an ADR whenever:
- A decision cannot be reversed cheaply (technology selection, data storage choice, API contract design, service boundary placement).
- The same question is likely to be asked again by a new team member or auditor.
- There is genuine disagreement within the team and the reasoning needs to be traceable.

Do not write an ADR for implementation details that are local to a single component and can be changed without affecting other components.

### ADR format

```
# ADR-NNNN: [Short imperative title, e.g. "Use PostgreSQL as the primary datastore"]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]
**Date:** YYYY-MM-DD
**Deciders:** [Names or roles of people who made or approved the decision]

## Context

[Two to five sentences describing the problem, the constraints, and the forces at play.
State what makes this decision necessary and what changes if the decision is wrong.]

## Decision

[One to three sentences stating the decision taken and the primary reason.]

## Options considered

| Option | Pros | Cons |
|--------|------|------|
| [Option A — the chosen option] | ... | ... |
| [Option B] | ... | ... |
| [Option C] | ... | ... |

## Consequences

**Positive:** [What becomes easier or better.]
**Negative:** [What becomes harder, more expensive, or riskier — do not omit this.]
**Risks:** [Open risks that need monitoring or a follow-up decision.]

## References

[Links to relevant RFC, benchmarks, prior art, or related ADRs.]
```

### ADR discipline

- Number ADRs sequentially. Never delete a deprecated ADR — mark it superseded.
- Store ADRs in version control alongside the code they govern (e.g. `docs/decisions/`).
- One decision per ADR. If two decisions are coupled, write two ADRs and cross-reference them.
- Keep the "Options considered" section even after a decision is made. Future readers need to know what was rejected and why, or they will relitigate the same decision.
- The ADR is the home for design rationale — the team's rule against non-functional inline comments depends on it. The *why* behind a structure, boundary, or trade-off lives in an ADR, never in inline code comments; if an explanation is begging to be written next to the code, it is an ADR (or a rename) waiting to happen.

---

## 4. Trade-off analysis frameworks

### Consistency vs availability (CAP / PACELC)

In a distributed system, under a network partition, the system must choose between consistency (every read returns the latest write) and availability (every request receives a response). Apply PACELC to extend this to the normal (no-partition) case: what is the trade-off between latency and consistency?

- Choose consistency when: financial transactions, inventory counts, access control decisions, or any scenario where a stale read causes real-world harm.
- Choose availability when: product catalog, social feed, recommendation results — where a briefly stale read is tolerable and a failed read is worse than a stale one.
- Document the choice per data entity, not per system. Different entities in the same system may have different requirements.

### Synchronous vs asynchronous integration

| Dimension | Synchronous (REST/gRPC) | Asynchronous (queue/event) |
|-----------|------------------------|---------------------------|
| Latency coupling | Caller waits; latency chains multiply | Caller continues immediately |
| Availability coupling | Provider outage blocks caller | Provider outage is buffered |
| Complexity | Simpler to reason about in isolation | Requires idempotency, dead-letter handling, ordering guarantees |
| Data freshness | Immediate | Eventually consistent |

Use synchronous integration when: the caller needs the result to proceed, the operation must be atomic, or the latency budget is tight.
Use asynchronous integration when: decoupling availability is more important than immediacy, or fanout (one event, many consumers) is needed.

### Build vs buy

| Factor | Lean toward build | Lean toward buy |
|--------|-------------------|-----------------|
| Differentiation | Core competitive capability | Commodity capability (auth, email, payments) |
| Cost | Build effort is small; vendor fee is ongoing | Vendor fee is small relative to build cost |
| Control | Specific customization required | Standard behavior is acceptable |
| Maintenance | Team has capacity to maintain | Team lacks capacity; vendor provides upgrades |
| Lock-in risk | Switching costs are acceptable | Lock-in is a strategic risk |

Default to buy for commodity capabilities. The burden of proof is on build. Document the reasoning in an ADR.

### Monolith vs services

| Signal | Lean toward monolith | Lean toward services |
|--------|---------------------|---------------------|
| Team size | Small (< 8 engineers) | Multiple autonomous teams |
| Release cadence | Single coordinated deployment is acceptable | Teams need independent deployments |
| Operational maturity | Limited observability tooling | Mature platform with service mesh, tracing, per-service alerting |
| Domain clarity | Bounded contexts are not yet stable | Domain boundaries are well-understood and stable |
| Latency budget | In-process calls needed for performance | Network latency is acceptable for the use case |

Prefer a modular monolith until team size or deployment independence forces services. Microservices add distributed system complexity that must be paid for in operational investment.

---

## 5. Architectural patterns

### Layered architecture

**Structure:** Presentation → Application → Domain → Infrastructure. Each layer depends only on the layer below it.

**Use when:** the domain is well-understood, the team is small, CRUD workloads dominate, and rapid development velocity matters more than strict testability of the domain.

**Avoid when:** the domain logic is complex and needs to be tested without infrastructure; business rules frequently change independently of persistence or transport concerns.

### Hexagonal architecture (ports and adapters)

**Structure:** Application core (domain + application services) is surrounded by inbound adapters (HTTP, message consumer, CLI) and outbound adapters (database, external API, email). The core depends only on port interfaces, never on adapter implementations.

**Use when:** the domain is complex and must be testable without database or HTTP; adapters change frequently (e.g. swapping persistence engines, multiple delivery channels).

**Avoid when:** the application is primarily CRUD with minimal business logic; the added abstraction cost exceeds the testability benefit.

### Event-driven architecture

**Structure:** Components communicate by publishing and consuming events through a broker (Kafka, RabbitMQ, EventBridge). Producers do not know their consumers.

**Use when:** fanout is needed (one event triggers many independent reactions); teams need deployment independence; audit trails and temporal decoupling are important.

**Avoid when:** the team lacks experience with distributed messaging; ordering guarantees, exactly-once semantics, or schema evolution are not accounted for; synchronous request/reply is the dominant interaction model.

### Microservices

**Structure:** Each service owns a bounded context, its own datastore, and its own deployment pipeline.

**Use when:** multiple autonomous teams need to deploy independently; service-level SLAs differ significantly across domains; horizontal scaling is needed at the service level.

**Avoid when:** the domain model is unstable (service boundaries drawn too early become expensive to change); the team lacks platform maturity (distributed tracing, health checks, circuit breakers, container orchestration); the network latency cost of remote calls is not budgeted.

### CQRS (Command Query Responsibility Segregation)

**Structure:** Write operations (commands) go through one model optimized for consistency; read operations (queries) go through a separate model optimized for query performance (often a denormalized read replica or projection).

**Use when:** read and write workloads scale independently; the read model requires a different shape than the write model (reporting, search); combined with event sourcing to rebuild read projections.

**Avoid when:** the added complexity of maintaining two models is not justified by load or query complexity; the team is not yet comfortable with eventual consistency on the read side.

### Event sourcing

**Structure:** State is derived by replaying a log of immutable domain events rather than storing the current state directly.

**Use when:** a full audit trail is a regulatory or business requirement; the system must support temporal queries ("what was the state at time T?"); rebuilding read projections from events is required.

**Avoid when:** the team is unfamiliar with the consistency and ordering guarantees required; event schema evolution is not planned for; simple CRUD is sufficient — event sourcing adds significant complexity without a commensurate benefit.

---

## 6. C4 model documentation

The C4 model provides four levels of architectural abstraction. Use the level appropriate to the audience and the decision at hand.

### Level 1 — System Context diagram

Shows the system under design, the users who interact with it, and the external systems it integrates with. No internal detail.

- Audience: executives, business stakeholders, new team members.
- Content: the system as a single box; actors (users, roles); external systems; communication directions labeled with "uses" or "sends events to."
- Rule: every box must be named and every line must be labeled with the nature of the interaction.

### Level 2 — Container diagram

Shows the deployable units inside the system (web app, API, database, message broker, background worker).

- Audience: architects, senior engineers, platform team.
- Content: containers with technology labels; communication protocols between containers (HTTPS, AMQP, SQL); which containers the external actors interact with directly.
- Rule: a container is anything that must be deployed and managed separately. Do not confuse with Docker containers — a container in C4 is a deployment unit, which may or may not use containerization.

### Level 3 — Component diagram

Shows the major components inside a single container.

- Audience: the team building that container.
- Content: components (services, controllers, repositories, domain objects); their responsibilities; the interfaces between them.
- Rule: generate or keep these up to date only if the container is complex enough to warrant it. Many codebases do not need Level 3 documentation.

### Level 4 — Code diagram

A class or sequence diagram for a specific component. Rarely maintained as a persistent artifact; use for communicating a complex algorithm or interaction sequence.

### Documentation discipline

- Always produce Level 1 and Level 2 before design sign-off. Level 3 is optional unless the component contains complex interactions.
- Use text-based diagram formats (Mermaid, PlantUML, Structurizr DSL) so diagrams are version-controlled and diffable.
- Label every arrow with both the protocol and the direction. Ambiguous arrows are the primary source of architecture misunderstandings.

---

## 7. Data and integration design

### Data ownership

Each service or bounded context owns exactly one database schema. No service reads another service's database directly. Data is shared via APIs or events — not shared tables.

### Data contracts

A data contract is the formal interface between a producer and its consumers. It specifies the schema, the versioning strategy, and the SLA for change notification.

- Use semantic versioning for APIs and event schemas: breaking changes increment the major version.
- Never remove or rename a field in a backward-compatible release. Add new fields; deprecate old ones with a documented sunset date.
- For event-driven integration, register schemas in a schema registry (e.g. Confluent Schema Registry, AWS Glue) and enforce compatibility checks in the CI pipeline.

### Integration patterns

| Pattern | Use when |
|---------|---------|
| **Request/response (REST, gRPC)** | The caller needs the result to proceed; the operation is user-facing and latency-sensitive. |
| **Publish/subscribe (events)** | Multiple consumers react to the same event; the producer does not need to know its consumers. |
| **Batch/bulk transfer** | Large data volumes are moved periodically; real-time latency is not required (ETL, reporting). |
| **Saga (choreography or orchestration)** | A business transaction spans multiple services; each step must be compensatable if a later step fails. |
| **Outbox pattern** | A service must atomically write to its own database and publish an event — avoids dual-write inconsistency by writing events to an outbox table in the same transaction, then relaying asynchronously. |

---

## 8. Technology selection criteria

Apply these criteria in order. Stop when a criterion eliminates an option.

1. **Fitness for purpose.** Does the technology satisfy the stated NFRs and ASRs? A technology that cannot meet the availability or latency target is disqualified regardless of other merits.
2. **Team familiarity.** How long would it take the team to operate this technology in production? Unfamiliar technology adds an adoption tax that is often underestimated.
3. **Ecosystem maturity.** Is there an active community, commercial support, and a track record at the required scale? Evaluate the technology at the scale the system will reach, not at current scale.
4. **Operational burden.** What does the team own? Managed services reduce operational burden at the cost of reduced control. Self-hosted solutions give control but require capacity to operate.
5. **Vendor and lock-in risk.** Can the team migrate away if the vendor raises prices, changes terms, or discontinues the product? Document the exit path before committing.
6. **Cost.** Compute total cost of ownership: license or subscription fees, egress costs, engineering time to adopt and maintain, and projected costs at scale.
7. **License compatibility.** For open-source components, verify the license is compatible with the product's distribution model and commercial terms.

Document the evaluation in an ADR. Include rejected options with the reason for rejection.

---

## 9. Risk identification

Architecture risks are conditions that, if they materialize, would prevent the system from meeting its quality attributes or business goals.

### Risk categories

| Category | Example |
|----------|---------|
| **Availability risk** | Single point of failure in the critical path; no failover for the primary database. |
| **Performance risk** | No load test data; assumption that a third-party API can handle peak load. |
| **Security risk** | PII stored without encryption at rest; no rate limiting on the authentication endpoint. |
| **Dependency risk** | Critical dependency on a single vendor with no stated SLA or exit path. |
| **Scalability risk** | Synchronous in-process job that blocks request threads under load. |
| **Operational risk** | No distributed tracing; failures in distributed transactions cannot be diagnosed. |
| **Accidental complexity risk** | A pattern adopted (e.g. microservices, event sourcing) that the team does not yet have the operational maturity to run. |

### Risk register format

For each identified risk, record:
- **Risk ID and title.**
- **Probability:** Low / Medium / High.
- **Impact:** Low / Medium / High (consequence if the risk materializes).
- **Mitigation:** the architectural or operational action that reduces probability or impact.
- **Owner:** the person or team responsible for the mitigation.
- **Status:** Open / Mitigated / Accepted.

Accepted risks must be explicitly acknowledged by the appropriate decision-maker. Untracked risks are not lower in probability — they are just invisible.

---

## 10. Avoiding over-engineering and accidental complexity

**The principle of the simplest architecture that satisfies the stated quality attributes.** Every layer of abstraction, every additional service, and every adopted pattern carries a cost. That cost must be justified by a concrete requirement — not by anticipated future flexibility.

### Common over-engineering signals

- Adopting microservices with a team smaller than can own each service independently.
- Adding a message broker to a system where synchronous calls would suffice.
- Implementing event sourcing when a simple audit log column meets the requirement.
- Building a generic platform before a concrete use case exists.
- Adding abstraction layers to prepare for integrations that are speculative.
- Designing for 100× the current scale when 10× is the realistic growth horizon.

### How to counter over-engineering pressure

- Name the concrete requirement the added complexity satisfies. If none can be named, the complexity is speculative.
- Estimate the adoption cost (engineering days) and compare it to the probability-weighted benefit.
- Apply the "simplest thing that could possibly work" test: would a simpler approach satisfy all the stated ASRs? If yes, choose the simpler approach and record the decision.
- Prefer reversible decisions over irreversible ones. An architecture that can be evolved incrementally is safer than one that front-loads all complexity.

### Systemic complexity: what accumulates across many small, individually-fine changes

Over-engineering is one path to unjustified complexity; the other is the
opposite — many individually reasonable changes, each passing its own review,
that together erode the architecture. No single change is big enough to trip
checklist item 8.5; the cost is systemic, not local, and shows up only in
aggregate (a module that quietly became a god-object, a dependency direction
that quietly reversed).

`/patterns` (`tools/patterns.py`) surfaces this as a **hotspot**: a file or area
that recurs across several distinct specs/refinements (deduplicated by the
originating `source:` decision/spec, so iterative implementation snapshots of
one spec count once, not once per snapshot). Treat 3+ specs/refinements
touching the same file or module as a trigger to re-run the
"Simplicity and reversibility" checklist for that area — even though each
change passed review on its own — and decide whether a `/refine` (extract a
boundary, split a responsibility) is now justified by the accumulated evidence.
This is evidence-based by construction: nothing is restructured until the
recurrence is observed, never in anticipation of it.

### Quantitative thresholds: code-quality metrics

Checklist items 8.6 (hotspot) and 8.7 (maintainability rating) are judgment
calls grounded in numbers, not vibes. `rules/code-quality-metrics.md` gives
the shared vocabulary and default min/max thresholds — Maintainability
Rating, Technical Debt Ratio, Cyclomatic/Cognitive Complexity, Coverage,
Duplicated Lines — aligned to SonarQube's default Quality Gate. Use the repo's
own configured quality gate when one exists; fall back to these defaults when
it does not.
