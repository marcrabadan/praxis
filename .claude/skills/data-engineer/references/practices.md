# Data Engineering Practices

Core data engineering practices across pipeline design, data modeling, storage, orchestration, streaming, data quality and contracts, governance, DataOps, cost, and data observability. The unifying principle: data must arrive **correct, on time, traceable, and replayable**, at a cost the organization can sustain.

---

## 1. Pipeline design fundamentals

A data pipeline is a contract about data arriving correctly and on time, not just a script that moves rows.

### ETL vs ELT
- **ELT** (extract → load raw → transform in the warehouse) is the default for modern cloud warehouses (Snowflake, BigQuery, Redshift). Land raw data first, transform with SQL/dbt where the compute and lineage live. Raw data preserved on landing is your replay safety net.
- **ETL** (transform before load) earns its place when the target cannot transform efficiently, when PII must be masked or dropped before it ever lands, or when the transformation needs a processing engine the warehouse lacks.
- Keep a **raw / staging / curated** separation regardless of ETL or ELT. Never let consumers read from raw, and never transform in place over the only copy of source data.

### Idempotency and replayability
- Every pipeline run must be **idempotent**: re-running it for the same logical window produces the same result, not duplicates. This is the single most important property of a production pipeline.
- Implement idempotency with `MERGE`/upsert on a stable business key, `INSERT OVERWRITE` of a partition, or delete-and-reinsert scoped to the run window — never blind `INSERT` of everything fetched.
- Design every pipeline so it can be **replayed**: re-run any past window after a bug fix and get correct output. If you cannot replay, you cannot recover from a logic error without manual surgery.

### Incremental vs full loads
- Prefer **incremental** loads keyed on a high-watermark (an `updated_at` timestamp, an autoincrement id, or a CDC log position). Process only new or changed rows; full-refresh only what is small or has changed semantics.
- Store the watermark durably and advance it **only after** the load for that window has committed successfully. A watermark advanced before commit silently drops data on failure.
- Account for **late-arriving data**: pick the watermark column carefully (event time vs ingestion time) and add a lookback window so records that arrive after their event time are not missed.
- Keep a **full-refresh path** available even for incremental models — you will need it after a backfill, a schema change, or a correctness fix.

### Backfills
- A backfill is a controlled replay of history. Run it in **bounded, idempotent chunks** (per day/partition), not one unbounded query that locks tables or runs for hours.
- Backfill into the same idempotent merge logic the incremental path uses, so a backfilled partition and an incrementally-loaded partition are indistinguishable.
- Size backfill chunks to the warehouse's strengths and watch cost — a naive full-history backfill can cost more than a month of normal operation.

### Schema-on-read vs schema-on-write
- Schema-on-write (warehouse tables) gives strong guarantees to consumers; schema-on-read (raw files in a lake) gives flexibility on ingestion. Use schema-on-read at the landing boundary and schema-on-write for curated, consumer-facing data.

---

## 2. Data modeling

The model is the interface consumers depend on. Get the grain right and most other problems shrink.

### Grain first
- Define the **grain** of every table before writing a column: "one row per order line per day" is a grain; "order stuff" is not. Mixed-grain tables are the root cause of double-counted metrics.
- Document the grain in the table description. Every aggregation correctness argument starts from the grain.

### Dimensional modeling (star schema)
- Model analytical data as **facts** (measurements, events, transactions — numeric and additive where possible) surrounded by **dimensions** (the who/what/where/when context).
- Keep fact tables narrow and long; keep dimensions wide and descriptive. Conform dimensions (a single `dim_customer` shared across facts) so metrics join consistently across the business.
- Use **surrogate keys** for dimension joins, but retain the natural/business key for lineage and debugging.

### Slowly changing dimensions (SCD)
- **Type 1** (overwrite) when history does not matter. **Type 2** (new row per change, with `valid_from`/`valid_to`/`is_current`) when consumers need point-in-time correctness — e.g. "what region was this customer in when they ordered?"
- Pick the SCD type per attribute from a real consumer question, not reflexively. Type 2 everywhere inflates storage and join complexity for history nobody queries.

