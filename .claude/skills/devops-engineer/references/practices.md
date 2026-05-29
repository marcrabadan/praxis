# DevOps Practices

Core DevOps engineering practices across CI/CD pipeline design, infrastructure as code, containerization, deployment strategies, observability, configuration and secrets management, reliability, DORA metrics, DevSecOps, and cost awareness.

---

## 1. CI/CD pipeline design

A pipeline is a contract between engineering and production: every commit must prove fitness before it ships.

### Stage ordering and fast feedback
- Order stages by increasing cost and decreasing speed: lint → unit tests → build → integration tests → security scans → deploy to staging → smoke tests → deploy to production.
- The first stage to fail must stop the pipeline immediately. Never continue past a broken gate.
- Surface failures within five minutes for the inner loop (lint, unit tests). Engineers who wait longer will push again without fixing the root cause.
- Parallelize independent stages (e.g. frontend and backend unit tests) rather than running them sequentially.

### Build stage
- Produce a single artifact (container image, JAR, ZIP) that is tagged with a commit SHA and never rebuilt for later stages. Same artifact, different environment.
- Cache dependency layers aggressively (npm/pip/maven caches keyed by lock-file hash). A warm cache build should be under two minutes.
- Fail the build if any dependency lock file is missing or out of date. Lock files are not optional.

### Test stages
- Unit tests: run in-process, no external services, sub-60-second target. Any test that requires a network call is an integration test, not a unit test.
- Integration tests: use containerized dependencies (Docker Compose or Testcontainers). Do not test against shared environments.
- End-to-end tests: run against a deployed staging environment. Scope to critical user journeys only; keep the suite under 15 minutes.
- Enforce a minimum coverage threshold as a hard gate only when the team agrees on a meaningful target. A fixed percentage enforced without context creates coverage theater.

### Security scan stage
- Static analysis (SAST) on every commit. Treat high-severity findings as pipeline blockers, not warnings.
- Dependency vulnerability scanning (SCA) on every build. Block on CVSS ≥ 7.0 by default; tune the threshold after the first triage pass.
- Container image scanning before any image is pushed to a registry. Never push an unscanned image.
- Secret detection (e.g. truffleHog, detect-secrets) as a pre-commit hook and again in CI. Rotate any secret found; do not suppress the finding.

### Deploy stages
- Deploy to a staging environment before production. Staging must be structurally identical to production (same IaC modules, same secret management path, different config values).
- Gate production deployment on manual approval or automatic canary health checks. Never deploy to production without an explicit promotion decision.
- Deploy atomically: the deployment either fully succeeds or fully rolls back. Partial deploys cause inconsistent state.

---

## 2. Infrastructure as code (IaC)

IaC means the running state of infrastructure is derived from version-controlled definitions. Manual changes in the console are bugs.

### Declarative over imperative
- Write what the infrastructure should be, not what commands to run. Terraform HCL, CloudFormation YAML, and Kubernetes manifests are declarative. Shell scripts that call `aws ec2 create-instance` are imperative and break idempotency.
- Every resource that exists in production must exist in the IaC repository. If it cannot be expressed in IaC, document why and create a tracking issue.

### Immutability
- Never patch a running server in place. Replace the entire instance or container with a newly built artifact.
- Immutable infrastructure eliminates configuration drift and makes rollback a matter of redeploying the previous artifact.
- Use AMIs, container images, or machine images as the unit of immutability, not user-data scripts that run on boot.

### Idempotency
- Running `terraform apply` (or equivalent) twice with no changes must produce no changes. Fail if it does not.
- Use resource lifecycle policies (`create_before_destroy`, `prevent_destroy`) explicitly. Do not rely on defaults.
- Test idempotency in the CI pipeline by applying the same configuration twice in sequence.

### Module and state hygiene
- Organize IaC into modules with a single responsibility: network, compute, database, monitoring. Do not create a single root module that manages everything.
- Store Terraform state in a remote backend with state locking (S3 + DynamoDB, GCS, or Terraform Cloud). Never commit state files to version control.
- Separate state per environment (dev, staging, prod) and per team boundary. A staging apply must never touch production state.
- Pin provider and module versions. Unpinned versions break reproducibility.

