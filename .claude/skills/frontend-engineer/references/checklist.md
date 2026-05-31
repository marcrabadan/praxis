# Frontend Engineering Self-Review Checklist

A self-review checklist a frontend engineer runs before opening or merging a pull request. Work through every section; flag outstanding items in the PR description rather than ignoring them.

---

## 1. Component design

- [ ] Each component does one thing; oversized components are split into children.
- [ ] Presentational and data-aware (container) concerns are separated where it helps reuse and testing.
- [ ] Reused stateful logic is extracted into a custom hook, not copy-pasted.
- [ ] The component API is small — composition is preferred over a pile of boolean/config props.
- [ ] No dead props, unused state, or commented-out JSX left behind.

---

## 2. State and data

- [ ] State lives in the right scope (local / lifted / global) and the right tool (UI state vs. server cache).
- [ ] Server data is fetched via the query library, not cached in a global client store.
- [ ] Derived values are computed during render, not duplicated into state where they can go stale.
- [ ] Cache keys encode every input the request depends on; mutations invalidate or optimistically update with a rollback path.
- [ ] Stale/cancelled requests cannot overwrite newer results.

---

## 3. Forms and validation

- [ ] Validation runs against a schema (zod/yup) that also drives the type where possible.
- [ ] Errors appear at field level at a sensible time (blur/submit), not aggressively on every keystroke.
- [ ] Every input has an associated label; errors are tied via `aria-describedby` and the field is marked `aria-invalid`.
- [ ] Submit is disabled or guarded against double-submission; focus moves to the first error on failure.

---

## 4. Accessibility

- [ ] Semantic HTML is used first; interactive elements are real `<button>`/`<a>`, not click-handled `<div>`s.
- [ ] ARIA is used only where native semantics fall short, and used correctly.
- [ ] Everything is keyboard operable with a logical tab order and a visible focus indicator (`:focus-visible`).
- [ ] Dialogs/menus manage focus (move in, trap, return on close); route changes move focus and are announced.
- [ ] Icon-only controls have accessible names; async status uses a live region.
- [ ] Tested by querying by role/accessible name (which doubles as an a11y check).

---

## 5. Performance and re-renders

- [ ] No unnecessary re-renders introduced; unstable object/function/array props to memoized children are avoided.
- [ ] Memoization (`memo`/`useMemo`/`useCallback`) is applied only where it measurably helps, not by reflex.
- [ ] Long lists are virtualized; heavy/rare components are lazy-loaded.
- [ ] No large dependency pulled in for a small need; imports are modular.
- [ ] Any optimization claim is backed by a profile, not a guess.

---

## 6. Styling and responsiveness

- [ ] Styling uses the project's established approach consistently; no new system introduced ad hoc.
- [ ] Values come from tokens/CSS variables, not hard-coded colors and pixels.
- [ ] Layout is mobile-first and works at small widths and with enlarged text.
- [ ] `prefers-reduced-motion` and dark mode (where supported) are respected.
- [ ] Selector specificity is low; styles are component-scoped and don't leak.

---

## 7. TypeScript and types

- [ ] Props and public APIs are explicitly typed; `any` is avoided (`unknown` + narrowing at boundaries).
- [ ] Impossible states are unrepresentable (discriminated unions over optional-everything).
- [ ] Types are derived from schemas/generated API types rather than hand-redeclared.
- [ ] `as` casts and `eslint-disable` lines are justified with a comment or removed.

---

## 8. Testing

- [ ] New/changed behavior is covered by tests that assert observable output, not internals.
- [ ] Tests query by role/accessible name and drive interactions with `user-event`.
- [ ] Network is mocked at the boundary (e.g. MSW), not by stubbing internal modules.
- [ ] Critical user journeys have or retain E2E coverage; design-system components have visual coverage where relevant.
- [ ] All tests pass locally; none are skipped to make the suite green.

---

## 9. Error, loading, and empty states

- [ ] Loading, error, and empty states are implemented — not just the happy path.
- [ ] Error boundaries wrap risky subtrees with a useful fallback; one widget can't blank the page.
- [ ] Failures show a human-readable message and a retry affordance, never a raw stack trace.
- [ ] No layout shift when async content arrives (space is reserved).

---

## 10. Cross-browser and cross-device

- [ ] Verified at mobile and desktop widths and (where relevant) on touch.
- [ ] No SSR hydration mismatch (no `window`/`Date.now()`/random in render; values rendered after mount where needed).
- [ ] Effects clean up subscriptions/timers; no console errors or warnings left in the output.
- [ ] No debug output (`console.log`) or leftover TODO/breakpoints in the diff.