### Normalization vs denormalization
- Normalize in transactional/source-aligned layers to avoid update anomalies; **denormalize in serving layers** to avoid expensive joins at query time. The warehouse is for reading, so optimize the marts for the read pattern.
- **Data Vault** (hubs, links, satellites) suits highly auditable, multi-source enterprise integration where source systems change often. It is heavier than a star schema — adopt it for the auditability/agility it buys, not by default.

### Layered transformation (the dbt pattern)
- Structure transformations in layers: **staging** (one model per source, light renaming and typing, no business logic) → **intermediate** (reusable joins and logic) → **marts** (consumer-facing facts and dimensions). This makes lineage legible and logic reusable.
- Keep business logic in exactly one place. Duplicated definitions of "active customer" across models guarantee two different numbers in two dashboards.

---

## 3. Storage: warehouses, lakes, and lakehouses

### Choosing the store
- **Warehouse** (Snowflake, BigQuery, Redshift): structured, SQL-first, strong consistency, great for curated analytics. Default for the serving layer.
- **Data lake** (object storage + files): cheap, schema-flexible, holds raw and semi-structured data at scale. Default for landing and for data that is too large or too raw for the warehouse.
- **Lakehouse** (Delta Lake, Apache Iceberg, Apache Hudi over object storage): adds ACID transactions, schema evolution, and time travel to lake storage — table semantics on cheap storage. Choose it when you want one copy of data serving both batch and streaming without a separate warehouse load.

### File formats
- Use **columnar formats** (Parquet, ORC) for analytical data — they prune columns and compress far better than CSV/JSON. Reserve row formats (Avro) for streaming/serialization where whole records move together.
- Never serve analytics from CSV or line-delimited JSON at scale; convert to Parquet on landing.

### Partitioning and file sizing
- **Partition** large tables on the column you filter by most (usually a date). Partitioning lets the engine skip data; partitioning on a high-cardinality column you rarely filter on just creates overhead.
- Avoid the **small-files problem**: thousands of tiny files cripple read performance and metadata operations. Compact to target file sizes around 128 MB–1 GB. Avoid the opposite extreme of single giant files that cannot be read in parallel.
- Use **clustering / sort keys / Z-ordering** (warehouse-dependent) to co-locate rows that are queried together, reducing scanned bytes.

### Time travel and retention
- Lakehouse and modern warehouses offer **time travel** — query or restore a table as of a past timestamp. Use it for recovery and reproducibility, and set retention deliberately: longer retention costs storage, shorter retention narrows your recovery window.

---

## 4. Orchestration

Orchestration turns a pile of scripts into a dependable, observable system.

### DAGs and dependencies
- Model the pipeline as a **DAG** (Airflow, Dagster, Prefect) where each task declares its dependencies. A task runs only after its inputs are ready; never chain on a fixed sleep or a guessed time.
- Prefer **data-aware / asset-based** orchestration (Dagster assets, Airflow datasets) so runs trigger on data availability, not just a wall-clock schedule.
- Keep tasks **atomic and single-purpose** so a failure is localized and re-runnable. A 500-line monolithic task that fails at step 9 forces you to re-run steps 1–8.

### Retries, idempotency, and failure
- Configure **retries with backoff** for transient failures (network, rate limits), but only on idempotent tasks — retrying a non-idempotent insert duplicates data.
- Make failure **loud and specific**. A task that swallows an exception and exits 0 produces silently incomplete data, which is worse than a visible failure.
- Use **sensors/timeouts** for external dependencies, with a bounded wait. A sensor that waits forever is an outage in disguise.

### Scheduling, SLAs, and freshness
- Define a **freshness SLA** per dataset ("orders mart is no more than 2 hours behind source") and alert when it is missed. Freshness is the data equivalent of uptime.
- Schedule from the **consumer's** needs and the source's availability, not from habit. Don't run hourly what is consumed once a day; don't run daily what a dashboard needs by 8 am.
- Set **execution-time alerts**: a job that normally takes 10 minutes and now takes 2 hours is a problem even if it eventually succeeds.

