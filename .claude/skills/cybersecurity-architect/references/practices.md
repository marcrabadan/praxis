# Cybersecurity Architect Practices

Core practices for designing and reasoning about security architecture at the system and organization level. Work at the level of trust models, identity, segmentation, data protection, control frameworks, and risk — not single functions.

---

## 1. Foundational principles

Security architecture is the deliberate arrangement of controls so that the failure of any one does not compromise the whole. A handful of principles drive every decision.

- **Defense in depth.** No single control is load-bearing. Layer preventive, detective, and responsive controls so a bypass at one layer is caught at another.
- **Assume breach.** Design as though the perimeter is already crossed. Limit what an attacker who is already inside can reach (blast radius), not just whether they can get in.
- **Least privilege.** Every identity (human or machine) gets the narrowest access that works, for the shortest time. Default deny; grant explicitly.
- **Minimize attack surface.** Fewer entry points, fewer enabled features, fewer trusted parties. Every interface is a liability until justified.
- **Fail securely.** A failing control denies access (fails closed) rather than opening it; errors do not leak internals.
- **Secure by design and by default.** Security is a design input, not a bolt-on; the default configuration is the safe one.
- **Separation of duties.** No single actor can both perform and conceal a high-impact action.
- **Proportionality.** Controls are sized to the risk and the data sensitivity. Over-engineering is a cost and a gap (complexity hides flaws), just like under-engineering.

---

## 2. Zero trust

Zero trust replaces "trusted internal network vs. hostile internet" with "never trust, always verify." Trust is established per request from identity and context, not from network location.

- **Strong identity is the new perimeter.** Every access is authenticated and authorized; network position grants nothing by itself.
- **Verify explicitly.** Decide access from multiple signals — identity, device posture, location, behavior, sensitivity of the resource — not a single factor.
- **Per-request, least-privilege access.** Grant just-in-time, just-enough access; re-evaluate continuously rather than once at login.
- **Microsegmentation.** Partition the environment so lateral movement is contained; a compromised workload reaches only what its identity is explicitly allowed.
- **Assume the network is hostile.** Encrypt service-to-service traffic (mTLS); do not rely on a private network as a trust signal.

Zero trust is a direction, not a product. Adopt it incrementally: start with the most sensitive assets and strongest-identity paths.

---

## 3. Identity and access management (IAM)

Identity is the control plane of a modern system. Most breaches are identity failures.

- **Authentication topology:** centralize on an identity provider (IdP); use **SSO** with **OIDC**/**SAML** for humans and **OAuth 2.0** client credentials or workload identity (mTLS, SPIFFE/SVID, cloud instance identity) for machines. Avoid local accounts and shared credentials.
- **Federation:** federate external identities (partners, customers) rather than provisioning local accounts; map external claims to internal roles at the boundary.
- **Authorization model:** choose **RBAC** for coarse, role-stable access; **ABAC**/policy-as-code (attributes, context) when access depends on resource and request attributes. Centralize policy decisions; enforce them at each resource.
- **Privileged access:** separate admin identities from daily-use ones; require MFA and just-in-time elevation for privileged actions; record and review privileged sessions.
- **Machine and secret identity:** prefer short-lived, automatically-rotated credentials issued by a broker over long-lived static secrets. Secrets live in a manager/KMS, never in code or images.
- **Lifecycle:** provision, review (recertify access periodically), and **deprovision promptly** — orphaned access is a standing risk.

---

## 4. Network segmentation and trust zones

Segmentation limits blast radius: a compromise in one zone should not reach another for free.

- Define **trust zones** by sensitivity and exposure (public/DMZ, application, data, management) and put explicit, default-deny controls between them.
- Allow only the flows the system needs (allowlist east-west and north-south traffic); document each allowed flow and why.
- **Microsegment** at the workload level in dynamic environments; identity-based policy beats IP-based rules that drift.
- Isolate the **management/control plane** from the data plane; admin interfaces are never internet-exposed.
- Put **data stores deepest**, reachable only from the application tier, never directly from the edge.

---

## 5. Data classification and protection

You cannot protect data uniformly — classify it, then apply controls proportionate to its sensitivity.

- **Classify** data into tiers (e.g. public, internal, confidential, restricted/regulated). Classification drives every downstream control.
- **Minimize and retain deliberately:** collect only what is needed, keep it only as long as needed, and delete on a schedule. Data you do not hold cannot be breached.
- **Protect by state:**
  - *In transit:* TLS everywhere, modern versions/ciphers, validated certificates, mTLS for service-to-service.
  - *At rest:* encryption keyed by classification; consider field-level encryption or **tokenization** for the most sensitive fields (e.g. PAN, SSN).
  - *In use:* limit who and what can read it; consider confidential-computing only when the threat model justifies the cost.
- **Data residency and sovereignty:** place and process regulated data in permitted regions; track cross-border flows.
- **Access governance:** access to classified data is least-privilege, logged, and periodically recertified.

