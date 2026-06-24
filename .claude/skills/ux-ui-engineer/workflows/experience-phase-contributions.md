# Experience Grounding — Phase Contributions

For each generic spec-driven phase, name exactly what design intelligence to inject and which reference to load. The host workflow owns the artifact; this workflow says what design content goes into it and stops there.

Load only the reference the active phase needs. Do not pull the whole reference library at every phase.

## When to run

Run from [experience-grounding](experience-grounding.md) Steps 3, 4, and 6, once per phase as the host workflow advances (spec, clarify, plan, tasks, implement). The gate-to-phase mapping is in [gate-phase-map](../references/gate-phase-map.md).

## Per-phase contributions

### Spec / define

Inject the **experience requirements**, derived from the discovery line in [ux-comprehension-and-friction](../references/ux-comprehension-and-friction.md) (`G-ux`) and the information-architecture rules in [practices.md](../references/practices.md) §9 (`G-ia`):

- the user, primary job, and failure cost, written as user stories and success criteria
- the smallest surface that solves the job, so the spec does not over-scope
- per screen: the primary action and must-show content, as acceptance criteria
- accessibility and content expectations as functional requirements, not afterthoughts
- for marketing or recruitment surfaces, page job, visitor stage, proof, and CTA strategy from [landing-conversion](../references/landing-conversion.md)

### Clarify

Surface design ambiguities as clarification questions:

- unknown user or failure cost
- unnamed primary action
- missing design source of truth
- undefined default, hover, focus, disabled, loading, empty, and error states
- unclear content voice or trust/proof requirement

These are the same discovery questions a strong prototype workflow would ask, but recorded in the host workflow's clarification artifact.

### Plan

Contribute the **design-system architecture**, from the tokens/theming and component-library rules in [practices.md](../references/practices.md) §1, §2 (`G-tokens`, `G-components`):

- which component library and token set the app builds on, and the active theme/mode
- the aesthetics source: a design system, Figma file, `DESIGN.md`, brand note, or "free"
- how the governance principles constrain the chosen stack
- known token, component, state, or Figma mapping gaps

Hand details to [experience-design-system-grounding](experience-design-system-grounding.md).

### Tasks

Ensure each screen-building task names its design acceptance:

- components to use
- states to cover: default, hover, focus, disabled, loading, empty, error
- gates that must pass
- a per-screen design-rationale task using [design-rationale-snippet](../references/design-rationale-snippet.md)

### Implement

Apply per-screen gates at build time:

- visual hierarchy and layout — [practices.md](../references/practices.md) §3, §5, §8 (`G-hierarchy`)
- components and actions — [practices.md](../references/practices.md) §1 (`G-components`)
- content and tone — [practices.md](../references/practices.md) §10 (`G-content`)
- for marketing surfaces, [imagery-visuals-and-taste](../references/imagery-visuals-and-taste.md) (`G-imagery`) and [landing-conversion](../references/landing-conversion.md) (`G-landing`)

Fill the embedded design-rationale block as the screen is built.

**Load [implementation-guardrails](../references/implementation-guardrails.md)** here, always. It keeps implementation minimal, surgical, and verifiable. Apply the registered aesthetics source through the selected component library or token layer instead of hardcoding per component.

## Output

- design content written into the active phase's governed artifact
- the gate-to-phase mapping honored (see [gate-phase-map](../references/gate-phase-map.md))

## Stop condition

Stop when the active phase's artifact carries its design contribution and the next phase has what it needs.
