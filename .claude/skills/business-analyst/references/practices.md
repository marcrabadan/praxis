# BA Practices

Core Business Analyst techniques and principles for eliciting, structuring, and validating requirements across the SDLC.

---

## 1. Requirements elicitation techniques

Use the technique that matches the situation. Do not default to interviews alone.

### Interviews
- Conduct one-on-one sessions with individual stakeholders to surface expectations, constraints, and domain knowledge.
- Prepare open-ended questions ("What does success look like?") alongside specific probing questions ("What happens when the payment fails?").
- Distinguish between what the stakeholder *wants* (desires) and what they *need* (requirements). Challenge assumptions politely.
- Record verbatim quotes for ambiguous or contested points; paraphrase back for confirmation before moving on.

### Workshops (JAD/RAD sessions)
- Bring multiple stakeholders together to resolve conflicts in real time and build shared understanding.
- Use a neutral facilitator. The BA facilitates; product owners and subject-matter experts contribute.
- Timebox each topic. Capture decisions, open items, and parking-lot items separately.
- Workshops are most efficient when a draft artifact (e.g. a rough process map or a set of proto user stories) exists for participants to react to.

### Observation (contextual inquiry)
- Watch users perform the actual task in their real environment rather than describing it from memory.
- Note workarounds, informal processes, and shadow systems that stakeholders rarely mention in interviews.
- Take timestamped notes. Distinguish observed behavior from inferred intent.
- Observation is especially valuable for as-is process documentation and for discovering non-functional requirements (response-time expectations, error frequency).

### Document analysis
- Review existing artifacts: policy documents, existing system specs, data dictionaries, regulatory texts, and training materials.
- Identify requirements implied by existing workflows even if never explicitly stated.
- Flag inconsistencies between documents. Do not silently pick one version; surface the conflict.
- Map each requirement extracted from a document to its source (document name, section, page).

### Prototyping
- Use low-fidelity wireframes or mock data flows to elicit feedback on gaps the stakeholder cannot articulate in the abstract.
- Treat prototypes as a requirements-discovery tool, not a commitment to the final design.
- Capture requirements that emerge from prototype reviews before the prototype itself is discarded.

---

## 2. Stakeholder identification and RACI

### Identifying stakeholders
- Start with the sponsoring executive or product owner, then fan out: who is affected by the system, who feeds it data, who consumes its outputs, who must approve it, and who supports it.
- Consider internal and external stakeholders: end users, operations, legal/compliance, IT security, third-party integrators, and regulators.
- Stakeholders who are *not* affected but hold veto power (e.g. procurement, legal) are still stakeholders.

### RACI matrix
Assign exactly one **R** (Responsible) per decision or artifact. Multiple **R** assignments create accountability gaps.

| Role | Meaning |
|------|---------|
| **R — Responsible** | Does the work or makes the decision. |
| **A — Accountable** | Signs off. The buck stops here. One person only. |
| **C — Consulted** | Provides input before the decision is made. Two-way communication. |
| **I — Informed** | Notified after the fact. One-way communication. |

- Build the RACI at the start of the requirements phase. Revisit it when the stakeholder map changes.
- If no one is Accountable for a requirement, it will not get resolved. Escalate immediately.

---

## 3. Requirement types

Distinguishing types prevents mixing concerns and helps route requirements to the right teams.

### Business requirements
- State the *why*: the organizational goal or problem the initiative addresses.
- Written in business terms, not system terms.
- Example: "Reduce customer onboarding time from 5 days to 1 day."

### Functional requirements
- State *what* the system must do: specific behaviors, features, and data transformations.
- Each functional requirement is verifiable by a test.
- Example: "The system shall send a confirmation email within 30 seconds of account creation."

### Non-functional requirements (NFRs)
- State *how well* the system must perform: performance, availability, security, scalability, usability, compliance.
- NFRs are often harder to negotiate away than functional requirements because they are governed by SLAs or regulation.
- Example: "The login endpoint shall respond within 400 ms at the 95th percentile under a load of 500 concurrent users."

### Constraints
- Conditions that limit the solution space: budget, timeline, technology stack, regulatory mandates.
- Constraints are not requirements; they are boundaries. Document them separately so they are not confused with functional scope.

---

## 4. Definition of good requirements

A requirement is *good* if it meets all five criteria:

| Criterion | Test |
|-----------|------|
| **Unambiguous** | Every reader reaches the same interpretation. No weasel words ("user-friendly", "fast", "as needed"). |
| **Testable** | A tester can write a pass/fail test without further clarification. |
| **Atomic** | States exactly one thing. Split compound requirements (those joined by "and") into separate items. |
| **Traceable** | Can be linked to a business goal (upstream) and a test case or acceptance criterion (downstream). |
| **Feasible** | Can be implemented within the known constraints. Flag requirements that appear infeasible rather than silently dropping them. |

