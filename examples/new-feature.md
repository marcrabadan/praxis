# Sample: `/new-feature` — the core six, end to end

> Illustrative transcript. See [README](README.md) for what that means. `/new-feature` runs the
> six SDLC experts in lifecycle order in **one** conversation, each phase building on the last,
> and closes with the consolidated summary below. (The per-phase working is elided here; the
> deliverable is the summary.)

---

**Prompt**

```text
/new-feature Let returning customers save a payment method at checkout and reuse it next time.
```

---

**Response** *(consolidated plan)*

**Problem & scope** *(Business Analyst)*
Returning, authenticated customers re-enter card details every order. Let them save a method
during checkout and reuse it later. Guests are out of scope. Assumes **tokenized** storage
(processor token, no PAN). Open question: max saved methods per account.

**Prioritized increments + sprint goal** *(Product Owner)*
Thin vertical slices, ordered by value/effort (WSJF):
1. **Save a card at checkout** (opt-in) — unlocks everything else. ⬅ sprint goal.
2. **Pay with a saved card** — the actual time-saving payoff.
3. **Manage saved methods** (list + delete) — table stakes for trust/compliance.

*Sprint goal:* a returning customer can save a card on one order and pay with it on the next.
*DoR:* tokenization confirmed, designs ready. *DoD:* slices 1–2 shipped behind a flag, tests green, audit log live.

**Design decisions, NFRs, risks** *(Software Architect)*
- **ADR-0007:** store only a Stripe `PaymentMethod` token + display metadata → PCI-DSS SAQ-A
  (see [architect-adr.md](architect-adr.md)).
- **Driving NFRs:** security/compliance, then maintainability.
- **Top risk:** the pay-with-saved path must verify token ownership (IDOR). Flagged to security + dev.

**Implementation plan** *(Developer — slice 1)*
- Front end: Stripe.js tokenizes the card; add a "save this card" opt-in on the payment step (auth users only).
- API: `POST /payment-methods` persists `{owner_id, token, brand, last4, exp}`; never logs the token.
- Data: `payment_methods` table, FK to account, unique on `(owner_id, token)`.
- Tasks: schema migration → tokenize on client → persist endpoint (owner-scoped) → account UI list. *No prod code until asked.*

**Test strategy & key cases** *(QA Engineer)*
- *Positive:* save → appears in account with brand/last4; reuse on next order succeeds.
- *Negative:* user A cannot read/charge user B's `method_id` (expect 404); guest sees no save option.
- *Boundary:* expired saved card; deleted method no longer selectable; duplicate save is idempotent.
- Riskiest area = authorization on the pay path → highest regression priority.

**Rollout & production-readiness** *(DevOps Engineer)*
- Ship behind a `saved-payment-methods` flag; canary to 5% → 100%.
- Gates: migration is backward-compatible and reversible; secret scanning on the token path.
- Observe: success/decline rate, p95 latency on pay route, alert on charge-error spike; audit log shipped to the SIEM.
- Rollback: flag off (no schema rollback needed for additive migration).

**Open questions / assumptions**
1. Tokenized storage (assumed) vs. self-stored card data — **confirm**; changes compliance scope entirely.
2. Max saved methods per account?
3. Expired-card behavior: auto-prune or prompt to update?

---

*Next step:* take slice 1 to implementation (`/developer`) or pressure-test the money path
(`/security`, see [security-threat-model.md](security-threat-model.md)).
