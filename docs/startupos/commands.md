# StartupOS — Commands

StartupOS commands follow Praxis command conventions: each is a Claude Code-native command file under [`.claude/commands/startupos/`](../../.claude/commands/startupos/) with `description` + `argument-hint` frontmatter, discovered automatically and invoked as `/startupos:<name>`.

> **Namespacing.** The `startupos/` subdirectory gives the `startupos:` prefix. When this repo is the workspace, the commands appear as `/startupos:discover` etc. Existing flat Praxis commands (`/architect`, `/new-feature`, …) are untouched, and the catalog/integration generators — which only read flat command files — are unaffected.

Every command documents the same seven facets: **purpose · input · output · workflow steps · guardrails · approval gates · expected generated files**.

## The commands

| Command | Lifecycle stage | Purpose |
| ------- | --------------- | ------- |
| [`/startupos:discover`](../../.claude/commands/startupos/discover.md) | Observe → Discover | Find & frame candidate opportunities from signals |
| [`/startupos:research`](../../.claude/commands/startupos/research.md) | Research → Cluster | Market / customer / competitor research → thesis |
| [`/startupos:validate`](../../.claude/commands/startupos/validate.md) | Validate | Design falsifiable validation experiments |
| [`/startupos:challenge`](../../.claude/commands/startupos/challenge.md) | Challenge → Improve | Red-team the idea; expose failure modes; improve |
| [`/startupos:rank`](../../.claude/commands/startupos/rank.md) | Score → Rank | Score & order the candidate shortlist |
| [`/startupos:select`](../../.claude/commands/startupos/select.md) | Select ✋ | Human selects the idea to take forward |
| [`/startupos:business-case`](../../.claude/commands/startupos/business-case.md) | Business Case | Model, pricing, unit economics, GTM |
| [`/startupos:prd`](../../.claude/commands/startupos/prd.md) | Product Requirements | MVP scope, user stories, success metrics |
| [`/startupos:architecture`](../../.claude/commands/startupos/architecture.md) | Architecture | High-level AI-native architecture |
| [`/startupos:roadmap`](../../.claude/commands/startupos/roadmap.md) | Roadmap | Phased path to launch |
| [`/startupos:export-praxis`](../../.claude/commands/startupos/export-praxis.md) | Export to Praxis ✋ | Human-approved handoff to Praxis |

`✋` = command contains a mandatory human-in-the-loop approval gate.

## Command anatomy

Each command file is structured as:

```markdown
---
description: <one-line, used by Claude Code discovery>
argument-hint: <what to pass>
---

Adopt the StartupOS <stage> posture: load the `startupos-<agent>` skill(s) and reason as those agents.

$ARGUMENTS

## Purpose
## Input
## Workflow
## Output / expected generated files
## Guardrails
## Approval gates
## Next
```

Like Praxis's persona commands (`/architect`, `/analyst`, …), each StartupOS command **loads a skill and answers in-persona**: the agent doctrine lives in the [StartupOS agent skills](agents.md) (`.claude/skills/startupos-*`), and the command holds the per-stage *workflow* that orchestrates those agents (much as `/new-feature` orchestrates the SDLC experts). The 12 agent skills are real, validated Tier 2 skills listed in [`SKILLS.md`](../../SKILLS.md).

## Typical sequence

```text
/startupos:discover "<domain or observed pain>"
/startupos:research <slug>
/startupos:validate <slug>
/startupos:challenge <slug>
/startupos:rank
/startupos:select <slug>            # ✋ human gate
/startupos:business-case <slug>
/startupos:prd <slug>
/startupos:architecture <slug>
/startupos:roadmap <slug>
/startupos:export-praxis <slug>      # ✋ human gate → hands off to Praxis
```

After export, you continue in **Praxis**:

```text
/praxis:idea ...
/praxis:new-feature ...
/praxis:analyst ... /praxis:product ... /praxis:architect ...
/praxis:security ... /praxis:ml ... /praxis:review-changes
```

See [praxis-integration.md](praxis-integration.md) for the handoff detail and [templates.md](templates.md) for the files each command generates.
