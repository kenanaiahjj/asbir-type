# Asbir Sans Download Layout Design

## Goal

Make the public Asbir Sans 1.0.0 ZIP extract into one clearly labelled release folder, with static OTF, static TTF, and variable-font files separated for immediate use.

## Chosen layout

```text
AsbirSans-1.0.0/
  OTF/
    AsbirSans-Thin.otf … AsbirSans-Black.otf
  TTF/
    AsbirSans-Thin.ttf … AsbirSans-Black.ttf
  Variable/
    AsbirSans-Variable.ttf
  README.md
  THIRD_PARTY_NOTICES.md
```

The ZIP will use exactly this top-level structure. The release files drop the internal `Review` suffix; the proof assets served by the studio retain their existing filenames.

## Packaging behavior

The package command rebuilds the local release directory and its matching public ZIP from the approved binaries in `public/downloads`. It fails clearly when a required binary or notice file is missing.

## Verification

A focused test will assert the release folders, expected font names, and ZIP paths. The full Vite build will then ensure the public download artifact is included before production deployment.
