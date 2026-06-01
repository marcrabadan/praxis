# Workflow — Capture

Record a durable artifact (plan, decision, implementation, test strategy, rollout,
or other artifact) as a ledger entry.

## When you reach here

- A command/skill just produced a durable artifact, or
- The user explicitly asks to remember / save / log something.

## Steps

1. **Decide if it's worth recording.** Record decisions, plans, designs, test
   strategies, rollout plans, and shipped changes. Skip throwaway exploration.
   When unsure and the artifact is significant, record it as `pending`.

2. **Pick the type.** One of: `plan`, `decision`, `implementation`, `artifact`,
   `test-strategy`, `rollout`, `note`. For *code that changed on disk*, prefer a
   `snapshot` (step 4) — it also captures a rollback patch.

3. **Log it.** Write a self-contained body (see
   [../references/rules.md](../references/rules.md) for the shape — a decision
   should read like a mini-ADR: context, decision, rationale, consequences).

   ```bash
   python .claude/skills/memory/scripts/ledger.py log \
     --type decision \
     --title "Adopt hexagonal ports for the payments module" \
     --source /architect \
     --tags arch,adr,payments \
     --body "Context: ...\nDecision: ...\nWhy: ...\nConsequences: ..."
   ```

   - `--source` is the command/skill that produced it (`/new-feature`,
     `/architect`, `/review-changes`, …) so the ledger shows provenance.
   - Long bodies: write to a temp file and pass `--body-file`, or pipe via
     `--body -`.
   - Replacing an earlier decision? Pass `--supersedes <id>`; the old entry is
     marked `superseded` automatically.

4. **For changes already on disk, snapshot instead.** This stores a
   reverse-appliable patch so the change can be rolled back later:

   ```bash
   python .claude/skills/memory/scripts/ledger.py snapshot \
     --source /new-feature --title "Auth slice 1 — login endpoint"
   ```

   By default it captures uncommitted changes (`git diff HEAD`). To capture
   everything since a ref (committed + uncommitted), pass `--since <ref>`.
   Identical diffs are de-duplicated, so it is safe to run repeatedly.

5. **Default status is `pending`.** Use `pending` unless the user has already
   approved the artifact, in which case `--status accepted`.

6. **Report back.** State what was recorded, its id, and its status. Do not
   announce every tiny log line during a long task — batch into one rich entry
   per artifact.

## One entry per artifact

Prefer a single coherent entry over many fragments. A `/new-feature` run should
leave a small handful of entries (the plan, the key decisions, optionally a
snapshot of the first slice) — not one per phase sentence.
