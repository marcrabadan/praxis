# BA Readiness Checklist

Concrete review checklist a Business Analyst runs over a requirements artifact or user story before marking it "ready for development". Work through every section in order. Record each finding with the item ID, the artifact ID, and the action required.

---

## Section 1 — Individual requirement quality

Run this section for every requirement or acceptance criterion in scope.

### 1.1 Unambiguity
- [ ] **R-01** The requirement contains no weasel words: "user-friendly", "fast", "as needed", "appropriate", "reasonable", "etc.", "and/or", "typically", "usually". Replace each with a specific, measurable term.
- [ ] **R-02** All pronouns ("it", "they", "this") resolve unambiguously to a named actor or system. Rewrite any pronoun whose referent is not obvious from the immediately preceding sentence.
- [ ] **R-03** All domain terms are defined in a glossary or are commonly understood by the entire team. Flag undefined terms; do not assume shared meaning.
- [ ] **R-04** Every numeric constraint names the measurement unit and the condition under which it applies (e.g. "within 400 ms at the 95th percentile under 500 concurrent users", not "fast").

### 1.2 Testability
- [ ] **R-05** A tester can write a pass/fail test for the requirement without asking any clarifying questions. If not, the requirement is not yet testable — refine it.
- [ ] **R-06** Every acceptance criterion has a distinct, observable `Then` clause that does not require judgment to evaluate.
- [ ] **R-07** Edge cases and failure paths are either covered by a dedicated scenario or explicitly declared out of scope.

### 1.3 Atomicity
- [ ] **R-08** Each requirement states exactly one verifiable thing. Requirements joined by "and" are split into separate items.
- [ ] **R-09** Each acceptance criterion scenario tests exactly one behavior. Scenarios that test multiple behaviors simultaneously are split.

### 1.4 Traceability
- [ ] **R-10** Every requirement has a stable, unique ID (e.g. REQ-042).
- [ ] **R-11** Every requirement is linked upstream to at least one business goal or user need.
- [ ] **R-12** Every requirement is linked downstream to at least one user story, acceptance criterion, or test case ID (or the gap is flagged and assigned an owner to close).

### 1.5 Feasibility
- [ ] **R-13** No requirement contradicts a known constraint (budget, timeline, technology stack, regulation). If a potential contradiction exists, it is flagged for the Accountable owner — not silently dropped.
- [ ] **R-14** Non-functional requirements (performance, availability, security) have been reviewed with the engineering lead to confirm they are achievable within the solution approach.

---

## Section 2 — User story format

Run this section for every user story (in addition to Section 1).

### 2.1 Story card format
- [ ] **S-01** The story follows the canonical format: "As a [persona], I want [capability], so that [benefit]."
- [ ] **S-02** The persona is a named role or actor ("registered customer", "warehouse picker"), not a generic "user".
- [ ] **S-03** The capability describes what the user wants to accomplish, not how the system will do it. Implementation detail belongs in the acceptance criteria or in a technical note, not in the story card.
- [ ] **S-04** The benefit states the business or user value. If no one can articulate the benefit, the story may not be worth doing — escalate before proceeding.

### 2.2 INVEST assessment
- [ ] **S-05 — Independent:** The story can be developed and demonstrated without depending on another incomplete story. If a dependency exists, it is recorded and the dependency story is scheduled first.
- [ ] **S-06 — Negotiable:** The story describes a goal; it does not prescribe a specific UI layout, algorithm, or technology choice. Those details are negotiated with the development team.
- [ ] **S-07 — Valuable:** The story delivers demonstrable value to the stated persona or to the business. A story that only moves data between systems with no user-visible outcome should be restructured or linked to a story that does deliver value.
- [ ] **S-08 — Estimable:** The development team has confirmed they can size the story. If they cannot, the story needs more detail or must be split.
- [ ] **S-09 — Small:** The story is completable within one sprint at the team's normal capacity. Epics must be split before entering the sprint backlog.
- [ ] **S-10 — Testable:** At least two Gherkin-style acceptance criteria scenarios exist (see Section 3).

