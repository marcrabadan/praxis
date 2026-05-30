# Security Review Checklist

A checklist a Security Engineer runs over a change, a feature, or a release before sign-off. Work through every section that the change touches. Each item maps to a control in `practices.md`. Flag outstanding items with a severity rather than ignoring them.

---

## 1. Trust boundaries and threat model

- [ ] The change has been mapped against its trust boundaries; any new boundary (new input, new external call, new privilege) is identified.
- [ ] STRIDE has been considered for each new boundary; realistic abuse cases are written down.
- [ ] The threat model is updated if the design changed; mitigations exist for each high-likelihood/high-impact threat.

---

## 2. Access control (authorization)

- [ ] Every new endpoint, action, and object access enforces authorization **server-side**.
- [ ] Authorization fails **closed**: a missing rule denies access.
- [ ] Object access verifies the principal owns or may access the **specific** object (no IDOR); IDs from the client are never trusted as authorization.
- [ ] Privileges granted are the narrowest that work (least privilege); high-impact actions have segregation of duties.

---

## 3. Authentication and session/token handling

- [ ] Passwords (if any) are stored with Argon2id/scrypt/bcrypt and a per-user salt — never reversible or plain hash.
- [ ] Failed logins are throttled/locked out; secret comparisons are constant-time.
- [ ] Sessions/cookies are `HttpOnly`, `Secure`, `SameSite`, high-entropy, rotated on privilege change, and expired (idle + absolute).
- [ ] Tokens (JWT/OAuth/OIDC) validate signature **and** algorithm (no `alg: none`), `iss`, `aud`, and `exp`; lifetimes are short.

---

## 4. Input validation and output encoding

- [ ] All untrusted input (body, params, headers, cookies, uploads, inter-service responses) is validated allowlist-style at the boundary.
- [ ] Output is encoded for its destination context (HTML/attribute/JS/URL/SQL/shell/LDAP).
- [ ] Paths and Unicode are canonicalized before validation; path-traversal sequences are rejected.
- [ ] File uploads validate content type (not extension), cap size, store outside the web root, and are never executed.
- [ ] No native deserialization of untrusted data; data formats use a strict schema.

---

## 5. Injection sinks

- [ ] Database access uses parameterized queries / prepared statements / bound ORM params — no string concatenation with input.
- [ ] No shelling out with a built command string; arguments are passed as an array and the executable is allowlisted.
- [ ] XML parsing disables external entities (XXE); templates use safe (auto-escaping) rendering.
- [ ] Untrusted input is never reflected into response headers (no CRLF/header injection).

---

## 6. Cryptography and secrets

- [ ] No custom cryptography; a vetted library is used.
- [ ] Encryption is authenticated (AES-GCM / ChaCha20-Poly1305); no ECB; nonces/IVs are never reused with a key.
- [ ] All randomness for tokens/salts/keys uses a CSPRNG, not a general-purpose RNG.
- [ ] Keys live in a KMS or secrets manager, are separated by purpose/environment, and have a rotation plan.
- [ ] **No secrets are committed** to source control, config, or logs; any leaked secret is rotated immediately.
- [ ] Data is encrypted in transit (TLS, validated certs, modern versions/ciphers) and sensitive data at rest.

---

## 7. Dependencies and supply chain

- [ ] A lockfile is committed; versions are pinned so the build is reproducible.
- [ ] SCA has run; no Critical/High known-vulnerable dependencies are introduced (or each is justified/mitigated).
- [ ] New dependencies are intentional, maintained, and not typosquats; internal package names cannot be resolved from public registries.
- [ ] An SBOM is produced/updated where the policy requires it.

---

## 8. Pipeline gates (DevSecOps)

- [ ] Secret scanning, SAST, and SCA run on this change in CI; blocking severities are enforced by policy.
- [ ] IaC and container images (if changed) are scanned for misconfiguration and vulnerable base images.
- [ ] Suppressed findings have an explicit reason and an owner (no silent ignores).
- [ ] The pipeline itself uses least-privilege tokens and pinned action/image digests; secrets do not appear in logs.

---

## 9. Logging, monitoring, and error handling

- [ ] Security-relevant events (authn, authz failures, validation failures, privilege changes) are logged with enough context to investigate.
- [ ] No secrets, tokens, or full PII are written to logs.
- [ ] Anomalies (brute force, authz-failure spikes, abnormal data access) are alertable, not just recorded.
- [ ] Errors fail closed and do not leak stack traces, internal paths, or sensitive data to the client.

---

## 10. Findings and sign-off

- [ ] Every finding has a vulnerability class (CWE where useful), a severity (CVSS where a numeric score is warranted, with the vector recorded), and a concrete fix.
- [ ] Each fix has a regression test or check that proves it.
- [ ] Every open finding ends in a decision: fix, mitigate, accept (with owner + expiry + rationale), or false positive (suppressed with a reason).
- [ ] Residual risk and threat-model assumptions are stated explicitly in the sign-off.
