# StartupOS — Using it with Cursor, Claude Code, and Codex

StartupOS is Claude Code-native (same as Praxis), but the three tools play different roles across the StartupOS → Praxis flow. Use each where it is strongest.

## Claude Code — the primary driver

**Best for: large, repo-aware work and running the StartupOS lifecycle.**

- Recommended for creating and evolving the StartupOS structure, docs, commands, templates, and refactors.
- Use it when context across many files is needed — discovery and research touch the whole `memory/startupos/` tree.
- Run the `/startupos:*` commands here. When this repo is the workspace they are discovered automatically; installed as a plugin they are namespaced under the plugin.

```text
/startupos:discover "<domain or observed pain>"
/startupos:research <slug>
...
/startupos:export-praxis <slug>
```

## Cursor — review & manual refinement

**Best for: editing, navigating, and refining the generated docs by hand.**

- After a StartupOS command generates files, open them in Cursor to review, edit, and tighten — especially the business case, financials, and PRD, where human judgment matters most.
- Recommended workflow:
  1. Run a StartupOS command in Claude Code.
  2. Review the generated files (`memory/startupos/`, `docs/startupos/templates/` outputs) in Cursor.
  3. Edit the docs — sharpen assumptions, correct numbers, add sources.
  4. Run the next StartupOS command, or run Praxis once exported.
- Praxis already ships generated Cursor rules under `integrations/cursor/`; StartupOS docs sit alongside them and are read the same way.

## Codex — focused implementation tasks

**Best for: isolated, well-scoped code changes after Claude Code creates the structure.**

- Recommended for tests, scripts, command fixes, validation logic, and CI improvements.
- Use it *after* Claude Code has created the initial StartupOS structure — Codex is the scalpel, Claude Code is the architect.
- Example uses: add a validator for StartupOS template completeness, write a script that checks every memory file carries a `[FACT]/[ASSUMPTION]/[ESTIMATE]` label, fix a malformed command file.

## Recommended division of labor

| Phase | Tool | Why |
| ----- | ---- | --- |
| Create StartupOS structure / docs / commands | **Claude Code** | Repo-wide context |
| Run the lifecycle (`/startupos:*`) | **Claude Code** | Reads/writes across `memory/startupos/` |
| Review & refine generated docs | **Cursor** | Fast editing & navigation, human judgment |
| Tests, scripts, validators, CI, command fixes | **Codex** | Focused, isolated changes |
| Build the product after handoff | **Praxis** (in Claude Code) | `/praxis:new-feature` → release |

## A full round-trip

```text
Claude Code:  /startupos:discover … → /startupos:research … → /startupos:validate …
Cursor:       review & refine memory/startupos/* and the rendered templates
Claude Code:  /startupos:challenge … → /startupos:rank → /startupos:select  (✋)
Claude Code:  /startupos:business-case … → /startupos:prd … → /startupos:architecture … → /startupos:roadmap …
Cursor:       final human polish of the docs/ bundle
Claude Code:  /startupos:export-praxis …  (✋)  → /praxis:idea → /praxis:new-feature
Codex:        write the validators/tests/scripts the build needs
```
