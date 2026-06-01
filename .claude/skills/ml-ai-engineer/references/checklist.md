# Model / AI-System Production-Readiness Checklist

A structured checklist for evaluating whether a model or AI system is ready to expose to users or downstream systems. Each item has a pass criterion. Any fail item must have a documented remediation (with a named owner) before the system goes live.

Use this checklist for: a model's first production deployment, a major retrain or architecture change, a migration to a new model or serving platform, and any LLM/GenAI feature going live. The LLM-specific section (8) applies only to generative/LLM systems.

---

## Section 1: Problem framing and objective

### 1.1 The problem is well-posed
- [ ] The model drives a **specific decision or product outcome**; "what changes when the prediction arrives" is documented.
- [ ] The **target/label** is precisely defined (what, at what grain, ground-truth source), and label quality/noise is understood.
- [ ] The **cost structure** is explicit — the relative cost of a false positive vs false negative (or the error the product cares about) is agreed.

### 1.2 Baseline and bar
- [ ] A **baseline** (heuristic, previous model, or simple model) exists, and the model **beats it** by a margin that justifies its operational cost.
- [ ] A **"good enough to ship"** threshold, tied to the product outcome, was agreed **before** final evaluation — not reverse-engineered from the result.

---

## Section 2: Data and features

### 2.1 Data is representative and sufficient
- [ ] Training data is **representative of production** input; known distribution gaps are documented.
- [ ] There is **enough labeled data**, and collection bias (selection/survivorship/feedback-loop) has been considered.

### 2.2 No leakage, no skew
- [ ] **No target leakage**: no feature is a proxy for, or computed after, the label.
- [ ] **No temporal leakage**: every feature is computed strictly from data available before the prediction time (point-in-time correct).
- [ ] **No train/test contamination**: scalers, encoders, imputers, and feature selection are fit on **train only** (ideally inside a pipeline).
- [ ] **No train/serve skew**: feature transforms in serving are identical to training (shared code or a feature store), and this is verified, not assumed.

### 2.3 Feature handling
- [ ] Missing values are handled with a fitted, documented strategy; informative missingness is captured.
- [ ] Features are versioned/reproducible, and the serving path can compute them within the latency budget.

---

## Section 3: Evaluation

### 3.1 Sound evaluation design
- [ ] The **test set is held out** and was not used for tuning or model selection.
- [ ] The split matches the data: **temporal split** for time-dependent data; **grouped split** so one entity does not straddle train/test.
- [ ] The **evaluation set is representative** of production inputs, including the hard and rare cases.

### 3.2 Right metrics, looked at properly
- [ ] The **primary metric matches the cost structure** (e.g. PR-AUC / recall-at-precision for rare positives, not bare accuracy), and the **decision threshold** is set deliberately from the trade-off.
- [ ] **Slice / subgroup metrics** are reported; performance on segments that matter is acceptable (no hidden failure on a key slice).
- [ ] **Calibration** is checked if the probability (not just the ranking) feeds a downstream decision.
- [ ] The offline metric is **connected to the online outcome** it proxies, and the gap is named (ideally validated by an A/B test).

---

## Section 4: Reproducibility and tracking

- [ ] The experiment is **tracked**: params, metrics, data version, and code version are recorded.
- [ ] **Code, data, and the model artifact are all versioned**, so the model can be reproduced.
- [ ] Seeds and environment (dependencies, runtime) are captured; the result is reproducible within known nondeterminism.
- [ ] The model is in a **registry** with a stage, lineage to its data/code, and the evaluation that justified promotion.

---

## Section 5: Serving and deployment

- [ ] The **serving mode** (batch / online / streaming) fits the freshness need; latency (p99) and throughput meet the budget for online/streaming.
- [ ] The **full pipeline** (preprocessing + model) is packaged and deployed — training/serving parity is guaranteed.
- [ ] Rollout uses a **safe strategy** (shadow and/or canary/gradual), and an **online A/B test** measures the real business metric before full rollout.
- [ ] **Rollback is trivial**: the previous model version is retained and can be re-promoted instantly.

---

## Section 6: MLOps and testing

- [ ] Training and inference run as **automated, version-controlled pipelines**, not manual notebooks.
- [ ] **CI/CD for the model** evaluates against the bar **as a gate** — a model that fails evaluation cannot be promoted.
- [ ] The system has **code, data, and model (behavioral) tests** — known-case behavior is pinned so regressions surface.
- [ ] If retraining is automated, every retrained model is **validated against the current production model** before promotion.

---

## Section 7: Monitoring and incident readiness

- [ ] **Data drift, prediction drift, and (once labels arrive) performance** are monitored — not just infra latency/errors.
- [ ] **Train/serve skew is monitored in production** (served feature values logged and compared to training).
- [ ] **Retraining triggers** (drift threshold, performance decay, cadence) are defined and alert a **named owner**.
- [ ] A documented **incident response for the model** exists: roll back to the last good version, assess who acted on bad predictions, and add the missing monitor/test.

---

## Section 8: Responsible AI

- [ ] **Fairness**: performance/error rates are evaluated across sensitive subgroups; proxy discrimination has been checked; a fairness criterion appropriate to the context is met or the residual risk is accepted by a named owner.
- [ ] **Explainability** appropriate to the stakes is available (interpretable model or post-hoc explanations) where decisions must be justified.
- [ ] **Privacy**: PII in training data is minimized and compliant (consent/regulation); memorization/leakage risk is considered for sensitive data; deletion/right-to-be-forgotten is supported where required.
- [ ] A **model card** documents intended use, training data, evaluation (incl. slices), limitations, and ethical considerations.

---

## Section 9: LLM / GenAI systems (only if applicable)

- [ ] The approach is the **lightest sufficient** one (prompting → RAG → fine-tuning justified), and the **smallest model that passes evals** is used.
- [ ] An **eval set and method** exist and run as a **regression suite** on every prompt/model/RAG change — quality cannot silently regress.
- [ ] Evals measure what matters: **task success, groundedness/faithfulness, relevance, safety/toxicity, format adherence, latency, and cost** (LLM-as-judge is validated against human judgment where used).
- [ ] **Hallucination is mitigated**: answers are grounded in retrieved context, the system can say "I don't know", and sources are cited where applicable.
- [ ] **Structured output** is validated where downstream code consumes it.
- [ ] **Guardrails** are in place: input/output filtering and **prompt-injection** defenses (untrusted retrieved/user content cannot override system instructions); tool-using/agentic actions are scoped and irreversible actions confirmed.
- [ ] **Cost and latency** are budgeted and monitored (caching, streaming, context management).

---

## Go / No-go decision

**Go:** All items in Sections 1–7 (plus 8, and 9 if applicable) are checked, or each unchecked item has an accepted risk documented with a named owner and a remediation deadline.

**No-go:** Any unchecked item in Section 2.2 (leakage / train-serve skew), Section 3 (evaluation soundness), or Section 5 (rollback / parity); unmitigated bias or privacy risk in Section 8; for LLM systems, no working eval/regression suite (Section 9); or more than two unchecked items in any other section without accepted risks and owners.

A no-go is the checklist working as designed. Document the blocking items, assign owners, and schedule the go-live for when the blockers are resolved.
