# Frontend Engineering Practices

Core techniques for implementing user interfaces in code — composing components, wiring state and data, handling forms, styling, typing, optimizing, and testing. Examples use React/TypeScript idioms but the principles carry across frameworks.

---

## 1. Component design and composition

A component does one thing and exposes a small, honest API. Composition beats configuration.

- Split **presentational** (props in, markup out, no data access) from **container** (fetches/derives data, passes it down). Presentational components stay reusable and trivially testable.
- Prefer **composition over a pile of boolean props**. A component with `isPrimary`, `isLarge`, `withIcon`, `isLoading` is a smell; model variants explicitly or compose smaller pieces.
- Use **compound components** for related parts that share implicit state (`<Tabs><Tabs.List><Tabs.Tab/></Tabs.List></Tabs>`) instead of one component with a giant props object.
- Extract a **custom hook** when stateful logic is reused or when a component mixes concerns (data + UI). Hooks named `useX` encapsulate behavior; components stay about rendering.
- Keep components small enough to read at a glance. If JSX needs scrolling to understand, extract a child.

```tsx
// Prefer composition...
<Card>
  <Card.Header>Invoice</Card.Header>
  <Card.Body>{children}</Card.Body>
</Card>
// ...over a configuration blob:
<Card header="Invoice" body={children} variant="bordered" padded large />
```

---

## 2. State management usage

Put state in the smallest scope that works, and use the tool that matches the *kind* of state. Most state bugs are misplaced state.

| Kind of state | Use |
|---------------|-----|
| One component's UI (open, hovered, input value) | `useState` / `useReducer` |
| A few nearby components | Lift to the closest common parent |
| App-wide client state (theme, auth, flags) | Context, or a small store (Zustand/Jotai) |
| Server data (fetched entities/lists) | A server-cache library (TanStack Query / SWR / RTK Query) — **not** a global store |
| Complex local transitions with many actions | `useReducer` |

- Reach for `useReducer` over multiple `useState`s when updates are interdependent or follow clear action types.
- Avoid putting derived values in state. Compute them during render; store only the source. Storing derived state invites it going stale.
- Don't reach for Redux/Zustand for server data — caching, dedup, and revalidation are solved by query libraries.
- Keep context providers focused. A single mega-context re-renders every consumer on any change; split by concern or use selectors.

---

## 3. Data fetching and async states

Every async read has four states. Handle all of them, every time.

- Always render **loading**, **error**, **empty**, and **success** explicitly. A view that only handles the happy path will flash, blank, or crash for real users.
- Use a server-cache library for fetching: it gives you cache keys, request dedup, background refetch, and stale-while-revalidate for free.

```tsx
const { data, isPending, isError, error } = useQuery({
  queryKey: ['invoice', id],
  queryFn: () => fetchInvoice(id),
});
if (isPending) return <Spinner />;
if (isError) return <ErrorState message={error.message} onRetry={refetch} />;
if (data.items.length === 0) return <EmptyState />;
return <InvoiceList items={data.items} />;
```

- Structure **cache keys** to encode every input the request depends on (`['invoice', id, filters]`) so changing an input refetches and caching stays correct.
- For **mutations**, decide invalidate-vs-optimistic per case. Optimistic updates feel instant but require a rollback path on failure — implement the rollback, don't hand-wave it.
- Cancel or ignore stale requests (the library or `AbortController`) so a slow earlier response can't overwrite a newer one.

---

## 4. Forms and validation

Forms are where data quality and accessibility are won or lost. Lean on a form library and a schema.

- Prefer a form library (react-hook-form) over hand-wiring dozens of `useState`/`onChange` pairs; you get less re-rendering, built-in validation wiring, and dirty/touched tracking.
- Validate against a **schema** (zod/yup) so the same shape drives runtime validation and (with zod) the TypeScript type. One source of truth for "what is valid".
- Show **field-level errors** next to the field, after the user leaves it (on blur) or on submit — not aggressively on every keystroke.
- Make forms **accessible**: every input has an associated `<label>`; errors are tied via `aria-describedby`; the invalid field gets `aria-invalid`; focus moves to the first error on a failed submit.
- Decide controlled vs uncontrolled deliberately. Uncontrolled (via refs / react-hook-form) is cheaper for large forms; controlled is needed when other UI reacts to the value live.

---

## 5. Client-side routing usage

Routing is part of the UI contract: it should be linkable, restorable, and accessible.

- Read route and query **params as the source of truth** for navigable state (current tab, filters, selected id) so the page survives reload and share.
- Lazy-load route components so navigation only downloads the visited route.
- Implement route **guards** (auth/role) as redirects with a clear post-login return path — and remember they are UX, not security; the server still enforces access.
- Manage **focus on navigation**: move focus to the new page's heading or main region so keyboard and screen-reader users aren't stranded at the top of stale DOM.

---

## 6. Styling and responsiveness

Match the project's styling approach; don't introduce a fifth one. Build mobile-first and let layout adapt.

- Use the established system consistently — CSS Modules, Tailwind, or CSS-in-JS — rather than mixing. Consistency beats personal preference.
- Style from **design tokens / CSS variables**, not hard-coded hex and pixel values, so theming and dark mode work and the UI stays consistent.
- Write **mobile-first**: base styles for small screens, `min-width` media (or container) queries to enhance upward.
- Build responsive **layouts with Flexbox and Grid**; avoid fixed pixel widths that break on small screens or large text. Respect `prefers-reduced-motion` and `prefers-color-scheme`.
- Keep specificity low and avoid deep selector nesting; prefer component-scoped styles so a change can't leak across the app.

