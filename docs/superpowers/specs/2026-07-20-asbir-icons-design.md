# Asbir Icons — Soft UI Icon Library Design

## Goal

Create a standalone Asbir UI icon library inside the existing Asbir type studio. The first release is a general-purpose web and product UI collection with 150–250 semantic icons, paired outline and filled variants, an SVG-first download workflow, and ReIcon-inspired browse and developer handoff pages.

The library must be maintainable as new icons are added and as future Asbir packs introduce different usage or personality directions.

## Product decisions

- Product name: `Asbir Icons`.
- First pack: `Soft`.
- Audience: web designers and product engineers building general web and product interfaces.
- Initial size: 150–250 semantic icons, each with an outline and filled variant.
- Geometry: conventional `24 × 24` UI grid, soft rounded construction, rounded caps and joins, a base outline stroke width of `2`, and consistent optical padding.
- Delivery: original SVGs are canonical; PNG and WebP are generated exports.
- License: MIT.
- Website shape: existing Asbir type studio at `/`, icon browser at `/icons`, and deep-linkable icon pages at `/icon/:slug`.
- Architecture: retain the current Vite and vanilla JavaScript application; add a route-aware icon module without migrating the application to a framework.
- Future packs: share the catalog, renderer, browser, detail-page system, export behavior, and QA contracts while keeping their artwork and metadata separate.

## Scope

### Included in the first release

- A `Soft` pack with 150–250 semantic icons.
- Matched `outline` and `filled` SVG assets for every icon.
- General-purpose categories: Actions, Arrows, Communication, Commerce, Content, Devices, Files, Interface, Location, Media, Navigation, People, Security, Status, and Time.
- Search by display name, stable slug, alias, and keyword.
- Category, pack, and outline/filled filters.
- Responsive icon grid.
- Individual icon detail pages.
- SVG, PNG, and WebP downloads at selectable sizes.
- Copy Name, Copy SVG, and copy-ready code examples.
- Contextual UI examples for every icon page.
- Related-icon recommendations.
- MIT license, release README, manifest, and changelog.
- Automated asset/catalog and route checks.

### Explicitly deferred

- An installable npm package.
- A Figma plugin or Figma component library.
- A custom icon drawing editor.
- An icon font.
- User accounts, favorites, collections, or uploads.
- A separate Asbir Icons repository or application.
- Additional packs beyond the `Soft` pack’s data model and selector support.

## Routes and navigation

The current type studio remains the root experience.

| Route | Behavior |
| --- | --- |
| `/` | Render the existing Asbir type studio without changing its family/specimen state model. |
| `/icons` | Browse the default `Soft` pack. |
| `/icons?pack=soft&category=navigation&q=arrow` | Browse with URL-persisted pack, category, and search state. |
| `/icon/:slug` | Render an icon from the default `Soft` pack. |
| `/icon/:pack/:slug` | Reserved for future non-default packs and duplicate slugs. |
| Unknown path or slug | Render an accessible not-found state with a direct link back to `/icons`. |

Internal navigation should use normal links so deep links remain copyable, bookmarkable, and usable without JavaScript-enhanced click handlers. The client may use `history.pushState` for filter changes when it improves responsiveness, but the URL must remain the source of truth after refresh.

The production deployment must serve the application entry point for `/icons` and `/icon/...` so direct navigation and refresh work on Vercel. The implementation plan must add the smallest Vercel rewrite configuration required for this fallback without altering download paths.

## Browse experience

The browse surface should take the efficient library-discovery approach shown by the ReIcon reference while using Asbir’s existing dark editorial system.

### Header and discovery controls

- Identify the product as `Asbir Icons` and the active pack as `Soft`.
- Show the total semantic icon count and the fact that outline and filled variants are available.
- Provide one prominent search field with a visible keyboard shortcut hint where practical.
- Keep pack selection available from the same control area so future packs do not require a new page architecture.
- Provide category filters using the approved category set.
- Provide an outline/filled filter with a neutral `All` option.
- Keep all filter state in query parameters so filtered collections can be shared.

### Icon grid

- Use a dense, responsive grid suitable for scanning a 150–250 icon collection.
- Each tile is an accessible link to `/icon/:slug` or the future pack-qualified route.
- The tile shows the icon, display name, and category; the visual is the primary material.
- Hover and focus states may expose a quiet quick-copy affordance, but the tile’s main action remains navigation to the detail page.
- Do not put full export controls into every tile; that would compete with discovery and duplicate the detail surface.

### Browse states

