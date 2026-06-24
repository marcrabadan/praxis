# Experience Grounding — Design Checklist

Express the design gates as a pass/fail checklist for any spec-driven analysis, checklist, review, or quality-gate phase. The checklist validates that the spec, plan, tasks, and implementation honor the design principles in the governance artifact.

Mark a check `not-applicable` with a one-line reason when the surface genuinely does not engage that gate. Accessibility and usability are never not-applicable.

## When to run

Run from [experience-grounding](experience-grounding.md) Step 6 for any analysis, checklist, review, or quality-gate phase. For a full design-quality pass on a built UI, use the line-by-line [checklist.md](../references/checklist.md) as well.

## The checks

| Check | Gate | Pass when |
|---|---|---|
| Accessibility | `G-accessibility` | Contrast meets WCAG AA, focus is visible, status uses two or more signals, labels are real and not placeholders. |
| Usability floor | `G-usability` | Chunking, option counts, and disclosure stay within the heuristic floor for the named user. |
| Information architecture | `G-ia` | One primary action per surface, a declared region map, an honest scan path. |
| Visual hierarchy and states | `G-hierarchy` | Density, grid, and responsive plan are defined; every interactive element covers default/hover/focus/disabled/loading/empty/error. |
| Components and actions | `G-components` | Each element uses the intent-mapped component; one primary action per area; charts use the agreed approach. |
| Tokens and design system | `G-tokens` | Values come from the selected token source; missing ones are reported as gaps, not invented. |
| Content and tone | `G-content` | Operational voice, no marketing filler in product flows, no em-dashes or fake-precise numbers in user copy. |
| UX and friction | `G-ux` | The discovery line is honored: user, job, failure cost, smallest useful surface; friction matches failure cost. |
| Imagery and taste | `G-imagery` | Marketing or visual surfaces use real images or declared placeholders; anti-AI-tell catalogue honored. |
| Landing conversion | `G-landing` | Marketing surfaces have clear page job, visitor stage, proof, and CTA strategy. |

The first seven checks are detailed in [practices.md](../references/practices.md) and [checklist.md](../references/checklist.md); `G-ux`, `G-imagery`, and `G-landing` are detailed in [ux-comprehension-and-friction](../references/ux-comprehension-and-friction.md), [imagery-visuals-and-taste](../references/imagery-visuals-and-taste.md), and [landing-conversion](../references/landing-conversion.md).

## Procedure

1. Select the checks relevant to the surface; keep accessibility and usability always.
2. For a checklist phase, emit the selected checks as the design section of the generated checklist.
3. For an analysis or review phase, run the checks against the spec, plan, tasks, and implementation and report each as pass, fail, or not-applicable with a reason.
4. Tie each failure back to the governance article it violates, so the fix is governed, not cosmetic.

## Output

- a design checklist section, or a pass/fail/not-applicable report for a review or analysis artifact

## Stop condition

Stop when every applicable check has a verdict and each failure names the governance article it breaks.
