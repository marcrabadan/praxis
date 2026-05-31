# Security Policy

## What this repo contains

`praxis` is a library of Claude Code **skills** — instruction packages and
small authoring/validation tooling (Python scripts) that teach Claude Code how
to perform tasks. It is not a deployed service and stores no secrets,
credentials, or user data. The realistic security surface is:

- the authoring/validation scripts under `.claude/factory/` and
  `.claude/skills/*/scripts/`;
- the GitHub Actions workflow under `.github/workflows/`;
- the guidance in the skills themselves, which should never instruct an agent
  to perform unsafe actions (e.g. exfiltrating secrets, disabling safeguards).

## Supported versions

The latest release on `main` is supported. See [CHANGELOG.md](CHANGELOG.md)
for released versions.

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅        |
| < 1.0   | ❌        |

## Reporting a vulnerability

Please report security issues **privately** — do not open a public issue for
anything exploitable.

1. Preferred: open a [GitHub private security advisory](https://github.com/marcrabadan/praxis/security/advisories/new)
   ("Report a vulnerability"), which keeps the report confidential until a fix
   is ready.
2. Alternative: email the maintainer at `marcrabadan@gmail.com` with a clear
   description and reproduction steps.

Please include:

- the affected file(s) or skill(s) and version/commit;
- a description of the issue and its impact;
- steps to reproduce, and a proof of concept if you have one.

## What to expect

- **Acknowledgement** within 5 business days.
- An initial assessment and severity triage within 10 business days.
- Coordinated disclosure: we'll agree on a timeline and credit you in the
  advisory unless you prefer to remain anonymous.

## Scope notes

Reports about the *content* of a skill that could lead Claude Code to take an
unsafe action are in scope and welcome. Generic findings produced by automated
scanners with no demonstrated impact may be closed without action.