---

## 5. Streaming and change data capture

Streaming trades batch's simplicity for low latency. Adopt it when latency requirements — not novelty — demand it.

### When to stream
- Stream when consumers need **seconds-to-minutes** latency (fraud detection, real-time inventory, live dashboards). For hourly or daily needs, batch is simpler, cheaper, and easier to reason about.

### Delivery semantics
- Understand the guarantee you actually have: **at-least-once** (possible duplicates — the common default) vs **exactly-once** (no duplicates, more expensive and constrained). Most "exactly-once" in practice is at-least-once delivery plus **idempotent writes** on the consumer. Design the sink to dedupe on a key.
- **Event time vs processing time**: window and aggregate on event time, and handle **late and out-of-order** events explicitly with watermarks and allowed lateness. Ignoring this produces metrics that quietly drift.

### Change data capture (CDC)
- Use CDC (Debezium, native connectors) to stream inserts/updates/deletes from a source database's log instead of polling — lower load on the source and no missed changes between polls.
- Handle the full change set: **deletes and updates**, not just inserts. A CDC pipeline that only appends inserts produces a table that never reflects deletions.
- Account for **schema changes** in the source: a column added or dropped upstream must not silently break or corrupt the stream.

### Backpressure and ordering
- Plan for **backpressure**: when the sink is slower than the source, the system must buffer or slow down, not drop data or crash. Size topics/partitions and consumer parallelism for peak, not average.
- Preserve **ordering** where it matters by keying records to the same partition (e.g. all events for one account in order). Cross-partition ordering is not guaranteed.

---

## 6. Data quality and contracts

Untested data pipelines ship wrong numbers confidently. Tests are how data earns trust.

### Test the data, not just the code
- Add automated checks for the dimensions that break silently:
  - **Schema**: expected columns and types are present; unexpected columns are caught.
  - **Not-null / uniqueness**: primary keys are unique and non-null; required fields are populated.
  - **Referential integrity**: every foreign key resolves to a dimension row.
  - **Volume / anomaly**: row counts are within an expected band — a load that drops from 1M to 1K rows should fail, not publish.
  - **Freshness**: the max timestamp is within the SLA window.
  - **Distribution**: categorical values stay within the known set; numeric ranges stay plausible.
- Tools: dbt tests, Great Expectations, Soda, or warehouse assertions. Run them **in the pipeline as gates**, not as an afterthought report nobody reads.

### Fail closed on critical data
- For consumer-facing datasets, a failed quality gate should **block publication** (quarantine the bad batch) rather than overwrite good data with bad. Decide per dataset whether to fail open (publish with a warning) or fail closed (hold) — and make it explicit.

### Data contracts
- A **data contract** is an agreement between a producer and consumer about schema, semantics, freshness, and allowed changes. Make breaking changes (dropping/renaming a column, changing a type or meaning) a **versioned, announced** event — not a surprise that breaks every downstream dashboard at once.
- Enforce contracts in CI: a producer's schema change that violates the contract fails the producer's build, surfacing the break before it ships.

### Schema evolution
- Prefer **additive, backward-compatible** changes (add nullable columns). For breaking changes, version the dataset or run old and new in parallel during a deprecation window.

---

## 7. Governance, lineage, and cataloging

### Lineage
- Maintain **column- and table-level lineage** so anyone can answer "where did this number come from?" and "what breaks if I change this source?". dbt, OpenLineage, and modern catalogs derive lineage automatically — use it for impact analysis before changing upstream models.

