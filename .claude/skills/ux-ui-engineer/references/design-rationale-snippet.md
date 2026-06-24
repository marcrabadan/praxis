# Per-Screen Design Rationale (embed block)

Embed this block inside the governed artifact for a screen: its spec section, plan section, task block, implementation note, or equivalent. It records which design gate decision was made for this screen and why, so the reasoning lives with the workflow's source of truth.

Use a sidecar only when the host workflow has no mutable governed artifact. If you use a sidecar, state why and link it from the governed artifact.

Fill every applicable row. Mark a row `not-applicable` with a one-line reason when the surface genuinely does not engage that gate. Accessibility and usability are never not-applicable.

```markdown
### Design rationale: <screen name>

- User and job: <who, and the one job this screen does>
- Failure cost: <low / medium / high> - <what breaks if the screen fails>
- Primary action: <the single primary action>

| Gate | Verdict | Note |
|---|---|---|
| G-accessibility | applied | <contrast, focus, status signals, label decisions> |
| G-usability | applied | <chunking / option / disclosure decisions for this user> |
| G-ia | applied | <region map, scan path, what was deferred or cut> |
| G-tokens | applied | <token set and mode used; gaps reported> |
| G-components | applied | <intent-to-component choices; one primary per area> |
| G-hierarchy | applied | <density, grid, responsive, state coverage> |
| G-content | applied | <voice, labels, empty/error copy decisions> |
| G-ux | applied | <friction tuned to failure cost> |
| G-imagery | not-applicable | <reason, or imagery decisions for marketing surfaces> |
| G-landing | not-applicable | <reason, or page-job/proof/CTA for marketing surfaces> |

Open design questions: <list, or "none">
```
