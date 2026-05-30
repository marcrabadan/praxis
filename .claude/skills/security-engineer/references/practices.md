# Security Engineer Practices

Core application-security practices for threat-modeling, building, and hardening code, dependencies, and delivery pipelines. Work at the level of a function, an endpoint, a dependency, or a CI job.

---

## 1. Threat modeling with STRIDE

Threat modeling is the cheapest security activity per bug prevented because it happens before code exists. Do it for any feature that crosses a trust boundary (handles untrusted input, touches authn/authz, stores sensitive data, or talks to another service).

### The four questions
1. **What are we building?** Draw the data flow: external entities, processes, data stores, and the trust boundaries between them.
2. **What can go wrong?** Walk each element through STRIDE.
3. **What are we going to do about it?** Pick a control per realistic threat.
4. **Did we do a good job?** Validate the model against the implementation; revisit when the design changes.

### STRIDE categories

| Threat | Property violated | Typical control |
|--------|-------------------|-----------------|
| **S**poofing | Authentication | Strong authn, MFA, mutual TLS, signed tokens |
| **T**ampering | Integrity | Input validation, signatures, integrity checks, least privilege on writes |
| **R**epudiation | Non-repudiation | Audit logs, signed events, tamper-evident logging |
| **I**nformation disclosure | Confidentiality | Encryption in transit/at rest, access control, minimizing data returned |
| **D**enial of service | Availability | Rate limiting, quotas, timeouts, resource caps, backpressure |
| **E**levation of privilege | Authorization | Authorization checks on every action, deny-by-default, segregation of duties |

- Anchor the model on **trust boundaries**: the line where data crosses from a less-trusted zone to a more-trusted one. Most vulnerabilities live on these lines.
- Write **abuse cases** alongside use cases: "as an attacker, I submit a crafted ID to read another tenant's record."
- Prioritize by likelihood × impact, not by how interesting the attack is. Fix the boring, likely bugs first.

---

## 2. The OWASP Top 10 with concrete defenses

The Top 10 is the baseline coverage for web and API code. Know each class and its primary defense.

- **Broken access control (IDOR, missing function-level checks):** enforce authorization on every request server-side, deny by default, and check object ownership — never trust an ID supplied by the client. The most common and most severe class.
- **Cryptographic failures:** encrypt sensitive data in transit (TLS) and at rest; never roll your own crypto; see §5.
- **Injection (SQL, NoSQL, OS command, LDAP):** use parameterized queries / prepared statements / safe APIs. Never build a query, command, or path by string concatenation with untrusted input. See §6.
- **Insecure design:** missing threat model. Fix with §1, not with a patch.
- **Security misconfiguration:** disable debug endpoints, default credentials, verbose errors, and unused features in production; set security headers.
- **Vulnerable and outdated components:** track and patch dependencies; see §7.
- **Identification and authentication failures:** strong session/token handling, MFA, lockout/throttling, secure password storage; see §3.
- **Software and data integrity failures:** verify integrity of dependencies, updates, and CI artifacts; protect deserialization; see §7.
- **Security logging and monitoring failures:** log security-relevant events (authn, authz failures, input validation failures) without logging secrets; make them alertable.
- **Server-side request forgery (SSRF):** validate and allowlist outbound URLs; block requests to internal/metadata addresses; do not let user input choose the host.

For deeper, testable requirements, map controls to the **OWASP ASVS** levels rather than to ad-hoc checks.

---

## 3. Authentication and authorization

Authn proves *who you are*; authz decides *what you may do*. They fail differently and must both be enforced server-side.

### Authentication
- Never store passwords reversibly. Use a memory-hard adaptive hash — **Argon2id**, **scrypt**, or **bcrypt** — with a per-user salt. Never SHA-256 alone.
- Throttle and lock out after repeated failures; use constant-time comparison for secrets and tokens to avoid timing leaks.
- Offer / require **MFA** for sensitive accounts and actions.
- Sessions: generate high-entropy IDs, set `HttpOnly`, `Secure`, and `SameSite` cookies, rotate on privilege change, and expire idle and absolute sessions.
- Tokens (JWT/OAuth/OIDC): verify the signature **and** the algorithm (reject `alg: none`), validate `iss`, `aud`, and `exp`, keep lifetimes short, and prefer opaque reference tokens when revocation matters.

### Authorization
- Check authorization on **every** request at the server, for every object and every action — never rely on a hidden UI element or a client-side check.
- Default to **deny**: a missing rule must fail closed, not open.
- Guard against **IDOR**: verify the authenticated principal owns or may access the specific object, not just that they are logged in.
- Apply **least privilege**: grant the narrowest scope/role that works; separate duties for high-impact actions.

---

## 4. Input validation and output encoding

Untrusted input is anything from outside the current trust boundary: request bodies, query and path params, headers, cookies, file uploads, message-queue payloads, and responses from other services.

- **Validate at the boundary**, allowlist-style: type, length, range, format, and character set. Reject what does not match rather than trying to sanitize it into shape.
- **Encode on output** for the destination context — HTML, attribute, JS, URL, SQL, shell, LDAP. The same value is dangerous in one context and safe in another; encode for where it is going.
- Treat **canonicalization** carefully: normalize paths and Unicode before validating, so `..%2f` and look-alikes cannot bypass checks. Reject path-traversal sequences.
- For file uploads: validate type by content not extension, cap size, store outside the web root, and never execute uploaded content.
- For deserialization: avoid native deserialization of untrusted data; prefer data-only formats (JSON) with a strict schema.

---

