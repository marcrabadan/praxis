# Detect & Route

The entry workflow. Confirm a knowledge gap is real and worth capturing, find
out whether anything already covers it, and decide which way to route. Do **not**
start authoring here — this step only produces a decision.

## 1. Name the gap

State, in one line, what the expert was asked and what it could not answer from
captured knowledge. Example: "devops-engineer was asked how *this org* lays out
Terraform modules and remote state for Azure; no convention is captured."

## 2. Apply the capturability test (Rule 2)

A gap is worth capturing only if the knowledge is **org-specific** — conventions,
runbooks, decisions, preferences. If the missing piece is public knowledge the
model already produces (plain Terraform/HCL syntax, what an Azure resource group
is), **decline**: answer the question normally and stop. Say why you declined.

If the user is *supplying* the org knowledge ("here's how we do it: …"), it is
capturable even if the surrounding topic is public.

## 3. Search existing coverage

Before proposing anything new, look for a home that already exists. Search:

- `.claude/skills/*/SKILL.md` descriptions for the topic (the role expert — e.g.
  `devops-engineer` — usually owns it).
- That expert's `references/` for a near-miss file to extend.
- Other skills whose trigger surface overlaps, to avoid creating a collision.

Use `grep`/`Glob` over `.claude/skills/`. Record what you found.

## 4. Decide the route

| Finding | Route |
|---------|-------|
| A skill/reference covers this but is **wrong or incomplete** | [refine-existing.md](refine-existing.md) |
| **No** captured coverage exists | [create-new.md](create-new.md) |
| Coverage is correct and complete already | No action — the gap was a retrieval miss, not a knowledge gap. Point the expert at the existing reference. |

## 5. Hand off

Carry into the chosen workflow: the gap statement, the capturability verdict,
the search results, and the target destination you have in mind. The next
workflow refines that into a concrete proposal and a skill-creator handoff.

## Stop conditions

- The gap is stated and classified capturable / declined / already-covered.
- A route is chosen with a candidate destination, or the gap is closed with a
  reason.
