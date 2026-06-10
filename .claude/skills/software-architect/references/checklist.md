# Architecture Review Checklist

Run this checklist over a proposed design before sign-off. Mark each item **Pass**, **Fail**, or **N/A** with a brief note. Every Fail must be resolved or explicitly accepted (with an owner and a target date) before the design is approved.

---

## 1. Non-functional requirements (NFRs)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1.1 | Each NFR (scalability, availability, latency, security, maintainability, cost) has been captured with a measurable threshold and a measurement condition. | | |
| 1.2 | NFRs have been prioritized relative to each other; conflicts between NFRs (e.g. latency vs consistency) are documented and resolved. | | |
| 1.3 | Architecturally significant requirements (ASRs) have been identified — the subset of requirements that constrain structural decisions. | | |
| 1.4 | Availability SLOs are stated (e.g. 99.9% uptime = 44 min/month downtime). The design's failure modes have been compared against these SLOs. | | |
| 1.5 | Latency targets (p50/p95/p99) exist for user-facing synchronous operations. | | |
| 1.6 | A peak-load estimate and a growth horizon (e.g. 6 months, 2 years) have been stated and the design validated against them. | | |
| 1.7 | **Team rule — testability:** boundaries and dependencies are designed so complex domain logic can be unit-tested in isolation (test-first is the team norm); no component requires integration infrastructure to test its core logic. | | |

---

## 2. Architectural decisions recorded

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2.1 | Each irreversible or cross-cutting decision (technology choice, service boundary, data storage, API contract style) has an ADR. | | |
| 2.2 | Each ADR includes context, the decision, options considered with pros/cons, and consequences (positive and negative). | | |
| 2.3 | Rejected options are documented in each ADR so the decision cannot be relitigated without new information. | | |
| 2.4 | ADRs are stored in version control alongside the code they govern. | | |
| 2.5 | Build-vs-buy decisions for non-trivial components are documented in an ADR with a cost-of-ownership estimate. | | |
| 2.6 | **Team rule — no non-functional inline comments:** design rationale lives in ADRs, not inline comments; no decision in the design relies on a code comment as its only record. | | |

---

## 3. Pattern and style selection

| # | Item | Status | Notes |
|---|------|--------|-------|
| 3.1 | The chosen architectural style (layered, hexagonal, event-driven, microservices, CQRS, or combination) is stated and justified against the ASRs. | | |
| 3.2 | If microservices are chosen: the team is large enough to own each service independently, the domain model is stable, and the platform has distributed tracing, health checks, and circuit breakers in place. | | |
| 3.3 | If event-driven architecture is used: idempotency, dead-letter handling, schema evolution, and ordering guarantees are addressed. | | |
| 3.4 | If CQRS or event sourcing is used: the added complexity is justified by a concrete requirement (independent read/write scaling, audit trail mandate, temporal queries). | | |
| 3.5 | Over-engineering signals have been checked: no pattern adopted for anticipated future flexibility without a concrete current requirement. | | |

---

## 4. Failure modes and resilience

| # | Item | Status | Notes |
|---|------|--------|-------|
| 4.1 | All single points of failure in the critical path have been identified. Each is either eliminated or its risk has been explicitly accepted. | | |
| 4.2 | The behavior of the system under each failure mode is defined: fail-fast, graceful degradation, retry with backoff, circuit breaker, or fallback. | | |
| 4.3 | External dependency failures (third-party APIs, managed services) are handled: timeouts, retries, circuit breakers, and fallbacks are specified. | | |
| 4.4 | Data loss scenarios have been analyzed: backup and recovery strategy, RPO (recovery point objective), and RTO (recovery time objective) are stated. | | |
| 4.5 | Cascading failure risks have been identified. Bulkhead or rate-limiting patterns are applied where one consumer could exhaust shared resources. | | |

---

## 5. Security

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5.1 | Data classification is documented: which data is PII, PCI, PHI, or otherwise sensitive. Storage and transit protections match the classification. | | |
| 5.2 | Authentication and authorization boundaries are explicit: who can call what, with what credentials, and under what conditions. | | |
| 5.3 | Secrets (API keys, database credentials, certificates) are never hardcoded. A secrets management strategy is in place (e.g. Vault, AWS Secrets Manager, environment injection). | | |
| 5.4 | Input validation boundaries are identified. User-controlled input is validated at the first trust boundary before being passed to downstream systems. | | |
| 5.5 | Applicable compliance mandates (GDPR, PCI-DSS, SOC 2, HIPAA) have been identified and the design addresses their technical requirements. | | |
| 5.6 | Network segmentation is specified: which components are in a private network, which are internet-facing, and what controls exist at each boundary. | | |

---

## 6. Observability

