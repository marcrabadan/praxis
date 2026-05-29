# Product Owner Practices

Core practices for owning a product backlog, prioritizing work, and maximizing delivered value across the SDLC.

---

## Backlog ownership

- The PO owns the backlog: only the PO adds, removes, and reorders items. Engineers and stakeholders may propose; the PO decides.
- The backlog is a living artifact. Stale items older than two sprints without refinement activity should be challenged or removed.
- Maintain a three-layer view: (1) ready items for the next one to two sprints, (2) refined but not ready for the next two to six weeks, (3) raw ideas beyond that.
- Express backlog items as outcomes wherever possible. "User can complete checkout without re-entering shipping address on return visit" beats "Add saved-address feature."
- Keep epics at the theme/outcome level. Break epics into stories only when the team is within two sprints of working on them.

## Writing backlog items

- Use the role/goal/benefit format as a default: "As a [role] I want [goal] so that [benefit]."
- Switch to an outcome-oriented format when the solution is unknown: "Reduce cart abandonment at the address step by 15%."
- Every story must have acceptance criteria before refinement. Write them as testable conditions — Given/When/Then or a bulleted list of observable outcomes.
- Include non-functional requirements (performance, accessibility, security) explicitly in acceptance criteria, not as implied expectations.
- A story is not a task list. It describes the value and the boundary; the team decides the tasks.
- Spike stories are time-boxed investigations. State the question to be answered and the timebox; the output is knowledge, not shippable code.

## Prioritization frameworks

Use the framework that matches the information available and the decision at hand. Apply one framework per prioritization session — mixing frameworks in a single ranking produces noise.

### MoSCoW
**Use when:** the team needs a quick alignment on what ships in a fixed release and what does not. Best for release scoping, MVP definition, or stakeholder negotiation.
- Must Have: the release fails without this. Non-negotiable.
- Should Have: high value; will be missed if absent, but a workaround exists.
- Could Have: nice to have; omit if time pressure arises.
- Won't Have (this time): explicitly out of scope for this release.
- Rule: if more than 60% of scope is "Must Have," the prioritization is not doing its job. Force harder choices.

### RICE
**Use when:** the team has enough data to estimate reach, impact, confidence, and effort. Best for mid-backlog ranking where multiple features compete.
- Score = (Reach × Impact × Confidence) / Effort.
- Reach: number of users or events per period affected.
- Impact: ordinal scale (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal).
- Confidence: percentage (100% = data-backed, 80% = reasonable assumption, 50% = mostly guessing).
- Effort: person-months or normalized story points.
- Higher score = higher priority. Surface assumptions explicitly — a high-confidence low-reach item can outrank a low-confidence high-reach one.

### WSJF (Weighted Shortest Job First)
**Use when:** the team is working in SAFe or needs to account for time-criticality and risk explicitly. Best for PI planning, program-level backlogs, and items with regulatory or market-timing pressure.
- Score = Cost of Delay / Job Duration.
- Cost of Delay = User/Business Value + Time Criticality + Risk Reduction / Opportunity Enablement.
- Use a relative Fibonacci scale (1, 2, 3, 5, 8, 13, 20) for each component.
- Smaller job with the same Cost of Delay always scores higher — short items rise to the top naturally.

### Kano model
**Use when:** the team is deciding which features to invest in for customer delight, or distinguishing table-stakes from differentiators. Best for product discovery, feature selection, and roadmap strategy.
- Basic (Must-Be): absence causes dissatisfaction; presence is expected. Invest minimally — just enough.
- Performance (Linear): more is better; directly correlates with satisfaction. Invest proportionally.
- Delighter (Exciter): unexpected; creates delight. Invest strategically for differentiation.
- Indifferent: users do not care. Cut or defer.
- Rule: validate Kano classification with actual user research, not stakeholder assumption.

### Value-vs-Effort (2×2)
**Use when:** the team needs a fast visual alignment with limited data. Best for quick grooming sessions, workshops, and stakeholder conversations.
- Plot items on a 2×2 matrix: high/low value on the Y-axis, high/low effort on the X-axis.
- Quick wins (high value, low effort): do first.
- Strategic bets (high value, high effort): plan carefully; break into smaller increments.
- Fill-ins (low value, low effort): do only if capacity permits.
- Reconsider (low value, high effort): cut or park indefinitely.
- Limitation: "value" and "effort" must be defined before plotting or the matrix is noise.

