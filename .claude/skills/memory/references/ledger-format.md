# Ledger format

The deterministic data model behind the skill. The CLI owns these files — this
doc is for understanding and debugging, not hand-editing.

## Layout

```
.praxis/memory/
  ledger.jsonl        index, one JSON object per line
  entries/<id>.md      full content (frontmatter + body)
  patches/<id>.patch   reverse-appliable unified diff (implementation entries)
  README.md
```

## Entry id

`YYYYMMDD-HHMMSS-xxxx` — UTC timestamp plus a 4-char random suffix, e.g.
`20260601-153012-9af3`. Sortable and collision-resistant. Commands accept any
unambiguous prefix.

## Index line (`ledger.jsonl`)

One compact JSON object per entry, holding the metadata needed to list and filter
without opening every file:

```json
{"id":"20260601-153012-9af3","created":"2026-06-01T15:30:12Z","updated":"2026-06-01T15:30:12Z","source":"/architect","type":"decision","status":"pending","title":"Adopt hexagonal ports","tags":["arch","adr"],"diff_hash":null,"supersedes":null}
```

## Entry file (`entries/<id>.md`)

Frontmatter mirrors the index and adds the body-only fields, followed by the
human-readable content:

```markdown
---
id: 20260601-153012-9af3
created: 2026-06-01T15:30:12Z
updated: 2026-06-01T15:30:12Z
source: /architect
type: decision
status: pending
title: Adopt hexagonal ports for the payments module
tags: arch, adr, payments
---

Context: ...
Decision: ...
Rationale: ...
Consequences: ...
```

Implementation entries (from `snapshot`) additionally carry:

```
git_base: a1b2c3d        # short sha the diff was taken against
patch: patches/<id>.patch
diff_hash: 9af3c1e0b2d4   # sha1 prefix of the diff, for de-duplication
```

## Fields

| Field | Meaning |
|-------|---------|
| `type` | `plan`, `decision`, `implementation`, `artifact`, `test-strategy`, `rollout`, `note` |
| `status` | `pending`, `accepted`, `rejected`, `rolled-back`, `superseded` |
| `source` | command/skill that produced it (`/new-feature`, `/architect`, `auto`, `manual`) |
| `tags` | free-form comma-separated labels for filtering |
| `supersedes` | id of an entry this replaces (the old one flips to `superseded`) |
| `git_base` / `patch` / `diff_hash` | snapshot-only; enable rollback and de-dup |

## Lifecycle

```
            log / snapshot
                 │
                 ▼
              pending ──accept──▶ accepted ──rollback (impl)──▶ rolled-back
                 │                   │
               reject              rollback (impl)
                 │                   │
                 ▼                   ▼
             rejected            rolled-back

  any open entry + a superseding log  ──▶  superseded
```

Status changes append a dated footer to the entry body so the file keeps its own
audit trail.

These five are the **complete, closed set** of statuses. The CLI enforces it —
`--status` is a fixed `choices=` list and `accept` / `reject` / `rollback` /
`--supersedes` write hard-coded values — so a status outside the set can only
appear if someone hand-edits the ledger, which is forbidden. Never invent a new
status (e.g. `in-progress`, `approved`, `super-seeded`); if you think the
lifecycle needs another state, change the doctrine and the CLI together, not a
single entry.
