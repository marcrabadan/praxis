# Review-Skill Workflow

Read an existing skill and propose targeted improvements. Run when the user asks to review, audit, or improve a skill.

## Inputs

- Path to the skill folder (factory-owned or produced).
- Optionally the original `skill-brief.md` if it exists.

## Steps

### 1. Read the skill

Read `SKILL.md` end-to-end and every file in `references/`, `workflows/`, `scripts/`, `evals/`, and `agents/` if present.

### 2. Identify the current tier

Use the heuristic in [classify-tier.md](classify-tier.md) to infer the tier from the folder shape and `tier:` frontmatter (if present).

### 3. Check the tier fit

Ask:

- Is the current tier appropriate given what the skill actually does?
- Does the folder contain mostly-empty directories (suggesting downgrade)?
- Are there long sections in `SKILL.md` that should move to `references/` (suggesting upgrade from Tier 1 to Tier 2)?

Recommend a tier change if warranted, with reasoning.

### 4. Review the description

Apply the checklist from [../references/description-writing.md](../references/description-writing.md):

- Third person?
- Concrete verbs?
- "Use when" + realistic trigger phrases?
- Under 1024 characters?
- One consistent term per concept?
- No "helps with", "deals with", "assists" without specifics?

Propose a rewrite if the description fails any check.

### 5. Review the body

Look for:

- `SKILL.md` over 500 lines → split material into `references/`.
- Long prose that should be a numbered procedure → move to `workflows/`.
- Deterministic checks described in prose that should be scripts → propose a script.
- Hard-coded paths, time-sensitive instructions, ALL-CAPS shouting without explanation → flag per [../references/anti-patterns.md](../references/anti-patterns.md).

### 6. Review evals

If `evals/` exists:

- Are positive **and** negative trigger cases present?
- Are negative cases near-misses (not obviously irrelevant)?
- Do output evals have realistic prompts and verifiable assertions?
- Does `python .claude/factory/validators/validate_skill.py <path>` pass?

If evals are missing for a Tier 4 or 5 skill, recommend adding them.

### 7. Review scripts

For each script in `scripts/`:

- Does it accept inputs via argparse?
- Does it exit 0 / non-zero appropriately?
- Is it documented in `SKILL.md`?
- Does it do something deterministic, or does it punt back to the agent?

Flag scripts that look like placeholders.

### 8. Identify duplicates and outdated material

- Same rule restated in multiple files → consolidate.
- References to deprecated tools, APIs, or paths → update or move to a "deprecated" collapsible.

### 9. Produce the review report

Output as markdown:

```markdown
# Review of <skill-name>

## Tier
- Current: <N>
- Recommended: <N> (reason)

## Description
- Current: "<text>"
- Issues: <list>
- Proposed: "<rewrite>"

## SKILL.md body
- Length: <N> lines (limit 500)
- Issues: <list>
- Recommended moves:
  - Move section X to references/Y.md
  - Move section Z to workflows/W.md

## References
- <observations>

## Workflows
- <observations>

## Scripts
- <observations>

## Evals
- Trigger evals: <present? positive + negative? near-misses?>
- Output evals: <present? realistic? verifiable?>

## Anti-patterns flagged
- <list with file:line>

## Recommended migration plan
1. <ordered, concrete steps>
2. ...

## Validation
- validate_skill.py: <ok/fail with details>
```

### 10. Apply changes only if requested

The review workflow **proposes**. It does not edit the skill unless the user explicitly asks.

If the user asks to apply, switch to [create-skill.md](create-skill.md) and execute the migration plan step by step, validating after each change.

### 11. Watch for iteration on the review itself

If the user pushes back on a finding in the review report ("no, that section should stay where it is", "drop recommendation #3 — that's not actually a problem"), do not silently re-edit the report. Switch to [capture-iteration.md](capture-iteration.md) and ask whether the pushback is:

- a correction to this specific review (one-off);
- a rule the skill being reviewed should carry going forward (e.g. "this skill is allowed to have a long SKILL.md because the body is examples-heavy");
- a meta-rule for the skill-creator (e.g. "from now on, don't flag long bodies for skills tagged examples-heavy").

This protects the user's intent from being silently lost in a rapid back-and-forth.

## Stop conditions

The review is done when:

- every section of the report has been filled (or explicitly marked "n/a");
- the validation result is included;
- the migration plan is concrete and ordered.