### 2.3 Acceptance criteria — Gherkin format
- [ ] **S-11** At minimum, one happy-path scenario and one failure/edge-case scenario are present.
- [ ] **S-12** Each scenario uses the `Given / When / Then` structure. `And` / `But` lines are used to extend a step rather than cramming multiple conditions into one line.
- [ ] **S-13** `Given` clauses describe a complete, reproducible precondition — no hidden state assumptions.
- [ ] **S-14** `When` clauses describe a single, discrete actor action.
- [ ] **S-15** `Then` clauses use concrete, observable values ("the order status is set to 'Confirmed'", "an email with subject 'Order Confirmed' is sent to the registered address") rather than vague assertions ("the user sees a success message").
- [ ] **S-16** No scenario contains numeric thresholds or data values that are under active negotiation. Placeholder values are flagged with `[TBD: owner, deadline]`.

---

## Section 3 — Stakeholder and RACI completeness

Run this section when reviewing a requirements package (not required for individual stories).

- [ ] **T-01** A stakeholder register exists listing every party who is affected by, feeds, consumes, approves, or supports the system.
- [ ] **T-02** A RACI matrix exists covering all key requirements decisions and review gates. Each row has exactly one **A** (Accountable) and at least one **R** (Responsible).
- [ ] **T-03** Every requirement in the package can be traced to at least one named stakeholder who originated or validated it.
- [ ] **T-04** No stakeholder who holds veto power (legal, security, compliance, procurement) is missing from the register.

---

## Section 4 — Requirement types and classification

- [ ] **C-01** Business requirements, functional requirements, non-functional requirements, and constraints are kept in separate labeled lists. No mixing of types within a single list.
- [ ] **C-02** Every NFR specifies the metric, the target value, the measurement condition, and the measurement method (or the method is flagged as TBD with an owner).
- [ ] **C-03** Constraints are documented separately and do not appear in the functional requirements list.
- [ ] **C-04** Each requirement is labeled with its MoSCoW priority (Must / Should / Could / Won't), agreed with the product owner.

---

## Section 5 — Process model completeness

Run this section when a process model (as-is or to-be) is part of the artifact.

- [ ] **P-01** An as-is process model exists and has been validated by the people who actually perform the process (not only by management).
- [ ] **P-02** The to-be process model identifies every delta from the as-is. Each delta is linked to at least one functional requirement.
- [ ] **P-03** Every actor, decision point, handoff, exception path, and known pain point is represented in the model.
- [ ] **P-04** Eliminated steps are explicitly noted; any downstream dependency on those steps has been investigated.
- [ ] **P-05** The diagram uses consistent BPMN element names (Pool, Lane, Task, Gateway, Event) or the notation used is defined in a legend.

---

## Section 6 — Conflict and ambiguity resolution

- [ ] **A-01** No requirement contains an unresolved conflict marker (`[CONFLICT]`, `TBD`, `???`, `to be agreed`).
- [ ] **A-02** Every conflict that was raised during elicitation is recorded in the decision log with: the conflicting positions, the resolution, the rationale, and the name of the Accountable owner who made the call.
- [ ] **A-03** Every ambiguous term that was identified has been defined in the glossary or replaced with a concrete, specific term.
- [ ] **A-04** If a conflict was resolved by deferring one stakeholder's need, a compensating requirement or a "Won't have (this time)" entry documents what was traded away and why.

---

## Section 7 — Traceability matrix health

- [ ] **M-01** Every requirement with MoSCoW priority Must or Should has a corresponding row in the traceability matrix.
- [ ] **M-02** No orphan requirements exist (requirements with no linked test case and no recorded reason for the gap).
- [ ] **M-03** No gold-plating exists (test cases in the matrix that map to no requirement).
- [ ] **M-04** The matrix version and last-updated date are current. A matrix not updated since the last requirements change is stale and must be refreshed before sign-off.

---

## Sign-off gate

The artifact is "ready for development" when:

1. All checked items in Sections 1–4 pass (Sections 5–7 apply only when the relevant artifact type is in scope).
2. All open items are recorded in the decision log or flagged as TBD with a named owner and a resolution deadline.
3. The product owner has reviewed and accepted the MoSCoW assignments.
4. The development team lead has confirmed the Must-have set is deliverable within the agreed sprint or release constraints.

Do not mark an artifact "ready" if any Section 1 item (R-01 through R-14) is unresolved. Quality of individual requirements is the non-negotiable baseline.
