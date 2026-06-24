# Experience Grounding — Governance Seed

Turn always-on design gates into **non-negotiable governance principles** for a spec-driven project, so every later phase is checked against concrete UX/UI law rather than vague intent.

This is the highest-leverage injection point: a rule in the governance artifact should propagate downstream through whatever review, plan, or analysis gates the host workflow already uses.

## When to run

Run from [experience-grounding](experience-grounding.md) Step 2, once per project (and again when the project's principles change), after an idea brief exists and the governance artifact has been located.

## Which gates become principles

Seed these, because they apply to almost any app surface:

- `G-accessibility` → an accessibility principle: WCAG AA contrast, focus visibility, status never by color alone, labels not placeholders. Never optional. (Source: [practices.md](../references/practices.md) §4, §7.)
- `G-usability` → a usability-floor principle: chunking, option counts, progressive disclosure, recognition over recall. (Source: [practices.md](../references/practices.md) §9.)
- `G-tokens` → a design-system / token-discipline principle: use real tokens and components first; missing ones are gaps to report, not values to invent. (Source: [practices.md](../references/practices.md) §1, §2.)
- `G-ia` → an information-architecture principle: one primary action per surface, declared region map, honest scan path. (Source: [practices.md](../references/practices.md) §9.)
- `G-content` → a content principle: operational voice, no marketing filler in product flows, no em-dashes or fake-precise numbers in user-visible copy. (Source: [practices.md](../references/practices.md) §10.)

Leave surface-specific gates (`G-hierarchy`, `G-components`, `G-imagery`, `G-landing`) to per-screen phase contributions; they are too situational to be governance law for every surface.

## Procedure

1. Read the always-on design domains in [practices.md](../references/practices.md) (accessibility, usability, tokens/components, IA, content) so the articles cite concrete, verifiable standards.
2. Open [governance-design-articles](../references/governance-design-articles.md) and tailor each article to the project's design source of truth: named design system, token set, component library, `DESIGN.md`, Figma source, or "free".
3. Read the existing mapped governance artifact if present. Merge the design articles as new principles, or fold them into the matching existing quality/UX section; do not overwrite or renumber existing principles without approval.
4. Keep each article testable: a reviewer or analysis phase must be able to judge pass or fail.
5. Record which design source of truth the articles assume, so the plan phase can bind to it.

## Output

- design principles merged into the workflow's governance artifact
- a one-line note of which gates were seeded and which were deferred to per-screen contributions

## Stop condition

Stop when the governance artifact carries the always-on design articles, tailored to the project's design source of truth, with existing principles preserved.
