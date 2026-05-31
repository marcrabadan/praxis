# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Plugin versions are tracked independently in each plugin's
`.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. A repo
release tag (`vX.Y.Z`) marks the state of the whole library at a point in time.

## [Unreleased]

### Added

- `LICENSE` (Apache-2.0) and `NOTICE`, making the project open source.
- `SECURITY.md` with a private vulnerability-reporting process.
- `CHANGELOG.md` (this file) and a documented versioning scheme.

### Changed

- Hardened the `validate` GitHub Actions workflow with a least-privilege
  `permissions: contents: read` block.
- Updated the README License section to reflect the Apache-2.0 license.

## [1.0.0] - 2026-05-31

### Added

- Initial public release of the **praxis** skill factory.
- `skill-creator` meta-skill — the pattern for scaffolding, classifying,
  reviewing, and validating new Claude Code skills.
- Eight SDLC expert skills: business-analyst, product-owner,
  software-architect, developer, qa-engineer, devops-engineer,
  security-engineer, and cybersecurity-architect.
- Per-expert slash commands and the `/new-feature` orchestrator.
- `/review-changes` diff router plus opt-in CI and local-hook integrations.
- Two distributable plugins (`praxis` and `skill-factory`) at version `1.0.0`,
  published via `.claude-plugin/marketplace.json`.
- Deterministic skill generator, validators, catalog builder, and CI.

[Unreleased]: https://github.com/marcrabadan/praxis/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/marcrabadan/praxis/releases/tag/v1.0.0
