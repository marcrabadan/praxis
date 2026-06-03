# Workflow — Full Manual (Functional + Technical)

Generate both the functional and technical manuals in one pass, cross-linked into a unified documentation set.

## When you reach here

The scope is broad — "document the project", "generate all the docs", "create a documentation baseline". Both manuals are produced, then stitched with shared cross-links so a reader can navigate from a feature description in the functional manual directly to the architecture section that implements it.

## Steps

### 1. Gather shared context (once, cheap)

Run in parallel:

```bash
# Memory ledger
python .claude/skills/memory/scripts/ledger.py list --status accepted
python .claude/skills/memory/scripts/ledger.py list --status pending

# Codebase
find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.py" -o -name "*.go" \) | head -60
find . -name "README*" -o -name "*.md" -path "*/docs/*" | head -20
```

Also check what documentation already exists to avoid duplication.

### 2. Confirm scope if large

If the system has many modules or the ledger has many entries, surface a brief plan:

> "I'll produce: (1) `docs/functional-manual.md` — BA + PO + UX; (2) `docs/technical-manual.md` — Architect + Developer + DevOps + [domain experts if warranted]. Shall I proceed?"

Wait for confirmation before starting the subagents.

### 3. Run both workflows in order

Run the **functional** workflow first — its feature catalogue is input to the technical manual's implementation reference.

1. Follow [functional.md](functional.md) to completion.
2. Pass the functional manual as additional context when starting [technical.md](technical.md).

Within each workflow, follow the subagent dispatch and stitching instructions in that workflow file.

### 4. Add cross-links

After both files exist, add a `## See also` section to each:

**In `functional-manual.md`:**
```markdown
## See also

- [Technical Manual](technical-manual.md) — how the features described here are implemented
```

**In `technical-manual.md`:**
```markdown
## See also

- [Functional Manual](functional-manual.md) — the user-facing description of what this system does
```

Also link specific sections where a feature in the functional manual maps to a component in the technical manual.

### 5. Record to the ledger

One entry for the full pass:

```bash
python .claude/skills/memory/scripts/ledger.py log \
  --type artifact \
  --title "Documentation: functional + technical manual — <scope>" \
  --source /docs \
  --tags docs,manual,functional,technical \
  --body "Full documentation pass. Functional: docs/functional-manual.md (BA + PO + UX). Technical: docs/technical-manual.md (Architect + Developer + DevOps + <domain experts>). Ledger entries used: <ids>."
```

### 6. Report

Summarise:
- Files written (paths)
- Experts used per manual
- Ledger entries rendered
- Sections skipped and why
- Suggested next step (e.g. "review the artifact entries in /memory and accept them, then commit `docs/`")
