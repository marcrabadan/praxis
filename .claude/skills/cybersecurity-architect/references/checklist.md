# Security Architecture Review Checklist

A checklist a Cybersecurity Architect runs over a system design before sign-off, or as a risk/audit assessment. Work through every section the design touches. Mark each item pass / fail / N-A and summarize open risks with an owner. Each item maps to a practice in `practices.md`.

---

## 1. Principles and trust model

- [ ] The design layers controls (defense in depth) — no single control is load-bearing.
- [ ] The design assumes breach: blast radius from a compromised component or identity is explicitly bounded.
- [ ] Default-deny and fail-closed apply across access decisions.
- [ ] Controls are **proportionate** to the data sensitivity and threat model — neither under- nor over-engineered.
- [ ] Trust boundaries and trust zones are drawn and documented.

---

## 2. Threat model and risk

- [ ] The attack surface is mapped (entry points, data flows, dependencies, available privileges).
- [ ] Credible threat actors are named with their capability/motivation; controls are sized to them.
- [ ] Each significant threat has a likelihood × impact rating and a treatment (mitigate / transfer / avoid / accept).
- [ ] **Residual risk** is stated explicitly and has a named owner who accepts it.
- [ ] Assumptions (scope, actor capability, in-scope data) are written down.

---

## 3. Identity and access management

- [ ] Authentication is centralized on an IdP; SSO (OIDC/SAML) for humans, workload identity / OAuth client credentials for machines.
- [ ] No shared accounts or long-lived static credentials where a brokered short-lived credential is feasible.
- [ ] Authorization model (RBAC/ABAC) is explicit, centrally decided, and enforced at each resource.
- [ ] Privileged access requires MFA and just-in-time elevation; privileged sessions are recorded/reviewed.
- [ ] Identity lifecycle covers provisioning, periodic access recertification, and **prompt deprovisioning**.

---

## 4. Network and segmentation

- [ ] Trust zones are separated by sensitivity/exposure with default-deny controls between them.
- [ ] Only required flows are allowed (allowlisted east-west and north-south); each is documented.
- [ ] The management/control plane is isolated from the data plane; admin interfaces are not internet-exposed.
- [ ] Data stores are reachable only from the application tier, never directly from the edge.
- [ ] Service-to-service traffic is encrypted (mTLS); network location alone grants no trust.

---

## 5. Data protection

- [ ] Data is classified into sensitivity tiers, and controls scale with the tier.
- [ ] Data is minimized and has a defined retention/deletion schedule.
- [ ] Encryption in transit (modern TLS, validated certs) and at rest is applied per classification; tokenization/field-level encryption is used for the most sensitive fields.
- [ ] Data residency / sovereignty requirements are met; cross-border flows are tracked.
- [ ] Access to classified data is least-privilege, logged, and periodically recertified.

---

## 6. Encryption and key management

- [ ] Only vetted primitives are used (authenticated encryption, modern TLS); no bespoke crypto.
- [ ] Keys use a hierarchy (envelope encryption) rooted in a KMS/HSM; root keys stay in managed hardware.
- [ ] Keys are separated by purpose, environment, and tenant to bound blast radius.
- [ ] Key rotation and revocation are designed in (key versioning; no synchronous full re-encryption required).
- [ ] Access to keys is governed and audited as strictly as access to the data; the design is crypto-agile.

---

## 7. Control frameworks and compliance

- [ ] Controls are mapped to a primary framework (NIST CSF/800-53, ISO 27001, or CIS) so coverage is auditable.
- [ ] Whole-category gaps are checked (e.g. strong Protect but weak Detect/Respond/Recover).
- [ ] Applicable compliance obligations (SOC 2 / GDPR / PCI-DSS / HIPAA) are identified and each maps to a concrete control.
- [ ] The evidence trail (logs, access reviews, change control) is designed in, not retrofitted for audit.
- [ ] Scope-reduction levers (e.g. tokenization/segmentation for PCI) are applied where they cut compliance burden.

---

## 8. Detection, response, and recovery

- [ ] Security-relevant events are logged centrally with enough context to investigate; no secrets/PII in logs.
- [ ] Misconfiguration and anomalous access are alertable, not just recorded.
- [ ] There is a defined path to rotate a leaked credential, revoke a token, and isolate a compromised component quickly.
- [ ] Backups/recovery are protected (e.g. against ransomware: immutable/offline copies) and periodically tested.
- [ ] Incident response roles and escalation are defined for this system.

---

## 9. Cloud architecture (if applicable)

- [ ] Workloads/environments are separated into distinct accounts/subscriptions/projects to bound blast radius.
- [ ] Identity-first access (cloud workload identity/roles); no long-lived access keys; least-privilege, deny-by-default policies.
- [ ] Private subnets for data/compute, controlled egress, private endpoints to managed services; no implicit internet exposure.
- [ ] Encryption-by-default and KMS-managed keys; public storage exposure is blocked.
- [ ] Preventive guardrails (org/service control policies, IaC policy-as-code) and detective posture monitoring are in place.

---

## 10. Decision record and sign-off

- [ ] Significant security decisions are recorded as ADR-style notes (context, decision, alternatives, consequences, residual risk).
- [ ] Every control maps to a named threat and (where relevant) a framework/compliance requirement — no orphan controls or threats.
- [ ] Open risks are summarized with severity and an accepting owner.
- [ ] The design has no unexplained jargon and no control disproportionate to the stated risk and constraints.
