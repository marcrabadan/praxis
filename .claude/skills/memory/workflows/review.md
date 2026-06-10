# Workflow — Review

Inspect the ledger and advance entries through their lifecycle. Use when the user
asks "what's pending / what did we decide / what did we build", or wants to
accept or reject recorded entries.

## Steps

1. **Show the relevant slice.** Default to pending when the user asks "what's
   outstanding":

   ```bash
   python .claude/skills/memory/scripts/ledger.py pending
   python .claude/skills/memory/scripts/ledger.py list --status accepted
   python .claude/skills/memory/scripts/ledger.py list --type decision
   python .claude/skills/memory/scripts/ledger.py status        # dashboard
   ```

2. **Inspect full content** when the user drills into one:

   ```bash
   python .claude/skills/memory/scripts/ledger.py show <id>
   ```

3. **Advance the lifecycle — only on explicit user intent.** Never auto-accept or
   auto-reject; the lifecycle is the user's call.

   ```bash
   python .claude/skills/memory/scripts/ledger.py accept <id> --note "shipped in PR #42"
   python .claude/skills/memory/scripts/ledger.py reject <id> --note "superseded by new design"
   ```

   Ids accept an unambiguous prefix, so a user can pass the first few characters.

4. **Accept is the trigger — execute on it.** Accepting is not just bookkeeping:
   it is the green light the pending status was waiting for. When the user
   accepts a `plan`, `decision`, `test-strategy`, or `rollout` whose work has
   not been done yet, **carry that work out in the same turn** (`show <id>` for
   the full body) — don't make the user ask a second time. If the authorized
   work is large or its scope is ambiguous, confirm the scope with one focused
   question, then execute. A `reject` is the opposite signal: do not act, and
   do not re-propose the same thing unchanged. Accepting an `implementation`,
   `artifact`, or `note` usually just ratifies something that already exists —
   nothing further to run.

5. **Summarize.** After a status change, confirm the entry's new state and —
   when acceptance triggered work — what was executed. When listing, give a
   short human summary (e.g. "3 pending decisions, 1 accepted implementation")
   rather than only dumping the raw list.

## Notes

- `superseded` is set automatically when a new entry is logged with
  `--supersedes <id>`; you don't set it by hand.
- To undo a shipped implementation, use [rollback.md](rollback.md), not `reject`
  (reject only changes status; rollback also reverts the code).
