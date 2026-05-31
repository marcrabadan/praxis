# Frontend Architecture Practices

Core principles and decision frameworks for designing the structure of a frontend application — the choices that are cheap to make early and expensive to reverse later.

---

## 1. Framework and meta-framework selection

Pick the framework that fits the team and the constraints, not the one that is trending. The cost of a framework is paid in hiring, maintenance, and migration — all of which dwarf the cost of writing the first feature.

- Separate the **rendering library** (React, Vue, Svelte, Angular, Solid) from the **meta-framework** that wraps it (Next.js, Nuxt, Remix/React Router, SvelteKit, Astro, Angular). The meta-framework decides routing, rendering, and data conventions; choose it deliberately rather than inheriting it.
- Weigh the decision against concrete constraints: team familiarity, hiring pool, SEO requirements, interactivity level, time-to-first-byte targets, hosting/edge capabilities, and the expected lifespan of the app.
- Prefer the boring, well-supported default unless a constraint rules it out. A framework with a large ecosystem and a clear upgrade path is worth more than marginal runtime wins.

| App profile | Reasonable default | Why |
|-------------|--------------------|-----|
| Content/marketing site, SEO-critical, low interactivity | Astro or SSG (Next/Nuxt static) | Ship near-zero JS; HTML-first |
| Content-heavy app with islands of interactivity | Astro islands, or Next App Router | Hydrate only what's interactive |
| Highly interactive app, SEO matters | Next.js / Nuxt / SvelteKit (SSR) | Server render + hydrate |
| Internal tool / dashboard behind auth, SEO irrelevant | SPA (Vite + React/Vue/Svelte) | No SSR complexity to carry |
| Enterprise app, large team, strong conventions | Angular | Batteries-included, opinionated |

- State the migration cost in the recommendation. "We can adopt X now and move to Y later" is only true if you name what that move would touch.

---

## 2. Rendering strategy

Rendering strategy is the single highest-leverage frontend architecture decision. It sets your SEO ceiling, your time-to-interactive floor, and your hosting model.

| Strategy | Renders | Best for | Cost |
|----------|---------|----------|------|
| **CSR** (client-side) | In the browser after JS loads | Apps behind auth, no SEO need | Slow first paint, weak SEO |
| **SSG** (static) | At build time | Content that changes rarely | Rebuild to update; build time scales with pages |
| **SSR** (server) | Per request on the server | Dynamic, SEO-critical, personalized | Server cost, TTFB depends on data |
| **ISR** (incremental static) | At build + revalidated on demand | Large catalogs, semi-fresh content | Stale window; cache invalidation |
| **Streaming SSR** | Server, flushed in chunks | Slow data without blocking shell | More complex; needs Suspense boundaries |
| **RSC** (server components) | On the server, no client JS | Reducing bundle, server-side data access | React-specific; mental-model shift |
| **Islands** | Static HTML + hydrated islands | Mostly static with interactive pockets | Coordinating island state |

- Choose **per route**, not per app. A marketing landing page (SSG) and a logged-in dashboard (CSR/SSR) can live in one codebase with different strategies.
- Hydration is not free. Every interactive component shipped to the client costs parse, execution, and memory. Prefer architectures (RSC, islands, partial hydration) that ship interactivity only where it is needed.
- If SEO and first-paint do not matter (authenticated internal tools), do not pay the SSR tax. A clean SPA is the simpler, cheaper architecture.

---

## 3. Application and component architecture

A frontend codebase needs a structure that survives growth and team turnover. Decide it once, write it down, and enforce it.

- Organize by **feature/domain**, not by file type. `features/checkout/{components,hooks,api}` scales better than top-level `components/`, `hooks/`, `utils/` buckets that grow into dumping grounds.
- Separate **presentational** (dumb, props-in/markup-out) from **container/connected** (data-aware) components so the visual layer stays testable and reusable.
- Define clear **layering**: UI components → feature modules → shared domain logic → API/data layer. Dependencies point inward; UI never imports another feature's internals directly.
- Establish boundaries that prevent the "big ball of mud": a feature module exposes a public surface (an `index.ts`) and hides the rest. Cross-feature reuse goes through a shared layer, not through reaching into a sibling.
- Keep a single source of truth for cross-cutting concerns (auth context, theme, feature flags, i18n) provided high in the tree, consumed where needed.

