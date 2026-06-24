# Governance Design Articles (seed block)

Merge these articles into the host workflow's durable governance artifact: constitution, principles, standards, rules, quality bar, or equivalent. Add them after existing principles or fold them into an existing UX/quality section. Do not overwrite or renumber what is already there. Tailor each `<...>` placeholder to the project's design source of truth before merging.

Each article is written to be testable so a review or analysis phase can judge pass or fail.

---

## Article: Accessibility (non-negotiable)

All text and meaningful UI meet WCAG AA contrast. Interactive elements have a visible focus state and are keyboard operable. Status and meaning are conveyed by at least two signals, never color alone. Form fields have persistent visible labels, not placeholder-only labels. Violations are allowed only with a recorded, justified exception.

## Article: Usability floor (non-negotiable)

The UI stays within the usability floor for the named primary user: group or defer content past the chunk limit, avoid forcing more options than the user can scan, prefer recognition over recall, and use progressive disclosure when a surface overflows. Expert, high-frequency surfaces may relax this with a recorded reason.

## Article: Design system and tokens

The app builds on <named design system / component library / token set / "free">. Color, spacing, type, and elevation come from its tokens where tokens exist; components come from its library where a library exists. Missing tokens or components are reported as gaps and resolved with the design owner. They are never invented inline. The active theme/mode is <light / dark / brand mode> set once at the app root.

## Article: Information architecture

Every screen has exactly one primary action, a declared region map, and an honest scan path. Content that does not serve the screen's job is cut or deferred, not crammed in.

## Article: Content and tone

User-visible copy uses an operational voice in the product's domain verbs. No marketing filler in product workflows. Empty states and errors are specific and useful. No em-dashes and no fake-precise numbers in user-visible copy. Target locale conventions apply to dates, currency, and names where <locale> is set.

---

## Merge note

If the project's governance artifact already has a UX, accessibility, quality, or design-system section, fold these articles into it rather than creating a parallel section. Keep the article titles so [experience-design-checklist](../workflows/experience-design-checklist.md) can map a failed check back to the article it breaks.
