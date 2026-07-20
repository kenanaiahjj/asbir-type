# Asbir Icons — Soft 1.0.0

Asbir Icons is an original, soft-rounded SVG icon pack for general web and product UI. This release contains 180 semantic icons, each with matched `outline` and `filled` variants.

## Contents

- `icons/soft/<slug>/outline.svg` — canonical outline artwork.
- `icons/soft/<slug>/filled.svg` — canonical filled artwork.
- `manifest.json` — names, categories, aliases, keywords, relationships, and asset paths.
- `LICENSE` — MIT license for the icon artwork and metadata.
- `CHANGELOG.md` — release history.

## Usage

Use an SVG directly in HTML:

```html
<img src="icons/soft/search/outline.svg" alt="Search">
```

Or inline the SVG when you want to control its color with CSS. The canonical files use `currentColor`, a `24 24` viewBox, and rounded construction. Preserve the `viewBox` when resizing.

Stable names use lowercase kebab-case slugs. Search the manifest for aliases and keywords when mapping product concepts to icons. Outline and filled are semantic variants of the same icon; choose one consistently within a UI surface.

## License

The icons and metadata in this archive are released under the MIT License. See `LICENSE` for the full text.
