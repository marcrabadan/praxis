# UX/UI Engineering Practices

Core principles for the design–code bridge: building systematic, accessible, consistent interfaces and specifying them with enough fidelity to build right. Standards are cited by name so recommendations are verifiable, not matters of taste.

---

## 1. Design systems and component libraries

A design system is a shared language, not a sticker sheet. Design components as systems of states and variants, and document the rules so others can extend them correctly.

- Specify every component's **anatomy** (its named parts), its **variants** (primary/secondary, sizes), and its full set of **states**: default, hover, focus, active, disabled, loading, error, selected, read-only. A spec that omits states ships bugs.
- Name things by **intent and role**, not appearance. `Button / Primary` survives a rebrand; `Button / Blue` does not.
- Document **usage rules**: when to use this component vs. a similar one, do/don't examples, and the accessibility contract (keyboard model, roles, labels) the implementation must honor.
- Establish **governance**: who can add or change a component, how contributions are reviewed, and how the system stays consistent as it grows. Without governance, a design system fragments back into one-offs.

---

## 2. Design tokens and theming

Tokens turn design decisions into named, reusable values so the UI stays consistent and themeable. Layer them by intent.

| Tier | Purpose | Example |
|------|---------|---------|
| **Primitive** | Raw values, no meaning | `blue-600 = #2563EB`, `space-4 = 16px` |
| **Semantic** | Intent, references primitives | `color.text.danger`, `color.bg.surface` |
| **Component** | Component-specific, references semantic | `button.primary.bg`, `input.border.focus` |

- Components consume **semantic/component tokens**, never raw primitives. That is what makes a theme swap (light/dark, brand A/B) a value change rather than a redesign.
- Define **light and dark** (and any brand) as alternative values for the same semantic tokens. Don't fork components per theme.
- Keep naming consistent and predictable (`category.property.variant.state`). Tokens are an API; renaming them is a breaking change.

---

## 3. Typography

Typography carries most of an interface's hierarchy and readability. Use a scale, not arbitrary sizes.

- Define a **type scale** (a small set of steps from a ratio, e.g. 1.2–1.25) rather than ad-hoc px values. Each step has a size, line-height, and weight.

| Step | Use | Example |
|------|-----|---------|
| Display / H1–H3 | Page and section titles | tight line-height, heavier weight |
| Body | Paragraphs, controls | ~1.5 line-height for readability |
| Caption / small | Metadata, helper text | ≥ 12px; don't go smaller for body text |

- Establish clear **hierarchy** through size, weight, and spacing — not color alone (color is not perceivable by everyone).
- Keep body line length to roughly **45–75 characters** for readability; set comfortable line-height (~1.5 for body).
- Limit typefaces and weights; every extra font is a performance and consistency cost.

---

## 4. Color and contrast

Color must work for everyone and survive theming. Treat contrast as a requirement, not a preference.

- Meet **WCAG 2.2** contrast minimums:

| Content | AA | AAA |
|---------|----|----|
| Normal text (< 18.66px bold / 24px) | **4.5:1** | 7:1 |
| Large text (≥ 18.66px bold / 24px) | **3:1** | 4.5:1 |
| UI components & graphics (1.4.11) | **3:1** | — |

- Never use **color as the only means** of conveying information (WCAG 1.4.1) — pair it with text, an icon, or a pattern (e.g. error = red **and** an icon **and** a message).
- Build color as **semantic tokens** (text, surface, border, accent, success/warning/danger) so dark mode and brands are token swaps and contrast is checked once per theme.
- Verify contrast at design time with a checker; don't eyeball it.

---

## 5. Spacing, grid, and elevation

Consistent space and alignment are what make an interface feel "designed". Systematize them.

- Use a **spacing scale** based on a base unit (commonly 4px or 8px): 4, 8, 12, 16, 24, 32, 48… Every margin and padding is a step on the scale, not a one-off.
- Define a **layout grid** (columns, gutters, margins) and responsive breakpoints, and align content to it.
- Apply spacing by **relationship**: related elements sit closer; unrelated groups get more space (the proximity principle). Whitespace is a tool, not wasted room.
- Use an **elevation system** (a small set of shadow/overlay levels) to express layering consistently rather than arbitrary shadows.

---

## 6. Interaction and motion design

Motion should clarify, not decorate. Every animation needs a reason.

- Use motion to communicate **cause/effect, continuity, and state change** — where something came from, that an action registered, that content is loading.
- Keep UI transitions **fast and subtle**: roughly 150–300 ms for most interface motion; longer feels sluggish, instant feels jarring. Use natural easing (ease-out for entering, ease-in for leaving).
- Provide feedback for **every interactive state** (hover, focus, active, loading, success, error) so the interface feels responsive and predictable.
- Always honor **`prefers-reduced-motion`** (WCAG 2.3.3): offer a reduced or no-motion alternative for users who are sensitive to movement.

---

## 7. Accessibility as a design responsibility

Accessibility starts in design. Most accessibility failures are decisions made (or omitted) before any code is written. Design to WCAG 2.2 AA as the baseline.

