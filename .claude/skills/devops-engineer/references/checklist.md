# Production-Readiness and Deployment-Readiness Checklist

A structured checklist for evaluating whether a service or a specific deployment is ready for production. Each item has a pass criterion. Any fail item must have a documented remediation before the service goes live or the deployment proceeds.

Use this checklist for: new service go-lives, major feature releases, infrastructure changes, and quarterly production-readiness reviews.

---

## Section 1: CI/CD pipeline gates

### 1.1 Pipeline exists and is the only path to production
- [ ] All deployments to staging and production are triggered by the CI/CD pipeline. No manual `kubectl apply` or console clicks deploy to production.
- [ ] The pipeline is defined as code in the service repository (e.g. `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`).

### 1.2 Required gates are enforced
- [ ] Unit tests run on every commit and the pipeline fails on test failure.
- [ ] Integration tests run before any deployment to staging.
- [ ] SAST scan runs on every commit. High-severity findings block merge.
- [ ] Dependency vulnerability scan (SCA) runs on every build. CVSS ≥ 7.0 findings block the pipeline.
- [ ] Secret detection runs as a pre-commit hook and in CI. Any detected secret blocks the pipeline.
- [ ] Container image scan runs before the image is pushed. No unscanned images are deployed.

### 1.3 Artifact immutability
- [ ] The same artifact (image digest or binary SHA) promoted through staging is deployed to production. The artifact is not rebuilt between environments.
- [ ] Artifacts are tagged with the commit SHA that produced them. Tags like `latest` or `main` are not used as deployment targets.

### 1.4 Deployment automation
- [ ] Production deployment requires an explicit promotion action (manual approval button or automated canary health check). Staging does not auto-promote to production.
- [ ] Deployment duration is within the team's accepted window (e.g. under 10 minutes for a rolling update). Deployments that take longer than expected trigger an investigation.

---

## Section 2: Monitoring and alerting

### 2.1 The four golden signals are instrumented
- [ ] **Latency:** request duration is measured as a histogram. p50, p95, and p99 are visible on a dashboard.
- [ ] **Traffic:** request rate (requests per second) is measured and graphed.
- [ ] **Errors:** error rate (5xx responses / total responses) is measured and graphed.
- [ ] **Saturation:** CPU, memory, and queue depth (as applicable) are measured and graphed.

### 2.2 SLO and SLI are defined
- [ ] At least one SLI is defined as a ratio metric (good events / total events).
- [ ] An SLO target and measurement window are documented (e.g. "99.5% of requests complete in under 300 ms over a 28-day window").
- [ ] An error budget is calculated from the SLO and the team knows the current budget balance.

### 2.3 Alerts are configured and actionable
- [ ] At least one page-worthy alert fires when the SLO burn rate indicates the error budget will be exhausted within one hour.
- [ ] Every alert has a linked runbook or a documented first-response action.
- [ ] Alerts fire to a named on-call rotation, not just a shared inbox.
- [ ] Alert thresholds have been validated: the alert fires on the last three production incidents and does not fire more than twice per week in steady state (alert fatigue check).

### 2.4 Dashboards exist and are useful
- [ ] A service dashboard exists showing the golden signals for the last 24 hours.
- [ ] The dashboard is linked from the service README or runbook.
- [ ] The dashboard has been reviewed by at least one engineer other than the author.

### 2.5 Log aggregation
- [ ] Logs are structured (JSON) with at minimum: timestamp, severity, service name, and trace ID.
- [ ] Logs are shipped to a centralized store. Local-only logs are not accepted.
- [ ] Log retention meets the regulatory or compliance requirement for the service.

### 2.6 Distributed tracing
- [ ] Trace context (trace ID, span ID) is propagated across all service-to-service calls.
- [ ] Trace IDs are included in log lines so logs and traces are joinable.
- [ ] Traces are sampled at a rate that makes tail latency visible in production.

---

## Section 3: Rollback plan

### 3.1 Rollback procedure is documented
- [ ] A written rollback procedure exists for this deployment. It is findable from the deployment runbook.
- [ ] The rollback procedure is tested: it has been executed (in staging at minimum) and the expected outcome is documented.
- [ ] The rollback owner is named: there is a specific engineer who is responsible for executing the rollback during this deployment window.

### 3.2 Rollback is fast and safe
- [ ] The rollback procedure can be completed within the team's accepted MTTR target (e.g. under 30 minutes).
- [ ] If the deployment includes a database migration, the rollback plan explicitly addresses whether the migration is reversible. If it is not reversible, a forward-fix procedure is documented.
- [ ] Automated rollback is triggered by health-check failure where the deployment tooling supports it (e.g. Argo Rollouts, AWS CodeDeploy automatic rollback).

### 3.3 Previous artifact is available
- [ ] The artifact from the previous production deployment is retained and can be redeployed immediately.
- [ ] The previous artifact's configuration values (not secrets) are documented or retrievable from version control.

