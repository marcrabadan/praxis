# Frontend Architecture Review Checklist

A checklist a frontend architect works through when reviewing or signing off a frontend design or application. Mark each item pass / fail / N-A and summarize the open risks. Flag unresolved items explicitly rather than waving them through.

---

## 1. Rendering strategy

- [ ] The rendering strategy (CSR / SSR / SSG / ISR / streaming / RSC / islands) is chosen deliberately and matches the route's SEO, freshness, and interactivity needs.
- [ ] Strategy is decided per route where it varies, not forced app-wide.
- [ ] Hydration cost is justified — interactive JS is shipped only where interactivity is actually needed.
- [ ] SEO-critical routes are server-rendered or statically generated; auth-only routes do not pay an unnecessary SSR tax.

---

## 2. State and data architecture

- [ ] State is classified (server / URL / global client / local UI / form) and each category uses the right tool.
- [ ] Server data is held in a server-cache library, not hand-rolled in a global store.
- [ ] State lives as local as possible; nothing is global without a sharing reason.
- [ ] Bookmarkable/shareable state (filters, tabs, selection) lives in the URL.
- [ ] The API style (REST / GraphQL / tRPC) suits the client's needs; contract ownership and versioning are defined.
- [ ] A BFF is introduced only where aggregation, auth exchange, or payload shaping justifies it.
- [ ] Caching layers (CDN/HTTP, client cache, edge) and per-resource freshness are explicit.

---

## 3. Routing and code splitting

- [ ] Routing approach (file-based vs config) is consistent across the app.
- [ ] Code is split at the route level so users download only what they visit.
- [ ] Heavy/below-the-fold/rarely-used modules are lazy-loaded; the app is not over-split into chunk churn.
- [ ] Shared chrome uses nested layouts rather than re-rendering on every navigation.

---

## 4. Build and bundle budgets

- [ ] A bundle budget (initial JS, total JS, largest chunk) is defined and enforced in CI.
- [ ] Tree shaking works; large dependencies are audited and modular/native alternatives preferred.
- [ ] The build toolchain gives fast local feedback and reproducible output.
- [ ] A monorepo, if used, is justified by shared code across apps/packages — not adopted for a single app.

---

## 5. Design system and theming

- [ ] Tokens are layered (primitive → semantic → component) and sourced once.
- [ ] Theming (light/dark, multi-brand) is a token swap on CSS variables, not a fork.
- [ ] The design system is distributed as a versioned package with a changelog and documented breaking changes.
- [ ] Components hard-code no raw values that should be tokens.

---

## 6. Performance and Core Web Vitals

- [ ] Numeric targets are set: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (or stated, justified alternatives).
- [ ] An image strategy (responsive, modern formats, explicit dimensions, lazy below the fold) is defined.
- [ ] A font strategy (`font-display`, preloading the critical font/LCP image) is defined.
- [ ] Edge/CDN and caching are used to reduce TTFB.
- [ ] Performance is measured with field data (RUM/CrUX), not only lab scores.

---

## 7. Accessibility and internationalization

- [ ] The component library is accessible by default (focus, keyboard, semantic primitives) so feature teams inherit it.
- [ ] If the app is localized: strings are externalized, layout handles text expansion and RTL, and Intl is used for dates/numbers/currency.
- [ ] Locale routing strategy (subpath/subdomain/domain) is decided where applicable.

---

## 8. Security (client-side)

- [ ] No secrets or privileged logic ship to the browser; sensitive calls run on the server/BFF.
- [ ] Tokens are stored safely (httpOnly cookies preferred over `localStorage`).
- [ ] A Content Security Policy is defined; any raw-HTML injection is sanitized.
- [ ] Authorization is enforced on the server; client-side route guards are treated as UX only.

---

## 9. Observability and error handling

- [ ] Client errors are captured and reported (error tracking / RUM), with source maps available.
- [ ] Error boundaries and sensible fallback UI exist at the right boundaries; one failing widget cannot blank the page.
- [ ] Loading, empty, and error states are an architectural expectation, not an afterthought left to each feature.

---

## 10. Maintainability and scalability

- [ ] The codebase is organized by feature/domain with clear module boundaries and public surfaces.
- [ ] Dependencies point inward; features do not reach into each other's internals.
- [ ] The architecture is no more complex than the constraints require — no speculative micro-frontends, monorepos, or abstractions.
- [ ] Significant decisions (framework, rendering, state, API, distribution) are recorded as short frontend ADRs.
- [ ] The upgrade/migration path for the framework and key dependencies is understood and not a dead end.