---

## 4. State architecture — decide where state lives

Most frontend pain comes from putting state in the wrong place or using one tool for everything. Classify state first, then pick a tool per category.

| State category | Examples | Right home |
|----------------|----------|------------|
| **Server state** | Fetched data, lists, entities | A server-cache lib (TanStack Query, SWR, RTK Query, Apollo) — not your global store |
| **URL state** | Filters, pagination, tab, search query | The URL (route params / query string) |
| **Global client state** | Auth/session, theme, feature flags | A small global store (Zustand/Jotai) or context |
| **Local UI state** | Open/closed, hover, input focus | Component `useState`/`useReducer` |
| **Form state** | Field values, validation, dirtiness | A form library (react-hook-form), kept local |

- The most common anti-pattern is caching server data in a global Redux store and hand-writing loading/error/refetch logic. Use a purpose-built server-cache library instead; it handles caching, dedup, revalidation, and stale-while-revalidate.
- Put state as **local as possible**. Lift it only when two siblings genuinely need to share it. Global-by-default creates coupling and re-render storms.
- Prefer the **URL as state** for anything a user should be able to bookmark, share, or reload into — filters, current tab, selected item. It is free persistence and deep-linking.

---

## 5. Data-fetching and BFF design

The frontend's relationship to its data sources is an architectural concern, not an implementation detail.

- Choose the API style from the frontend's needs: **REST** (simple, cacheable, ubiquitous), **GraphQL** (client-shaped payloads, avoids over/under-fetching, heavier infra), **tRPC** (end-to-end types in a TS monorepo, no schema layer, tightly coupled). State who owns the contract and how it versions.
- Consider a **Backend-for-Frontend (BFF)** when the frontend must aggregate several services, hide internal APIs, handle auth/token exchange, or shape payloads for the UI. A BFF keeps the client thin and the contract owned by the frontend team — at the cost of another deployable.
- Decide the **caching layers** explicitly: HTTP cache headers / CDN, the client data cache (query cache), and any edge cache. Name the freshness requirement per resource (real-time, seconds-stale-ok, daily) and let it drive the strategy.
- Keep secrets and privileged calls on the server (RSC, route handlers, or BFF). The browser is a hostile environment; anything shipped to it is public.

---

## 6. Routing and code splitting

Routing structure and bundle structure are linked: the route map is the natural seam for splitting code.

- Prefer **route-level code splitting** so a user downloads only the routes they visit. Most meta-frameworks do this automatically with file-based routing; in an SPA, lazy-load route components.
- Use **nested layouts** to share chrome (nav, sidebar) without re-rendering or re-fetching it on every navigation.
- Split further at **heavy, below-the-fold, or rarely-used** boundaries — a charting library, a rich text editor, a modal flow — with dynamic import. Do not over-split; each chunk has request overhead.
- Decide file-based vs. config-based routing once and stay consistent. File-based is conventional and discoverable; config-based gives central control for complex guard/redirect logic.

---

## 7. Build, bundling, and monorepos

The build system is infrastructure. Choose for fast feedback loops and predictable output.

- Default to **Vite/esbuild/Rollup** (or the framework's bundler — Turbopack, SvelteKit's build) for dev speed and modern output. Reach for webpack only when a specific plugin/feature requires it.
- Enforce **bundle budgets** in CI so size regressions fail the build rather than being discovered in production. Track initial JS, total JS, and the largest chunks.
- Ensure the toolchain does **tree shaking** and that dependencies are ESM and side-effect-free where possible. Audit large dependencies (moment, lodash, full icon sets) and prefer modular or native replacements.
- For **monorepos**, use Nx, Turborepo, or pnpm workspaces when multiple apps/packages share code (a design system, shared types, a BFF). Get task caching and affected-only builds; pay the setup and discipline cost. Do not adopt a monorepo for a single app.

---

## 8. Micro-frontends and Module Federation

Micro-frontends are an organizational solution to an organizational problem. They are rarely a technical win on their own.

