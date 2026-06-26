# StartupOS → Praxis integration

StartupOS and Praxis are two halves of one delivery lifecycle:

```
  StartupOS                         │  Praxis
  what / why / who / company        │  how to build it correctly
  ──────────────────────────────────┼──────────────────────────────
  discover → … → roadmap            │  /praxis:idea → /praxis:new-feature → release
                    ╲               │   ╱
                     ╲  export-praxis (✋ human gate)
                      ▼            │
              Praxis-ready project ┘
```

StartupOS's **terminal action** is `/startupos:export-praxis`. It never builds product; it hands Praxis a validated, self-contained project so engineering starts with full context instead of a blank page.

## The handoff gate

`/startupos:export-praxis` is a **mandatory human-in-the-loop gate**. It will not export without explicit human approval. Before exporting it runs a completeness check (no stub artifacts) and reports anything still assumption-heavy — it does **not** fabricate missing pieces to complete the bundle.

## What the handoff generates

A Praxis-ready project with a complete `docs/` bundle:

```
docs/
  vision.md                 market-research.md       business-case.md
  competitive-analysis.md   pricing.md               financials.md
  product-requirements.md   architecture.md          roadmap.md
  validation-plan.md        gtm.md                   risk-analysis.md
  praxis-handoff.md
```

`praxis-handoff.md` is the manifest: it states what was **validated** (`[FACT]`), what is still **assumption**, the open questions Praxis should resolve first, and the recommended command sequence. See the [praxis-handoff template](templates/praxis-handoff.md).

## Recommended Praxis command sequence

The handoff writes this sequence into `praxis-handoff.md` so the builder knows exactly where to start:

```text
/praxis:idea            # triage the handed-off product idea into the Praxis harness
/praxis:new-feature     # run the MVP wedge through the full SDLC (discovery → … → release)
/praxis:analyst         # refine requirements / user stories from product-requirements.md
/praxis:product         # backlog, prioritization, sprint goal from the roadmap
/praxis:architect       # detailed design / ADRs — architecture.md is the L1/L2 input
/praxis:security        # threat-model the MVP
/praxis:ml              # only if the product is AI/ML-native
/praxis:review-changes  # review the diff before merge
```

> When this repo is the workspace these are `/idea`, `/new-feature`, …; installed as a plugin they are `/praxis:idea`, `/praxis:new-feature`, …. The handoff uses the namespaced form for clarity.

## How StartupOS artifacts map to Praxis inputs

| StartupOS artifact | Praxis consumer | What Praxis does with it |
| ------------------ | --------------- | ------------------------ |
| `vision.md` | `/praxis:idea` | Triages the idea into the harness |
| `product-requirements.md` | `business-analyst`, `product-owner` | Requirements, user stories, backlog (already INVEST + Gherkin) |
| `architecture.md` (C4 L1/L2) | `software-architect` | Takes ownership of detailed design + ADRs |
| AI strategy section | `ml-ai-engineer` | Metric/eval design, serving, guardrails |
| `risk-analysis.md` | discovery / `security-engineer` | Threat model, risk-driven test focus |
| `validation-plan.md` | discovery / research | Open assumptions become early spikes/tasks |
| `roadmap.md` | `product-owner` | Phasing, sprint goals, release planning |
| `business-case.md`, `financials.md`, `gtm.md`, `pricing.md` | context | Business rationale that frames build trade-offs |

## Boundary discipline

- **Labels survive the boundary.** `[FACT]` / `[ASSUMPTION]` / `[ESTIMATE]` are preserved so Praxis knows what is proven. An open assumption becomes a Praxis spike, not a silent requirement.
- **Altitude is respected.** StartupOS hands off L1/L2 architecture and product requirements; Praxis owns detailed design, code, tests, and delivery.
- **Ownership transfers.** After a successful export, the project is Praxis's. StartupOS's job is done unless the human sends it back to revise.

## Harness mode note

Praxis always runs in harness mode and will auto-bootstrap a project (`tools/ensure_harness.py`) on the first command if the target repo has no `.praxis/config.json`. The export can target either a new `projects/<slug>/` inside this harness (central mode) or a separate product repo path; in both cases the `docs/` bundle is what Praxis's lifecycle reads first.
