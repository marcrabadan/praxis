# QA Practices

Core quality-assurance techniques, test-design methods, and testing principles for the entire SDLC. Third-person, concrete, with examples.

---

## 1. Test automation pyramid

The pyramid defines the proportion and purpose of each test layer. Violating it — over-investing in UI tests, under-investing in unit tests — creates slow, brittle suites.

| Layer | Description | Proportion | Speed | Cost to maintain |
|-------|-------------|------------|-------|-----------------|
| **Unit** | Tests a single function, class, or module in isolation. Dependencies are mocked. | ~60–70 % | Milliseconds | Low |
| **Integration / service** | Tests the interaction between two or more components or services (e.g. API + database). | ~20–30 % | Seconds | Medium |
| **End-to-end (E2E) / UI** | Tests a complete user journey through the deployed system. | ~5–10 % | Minutes | High |

- Keep E2E tests to the most critical user journeys; they are expensive to write, slow to run, and fragile.
- Integration tests are where contract violations between services are caught earliest.
- Unit tests must be fast enough to run on every commit without debate.
- A pyramid that is actually an ice-cream cone (mostly E2E) signals inadequate unit coverage; refactor toward the base.

---

## 2. Test-design techniques

Apply the technique that fits the input space. Combining techniques eliminates more defects than any single technique alone.

### 2.1 Equivalence partitioning (EP)
Divide the input domain into partitions where every value in a partition is expected to behave identically. Write one test per partition rather than testing every value.

**Example — age field (valid: 18–99):**
- Partition 1 (below minimum): age = 17 → invalid
- Partition 2 (valid): age = 35 → valid
- Partition 3 (above maximum): age = 100 → invalid

### 2.2 Boundary value analysis (BVA)
Test values at and just across the edges of each partition. Boundary defects (off-by-one errors, inclusive/exclusive confusion) are among the most common.

**For the same age field:**
- 17, 18, 19 (around lower bound)
- 98, 99, 100 (around upper bound)

Always test at, just below, and just above each boundary.

### 2.3 Decision tables
Model combinations of conditions and their resulting actions. Useful when behavior is determined by multiple independent boolean or enumerated inputs.

**Example — discount eligibility:**

| Member? | Basket ≥ £50? | Promo code valid? | Outcome |
|---------|--------------|-------------------|---------|
| Y | Y | Y | 25 % discount |
| Y | Y | N | 15 % discount |
| Y | N | Y | 10 % discount |
| Y | N | N | 5 % discount |
| N | Y | Y | 10 % discount |
| N | Y | N | 0 % discount |
| N | N | * | 0 % discount |

Each row is a test case. Collapse rows with identical outcomes where the varying condition has no effect (indicated by *).

### 2.4 State transition testing
Model a system that has distinct states and transitions between them (e.g. user accounts, order lifecycles, session management). Test valid transitions, invalid transitions, and transitions that should be blocked.

**Example — order lifecycle:**
- States: Draft → Submitted → Processing → Shipped → Delivered | Cancelled
- Valid: Draft → Submitted on "Submit" action
- Invalid: Shipped → Draft (should be blocked)
- Test every valid transition at least once; test the most critical invalid transitions.

### 2.5 Pairwise (all-pairs) testing
When a full combinatorial explosion of N variables is too expensive, test every pair of values at least once. Pairwise typically reduces test count by 60–90 % while catching most interaction defects.

Use a pairwise generator tool (e.g. PICT, AllPairs) when there are four or more independent variables each with two or more values.

---

## 3. Turning acceptance criteria into test cases

### Mapping process
1. Parse each acceptance criterion (AC) sentence by sentence.
2. Identify the actor, pre-condition, trigger/action, and expected outcome.
3. Write at least: one positive case (happy path), one negative case (invalid input or wrong state), one boundary case, and one exploratory case per AC.
4. Assign each test case a unique ID and link it to its AC ID (e.g. TC-042 → AC-007).