## 5. Using cryptography correctly

The failure mode is almost never a broken algorithm — it is misuse.

- **Do not invent crypto.** Use a vetted library (libsodium, the platform's crypto stdlib, a maintained TLS stack). Do not implement your own cipher, mode, or protocol.
- **Hashing for storage of secrets:** Argon2id/scrypt/bcrypt (see §3). **Hashing for integrity:** SHA-256/SHA-3. Do not confuse the two.
- **Encryption:** use authenticated encryption (AES-GCM, ChaCha20-Poly1305). Never use ECB. Never reuse a nonce/IV with the same key.
- **Randomness:** use a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `/dev/urandom`) for tokens, salts, IVs, and keys — never `rand()`/`Math.random()`.
- **Keys:** generate with sufficient length, store in a KMS or secrets manager (not in code or config), rotate on a schedule, and separate keys by purpose and environment.
- **TLS:** enforce TLS for all data in transit, validate certificates, disable obsolete versions and ciphers, and use HSTS for browsers.

---

## 6. Injection prevention by sink

Injection happens at a **sink** — the place where data is interpreted by an interpreter. Defend at the sink, not only at the source.

- **SQL/NoSQL:** parameterized queries / prepared statements / an ORM with bound parameters. Never concatenate input into a query. Validate column/table names against an allowlist when they must be dynamic.
- **OS command:** avoid shelling out; if unavoidable, pass arguments as an array (no shell), never build a command string. Allowlist the executable and arguments.
- **Path / file:** canonicalize then verify the resolved path stays within an allowed base directory.
- **LDAP / XML / template / header:** use the library's escaping for that sink; disable XML external entities (XXE); never reflect untrusted input into response headers (CRLF injection / response splitting).

---

## 7. Dependency and supply-chain security

Most modern code is mostly dependencies. The supply chain is now a primary attack surface.

- **Pin and lock:** commit a lockfile; pin versions (or hashes) so builds are reproducible and a published-package swap cannot silently change the build.
- **Scan continuously:** run **SCA** (software composition analysis) in CI to flag known-vulnerable versions (CVEs); fail the build on Critical/High by policy.
- **Generate an SBOM** (e.g. CycloneDX/SPDX) so you can answer "are we affected by CVE-X?" in minutes, not days.
- **Verify integrity and provenance:** prefer signed packages and artifacts; verify checksums; be alert to typosquatting and dependency-confusion (internal package names must not be resolvable from public registries).
- **Minimize surface:** remove unused dependencies; prefer well-maintained, audited libraries over many small unmaintained ones.
- **Protect the build:** treat CI as production — least-privilege tokens, no long-lived secrets in logs, and pinned action/image digests.

---

## 8. DevSecOps — shifting security left in CI/CD

Security controls run as automated gates, early and on every change, so feedback is fast and cheap.

| Gate | Tool class | Catches |
|------|-----------|---------|
| **Secret scanning** | pre-commit + CI | Committed keys, tokens, credentials |
| **SAST** | static analysis | Injection, unsafe APIs, hardcoded secrets, taint flows |
| **SCA** | dependency scan | Known-vulnerable dependencies (CVEs) |
| **IaC scan** | config analysis | Misconfigured cloud/infra, open buckets, permissive policies |
| **Container scan** | image scan | Vulnerable base images and OS packages |
| **DAST** | dynamic analysis | Runtime issues against a deployed instance |

- **Fail fast, fail useful:** a gate that floods developers with noise gets disabled. Tune to high-confidence findings, suppress reviewed false positives explicitly (with a reason and an owner), and break the build only on the severities your policy says must block.
- **Baseline then ratchet:** on a legacy codebase, baseline existing findings and block only *new* ones, then drive the baseline down.
- **Make the secure path the easy path:** provide vetted libraries, secure defaults, and templates so developers do not have to be security experts to ship safely.

---

## 9. Vulnerability management and CVSS

Findings are infinite; capacity is not. Manage them as a prioritized queue, not a panic.

- **Triage every finding:** confirm it is real (not a false positive), determine exploitability in *your* context, and assign an owner and a due date.
- **Score with CVSS** when a consistent numeric severity is needed. The base metrics — attack vector, complexity, privileges required, user interaction, and the confidentiality/integrity/availability impact — produce a 0–10 score and a qualitative band (Low/Medium/High/Critical). Always record the vector string and the assumptions behind it.
- **Adjust for context:** a "Critical" CVE in a dependency you do not actually call may be a Low for you; an internal-only Medium reachable by any user may be your top priority. Score the risk, not the headline.
- **Decide explicitly:** every finding ends in *fix*, *mitigate* (compensating control), *accept* (with an owner, an expiry, and a rationale), or *false positive* (suppressed with a reason). No silent backlog.
- **Define SLAs by severity** (e.g. Critical in days, High in weeks) and track time-to-remediate as the health metric.

---

## 10. Security logging, monitoring, and incident readiness

You cannot respond to what you cannot see.

- **Log security events:** authentication success/failure, authorization denials, input-validation failures, privilege changes, and use of sensitive functions — with enough context (who, what, when, source) to investigate.
- **Never log secrets or full PII.** Scrub tokens, passwords, and sensitive fields before they reach a log sink.
- **Make logs alertable:** brute-force patterns, spikes in authz failures, and anomalous data access should page someone, not sit in a file.
- **Be ready to respond:** know how to rotate a leaked credential, revoke a token, and disable an account quickly. A committed secret is compromised the moment it lands in history — rotate it; a force-push does not erase it from clones and forks.
