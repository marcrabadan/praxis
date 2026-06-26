<!--
StartupOS template — praxis-handoff.md
Filled by /startupos-export-praxis. The manifest that crosses the StartupOS → Praxis boundary.
Carry fact/assumption/estimate labels across — never launder a StartupOS assumption into a Praxis "requirement".
-->

# Praxis handoff — <Idea name>

- **Slug:** `<slug>`
- **Exported:** <YYYY-MM-DD>
- **Approved by (human):** <name>
- **Target Praxis project:** `projects/<slug>/` (or `<repo path>`)

> **Boundary:** StartupOS answered *what to build, why, and for whom, and how to turn it into a company.*
> Praxis now answers *how to build it correctly.* Ownership passes here.

## Bundle contents

The export generates a Praxis-ready `docs/` set. Each row links the source StartupOS artifact and its evidence status.

| File | Source command | Evidence status |
| ---- | -------------- | --------------- |
| `docs/vision.md` | `/startupos-discover` | <validated/assumption-heavy> |
| `docs/market-research.md` | `/startupos-research` | <…> |
| `docs/business-case.md` | `/startupos-business-case` | <…> |
| `docs/competitive-analysis.md` | `/startupos-research` `/startupos-challenge` | <…> |
| `docs/pricing.md` | `/startupos-business-case` | <…> |
| `docs/financials.md` | `/startupos-business-case` | <…> |
| `docs/product-requirements.md` | `/startupos-prd` | <…> |
| `docs/architecture.md` | `/startupos-architecture` | <…> |
| `docs/roadmap.md` | `/startupos-roadmap` | <…> |
| `docs/validation-plan.md` | `/startupos-validate` | <…> |
| `docs/gtm.md` | `/startupos-business-case` | <…> |
| `docs/risk-analysis.md` | `/startupos-challenge` | <…> |
| `docs/praxis-handoff.md` | `/startupos-export-praxis` | this file |

## What was validated

The hypotheses that experiments confirmed (with the evidence). These are `[FACT]` — Praxis can build on them.

## What is still assumption

The leaps Praxis must **not** treat as proven. Each should become an early task or spike.

| Open assumption | Risk if wrong | Suggested first Praxis action |
| --------------- | ------------- | ----------------------------- |

## Open questions for Praxis to resolve first

The questions discovery/research could not close — Praxis should address these before deep build.

## Recommended Praxis command sequence

```
/praxis:idea            # triage the handed-off product idea into the harness
/praxis:new-feature     # run the MVP wedge through the full SDLC (discovery → … → release)
/praxis:analyst         # refine requirements / user stories from product-requirements.md
/praxis:product         # backlog, prioritization, sprint goal from the roadmap
/praxis:architect       # detailed design / ADRs — architecture.md is the L1/L2 input
/praxis:security        # threat-model the MVP
/praxis:ml              # only if the product is AI/ML-native
/praxis:review-changes  # review the diff before merge
```

## MVP definition (the first thing Praxis should build)

The wedge from `product-requirements.md`, with its success metrics and validation thresholds.

## Handoff sign-off

- [ ] All bundle files present and non-stub
- [ ] Fact/assumption/estimate labels carried through
- [ ] Risks and validation plan included
- [ ] Human approved the export (mandatory gate)
