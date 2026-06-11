# Code Quality Metrics

This is a **harness rule**. It is short and behavior-changing. It gives every
skill a shared vocabulary and a set of default min/max thresholds for
code-quality metrics — aligned to SonarQube's default ("Sonar way") Quality
Gate — so reviews and checklists across `developer`, `qa-engineer`,
`software-architect`, and `security-engineer` measure the same things the same
way.

## Precedence

These are **praxis defaults**, not a substitute for a repo's own configured
quality gate. If the repo already has a configured SonarQube Quality Gate (or
an equivalent — ESLint complexity rules, coverage thresholds enforced in CI,
etc.), **that configuration is binding for that repo**; treat it as the
operative threshold and use this rule only for the shared vocabulary. Use the
defaults below when the repo has no such configuration.

## Quality gate (new/changed code)

| Metric | Default threshold |
|---|---|
| Coverage on new code | >= 80% |
| Duplicated lines on new code | <= 3% |
| Maintainability rating on new code | A |
| Reliability rating on new code | A |
| Security rating on new code | A |
| Security hotspots reviewed | 100% |

## Per-function / per-file thresholds

| Metric | Default threshold | Action above threshold |
|---|---|---|
| Cyclomatic complexity (function) | <= 10 | refactor or justify |
| Cognitive complexity (function) | <= 15 | refactor or justify |
| Duplicated lines (file) | <= 3% | extract per the DRY 3+-copies rule |

## Ratings derived from issues

| Rating | Maintainability (Technical Debt Ratio) | Reliability / Security (worst issue found) |
|---|---|---|
| A | <= 5% | none |
| B | <= 10% | Minor / Low |
| C | <= 20% | Major / Medium |
| D | <= 50% | Critical / High |
| E | > 50% | Blocker |

Technical Debt Ratio = remediation cost of all open Code Smells / estimated
cost to develop the codebase from scratch.

## How skills use this

- **`developer`** — duplication and complexity thresholds during
  implementation and pre-merge review (`practices.md` §2 DRY, `checklist.md`
  §3 Code quality).
- **`qa-engineer`** — coverage-on-new-code threshold as part of test
  readiness (`checklist.md` §B Test coverage).
- **`software-architect`** — Maintainability Rating / Technical Debt Ratio as
  a quantitative companion to the `/patterns` hotspot signal (`checklist.md`
  §8 Simplicity and reversibility).
- **`security-engineer`** — Security Rating and Security Hotspots Reviewed as
  evidence for `G-security` (`checklist.md` §8 Pipeline gates).

## What this rule does not do

- It does not add a new mandatory verify gate. `G-lint`, `G-tests`, and
  `G-security` already cover this ground; this rule gives the skills that
  prepare evidence for those gates concrete numbers and a shared vocabulary.
- It does not require SonarQube specifically. Any tool that reports the same
  metrics (CodeClimate, ESLint plus coverage tooling, etc.) satisfies the same
  checklist items.
