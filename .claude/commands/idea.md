---
description: Triage a raw idea — clarify it, classify it as a feature, bug, or refinement (or not worth doing), record it as a pending ledger note, and recommend the next lifecycle command. The intake front door before /new-feature, /fix-bug, or /refine. Use for a half-formed thought.
argument-hint: "<a raw idea, bug, or improvement — in your own words>"
---

`/idea` is the **intake and triage** front door. It takes a raw, half-formed
thought, works out what kind of work it is, leaves a durable record, and points
you at the right lifecycle command. It does **not** plan, write a spec, or run the
lifecycle — it classifies, captures, and recommends, then stops.

The idea:

$ARGUMENTS

## How to handle it

1. **Clarify only if needed.** If the idea is too vague to classify, ask **at most
   two** questions with `AskUserQuestion` — never a third. If still ambiguous,
   classify on what you have and note the residual uncertainty.
2. **Classify** the (clarified) idea into exactly one category:

   | Class | Route | When |
   |-------|-------|------|
   | `feature` | `/new-feature` | new user-observable behavior |
   | `bug` | `/fix-bug` | existing behavior deviates from what's expected |
   | `refinement` | `/refine` | behavior-preserving — absorbs docs, dependency bumps, process changes |
   | `not-worth-doing` | _(none)_ | insufficient signal, or cost outweighs value |

3. **Capture** it — always, for every class, before any output:

   ```bash
   python .claude/skills/memory/scripts/ledger.py log --type note --source /idea \
     --status pending --tags "intake,<class>" --title "<clarified one-line summary>"
   ```

4. **Recommend, then stop.** Print the class, the ledger id, and — for a routable
   class — `Next: <route> "<the same summary>"` for the user to run. For
   `not-worth-doing`, replace the route line with one sentence of idea-specific
   rationale. Do not invoke the lifecycle command yourself; write nothing after.
