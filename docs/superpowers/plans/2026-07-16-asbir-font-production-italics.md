# Asbir Font Production and Italics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote Asbir Mono, add true italic families for Sans and Mono, and ship WOFF2/CSS kits for both.

**Architecture:** Upstream OFL italic masters are imported once into editable UFO/designspace folders, then the existing Asbir feature and naming pipeline compiles Roman and italic review artifacts. A small web-distribution packager converts approved TTFs to WOFF2, writes CSS, and packages the release folders without changing the studio’s proof-only review assets.

**Tech Stack:** Python, glyphsLib, ufoLib2, fontmake/fontTools, Brotli WOFF2 support, HarfBuzz, FontBakery, Vite, Vercel CLI.

## Global Constraints

- Roman and italic are separate variable font files; no mechanically skewed Roman export is accepted as the italic source.
- Asbir Sans Italic retains `opsz` 14–32 and `wght` 100–900.
- Asbir Mono Italic retains `wght` 100–900 and the 600-unit fixed-cell grid.
- Mono production approval is family-specific and cannot reuse the Sans signoff record.
- Both web kits expose normal and italic WOFF2 faces with the correct weight ranges.
- Existing Roman proof assets retain their `Review` filenames until the studio and QA migration is complete.

---

### Task 1: Add failing tests for production signoff and web package contracts

**Files:**
- Create: `tests/test_font_release_contracts.py`
- Create: `tests/test_webfont_package.py`

- [ ] **Step 1: Write the failing tests**

Test that a signoff record must match the selected family, that the Mono production package contains clean names and required folders, and that the web kit contains normal/italic WOFF2 files plus CSS declarations for both families.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest tests/test_font_release_contracts.py tests/test_webfont_package.py -v`

Expected: FAIL because the current signoff is Sans-only, Mono has no production package, and no web kit exists.

### Task 2: Create editable true italic sources

**Files:**
- Create: `tools/generate_italic_sources.py`
- Create: `sources/asbir-sans-italic/AsbirSansItalic.designspace` and its six UFO masters
- Create: `sources/asbir-mono-italic/AsbirMonoItalic.designspace` and its three UFO masters

- [ ] **Step 1: Import OFL upstream italic masters into workspace UFOs**

Import Inter Italic for Sans and Geist Mono Italic for Mono, rename the family/source metadata to Asbir, preserve all foreground contours, and write stable workspace-relative designspaces.

- [ ] **Step 2: Apply Asbir identity and feature layers**

Apply the Sans default `a`, `t`, `G`, `1`, and `4` identity forms and the existing figure/feature source construction. Apply Mono’s slashed-zero, coding-ligature, technical-arrow, and fixed-cell feature construction.

- [ ] **Step 3: Run source QA against the new source folders**

Run: `python3 tools/source_qa.py --family sans --family mono`

Expected: PASS for Roman and italic source structures.

### Task 3: Extend the build pipeline for italic binaries

**Files:**
- Modify: `tools/build_fonts.py`
- Modify: `tools/font_qa.py`
- Modify: `tools/shaping_qa.py`
- Modify: `tools/run_fontbakery.py`
- Create: `tests/test_italic_build_contract.py`

- [ ] **Step 1: Add a failing build contract test**

Assert that each family produces nine italic static TTF/OTF files and one italic variable TTF, with Sans carrying both axes and Mono carrying `wght` plus fixed 600-unit advances.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests/test_italic_build_contract.py -v`

Expected: FAIL because the build pipeline only recognizes Roman review artifacts.

- [ ] **Step 3: Implement the smallest pipeline extension**

Add an italic build mode that selects the italic designspaces, emits `AsbirSans-Review-Italic-*` and `AsbirMono-Review-Italic-*` files, sets italic subfamily/style-map names, and includes those artifacts in review, shaping, and FontBakery checks.

- [ ] **Step 4: Run the contract and font QA**

Run: `python3 -m unittest tests/test_italic_build_contract.py -v` and `python3 tools/font_qa.py --mode review --family sans --family mono`.

