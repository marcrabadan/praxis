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

## Promotion decision

Who approved, when, and against which criteria. Production apply requires a
**manual human promotion decision** — record it explicitly. `auto` (non-prod)
targets state the green automated checks that authorised the apply.

## Health evidence (`deploy-healthy`)

Post-apply health against the promotion criteria: readiness green, error rate
and latency within budget for the stated window. A failed check triggers
rollback and routes back to `build` for a forward fix.

## Rollback

The verbatim rollback command/procedure (blue/green switch-back,
`kubectl rollout undo`, or `terraform apply` of the previous pinned artifact),
defined before the apply began.

## Traceability

- This artifact id: `DEP-<NNN>`
- Sources: release notes (`REL-<NNN>`), spec (`SPEC-<NNN>`)
- Closes: `IDEA-<NNN>`
