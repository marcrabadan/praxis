# Workflow — Bootstrap (init)

Prime a fresh ledger so memory reflects the project **from day one**, instead of
only capturing what happens after the skill is installed. This is the `/memory
init` mode — run it once when adopting praxis in a repo (or any time you want to
backfill decisions that predate the ledger).

## When you reach here

- The user ran `/memory init` (or asked to "bootstrap / seed / initialize memory").
- The SessionStart hook reported the ledger is empty and you want to seed it.

## Steps

1. **Gather the raw context (deterministic).** Run the CLI — it ensures the
   ledger exists, then reports the existing entry count, the durable-context docs
   present in the repo, and a git-history summary:

   ```bash
   python .claude/skills/memory/scripts/ledger.py bootstrap
   ```

   The script never writes entries. Deciding *what is worth remembering* is your
   job (see [../references/rules.md](../references/rules.md)).

2. **If the ledger already has entries, stop seeding.** Surface what's on record
   (`/memory` → `status` + recent) and only add new entries on explicit request.
   Don't duplicate what's already captured.

3. **Read the candidate docs and history.** Open the docs the report listed
   (`AGENTS.md`, `README.md`, `ARCHITECTURE.md`, ADRs under `docs/adr/…`, etc.)
   and skim `git log`. You are looking for **durable decisions and structure**,
   not a summary of every file.

4. **Record one rich entry per durable decision**, as `pending`, attributing the
   source to the bootstrap:

   ```bash
   python .claude/skills/memory/scripts/ledger.py log \
     --type decision \
     --title "Hexagonal architecture for the payments module" \
     --source /memory --tags bootstrap,arch,adr \
     --body "Context: ...\nDecision: ...\nRationale: ...\nConsequences: ..."
   ```

   Good things to seed (when the repo actually shows them):
   - **decisions** — architecture style, language/framework choices, key ADRs.
   - **plan** — the active roadmap or in-flight initiative, if one is documented.
   - **artifact / note** — a load-bearing interface contract, a diagram path, a
     non-obvious constraint the next teammate must know.

   Write each entry per [../references/rules.md](../references/rules.md): a
   decision reads like a mini-ADR. Tag them `bootstrap` so the seeded set is easy
   to find and prune later.

5. **Be conservative.** Seed only what a teammate opening the repo would genuinely
   want in memory. A handful of meaningful entries beats a transcription of the
   README. **Never record secrets, tokens, or credentials.**

6. **Leave them pending.** Bootstrapped entries start `pending` so the user
   accepts the ones worth keeping and rejects the noise. Report the ids you
   created and point the user at `/memory` to review.

## Stop conditions

- The ledger was initialized and either seeded with a small set of `pending`
  entries (ids reported) or left empty because there was nothing durable to seed.
- An already-populated ledger was surfaced rather than re-seeded.