### Gherkin-style test case anatomy
```
ID:            TC-042
AC ref:        AC-007
Type:          Negative
Precondition:  User is logged in; basket contains 2 items.
Steps:
  1. Navigate to checkout.
  2. Enter expired credit card number 4111 1111 1111 1111 (exp 01/20).
  3. Click "Pay now".
Expected:      Error message "Your card has expired. Please use a different card." is displayed. No charge is made.
Actual:        (fill at execution time)
Pass / Fail:   —
```

- Preconditions must be specific enough to reproduce exactly.
- Expected results must be observable (UI message, response code, database state) — never "it should work".

---

## 4. Positive, negative, edge, and exploratory testing

| Type | Purpose | Example |
|------|---------|---------|
| **Positive** | Confirm the happy path works with valid, expected input. | Login with correct credentials → user reaches dashboard. |
| **Negative** | Confirm the system handles invalid, missing, or malformed input gracefully. | Login with wrong password → error message; no account lockout on first attempt. |
| **Boundary / edge** | Probe limits of input ranges, collection sizes, date extremes, empty states. | Upload file exactly at the 10 MB limit; upload 0-byte file. |
| **Exploratory** | Unscripted testing where the tester designs tests in real time based on what they observe. Sessions are time-boxed (30–90 min) with a charter ("explore the checkout flow as a returning customer with an expired card"). |

Exploratory testing is not ad hoc — it is structured, session-based, and documented with a charter, notes, and any defects found.

---

## 5. Risk-based testing and prioritization

Risk = Likelihood of failure × Impact of failure.

### Risk assessment steps
1. Identify risk areas: new code, changed code, integrations, complex business logic, data-migration paths, third-party dependencies.
2. Score each area: High / Medium / Low for both likelihood and impact.
3. Prioritize test coverage: High × High areas get positive + negative + boundary + exploratory; Low × Low areas may get smoke-test only.
4. Document risk decisions so they are revisited if requirements change.

### Risk matrix (example)

| Risk area | Likelihood | Impact | Priority |
|-----------|-----------|--------|----------|
| Payment processing change | High | High | P1 — full test coverage |
| UI label update | Low | Low | P3 — smoke test only |
| Third-party shipping API integration | Medium | High | P1 — full + contract test |
| Admin-only config page | Low | Medium | P2 — positive + negative |

---

## 6. Bug report structure

A complete bug report answers every question a developer needs without follow-up.

### Required fields

| Field | Guidance |
|-------|---------|
| **Title** | One-line summary: [Component] Short description of what is wrong. E.g. "Checkout: VAT not recalculated when delivery country changes." |
| **Environment** | Browser/version, OS, device, app version or commit SHA, test data used, feature flags active. |
| **Steps to reproduce** | Numbered, atomic steps starting from a clean/known state. Anyone must be able to follow them blindly and see the defect. |
| **Expected result** | What should happen according to the spec, AC, or reasonable expectation. |
| **Actual result** | Exactly what happened. Include error messages verbatim; attach screenshots or screen recordings. |
| **Severity** | Impact on the system or user: Critical / High / Medium / Low (see below). |
| **Priority** | Business urgency for fixing it: P1 / P2 / P3 / P4. Set by the product owner, not the tester. |
| **Supporting evidence** | Screenshots, logs, HAR files, console output. |

### Severity vs priority — always stated separately

| Severity | Meaning | Example |
|----------|---------|---------|
| **Critical** | System crash, data loss, security breach, or complete feature blockage. | Payment API returns 500 for all transactions. |
| **High** | Major feature broken with no workaround. | User cannot reset password. |
| **Medium** | Feature partially works; workaround exists. | Sorting by date is reversed. |
| **Low** | Cosmetic or minor inconvenience. | Tooltip text has a typo. |

Priority is how urgently the business needs the fix. A Low-severity cosmetic issue on the home page of a marketing campaign may be P1 because of business deadlines. Never conflate severity with priority.

---

## 7. Non-functional testing at a QA level

QA designs the approach and acceptance criteria for non-functional testing; implementation of load-test scripts or penetration tests may involve specialists.

### Performance testing
- **Load test:** target load at expected peak. Pass criterion: 95th-percentile response time ≤ stated SLA (e.g. ≤ 400 ms for API calls).
- **Stress test:** beyond peak load to find the breaking point and observe graceful degradation.
- **Soak/endurance test:** sustained load over hours to detect memory leaks or connection pool exhaustion.
- Baseline before the release and compare after; regressions in response time are defects.

