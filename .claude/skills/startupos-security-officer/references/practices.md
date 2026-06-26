# Security Officer — practices

## Map the valuable data

Where does sensitive data live (PII, secrets, payment, customer data)? Data gravity attracts attackers — name it first.

## Trust boundaries

Identify every boundary where trust changes (user ↔ app, app ↔ third party, tenant ↔ tenant). These are where threats concentrate.

## Abuse surface (think like a CTF player)

Where would an attacker look for the flag? Auth, multi-tenancy isolation, untrusted input, file uploads, AI prompt injection, billing abuse, scraping. List the highest-value targets.

## High-level threat posture

Sketch the top threats (no full STRIDE here — that's Praxis). For each, the impact and whether it changes the architecture or the business model.

## Flag, don't fix

Stay at startup altitude: name risks and boundaries, defer deep mitigation to Praxis's `security-engineer`. But if something is obviously negligent (plaintext secrets, no tenant isolation), flag it loudly as a must-fix-early.
