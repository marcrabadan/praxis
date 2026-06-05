# Examples

Worked examples of the loop. Each shows the gap, the decision, and the route.

## Example 1 — The Terraform/Azure gap (create new → reference)

**Situation.** While running `/devops`, the user asks: "how should I structure
our Terraform for the Azure landing zone?" The expert can describe Terraform and
Azure generically but has no captured *org* convention.

**detect-gap.** The org-specific part — *our* module layout, *our* state backend,
*our* tagging policy — is capturable (Rule 2). Generic HCL/Azure explanation is
not. Search `.claude/skills/`: `devops-engineer` owns IaC, but its
`references/practices.md` has no Azure-landing-zone specifics. → route to
**create-new**.

**create-new.** Granularity (Rule 3): this belongs to an existing role expert and
is not yet large enough for its own skill → a new reference
`devops-engineer/references/azure-landing-zone.md`, linked from that skill's
`## References`. No new top-level skill; no `iac-azure` skill yet.

**Captured content (org-specific only):**
- Module layout: `infra/modules/<service>`, environments in `infra/envs/<env>`.
- State: one Azure Storage backend container per environment; no local state.
- Tagging: every resource carries `cost-center`, `owner`, `env`.
- Naming: `<org>-<env>-<service>` for resource groups.

**Propose.** `ledger.py log --type decision --status pending --title
"Learn: Azure landing-zone convention into devops-engineer"`. Validate the
touched skill. Wait for the user to accept before treating it as canonical.

## Example 2 — Wrong captured answer (refine existing)

**Situation.** A reference says remote state lives in an S3 bucket, but this org
is Azure-only and uses an Azure Storage backend.

**detect-gap.** Coverage exists but is wrong for this org → route to
**refine-existing**.

**refine-existing.** This is a **correction** (capture-iteration). Fix the one
line in `devops-engineer/references/azure-landing-zone.md`, route through the
skill-creator review flow, log a `pending` ledger entry, re-validate. Do not
widen the skill's description.

## Example 3 — Decline (public knowledge, not capturable)

**Situation.** The user asks "what's the difference between a Terraform `count`
and `for_each`?"

**detect-gap.** This is public knowledge the model already produces (Rule 2).
**Decline to capture** — answer the question directly and stop. Nothing is logged
to the ledger. Creating a skill here would only add trigger noise.

## Example 4 — The language-granularity call (per language vs agnostic)

**Question.** "Should we have a skill per programming language, or stay
language-agnostic?"

**Answer (Rule 3).** Keep the role experts (`developer`, `devops-engineer`, …)
language-agnostic — they encode principles, not syntax. Put a language's *org
conventions* in a reference inside the relevant expert (e.g.
`developer/references/python-conventions.md`). Only when one language's reference
is independently invoked across many sessions, with a trigger surface distinct
from the role expert, does it earn promotion to a dedicated `lang-python` skill.
Creating `python-skill`, `go-skill`, `terraform-skill`, … up front is
pre-emptive splitting: the skills share trigger phrases, compete in routing, and
under-trigger. Promote on evidence, never on anticipation.