### Drift detection
- Run `terraform plan` in CI on a schedule (e.g. nightly) against live infrastructure. Alert if the plan shows unexpected drift. Drift is either an unreviewed manual change or a bug.

---

## 3. Containerization and orchestration

Containers standardize the runtime environment across development, staging, and production.

### Dockerfile hygiene
- Use multi-stage builds to separate build dependencies from the runtime image. The final image should contain only what the process needs at runtime.
- Pin base image versions to a digest, not a mutable tag like `latest`. `ubuntu:22.04@sha256:...` is reproducible; `ubuntu:latest` is not.
- Run as a non-root user. Add `USER nonroot` or create a dedicated application user in the Dockerfile.
- Minimize layer count and size. Combine `RUN` instructions that install and clean up packages in the same layer.
- Scan the final image for vulnerabilities before pushing (Trivy, Grype, Snyk).

### Kubernetes basics
- Set CPU and memory `requests` and `limits` on every container. Omitting `requests` prevents the scheduler from making sound placement decisions; omitting `limits` allows a single container to starve the node.
- Define `readinessProbe` and `livenessProbe` for every container. Readiness controls traffic routing; liveness triggers automatic restarts.
- Use `Deployment` for stateless workloads and `StatefulSet` for stateful workloads. Never use bare `Pod` objects in production.
- Store configuration in `ConfigMap` and secrets in `Secret` (or an external secrets operator). Do not embed configuration values in container images.
- Use `PodDisruptionBudget` for any service with an availability SLO. It prevents maintenance operations from taking the service down entirely.
- Apply `NetworkPolicy` to enforce least-privilege east-west traffic. Default-deny inbound, allow only documented paths.

---

## 4. Deployment strategies

The choice of strategy determines the blast radius of a bad deploy and the speed at which risk is retired.

### Rolling update
- Replace instances one at a time (or in small batches) with the new version while the rest continue serving traffic.
- Suitable for stateless services where both versions can coexist and the API is backward-compatible.
- Set `maxSurge` and `maxUnavailable` explicitly in the Kubernetes `Deployment` spec. The defaults are not tuned for any particular service.

### Blue/green
- Maintain two identical environments (blue = current, green = new). Route all traffic to blue; deploy to green; validate green; switch the load balancer to green in one atomic step.
- Rollback is instant: switch the load balancer back to blue.
- Cost: requires running two full environments simultaneously during the switch window.
- Suitable for high-traffic services where even a brief period of mixed versions is unacceptable.

### Canary
- Route a small percentage of traffic (e.g. 1–5%) to the new version. Expand the percentage in increments based on error rate, latency, and business metrics.
- Define explicit promotion criteria before the deploy starts: "error rate below 0.1% and p99 latency below 300 ms for 30 minutes at 10% traffic."
- Define explicit rollback triggers before the deploy starts: "error rate exceeds 1% at any canary percentage."
- Use a traffic management layer (Istio, Argo Rollouts, AWS CodeDeploy) to split traffic precisely. Do not rely on DNS-based splitting.

### Feature flags
- Deploy code continuously; control activation with a runtime flag. Feature flags decouple deployment from release.
- Limit flag lifetime. A flag that is always on is dead code. Remove flags within one sprint of full rollout.
- Never use feature flags as a substitute for a rollback plan. Flags reduce blast radius; they do not replace safe deployment practices.

### Rollback
- Every deployment must have a defined rollback procedure documented before the deploy begins.
- Prefer forward rollbacks (deploy a fix) for database migration scenarios where the old schema cannot be applied after data has been written in the new schema.
- Automate rollback triggers from health-check failures. A rollback initiated by an alert at 3 am is faster than one initiated by a pager.

---

## 5. Observability

Observability is the ability to ask new questions about a system's behavior from its outputs without changing its code.

### The three pillars

