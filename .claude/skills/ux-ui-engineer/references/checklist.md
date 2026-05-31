# UX/UI Design Review Checklist

A checklist a UX/UI engineer works through when reviewing a design or a built UI for design quality and fidelity. Label findings by severity (nit / suggestion / must-fix) — any WCAG 2.2 AA failure is a must-fix. Cite the specific criterion, token, or heuristic for each finding.

---

## 1. Visual hierarchy and layout

- [ ] The most important element is clearly the most prominent; the eye lands where intended.
- [ ] Related items are grouped and unrelated ones separated (proximity); alignment is consistent.
- [ ] The layout follows the grid; nothing is visually off-axis without reason.
- [ ] The screen is not overcrowded — each element earns its place (minimalist design).

---

## 2. Typography

- [ ] Type sizes come from the defined scale; no ad-hoc sizes.
- [ ] Hierarchy is expressed through size/weight/spacing, not color alone.
- [ ] Body line length (~45–75 chars) and line-height (~1.5) support readability.
- [ ] No body text below ~12px; the number of typefaces/weights is limited.

---

## 3. Color and contrast

- [ ] Normal text meets 4.5:1; large text and UI components/graphics meet 3:1 (WCAG 1.4.3 / 1.4.11).
- [ ] Information is never conveyed by color alone (1.4.1) — paired with text/icon/shape.
- [ ] Colors are used as semantic tokens; the palette is consistent across the UI.
- [ ] Contrast holds in every theme (light and dark / each brand).

---

## 4. Spacing, grid, and elevation

- [ ] All margins/padding are steps on the spacing scale, not one-off values.
- [ ] Content aligns to the layout grid; gutters and margins are consistent.
- [ ] Elevation/shadows come from the defined set, used to express layering consistently.

---

## 5. Design tokens and consistency

- [ ] Components reference semantic/component tokens, not raw primitive values.
- [ ] The same element looks and behaves consistently everywhere it appears.
- [ ] Token names follow the naming convention; no undocumented one-off values.
- [ ] New patterns reuse existing components/variants rather than inventing near-duplicates.

---

## 6. Interaction and motion

- [ ] Every interactive element specifies hover, focus, active, disabled, loading, and error states.
- [ ] Motion has a purpose (status/continuity/feedback); durations are ~150–300ms with natural easing.
- [ ] A reduced-motion alternative is provided (`prefers-reduced-motion`, WCAG 2.3.3).
- [ ] Feedback is given for every user action (nothing happens silently).

---

## 7. Accessibility (WCAG 2.2 AA)

- [ ] A clear, non-obscured focus indicator is designed for every interactive element (2.4.7 / 2.4.11).
- [ ] Interactive targets are at least 24×24 CSS px (2.5.8); primary touch targets approach ~44×44.
- [ ] Heading hierarchy, reading order, focus order, and landmark structure are specified.
- [ ] Every control and icon-only button has an accessible name; form fields have persistent labels.
- [ ] No keyboard traps and no hover-only or color-only affordances.

---

## 8. Responsive and adaptive

- [ ] The design works mobile-first and at each breakpoint; breakpoints are content-driven.
- [ ] Type and spacing scale fluidly between breakpoints (no awkward jumps).
- [ ] Content reflows without horizontal scroll down to 320px (1.4.10) and is usable at 200% zoom (1.4.4).
- [ ] Touch ergonomics considered (target size, reach, no hover dependence on touch).

---

## 9. Content and UX writing

- [ ] Labels and buttons describe the action in the user's language (sentence case, active voice).
- [ ] Error messages name the problem and the fix; no codes, no blame.
- [ ] Microcopy is consistent in terminology, tone, and capitalization across the UI.
- [ ] Text allows for translation/expansion and avoids idioms; nothing critical is baked into images.

---

## 10. States (empty / loading / error / success)

- [ ] Empty states are designed with guidance and a clear next action, not a blank area.
- [ ] Loading states avoid layout shift (skeletons/reserved space) and match wait length.
- [ ] Error states are recoverable with a clear path; success states confirm the outcome.

---

## 11. Usability heuristics

- [ ] System status is always visible (loading, saved, progress) — Nielsen #1.
- [ ] Users have control and freedom: undo, cancel, and clear exits exist — #3.
- [ ] The design prevents errors (good defaults, constraints, confirmation) — #5.
- [ ] Options are recognizable, not recall-dependent — #6; established patterns used over novelty.
- [ ] No dark patterns or known anti-patterns.

---

## 12. Handoff and fidelity

- [ ] The spec covers spacing, color/type tokens (by name), all states, responsive behavior, and the accessibility contract.
- [ ] Tokens and components are referenced by name; magic numbers are minimized.
- [ ] Non-obvious flows and motion are communicated via interactive prototypes.
- [ ] The built UI matches the spec on spacing, type, color, states, motion, and accessibility (design QA done); deviations are filed with severity and the specific token/criterion.
