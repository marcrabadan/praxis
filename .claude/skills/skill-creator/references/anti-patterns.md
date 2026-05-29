# Anti-Patterns

Common failures when creating skills, and the correct alternatives. If you find yourself doing one of these, stop and refactor.

## 1. Skipping the interview

**Symptom.** Agent writes a skill folder without ever asking about purpose, audience, or trigger context. The result fits the agent's guess about the user's intent, not the user's actual intent.

**Fix.** Run [../workflows/interview-intake.md](../workflows/interview-intake.md) first. One question at a time, with suggested answers.

## 2. Vague description

**Symptom.** `description: Helps with X.` or `description: A skill for X.`

**Fix.** Read [description-writing.md](description-writing.md). Use the template: concrete verbs + "use when" + multiple realistic trigger phrases.

## 3. Skill too broad

**Symptom.** One skill is supposed to handle PDF, Excel, CSV, JSON, and YAML "because they're all data files."

**Fix.** Split by domain. Each skill owns a narrow trigger surface. If a skill's description has to enumerate five unrelated file types, it is two skills wearing one hat.

## 4. Skill too narrow

**Symptom.** Three skills each handle one variant of the same task ("PDF reader v1", "PDF reader v2 with OCR", "PDF reader for forms"). Trigger surface collides; user has to pick.

**Fix.** Collapse into one skill with workflows or conditional logic.

## 5. Long body, empty references

**Symptom.** `SKILL.md` is 800 lines; `references/` exists but is empty.

**Fix.** Move long knowledge sections into `references/rules.md`, `references/examples.md`, etc. Link from `SKILL.md` with a one-line pointer per file.

## 6. Empty workflows

**Symptom.** `workflows/default.md` contains only "TODO: write workflow" or boilerplate.

**Fix.** Either fill it with a real numbered procedure, or delete the file and demote the skill from Tier 3 to Tier 2.

## 7. Scripts that punt to the LLM

**Symptom.** `scripts/validate.py` is a Python file whose body is `print("Please check this manually")`.

**Fix.** Either implement the check deterministically or remove the script. A script that does nothing is worse than no script — it implies a check that does not exist.

## 8. Fake evals

**Symptom.** `evals/trigger-evals.json` contains entries like `{"query": "do the thing", "should_trigger": true}`.

**Fix.** Trigger evals must be realistic, specific user queries. Include file names, contexts, casual phrasing, typos. Negative cases must be near-misses, not obviously unrelated queries.

## 9. Speculative architecture

**Symptom.** A new skill has `agents/`, `assets/`, `reports/`, and a custom subagent for grading — and was triggered three times total.

**Fix.** Start at the lowest reasonable tier. Promote when the harness earns its cost through measurable improvement, not anticipation.

## 10. Production code in this repo

**Symptom.** A skill's `scripts/` directory contains a working React component or backend handler intended to be used in production.

**Fix.** Move the production code to its product repo. Keep only examples, fixtures, generators, validators, and patches here.

## 11. Hard-coded paths

**Symptom.** `SKILL.md` says "read C:\Users\me\thing.md" or "save to /home/user/output".

**Fix.** Use repo-relative paths. Make output paths configurable via interview / script arguments.

## 12. Windows-style backslashes in links

**Symptom.** Markdown links like `[reference](references\rules.md)`.

**Fix.** Always use forward slashes in markdown links. The validator flags backslashes in links.

## 13. Time-sensitive instructions

**Symptom.** "If it's before August 2026, use the old API."

**Fix.** Use a "current method" section and a collapsible "deprecated" section. Do not embed dates the skill will outgrow.

## 14. Inconsistent terminology

**Symptom.** The same concept is called "endpoint" in one paragraph, "URL" in the next, "route" in a third.

**Fix.** Pick one term. Use it everywhere. Define it once in `references/glossary.md` if it is not obvious.

## 15. MUST and NEVER without reason

**Symptom.** `SKILL.md` is full of ALWAYS, MUST, NEVER, CRITICAL — but does not explain why.

**Fix.** Replace shouting with the reasoning. Modern LLMs follow well-reasoned instructions; they ignore unexplained ones over time.

## 16. Mixed concerns in one skill

**Symptom.** A skill both teaches the agent what good UX writing looks like (knowledge) and runs a JSON-to-CSS conversion (codegen).

**Fix.** Split. The trigger contexts are different and the tier requirements are different.

## 17. Outputs the agent can't validate

**Symptom.** A skill produces a PDF or a binary blob and has no way to check whether it is correct.

**Fix.** Either add a validator (open the file, check structure) or add an explicit "ask the user to verify" stop condition. Never silently assume success.

## 18. Skipping validation

**Symptom.** The agent declares the skill done without running `scripts/validate_skill.py`.

**Fix.** Validation is part of the stop condition, not an optional extra. Run it.
