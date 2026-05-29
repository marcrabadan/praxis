# Wiring praxis into your dev flow

The six SDLC experts are most useful when they reach the code **at the moment a mistake is
made** — not only when someone remembers to ask. This is the gap these integrations close:
they move the experts from *pull* (you invoke them) to *push* (they show up automatically),
so juniors catch bad practices they didn't know to look for, seniors get a low-friction
second pair of eyes, and architects see the team's standards enforced consistently.

Everything here is **opt-in and portable** — copy it into a consuming repository. `praxis`
itself ships these as templates and does not enable them on its own CI.

## The reviewer: `/review-changes`

The behaviour everything below triggers. It reads the current diff, routes to only the
relevant experts (developer / qa / architect / devops), and returns **severity-tagged,
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

## Which to use

| Want… | Use |
| ----- | --- |
| Team-wide safety net, no local setup per dev | The **CI** action (1) |
| Fast personal feedback before pushing | The **local hooks** (2) |
| Both | Install both — they complement each other |

## 3. Other agents: Cursor, IntelliJ, OpenAI Codex

The six experts and the `/new-feature` + `/review-changes` workflows are **Claude Code
native** (`.claude/skills/`, `.claude/commands/`). To use the *same* personas from another
agentic IDE, this repo ships generated, copy-in integrations — one per tool — each in that
tool's native format and location:

| Tool | Folder | What it ships |
| ---- | ------ | ------------- |
| **Cursor** | [`cursor/`](cursor/) | `.cursor/rules/*.mdc` (the six personas as auto-attaching rules + an always-on roster) and `.cursor/commands/*.md` (`/architect`, `/review-changes`, …) |
| **OpenAI Codex** | [`codex/`](codex/) | `AGENTS.praxis.md` (roster for `AGENTS.md`), `.praxis/*.md` (in-repo persona guides) and `prompts/*.md` for `~/.codex/prompts/` (`/praxis-architect`, …) |
| **IntelliJ** (JetBrains AI Assistant & Junie) | [`intellij/`](intellij/) | `.junie/guidelines.md` + `.junie/praxis/*.md` (persona guides) and `prompts/*.md` (ready-to-paste prompt snippets) |

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
