# Imagery, Visuals, and Taste

How expressive the surface should be, what images it uses, and the default-pattern tells to avoid. Most of this binds on landing, marketing, campaign, and brand-expressive surfaces; for quiet product surfaces most of it is softened by the mode's component defaults.

## Surface classification and expression budget

- **Product / SaaS / app**: restrained, mostly quiet, density wins. Imagery is rare (avatars, charts, icons).
- **Utility / internal tool**: most restrained, purely functional, no decoration.
- **Landing / marketing / campaign**: looser, hero allowed, more whitespace, real images required.
- **Brand / expressive / entertainment**: expressive; decoration earns its place by serving the brand.

When in doubt, choose restrained. Declare the class in the discovery line. The most common mistake is over-applying landing taste to a product screen or under-applying it to a marketing page: a product onboarding flow is a title plus a form plus a primary action, not a hero with a stock photo; a marketing page that sells onboarding does get a hero, real imagery, and section variety.

## Read the room

Before composing a marketing surface, declare one line: "Reading this as: [surface class] for [user], with a [vibe] tone." If the brief names a product the user wants it to feel like, say what that is and reach for the matching direction honestly rather than pretending.

## Real images strategy (landing / marketing)

Text-only pages with fake-screenshot divs are slop. Priority: an image-generation tool first when available; then a real photo source (a seeded placeholder photo service, brand assets, open-licence sources); then an explicit placeholder slot as a last resort, with the needed images listed in the chat summary. Never build a fake product UI out of styled div rectangles to simulate a screenshot. Use real SVG logos for any "trusted by" wall, not plain text wordmarks. Even minimalist pages need a few real images.

## Anti-AI-tell catalogue (banned unless the brief justifies them)

Section-numbering eyebrows ("00 / INDEX", "001 . Capabilities"); a decorative colored dot before every nav item or row; the middle-dot used as a separator everywhere (max one per metadata line); italic line-broken headlines as a default move; vertical rotated section labels; crosshair or hairline grid lines as decoration; pills overlaid on images; photo-credit captions on stock images; version footers on marketing pages; locale/time/weather strips in headers and footers; scroll cues ("Scroll", "Scroll to explore"); decoration text strips at the hero bottom; generic placeholder names ("John Doe", "Acme Corp") - use realistic locale-appropriate names and a simple monogram for invented brands.

## Hero and section discipline (landing / marketing)

Hero fits the first viewport: headline at most 2 lines, subtext short, primary CTA visible without scroll, at most four text elements (eyebrow or brand strip, headline, subtext, CTAs). No in-hero trust micro-strip, pricing teaser, or feature list; trust logos go in a dedicated section under the hero. A layout family appears at most once per page; eight sections need at least four families. Bento grids vary cell sizes and have exactly as many cells as items. Navigation renders on one line at desktop. Every CTA passes contrast and does not wrap to two lines.

## Gate

- **Inspect**: the surface class, the imagery needs, and the section plan.
- **Decide**: the expression budget, the images and their source, and which expressive patterns are justified.
- **Record** under gate id `G-imagery`: the surface class and expression budget, the image sources used or the placeholder list, and confirmation that the anti-tell catalogue was honored. Mark not-applicable with one reason for a quiet internal product surface with no imagery.
