# Sample: `/analyst` — idea → user stories

> Illustrative transcript. See [README](README.md) for what that means.

---

**Prompt**

```text
/analyst Let customers save a card during checkout so they don't re-enter it next time.
```

---

**Response** *(Business Analyst)*

One thing materially changes scope, so I'll flag it rather than guess: **are we storing card
data ourselves, or delegating to the payment processor (e.g. a Stripe/Braintree token)?** I'll
write the stories for the **tokenized** case (no PAN ever touches our systems) — the safer
default — and flag the alternative as an open question.

### Requirements

**Functional**
- FR-1: A customer can opt to save the payment method used for the current order.
- FR-2: A returning, authenticated customer can select a previously saved method at checkout.
- FR-3: A customer can delete a saved method from their account.

**Non-functional**
- NFR-1 (Security): No raw PAN/CVV is stored; only a processor token + display metadata (brand, last4, expiry).
- NFR-2 (Privacy): Saved methods are scoped to the owning account and never exposed cross-account.

### User stories

**US-1 — Save a card at checkout**

> As a **returning customer**, I want to **save my card while paying** so that **I don't re-enter it on my next order**.

*INVEST:* Independent (no dependency on US-2/3) · Negotiable · Valuable (faster repeat checkout) ·
Estimable (small, given the processor already returns a token) · Small · Testable (see AC).

```gherkin
Scenario: Customer opts in to saving a card
  Given an authenticated customer is on the payment step
  And they have entered valid card details
  When they tick "Save this card for next time" and place the order
  Then the order is paid
  And a saved method showing brand + last4 + expiry appears in their account
  And no PAN or CVV is persisted anywhere in our systems

Scenario: Guest checkout cannot save a card
  Given an unauthenticated (guest) customer is on the payment step
  When the page renders
  Then the "Save this card" option is not offered
```

**US-2 — Pay with a saved card** *(stories US-2 and US-3 abbreviated for the sample)*

> As a **returning customer**, I want to **pick a saved card at checkout** so that **I can pay in one tap**.

```gherkin
Scenario: Reuse a saved card
  Given an authenticated customer with at least one saved method
  When they select it and place the order
  Then the order is paid using that method without re-entering card details
```

### Open questions (for stakeholders)
1. **Tokenized vs. self-stored card data?** Assumed tokenized. Self-storing pulls full PCI-DSS
   scope into our systems — confirm before estimating.
2. Max number of saved methods per account? (Affects US-3 / list UI.)
3. What happens to a saved method when the underlying card expires — auto-prune or prompt?

*Readiness: US-1 passes the BA readiness checklist; US-2/US-3 are blocked on open question #1.*
