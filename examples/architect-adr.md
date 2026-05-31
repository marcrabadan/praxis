# Sample: `/architect` — a decision as an ADR

> Illustrative transcript. See [README](README.md) for what that means.

---

**Prompt**

```text
/architect For saved payment methods, should we store card data ourselves or use
processor tokens? Small team, Stripe is already our processor.
```

---

**Response** *(Software Architect)*

This is a decision worth recording — it's expensive to reverse and it changes your compliance
posture — so here it is as an ADR. The short version: **delegate to Stripe tokens.** Self-storing
card data pulls full PCI-DSS scope onto your systems for zero product upside.

```
# ADR-0007: Use Stripe tokenization for saved payment methods

**Status:** Accepted
**Date:** 2026-05-31
**Deciders:** Architecture, Security Engineering

## Context
We want returning customers to save a card for faster repeat checkout. Two storage options
exist for the card credential. Stripe is already our processor and returns a reusable
`PaymentMethod`/customer token. The team is small (5 engineers) with limited security-ops
capacity. Card data is the highest-sensitivity data we'd ever hold.

## Decision
Store only a Stripe `PaymentMethod` token plus non-sensitive display metadata
(brand, last4, expiry month/year) keyed to our account ID. No PAN or CVV ever transits or
rests in our systems; the browser tokenizes via Stripe.js before anything reaches our API.

## Options considered
1. **Self-store encrypted card data.** Rejected: pulls full PCI-DSS Level 1 scope onto our
   stack (network segmentation, key management, quarterly ASV scans, annual audit). Enormous
   ongoing cost for a 5-person team; one breach is existential.
2. **Stripe tokenization (chosen).** Keeps us in PCI-DSS SAQ-A (the lightest scope). Stripe
   owns the vault. Trade-off: hard dependency on Stripe and its availability/pricing.
3. **Third-party vault (e.g. Basis Theory).** Rejected for now: adds a vendor and integration
   without enough benefit while Stripe is our only processor.

## Consequences
**Positive:** Minimal compliance scope; no card data at rest; faster to ship; smaller blast radius.
**Negative / accepted:** Vendor lock-in to Stripe; saved methods are unusable if we ever switch
processors (migration would require re-collection). Token lifecycle (card expiry, deletion) must
be handled — see follow-up ADR-0008.
```

**Driving NFRs:** Security/compliance (dominant), then maintainability. **Top risk:** treating the
token as low-sensitivity — it still authorizes charges, so authorization on the `pay-with-saved`
path must verify the token belongs to the requesting account (raised to the security review).