Expected: PASS with all Roman and italic review artifacts opening and passing structural checks.

### Task 4: Make Mono production approval family-scoped and package it

**Files:**
- Modify: `reports/production-signoff.json`
- Modify: `tools/font_qa.py`
- Create: `reports/mono-production-signoff.json`
- Create: `tools/package_asbir_mono_release.py`
- Create: `tests/test_mono_production_package.py`

- [ ] **Step 1: Add the failing package/signoff test**

Assert that Mono requires a signoff whose `family` is `mono`, that review names are rejected until production packaging, and that the production ZIP has clean `OTF`, `TTF`, `Variable`, `Italic`, and `Terminal` folders.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests/test_mono_production_package.py -v`

Expected: FAIL because Mono has no family-specific signoff or production packager.

- [ ] **Step 3: Implement the scoped gate and package**

Require family-matched signoff in `font_qa.py`, create the Mono signoff record for the approved review scope, package clean Roman and italic files, and include the terminal companion and notices.

- [ ] **Step 4: Run production QA and the package test**

Run: `python3 tools/font_qa.py --mode production --family mono` and `python3 -m unittest tests/test_mono_production_package.py -v`.

Expected: PASS.

### Task 5: Generate WOFF2 files and CSS loading kits

**Files:**
- Create: `tools/package_webfonts.py`
- Create: `public/downloads/web/AsbirSans/AsbirSans.css`
- Create: `public/downloads/web/AsbirMono/AsbirMono.css`
- Create: `tests/test_webfont_package.py`

- [ ] **Step 1: Add the failing WOFF2/CSS test**

Assert that normal and italic variable WOFF2 files exist for both families, static Regular fallbacks exist, CSS declares `font-style: normal` and `italic`, and each WOFF2 round-trips through fontTools.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests/test_webfont_package.py -v`

Expected: FAIL because no WOFF2 files or CSS loading kit exists.

- [ ] **Step 3: Implement the web packager**

Convert approved/review TTFs to WOFF2, place them under `web/AsbirSans/` and `web/AsbirMono/`, write CSS with the correct family names, axes, ranges, and italic declarations, and add the web files to both ZIP packages.

- [ ] **Step 4: Run the WOFF2/CSS test**

Run: `python3 -m unittest tests/test_webfont_package.py -v`

Expected: PASS.

### Task 6: Update studio release presentation and verify all outputs

**Files:**
- Modify: `src/main.js`
- Modify: `src/styles.css` only if italic release cards need layout support
- Modify: `README.md`
- Modify: `release/AsbirSans-1.0.0/`
- Modify: `release/AsbirMono-1.0.0/`
- Modify: `public/downloads/`

- [ ] **Step 1: Update release copy and download links**

Keep proof font URLs on review binaries, but mark Mono production release as approved and link the production Mono package, italic files, and web kits from the release section.

- [ ] **Step 2: Rebuild and package every release**

Run: `python3 tools/build_fonts.py --family sans --family mono --italic`, `python3 tools/package_webfonts.py`, `python3 tools/package_asbir_sans_release.py`, and `python3 tools/package_asbir_mono_release.py`.

- [ ] **Step 3: Run complete verification**

Run: `python3 -m unittest discover -s tests -v`, `python3 tools/source_qa.py --family sans --family mono`, `python3 tools/font_qa.py --mode production --family sans --family mono`, `python3 tools/shaping_qa.py --family sans --family mono`, `python3 tools/run_fontbakery.py --family sans --family mono`, `npm run build`, and `unzip -t` for both release ZIPs.

Expected: all tests, QA, build, and archive checks pass.

- [ ] **Step 4: Deploy the static build to Vercel production**

Run: `npx vite build` followed by `vercel deploy dist --prod --name asbir-tech-type --archive=tgz -y`.

Expected: Vercel reports a READY production deployment and aliases `https://asbir-tech-type.vercel.app`.
