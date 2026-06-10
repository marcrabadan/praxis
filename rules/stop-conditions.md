# Stop Conditions

This is a **harness rule**. It makes "ask when unclear" first-class. When any
condition below holds, the agent **stops and asks** instead of guessing — because
guessing wrong would change ownership, destination, behavior, architecture,
security posture, or the verification standard.

This is the global stop list. Individual workflows may add their own local stop
conditions on top of these.

## Stop and ask when ambiguity would change

- **Project ownership** — which project this work belongs to (unresolved
  `projectId`, unknown project mapping).
- **Artifact destination** — where a spec, decision, or plan should be written.
- **Source of truth** — which file or repo is canonical for the thing being
  edited; conflicting repo-local docs.
- **Product behavior** — what the feature should actually do for a user.
- **Architecture** — a structurally significant choice (new boundary, new
  datastore, new integration, a pattern the project hasn't used).
- **Security posture** — authn/authz, secrets handling, data classification,
  exposure of a new surface.
- **Verification standard** — what "done" and "tested" mean for this change when
  it is not already declared.
- **Whether a pending decision is approved** — a `pending` entry is a proposal,
  **not** authorization. Do not execute the work it authorizes until the user
  accepts it. When the work is observably about to execute on a still-pending
  authorization, this hardens into catalog condition `U-11`.

## Hard blocks (cannot proceed at all)

These are not "ask if convenient" — they block implementation outright:

- **Broken harness config** — a `.praxis/config.json` that is *present* but
  unusable: malformed JSON, or a `harnessRoot` that does not resolve to an
  existing path. Stop and ask; never overwrite a config you did not write.
  (A **missing** config is *not* a hard block — harness mode is always on, so the
  harness auto-bootstraps one via `tools/ensure_harness.py` and continues.)
- **Unresolvable project id** — a config declares a `projectId` that maps to no
  project under `projects/` (in `central` mode) or has no `.praxis/project/`
  (in `local` mode). A *declared-but-broken* pointer is a hard block: stop and
  ask. An *absent* config is handled by auto-bootstrap, not a stop.
- **Missing project memory for the active project** — no `current-state.md` or
  `open-questions.md`.
- **Missing source of truth** — the artifact you would edit has no canonical
  home and you'd have to invent one.
- **Open questions that affect the current step** — an unresolved entry in
  `open-questions.md` directly gates the work in front of you.

## How to ask

Ask one focused question at a time with suggested answers. State the assumption
you would otherwise make and why it is material. Record the resolution where it
belongs (project decision or memory ledger) once the user answers — do not let
the answer live only in chat.

## Deterministic stop conditions (the catalog)

The conditions above are **judgement** calls — ambiguity that *would change*
something material, so you ask. Beside them is the *hard-blocker* half:
[stop-conditions-catalog.md](stop-conditions-catalog.md) enumerates observable
triggers (`U-1…U-11`, plus per-project `P-*` and per-spec `S-*`) with the exact
`STOP[...]` text to surface and the gate that resolves each. Those are not "ask if
unclear" — an undefined value, an unresolvable asset, a gate that cannot run, a
self-certified gate: the agent halts, writes a [run log](../projects/_template/specs/_template/runs/_run-log.md),
and resumes only on the resolution gate.

The three mechanisms partition cleanly: a **soft, low-confidence guess** →
[assumptions ledger](never-assume.md); **material judgement ambiguity** → this
file; a **hard observable blocker** → the catalog.

## What is *not* a stop condition

Do not stop for choices with a conventional default you can verify from the
codebase, for cosmetic preferences, or for low-stakes reversible steps. Stopping
has a cost; reserve it for material ambiguity.
