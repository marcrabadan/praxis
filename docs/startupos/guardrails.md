# StartupOS — Guardrails

These rules are binding on every `/startupos-*` command. They are what separate StartupOS from a confident idea-fabrication machine. Each command restates the guardrails relevant to its stage; this is the canonical list.

## 1. Never invent market data

Do not state a market size, growth rate, conversion rate, price, or customer quote that you did not observe or source. If you don't have it, **say so and mark it an assumption** — never present a guess as a fact.

## 2. Separate facts, assumptions, estimates, and hypotheses

Every claim is labeled exactly one of:

| Label | Meaning | Requirement |
| ----- | ------- | ----------- |
| `[FACT]` | Observed or sourced | Must cite the source |
| `[ASSUMPTION]` | Believed, unverified | Stated plainly as unverified |
| `[ESTIMATE]` | Derived | Must show the derivation/method |
| `[HYPOTHESIS]` | Testable claim | Must have (or get) an experiment |

Blurring these is the single most common failure mode this module exists to prevent.

## 3. Require human approval before selecting the final idea

`/startupos-select` is a **hard human gate**. Ranking is advisory; the agent never self-selects. Selecting a never-validated or `KILL`'d idea requires an explicit, recorded human override.

## 4. Require human approval before exporting to Praxis

`/startupos-export-praxis` is a **hard human gate**. The agent never self-exports. Crossing into engineering spend is a human decision.

> **Pending is not approval.** A recorded recommendation is a proposal. Both gates require an explicit human *accept*.

## 5. Reject weak ideas

Killing ideas is the goal of the divergence phase, not a failure. An idea is weak — and should be rejected or sent back — if it lacks:

- **Real pain** (intense and/or frequent), or
- **Existing spend** / budget that already exists, or
- A plausible path to **recurring revenue**, or
- Genuine **AI leverage** (newly possible or 10× better), or
- Any **defensibility** (a credible moat thesis).

A `KILL` verdict in `/startupos-challenge` is a successful outcome.

## 6. Prefer strong business opportunities

Bias selection toward opportunities that combine: **real pain + existing spending + recurring revenue + AI leverage + defensibility.** The more of these an idea has — with evidence, not assumption — the stronger it ranks.

## 7. Always include risks and failure modes

No artifact is complete without its risks. An idea with an empty risk register has not been challenged. Every business case, architecture, and roadmap names its top failure modes and their early-warning signals.

## 8. Always include validation experiments before implementation

Demand is validated before supply is built. `/startupos-validate` is mandatory before `/startupos-select`, and the validation plan travels with the idea into the Praxis handoff so engineering builds on evidence, not hope.

## 9. Carry labels across the Praxis boundary

At export, `[FACT]` / `[ASSUMPTION]` / `[ESTIMATE]` labels are preserved. Never launder a StartupOS assumption into a Praxis "requirement" — Praxis must know what is proven versus assumed so it can spike the unknowns first.

## 10. Stay at the right altitude

StartupOS works at market/business/product/high-level-architecture altitude. It does **not** write production code, detailed designs, or test suites — that is Praxis's job after handoff. Respecting this boundary keeps the two systems clean and complementary.

---

## Why these guardrails

They encode the cheapest lessons in company-building: most ideas should die early; confident fabrication is worse than honest uncertainty; and the two most expensive mistakes — *building the wrong thing* and *building a thing nobody validated* — are exactly the two decisions StartupOS gates behind a human.
