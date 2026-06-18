# Deploy Report — <Feature title>

> Optional terminal step of `feature-development`, after `release`. Runs only
> when `.praxis/config.json` declares a `deploy` target; otherwise this file
> records the skip and nothing is applied (a cloud target is never assumed).
> Doctrine: [`devops-engineer/references/deploy.md`](../../../../../../.claude/skills/devops-engineer/references/deploy.md).

## Status

One of: `applied` · `plan-only (no execution backend configured)` ·
`skipped (no deploy target configured)`. If skipped, state the one-line reason
and stop here.

## Target

- **Target id / cloud / environment:** e.g. `prod-eks` · `aws` · `production`
- **Cluster / runtime:** EKS / GKE / AKS / generic Kubernetes context
- **Image / SHA:** the exact artifact deployed (same artifact proven in verify)
- **Strategy:** rolling / blue-green / canary
- **MCP server (pinned):** name + version/digest, or `none (plan-only)`

## Terraform plan

Summary of `terraform plan` for the target's `terraformDir`: counts of
add / change / destroy, and any flagged resource (unexpected destroy, IAM or
security-group change). An anomaly here is a stop-and-ask, not an auto-approve.

## Plan guardrails (`deploy-plan-guardrails`)

Deterministic checks over the plan, evaluated before promotion. Record each as
`pass` / `fail` / `skipped (not configured)`:

- **Cost (Infracost):** projected monthly delta vs `guardrails.costBudget`.
- **Policy-as-code (OPA/Conftest):** high-severity violations over plan + manifests.
- **IaC scan (tfsec/Checkov):** unaddressed high-severity findings.

A configured check that fails blocks promotion (fixed or carries a recorded risk
acceptance); on a production target an inconclusive check is fail-closed.

## Supply-chain integrity (`deploy-supply-chain`)

Proven before apply. Record each verdict:

- **SBOM (Syft):** reference/attachment.
- **Signature (cosign):** verified against `supplyChain.cosignIdentity`.
- **Provenance (SLSA):** verified when required.
- **Admission control:** would reject unsigned/unattested images.

An unsigned or unverifiable image blocks the deploy.

## Promotion decision

Who approved, when, and against which criteria. Production apply requires a
**manual human promotion decision** — record it explicitly. `auto` (non-prod)
targets state the green automated checks that authorised the apply.

## SLO & health (`deploy-healthy`)

Post-apply health tied to the target's SLO, not just "probes green": the
error-budget burn over `slo.burnRateWindow` must stay within budget. A failed
check triggers rollback and routes back to `build` for a forward fix.

### DORA metrics

Captured for this deploy:

- **Deployment frequency:** this deploy's contribution.
- **Lead time for change:** commit → production.
- **Change failure:** did this deploy cause a failure? (yes/no)
- **MTTR:** if it failed, time to restore.

## Rollback

The verbatim rollback command/procedure (blue/green switch-back,
`kubectl rollout undo`, or `terraform apply` of the previous pinned artifact),
defined before the apply began.

## Traceability

- This artifact id: `DEP-<NNN>`
- Sources: release notes (`REL-<NNN>`), spec (`SPEC-<NNN>`)
- Closes: `IDEA-<NNN>`
