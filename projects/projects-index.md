# Projects Index

This is the registry of projects the harness governs. Each project has a folder
under `projects/<project-id>/` following the shape in
[`_template/`](_template/). To add a project, copy `_template/` to
`projects/<your-project-id>/`, fill in `PROJECT.md`, and add a row below.

The harness validator (`tools/validate_harness.py`) checks that every project
listed here exists with the required shape, and that every project folder on disk
(except `_template/`) is listed here.

| Project id | Name | Status | Notes |
|------------|------|--------|-------|
| `helios` | Helios | active | Example **multi-repo** project (central mode) — last-mile logistics across 4 repos. |

## Status values (closed set)

A project's `status` (in its `PROJECT.md` frontmatter) is exactly one of:

| Status | Meaning |
|--------|---------|
| `active` | Currently worked on; agents may load and update its memory. |
| `paused` | Temporarily inactive; kept for context, not actively changed. |
| `archived` | Closed out; retained for history only. |

Never invent another status. If the lifecycle needs a new state, change the
schema and this doc together — not a single project file.
