# Asbir Icons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first Asbir Icons Soft pack and its `/icons` browser plus `/icon/:slug` developer handoff pages inside the existing Vite type studio.

**Architecture:** Keep the existing vanilla JavaScript/Vite application and add an isolated `src/icons/` route and rendering boundary. Canonical SVG assets and a generated JSON manifest drive browse pages, detail pages, exports, code examples, release packaging, and future pack support. The existing type studio remains the root route and keeps its current renderer/state behavior.

**Tech Stack:** Vite 7, browser-native JavaScript modules, semantic HTML/CSS, Python 3 standard library for asset/catalog generation and release packaging, Node `node:test` for pure JavaScript contracts, Python `unittest` for asset/release contracts.

## Global Constraints

- First pack is `Soft` and contains 150–250 semantic icons.
- Every semantic icon has matched `outline` and `filled` SVG variants.
- Every SVG uses a `24 × 24` viewBox, base outline stroke width `2`, rounded caps/joins, `currentColor`, and no external references.
- SVG is canonical; browser-generated PNG and WebP are derived exports and never maintained as source artwork.
- Routes are `/`, `/icons`, `/icon/:slug`, and future `/icon/:pack/:slug`.
- The current root type studio must remain behaviorally unchanged.
- The icon pack is MIT licensed.
- No npm package, Figma plugin, icon font, user accounts, or custom drawing editor is included.
- Do not copy ReIcon artwork, code, bulk naming, or branding.
- Preserve all unrelated dirty working-tree changes.

---

## File map

### New files

- `src/icons/catalog.json` — generated pack/version/icon metadata.
- `src/icons/catalog.js` — catalog lookup, filters, pack/category helpers, and asset URLs.
- `src/icons/router.js` — pathname/query parsing and URL builders.
- `src/icons/render.js` — HTML escaping, SVG normalization, code examples, and raster export helpers.
- `src/icons/browse.js` — `/icons` page rendering.
- `src/icons/detail.js` — `/icon/:slug` page rendering.
- `src/icons/app.js` — route mounting, navigation, clipboard, exports, and status feedback.
- `src/icons/icons.css` — icon-only layout, responsive, focus, and reduced-motion rules.
- `tools/generate_icon_pack.py` — deterministic original Soft-pack SVG and manifest generator.
- `tools/package_asbir_icons_release.py` — release archive builder.
- `tests/test_icon_pack_contract.py` — Python asset, manifest, SVG, and count tests.
- `tests/test_asbir_icons_release.py` — Python release archive tests.
- `tests/icons.test.mjs` — JavaScript route, filter, and rendering tests.
- `public/icons/soft/` — generated browser assets.
- `release/AsbirIcons-Soft-1.0.0/` and `release/AsbirIcons-Soft-1.0.0.zip` — generated release outputs.
- `vercel.json` — SPA fallback rewrites, if no existing deployment config provides them.

### Modified files

- `src/main.js` — delegate non-root routes without changing existing type-studio functions.
- `index.html` — retain safe root defaults; route titles are set by JavaScript.
- `package.json` — add icon generation, tests, and packaging scripts.

---

## Task 1: Establish the original Soft asset and manifest contract

**Files:**

- Create: `tests/test_icon_pack_contract.py`
- Create: `tools/generate_icon_pack.py`
- Create: `src/icons/catalog.json`
- Create: `public/icons/soft/**` generated SVG assets
- Modify: `package.json`

**Interfaces:**

- `python3 tools/generate_icon_pack.py --pack soft --version 1.0.0` is deterministic and rerunnable.
- `catalog.json` has `version`, `license`, `packs`, and `icons` fields.
- Each icon has `pack`, `slug`, `name`, `category`, `aliases`, `keywords`, `outlineAsset`, `filledAsset`, `related`, `contextExamples`, and `introducedIn`.
- Each icon produces `/icons/soft/<slug>/outline.svg` and `/icons/soft/<slug>/filled.svg`.

- [ ] **Step 1: Write failing Python contract tests**

