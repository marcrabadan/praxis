# Technical Manual

Operational reference for the praxis repo and plugin. Add per-command or per-feature runbook sections as features ship.

---

## Operations / Runbook — `/idea` command

**Artifact type:** markdown command file + plugin symlink + catalog regeneration  
**Shipped via:** next plugin/repo release (no separate deployment step)  
**Files changed:**
- `.claude/commands/idea.md` — the command
- `plugin-praxis/commands/idea.md` — relative symlink → `../../.claude/commands/idea.md`
- `SKILLS.md` — regenerated (never hand-edited; produced by `make catalog`)

---

### Pipeline gates (PR → merge)

All gates run in `.github/workflows/validate.yml` on every PR targeting `main`. All must be green before merge. No new gates are required for this artifact.

| Gate | Make target | What it checks | Applies to `/idea`? |
|------|-------------|---------------|---------------------|
| Skill validation | `make validate-all` | Every skill under `.claude/skills/` and `dist/` passes `validate_skill.py` | Not directly (command, not a skill) — but the full sweep runs and must stay green |
| Catalog is up to date | `make catalog-check` | `build_catalog.py --check` — SKILLS.md matches what a fresh `make catalog` would produce | **Yes — primary gate.** After adding `idea.md` + symlink and running `make catalog`, this must report no drift. |
| Integrations are up to date | `make integrations-check` | `build_integrations.py --check` — per-command porting is the symlink only; no integrations manifest entry per command (Assumption A-1 in implementation plan) | **Yes — confirm no drift.** If drift is reported, run `make integrations` and re-commit. |
| Harness validation | `make validate-harness` | `validate_harness.py` — projects, schemas, config integrity | Passes unchanged; command file adds no harness state. |
| Ledger unit tests | `make test` | `test_*.py` under `memory/scripts` and `tools/` | Passes unchanged. |
| JSON schema sanity | (inline CI step) | Five schema files parse as valid JSON | Passes unchanged. |
| Generator smoke test | (inline CI step) | `create_skill.py` produces deterministic output; `command.md` absent from generated skill | Passes unchanged. |

**No new CI check is needed.** The `catalog-check` and `integrations-check` gates together provide the only structural assurance required for a command file.

**Pre-merge static checks** (run locally before opening the PR — these are not automated in CI but are required by spec):

```bash
# Line count must be 31–41
wc -l .claude/commands/idea.md

# Frontmatter must contain "intake and triage", must not contain "plan a feature"
grep "intake and triage" .claude/commands/idea.md
grep -c "plan a feature" .claude/commands/idea.md   # must print 0

# No allowed-tools key
grep -c "allowed-tools" .claude/commands/idea.md    # must print 0

# No Agent/Skill tool invocation in body
grep -c "\bAgent\b\|\bSkill\b" .claude/commands/idea.md   # must print 0

# Static classification table present (all four categories)
grep -E "feature|bug|refinement|not-worth-doing" .claude/commands/idea.md

# Catalog check — must show no drift
make catalog-check

# Integrations check — must show no drift
make integrations-check
```

---

### Rollout and versioning

This command ships when the next plugin release is cut. There is no independent deployment step.

**Version bump decision:**

