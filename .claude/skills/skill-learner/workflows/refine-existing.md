# Refine Existing

Reached from [detect-gap.md](detect-gap.md) when a skill or reference already
covers the topic but gave an answer that was **wrong or incomplete** for this
org. Update it with what was learned — through the skill-creator's review flow,
not by silent edits.

## 1. Locate the exact target

Name the file that needs to change: the expert's `SKILL.md`, or a specific
`references/<topic>.md`. Quote the line(s) that are wrong or the gap that is
missing. If the existing content is correct but the expert simply did not read
it, this is a retrieval miss, not a refinement — stop and point the expert at it.

## 2. Frame the delta as iteration

This is exactly the case the skill-creator's
[capture-iteration workflow](../../skill-creator/workflows/capture-iteration.md)
exists for. Decide which kind of change it is:

- **Correction** ("our remote state is in Azure Storage, not S3") → fix the
  reference and record it as a durable rule for that skill.
- **Addition** ("we also tag every resource with cost-center") → extend the
  reference.
- **Meta-rule** ("from now on every IaC answer must state the state backend") →
  belongs in the skill-creator's `learned-rules.md`, not the expert.

## 3. Hand off to the skill-creator review flow

Route to [../../skill-creator/workflows/review-skill.md](../../skill-creator/workflows/review-skill.md)
(and `capture-iteration.md` for the rule-vs-once decision). Apply the smallest
edit that closes the gap. Keep captured content **org-specific** — do not pad the
reference with generic explanation the model already produces.

Preserve the skill's description and trigger surface unless the refinement
genuinely changes what the skill covers; widening a description to "earn" scope
is an anti-pattern (see the promotion policy).

## 4. Propose via the memory ledger

Log a `pending` entry (see [references/rules.md](../references/rules.md), Rule 1):

```
python .claude/skills/memory/scripts/ledger.py log \
  --type decision --status pending \
  --title "Refine <skill>: <topic>" \
  --body "<what was wrong/missing, the corrected content, why it is org-specific>"
```

Do not present the refined skill as canonical until the user accepts.

## 5. Validate

```
python .claude/skills/skill-creator/scripts/validate_skill.py .claude/skills/<skill>
```

## Stop conditions

- The exact target file and the delta are identified.
- The change is classified (correction / addition / meta-rule) and applied as the
  smallest edit, or deferred to the user.
- A `pending` ledger entry exists.
- The validator passes on the refined skill.