**Logs**
- Emit structured logs (JSON) with a consistent schema: timestamp, severity, service name, trace ID, span ID, and a machine-readable `event` field.
- Log at boundaries: service entry/exit, external calls, and decision points. Do not log in tight loops.
- Severity levels: DEBUG (development only), INFO (normal operation), WARN (unexpected but handled), ERROR (unexpected, requires attention), FATAL (unrecoverable, service stopping).
- Ship logs to a centralized store (Elasticsearch, CloudWatch, Loki). Local-only logs do not survive instance termination.

**Metrics**
- Instrument the four golden signals: latency, traffic, errors, and saturation. These four cover the majority of production issues.
- Use histograms for latency and size distributions; counters for request counts; gauges for saturation metrics. Do not use averages for latency — use percentiles (p50, p95, p99).
- Label metrics by service, environment, and the dimensions needed to answer the most common operational questions. Do not add high-cardinality labels (e.g. user ID, request ID) to metrics.
- Push metrics to a time-series store (Prometheus, Datadog, CloudWatch Metrics) with a scrape or push interval no coarser than 15 seconds for production services.

**Traces**
- Instrument every service entry point and every outbound call with a span. Propagate the trace context (W3C Trace Context or B3) across service boundaries.
- Attach the trace ID to log entries so logs and traces are joinable.
- Sample at a rate that makes tail latency visible. 100% sampling is too expensive for high-traffic services; 0.1% misses rare errors. Use head-based sampling with a tail-based override for errors.

### SLOs, SLIs, and error budgets
- Define SLIs as ratio metrics: the fraction of events that are "good" out of all valid events. Example: "fraction of HTTP requests completing in under 300 ms with a 2xx status code."
- Set SLOs as a target percentage over a rolling window: "99.5% of requests meet the SLI over a 28-day window."
- The error budget is `1 − SLO_target`. A team with a 99.5% SLO has 0.5% of requests as budget for failures, experiments, and deploys.
- Stop risky deployments when the error budget is exhausted. Resume when the budget is replenished.
- Review SLOs quarterly. An SLO that is never breached may be too loose; one that is always breached is a target, not a contract.

### Alerting
- Alert on symptoms (the user experience is degraded), not causes (CPU is high). A high CPU that does not affect latency or errors is not an incident.
- Every alert must have a documented response action. An alert that a human cannot act on is noise. Delete it.
- Use multi-window, multi-burn-rate alerting for SLO-based alerts (e.g. Google SRE Workbook burn-rate rules). A 14.4x burn rate on a 1-hour window catches fast burns; a 1x burn rate on a 3-day window catches slow burns.
- Distinguish between pages (require immediate human action, wake someone up) and tickets (require action within business hours).

---

## 6. Configuration and secrets management

### Configuration promotion
- Use environment variables or external configuration (e.g. AWS SSM Parameter Store, HashiCorp Consul) to separate config from code.
- Promote configuration through environments (dev → staging → prod) using the same keys with environment-specific values. Never copy-paste config between environments.
- Keep configuration under version control as IaC or in a config management system. Undocumented configuration changes cause incidents.

### Secrets management
- Never store secrets in source code, environment files committed to version control, or container images.
- Use a secrets manager (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) as the single source of truth for credentials, API keys, and certificates.
- Apply least privilege: each service has its own identity and can read only the secrets it needs, nothing else.
- Rotate secrets on a schedule and immediately after any exposure event. Automate rotation where the secrets manager supports it.
- Audit secret access. Every read of a production secret should be logged and anomalous access should alert.

---

## 7. Reliability and incident response

### On-call and escalation
- Every service with a production SLO must have a named on-call owner. "The whole team is on-call" means no one is on-call.
- Rotate on-call weekly or bi-weekly. No single engineer should carry the pager indefinitely.
- Define escalation paths: primary on-call → secondary → service owner → incident commander. Document and test the escalation path before an incident.

### Runbooks
- Write a runbook for every page-worthy alert. The runbook must be findable from the alert (link in the alert body or dashboard annotation).
- A runbook must answer: what is the symptom, what is the likely cause, what are the diagnostic steps (with exact commands), and what are the remediation options.
- Test runbooks regularly. An untested runbook fails at 3 am.
- Keep runbooks in version control alongside the service they describe. Runbooks that live in a separate wiki become stale.

