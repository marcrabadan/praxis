<!--
StartupOS template — architecture.md
Filled by /startupos-architecture. STARTUP ALTITUDE: high-level shape + key decisions, not detailed design.
Praxis's software-architect owns ADRs and detailed design after handoff.
-->

# Architecture (high-level) — <Idea name>

- **Slug:** `<slug>` · **Updated:** <YYYY-MM-DD>

## System context (C4 L1)

The product, its users, and the external systems it touches. A short narrative or a Mermaid diagram.

```mermaid
%% optional context diagram
```

## Container view (C4 L2)

Major components and how they communicate. One line of rationale per boundary.

| Component | Responsibility | Build / Buy / Reuse |
| --------- | -------------- | ------------------- |

## AI strategy

- **Where AI creates leverage:** <…>
- **Approach:** LLM / RAG / fine-tune / classic ML / agentic — and why. [ASSUMPTION|HYPOTHESIS]
- **Data needed:** <…> (and how it's sourced)
- **Evaluation & guardrails:** how quality is measured and unsafe output prevented
- **Cost & latency posture:** rough budget per request [ESTIMATE]

## Build vs buy

For each major capability, name the off-the-shelf option before any custom build. Flag every custom-build decision.

## Data & privacy

What data is collected, where it lives, retention, and the compliance surface (PII/GDPR/etc.). Flagged by the Legal/Compliance Reviewer.

## Key NFRs & risks (top 5)

| # | Risk / NFR | Severity | Mitigation or spike |
| - | ---------- | -------- | ------------------- |

## Feasibility verdict

Can a small team ship the MVP? The riskiest technical unknown and the spike that retires it.

## Handoff note to Praxis

This is L1/L2 only. `/praxis:architect` takes ownership of detailed design, ADRs, and NFR validation.