Avoid requirements that contain: "shall be able to optionally", "typically", "usually", "etc.", "and/or", "as appropriate". Each of these introduces ambiguity.

---

## 5. User stories and acceptance criteria

### User story format
```
As a [persona],
I want [capability],
so that [benefit / business value].
```

The persona must be a named role or actor (e.g. "registered customer", "warehouse picker"), not a generic "user".

### INVEST criteria
Every user story must satisfy INVEST before it enters a sprint:

| Letter | Criterion | What to check |
|--------|-----------|---------------|
| **I** | Independent | Can be developed without depending on another incomplete story. Refactor if dependencies exist. |
| **N** | Negotiable | The story describes a goal, not a contract. Implementation details are left to the team. |
| **V** | Valuable | Delivers demonstrable value to the persona or the business. If it does not, split or discard it. |
| **E** | Estimable | The team can size it. If they cannot, it needs more detail or needs to be split. |
| **S** | Small | Completable within one sprint. Epics must be split before entering the sprint backlog. |
| **T** | Testable | Acceptance criteria exist and are sufficient to verify the story is done. |

### Gherkin-style acceptance criteria
Write at least two scenarios per story: one happy path and one failure/edge case.

```
Scenario: [brief scenario title]
  Given [precondition — state of the world before the action]
  When  [actor performs an action]
  Then  [observable outcome]
```

- Use concrete values ("amount greater than £1,000") rather than abstract terms ("large amount").
- Each `Then` clause is independently verifiable.
- Add `And` / `But` lines to extend a step rather than squashing multiple conditions into one line.

---

## 6. Process modeling (as-is / to-be)

### As-is process
- Document the current state before proposing change. Discovering the as-is often reveals requirements the stakeholder forgot to mention.
- Walk through the process step by step with the people who actually do it.
- Capture: actors, inputs, outputs, decisions, exception paths, handoff points, and known pain points.

### To-be process
- Model the desired future state after the system change.
- Every delta between as-is and to-be is a candidate requirement. Trace each delta back to a functional or NFR.
- Flag steps that are eliminated: someone may depend on them in a way that was not surfaced.

### BPMN basics (use these element names for clarity)
| Element | Meaning |
|---------|---------|
| **Pool** | Represents a participant (organization or system). |
| **Lane** | Represents a role or department within a pool. |
| **Task** | A unit of work performed by an actor. |
| **Gateway (exclusive ✕)** | A decision point; one path taken. |
| **Gateway (parallel +)** | All outgoing paths taken simultaneously. |
| **Intermediate event** | Something that happens mid-process (timer, message received). |
| **Start / end event** | Entry and exit points of the process. |

Keep BPMN diagrams at the level of granularity that fits on one screen. Sub-processes can be collapsed and detailed separately.

---

## 7. Scope and MoSCoW prioritization

### MoSCoW
| Category | Meaning |
|----------|---------|
| **M — Must have** | Non-negotiable. The release fails without this. |
| **S — Should have** | High value, expected, but a workaround exists for the short term. |
| **C — Could have** | Desirable but not critical. Drop first when scope pressure increases. |
| **W — Won't have (this time)** | Explicitly out of scope for this release. Agreed, documented, and deferred. |

- Every item in the backlog must have an explicit MoSCoW assignment agreed with the product owner.
- The Must-have set alone must be deliverable within the agreed constraints. If it is not, negotiate scope before development starts.
- "Won't have" is not the same as "rejected forever." Record the rationale and revisit in future iterations.

---

## 8. Traceability matrix

A traceability matrix links each requirement to its source and its verification evidence.

Minimum columns:

| Req ID | Requirement summary | Source (business goal / stakeholder) | Story / feature | Test case ID | Status |
|--------|--------------------|------------------------------------|-----------------|-------------|--------|

- Assign a stable, unique ID to every requirement (e.g. REQ-001, REQ-002).
- Update the matrix whenever a requirement changes; stale matrices mislead.
- Use the matrix to identify orphan requirements (no test case) and gold-plating (test cases with no requirement).
- At release, every Must-have requirement must have a passing test case entry.

---

## 9. Handling ambiguous or conflicting requirements

### Ambiguity
- Identify the ambiguous term or phrase explicitly. Do not guess the intended meaning.
- Propose two or three concrete interpretations and ask the stakeholder to select or revise.
- Record the chosen interpretation in the requirement and in a decision log.
- Common sources of ambiguity: pronouns ("it", "they"), vague quantifiers ("large", "many"), implicit actors, undefined edge cases.

### Conflicts
- Surface the conflict to both stakeholders at the same time. Do not resolve it unilaterally.
- Frame the conflict as a trade-off: "Stakeholder A needs X; Stakeholder B needs Y. These cannot both be true simultaneously. Which takes precedence, and why?"
- Document the decision, the rationale, and any compensating requirements that address the losing party's underlying concern.
- Escalate to the Accountable owner (per RACI) if the conflict cannot be resolved at the stakeholder level.
