# Asbir Font Production and Italics Design

## Scope

This change promotes Asbir Mono to production, creates true italic source families for Asbir Sans and Asbir Mono, and adds a WOFF2/CSS web distribution kit for both families.

## Font architecture

Roman and italic remain separate variable files. Asbir Sans Italic retains `opsz` 14–32 and `wght` 100–900; Asbir Mono Italic retains `wght` 100–900. Each italic family is built from real italic masters derived from the corresponding OFL upstream italic source and then receives the Asbir character system, features, names, metrics, and QA treatment. A mechanically skewed Roman export is not accepted as the italic source.

The editable italic UFOs live in `sources/asbir-sans-italic/` and `sources/asbir-mono-italic/`. Their designspaces and generation metadata make the compiled review and production artifacts reproducible from the workspace.

## Production packaging

Asbir Mono becomes `AsbirMono-1.0.0` with `OTF`, `TTF`, `Variable`, `Italic`, and `Terminal` folders. The package includes the production Mono files, both variable italic files, the terminal companion, notices, QA notes, and a Mono-specific human signoff. Existing review artifacts remain available for proofing until the production package is verified.

## Web distribution

Both families get a `web/<Family>/` folder containing variable and static WOFF2 files plus one CSS loading kit. CSS uses `font-style: normal` and `font-style: italic`, exposes the existing weight ranges, documents the Sans optical-size axis, and keeps the terminal Nerd Font separate from the core Mono family.

## QA and release gates

The production signoff schema becomes family-scoped so Sans approval cannot satisfy Mono approval. Review QA, source QA, HarfBuzz shaping QA, FontBakery, WOFF2 round-trip checks, package-structure checks, and a Vite build must pass for both Roman and italic outputs before packaging and deployment.
