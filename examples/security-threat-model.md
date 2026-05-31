# Sample: `/security` — STRIDE threat model

> Illustrative transcript. See [README](README.md) for what that means.

---

**Prompt**

```text
/security Threat-model the "pay with a saved card" endpoint: authenticated POST that
charges a stored Stripe token by method_id.
```

---

**Response** *(Security Engineer)*

Trust boundary: an authenticated browser → our API → Stripe. The asset is the ability to
*charge a stored card*. Walking STRIDE over that flow:

| STRIDE | Threat | Likelihood / Impact | Mitigation |
| ------ | ------ | ------------------- | ---------- |
| **S**poofing | Caller impersonates another user to reach the endpoint | Med / High | Authn already required; ensure session/token can't be replayed (short-lived, `Secure`+`HttpOnly` cookies or bearer with exp). |
| **T**ampering | Client supplies `amount`, or a `method_id` they don't own (IDOR) | **High / Critical** | Derive amount server-side from the order; scope `method_id` lookup to `owner = user.id`, return 404 on mismatch. *(This is the blocker the review flagged.)* |
| **R**epudiation | "I never made that charge" | Med / High | Append-only audit log: `(user_id, method_id, order_id, amount, charge_id, ts)`. Rely on Stripe's idempotency keys + receipts. |
| **I**nfo disclosure | Endpoint leaks card details or valid `method_id`s | Low / High | Only ever return brand/last4; never the token. Use 404 (not 403) for unauthorized IDs so existence isn't probeable. |
| **D**enial of service | Charge spam / card-testing via the saved-method path | Med / Med | Per-user + per-IP rate limits on the pay route; Stripe Radar for velocity; CAPTCHA/step-up after N failures. |
| **E**levation of privilege | A normal user triggers admin/refund actions through this route | Low / High | Endpoint does one thing (charge own order); no role-switch parameters; refunds live behind a separate authz'd route. |

### Top mitigations, in priority order
1. **Object-level authorization** on `method_id` (owner-scoped lookup) — closes the Critical IDOR.
2. **Server-authoritative amount** — never trust the client for money.
3. **Idempotency key** on the Stripe call — prevents double-charge on retries.
4. **Rate limiting + audit log** on the pay route — blunts card-testing and gives non-repudiation.

### Notes
- **Scope check:** since only a Stripe token is stored (per ADR-0007), no PAN/CVV is at rest →
  you stay in PCI-DSS SAQ-A. Don't regress that by logging the token in plaintext.
- **Test it:** add a negative test that user A cannot charge user B's `method_id` (expect 404),
  and a declined-card path. *(Handed to QA.)*