---

## Sprint goals and Definition of Done

- A sprint goal is a single sentence expressing the business outcome the team will achieve. It is not a list of stories; it is the reason those stories exist.
- The sprint goal is committed by the team, not assigned by the PO. The PO proposes; the team accepts or negotiates.
- The Definition of Done (DoD) defines the quality bar that applies to every item marked complete. It is not story-specific; it is team-wide.
- A DoD typically includes: code reviewed and merged, automated tests passing, accessibility criteria met, deployed to staging, product owner has accepted.
- The PO does not override the DoD. If an item does not meet the DoD, it is not done — it rolls over or is explicitly cut with documented tech debt.

---

## Roadmapping and release planning

- A roadmap communicates direction and intent, not a delivery schedule. Express themes and outcomes over a rolling three- to twelve-month horizon; avoid committing to specific features on specific dates beyond the next one to two quarters.
- Use a now/next/later structure as the default. "Now" = committed and in flight. "Next" = shaped and sequenced. "Later" = directional, subject to change.
- Release plans are short-horizon commitments (one to two sprints) that slice the roadmap into deployable increments. Every release plan must state: what ships, what the success metric is, and what is explicitly excluded.
- Communicate roadmap confidence levels explicitly: committed, likely, possible, exploring. Stakeholders who conflate "likely" with "committed" create trust debt.
- Review the roadmap at least once per quarter against actual outcomes. Remove items that evidence has invalidated.

---

## Outcome-oriented goals

- OKRs (Objectives and Key Results): the Objective states a qualitative direction; Key Results are measurable outcomes, not outputs. "Launch the new checkout flow" is an output. "Reduce checkout abandonment rate from 42% to 28%" is an outcome.
- A north-star metric is the single leading indicator most correlated with long-term product value. Align sprint goals and roadmap themes to movement on the north-star metric.
- Success criteria for a story or epic should be defined before work starts, not after. If the team cannot agree on what "done and valuable" looks like, the item is not ready to be worked.
- Avoid vanity metrics (page views, registered users) when engagement, retention, or conversion metrics are available.

---

## Stakeholder alignment and saying "no"

- Stakeholders propose; the PO decides. The PO is accountable for the backlog order, not obligated to implement every request.
- Say "no" with evidence: cite the framework score, the opportunity cost, or the misalignment with the current objective. "No, because X is five times the effort for half the reach of Y, which also serves the same user segment" is a defensible answer.
- Surface trade-offs explicitly: "If we add this, we push the fraud-detection story out of the sprint. Which do you want?" Never absorb scope silently.
- Differentiate between stakeholder wants and user needs. Use research, data, and direct user feedback to anchor decisions.
- Maintain a "parking lot" — a visible, acknowledged list of deferred items. Stakeholders are more accepting of "not now" when they can see the item is recorded and will be revisited.

---

## Story splitting

Thin vertical slices deliver working software end-to-end for a narrow use case. The following patterns apply to most stories:

- **By workflow step:** split a complete flow into the individual steps (e.g., split "user can manage addresses" into "add address," "edit address," "delete address").
- **By data variation:** deliver the happy path first; add edge cases and error states as separate stories.
- **By user role:** implement for the most common role first; extend to other roles in follow-on stories.
- **By interface:** deliver the core logic and API first; add the UI layer as a separate story.
- **By acceptance criterion:** if a story has five acceptance criteria that represent independent value, split them.
- **Spike first:** if a story is too uncertain to size, create a time-boxed spike to reduce uncertainty before committing.
- Anti-pattern: splitting horizontally by layer (backend story, frontend story, QA story). This produces partial work that cannot be accepted until all layers are complete — it is task management, not story splitting.

---

## Acceptance of completed work

- Acceptance is the PO's responsibility. Engineers do not accept their own work.
- Acceptance is based on the acceptance criteria written before the sprint, not on new requirements discovered at demo time.
- If new requirements surface at acceptance, create a new backlog item rather than expanding the definition of done retroactively.
- A story that meets all acceptance criteria but fails the DoD is not accepted.
- Acceptance should happen as soon as a story is done — not batched to the end of the sprint. Late acceptance batching creates end-of-sprint risk.
- Document acceptance with a brief note or status change. "Accepted 2026-05-29 — all criteria met, deployed to staging, smoke-tested" is sufficient.
