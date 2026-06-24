# Experience Grounding — Guided Run

The entry workflow for grounding a spec-driven product or software process in UX, UI, accessibility, and design-system discipline. Drive the grounding flow interactively, from process detection through implementation support, so the user does not have to translate design discipline into every lifecycle phase manually.

The contract stays **non-owning**: this workflow identifies the host workflow's next step and injects design judgment from the sibling experience-grounding workflows. The host workflow still authors specs, plans, tasks, code, and verification artifacts.

## When to run

Run this workflow when the user is building or extending a real app through a spec-driven, PRD-driven, SDD, or governed development process and wants UX/UI rigor in the specs, plans, tasks, or implementation — or wants an upfront interview that produces durable idea context before spec writing begins.

Do **not** run it for a quick throwaway prototype with no governed lifecycle, to author the design system itself, or when there is no target repo, process, or artifact set to ground.

## Interaction principle

- If the user gave a clear process, artifact map, idea, and active phase, move straight to the next actionable grounding step.
- If the user gave little or nothing, use the [interview protocol](../references/interview-protocol.md) and run a short interview scoped to the current phase's missing input. Do not advance a phase until that phase's minimum input exists.
- After every step, state plainly: what happened, which host workflow step comes next, and what design judgment was injected.

## Artifact map

Before writing anything, establish the host workflow's artifact map:

| Generic role | Required mapping |
|---|---|
| durable memory | where the idea brief and durable context should live |
| governance artifact | constitution, principles, standards, rules, or quality bar file |
| spec artifact | where user stories, requirements, screens, and acceptance criteria live |
| clarification artifact | where open questions and resolved answers live |
| plan artifact | where stack, architecture, design-source, and constraints live |
| task artifact | where implementation tasks and gate references live |
| analysis/checklist artifact | where design checks or review verdicts live |
| implementation artifact | where build instructions or generated code references live |

If the workflow does not have one of these artifacts, mark it `none` with a reason. If more than one path could own a role, ask before writing.

## Gathering missing input with the interview

When a phase is missing its minimum input, run the [interview protocol](../references/interview-protocol.md) with an explicit objective and completion signal, then feed the captured answers into that phase:

- **Frame the idea**: objective = shape the raw idea into an idea brief; the user states the completion signal, and the outcome is saved to the mapped durable memory location.
- **Governance**: objective = the project's non-negotiable principles, quality bar, design strictness, and design source of truth.
- **Spec**: objective = the product slice and discovery line: who it is for, the core job, failure cost, and smallest useful surface.
- **Clarify**: objective = resolve design and scope ambiguities the spec left open.

The interview protocol asks one question at a time with suggested answers and registers each answer; this workflow turns those answers into grounded workflow contributions.

## Step 0 — Detect the workflow

1. Inspect the current folder and conversation for a named process, existing spec files, workflow docs, commands, and artifact folders.
2. Build the artifact map above.
3. If the process is absent or only aspirational, ask the user what spec-driven process they want to use and where durable artifacts should live.
4. If the process exists, read the mapped governance artifact, latest spec, latest plan/tasks, and any existing idea brief. Resume at the first phase missing design grounding.

## Step 1 — Frame the idea

This happens before governance or spec writing when no idea brief exists.

1. Take whatever the user said they want to build.
2. Run the interview protocol with objective = "shape this app idea enough to write governance and the first spec" and let the user state the completion signal.
3. Capture the outcome into an idea brief in the mapped durable memory location. Include: app in one line, primary user, core job, failure cost, smallest first slice, design source of truth, component library, constraints, and open questions.
4. When the outcome is met, stop and recommend the next host workflow step.

The idea brief lets later phases run with less re-asking.

## Step 2 — Seed governance

- Read the idea brief and mapped governance artifact.
- Apply [experience-governance-seed](experience-governance-seed.md) to draft or merge the design principles.
- Ask only if the brief leaves a governance-level non-negotiable genuinely undecided.
- Tell the user which host workflow step comes next.

## Step 3 — Specify or define

- Read the idea brief and active spec artifact.
- If a new feature's specifics are missing, run a short interview pass scoped to that feature.
- Apply the spec section of [experience-phase-contributions](experience-phase-contributions.md): inject the discovery line, primary action, must-show content, accessibility requirements, and per-screen acceptance criteria.
- Register the design source of truth when known.

## Step 4 — Clarify

- Apply the clarification section of [experience-phase-contributions](experience-phase-contributions.md): raise design ambiguities as questions.
- Do not let unknown user, failure cost, primary action, empty/error states, design source, or token source stay implicit.

## Step 5 — Plan

- Apply [experience-design-system-grounding](experience-design-system-grounding.md) to pin the component library, aesthetics source, token set, active mode, and Figma source.
- Record gaps rather than inventing missing tokens or components.

## Step 6 — Tasks, analysis, implementation

- **Tasks**: apply the task section of [experience-phase-contributions](experience-phase-contributions.md) so each screen task names components, states, gates, and a design-rationale task.
- **Analyze / review / checklist**: apply [experience-design-checklist](experience-design-checklist.md) to report each gate pass/fail/not-applicable against the governance artifact.
- **Implement**: load the [implementation guardrails](../references/implementation-guardrails.md) so code stays simple, surgical, and verifiable. Apply the registered aesthetics source through the component library or token layer. Embed [design-rationale-snippet](../references/design-rationale-snippet.md) as each screen lands.

## Quick-reference order

```text
detect workflow and artifact map       (once per project or when process changes)
frame idea via interview               (once, saved in durable memory)
seed governance                        (once per project, updated when principles change)
specify / define                       (per feature)
clarify                                (until blocking ambiguity is resolved)
plan                                   (design-system + aesthetics grounding)
tasks                                  (screen states + gate coverage)
analyze / review / checklist           (design gate verdicts)
implement                              (with implementation guardrails)
```

## Stop conditions

- Stop when the workflow or artifact map is ambiguous.
- Stop before writing to an existing governance artifact if merge intent is unclear.
- Stop at any phase whose minimum input is missing, and ask one question to get it.

## Output

- an artifact map
- a persisted idea brief
- the user guided to the correct next host workflow step
- design judgment injected per phase
- implementation grounded in the implementation guardrails