- **Color & contrast** (1.4.3, 1.4.11): meet the ratios in §4; don't rely on color alone (1.4.1).
- **Focus visibility** (2.4.7, 2.4.11): design a clear, non-obscured focus indicator for every interactive element — don't remove focus rings without a better replacement.
- **Target size** (2.5.8): interactive targets at least **24×24 CSS px** (AA); aim for ~44×44 for primary touch targets.
- **Logical order & structure**: specify heading hierarchy, reading/focus order, and landmark regions in the design so the built page is navigable by screen reader and keyboard.
- **Accessible names & labels**: every control and icon-only button has a visible or programmatic name; form fields have persistent labels (not placeholder-only).
- **Don't design keyboard traps or hover-only affordances**; anything reachable by mouse must be reachable by keyboard.
- (This skill owns *which criteria apply and what the design must satisfy*; the **frontend-engineer** owns turning that into semantic HTML, ARIA, and keyboard behavior in code.)

---

## 8. Responsive and adaptive design

Design for a range of screens and inputs, not a single mockup. Start small.

- Design **mobile-first**: the small-screen layout forces prioritization, then enhance for larger viewports.
- Define **breakpoints by content** (where the layout breaks down), not by specific device names. Use **fluid type and spacing** (`clamp()`) so the design scales smoothly between breakpoints rather than jumping.
- Distinguish **responsive** (same layout reflowing) from **adaptive** (different layouts/components per breakpoint) and choose deliberately per pattern.
- Design for **input and context**: touch target sizes, hover not being available on touch, one-handed reach, and bright-sunlight/low-vision conditions.
- Ensure content **reflows without horizontal scroll** down to 320px (WCAG 1.4.10) and remains usable at 200% zoom (1.4.4).

---

## 9. Usability heuristics and UX patterns

Evaluate designs against established heuristics before subjective opinion. Nielsen's 10 are the common vocabulary.

1. Visibility of system status — show what's happening (loading, saved, progress).
2. Match between system and the real world — speak the user's language.
3. User control and freedom — undo, cancel, clear exits.
4. Consistency and standards — follow platform and internal conventions.
5. Error prevention — prevent mistakes (confirmation, constraints, good defaults).
6. Recognition rather than recall — make options visible; don't make users remember.
7. Flexibility and efficiency — shortcuts for experts, simple paths for novices.
8. Aesthetic and minimalist design — every extra element competes for attention.
9. Help users recognize, diagnose, and recover from errors — plain-language, actionable messages.
10. Help and documentation — available when needed, in context.

- Reach for **established UX patterns** (well-understood navigation, forms, search, pagination) before inventing; novelty has a learnability cost. Avoid known **anti-patterns** (dark patterns, mystery-meat navigation, infinite scroll where users need to find footers).
- Get the **information architecture** right — labels, grouping, and navigation that match users' mental models — before polishing visuals.

---

## 10. Forms and content/UX writing

Forms and words are where users succeed or give up. Design both as part of the UI.

- **Forms:** one column, logical grouping, labels above fields (persistent, not placeholder-only), clear required/optional marking, helpful inline validation after the field, and human error messages that say what's wrong and how to fix it. Ask for the minimum; don't make optional data feel mandatory.
- **UX writing:** be clear, concise, and consistent. Use sentence case, active voice, and the user's vocabulary. Labels and buttons describe the action (`Save changes`, not `Submit`).
- **Error messages:** name the problem, the cause if knowable, and the fix — never blame the user or show a code. "Card declined — check the number or try another card," not "Error 402."
- Define **empty, loading, error, and success states** as first-class screens with their own copy and next action, not afterthoughts.

---

## 11. Inclusive and internationalized design

Design for the full range of users and locales from the start; retrofitting is expensive and exclusionary.

- **Internationalization:** never hard-code concatenated strings; allow for **text expansion** (German/Finnish can run 30–40% longer) so layouts don't break; support **RTL** mirroring for Arabic/Hebrew; localize dates, numbers, and currency formats; don't bake text into images.
- **Inclusive design:** consider color-vision deficiency, low vision, motor and cognitive differences, situational limitations (one hand, bright sun, slow network), and diverse names/addresses/pronouns in forms.
- Use **plain language** and avoid idioms that don't translate; write for a broad reading level.

---

## 12. Prototyping and the design-to-development handoff

The handoff is a contract. A vague handoff produces a UI that doesn't match the design and burns review cycles.

- Hand off **complete specs**: spacing and sizing (from the scale/tokens), color and type tokens (by name, not hex), all states, responsive behavior, and the accessibility contract (focus order, labels, keyboard model).
- Reference **tokens and components by name** so engineering wires the design system, not magic numbers. Redline only what tokens don't cover.
- Provide **interactive prototypes** for non-obvious flows and motion so behavior, not just static frames, is communicated.
- Run **design QA / visual-fidelity review** on the built UI against the spec: spacing, type, color, states, responsive behavior, motion, and accessibility. File findings with severity (must-fix includes any AA accessibility failure) and the specific token/criterion that's off.
- Treat the design–dev relationship as a loop: capture what engineering can't build as designed and feed it back into the system.
