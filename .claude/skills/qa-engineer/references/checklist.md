# QA Checklists

Two standalone checklists: one for test readiness / release quality, one for good bug reports. Run the relevant checklist before marking work ready or filing a defect.

---

## Checklist 1 — Test readiness and release quality

Use this checklist before declaring a feature, sprint, or release ready to progress (e.g. dev-complete → QA, QA → staging, staging → production).

### A. Requirements and acceptance criteria

- [ ] Every user story or ticket in scope has written, reviewed, and agreed acceptance criteria.
- [ ] Acceptance criteria are testable (each criterion has an observable pass/fail outcome).
- [ ] No acceptance criterion uses vague language ("user-friendly", "fast", "as appropriate") without a measurable threshold.
- [ ] Non-functional requirements (performance SLAs, accessibility level, security controls) are explicitly stated, not assumed.
- [ ] Edge cases and failure paths are addressed in the ACs or explicitly acknowledged as out of scope.

### B. Test coverage

- [ ] A coverage matrix or equivalent exists mapping each AC to at least one test case ID.
- [ ] Every AC has at least one positive test case.
- [ ] Every AC that involves input validation, error handling, or business rules has at least one negative test case.
- [ ] Boundary values are tested for every numeric, date, or length-limited field.
- [ ] High-risk areas (new code, integrations, changed business logic) have positive + negative + boundary + exploratory coverage.
- [ ] **Team rule — test-first:** complex logic in the change (non-trivial conditionals, calculations, parsing/serialization, state machines, concurrency, security-sensitive paths) carries unit tests written *before* the implementation; complex logic without unit tests is flagged as a release risk, and every fixed defect has the regression test that failed before the fix.
- [ ] Exploratory testing has been performed with a documented session charter and notes.
- [ ] Code coverage on new/changed code meets the default in `rules/code-quality-metrics.md` (>= 80%) or the repo's configured quality gate; shortfalls are documented as a gap below.
- [ ] Any gaps in coverage are documented and risk-accepted by the product owner in writing.

### C. Defect status

- [ ] No open Critical severity defects linked to in-scope stories.
- [ ] No open High severity defects without a documented resolution plan and product-owner sign-off.
- [ ] All defects fixed in this cycle have been re-verified against the exact fix (not just closed by the developer).
- [ ] Regression defects (defects in previously passing tests) are flagged and their root cause understood.

### D. Regression and automation

- [ ] The smoke suite passes on the target environment.
- [ ] The core regression suite passes (or failures are triaged and accepted).
- [ ] Any new test cases written for this cycle are added to the appropriate regression suite.
- [ ] New defect fixes have a corresponding regression test case that would have caught the defect.
- [ ] No test cases are skipped without documented justification.

### E. Test environment and test data

- [ ] The test environment matches the production configuration in all material ways (feature flags, integrations, data volumes).
- [ ] Test data is representative of production patterns including edge-case records.
- [ ] No production PII or sensitive data is present in the test environment.
- [ ] Test data created by automated tests is cleaned up after each run; no residual state from previous runs.
- [ ] Environment-specific defects (works in staging, broken in production) are investigated and ruled out.

### F. Non-functional checks

- [ ] Performance: key endpoints or flows have been tested under expected load; results are within the stated SLA.
- [ ] Accessibility: automated scan (axe-core or equivalent) shows zero Critical and Serious violations on affected pages.
- [ ] Accessibility: keyboard navigation and at least one screen-reader walkthrough have been performed on critical flows.
- [ ] Security: authentication and authorisation rules have been verified (correct users see correct data; unauthorised access is blocked).
- [ ] Security: no sensitive data (tokens, passwords, PII) appears in logs, API responses, or client-side storage.
- [ ] Usability: error messages are actionable and appear inline; empty states and loading states are handled.

### G. Entry and exit criteria sign-off

- [ ] All entry criteria were met before testing began (green build, agreed ACs, available environment).
- [ ] All exit criteria are now met, or unmet criteria are explicitly risk-accepted in writing.
- [ ] The product owner or designated approver has reviewed and accepted the test summary.
- [ ] Test evidence (results report, defect list, coverage matrix) is linked to the relevant ticket or release artefact.

---

## Checklist 2 — Good bug report

Use this checklist before filing or updating a defect ticket. A bug report that fails this checklist will be returned for more information.

### Required fields

- [ ] **Title** is a one-line summary in the form "[Component]: what is wrong" — specific enough to distinguish from any other defect, not a question or a symptom description ("Login broken" is bad; "Login: 'Forgot password' link returns 404 on mobile Safari 17" is good).
- [ ] **Environment** is fully specified: browser and version or app version, OS and version, device type, deployment environment (staging/UAT/production), commit SHA or release tag if known, feature flags active.
- [ ] **Steps to reproduce** are numbered, start from a clean and reproducible initial state, and can be followed blindly by someone with no prior knowledge of the defect.
- [ ] Each step in the reproduction sequence is a single atomic action (not "log in and navigate to checkout").
- [ ] **Expected result** states what should happen according to the acceptance criteria, specification, or reasonable user expectation — not what the reporter wishes would happen.
- [ ] **Actual result** states exactly what happened, including verbatim error messages, incorrect values, or absent UI elements.
- [ ] At least one piece of supporting evidence is attached: screenshot, screen recording, console log, or API response.
- [ ] **Severity** is assigned using the team's severity scale (Critical / High / Medium / Low) with a one-line rationale.
- [ ] **Priority** is either left for the product owner to assign or, if pre-assigned by the reporter, is clearly justified and separated from severity.
- [ ] Severity and priority are stated as separate fields — they are never combined into a single "importance" field.

### Reproducibility and accuracy

- [ ] The defect has been reproduced at least twice before filing, confirming it is not a one-off transient failure.
- [ ] The reporter has checked whether the defect exists on the main/trunk branch, not only on a feature branch.
- [ ] If the defect is intermittent, the report states the reproduction rate ("occurs 3 out of 5 attempts under the following conditions").
- [ ] The minimal reproduction case has been established: unnecessary steps have been removed until only the steps that trigger the defect remain.
- [ ] The reporter has searched for existing duplicate reports before filing a new one.

### Clarity and completeness

- [ ] The title and description use neutral, factual language — no blame, no urgency inflation ("this is CRITICAL and must be fixed NOW"), no hedging ("I think maybe").
- [ ] Technical jargon is either standard (and therefore unambiguous) or defined inline.
- [ ] The report does not include hypothesised root causes or implementation suggestions in the reproduction steps; root cause analysis belongs in a separate comment or field.
- [ ] If the defect was found during exploratory testing, the session charter and any relevant notes are referenced.
- [ ] The ticket is linked to the relevant story, test case, or acceptance criterion that the defect violates.