The addition of `/idea` is a new user-visible command. Under [semver](https://semver.org/) and the Keep a Changelog convention already in use, this is a **minor** addition — no existing behavior is changed or removed. The current plugin version is `1.9.0`.

Warranted action:
1. Bump `plugin-praxis/.claude-plugin/plugin.json` `version` from `1.9.0` → `1.10.0`.
2. Add a `CHANGELOG.md` entry under `[Unreleased]` → `### Added` (or open a new `[1.10.0]` block at release time):

```markdown
### Added

- **`/idea` — idea intake and triage command.** Accepts a raw, ambiguous idea,
  asks at most two clarifying questions, classifies into `feature` / `bug` /
  `refinement` / `not-worth-doing`, captures an unconditional `pending` ledger
  entry, and prints the classification + the exact downstream invocation string.
  The command stops there — it does not plan, spec, or invoke the lifecycle command.
```

The repo-level release tag (`vX.Y.Z`) is cut by the maintainer at release time and marks the whole library state. No action needed before merge.

---

### Rollback

Because the artifact is a file + symlink + catalog regeneration — not a deployed service — rollback is:

1. **Revert the commit** that added `idea.md`, the symlink, and the catalog regeneration. A `git revert <sha>` or re-running `make catalog` after deletion restores the prior catalog state.
2. **Delete the symlink** in `plugin-praxis/commands/` if the revert is partial.
3. **Re-run `make catalog`** to regenerate `SKILLS.md` without the `/idea` row.
4. **Verify:** `make catalog-check && make integrations-check` both pass.

No data migration, no running process to restart, no database to roll back. The ledger entries already written by users via `/idea` are `--type note` entries and remain in the ledger untouched — they do not need to be cleaned up on rollback.

Time to rollback: under five minutes.

---

### Observability

Honest assessment for a static markdown command:

**What is observable:**

- **Memory ledger** — every `/idea` invocation writes a `--type note --source /idea --status pending` entry tagged `intake,<class>`. Querying `python .claude/skills/memory/scripts/ledger.py list --source /idea` or running `/memory list --tags intake` surfaces all captured ideas. This is the primary signal of command adoption and intake volume.
- **`/patterns` output** — `make patterns` (or `/patterns`) mines recurring patterns from the ledger and run logs. `intake`-tagged entries will appear as a cluster once volume exceeds the minimum threshold (default `--min 3`). This is the closest available proxy for "are users using `/idea` and for what?".
- **PR / commit history** — the presence of `idea.md` and its symlink in the repo is auditable via `git log`.

**What is not observable without additional tooling:**

- Per-invocation latency or error rate — the command executes inline in the Claude conversation; no HTTP endpoint, no metrics scrape point.
- Classification accuracy — there is no automated feedback loop between a user's downstream lifecycle outcome and the original `/idea` classification. This is a known gap; it could be addressed in a future `/patterns` enhancement that correlates `intake`-tagged entries with their promoted downstream entries.
- Clarification question count per invocation — not captured in structured form; available only by reading the ledger entry body.

**No SLOs are defined** for this artifact. A static command file has no runtime uptime surface. If the command produces wrong output, the fix is a file edit + PR, not an incident response.

---

### Production-readiness checklist (adapted for a command file)

| Item | Status | Notes |
|------|--------|-------|
| Frontmatter valid (`description`, `argument-hint`, no `allowed-tools`) | Required before merge | Verify with static checks above |
| `description` contains "intake and triage", does not contain "plan a feature" | Required before merge | Spec FR-1, NFR-6 |
| File length 31–41 lines | Required before merge | Spec NFR-1 |
| No `Agent`/`Skill` tool invocation in body | Required before merge | Spec NFR-3 |
| Static four-way classification table present | Required before merge | Spec NFR-4 |
| Ledger call uses `--type note`, `--source /idea` | Required before merge | Spec NFR-5, FR-4 |
| Symlink created in `plugin-praxis/commands/idea.md` | Required before merge | Relative path matching existing entries |
| `make catalog` run; SKILLS.md regenerated | Required before merge | `make catalog-check` must pass in CI |
| `make integrations-check` shows no drift | Required before merge | Assumption A-1 in implementation plan |
| `make validate-all` passes | Required before merge | Full CI sweep stays green |
| `make validate-harness` passes | Required before merge | Harness state unchanged |
| CHANGELOG.md entry added under `[Unreleased]` | Required before release | See versioning section above |
| `plugin-praxis/.claude-plugin/plugin.json` version bumped to `1.10.0` | Required before release | Minor version — new command added |
| Dry-run of all four classification paths verified | Required before merge | Per implementation plan test approach |
| No blocking open questions in spec | Pass | All OQs resolved; OQ-R1 is non-blocking |

**Release blocker:** none identified beyond the checklist items above. The command is self-contained, adds no new dependencies, touches no existing logic, and its CI gates are a strict subset of what already runs on every PR.
