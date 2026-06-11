# Model tiers

*Match the model to the work — semantic tiers, never hardcoded vendor models.*

Praxis commands never name a concrete LLM. They name one of three **semantic
tiers**, and each runtime resolves a tier to whatever model it actually offers.
This keeps the doctrine portable across runtimes (Claude Code, OpenAI Codex,
Cursor, JetBrains Junie) and across model generations — when a vendor ships a
new model, only the mapping changes, never the commands.

## The tiers

| Tier | What it is for | Never use it for |
| ---- | -------------- | ---------------- |
| `light` | Pure retrieval and summarization: context digests, condensing a PRD, finding relevant files. | Any reasoning phase. |
| `standard` | Structured transformation of prior artifacts — **the default for every phase**: requirements, prioritization, test design, delivery planning, verification. | — |
| `deep` | Frontier reasoning where depth demonstrably pays: a genuinely hard design, a complex root-cause diagnosis, a high-stakes domain analysis (security, ML). | Routine phases — that is paying frontier prices for transformation work. |

**The default is `standard`. A phase *earns* `deep`; it is never given it by
reflex.** Escalate only when the specific work is genuinely hard — and tell the
user which phases you escalated and why. `light` never runs a reasoning phase.

## Resolution order

1. **`.praxis/config.json` → `models`** (per-repo, user-owned). When present,
   it wins:

   ```json
   {
     "models": {
       "light": "haiku",
       "standard": "sonnet",
       "deep": "opus"
     }
   }
   ```

   Values are **runtime-specific model identifiers, opaque to praxis** — an
   alias, a full model id, whatever the runtime accepts. On Claude Code you can
   map `deep` to a higher tier where your plan offers one (e.g. `fable`, the
   Mythos-class tier above Opus) or pin exact ids; on Codex you map the tiers
   to the OpenAI models your runtime exposes.

2. **Runtime defaults**, when the config has no `models` map:

   | Runtime | `light` | `standard` | `deep` |
   | ------- | ------- | ---------- | ------ |
   | Claude Code | `haiku` | `sonnet` | `opus` |
   | Single-conversation runtimes (Codex, Cursor, Junie) | — the runtime's configured model — | | |

   Single-conversation runtimes cannot switch models per phase; there the tiers
   are **advisory** — they still tell you where to spend care and iteration,
   and the config documents the team's intent for runtimes that can switch.

## Doctrine

- **Commands name tiers, never models.** A command that hardcodes a vendor
  model name is a defect — fix the command, not the config.
- **Default `standard`, escalate deliberately.** Cheap by default; depth where
  it pays; surface the choice to the user.
- **`light` is retrieval-only.** It condenses and locates; it never decides.
- **The config is the abstraction boundary.** Repo owners set `models` once per
  repo and every praxis command follows it — no per-command overrides to chase.
