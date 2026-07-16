# Asbir Sans Roadmap

## Product direction

Asbir Sans 1.0.0 is the stable foundation: nine static weights, a two-axis variable font, and production-approved Latin, Greek, Cyrillic, and Vietnamese coverage. Future work should make that release easier to adopt and maintain before expanding the family.

## Release 1.0.1 — Adoption hardening

**Timing:** Next 2–4 weeks

**Goal:** Make installation, web use, and support as dependable as the font files themselves.

- Publish a webfont package: variable and static WOFF2 files, a small CSS stylesheet, and clear licensing/install instructions.
- Test the existing OTF, TTF, and variable TTF on current macOS, Windows, Adobe apps, and Chrome, Safari, Firefox, and Edge.
- Add a concise changelog, versioning policy, and checksums to every public release.
- Keep one feedback route for spacing, rendering, language, and installation reports; turn each confirmed issue into a reproducible proof sample.
- Maintain the release script so every ZIP is rebuilt from approved binaries, with the same `OTF`, `TTF`, and `Variable` layout.

**Exit criteria:** A designer and an engineer can install or use the family on web without asking for conversion, file-selection, or licensing help.

## Release 1.1 — Language and text-quality revision

**Timing:** 1–3 months

**Goal:** Improve confidence in the existing repertoire through real usage rather than adding scripts prematurely.

- Arrange native-reader proof reviews for Greek, Cyrillic, and Vietnamese; track feedback by glyph, language, size, and context.
- Build a targeted backlog for spacing, kerning, punctuation, currency, mathematical signs, arrows, and numerals found in product UI and longer reading samples.
- Validate all corrections across static instances and the `wght` / `opsz` variable space using the existing shaping and FontBakery gates.
- Investigate variable-font file size only if it creates a real delivery problem; any optimization must preserve shaping and interpolation behaviour.

**Exit criteria:** All reported language and text-quality issues are either corrected, documented as intentional, or deferred with a named owner and proof case.

## Release 1.2 — Web and design-system distribution

**Timing:** 3–6 months

**Goal:** Make Asbir Sans an easy default for product teams.

- Provide documented WOFF2 loading recipes for the full variable font and static fallbacks.
- Define optional language subsets only after measuring actual product-language needs; preserve one full-font option.
- Publish type-scale, line-height, tracking, numeral-feature, and optical-size guidance for interface, body, and display use.
- Supply Figma-ready text styles and a short specimen that demonstrates UI, dashboard, editorial, and multilingual settings.

**Exit criteria:** A product team can implement a consistent Asbir Sans system from a single handoff page without custom typography decisions.

## Version 2.0 — Deliberate family expansion

**Timing:** After adoption evidence, not on a calendar deadline

**Goal:** Add the highest-value new capability without weakening the core family.

- Prioritise a true italic family if product and editorial usage shows a need. It should be drawn as an italic, not a mechanically slanted roman.
- Consider a grade axis only if UI rendering or dark-mode usage reveals a measurable need beyond the current weight axis.
- Add new writing systems only with a native-script design/review owner and an ongoing maintenance commitment.

**Exit criteria:** The expansion has a documented use case, named review ownership, source compatibility plan, and full release QA coverage.

## What stays separate

Asbir Mono remains a review build and Asbir Serif remains paused. Their release decisions should not delay or redefine the Asbir Sans roadmap.

## Immediate priority order

1. WOFF2 + CSS web package.
2. Cross-platform compatibility matrix and public changelog.
3. Native-language proof review and issue intake.
4. Design-system guidance and Figma text styles.
5. Decide on true italics from real adoption data.
