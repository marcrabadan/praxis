# Workflow — Rollback

Undo a snapshotted implementation by reverse-applying its recorded patch. Use when
the user says "roll back that change", "undo what we built", or accepts that a
recorded implementation should be reverted.

## Preconditions

- The entry must be an `implementation` with a recorded `patch:` (i.e. created via
  `snapshot`). Plain `log` entries (plans, decisions) have nothing to revert —
  use `reject` for those.

## Steps

1. **Find the entry.**

   ```bash
   python .claude/skills/memory/scripts/ledger.py list --type implementation
   python .claude/skills/memory/scripts/ledger.py show <id>
   ```

2. **Dry-run first.** This checks the patch still applies in reverse without
   touching the working tree:

   ```bash
   python .claude/skills/memory/scripts/ledger.py rollback <id> --dry-run
   ```

   - **Clean** → proceed to step 3.
   - **Does not apply** → the code has moved on since the snapshot. Do not force
     it. Tell the user, and offer to resolve manually with
     `git apply --reverse --3way .praxis/memory/patches/<id>.patch`.

3. **Roll back.** Reverts the snapshotted change in the working tree and marks the
   entry `rolled-back`:

   ```bash
   python .claude/skills/memory/scripts/ledger.py rollback <id> --note "why"
   ```

4. **Find and mark stale documentation and diagrams.**

   Docs and diagrams generated from this entry are tagged `source:<id>` in the
   ledger. Find them and mark them `superseded` so they are clearly stale:

   ```bash
   python .claude/skills/memory/scripts/ledger.py dependents <id>
   ```

   For each artifact returned, run:

   ```bash
   python .claude/skills/memory/scripts/ledger.py supersede <artifact-id> \
     --note "Source entry <id> was rolled back — this doc/diagram is now stale."
   ```

   If there are no dependents, skip this step silently.

5. **Surface the stale artifacts to the user.**

   After marking superseded entries, list them clearly so the user knows what
   needs regenerating:

   > **Stale docs/diagrams after rollback:**
   > - `<artifact-id>` — `<title>` (`<path if known>`)
   > - …
   >
   > Run `/docs` or `/diagram` to regenerate them against the updated codebase.

   If nothing was stale, say so: "No dependent docs or diagrams were found — nothing to regenerate."

6. **Hand back to the user.** The revert lands in the working tree but is **not
   committed**. Tell the user to review `git diff` and commit when satisfied.
   Optionally run `/review-changes` on the revert.

## Safety

- Rollback never force-applies and never commits. A failed dry-run stops the flow.
- It operates on the working tree only — it does not rewrite history.
- If the user wants to undo a *plan* or *decision* (not code), use `reject` in
  [review.md](review.md) instead, optionally logging a new superseding decision.
- `supersede` only marks the ledger entry — it does not delete the generated
  file on disk. The stale file remains until the user regenerates and overwrites it.
