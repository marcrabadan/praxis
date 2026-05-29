# Evaluate-Skill Workflow

Add or expand evals for a skill. Run when the user wants to verify a skill triggers correctly and produces correct output, or when promoting a skill to Tier 4 / Tier 5.

## Inputs

- Path to the skill folder.
- Optionally the `skill-brief.md` for trigger and output expectations.

## Two kinds of evals

| Kind | File | What it tests |
|------|------|---------------|
| Trigger evals | `evals/trigger-evals.json` | Whether the `description` routes the right queries to the skill and rejects near-misses. |
| Output evals | `evals/output-evals.json` | Whether the skill produces correct, verifiable output given a realistic prompt. |

Both are JSON files validated against [`schemas/eval.schema.json`](../../../factory/schemas/eval.schema.json).

## Steps for trigger evals

### 1. Draft 8–10 should-trigger queries

Make them realistic and specific. Include:

- formal phrasings;
- casual phrasings (typos, lowercase, abbreviations);
- queries that touch the skill's topic without naming its keywords;
- one or two uncommon-but-valid trigger cases.

Bad: `"do the thing"` — not specific.
Good: `"ok my boss just sent me a JSON token export from Figma at C:/exports/tokens-v3.json, can you turn it into a CSS variables file in src/styles/"`.

### 2. Draft 8–10 should-not-trigger queries

Make them **near-misses**, not obviously unrelated queries. The valuable negatives are queries that share keywords or concepts with the skill but actually need a different tool.

Bad (too easy): `"write a fibonacci function"` for a PDF skill.
Good (near-miss): `"I have a contract in PDF form that I need to scan and OCR for searchable text"` for a PDF-form-fill skill.

### 3. Save as `evals/trigger-evals.json`

Format:

```json
[
  { "query": "...", "should_trigger": true },
  { "query": "...", "should_trigger": false }
]
```

Pass the file through `validators/validate_skill.py <skill-path>` to confirm shape.

### 4. (Deferred to v2) Run the trigger eval loop

A future workflow will spawn the agent N times per query and measure the trigger rate against the description. For now, the eval set is documentation that a reviewer can use manually.

## Steps for output evals

### 1. Draft 2–5 test prompts

Each prompt should be a realistic user task that the skill would handle. For each prompt, capture:

- `id` — stable integer or string;
- `eval_name` — short descriptive name;
- `prompt` — the task as the user would say it;
- `expected_output` — a description (prose is fine) of what success looks like;
- `files` — input files the task depends on, if any;
- `assertions` — verifiable claims about the output.

### 2. Write assertions

Good assertions are objectively verifiable:

- "Output file `src/tokens.css` exists."
- "Output JSON has a `version` field equal to `2`."
- "Output markdown has exactly one H1 heading."

Avoid subjective assertions ("the writing is clear") unless the skill is explicitly subjective. For subjective skills, evaluate qualitatively in a review pass.

### 3. Save as `evals/output-evals.json`

Format:

```json
{
  "skill_name": "<slug>",
  "evals": [
    {
      "id": 1,
      "eval_name": "tokens-to-css-happy-path",
      "prompt": "...",
      "expected_output": "...",
      "files": ["evals/fixtures/tokens-v3.json"],
      "assertions": [
        { "text": "..." }
      ]
    }
  ]
}
```

If a fixture file is referenced, place it under `evals/fixtures/` and commit it.

### 4. Validate

Run:

```bash
python .claude/factory/validators/validate_skill.py <skill-path>
```

Confirm the eval files parse and conform to `schemas/eval.schema.json`.

## Stop conditions

The evaluate workflow is done when:

- `evals/trigger-evals.json` contains at least one positive and one negative case;
- `evals/output-evals.json` exists (or is explicitly skipped for a non-code skill);
- `validators/validate_skill.py` passes;
- the user has confirmed the evals are realistic.

## Deferred capabilities

The following are documented as v2 / autoresearch-loop work and are not part of this workflow yet:

- Running the trigger evals through a real agent and measuring trigger rate;
- Running the output evals through the skill and grading outputs against assertions;
- Comparing two versions of a skill (blind A/B);
- The full description-optimization loop (`run_loop.py` pattern).

For now, eval files serve as documentation a human reviewer (or a future automated runner) can use.