```python
import json
import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).parents[1]

class IconPackContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'src/icons/catalog.json').read_text())
        cls.icons = cls.catalog['icons']

    def test_soft_pack_has_150_to_250_semantic_icons(self):
        self.assertGreaterEqual(len(self.icons), 150)
        self.assertLessEqual(len(self.icons), 250)
        self.assertEqual({icon['pack'] for icon in self.icons}, {'soft'})

    def test_every_record_has_unique_slug_and_required_metadata(self):
        slugs = [icon['slug'] for icon in self.icons]
        self.assertEqual(len(slugs), len(set(slugs)))
        required = {'pack', 'slug', 'name', 'category', 'aliases', 'keywords', 'outlineAsset', 'filledAsset', 'related', 'contextExamples', 'introducedIn'}
        for icon in self.icons:
            self.assertTrue(required.issubset(icon))
            self.assertRegex(icon['slug'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

    def test_every_record_has_valid_outline_and_filled_svg(self):
        for icon in self.icons:
            for field in ('outlineAsset', 'filledAsset'):
                path = ROOT / icon[field].lstrip('/')
                self.assertTrue(path.exists(), path)
                root = ElementTree.fromstring(path.read_text())
                self.assertEqual(root.attrib.get('viewBox'), '0 0 24 24')
                source = path.read_text()
                self.assertIn('currentColor', source)
                self.assertNotRegex(source, r'https?://')

    def test_related_references_resolve(self):
        slugs = {icon['slug'] for icon in self.icons}
        for icon in self.icons:
            self.assertTrue(set(icon['related']).issubset(slugs), icon['slug'])

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the expected red state**

Run: `python3 -m unittest tests.test_icon_pack_contract -v`

Expected: FAIL because the catalog and generated assets do not exist.

- [ ] **Step 3: Implement the deterministic generator**

Implement `tools/generate_icon_pack.py` with a literal grouped specification containing 150–250 original named icons distributed across Actions, Arrows, Communication, Commerce, Content, Devices, Files, Interface, Location, Media, Navigation, People, Security, Status, and Time. Use original rounded geometric primitives; do not import or copy an external icon set.

The generator must use this output contract:

```python
VIEWBOX = '0 0 24 24'