---

## 6. Encryption and key-management strategy

Encryption is only as strong as its key management. Architect the key lifecycle, not just the algorithm.

- **Use vetted primitives** (authenticated encryption such as AES-GCM/ChaCha20-Poly1305; modern TLS). Never bespoke crypto. Algorithm choice is the easy part.
- **Key hierarchy:** use envelope encryption — data keys wrapped by key-encryption keys held in a **KMS/HSM**. The root of trust stays in hardware/managed KMS.
- **Separation:** separate keys by purpose, environment, and tenant; the blast radius of a compromised key is everything it can decrypt.
- **Rotation and revocation:** rotate keys on a schedule and on suspicion of compromise; design so rotation does not require re-encrypting everything synchronously (key versioning).
- **Access to keys is access to data:** apply least privilege and audit to KMS operations as strictly as to the data itself.
- **Plan for crypto-agility:** algorithms and key sizes age (and post-quantum migration is coming). Avoid hard-coding crypto choices so they can be swapped.

---

## 7. System-scale threat modeling and risk assessment

At the architecture level, threat modeling is about the **whole system's attack surface and the risk it carries**, not a single function.

- **Map the attack surface:** entry points, trust boundaries, data flows, external dependencies, and the privileges available at each. Tools: data-flow diagrams, STRIDE per boundary, and **attack trees** for the highest-value targets.
- **Model the threat actors:** who would attack this, with what capability and motivation (opportunistic, organized crime, insider, nation-state)? Controls are sized to the credible actor, not the worst imaginable.
- **Assess risk** as likelihood × impact per threat. Rate qualitatively (a risk matrix) or quantitatively where data supports it; record the assumptions.
- **Treat each risk explicitly:** *mitigate* (add/strengthen a control), *transfer* (insurance, contract), *avoid* (drop the feature), or *accept* (with a named owner, an expiry, and a rationale). Every risk ends in one of these.
- **State residual risk.** "Secure" is never a deliverable; the deliverable is a known, accepted residual-risk position.

---

## 8. Control frameworks

Frameworks give a shared, auditable vocabulary so controls are complete and comparable — use them as a checklist of coverage, not a substitute for thinking.

- **NIST Cybersecurity Framework (CSF):** organizes by function — *Govern, Identify, Protect, Detect, Respond, Recover*. Good for communicating posture to leadership and finding whole-category gaps (e.g. strong Protect, weak Detect/Recover).
- **NIST SP 800-53:** a deep control catalog for detailed control selection (common in regulated/government contexts).
- **ISO/IEC 27001 / 27002:** an information security management system (ISMS) — process and governance plus a control set; the basis for certification.
- **CIS Controls:** a prioritized, prescriptive, implementation-oriented set — a strong starting point for "what do we do first."
- Map your controls to one primary framework so coverage is auditable; do not adopt several at once for their own sake.

---

## 9. Compliance as architecture

Compliance obligations are requirements that must become concrete architectural controls — not paperwork bolted on at the end.

- **SOC 2:** trust-service criteria (security, availability, confidentiality, processing integrity, privacy) evidenced by operating controls; architecture must produce the evidence (logs, access reviews, change control).
- **GDPR / privacy:** lawful basis, data minimization, purpose limitation, data-subject rights (access/erasure), and breach notification — drive data classification, retention, residency, and deletion design.
- **PCI-DSS:** protecting cardholder data — drives segmentation (cardholder data environment), tokenization, encryption, and tightly scoped access; reducing scope is the main architectural lever.
- **HIPAA:** protected health information — drives access control, audit, encryption, and business-associate boundaries.
- Translate each obligation into a control and a piece of evidence: *requirement → control → owner → evidence*. Design the evidence trail from the start; retrofitting it for an audit is expensive.

---

## 10. Cloud security architecture

Cloud shifts the controls but not the responsibility; design within the **shared-responsibility model** and use the platform's guardrails.

- **Account/landing-zone structure:** separate workloads and environments into distinct accounts/subscriptions/projects to bound blast radius; centralize logging, identity, and guardrails in a management layer.
- **Identity-first:** use cloud-native workload identity and roles; eliminate long-lived access keys; scope policies to least privilege and deny by default.
- **Network:** private subnets for data and compute, controlled egress, private endpoints to managed services, no implicit internet exposure.
- **Data:** enable encryption by default, manage keys in the cloud KMS (or your own), and prevent public exposure of storage (block public buckets/blobs).
- **Guardrails as code:** enforce policy with preventive controls (org policies, service control policies, IaC policy-as-code) and detective controls (config monitoring, posture management) — manual review does not scale.
- **Centralized detection:** aggregate logs and security findings; make misconfiguration and anomalous access alertable.
- **Apply the platform's well-architected security guidance**, but size controls to your data sensitivity and threat model — do not enable everything by reflex.
