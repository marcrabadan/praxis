# Gate-to-Phase Map

This table says which reference feeds which generic spec-driven phase, so the right reference is loaded at the right moment. Open the linked reference and read the relevant section.

| Gate | Reference | Generic phase | What it contributes |
|---|---|---|---|
| `G-accessibility` | [practices.md](practices.md) §4, §7 / [checklist.md](checklist.md) §3, §7 | governance, analyze/review | WCAG AA, focus, status-not-by-color-alone, real labels. Always on. |
| `G-usability` | [practices.md](practices.md) §9 / [checklist.md](checklist.md) §11 | governance, analyze/review | Chunking, option counts, disclosure, recognition over recall. Always on. |
| `G-tokens` | [practices.md](practices.md) §2 / [checklist.md](checklist.md) §5 | governance, plan, implement | Token discipline, active mode, gaps reported not invented. |
| `G-ia` | [practices.md](practices.md) §9 | governance, spec/define | Region map, one primary action, scan path. |
| `G-content` | [practices.md](practices.md) §10 / [checklist.md](checklist.md) §9 | governance, spec/define, implement | Voice, labels, empty/error states, no filler or fake numbers. |
| `G-ux` | [ux-comprehension-and-friction](ux-comprehension-and-friction.md) | spec/define, clarify | Discovery line: user, job, failure cost, smallest useful surface. |
| `G-components` | [practices.md](practices.md) §1 | plan, implement | Intent-to-component mapping, action hierarchy, charts. |
| `G-hierarchy` | [practices.md](practices.md) §3, §5, §8 / [checklist.md](checklist.md) §1, §2, §4 | implement | Density, grid, responsive, full state coverage. |
| `G-imagery` | [imagery-visuals-and-taste](imagery-visuals-and-taste.md) | implement, marketing | Real images, anti-AI-tells, expression budget. |
| `G-landing` | [landing-conversion](landing-conversion.md) | spec/define, implement, marketing | Page job, visitor stage, proof, CTA strategy. |
| `G-qa` | [checklist.md](checklist.md) | checklist, analyze/review | Consolidated design-review gate, expressed as the design checklist. |

## How to use

- **Governance phase**: load always-on rows (`G-accessibility`, `G-usability`, `G-tokens`, `G-ia`, `G-content`) through [experience-governance-seed](../workflows/experience-governance-seed.md).
- **Spec / clarify phase**: load `G-ux` and `G-ia` (and `G-landing` for marketing) through [experience-phase-contributions](../workflows/experience-phase-contributions.md).
- **Plan phase**: load `G-tokens` and `G-components` through [experience-design-system-grounding](../workflows/experience-design-system-grounding.md).
- **Implement phase**: load `G-hierarchy`, `G-components`, `G-content`, and marketing rows when relevant.
- **Checklist / analyze / review phase**: load the full set through [experience-design-checklist](../workflows/experience-design-checklist.md), anchored on `G-qa`.
