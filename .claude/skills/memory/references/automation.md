# Automation — making memory automatic

The user asked memory to be captured **automatically across all commands and
skills**. In Claude Code, truly automatic behavior is driven by **hooks** (the
harness runs them), reinforced by **doctrine** (what the agent is told to do).
This skill ships both halves; the hook is opt-in per consuming repo.

## The two halves

1. **Doctrine (agent-driven, rich content).** The always-on rule in
   [../SKILL.md](../SKILL.md) and the global rule in the repo's `AGENTS.md` tell
   every command and skill to record durable artifacts before ending a turn.
   `/new-feature` and `/review-changes` call it out explicitly. This captures the
   *why* — decisions, plans, rationale — that a mechanical hook can't see.

2. **Hook (harness-enforced, mechanical capture).** The template at
   `integrations/hooks/memory.settings.example.json` wires:
   - **SessionStart** → `ledger.py init` + `ledger.py bootstrap --brief` +
     `ledger.py pending --brief`. Every session begins by ensuring the ledger
     exists, then orienting the session: `bootstrap --brief` prints one line —
     when the ledger is empty it suggests running `/memory init` to seed memory
     from the repo's existing context (the closest thing Claude Code offers to an
     on-install step), otherwise it reports how much is on record — and
     `pending --brief` surfaces entries still awaiting accept/reject. All injected
     into context so nothing is forgotten between sessions.
   - **PreToolUse (git commit/push)** → `ledger.py pending --brief` to stderr.
     Just before work ships, the entries still awaiting accept/reject are
     re-surfaced, so work whose only authorization is a `pending` decision or
     plan gets caught at the door (**pending is not approval** — stop condition
     `U-11`). A nudge, never a block: planning runs legitimately commit with
     everything pending.
   - **Stop** → `ledger.py snapshot --source auto`. When the agent finishes a
     turn with uncommitted changes, it captures a de-duplicated, rollback-able
     snapshot automatically — so even unrecorded implementations can be undone.

Together: the hook guarantees *something* is always captured and surfaced; the
doctrine makes the captured record meaningful.

## Why not "hook-only"

A hook sees tool I/O and git diffs, not the reasoning behind a decision. Hook-only
memory would store *what changed* but never *why it was chosen*. That's why this
skill pairs the snapshot hook with the doctrine that records decisions and plans.

## Installing the hook (consuming repo)

Copy the `hooks` block from `integrations/hooks/memory.settings.example.json`
into the repo's `.claude/settings.json` (merge if it already has hooks), and make
sure `.claude/skills/memory/` is present (via the `praxis` plugin or
`make export SKILL=memory TO=<repo>`). praxis ships this as a template and does
not enable it on itself.

**Seed it once after adopting praxis.** Claude Code has no true "on plugin
install" hook, so the one-time seed is an explicit `/memory init` (the
`bootstrap` workflow). It primes the ledger from the repo's existing context —
`AGENTS.md`, ADRs, architecture docs, and git history — so memory reflects the
project from day one instead of only what happens after install. The SessionStart
hook nudges you to run it whenever it finds the ledger empty.

## Tuning

- Don't want auto-snapshots on every stop? Drop the `Stop` hook and rely on
  explicit `snapshot`/`log` calls plus the doctrine.
- Snapshots de-duplicate by diff hash, so an unchanged working tree across several
  stops produces at most one pending entry.
- Review and prune pending auto-snapshots periodically (`/memory list pending`),
  accepting the meaningful ones and rejecting the noise.
