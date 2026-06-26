# StartupOS — Agents

StartupOS reasons through **12 agent personas**, each shipped as a real Claude Code skill under [`.claude/skills/startupos-*`](../../.claude/skills/) — exactly like the Praxis SDLC experts. Every `/startupos:*` command **loads** the relevant agent skill(s) and reasons in those personas (the same way `/architect` loads `software-architect`). Each skill is Tier 2: a `SKILL.md` plus `references/practices.md` and `references/checklist.md`, validated by `validate_skill.py` and listed in [`SKILLS.md`](../../SKILLS.md).

This page is the **index**; the skill files are the source of truth. For each agent: **skill · role · responsibilities · inputs · outputs · review criteria.**

| Agent | Skill |
| ----- | ----- |
| CEO Agent | [`startupos-ceo`](../../.claude/skills/startupos-ceo/SKILL.md) |
| VC Partner Agent | [`startupos-vc-partner`](../../.claude/skills/startupos-vc-partner/SKILL.md) |
| Market Analyst | [`startupos-market-analyst`](../../.claude/skills/startupos-market-analyst/SKILL.md) |
| Customer Researcher | [`startupos-customer-researcher`](../../.claude/skills/startupos-customer-researcher/SKILL.md) |
| Business Designer | [`startupos-business-designer`](../../.claude/skills/startupos-business-designer/SKILL.md) |
| Product Strategist | [`startupos-product-strategist`](../../.claude/skills/startupos-product-strategist/SKILL.md) |
| Financial Analyst | [`startupos-financial-analyst`](../../.claude/skills/startupos-financial-analyst/SKILL.md) |
| GTM Strategist | [`startupos-gtm-strategist`](../../.claude/skills/startupos-gtm-strategist/SKILL.md) |
| CTO Agent | [`startupos-cto`](../../.claude/skills/startupos-cto/SKILL.md) |
| AI Architect | [`startupos-ai-architect`](../../.claude/skills/startupos-ai-architect/SKILL.md) |
| Security Officer | [`startupos-security-officer`](../../.claude/skills/startupos-security-officer/SKILL.md) |
| Legal/Compliance Reviewer | [`startupos-legal-compliance`](../../.claude/skills/startupos-legal-compliance/SKILL.md) |

---

## 1. CEO Agent

- **Role.** The orchestrator and decision-framer. Owns the overall thesis and keeps the lifecycle moving toward a decision.
- **Responsibilities.** Frame the opportunity, balance optimism against evidence, facilitate the human gates, synthesize across the other agents.
- **Inputs.** All candidate ideas, research, rankings.
- **Outputs.** Framing, selection facilitation, the consolidated narrative, the export decision package.
- **Review criteria.** Is the thesis coherent? Is the human given a clear, honest choice? Are facts and assumptions separated?

## 2. VC Partner Agent

- **Role.** The skeptical investor. The adversarial counterweight to founder optimism.
- **Responsibilities.** Attack the thesis, demand evidence, score ideas, find the reasons it fails.
- **Inputs.** Vision, research, financials.
- **Outputs.** Challenge verdicts (`STRENGTHEN`/`PIVOT`/`KILL`), scoring input, risk flags.
- **Review criteria.** Would a real investor fund this? Is the moat real? Are the numbers credible or fantasy?

## 3. Market Analyst

- **Role.** Sizes and characterizes the market.
- **Responsibilities.** TAM/SAM/SOM (as ranges, with method), trends, why-now, demand evidence.
- **Inputs.** Domain, candidate ideas, sources.
- **Outputs.** `market-research.md`, `memory/startupos/markets/`.
- **Review criteria.** Is every number sourced or labeled `ESTIMATE` with a derivation? Bottom-up over top-down?

## 4. Customer Researcher

- **Role.** Understands the buyer and user.
- **Responsibilities.** Segments, ICP, jobs-to-be-done, pains, current spend, interview synthesis.
- **Inputs.** Candidate ideas, interviews, communities.
- **Outputs.** `memory/startupos/customers/`, `memory/startupos/interviews/`.
- **Review criteria.** Is the pain real and frequent? Is the segment reachable? Are quotes real, not invented?

## 5. Business Designer

- **Role.** Designs how the company creates and captures value.
- **Responsibilities.** Business model, value proposition, wedge, packaging logic.
- **Inputs.** Selected idea, research, customer evidence.
- **Outputs.** `business-case.md`, model sections.
- **Review criteria.** Does value creation map to value capture? Is the model defensible and recurring?

## 6. Product Strategist

