# Sample: `/ml` — framing, leakage, and the right metric

> Illustrative transcript. See [README](README.md) for what that means.

---

**Prompt**

```text
/ml We want to score checkout transactions for fraud risk and auto-decline the risky
ones. I have a notebook hitting 0.98 AUC with features like chargeback_count and
account_status. Is there leakage in these features, and what metric should I optimize?
```

---

**Response** *(ML/AI Engineer)*

Before the metric: that 0.98 is almost certainly **leakage**, not skill, and the metric you
*think* you want (AUC) is the wrong one for an auto-decline. Let me take the assumptions I'm
reasoning from, then the two fixes.

**Assumptions:** the decision is *block this transaction at checkout*; the label is
"transaction was later confirmed fraudulent (chargeback)"; a false positive blocks a paying
customer, a false negative eats a chargeback. Correct me if any of those is off.

### 1. The features leak — both of them

A feature is leakage if it won't exist, *with the same value*, at the moment you score. Walk the timeline:

- **`chargeback_count`** — a chargeback is filed **weeks after** the transaction. At checkout time
  this count reflects the *future*. This is **target leakage**: the feature is partly the label.
  It's why AUC looks magical and why the model will collapse in production, where the count is 0.
- **`account_status`** — if "suspended/closed" gets set *because* of the fraud you're predicting,
  same problem. Only safe if the status as-of-checkout is reconstructable point-in-time.

**Fix:** rebuild features with **point-in-time correctness** — every feature computed strictly from
data available *before* the checkout timestamp (velocity in the last 1h/24h, device/IP history,
billing-vs-shipping mismatch, amount vs the account's norm). Then re-establish the baseline on a
**temporal split** (train on the past, test on a later window) — a random split here also leaks the
future. Expect AUC to drop a lot; that lower number is the *real* one.

### 2. AUC is the wrong target for an auto-decline

Fraud is rare (~0.5–2% positives), so AUC is flattered by the easy negatives, and a threshold-free
metric can't express "don't block good customers." Optimize for the **decision and its costs**:

| Instead of… | Use… | Why |
| ----------- | ---- | --- |
| ROC-AUC | **PR-AUC** | Honest about rare positives; doesn't drown in true negatives. |
| "accuracy" | **Recall at a fixed precision** (e.g. recall @ precision ≥ 0.90) | Auto-decline needs *high precision* — most blocks must be real fraud, or you anger paying customers. |
| default 0.5 cut | a **threshold set from the cost ratio** | The block threshold is a business decision: cost of a chargeback vs cost of a false decline. |

Also report **slice metrics** (by region, card brand, new vs returning) — an aggregate number can
hide that you're disproportionately blocking one segment, which is both a fairness and a revenue problem.

### Ship it safely

- **Baseline first:** a simple rules layer (velocity + amount + AVS mismatch) is the bar. A model
  must beat it by enough to justify the pipeline.
- **Don't auto-decline on day one.** Run in **shadow** against live traffic, compare to the rules,
  then **canary** at a high threshold (decline only the most certain), and **review/queue** the
  middle band for a human rather than blocking outright.
- **Monitor for drift and skew** — fraud patterns shift weekly, so watch PR-AUC on labeled
  outcomes (delayed) plus prediction drift (immediate), and verify the served features match training.

Want me to run the **model production-readiness checklist** over this once the point-in-time
features are rebuilt? *(Upstream feature pipelines/backfill are a `/data` job; the decline UX and
the "your order needs review" message are `/ux` + `/product`.)*