def icon_svg(parts, variant):
    style = (
        'fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"'
        if variant == 'outline' else
        'fill="currentColor" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"'
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" aria-hidden="true"><g {style}>{parts}</g></svg>\n'
```

Each record must assign aliases, keywords, category, context examples, and related references only after all slugs are known. Related references must be existing slugs.

- [ ] **Step 4: Generate and verify the first Soft catalog**

Run: `python3 tools/generate_icon_pack.py --pack soft --version 1.0.0 && python3 -m unittest tests.test_icon_pack_contract -v`

Expected: generation prints the count and the contract tests pass.

- [ ] **Step 5: Add package scripts and commit**

Add these scripts to `package.json`:

```json
{
  "icons:generate": "python3 tools/generate_icon_pack.py --pack soft --version 1.0.0",
  "test:icons:python": "python3 -m unittest tests.test_icon_pack_contract tests.test_asbir_icons_release -v",
  "test:icons": "node --test tests/icons.test.mjs",
  "package:icons": "python3 tools/package_asbir_icons_release.py --pack soft --version 1.0.0"
}
```

```bash
git add tools/generate_icon_pack.py src/icons/catalog.json public/icons/soft tests/test_icon_pack_contract.py package.json
git commit -m "feat: add Asbir Icons Soft asset contract"
```

---

## Task 2: Add pure catalog, route, SVG, and code helpers

**Files:**

- Create: `src/icons/catalog.js`
- Create: `src/icons/router.js`
- Create: `src/icons/render.js`
- Create: `tests/icons.test.mjs`

**Interfaces:**

- `getIcon(pack, slug) -> icon | null`
- `filterIcons({ pack, query, category, variant }) -> icon[]`
- `getCategories(pack) -> string[]`
- `iconAssetUrl(icon, variant) -> string`
- `parseRoute(pathname, search) -> route object`
- `browseHref(filters) -> string`
- `iconHref(pack, slug) -> string`
- `renderInlineSvg(svg, { size, color }) -> string`
- `codeExamples(icon, variant, svg) -> object`

- [ ] **Step 1: Write failing Node tests**

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { filterIcons, getIcon } from '../src/icons/catalog.js';
import { browseHref, iconHref, parseRoute } from '../src/icons/router.js';

test('parses browse filters and default detail routes', () => {
  assert.deepEqual(parseRoute('/icons', '?pack=soft&category=Navigation&q=arrow'), {
    kind: 'browse', pack: 'soft', category: 'Navigation', query: 'arrow', variant: 'all',
  });
  assert.deepEqual(parseRoute('/icon/search', ''), { kind: 'detail', pack: 'soft', slug: 'search' });
});

test('builds shareable links', () => {
  assert.equal(browseHref({ pack: 'soft', category: 'Navigation', query: 'arrow', variant: 'outline' }), '/icons?pack=soft&category=Navigation&q=arrow&variant=outline');
  assert.equal(iconHref('soft', 'search'), '/icon/search');
  assert.equal(iconHref('technical', 'terminal'), '/icon/technical/terminal');
});

test('filters semantic records without duplicating outline and filled variants', () => {
  const results = filterIcons({ pack: 'soft', query: 'search', category: 'all', variant: 'filled' });
  assert.ok(results.length >= 1);
  assert.ok(results.every(icon => icon.pack === 'soft'));
  assert.equal(getIcon('soft', results[0].slug).slug, results[0].slug);
});
```

- [ ] **Step 2: Run the tests and verify the expected red state**

Run: `npm run test:icons`

Expected: FAIL because the catalog and helper modules do not exist.

- [ ] **Step 3: Implement the helpers**

Import `catalog.json` in `catalog.js`; match `name`, `slug`, aliases, and keywords case-insensitively; return one semantic record per result. `router.js` uses `URLSearchParams`, defaults missing pack to `soft`, category to `all`, and variant to `all`, and classifies `/` as `studio` and unknown paths as `not-found`. `renderInlineSvg` preserves `viewBox="0 0 24 24"`, applies requested size/color, and rejects scripts or external URLs. `codeExamples` generates self-contained inline-SVG examples; the CDN tab uses the stable hosted SVG path and does not claim an unpublished package.

- [ ] **Step 4: Run tests and commit**

Run: `npm run test:icons`

Expected: PASS.

```bash
git add src/icons/catalog.js src/icons/router.js src/icons/render.js tests/icons.test.mjs
git commit -m "feat: add Asbir Icons catalog and route helpers"
```

---

## Task 3: Build browse/detail renderers and interactions

**Files:**

- Create: `src/icons/browse.js`
- Create: `src/icons/detail.js`
- Create: `src/icons/app.js`
- Create: `src/icons/icons.css`
- Modify: `tests/icons.test.mjs`

**Interfaces:**

- `renderBrowsePage(route) -> string`
- `renderDetailPage(route) -> string`
- `mountIconRoute(root) -> boolean`
- `copyText(text) -> Promise<boolean>`
- `downloadSvg(icon, variant, size, color) -> Promise<void>`

- [ ] **Step 1: Write failing renderer contract tests**

```js
import { renderBrowsePage } from '../src/icons/browse.js';
import { renderDetailPage } from '../src/icons/detail.js';

test('browse markup includes accessible search, filters, grid links, and pack metadata', () => {
  const html = renderBrowsePage({ kind: 'browse', pack: 'soft', category: 'all', query: '', variant: 'all' });
  assert.match(html, /aria-label="Search icons"/);
  assert.match(html, /data-icon-grid/);
  assert.match(html, /href="\/icon\//);
  assert.match(html, /Soft/);
});

test('detail markup includes exports, code tabs, props, context, and related links', () => {
  const html = renderDetailPage({ kind: 'detail', pack: 'soft', slug: 'search' });
  for (const label of ['Copy Name', 'Copy SVG', 'SVG', 'PNG', 'WebP', 'React', 'Props', 'In context', 'Related icons']) {
    assert.match(html, new RegExp(label));
  }
  assert.match(html, /aria-label="Outline or filled variant"/);
});
```

- [ ] **Step 2: Run renderer tests and verify red**

Run: `npm run test:icons`

Expected: FAIL until the page modules export the render functions.

- [ ] **Step 3: Implement browse markup**

Render an Asbir Icons header, Soft/version metadata, labelled search, pack/category/variant controls, result count, no-results state, and dense responsive grid. Each tile is an `<a>` with an accessible name containing icon name and pack, an image from `iconAssetUrl`, visible name, and category. Preserve filter state in generated links.

- [ ] **Step 4: Implement detail markup**

Render breadcrumbs, back link, 24×24 grid preview, outline/filled control, size controls `16/24/32/48/64/128/256/512`, custom color, Copy Name/JSX/SVG actions, SVG/PNG/WebP buttons, JS/CDN/React/React Native/Vue/Svelte/Flutter/Direct tabs, props table, six contextual examples, and related links. Load canonical SVG asynchronously for copy/code/export panels without replacing the page shell.

- [ ] **Step 5: Implement route mounting and export behavior**

`mountIconRoute(root)` handles icon and not-found routes, sets the title, binds normal links plus `history.pushState` filter changes, handles `popstate`, focuses the page heading, and exposes copy status in a `role="status"` region. SVG downloads use normalized source; PNG/WebP rasterize the selected SVG into a canvas at the selected size. Raster failure preserves SVG and reports the unavailable format.

- [ ] **Step 6: Implement isolated responsive CSS**

Prefix icon selectors with `.icon-app`/`.icon-surface`. Add dark Asbir surfaces, restrained borders, warm orange interaction accent, rounded controls, dense grid, ReIcon-style detail split, code panel, props table, six contextual cards, related row, mobile stacking, visible focus, and reduced-motion behavior.

- [ ] **Step 7: Run tests and commit**

Run: `npm run test:icons`

Expected: PASS.

```bash
git add src/icons/browse.js src/icons/detail.js src/icons/app.js src/icons/icons.css tests/icons.test.mjs
git commit -m "feat: add Asbir Icons browse and detail pages"
```

---

## Task 4: Integrate icon routing without changing the type studio

**Files:**

- Modify: `src/main.js`
- Modify: `index.html`
- Create or modify: `vercel.json`
- Modify: `tests/icons.test.mjs`

**Interfaces:**

- Root route calls the existing `render()` and `bind()` lifecycle.
- Icon routes call `mountIconRoute(app)` and never initialize type specimen controls.
- Browser back/forward switches between icon and type-studio routes.

- [ ] **Step 1: Write a failing root/delegation contract**

```js
test('classifies the root and error routes for main-entry delegation', () => {
  assert.deepEqual(parseRoute('/', ''), { kind: 'studio' });
  assert.deepEqual(parseRoute('/missing', ''), { kind: 'not-found' });
});
```

- [ ] **Step 2: Run the contract and verify red**

Run: `npm run test:icons`

Expected: FAIL until `parseRoute` returns the root and not-found route objects.

- [ ] **Step 3: Add the smallest main-entry delegation**

Import `mountIconRoute` at the top of `src/main.js` and replace the unconditional final `render();` with:

```js
function renderCurrentRoute() {
  if (!mountIconRoute(app)) render();
}

window.addEventListener('popstate', renderCurrentRoute);
renderCurrentRoute();
```

Keep existing type-studio functions and selectors unchanged. Icon rendering removes icon-only root/body classes before root rendering; root rendering removes them before type content.

- [ ] **Step 4: Set route-aware metadata**

Keep `index.html`’s safe default title. The icon app sets `Asbir Icons — Browse` or `Asbir Icons — <Icon Name>`, and root rendering restores `Asbir Sans Studio`.

- [ ] **Step 5: Add Vercel SPA fallback rewrites**

If no deployment config exists, create:

```json
{
  "rewrites": [
    { "source": "/icons", "destination": "/index.html" },
    { "source": "/icons/:path*", "destination": "/index.html" },
    { "source": "/icon/:path*", "destination": "/index.html" }
  ]
}
```

Do not rewrite `/icons/soft/...svg`, `/downloads/...`, or any other static asset path.

- [ ] **Step 6: Run tests and Vite build**

Run: `npm run test:icons && npm run vercel-build`

Expected: all icon tests pass and Vite writes generated icon assets into `dist/icons/soft`.

- [ ] **Step 7: Commit the route integration**

```bash
git add src/main.js index.html vercel.json src/icons/app.js tests/icons.test.mjs
git commit -m "feat: route Asbir Icons from the type studio"
```

---

## Task 5: Package the MIT Soft release

**Files:**

- Create: `tools/package_asbir_icons_release.py`
- Create: `tests/test_asbir_icons_release.py`
- Create: `public/icons/soft/LICENSE`
- Create: `public/icons/soft/README.md`
- Create: `public/icons/soft/CHANGELOG.md`
- Create: `release/AsbirIcons-Soft-1.0.0/**` generated outputs

**Interfaces:**

- `python3 tools/package_asbir_icons_release.py --pack soft --version 1.0.0` produces a clean release directory and ZIP.
- Release contains outline SVGs, filled SVGs, `manifest.json`, `README.md`, `LICENSE`, and `CHANGELOG.md` only.
- Release tests verify archive members and MIT metadata.

- [ ] **Step 1: Write failing release tests**

```python
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).parents[1]
ARCHIVE = ROOT / 'release' / 'AsbirIcons-Soft-1.0.0.zip'

class AsbirIconsReleaseTests(unittest.TestCase):
    def test_archive_contains_icon_assets_and_no_font_files(self):
        self.assertTrue(ARCHIVE.exists())
        with ZipFile(ARCHIVE) as archive:
            names = set(archive.namelist())
        self.assertIn('AsbirIcons-Soft-1.0.0/manifest.json', names)
        self.assertIn('AsbirIcons-Soft-1.0.0/LICENSE', names)
        self.assertTrue(any(name.endswith('/outline.svg') for name in names))
        self.assertTrue(any(name.endswith('/filled.svg') for name in names))
        self.assertFalse(any(name.endswith(('.ttf', '.otf', '.woff2')) for name in names))

    def test_release_documents_mit_and_version(self):
        with ZipFile(ARCHIVE) as archive:
            license_text = archive.read('AsbirIcons-Soft-1.0.0/LICENSE').decode()
            readme = archive.read('AsbirIcons-Soft-1.0.0/README.md').decode()
        self.assertIn('MIT License', license_text)
        self.assertIn('Asbir Icons Soft 1.0.0', readme)

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run release tests and verify red**

Run: `python3 -m unittest tests.test_asbir_icons_release -v`

Expected: FAIL because the release builder and archive do not exist.

- [ ] **Step 3: Implement deterministic release packaging**

Copy only `public/icons/soft/<slug>/outline.svg` and `filled.svg` into `release/AsbirIcons-Soft-1.0.0/svg/<variant>/`, copy the catalog as `manifest.json`, write the MIT license and usage documents, rebuild only the exact generated release target, and create a ZIP with sorted deterministic members. Do not touch font release files.

- [ ] **Step 4: Add release documents and build**

The README documents version, MIT license, SVG paths, outline/filled variants, 24×24 viewBox, `currentColor`, and usage. The changelog records the initial Soft release. Run:

```bash
python3 tools/package_asbir_icons_release.py --pack soft --version 1.0.0
```

- [ ] **Step 5: Run all Python icon tests and commit**

Run: `npm run test:icons:python`

Expected: asset and release contracts pass.

```bash
git add tools/package_asbir_icons_release.py tests/test_asbir_icons_release.py public/icons/soft/LICENSE public/icons/soft/README.md public/icons/soft/CHANGELOG.md release/AsbirIcons-Soft-1.0.0
git commit -m "release: package Asbir Icons Soft 1.0.0"
```

---

## Task 6: Verify the complete icon experience

**Files:**

- Modify only when a verification defect requires it: `src/icons/**`, `src/main.js`, `index.html`, `vercel.json`, tests, or packaging tools.

- [ ] **Step 1: Run automated icon checks**

Run:

```bash
npm run test:icons
npm run test:icons:python
```

Expected: all JavaScript and Python icon contracts pass.

- [ ] **Step 2: Build the deployable Vite bundle**

Run: `npm run vercel-build`

Expected: Vite succeeds and `dist/icons/soft` contains the generated SVG assets.

- [ ] **Step 3: Run a local preview**

Run: `npm run preview -- --host 127.0.0.1`

Verify `/`, `/icons`, `/icons?category=Navigation&q=arrow`, `/icon/search`, and `/icon/soft/search` directly in the browser.

- [ ] **Step 4: Verify desktop and mobile behavior**

At approximately 1440px and 390px widths, check search, category/pack/variant filters, tile keyboard focus, detail preview, outline/filled switching, all sizes, custom color, copy actions, code tabs, SVG/PNG/WebP downloads, six context examples, related icons, no-results/not-found states, and browser back/forward navigation.

- [ ] **Step 5: Verify accessibility and root regression**

Use keyboard only for all controls. Confirm visible focus, heading focus after route changes, useful accessible names, no color-only states, reduced motion, and no horizontal mobile overflow. Verify root family switching, specimen controls, and the What’s New panel remain unchanged.

- [ ] **Step 6: Inspect the final diff**

Run:

```bash
git status --short
git diff --stat
```

Confirm unrelated existing font/release changes were not staged or modified by the icon work.

- [ ] **Step 7: Report the handoff**

Report routes, release archive path, automated checks, local preview URL, and remaining visual polish items only after the browser verification passes.
