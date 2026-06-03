# Documentation Quality Checklist

Run this before writing any file to disk. Every item must be satisfied.

---

## Scope

- [ ] The document has a single, named purpose — not a catch-all dump.
- [ ] The scope matches what the user asked for; nothing extra is added.
- [ ] The source data (ledger entries, code) has been read before writing — no guessing.

## Structure

- [ ] The document opens with a one-line purpose statement (what it is and who it is for).
- [ ] Sections follow the format shape in [formats.md](formats.md) for the chosen type.
- [ ] Headers are imperative or noun-phrase; no "Introduction" or "Overview" as the first and only section.
- [ ] Tables are used for structured data (parameters, fields, options); prose for rationale.

## Content

- [ ] Every claim is sourced from the ledger or the codebase — no hallucinated details.
- [ ] Code examples compile/run or are marked as pseudocode.
- [ ] ADRs: Status, Context, Decision, Consequences, and at least one Alternative are all present.
- [ ] API docs: every parameter has a type, whether it is required, and a brief description.
- [ ] Runbooks: every step is a concrete imperative action ("run X", "check Y"), not vague advice.

## Tone and length

- [ ] Written for the intended reader (onboarding engineer, on-call responder, API consumer).
- [ ] No filler phrases ("it is important to note that", "as mentioned above").
- [ ] Each section is under 30 lines unless the domain genuinely demands more.
- [ ] No internal commentary ("TODO", "FIXME", "add more here") left in the output.

## Memory

- [ ] A ledger `artifact` entry is planned (or already recorded) for each file written.
- [ ] The entry body includes the file path, doc type, and what source it was generated from.
