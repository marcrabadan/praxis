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

4. **Summarize.** After a status change, confirm the entry's new state. When
   listing, give a short human summary (e.g. "3 pending decisions, 1 accepted
   implementation") rather than only dumping the raw list.

## Notes

- `superseded` is set automatically when a new entry is logged with
  `--supersedes <id>`; you don't set it by hand.
- To undo a shipped implementation, use [rollback.md](rollback.md), not `reject`
  (reject only changes status; rollback also reverts the code).
