# Implementation plan — /idea intake & triage command

> Authorized once the spec is `accepted` (the `approved-spec` gate). Until then a
> draft proposal. This is a planning run — it does NOT write `idea.md` itself.

## Approach

Add one thin command, `.claude/commands/idea.md`, modelled exactly on
`memory.md` / `learn.md`: frontmatter (`description`, `argument-hint`) → purpose
paragraph → `$ARGUMENTS` placeholder → a `## How to handle it` routing section
with a static 4-row classification table and the exact ledger CLI call. All
reasoning is inline; no `Agent`/`Skill`, no `allowed-tools`. Design rationale is
fixed in [`../decisions/ADR-001-idea-triage-design.md`](../decisions/ADR-001-idea-triage-design.md).

## Components & files to touch

- `.claude/commands/idea.md` — **create.** The command. 31–41 lines (NFR-1).
- `plugin-praxis/commands/idea.md` — **create symlink** → `../../.claude/commands/idea.md`
  (relative, matching every existing entry, e.g. `memory.md -> ../../.claude/commands/memory.md`).
  Verified: all plugin commands are relative symlinks into `.claude/commands/`.
- `SKILLS.md` — **regenerate** via `make catalog` (runs
  `.claude/factory/scripts/build_catalog.py`). The catalog is generated from
  command frontmatter, so the new `/idea` row appears automatically once the file
  and symlink exist. Confirm with `make catalog-check`.
- **No integrations change.** Commands ARE ported via the symlink; there is no
  separate integrations manifest entry per command. Verified: `make integrations`
  is unrelated to per-command porting. (Assumption A-1 below — confirm with
  `make integrations-check` showing no drift after the change.)

## idea.md structure (to build, not now)

Frontmatter:
- `description:` — one line; **must contain** "intake and triage", **must not
  contain** "plan a feature" (FR-1, NFR-6); distinct from lifecycle commands.
- `argument-hint:` — e.g. `<a raw idea, bug, or improvement — in your own words>`.
- No `allowed-tools` (NFR-2).

Body (mirrors `memory.md`):
1. One purpose paragraph: `/idea` is the intake front door — classify, capture,
   recommend, stop. It does not plan, spec, or invoke the downstream command.
2. `$ARGUMENTS` placeholder under a short "The idea:" lead-in.
3. `## How to handle it`:
   - Clarify: if too vague to classify, ask ≤2 `AskUserQuestion` questions inline;
     never a third — classify on what's available and note residual ambiguity.
   - Static classification table (the determinism anchor, NFR-4):

     | Class | Route | Absorb rule |
     |-------|-------|-------------|
     | `feature` | `/new-feature` | new user-observable behavior |
     | `bug` | `/fix-bug` | existing behavior deviates from expected |
     | `refinement` | `/refine` | behavior-preserving; absorbs docs, dep bumps, process |
     | `not-worth-doing` | (none) | insufficient signal or unfavorable cost/value |

   - Capture (unconditional, all four outcomes):
     `python .claude/skills/memory/scripts/ledger.py log --type note
     --title "<clarified summary>" --source /idea --status pending
     --tags "intake,<class>" --body "<raw input + clarification Q&A>"`
   - Output block, then stop — the 4-line recommend-and-confirm shape for routable
     classes; the rationale + capture shape for `not-worth-doing` (no `Next:`).

## Test approach (verifies the AC table)

Static checks on the file (AC-01…AC-06, AC-13, AC-15):
- Line count between 31 and 41 inclusive (`wc -l`).
- Frontmatter has no `allowed-tools` key.
- `description` contains "intake and triage" and not "plan a feature".
- Body contains no `Agent`/`Skill` tool invocation.
- All four categories appear mapped to their routes (static table present).
- The ledger snippet uses `--type note` and `--source /idea`.
- `make catalog-check` and `make integrations-check` show no drift.

Classification → route table (manual dry-run, one per category, AC-07…AC-12, AC-14):

| Dry-run input | Expected class | Expected route | Tags |
|---------------|----------------|----------------|------|
| "add a caching layer to the fetch function" | feature | `/new-feature` | intake,feature |
| "the patterns output truncates at 250 lines" | bug | `/fix-bug` | intake,bug |
| "Update AGENTS.md to mention /patterns" | refinement | `/refine` | intake,refinement |
| "maybe do something with the config" | not-worth-doing | (none, + Rationale) | intake,not-worth-doing |

For each: confirm a `pending` ledger entry is written, `--title` equals the
`Next:` argument (AC-12), and no plan/spec content follows the block (AC-14).
Also dry-run a vague input ("improve the ledger") to confirm ≤2 questions (AC-11).

## Risks & assumptions

- **R-1 (top): description collision with `/new-feature`** (NFR-6). Mitigated by
  the "intake and triage" / not "plan a feature" wording constraint.
- **A-1 (assumption, non-blocking):** per-command porting is the symlink only — no
  integrations manifest edit. Confirm via `make integrations-check` after the
  change; if it reports drift, run `make integrations`. **Flagged for verify.**
- **A-2:** `make catalog` regenerates SKILLS.md purely from frontmatter (no manual
  table edit). Confirm via `make catalog-check`.

## Ordered tasks

High-level ordering; granular checklist in [`../tasks/tasks.md`](../tasks/tasks.md).
1. Author `idea.md`. 2. Verify static AC. 3. Symlink into plugin. 4. Regenerate
catalog. 5. Confirm no integrations drift. 6. Dry-run all four categories + vague.