### Security testing (QA perspective)
- Verify that authentication and authorisation rules are tested: can User A access User B's data? Can an unauthenticated user reach protected endpoints?
- Check input validation: SQL injection patterns, script injection in form fields, oversized payloads.
- Confirm sensitive data (passwords, tokens, PII) is not logged or returned in API responses.
- Review OWASP Top 10 for the relevant application type and create at least one test case per applicable item.

### Accessibility testing
- Automated pass: run axe-core or equivalent; zero Critical and Serious violations is the minimum bar.
- Manual pass: keyboard-only navigation (tab order, focus visibility, modal traps); screen-reader walkthrough (VoiceOver / NVDA) of critical flows; colour-contrast check (WCAG AA: 4.5:1 for normal text).
- Test pass criteria reference WCAG 2.1 AA unless a stricter standard is contractually required.

### Usability testing (QA scope)
- Verify error messages are actionable ("Password must be at least 8 characters" not "Invalid input").
- Confirm loading states, empty states, and zero-result states are handled and labelled.
- Check that form validation feedback appears inline next to the field, not only as a page-level summary.

---

## 8. Regression strategy

Regression testing prevents changes from breaking existing functionality.

### Suite composition
- **Smoke suite:** 10–20 tests covering the most critical end-to-end paths. Run on every build. Must complete in under 5 minutes.
- **Core regression suite:** tests for all high-priority features. Run daily or before every release candidate.
- **Full regression suite:** all automated tests. Run before major releases or after high-risk changes.

### What to retest after a change
1. The changed code paths (directly affected tests).
2. Tests that call the changed code indirectly (call-graph neighbours).
3. Any area that shares data, infrastructure, or configuration with the changed area.
4. The smoke suite always.

### Regression test selection heuristics
- New defect fix → add a regression test that would have caught the defect.
- Refactored module → run its full unit and integration suite.
- Database schema change → run all tests that touch the affected tables.
- Third-party dependency upgrade → run contract tests and the integration suite for that dependency.

---

## 9. Test data management

Good test data is deterministic, isolated, and non-destructive.

- **Isolate environments:** production data must never be used in test environments. Use anonymised or synthetically generated data.
- **Own your setup:** each test case must set up its own preconditions (or clearly state the required precondition). Tests that depend on execution order are fragile.
- **Clean up after tests:** automated tests should delete or reset the data they create. Shared test-environment pollution causes false failures.
- **Reference data vs transactional data:** maintain a stable set of reference data (product catalogue, user roles) that is seeded into every environment. Transactional data (orders, payments) is created and cleaned up per test.
- **Edge-case data:** maintain a library of pre-built edge-case datasets: strings with Unicode, maximum-length values, null/empty fields, dates at DST transitions, leap-year dates, and currency edge cases (zero amounts, negative amounts, largest representable value).

---

## 10. Entry and exit criteria

Entry criteria define when testing may begin. Exit criteria define when testing is complete enough to proceed.

### Entry criteria (testing may begin when)
- The feature branch is merged to a test-environment branch; the build is green.
- Acceptance criteria are written, reviewed, and agreed by product and development.
- Test data and test environment are available and configured.
- Any hard-blockers from the previous testing cycle are resolved.

### Exit criteria (testing is done when)
- All P1 and P2 test cases have been executed with a pass verdict.
- All Critical and High severity defects are resolved and re-verified.
- No open P1 defects. Open P2 defects are risk-accepted by the product owner in writing.
- Coverage matrix shows every AC mapped to at least one passing test case, or the gap is explicitly acknowledged.
- Exploratory testing charter is complete with no unresolved critical findings.

### Definition of "done / tested"
A story is "tested" when:
1. All acceptance criteria are covered by executed, passing test cases.
2. Exploratory testing has been performed with a documented charter.
3. No open Critical or High defects are linked to the story.
4. Non-functional requirements (if any) have been verified against their stated acceptance thresholds.
5. The test evidence (test results, defect list) is linked to or attached to the story ticket.
