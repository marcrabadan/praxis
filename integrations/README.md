# Wiring praxis into your dev flow

The praxis SDLC experts are most useful when they reach the code **at the moment a mistake is
made** — not only when someone remembers to ask. This is the gap these integrations close:
they move the experts from *pull* (you invoke them) to *push* (they show up automatically),
so juniors catch bad practices they didn't know to look for, seniors get a low-friction
second pair of eyes, and architects see the team's standards enforced consistently.

Everything here is **opt-in and portable** — copy it into a consuming repository. `praxis`
itself ships these as templates and does not enable them on its own CI.

## The reviewer: `/review-changes`

The behaviour everything below triggers. It reads the current diff, routes to only the
relevant experts (developer / qa / architect / devops / security / security-architect), and returns **severity-tagged,
didactic** findings — each one says *what* the bad practice is, *why* it matters, and *how*
to fix it. Run it by hand any time:

```text
/review-changes                      # review the working diff vs the base branch
/praxis:review-changes               # same, when installed as a plugin
```

## 1. Automatic review on every PR (CI)

Catches everyone's code at PR time and posts teaching-oriented comments — the highest-leverage
option for a whole team.

1. Copy [`github-actions/praxis-pr-review.yml`](github-actions/praxis-pr-review.yml) into your
   repo at `.github/workflows/praxis-pr-review.yml`.
2. Add an `ANTHROPIC_API_KEY` repository secret.
3. Open a PR — the review posts itself.

## 2. Local nudge before you push (hooks)

A pre-commit / end-of-session reminder to run `/review-changes` before the code leaves your
machine. A nudge, never a gate.

Copy the `hooks` block from [`hooks/settings.example.json`](hooks/settings.example.json) into
your repo's `.claude/settings.json` (merge it if the file already exists).

## 3. Automatic memory ledger (hooks)

Make the [`memory`](../.claude/skills/memory/) skill capture work automatically. The ledger
records plans, decisions, implementations, and artifacts under `.praxis/memory/` (committed
to git), each with a `pending → accepted | rejected | rolled-back` lifecycle, so the record
survives across sessions and changes can be rolled back.

1. Ensure the `memory` skill is present in your repo — install the `praxis` plugin, or
   `make export SKILL=memory TO=<your-repo>`.
2. Copy the `hooks` block from
   [`hooks/memory.settings.example.json`](hooks/memory.settings.example.json) into your
   repo's `.claude/settings.json` (merge if it already has hooks).

It wires two harness-enforced behaviors: **SessionStart** surfaces still-pending entries into
context, and **Stop** snapshots uncommitted changes as a rollback-able entry. Combine with the
doctrine in `AGENTS.md` (which records the *why* of decisions) for full coverage. Manage the
ledger any time with `/memory` (`list`, `accept`, `reject`, `rollback`).

## 4. Ambient validation: assumptions & loops (hooks)

Make the *never assume, always validate* and *loop control* rules ambient instead
of opt-in-per-invocation. Copy the `hooks` block from
[`hooks/validation.settings.example.json`](hooks/validation.settings.example.json)
into your repo's `.praxis`-adjacent `.claude/settings.json` (merge if it already
has hooks). It resolves the harness `tools/` dir from your `.praxis/config.json`
(`harnessRoot`), so no per-repo copy of the tools is needed.

It wires two nudges (never blocks): **SessionStart** surfaces open assumptions
(`assumptions.py open --brief`) and any escalated/running loops (`loop.py brief`)
into context; **before a commit or push** it re-surfaces them, so you don't ship
work resting on an unconfirmed guess or a loop that quietly gave up. Silent when
there is nothing to report. Pair with `assumptions.py sweep` to adjudicate.

## Which to use

| Want… | Use |
| ----- | --- |
| Team-wide safety net, no local setup per dev | The **CI** action (1) |
| Fast personal feedback before pushing | The **local review hooks** (2) |
| A durable, rollback-able record of decisions & changes | The **memory hooks** (3) |
| Open guesses & stuck loops surfaced automatically | The **validation hooks** (4) |
| Both review + memory | Install both hook blocks — they complement each other |

## 5. Other agents: Cursor, IntelliJ, OpenAI Codex

The twelve experts and the `/new-feature` + `/review-changes` workflows are **Claude Code
native** (`.claude/skills/`, `.claude/commands/`). To use the *same* personas from another
agentic IDE, this repo ships generated, copy-in integrations — one per tool — each in that
tool's native format and location:

| Tool | Folder | What it ships |
| ---- | ------ | ------------- |
| **Cursor** | [`cursor/`](cursor/) | `.cursor/rules/*.mdc` (the twelve personas as auto-attaching rules + an always-on roster) and `.cursor/commands/*.md` (`/architect`, `/security`, `/frontend`, `/review-changes`, …) |
| **OpenAI Codex** | [`codex/`](codex/) | `AGENTS.praxis.md` (roster for `AGENTS.md`), `.praxis/*.md` (in-repo persona guides) and `prompts/*.md` for `~/.codex/prompts/` (`/praxis-architect`, …) |
| **IntelliJ** (JetBrains AI Assistant & Junie) | [`intellij/`](intellij/) | `.junie/guidelines.md` + `.junie/praxis/*.md` (persona guides) and `prompts/*.md` (ready-to-paste prompt snippets) |

The optional **[StartupOS](../docs/startupos/README.md)** pre-build module rides along in
the same three folders, namespaced so it never mixes with the SDLC experts: its twelve agent
personas ship as `praxis-startupos-*` Cursor rules / `.praxis/startupos-*.md` Codex guides /
`.junie/praxis/startupos-*.md` Junie guides, and its lifecycle commands as `/startupos-*`
(Cursor) and `/praxis-startupos-*` (Codex) prompts. The StartupOS roster lives in the
`praxis-startupos` Cursor rule, a StartupOS section of Codex's `AGENTS.praxis.md`, and
IntelliJ's `.junie/praxis-startupos.md`.

Each folder has its own `README.md` with copy-and-go install steps. All three rely on
`AGENTS.md`, which every one of these tools reads natively, for repo-wide doctrine.

**These files are generated — do not edit them by hand.** They are re-expressed from the
canonical skills + commands by [`scripts/build_integrations.py`](scripts/build_integrations.py)
so they never drift:

```bash
make integrations          # regenerate after editing any skill or command
make integrations-check     # CI guard: fails if the checked-in output is stale
```

See the repo [README](../README.md#wiring-the-experts-into-your-workflow) for how this fits the
rest of the toolkit.
