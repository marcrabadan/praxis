# Create-Skill Workflow

Generate the scaffold and author the skill body. Run after [interview-intake.md](interview-intake.md) and [classify-tier.md](classify-tier.md).

## Inputs

- `skill-brief.md` with answers Q1–Q9 and a confirmed `tier`.
- Target output directory (default `dist/<slug>/`).

## Steps

### 1. Pick the output path

Default to `dist/<slug>/` from the repo root. The user can override with an explicit path during the interview.

If the target directory already exists and is non-empty, ask the user whether to overwrite. The generator script refuses overwrite without `--force`.

### 2. Run the generator

From the repo root:

```bash
python .claude/skills/skill-creator/scripts/create_skill.py \
  --brief dist/<slug>/skill-brief.md \
  --tier <N> \
  --name <slug> \
  --out dist/<slug>
```

The generator:

- copies `templates/tier-N-*/` into the output directory;
- substitutes `{{NAME}}`, `{{TITLE}}`, `{{DESCRIPTION}}`, `{{PURPOSE}}`, `{{TIER}}` placeholders;
- preserves the existing `skill-brief.md`.

A Claude Code skill needs no `command.md`: Claude Code discovers the skill from its `SKILL.md` frontmatter and exposes it via the Skill tool / `/<name>` automatically. The generator emits only `SKILL.md` (plus tier folders) and never a command file.

If the brief does not yet contain a finalized `description`, the generator inserts a placeholder and writes a `TODO` in `SKILL.md`. You will replace it in step 4.

Exit non-zero on failure with a clear message.

### 3. Read the scaffold

Read every file the generator produced. Confirm the folder shape matches the tier (see [../references/skill-anatomy.md](../references/skill-anatomy.md)).

### 4. Author the description

Replace the placeholder description with a final one per [../references/description-writing.md](../references/description-writing.md). The final description must:

- be third-person;
- include WHAT (concrete verbs) + WHEN (realistic trigger phrases);
- stay under 1024 characters;
- pass `validators/validate_frontmatter.py`.

### 5. Fill the body

For each section in the template:

1. Replace placeholders with content derived from the brief.
2. Move long knowledge into `references/<file>.md` rather than inlining in `SKILL.md`.
3. Move multi-step procedures into `workflows/<file>.md`.
4. Keep `SKILL.md` under 500 lines.

For Tier 4 and Tier 5 skills:

- Implement any scripts the brief implies (e.g. `scripts/generate.py`, `scripts/validate.py`). Follow [`ai/implementation-principles.md`](../../../factory/ai/implementation-principles.md).
- Author at least one positive and one negative case in `evals/trigger-evals.json` per [../references/description-writing.md](../references/description-writing.md).

### 6. Validate

Run:

```bash
python .claude/factory/validators/validate_skill.py <output-path>
```

If validation fails:

- read the error;
- fix the issue;
- re-run.

Do not declare done until validation exits 0.

### 7. Hand off

After successful validation, hand off as the user requests:

- to [review-skill.md](review-skill.md) for a structured review;
- to [evaluate-skill.md](evaluate-skill.md) to add or expand evals;
- promote the finished folder to `.claude/skills/<slug>/` when it is a shared asset;
- or stop here if the user only wanted a scaffold.

### 8. Watch for iteration

If the user's next message is corrective ("fix the description", "actually no, the rules should..."), switch to [capture-iteration.md](capture-iteration.md) **before** silently applying the change. The user may want the correction registered as a durable rule for the skill or as a meta-rule for the skill-creator. Asking first is part of the contract.

## Stop conditions

The workflow is complete when:

- the output folder exists and contains a non-empty `SKILL.md`;
- the description is final (no placeholder remains);
- `validators/validate_skill.py` exits 0 on the output folder;
- the `skill-brief.md` has been updated with the final tier, name, and any assumptions made during authoring.

## Required summary

Return to the user:

```
Created: dist/<slug>/
Tier: <N>
Files written:
- <list>
Assumptions:
- <list, or "none">
Validation: validate_skill.py returned OK
Next steps:
- <optional review / evaluate / package>
```
