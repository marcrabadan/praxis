# Create New

Reached from [detect-gap.md](detect-gap.md) when no captured coverage exists.
Decide *where* the new knowledge lands and *how big* a home it deserves, then
hand the authoring to the skill-creator. Default to the **smallest** home that
fits.

## 1. Choose granularity — reference vs new skill

This is the key decision, and the one the user asked about for programming
languages. Apply the promotion policy: **promote on evidence, never on
anticipation.**

| Situation | Home |
|-----------|------|
| The knowledge belongs to an existing role expert (Terraform/Azure → `devops-engineer`; a dbt convention → `data-engineer`) | A new **reference file** inside that expert: `references/<topic>.md`. This is the default. |
| The knowledge is a cross-cutting body of org doctrine that no single expert owns, and it is already substantial | A new **Tier 2 knowledge skill** |
| There is a repeatable multi-step org procedure (a runbook with modes) | A new **Tier 3 workflow skill** |

Do **not** create a skill-per-language (`terraform-skill`, `python-skill`, …) up
front. Start as a reference inside the role expert. Promote to a dedicated
`lang-*` / `iac-*` skill only when the promotion policy's criteria are met —
demonstrated independent invocation (~5+ sessions), a distinct trigger surface,
a stable interface, and folders that will actually be used. Pre-emptive
splitting causes trigger collisions and under-triggering.

## 2. Classify the tier

If a new skill is warranted, classify it with
[../../skill-creator/workflows/classify-tier.md](../../skill-creator/workflows/classify-tier.md).
Adding a reference to an existing Tier 1 expert may bump it to Tier 2 — that is
fine and expected.

## 3. Write a brief and hand off to the skill-creator

`skill-learner` does not scaffold skills itself. Produce a short brief (purpose,
trigger context, the org knowledge to capture, destination, tier) and route to:

- **New skill** → [../../skill-creator/workflows/create-skill.md](../../skill-creator/workflows/create-skill.md).
- **New reference in an existing skill** → edit/add `references/<topic>.md` in
  that skill and link it from the skill's `## References` and `How to use`
  sections, then run the skill-creator's review flow on the touched skill.

Keep the captured content **org-specific**: the decisions, names, layouts, and
rules that are true for this team. Leave generic explanation to the model.

## 4. Propose via the memory ledger

Log a `pending` entry describing the learning (see
[references/rules.md](../references/rules.md), Rule 1):

```
python .claude/skills/memory/scripts/ledger.py log \
  --type decision --status pending \
  --title "Learn: <topic> convention into <destination>" \
  --body "<what gap, what will be captured, where, tier/granularity rationale>"
```

`pending` is a proposal, not approval. Do not treat the new knowledge as
canonical until the user accepts the entry.

## 5. Validate

Run the validator on any skill you created or touched:

```
python .claude/skills/skill-creator/scripts/validate_skill.py .claude/skills/<skill>
```

## Stop conditions

- Granularity and (if applicable) tier are decided and justified against the
  promotion policy.
- The skill-creator handoff is made, or the reference is drafted and linked.
- A `pending` ledger entry exists.
- The validator passes on every touched skill.