### Cataloging and discovery
- Register datasets in a **catalog** (DataHub, Amundsen, Unity Catalog, or the warehouse's native catalog) with owner, description, grain, freshness, and classification. An undiscoverable dataset gets re-built by someone who couldn't find it.

### PII and data classification
- **Classify** columns by sensitivity (public, internal, confidential, PII/PCI/PHI). Drive masking, access, and retention from the classification, not ad hoc.
- Minimize and protect PII: drop or tokenize/hash it as early as possible (ideally before it lands in the lake), restrict access to classified columns, and support **deletion / right-to-be-forgotten** by being able to locate and purge a subject's data across the platform.
- Apply **least privilege** on datasets: consumers get the curated marts they need, not blanket access to raw PII.

### Retention
- Set retention per dataset from legal, regulatory, and cost requirements. Indefinite retention "just in case" is a compliance and cost liability.

---

## 8. DataOps — engineering discipline for data

Treat data transformations as software: version-controlled, tested, reviewed, and promoted through environments.

### Version control and CI
- Keep all transformation code (SQL, dbt models, DAG definitions, IaC for the data platform) in **version control**. No production transformation lives only in a notebook or a console.
- Run **CI on data transformations**: compile/parse models, run unit tests on transformation logic, run data tests against a sample or a dev warehouse, and check that models build before merge.

### Environment promotion
- Maintain **dev → staging → prod** environments (separate schemas/databases). Develop and test against dev/staging data; promote the same transformation code to prod. Never hand-edit prod models.
- Make environments structurally identical (same models, different data and credentials), so "works in dev" means something.

### Reproducibility
- A pipeline run should be **reproducible** from versioned code + a defined input window. Pin dependency and connector versions; capture the code version that produced a dataset for auditability.

### Code review for data
- Review transformation PRs for **grain, join fan-out (accidental row multiplication), null handling, and metric definitions** — the bugs that produce plausible-but-wrong numbers. A query that runs is not a query that is correct.

---

## 9. Cost and performance

In the cloud, every query and every byte stored has a price. Cost-awareness is part of correctness.

### Compute cost
- **Prune and partition**: scan only the partitions and columns a query needs. The cheapest byte is the one you never scan. Filter on partition columns; select columns explicitly instead of `SELECT *` in production models.
- **Incremental over full-refresh**: rebuilding a 5-year table every hour is the most common avoidable cost. Process the delta.
- Right-size **warehouse/cluster** compute and use auto-suspend. Idle warehouses left running are pure waste; oversized warehouses for tiny jobs are waste too.
- Watch **join fan-out** and exploding intermediate results — both a correctness bug and a cost bug.

### Storage cost
- Compress (columnar formats), compact small files, and **tier or expire** cold data (lifecycle rules to cheaper storage classes). Keep raw data as long as you need replay, not forever by default.

### Cost visibility
- **Tag and attribute** platform cost by dataset, pipeline, or team. Review the biggest queries and storage consumers regularly; a single unbounded scheduled query can dominate the bill.

---

## 10. Data observability and reliability

### Monitor the data, not just the jobs
- A green job that produced wrong or stale data is still an incident. Monitor the **four facets of data health**: freshness (is it up to date?), volume (right number of rows?), schema (did it change unexpectedly?), and quality/distribution (do the values make sense?).
- Alert on **freshness SLA breaches** and **volume anomalies** the same way services alert on latency and errors. Page on symptoms consumers feel (the dashboard is stale or wrong), not just on a failed task.

### Pipeline reliability
- Make pipelines **resumable**: a failure mid-run should resume from the last committed step, not restart from scratch and re-pay the cost.
- Isolate **poison records**: one malformed row should be quarantined (dead-letter), not crash the whole batch or stream.
- Set **timeouts** on every external read and write. An unbounded call to a slow source hangs the whole DAG.

### Incident response for data
- When bad data ships: **stop the bleed** (pause downstream/quarantine the dataset), assess **blast radius** via lineage (which dashboards/models consumed it), **backfill the fix** through the idempotent path, and **add the missing quality check** so the same class of error fails the gate next time.
- Run **blameless postmortems** for data incidents that reached consumers, with action items that strengthen tests and contracts — the conditions that allowed bad data through are the fix, not the person who merged it.
