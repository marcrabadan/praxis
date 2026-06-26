<!--
StartupOS template — product-requirements.md
Filled by /startupos:prd. The bridge artifact Praxis consumes (/praxis:idea, /praxis:new-feature).
Mirror Praxis BA conventions: INVEST stories + Gherkin acceptance criteria.
-->

# Product requirements — <Idea name>

- **Slug:** `<slug>` · **Updated:** <YYYY-MM-DD> · **Status:** draft | accepted

## Product vision

One paragraph: what the product is and the change it creates for the user.

## The wedge

The single capability that delivers value fastest and earns the right to expand.

## MVP scope

| In scope | Why (value/validation hypothesis it tests) |
| -------- | ------------------------------------------ |

| Explicitly out of scope | Why deferred |
| ----------------------- | ------------ |

## Personas & jobs-to-be-done

- **Primary persona:** <…> — top job: <…>
- **Secondary:** <…>

## Functional requirements

Numbered, testable. `FR-1 …`

## Non-functional requirements

Performance, availability, security, privacy, accessibility, cost ceilings. `NFR-1 …`

## User stories

> **US-1** — As a `<role>`, I want `<capability>`, so that `<benefit>`.
>
> **Acceptance (Gherkin):**
> - Given `<context>`, when `<action>`, then `<outcome>`.

(INVEST: independent, negotiable, valuable, estimable, small, testable.)

## Success metrics

| Metric | Definition | Target (validation threshold) |
| ------ | ---------- | ----------------------------- |
| Activation | <…> | <…> |
| Core value metric | <…> | <…> |
| Retention | <…> | <…> |

## Dependencies & assumptions

External dependencies and any requirement still resting on an unvalidated `[ASSUMPTION]` — flagged so Praxis does not treat it as fact.

## Out-of-bounds (Praxis owns)

Detailed design, implementation, test code, and delivery belong to Praxis — not this PRD.
