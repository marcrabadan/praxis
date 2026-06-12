# Prompting Best Practices

How to write the **instruction body** of a skill — `SKILL.md` sections, workflows, and references — for current Claude models. [description-writing.md](description-writing.md) covers the routing surface; this file covers everything the agent reads *after* the skill triggers.

The premise behind every practice here: modern Claude models follow instructions **literally and closely**. Guidance written to overcome the reluctance or sloppiness of older models now backfires — it overtriggers, over-constrains, and crowds out the model's own judgment. Write for a capable reader, not a reluctant one.

## 1. State the goal, not the steps

Over-prescriptive prompts reduce output quality on current models. Prefer stating the goal, the constraints, and what "done" looks like over enumerating how to get there.

**Bad** (step-enumeration where judgment would do better):

> 1. First, read the file. 2. Then identify the three most important functions. 3. For each function, write one sentence. 4. Combine the sentences into a paragraph. 5. Check the paragraph for clarity.

**Good** (goal + constraints + done-state):

> Summarize what this module does in one paragraph a new team member could act on. Cover the load-bearing functions; skip boilerplate.

Reserve numbered steps for procedures that are **genuinely deterministic** — run this script, check this exit code, write this file. That is what `workflows/` are for, and numbered procedures there are correct. The anti-pattern is scripting the model's *thinking*, not scripting its *mechanics*.

When a model upgrade lands, re-test skills with their step scaffolding removed — instructions that helped an older model often hold a newer one back.

## 2. Calibrate the language — no shouting, give the reason

`CRITICAL:`, `YOU MUST`, `ALWAYS`, `If in doubt, use X` were written to overcome old-model reluctance. Current models follow them literally, so they overtrigger.

| Instead of | Write |
|---|---|
| `CRITICAL: You MUST use this tool when...` | `Use this tool when...` |
| `ALWAYS validate before returning` | `Validate before returning — unvalidated output has shipped broken skills twice` |
| `If in doubt, use [tool]` | *(delete — name the actual condition, or trust the model)* |

A rule the model can't see the reason for gets ignored or misapplied over time; a rule with its reason attached gets generalized correctly. This is anti-pattern #15 in [anti-patterns.md](anti-patterns.md) — the fix is always the same: replace the volume with the reasoning.

## 3. Put trigger conditions where decisions are made

Saying a capability *exists* is not enough — say **when** to reach for it. Current models are conservative about expensive or optional capabilities (subagents, scripts, extra reference files) and won't use them unless reasonably sure they apply. Prescriptive "use this when…" conditions measurably raise correct-use rates.

- In the **description**: trigger phrases for routing ([description-writing.md](description-writing.md)).
- In **script and workflow listings**: the condition, not just the purpose — `Run scripts/validate.py before declaring done` beats `validate.py — validates the skill`.
- In **reference listings**: when to read each file — `Read references/edge-cases.md when the input is a scanned PDF` beats a bare link list.

## 4. Show positive examples, don't stack negative instructions

One worked example of the desired output outperforms a list of "do not" rules. Models mimic what they see more reliably than they avoid what they're told. When a skill keeps producing the wrong shape, add a Good/Bad pair (as in this file and [description-writing.md](description-writing.md)) rather than another prohibition.

Keep negative instructions for the few cases where the failure is silent or irreversible — and attach the reason (§2).

## 5. Give the intent, not just the task

The model performs better when it knows **why** the output is needed and who it is for. A skill body that says "produce a test plan" leaves the model to guess depth, format, and audience; "produce a test plan the QA lead can hand to a junior tester to execute unsupervised" pins all three. The interview captures purpose and audience — make sure they survive into the skill body instead of dying in `skill-brief.md`.

## 6. Front-load the full specification

For long or multi-step work, current models do markedly better with the complete task specification up front than with requirements drip-fed across turns. In skill terms:

- A workflow's **Inputs** section should name everything the procedure needs before step 1 — not reveal a required input at step 4.
- **Output expectations** and **stop conditions** belong in `SKILL.md` where the model sees them before starting, not implied at the end of a workflow.

## 7. Lead with the outcome in output formats

When a skill defines an output template, structure it so the **conclusion comes first** and supporting detail follows — the reader (human or downstream agent) should get the answer without scanning. A review report that opens with the verdict beats one that builds to it. Prefer selectivity (drop what doesn't change the reader's next action) over compression (fragments, abbreviations, arrow chains) — clarity beats brevity when they conflict.

## 8. Don't carry stale model workarounds

Scaffolding written to patch an old model's gaps becomes dead weight or active harm on newer ones. When reviewing a skill, flag instructions of these shapes and test the skill with them removed:

- forced progress narration — "after every N tool calls, summarize progress" (current models narrate appropriately on their own);
- forced verbal self-checks — "double-check the layout before returning" for tasks the model now verifies natively;
- aggressive triggering language (§2);
- step-enumeration of judgment work (§1).

This is the prompt-level twin of anti-pattern #13 (time-sensitive instructions): both embed an expiry date the skill will silently outgrow.

## Self-check

Before declaring a skill body done:

- Does every rule either carry its reason or have an obvious one?
- Are there zero ALL-CAPS imperatives left that a plain verb would cover?
- Could each numbered procedure be executed by a script — and if not, is it really a procedure, or scripted judgment?
- Does every capability listing (script, workflow, reference) say *when* to use it?
- Is there at least one positive example for any output the skill must shape?
- Do output templates lead with the outcome?
