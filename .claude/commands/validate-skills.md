---
description: Validate every skill in the repo — runs the deterministic validator across .claude/skills/ and dist/. Use to check skill structure and frontmatter before committing or shipping a skill.
allowed-tools: Bash(make validate-all), Bash(python .claude/factory/validators/validate_skill.py:*)
---

Run the deterministic skill validator across the whole repo:

```bash
make validate-all
```

This validates every skill under `.claude/skills/` and `dist/` (frontmatter shape, folder shape vs declared tier, eval JSON validity, link hygiene).

Report the result concisely:

- If everything passes, say so and list the skills checked.
- If anything fails, show the failing skill(s) and the exact error lines, then offer to fix them. Do not fix silently — validation failures often point at a real authoring mistake worth seeing.

To validate a single skill instead, run `python .claude/factory/validators/validate_skill.py <path>` (optionally `--tier <N>`).