---

## Section 4: Secrets and configuration

### 4.1 No secrets in source code or images
- [ ] A secret scan (truffleHog, detect-secrets, or equivalent) finds zero secrets in the repository.
- [ ] The container image has been scanned and contains no embedded secrets, credentials, or private keys.
- [ ] No `.env` files containing real credentials are committed to version control.

### 4.2 Secrets are managed centrally
- [ ] All production secrets are stored in the organization's approved secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager, or equivalent). No secrets are stored in CI environment variables as plain text.
- [ ] Each secret has a named owner and a documented rotation schedule.
- [ ] Secret rotation has been tested: the service handles a secret rotation without requiring a restart or causing a user-visible error.

### 4.3 Least privilege
- [ ] The service's runtime identity (IAM role, service account, Vault AppRole) has access only to the secrets and resources it requires. Unused permissions are removed.
- [ ] The CI/CD identity has access only to the environments it deploys to. The staging deploy identity cannot deploy to production.
- [ ] Secret access is audited. Access logs are shipped to the centralized log store.

### 4.4 Configuration is environment-specific
- [ ] Configuration values (non-secret) are separated by environment. The staging config is not used in production.
- [ ] All configuration changes go through a code review. No undocumented configuration differences exist between staging and production.

---

## Section 5: Scaling and reliability

### 5.1 Horizontal scaling is configured
- [ ] The service can scale horizontally. Multiple replicas run in staging without errors.
- [ ] A `HorizontalPodAutoscaler` (or equivalent) is configured with scale-out and scale-in thresholds appropriate for the expected traffic profile.
- [ ] `PodDisruptionBudget` is configured to prevent all replicas from being unavailable simultaneously during node maintenance.

### 5.2 Resource limits are set
- [ ] CPU `requests` and `limits` are set on every container. The `requests` value matches the steady-state consumption observed in staging.
- [ ] Memory `requests` and `limits` are set on every container. The `limits` value is set high enough to accommodate traffic spikes without OOMKilled events.
- [ ] Disk or volume usage is bounded. Unbounded disk growth is treated as a reliability risk.

### 5.3 Health checks are configured
- [ ] `readinessProbe` is configured. The probe checks that the service is actually ready to serve traffic (not just that the process started).
- [ ] `livenessProbe` is configured. The probe detects hung or deadlocked processes.
- [ ] Both probes have been validated: they correctly return failure when the service is unhealthy in staging.

### 5.4 Load and failure testing
- [ ] A load test has been run at the expected peak traffic level. No SLO violations occurred during the load test.
- [ ] At least one failure scenario has been tested: what happens when a downstream dependency is slow or unavailable? The service degrades gracefully (circuit breaker, fallback, timeout) rather than cascading.

### 5.5 Dependencies are accounted for
- [ ] All hard runtime dependencies (databases, caches, message queues, downstream APIs) are documented.
- [ ] The service has a defined behavior for each dependency failure (retry with backoff, fail open, fail closed). The behavior is tested.
- [ ] Timeouts are set on all outbound calls. No outbound call is made without a bounded timeout.

---

## Section 6: Runbook and operational readiness

### 6.1 Runbook exists
- [ ] A runbook exists for the service. It covers: service overview, normal operation, common failure modes, diagnostic commands, remediation steps for each alert, and escalation contacts.
- [ ] The runbook is linked from the alert definitions and the service dashboard.
- [ ] The runbook has been reviewed by at least one engineer other than the author in the last 90 days.

### 6.2 On-call is assigned
- [ ] A named primary on-call engineer is assigned for the deployment window.
- [ ] A named secondary on-call and an escalation path (service owner, incident commander) are documented.
- [ ] The on-call engineer has access to the runbook, dashboard, deployment tooling, and rollback procedure before the deployment begins.

### 6.3 Deployment communication
- [ ] Stakeholders who need to know about the deployment (product, support, downstream service teams) have been notified in advance.
- [ ] A communication template exists for notifying users if the deployment causes a visible incident.
- [ ] A change record has been created if the organization's change management process requires it.

### 6.4 Post-deployment verification
- [ ] A smoke test suite is defined that verifies the critical user journeys work after deployment.
- [ ] The smoke tests run automatically after deployment and block the pipeline if they fail.
- [ ] A manual verification step is defined for any behavior that cannot be covered by automated smoke tests.

---

## Go / No-go decision

**Go:** All items in Sections 1–6 are checked, or each unchecked item has an accepted risk documented with a named owner and a remediation deadline.

**No-go:** Any unchecked item in Section 3 (rollback plan) or Section 4 (secrets), or more than two unchecked items in any other section without accepted risks and owners.

A no-go decision is not a failure. It is the checklist working as designed. Document the blocking items, assign owners, and schedule the deployment for when the blockers are resolved.
