---
description: StartupOS — record the human's selection of the single idea to take forward into business design. A mandatory human-in-the-loop approval gate.
argument-hint: <the idea slug to select>
---

Adopt the **StartupOS** selection posture — the **CEO Agent** facilitates, but **the human decides** (see [docs/startupos/agents.md](../../../docs/startupos/agents.md)). This is the **Select** stage — the **first hard human gate** in the lifecycle.

The idea proposed for selection:

$ARGUMENTS

## Purpose

Commit, with explicit human approval, to **one** idea to carry into the business-case → PRD → architecture → roadmap → handoff chain. This is a decision, not a suggestion.

## Input

- The ranking from `/startupos:rank` (`memory/startupos/decisions/ranking-<date>.md`).
- The candidate's full memory trail (research, validation, challenge, risks).

## Workflow

1. **Present the case for selection.** Summarize the chosen idea: thesis, evidence strength, top risks, validation status, and why it ranks where it does. Be honest about what is still `ASSUMPTION`.
2. **Require explicit human approval.** Use `AskUserQuestion` to ask the human to confirm `SELECT | PICK ANOTHER | NOT YET`. **Do not proceed on a guess** — this gate is mandatory (guardrail).
3. **On SELECT:** record the decision with its rationale and the evidence it rests on. Note the open assumptions the human is knowingly accepting.
4. **On PICK ANOTHER / NOT YET:** record why and route back to `/startupos:rank`, `/startupos:research`, or `/startupos:validate`.

## Output / expected generated files

- `memory/startupos/decisions/selection-<slug>.md` — the selected idea, the human approver, date, rationale, accepted open assumptions, and the rejected alternatives.
- A chat summary confirming the selection and the next command.

## Guardrails

- **Require human approval before selecting the final idea** — this command never self-approves.
- Selecting an idea that was never validated or was `KILL`'d in challenge requires an explicit human override, recorded as such.
- Carry forward the assumption/fact separation — do not let selection launder assumptions into facts.

## Approval gates

**This is the gate.** Selection is blocked until the human explicitly confirms. Pending is not approval.

## Next

`/startupos:business-case <slug>` to design the business around the selected idea.
