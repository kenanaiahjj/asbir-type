# Asbir Sans Download Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish an Asbir Sans ZIP that extracts into organised OTF, TTF, and Variable folders.

**Architecture:** `tools/package_asbir_sans_release.py` copies approved proof binaries into a release tree, then writes the same tree into the public download archive. The studio continues to load its existing review-named proof binaries directly.

**Tech Stack:** Python standard library (`pathlib`, `shutil`, `zipfile`), Vite, Vercel CLI.

## Global Constraints

- The archive root is `AsbirSans-1.0.0/`.
- Static release names exclude `Review`.
- The package includes all nine weights in OTF and TTF plus one variable TTF.
- The release README and third-party notices sit at the archive root.

---

### Task 1: Make release packaging create the structured archive

**Files:**
- Create: `tests/test_package_asbir_sans_release.py`
- Modify: `tools/package_asbir_sans_release.py`

- [ ] **Step 1: Write the failing test**

Create small source fixtures for every expected proof binary and assert the package command emits the three folders and the archive paths under `AsbirSans-1.0.0/`.

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests/test_package_asbir_sans_release.py -v`

Expected: FAIL because the current packager does not write a ZIP archive or top-level release folder.

- [ ] **Step 3: Implement the minimal package change**

Build `OTF`, `TTF`, and `Variable` folders from the release tree, safely replace the generated release directory, and create `public/downloads/AsbirSans-1.0.0.zip` with the release directory as its sole archive root.

- [ ] **Step 4: Run the focused test**

Run: `python3 -m unittest tests/test_package_asbir_sans_release.py -v`

Expected: PASS.

### Task 2: Package, build, and deploy the release

**Files:**
- Modify: `release/AsbirSans-1.0.0/`
- Modify: `public/downloads/AsbirSans-1.0.0.zip`

- [ ] **Step 1: Rebuild the public release**

Run: `python3 tools/package_asbir_sans_release.py`

- [ ] **Step 2: Validate archive contents and build the studio**

Run: `unzip -l public/downloads/AsbirSans-1.0.0.zip` and `npm run build`

Expected: ZIP paths begin with `AsbirSans-1.0.0/`; Vite build exits 0.

- [ ] **Step 3: Deploy to Vercel production**

Run: `vercel deploy --prod -y`

Expected: Vercel returns the production deployment URL.
