# Rules

The four rules that keep the learning loop safe. Read these before running any
workflow in this skill.

## Rule 1 — Propose, never silently mutate

`skill-learner` never edits, creates, or rewrites a skill as a fait accompli.
Every create or refinement is recorded in the [memory ledger](../../memory/SKILL.md)
as a `pending` entry and surfaced to the user. **Pending is a proposal awaiting
the user's call, not approval to treat the new knowledge as canonical.** This is
the same human-in-the-loop discipline the whole repo runs on (`AGENTS.md` global
rules: "Leave a record", "pending is not approval").

Why: the factory's value is auditability and rollback. A loop that mutates its
own skills unattended would let unreviewed, possibly wrong "knowledge" harden
into doctrine.

## Rule 2 — Capture conventions, not public facts

A skill exists to hold knowledge the model does **not** reliably produce on its
own: *this org's* conventions, runbooks, decisions, and preferences. It is not a
place to cache public facts the model already knows.

- Capture: "our Terraform modules live in `infra/modules/<service>`, state in an
  Azure Storage backend per environment, every resource tagged `cost-center`."
- Do **not** capture: "Terraform uses HCL", "an Azure resource group groups
  resources" — answer those directly and move on.

When in doubt: if a competent engineer with no access to this org could write the
content from general knowledge, it does not belong in a skill.

## Rule 3 — Smallest home first; promote on evidence

Default to the smallest home that fits: a `references/<topic>.md` inside the role
expert that already owns the domain. Create a dedicated top-level skill (e.g.
`lang-terraform`, `iac-azure`) only when
[the promotion policy](../../../factory/ai/promotion-policy.md) criteria are met —
demonstrated independent invocation, a distinct trigger surface, a stable
interface, and harness folders that will actually be used.

This directly answers the "one skill per language vs language-agnostic" question:
**keep role experts language-agnostic; push language/tool specifics into their
references; promote a `lang-*` skill only on evidence.** Pre-emptive splitting
creates trigger collisions and under-triggering — the most common skill-factory
failure.

## Rule 4 — Delegate authoring; classify and validate

`skill-learner` decides *what* to learn and *where* it goes. It does not
re-implement scaffolding, tiering, or validation — it routes to the
[`skill-creator`](../../skill-creator/SKILL.md) for those. Always classify the
tier before scaffolding, and always run the deterministic validator
(`scripts/validate_skill.py`) on any touched skill before declaring done. Never
ask the model to do what a validator can check.
