# UX Comprehension and Friction

UX is whether the right user can understand the offer or interface, decide confidently, and take the next step with minimal unnecessary friction. Run discovery first; then apply only the UX lenses the screen needs.

## Discovery (run at the start of every generation)

Answer four questions in order; each shapes the next. Use the spec or prompt when it answers one; ask one clarifying question only when ambiguity would change the design.

1. **Who is the user?** Pick the single most relevant persona. Capture role, domain literacy (beginner vs expert), frequency (once vs daily vs hourly), channel (desktop vs mobile vs mixed), and context.
2. **What is the job?** One sentence: "[User] needs to [action] so that [outcome], before [next step / deadline / failure cost]." If you cannot complete it, ask.
3. **What is the failure cost?** High (financial, regulatory, irreversible) earns safe defaults, double-confirmation, explicit copy, redundant signals. Medium earns standard confirmations and clear errors. Low earns minimal friction. Push past the lazy "medium".
4. **What is the smallest screen that solves it?** Name the one primary action, the 3 to 5 pieces of context needed to take it, what is deferred, and what is removed.

Capture the answers as a short discovery line before any code:

- User: role + literacy + frequency + channel
- Job: one sentence
- Failure cost: high / medium / low + why
- Smallest screen: primary action + context + what is deferred
- Surface direction: product / utility / landing / expressive

## Comprehension

Apply the five-second test: on first impression, can the user say what this is, who it is for, and what to do next? Diagnose comprehension before aesthetics. Separate visual taste from a real decision failure. Use the user's own language, not internal jargon.

## Intent-stage fit

Match the page to the user's readiness. An unaware visitor needs the problem framed; a product-aware visitor needs specifics and a clear next step. Do not show ready-to-buy density to a first-touch visitor, or first-touch education to someone trying to finish a task.

## Forms and friction

Reduce burden to the minimum that serves the job. Ask only for what is needed now; defer the rest. Match commitment to failure cost. Validate inline and recover gracefully. Do not auto-advance focus in ways that break correction. Every field earns its place; a field used by a minority goes behind disclosure.

## Objection, trust, and proof

When the experience asks for belief, money, data, or commitment, map each claim to evidence and place the proof near the claim it supports. Surface the user's likely objections and answer them where they arise. Higher stakes need more explicit trust signals; do not fabricate metrics, testimonials, or certifications.

## Navigation and routing

Make the right route findable and the current location clear. Match navigation to page type and stage: product surfaces usually need persistent navigation; focused flows may reduce exits. Give the user control: clear Back, Cancel, and escape paths. Do not remove navigation, pricing, or content without checking the page type.

## Quality rules

- Do not encode "short attention span" as universal truth; users spend time when relevance is clear.
- Map every major recommendation to user intent, belief, risk, friction, or task completion.
- State assumptions when the only evidence is a screenshot or opinion.

## Gate

- **Inspect**: the brief, the user, and the task stage.
- **Decide**: the discovery line, and which UX lenses bind (comprehension, intent-stage, forms, proof, navigation) and what each implies for this screen.
- **Record** under gate id `G-ux`: the discovery line, the failure-cost level and its friction implications, and the specific UX fixes applied (for example, "deferred 6 optional KYC fields behind disclosure to cut a high-failure-cost onboarding form to 4 visible fields"). Always applies.