- Default: all icons in the selected pack, grouped only by the active filter state.
- Search results: filtered grid with result count and a clear-search action.
- Category results: filtered grid with category label and result count.
- No results: a clear message, reset action, and a small set of nearby category suggestions.
- Future pack: pack description, version, count, and the same grid behavior.
- Loading or catalog failure: a compact status message with a retry action; build-time catalog failures should fail the build before this state is reachable in production.

## Individual icon experience

The individual page is a developer handoff and proof surface, not only a larger preview.

### Page header

- Breadcrumbs identify `Asbir Icons`, the active pack, category, and icon name.
- A visible Back link returns to the previous browse context when possible and otherwise returns to `/icons`.
- The icon name, category, stable slug, and pack/version are visible near the primary proof area.

### Preview and customization

- Show the selected outline or filled asset inside a 24×24 grid.
- Show the current export size and a small set of selectable sizes: `16`, `24`, `32`, `48`, `64`, `128`, `256`, and `512`.
- Provide an outline/filled control labelled as a weight or variant selector.
- Provide a custom-color control that changes the preview and generated exports without modifying the source asset.
- Keep the source asset `currentColor`-based and preserve the original path data when color is not customized.

### Actions and exports

Provide these primary actions in a grouped utility panel:

- `Copy Name` copies the stable display-friendly identifier.
- `Copy SVG` copies the selected variant as normalized inline SVG.
- `Copy JSX` copies a copy-ready JSX representation of the selected variant.
- `SVG`, `PNG`, and `WebP` download actions export the selected variant at the active size.

SVG is the source of truth. The browser generates PNG and WebP from the selected SVG at download time and the active export size; they must not become separately maintained artwork. If browser rasterization fails, the page preserves SVG download and reports the unavailable raster format.

### Code examples

The page includes copy-ready examples generated from the same canonical SVG and manifest record. The initial tabs are:

- JS
- CDN
- React
- React Native
- Vue
- Svelte
- Flutter
- Direct

These examples must be self-contained or use a stable hosted SVG path. They must not claim that an installable package exists before a package is actually published. The examples are documentation output in v1; package publishing is deferred.

### Props and documentation

Show a compact props table for the generated component examples. At minimum it documents:

- `size`
- `color`
- `weight` or variant equivalent
- `className` or framework-specific class hook where applicable

Descriptions must explain what the property controls, its accepted type, and its default. The table is generated from the same icon/component contract used by the code examples so it cannot drift independently.

### In-context section

Every icon page includes a full-width contextual section with six standardized UI examples:

1. Sidebar navigation.
2. Buttons, including primary and secondary states.
3. Metric card.
4. Notification.
5. Input field, including disabled or placeholder state where appropriate.
6. Bottom tab bar.

The examples use the icon in realistic UI hierarchy rather than displaying isolated decorative boxes. The icon’s active state, muted state, and filled/outline choice should be visible when that helps explain usage.

### Related icons

End each detail page with a small related-icon row driven by explicit manifest relationships and shared keywords/categories. Related icons are links, not a second browse grid.

## Source-of-truth model

The icon system is data-driven and pack-aware.

### Asset contract

Each semantic icon has a stable slug and two canonical files:

- `outline.svg`
- `filled.svg`

Every SVG must:

- Use `viewBox="0 0 24 24"`.
- Use the 24×24 coordinate system.
- Use `currentColor` rather than hard-coded brand colors.
- Use rounded caps and joins for outline construction.
- Use a base outline stroke width of `2` with documented optical corrections only when required for the individual shape.
- Have intentional optical padding and remain legible at 16px, 24px, and 32px.
- Contain no raster images, external references, scripts, or embedded fonts.
- Be valid, normalized SVG suitable for inline use and download.

### Manifest contract

Each record contains:

- `pack`
- `slug`
- `name`
- `category`
- `aliases`
- `keywords`
- `outlineAsset`
- `filledAsset`
- `related`
- `contextExamples`
- `introducedIn`

The manifest is the only source used to populate browse results, detail-page metadata, code examples, props documentation, related icons, counts, and release inventories.

### Conceptual repository boundary

The implementation should keep icon concerns separate from the existing type specimen concerns. The approved boundary is:

- `src/icons/catalog.js` — pack and icon metadata.
- `src/icons/router.js` — pathname matching and icon-route selection.
- `src/icons/browse.js` — browse page rendering and browse state.
- `src/icons/detail.js` — individual icon page rendering and detail state.
- `src/icons/render.js` — SVG normalization, variant selection, and code/export rendering helpers.
- `src/icons/packs/soft/` — Soft-pack SVG assets and pack-specific metadata.

