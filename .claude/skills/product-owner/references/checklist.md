# Definition of Ready Checklist

A concrete checklist for reviewing a backlog item before it enters a sprint. Run this checklist item-by-item during backlog refinement. Produce a pass/fail verdict for each criterion and a concrete fix for every failure.

---

## 1. Title and summary

- [ ] The item has a descriptive title that states the outcome or goal, not the implementation task.
- [ ] The title is unique in the backlog — no duplicate or near-duplicate items.
- [ ] The item is written from the perspective of who benefits (role/goal/benefit format, or an outcome statement for discovery work).

**Failure fix:** rewrite the title to name the outcome. Example: change "Address input changes" to "Returning user can select a saved address at checkout."

---

## 2. Acceptance criteria

- [ ] At least one acceptance criterion is written before the session.
- [ ] Every acceptance criterion is testable: a human or automated test can determine pass or fail without ambiguity.
- [ ] Acceptance criteria use one of these formats: Given/When/Then or a bulleted list of observable outcomes.
- [ ] Non-functional requirements (performance thresholds, accessibility level, security controls) are stated explicitly as acceptance criteria, not left as implied expectations.
- [ ] Acceptance criteria describe the "what," not the "how" — they do not prescribe implementation.

**Failure fix:** for each vague criterion, rewrite it as "Given [context], When [action], Then [observable result]." If a non-functional requirement is missing, add it now.

---

## 3. Sizing and effort

- [ ] The team has estimated the item (story points, t-shirt size, or hours — whichever the team uses).
- [ ] The estimate fits within one sprint. If it does not, the item must be split before it can be marked ready.
- [ ] The size estimate is agreed by the whole delivery team, not assigned by the PO or a single engineer.

**Failure fix:** if the item is too large, apply a story-splitting pattern (by workflow step, by data variation, by role, by interface, or by acceptance criterion) and create child items.

---

## 4. Dependencies

- [ ] All upstream dependencies (other stories, external APIs, third-party decisions, legal approvals) are identified.
- [ ] Each dependency has a clear owner and a known or estimated resolution date.
- [ ] No unresolved blocking dependency will prevent the team from starting or completing the item within the sprint.

**Failure fix:** list each blocking dependency as an explicit item in the backlog or risk register. Do not mark the story ready until blocking dependencies are resolved or a parallel mitigation plan exists.

---

## 5. Value and priority rationale

- [ ] The business value or user value of the item is stated (even as a rough relative estimate).
- [ ] The item's position in the backlog order is justified — the PO can explain why this item ranks above or below its neighbors.
- [ ] The item aligns with the current sprint goal or roadmap theme. If it does not, it needs an explicit justification for inclusion.

**Failure fix:** apply a prioritization framework (MoSCoW for release scoping, RICE for mid-backlog ranking, WSJF for time-critical or program-level items, Value-vs-Effort for fast visual alignment) and document the score or category that justifies the rank.

---

## 6. Design and UX

- [ ] Any required UX designs, wireframes, or prototypes are available and linked.
- [ ] Open UX decisions that would block implementation are resolved.
- [ ] Copy, labels, and error messages are finalized (or explicitly marked as "placeholder, final copy TBD" with an owner).

**Failure fix:** flag unresolved design decisions to the designer and block the story until resolved. Do not accept "we'll figure it out during development" as a resolution.

---

## 7. Technical prerequisites

- [ ] The team has confirmed they understand the technical approach at a high level (not necessarily the full design).
- [ ] Any required infrastructure, environment setup, or tooling is in place or has a clear plan to be ready before the story starts.
- [ ] If the technical approach is unknown or high-risk, a spike story has been created and completed (or is scheduled before this story).

**Failure fix:** create a time-boxed spike to answer the specific technical question. The spike output must be knowledge (a documented decision or proof of concept), not partially complete code.

---

## 8. Test plan awareness

- [ ] The team knows who will test the item and roughly how.
- [ ] Any test data, test accounts, or environment configuration needed to verify the acceptance criteria is available or has a plan.
- [ ] Performance or load criteria have a defined test approach if they are part of the acceptance criteria.

**Failure fix:** assign a tester and identify test data gaps before the sprint starts. If test data must be seeded or a test environment must be configured, add that as a sub-task or a prerequisite story.

---

## 9. Definition of Done alignment

- [ ] The team has confirmed the item can meet the team's Definition of Done within the sprint (code reviewed and merged, automated tests passing, accessibility criteria met, deployed to staging, PO accepted).
- [ ] No items in the DoD are known to be impossible for this story within the sprint (e.g., a third-party integration that cannot be tested in staging).

**Failure fix:** if a DoD criterion cannot be met, decide now — either split the story so the unshippable part is a separate item, or explicitly document the exception and the plan to resolve it before production deployment.

---

## 10. Team clarity

- [ ] Every member of the team who attended refinement can explain what the story does and why it matters.
- [ ] There are no open questions that would require the team to stop work and wait for an answer during the sprint.
- [ ] The PO is available during the sprint to answer clarifying questions (or has designated a decision-making proxy).

**Failure fix:** if the team cannot explain the story back to the PO in their own words, the story needs another refinement pass. List all open questions and resolve them before the sprint planning session.

---

## Ready verdict

A backlog item is **ready** only when every criterion above is marked pass.

| Status | Meaning |
|--------|---------|
| All pass | Item is ready to enter sprint planning. |
| One or more fail | Item is not ready. Document each failure and assign a fix owner. Schedule a follow-up refinement before the next sprint planning session. |
| Multiple critical failures | Remove the item from the sprint candidate list. Revisit in the next refinement cycle once blockers are resolved. |

An item that enters sprint planning with unresolved failures is a sprint risk. The PO is accountable for not allowing unready items into a sprint.
