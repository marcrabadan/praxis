# Data-Product / Pipeline Production-Readiness Checklist

A structured checklist for evaluating whether a dataset, pipeline, or data product is ready to expose to consumers. Each item has a pass criterion. Any fail item must have a documented remediation (with a named owner) before the data product goes live.

Use this checklist for: new dataset go-lives, a pipeline serving its first downstream consumer, major schema or grain changes, a migration to a new platform, and periodic data-product reviews.

---

## Section 1: Correctness and modeling

### 1.1 Grain and schema are defined
- [ ] The **grain** of every output table is documented (e.g. "one row per order line per day"). Mixed-grain tables are resolved.
- [ ] Primary key columns are identified, **unique, and non-null** — verified by a test, not by assumption.
- [ ] Column names, types, and descriptions are documented and stable. Consumer-facing columns have human-readable descriptions.

### 1.2 Transformations are correct
- [ ] Joins have been checked for **fan-out** (accidental row multiplication). Row counts before and after each join are explained.
- [ ] Null handling is explicit at every join and aggregation. `NULL`s do not silently drop rows or skew metrics.
- [ ] Metric and business-logic definitions (e.g. "active customer", "net revenue") are defined in **one place** and reused, not redefined per model.
- [ ] Slowly changing dimensions use the correct type (1 vs 2) per a real consumer question, and point-in-time joins are validated.

### 1.3 Reproducible
- [ ] All transformation code is in **version control**. No production logic lives only in a notebook or console.
- [ ] The pipeline is **reproducible** from versioned code plus a defined input window. Connector and dependency versions are pinned.

---

## Section 2: Reliability and idempotency

### 2.1 Idempotent and replayable
- [ ] Re-running the pipeline for the same window produces the **same result** (no duplicates) — verified, not assumed. Loads use merge/upsert or partition overwrite on a stable key.
- [ ] The pipeline can be **replayed** for any past window after a fix and produce correct output.
- [ ] A **full-refresh / backfill path** exists and has been exercised, and backfills run in bounded idempotent chunks.

### 2.2 Incremental correctness
- [ ] If incremental, the high-watermark is stored durably and advanced **only after** a successful commit.
- [ ] **Late-arriving data** is handled: the watermark column and lookback window are chosen so late records are not missed.

### 2.3 Failure handling
- [ ] Retries with backoff are configured for transient failures, and only on idempotent tasks.
- [ ] Failures are **loud and specific** — no task swallows an exception and exits successfully on incomplete data.
- [ ] Malformed/poison records are **quarantined (dead-lettered)**, not allowed to crash the whole batch or stream.
- [ ] Every external read and write has a **bounded timeout**.

---

## Section 3: Data quality gates

### 3.1 Automated quality checks run in the pipeline
- [ ] **Schema** checks: expected columns/types present; unexpected schema change is caught.
- [ ] **Not-null / uniqueness** checks on keys and required fields.
- [ ] **Referential integrity** checks: foreign keys resolve to dimension rows.
- [ ] **Volume / anomaly** checks: row count within an expected band — a sudden drop or spike fails the run.
- [ ] **Freshness** check: the max event/load timestamp is within the SLA window.
- [ ] **Distribution** checks: categorical values within the known set; numeric ranges plausible.

### 3.2 Gates block bad data
- [ ] For this consumer-facing dataset, the fail behavior is **explicit** (fail closed / quarantine vs fail open / warn) and appropriate to its criticality. Critical datasets fail closed.
- [ ] Quality checks run **as pipeline gates**, not as an after-the-fact report.

---

## Section 4: Freshness, SLAs, and orchestration

### 4.1 Freshness SLA
- [ ] A freshness SLA is defined and documented (e.g. "no more than 2 hours behind source").
- [ ] An alert fires when the freshness SLA is breached, to a named owner — not a shared inbox nobody watches.

### 4.2 Scheduling and dependencies
- [ ] The pipeline is orchestrated as a **DAG** with declared dependencies; downstream tasks wait on real data availability, not a fixed sleep.
- [ ] The schedule matches the **consumer's need** and the source's availability (not run more or less often than required).
- [ ] An **execution-time / runtime anomaly** alert exists (a normally-10-minute job now taking hours is surfaced).

---

## Section 5: Governance, security, and cost

### 5.1 Ownership and discovery
- [ ] The dataset has a **named owner** and is registered in the data catalog with description, grain, freshness, and classification.
- [ ] **Lineage** (table/column level) is available so consumers can trace the data's origin and assess impact of upstream changes.

### 5.2 Classification and PII
- [ ] Columns are **classified** by sensitivity (public/internal/confidential/PII/PCI/PHI).
- [ ] PII is minimized: dropped, masked, or tokenized as early as possible, and access to classified columns is restricted (least privilege).
- [ ] **Deletion / right-to-be-forgotten** is supported: a subject's data can be located and purged across the platform.
- [ ] **Retention** is set per legal/regulatory/cost requirements — not "keep forever by default".

### 5.3 Cost
- [ ] Production models **prune** (partition + column) rather than scanning whole tables; no `SELECT *` in production transforms on large tables.
- [ ] Incremental processing is used where the table is large; full-refresh-every-run is justified or removed.
- [ ] Storage is compressed (columnar), small files are compacted, and cold data is tiered or expired.
- [ ] Platform cost is **attributable** (tagged by dataset/pipeline/team) and the largest consumers are reviewed.

---

## Section 6: Contracts and change management

### 6.1 Data contract
- [ ] A **data contract** (schema, semantics, freshness, allowed changes) exists between this dataset and its consumers.
- [ ] Breaking changes are **versioned and announced**, with a deprecation window — not shipped silently.
- [ ] The contract is enforced in CI: a producer change that violates it fails the producer's build.

### 6.2 Consumer readiness
- [ ] Known downstream consumers are documented and have been notified of the go-live (or the change).
- [ ] Schema evolution is additive/backward-compatible where possible; breaking changes run old and new in parallel during deprecation.

---

## Section 7: Observability and incident readiness

- [ ] **Data observability** monitors the four facets: freshness, volume, schema, and quality/distribution — not just job success/failure.
- [ ] Alerts page on **symptoms consumers feel** (stale or wrong data), not only on a failed task.
- [ ] The pipeline is **resumable** from the last committed step after a mid-run failure.
- [ ] A documented response exists for "bad data shipped": stop the bleed (quarantine), assess blast radius via lineage, backfill the fix through the idempotent path, and add the missing quality check.

---

## Go / No-go decision

**Go:** All items in Sections 1–7 are checked, or each unchecked item has an accepted risk documented with a named owner and a remediation deadline.

**No-go:** Any unchecked item in Section 2 (idempotency/reliability) or Section 3 (quality gates), or unprotected PII in Section 5.2, or more than two unchecked items in any other section without accepted risks and owners.

A no-go is the checklist working as designed. Document the blocking items, assign owners, and schedule the go-live for when the blockers are resolved.
