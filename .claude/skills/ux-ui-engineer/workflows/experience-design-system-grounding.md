# Experience Grounding — Design System and Figma Grounding

Fix the design source of truth before a spec-driven process plans or writes code.

Without this, a governed app can still invent colors, spacing, and components, then drift from the design system the governance artifact promised.

## When to run

Run from [experience-grounding](experience-grounding.md) Step 5 (plan phase), before tasks or implementation are written.

## What to ground

1. **Component source.** Name the library the app builds on: a named design system, shadcn, another component library, or "free". Record it in the plan artifact.
2. **Aesthetics source.** Name where the visual language comes from. It can be the component library's own tokens, a Figma file, a brand note, or a **`DESIGN.md` aesthetics file**: color roles, type roles, density, radii, and anti-patterns. Record the path so it is not lost between phases.
3. **Tokens.** From the token-discipline rules in [practices.md](../references/practices.md) §2 (`G-tokens`): token layers available, active theme/mode, and the rule that missing tokens are gaps to report rather than values to invent.
4. **Components.** From the component-library rules in [practices.md](../references/practices.md) §1 (`G-components`): intent-to-component mapping, one primary action per area, and chart/data approach.
5. **Figma, when present.** If a Figma file is the source of truth, inspect variables and components with whatever Figma access the current runtime provides. Map Figma variables and components to the code design system. Stop on unresolved token or component gaps instead of approximating silently.

## The component library plus DESIGN.md sub-case

A common setup: the component library is **shadcn/ui** or similar and the aesthetics come from a **`DESIGN.md`** file rather than a full design system. Ground it like this:

1. Record in the plan: component library, aesthetics source path, token surface, active mode.
2. Map the `DESIGN.md` roles to the component library's theming surface: color roles to CSS variables / Tailwind tokens, type and radii roles to the same, so the look is applied through the library token layer, not hardcoded per component.
3. At implementation time, the agent reads `DESIGN.md`, sets theme tokens from it once, and uses stock components styled by those tokens. Anything `DESIGN.md` specifies that the library cannot express is recorded as a gap, not faked.

## Procedure

1. Identify the design source of truth from the idea brief, plan inputs, existing code, Figma link, `DESIGN.md`, or by asking.
2. Record the component-source mode, aesthetics source, token set, active mode, and known gaps in the plan artifact.
3. For each unresolved mapping, record a gap and proposed resolution; do not silently invent.
4. Hand the grounded facts to implementation so code uses real tokens and components first, and applies the aesthetics source through the library's theme layer.

## Output

- a design-source-of-truth section in the plan artifact: component library, aesthetics source, token set, active mode, and known gaps

## Stop condition

Stop when the plan names the component library, aesthetics source or lack of one, token set, and mode, with gaps surfaced rather than guessed.
