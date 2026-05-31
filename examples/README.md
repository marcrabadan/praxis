# Examples — what the experts produce

Sample transcripts showing what each praxis entry point looks like in practice: the
prompt you type, and a representative response. They're here so you can judge the
output *before* installing anything, and so new teammates can see the house style.

> **These are illustrative.** Each transcript is a hand-written, representative example of
> the shape and altitude of a real response — not a verbatim capture, and not a promise of
> exact wording. Real output adapts to your codebase, constraints, and the surrounding
> conversation. They follow the formats defined by each skill's `references/` (ADR shape,
> review severities, INVEST + Gherkin, STRIDE, …).

| Sample | Entry point | What it demonstrates |
| ------ | ----------- | -------------------- |
| [new-feature.md](new-feature.md) | `/new-feature` | The core six experts run in lifecycle order → one consolidated plan. |
| [architect-adr.md](architect-adr.md) | `/architect` | A single design decision captured as an ADR. |
| [analyst-user-stories.md](analyst-user-stories.md) | `/analyst` | A vague idea turned into INVEST user stories with Gherkin acceptance criteria. |
| [review-changes.md](review-changes.md) | `/review-changes` | A diff reviewed into severity-tagged, didactic findings. |
| [security-threat-model.md](security-threat-model.md) | `/security` | An endpoint threat-modeled with STRIDE and concrete mitigations. |

Most samples share one running feature — **saved payment methods at checkout** — so you can
see the same problem move through requirements, architecture, build, and review.

To reproduce any of these, install the experts ([Install & integrate](../README.md#install--integrate))
and type the prompt shown at the top of each file. In plugin form the commands are
namespaced (`/praxis:new-feature`, `/praxis:architect`, …).
