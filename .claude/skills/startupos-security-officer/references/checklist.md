# Security Officer — review checklist

## Data & boundaries
- [ ] Where sensitive data lives is identified.
- [ ] The major trust boundaries are named.

## Abuse surface
- [ ] The highest-value attack targets are listed (auth, tenancy, input, AI injection, billing).
- [ ] AI-specific risks (prompt injection, data leakage) are considered if the product is AI-native.

## Posture & handoff
- [ ] The top high-level threats are named with their impact.
- [ ] Anything obviously negligent is flagged as must-fix-early.
- [ ] Items for Praxis's `security-engineer` are flagged for the handoff.
- [ ] Deep mitigation is deferred to Praxis (right altitude).