| # | Item | Status | Notes |
|---|------|--------|-------|
| 6.1 | Structured logging is specified at all service entry and exit points. Log format and required fields (trace ID, request ID, service name, severity) are defined. | | |
| 6.2 | Distributed tracing is in place for multi-service flows. A trace can be followed end-to-end across all components in the critical path. | | |
| 6.3 | Metrics are emitted for: request rate, error rate, and latency (the RED method) per service. Infrastructure metrics (CPU, memory, disk, connection pool saturation) are also collected. | | |
| 6.4 | Alerting thresholds are defined for each SLO. Alerts fire before the SLO is breached, not after. | | |
| 6.5 | A runbook or on-call guide exists for each alert. Alert-to-runbook mapping is maintained. | | |
| 6.6 | Correlation IDs are propagated through all inter-service calls and included in log lines and error responses. | | |

---

## 7. Data design

| # | Item | Status | Notes |
|---|------|--------|-------|
| 7.1 | Data ownership is clear: each entity is owned by exactly one service. No service reads another service's datastore directly. | | |
| 7.2 | Data contracts (API schemas, event schemas) are versioned. Breaking changes require a major version increment and a migration path. | | |
| 7.3 | Eventual consistency is acknowledged where it applies. The business impact of stale reads has been assessed and accepted by the relevant stakeholder. | | |
| 7.4 | Database technology choices are justified by the data model and access patterns (relational, document, key-value, time-series, graph) rather than familiarity alone. | | |
| 7.5 | Migration strategy is defined for schema changes: backwards-compatible migrations, dual-write periods, and rollback procedures. | | |
| 7.6 | Data retention and deletion requirements (regulatory and operational) are documented and the storage layer can enforce them. | | |

---

## 8. Simplicity and reversibility

| # | Item | Status | Notes |
|---|------|--------|-------|
| 8.1 | Each component and abstraction in the design can be justified by a concrete requirement. Speculative abstractions are absent. | | |
| 8.2 | The design has been tested against the "simplest architecture that satisfies the stated quality attributes" standard. No simpler alternative was overlooked. | | |
| 8.3 | Irreversible decisions (storage technology, public API contracts, event schema commitments) are identified. The team has explicitly accepted the lock-in implications. | | |
| 8.4 | The design can be evolved incrementally. If requirements change, the first increment of change is achievable without a full rewrite. | | |
| 8.5 | Operational complexity (number of services to deploy, infrastructure components to manage, runbooks to maintain) is proportionate to the team's size and operational maturity. | | |
| 8.6 | **Systemic complexity:** if `/patterns` flags this area as a recurring hotspot (3+ specs/refinements touching the same file or module), the team has re-reviewed it and either planned a `/refine` to extract a boundary or explicitly accepted the continued churn with a reason. | | |

---

## 9. Risk register

| # | Item | Status | Notes |
|---|------|--------|-------|
| 9.1 | A risk register has been produced covering: availability risks, performance risks, security risks, dependency risks, scalability risks, and operational risks. | | |
| 9.2 | Each risk has a probability rating, an impact rating, a mitigation action, an owner, and a status (Open / Mitigated / Accepted). | | |
| 9.3 | Accepted risks are acknowledged by the appropriate decision-maker (not silently carried by the architecture team). | | |
| 9.4 | Third-party dependency risks are included: vendor SLA adequacy, lock-in exposure, support model, and exit path. | | |

---

## 10. Documentation completeness

| # | Item | Status | Notes |
|---|------|--------|-------|
| 10.1 | A C4 Level 1 (System Context) diagram has been produced and reviewed by at least one non-technical stakeholder. | | |
| 10.2 | A C4 Level 2 (Container) diagram has been produced with all containers named, technology-labeled, and communication protocols annotated. | | |
| 10.3 | All ADRs are linked from the architecture document or README so they are discoverable by new team members. | | |
| 10.4 | Open questions and unresolved trade-offs are listed explicitly. None are hidden inside diagrams or implied by the absence of a decision. | | |

---

## Sign-off summary

Complete this table before the design is approved:

| Section | Overall status | Open Fails | Accepted risks |
|---------|---------------|------------|----------------|
| 1. NFRs | | | |
| 2. Decisions recorded | | | |
| 3. Pattern selection | | | |
| 4. Failure modes | | | |
| 5. Security | | | |
| 6. Observability | | | |
| 7. Data design | | | |
| 8. Simplicity | | | |
| 9. Risk register | | | |
| 10. Documentation | | | |

**Decision:** Approved / Approved with conditions / Rejected

**Conditions (if any):** [List items that must be resolved before implementation begins]

**Approvers:** [Names and roles]

**Date:** YYYY-MM-DD
