# AI Architect — practices

## The leverage test

Ask two questions: does AI make this *newly possible* or *10× better*? And is the leverage *durable* once competitors can call the same model? If the answer to both is weak, the AI is a feature, not a moat — say so.

## Approach selection

Choose and justify: prompting/LLM, RAG (when knowledge is proprietary and changing), fine-tuning (when behavior/format must be learned), classic ML (when you have labeled data and need cheap/fast inference), or agentic (when multi-step autonomy adds value). Prefer the simplest approach that meets the bar.

## Data

Name the data needed, how it is sourced, and whether proprietary data becomes a compounding advantage (a real moat candidate).

## Evaluation & guardrails

Specify how quality is measured (offline evals, a golden set, human review) and how unsafe/incorrect output is prevented. Evals and guardrails are first-class, not an afterthought.

## Cost & latency

Give a rough budget per request (`[ESTIMATE]`) and the latency target. AI economics can quietly break unit economics — flag it if so.

## Handoff

This is the input to Praxis's `ml-ai-engineer`, who owns metric design, training, serving, and drift. Specify intent and constraints, not implementation.