---

## 7. Frontend TypeScript

Types are documentation that can't go stale and a guardrail against whole classes of bugs. Use them precisely.

- Type component props with explicit interfaces. Avoid `any`; prefer `unknown` at boundaries and narrow it.
- Model "one of these shapes" with **discriminated unions** instead of optional-everything props — it makes impossible states unrepresentable.

```tsx
type Result =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: Invoice };
```

- Use **generics** for reusable components (`<Select<T>>`) so consumers keep their value types.
- Derive types from schemas/APIs (`z.infer`, generated OpenAPI/GraphQL types) rather than redeclaring them by hand and letting them drift.
- Type event handlers and refs properly; reach for `as` casts only with a comment justifying why the compiler can't see what you can.

---

## 8. In-code performance and re-renders

Measure before optimizing. Most "slow React" is unnecessary re-renders or shipping too much JS — not a missing `useMemo`.

- Profile first (React DevTools Profiler, browser performance panel). Optimize the path the data points at, not a guess.
- Understand why a component re-renders: parent re-rendered, props/state changed, or context value changed. Fix the cause (stable props, split context) before reaching for memoization.

| Tool | Use when |
|------|----------|
| `React.memo` | A pure component re-renders often with the same props |
| `useMemo` | An expensive computation runs each render with the same inputs |
| `useCallback` | A function identity must stay stable for a memoized child or effect dep |

- Don't memoize by reflex. `useMemo`/`useCallback` have their own cost and clutter; apply them where a profile shows benefit.
- **Virtualize** long lists (react-window/virtual) so only visible rows mount.
- Keep the bundle lean: lazy-load heavy components, prefer modular imports, and avoid pulling a whole library for one function.
- Avoid creating new object/array/function literals as props to memoized children — they break memoization every render.

---

## 9. Accessibility implementation

Accessibility is implemented in the markup and behavior. Start with the platform; it does most of the work for free.

- Use **semantic HTML first**: `<button>`, `<a>`, `<nav>`, `<label>`, `<ul>`, headings in order. A real `<button>` is focusable, keyboard-operable, and announced — a `<div onClick>` is none of those.
- Add **ARIA only when semantics fall short**, and correctly. The first rule of ARIA is "don't use ARIA if a native element does the job." Wrong ARIA is worse than none.
- Make everything **keyboard operable**: every interactive element reachable and activatable with Tab/Enter/Space/arrows; a visible focus indicator (`:focus-visible`); logical tab order.
- Manage **focus** for dynamic UI: move focus into an opened dialog and trap it, return it to the trigger on close, and announce route changes.
- Provide **accessible names** (label, `aria-label`, or `aria-labelledby`) for icon-only controls, and use **live regions** (`aria-live`) for async status (saved, error, results loaded).
- (Design-level criteria — contrast, target size, which pattern to use — belong to the **ux-ui-engineer**; this skill turns those into correct markup and behavior.)

---

## 10. Frontend testing

Test what the user experiences, not how the component is wired. Behavior-focused tests survive refactors.

- Use **React Testing Library** (or the framework equivalent): render the component and interact with it the way a user does.
- Query by **role and accessible name** first, then label/text; avoid `data-testid` unless nothing else identifies the element. Querying by role doubles as an accessibility check.

```tsx
await userEvent.click(screen.getByRole('button', { name: /save/i }));
expect(await screen.findByText(/saved/i)).toBeInTheDocument();
```

- Drive interactions with **`user-event`**, not raw `fireEvent` — it models real user behavior (focus, key sequences) more faithfully.
- Test **observable behavior** — rendered output, called callbacks, navigation — not internal state or implementation details that change on refactor.
- Mock at the **network boundary** (e.g. MSW) rather than mocking your own modules; it tests closer to reality.
- Add **E2E** (Playwright/Cypress) for the critical user journeys (login, checkout) and consider visual-regression for design-system components. Keep E2E few and high-value; they are slow and flakier.

---

## 11. Error and loading states; resilience

A robust UI degrades gracefully. Plan for slow, empty, and broken before shipping the happy path.

- Wrap risky subtrees in **error boundaries** with a useful fallback so one component's crash doesn't blank the whole app.
- Design the **empty state** (no data yet) as intentionally as the populated one — it's a user's first impression of a feature.
- Show **skeletons or spinners** appropriately: skeletons for content layout, spinners for short waits; avoid layout shift when content arrives (reserve space).
- Handle network failure with a **retry affordance** and a human-readable message — never a blank screen or a raw stack trace.

---

## 12. Debugging common frontend issues

Frontend bugs cluster into a few recurring shapes. Recognize them.

- **Re-render storms:** an unstable prop (new object/function each render) or a context value changing identity. Trace with the Profiler; stabilize the prop or split the context.
- **Stale closures:** an effect or callback captured an old value because a dependency was omitted. Fix the dependency array (and trust the lint rule) rather than disabling it.
- **Hydration mismatches** (SSR): server and client rendered different HTML — usually from `Date.now()`/random values, `window`/`localStorage` accessed during render, or locale differences. Render such values after mount, or make them deterministic.
- **Memory leaks:** subscriptions/timers not cleaned up. Return a cleanup function from `useEffect`.
- **Key warnings / list bugs:** use stable, unique keys (an id), never the array index for lists that reorder.