### Blameless postmortems
- Conduct a postmortem for every SEV1/SEV2 incident and any incident that exhausted the error budget.
- A postmortem is blameless: the goal is to understand system failure, not to assign personal fault. Systems fail because conditions allowed them to; fix the conditions.
- Postmortem structure: incident summary, timeline, contributing factors (using the five-whys or similar), action items with owners and due dates, and a lessons-learned section.
- Publish postmortems internally. Sharing failure analysis builds organizational resilience.

### MTTR reduction
- Mean time to recovery measures how long a degraded service takes to return to normal. Reduce it by: shortening detection time (better alerting), shortening diagnosis time (better observability), shortening remediation time (automated rollback, runbooks, on-call practice).
- Run game days: simulate failure scenarios to test detection, escalation, and recovery procedures before real incidents reveal gaps.

---

## 8. DORA metrics

DORA metrics measure software delivery performance. Use them to identify bottlenecks, not to rank engineers.

| Metric | Definition | Elite benchmark |
|--------|-----------|-----------------|
| **Deployment frequency** | How often the team deploys to production | Multiple times per day |
| **Lead time for changes** | Time from code commit to running in production | Less than one hour |
| **Change failure rate** | Percentage of deployments causing a production incident | Less than 5% |
| **MTTR** | Time to restore service after a production incident | Less than one hour |

### Improving each metric
- **Deployment frequency:** reduce batch size, automate the deploy pipeline, reduce manual approval steps. A deployment that takes 30 minutes of human coordination will not happen multiple times a day.
- **Lead time:** identify and eliminate the slowest pipeline stage. Common bottlenecks: slow integration tests, manual review queues, long staging bake times.
- **Change failure rate:** invest in automated testing coverage of the failure modes that recur in incidents. Improve feature flag coverage to reduce blast radius.
- **MTTR:** improve alerting fidelity, observability depth, runbook quality, and automated rollback triggers.

---

## 9. DevSecOps and supply-chain security

### Shift security left
- Run SAST, SCA, and secret detection in every pull request. Developers fix security findings in the same sprint they write the code. Findings that age become technical debt.
- Treat the security scan stage as a first-class pipeline gate, not an optional report. Merge is blocked on unresolved high-severity findings.

### Supply-chain security
- Pin all dependencies to exact versions and commit lock files. An unpinned dependency is an unaudited code change waiting to happen.
- Verify the provenance of build artifacts using SLSA (Supply-chain Levels for Software Artifacts). Aim for SLSA level 2 (scripted, version-controlled build) as a minimum, level 3 (hardened build environment) for critical services.
- Sign container images and verify signatures before deployment (Cosign, Notary). Unsigned images should be rejected by admission control.
- Audit the third-party packages in your dependency graph for known vulnerabilities weekly. Do not wait for a CI run to surface a new CVE.

### Least privilege in the pipeline
- CI/CD credentials should have the minimum permissions required to deploy. A deploy job does not need read access to all secrets or write access to all S3 buckets.
- Use short-lived credentials (OIDC tokens, AWS IAM roles with STS assumption) rather than long-lived API keys stored in CI secrets.
- Separate deploy credentials by environment. The staging deploy role must not have permission to deploy to production.

---

## 10. Cost and capacity awareness

### Cost visibility
- Tag all cloud resources with at minimum: service name, environment, and team. Without tags, cost allocation is impossible.
- Review cloud cost reports weekly. An unreviewed bill for three months is a surprise; a weekly review is an optimization opportunity.
- Set budget alerts at 80% and 100% of expected monthly spend per service. Alerts should notify the service owner, not just the finance team.

### Capacity planning
- Define capacity requirements from SLOs: if the SLO is 99.9% availability, the infrastructure must handle the expected peak traffic with headroom.
- Use horizontal autoscaling for stateless services. Define scale-out triggers based on CPU, memory, or queue depth at the percentile level, not averages.
- Run load tests before capacity-changing events (product launches, marketing campaigns). A load test that finds a bottleneck the week before launch is a success; finding it the day of is not.
- Right-size instances regularly. Over-provisioned instances are waste; under-provisioned instances are risk. Review sizing quarterly using actual utilization data.