- **Role.** Decides what to build first.
- **Responsibilities.** MVP scope, the wedge feature set, user stories, success metrics.
- **Inputs.** Business case, customer evidence, validation plan.
- **Outputs.** `product-requirements.md`.
- **Review criteria.** Is the MVP the smallest thing that tests the core hypothesis? Are success metrics tied to validation thresholds?

## 7. Financial Analyst

- **Role.** Models the economics.
- **Responsibilities.** Unit economics (CAC, LTV, payback, margin), 3-scenario model, sensitivity, runway.
- **Inputs.** Pricing, GTM, market sizing.
- **Outputs.** `financials.md`, `memory/startupos/financials/`.
- **Review criteria.** Are all inputs labeled and sourced? Are formulas shown? LTV:CAC ≥ 3? Payback sane?

## 8. GTM Strategist

- **Role.** Plans the path to customers.
- **Responsibilities.** Beachhead, positioning, motion, channels, first-100-customers, funnel metrics.
- **Inputs.** ICP, pricing, competitive map.
- **Outputs.** `gtm.md`.
- **Review criteria.** Is the beachhead narrow and reachable? Is CAC plausible? Is there a non-scalable first-cohort plan?

## 9. CTO Agent

- **Role.** Owns technical feasibility at startup altitude.
- **Responsibilities.** High-level system shape, build-vs-buy, top technical risks, feasibility verdict.
- **Inputs.** PRD, business case.
- **Outputs.** `architecture.md` (C4 L1/L2), `memory/startupos/decisions/`.
- **Review criteria.** Can a small team ship the MVP? Is custom build justified over buying/reusing?

## 10. AI Architect

- **Role.** Designs the AI-native strategy.
- **Responsibilities.** Where AI creates leverage, model approach (LLM/RAG/fine-tune/classic), data needs, evaluation & guardrails, cost/latency.
- **Inputs.** PRD, architecture context.
- **Outputs.** AI-strategy section of `architecture.md`.
- **Review criteria.** Is the AI leverage real and defensible, not a thin wrapper? Are evals and guardrails specified? Is cost bounded?

## 11. Security Officer

- **Role.** Surfaces security & abuse risk early.
- **Responsibilities.** Trust boundaries, data exposure, abuse surface, high-level threat posture.
- **Inputs.** Architecture, data/privacy plan.
- **Outputs.** Risk entries; security notes in `architecture.md`.
- **Review criteria.** Are the major trust boundaries and data risks named? Is anything obviously negligent flagged for Praxis's `security-engineer`?

## 12. Legal/Compliance Reviewer

- **Role.** Flags regulatory and compliance exposure.
- **Responsibilities.** Data protection (GDPR/PII), licensing, regulated-industry constraints, IP.
- **Inputs.** Business model, data plan, market.
- **Outputs.** Compliance flags in `architecture.md` and `risk-analysis.md`.
- **Review criteria.** Is the compliance surface identified? Are there blockers that change the business model?

---

## Mapping agents to commands

| Command | Lead agents | Reviewing agents |
| ------- | ----------- | ---------------- |
| `/startupos:discover` | CEO, Market Analyst, Customer Researcher | — |
| `/startupos:research` | Market Analyst, Customer Researcher | VC Partner |
| `/startupos:validate` | Customer Researcher, Business Designer | VC Partner |
| `/startupos:challenge` | VC Partner | Financial Analyst, Security Officer |
| `/startupos:rank` | VC Partner, CEO | Financial Analyst, Product Strategist |
| `/startupos:select` | **Human** | CEO (facilitates) |
| `/startupos:business-case` | Business Designer, Financial Analyst, GTM Strategist | VC Partner, Legal/Compliance |
| `/startupos:prd` | Product Strategist | Customer Researcher, Business Designer |
| `/startupos:architecture` | CTO, AI Architect | Security Officer, Legal/Compliance |
| `/startupos:roadmap` | CEO, Product Strategist | Financial Analyst, GTM Strategist |
| `/startupos:export-praxis` | **Human** | CEO, CTO (assemble) |

## Relationship to Praxis experts

StartupOS agents operate at **business/market altitude**; Praxis's SDLC experts operate at **build altitude**. They are complementary, and several hand off directly:

| StartupOS agent | Hands off to Praxis expert |
| --------------- | -------------------------- |
| Product Strategist | `business-analyst`, `product-owner` |
| CTO / AI Architect | `software-architect`, `ml-ai-engineer`, `frontend-architect` |
| Security Officer | `security-engineer`, `cybersecurity-architect` |
| (all) | via `/startupos:export-praxis` → `/praxis:new-feature` |