- Adopt them only when **independent teams must deploy independently** to the same shell, or when integrating apps built on different stacks. The driver is autonomy and deployment independence, not code reuse.
- Know the costs: duplicated dependencies (or fragile shared-singleton config), version skew, cross-app state and routing coordination, harder end-to-end testing, and a heavier performance baseline.
- Prefer cheaper alternatives first: a well-modularized monolith with clear feature boundaries, or a shared component library, solves most "we want independence" cases without the runtime tax.
- If you do adopt them (Module Federation, native federation, or build-time composition), define the contract: shared dependency versions, the routing owner, the shell's responsibilities, and how shared state crosses boundaries.

---

## 9. Design-system architecture

A design system is a product with consumers. Architect it for distribution and versioning, not just for the current app.

- Layer the **token pipeline**: primitive tokens (raw values) → semantic tokens (intent: `color.text.danger`) → component tokens. Source tokens once (e.g. a JSON/Style Dictionary source) and generate CSS variables, TS types, and platform outputs from it.
- Build **theming** on semantic tokens and CSS custom properties so light/dark and multi-brand are a token swap, not a fork. Avoid hard-coded values in components.
- Decide **distribution**: a versioned package (semver) consumed by apps, published to a registry, with a changelog and migration notes. Treat breaking changes as breaking — bump major, document the upgrade.
- Keep the component library **headless-friendly** where it helps: separate behavior/accessibility (the hard part) from skin (the themeable part) so the system survives a visual refresh.

---

## 10. Performance budgets and Core Web Vitals

Performance is an architectural property. Set numeric targets up front; "fast" is not a target.

- Own the **Core Web Vitals** at the architecture level:
  - **LCP** (Largest Contentful Paint) ≤ 2.5 s — driven by rendering strategy, server response, image strategy, and critical-path CSS.
  - **INP** (Interaction to Next Paint) ≤ 200 ms — driven by main-thread work and bundle size; the reason to ship less JS.
  - **CLS** (Cumulative Layout Shift) ≤ 0.1 — driven by reserving space for images/ads/embeds and avoiding layout-shifting injections.
- Set **bundle budgets** (e.g. ≤ 170 KB compressed initial JS as a starting heuristic) and enforce them in CI.
- Architect an **image and font strategy**: responsive images, modern formats (AVIF/WebP), explicit dimensions, lazy-loading below the fold, `font-display: swap`, and preloading the critical font/LCP image.
- Use the platform's edge/CDN and caching to cut TTFB. The fastest render is the one served from the edge already rendered.
- Measure with field data (RUM / CrUX) as well as lab (Lighthouse). Optimize what real users experience, not just the lab score.

---

## 11. Cross-cutting concerns: accessibility, i18n, security

These are architectural because retrofitting them is far more expensive than designing them in.

- **Accessibility:** make the component library accessible by default (focus management, semantic primitives, keyboard support baked in) so feature teams inherit it. Accessibility designed into the system is cheaper than auditing every screen. (Design-level criteria belong to the **ux-ui-engineer**; in-code implementation belongs to the **frontend-engineer** — this skill ensures the *architecture* supports both.)
- **Internationalization:** decide early whether the app is localized. Externalize strings, design for text expansion and RTL, format dates/numbers/currency through Intl, and choose routing for locales (subpath, subdomain, or domain). Retrofitting i18n touches every component.
- **Client-side security:** never trust the client. Keep tokens out of `localStorage` when possible (prefer httpOnly cookies); define a Content Security Policy; sanitize any HTML rendered via `dangerouslySetInnerHTML`/`v-html`; and keep authorization decisions on the server — client-side route guards are UX, not security.

---

## 12. Documenting frontend decisions (ADRs)

Significant frontend choices deserve a short Architecture Decision Record so the team understands the why six months later.

- Write a frontend ADR for: framework/meta-framework choice, rendering strategy, state-management approach, API style, monorepo adoption, and design-system distribution.
- Keep it to one page: **context** (the constraints), **decision** (what was chosen), **status**, **consequences** (what this makes easy and what it makes hard), and **alternatives considered** (and why rejected).
- Record the decision when it is made, not after it is regretted. The ADR is most valuable as a contract the team agreed to, not a postmortem.