The exact final split may follow existing project conventions, but icon rendering and data must not be embedded as large page-specific literal blocks inside the existing type-family renderer.

## Update and release workflow

Adding an icon follows the same repeatable sequence:

1. Draw the outline and filled pair on the 24×24 grid.
2. Assign a unique kebab-case slug and human-readable name.
3. Add aliases, keywords, category, pack, related icons, and context examples to the manifest.
4. Run SVG and manifest validation.
5. Verify both variants through the browse route and detail route.
6. Verify copy output and SVG/PNG/WebP exports at the required sizes.
7. Add the change to the changelog.
8. Bump the pack version according to the release policy.
9. Build the site and release archive.

Version policy:

- `1.0.0`: first approved Soft pack release.
- Minor release, such as `1.1.0`: new icons or additive metadata/context improvements.
- Patch release, such as `1.0.1`: corrections that preserve the existing icon meaning and slug.
- Major release, such as `2.0.0`: breaking slug changes, removals, or incompatible asset/component contracts.

The initial downloadable archive is `AsbirIcons-Soft-1.0.0.zip`. It contains:

- SVG outline assets.
- SVG filled assets.
- `manifest.json`.
- `README.md` with installation, usage, and naming guidance.
- `LICENSE` containing the MIT license.
- `CHANGELOG.md`.

The release layout must distinguish canonical source assets from generated website outputs and must not include unrelated font files.

## Accessibility and interaction requirements

- Use real links for icon tiles, breadcrumbs, related icons, and downloads.
- Use real buttons for copy, variant, size, color, filter, and code-tab controls.
- Every icon tile has an accessible name containing the icon name and pack context.
- Standalone preview icons receive an accessible label; decorative icons in UI examples use `aria-hidden="true"` when adjacent text already communicates their purpose.
- Copy actions expose success and failure through a `role="status"` live region.
- Clipboard failure provides a visible fallback that lets the user select or download the code instead.
- Code tabs use an accessible tablist/tab/tabpanel relationship and remain keyboard navigable.
- Focus moves to the new page heading after a route change when the change is initiated through client-side navigation.
- Search and filter controls remain usable with keyboard navigation and do not depend on color alone.
- Controls meet WCAG AA contrast against the dark Asbir surface.
- Motion is subtle and disabled or reduced under `prefers-reduced-motion: reduce`.
- The layout must remain usable at narrow mobile widths without horizontal scrolling.

## Error handling

- Invalid icon slug: show the icon-library not-found state with a browse link and a search recovery path.
- Invalid future pack: show a pack-not-found state with available-pack links.
- Empty search result: show the query, a reset action, and suggested categories.
- Clipboard unavailable or denied: preserve the code on screen and offer download/select fallback.
- Raster export failure: keep SVG download available and explain the failed format without losing the current page state.
- Malformed SVG, missing paired variant, duplicate slug, missing manifest field, or broken related-icon reference: fail icon QA/build validation with an actionable error rather than silently shipping a partial pack.

## Verification

The implementation is not complete until all of the following are verified:

- Every manifest record has exactly one outline and one filled asset.
- All slugs are unique within their pack and route resolution is deterministic.
- Every SVG passes XML/SVG validation and the 24×24/viewBox/color/asset contract.
- Browse search, category filters, variant filters, pack selection, and URL persistence work after refresh.
- Every icon detail route loads directly on a production preview.
- Copy Name, Copy SVG, Copy JSX, and code-tab copy actions return the selected icon variant.
- SVG, PNG, and WebP exports work at 16, 24, 32, 48, 64, 128, 256, and 512px.
- Outline and filled controls change both preview and generated output.
- Related icons resolve to existing routes.
- Not-found, no-results, clipboard-failure, and export-failure states are reachable and understandable.
- Keyboard navigation, focus behavior, screen-reader labels, reduced motion, and narrow-screen layout are checked manually.
- Existing `/` type studio behavior remains unchanged.
- The full project build and the icon-specific QA suite pass.
- The release archive contains only the approved Soft-pack assets and documentation.

## Non-goals and design guardrails

- Do not copy ReIcon’s SVG artwork, icon names as a bulk set, code, or visual branding.
- Do not turn the icon detail page into an editable drawing application.
- Do not introduce a second unrelated design language inside the Asbir site.
- Do not make framework snippets imply a published package that does not exist.
- Do not hand-maintain a separate page for every icon.
- Do not add new packs by forking the browse/detail implementation.
- Do not let generated PNG/WebP files become the design source.
