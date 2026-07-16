# Asbir Sans audit

## Current status

**Asbir Sans 1.0.0 is approved and packaged for release.** The approved human
signoff is recorded in `reports/production-signoff.json`. Serif and Mono are
intentionally out of scope for this pass and must not be represented by this
audit.

The family is an OFL-compliant derivative of Inter 4.001 with an authored
Asbir character system. It retains six compatible Text/Display UFO masters,
the `opsz` (14–32) and `wght` (100–900) axes, and a 2,987-glyph compiled
repertoire. The default system selects a single-storey `a`, alternate `t` and
`G`, and Asbir figures `1` and `4`; the source of each substitution is stored
as glyph metadata in every master.

The proof application uses the approved **77/100 x-height** setting. The
underlying source remains at Inter's native 2048 UPM with a 1118-unit x-height
and a 1490-unit cap height.

## Verified evidence

- Six compatible UFO masters compile into a two-axis variable TTF and nine
  static weights (Thin through Black) in both TTF and CFF OTF formats.
- All 19 Sans artifacts pass `python3 tools/font_qa.py --mode review --family sans`.
  This verifies names, tables, 1118/1490 metrics, named `wght` instances,
  `opsz`, outlines, advances, and a Windows clipping box of 2310/710.
- `python3 tools/shaping_qa.py --family sans` passes 528 real HarfBuzz shaping
  checks across static fonts and variable weights, language samples, kerning,
  figure systems, and numeral features.
- `python3 tools/source_qa.py --family sans` passes source-structure checks.
- The Vite proof build passes (`npx vite build`), and the live proof was
  visually checked with the Asbir character set and Latin, Greek, and Cyrillic
  text.
- The FontBakery Universal profile completes with no unwaived errors or
  failures for Sans Regular TTF, Regular OTF, and the variable TTF. See
  [FONTBAKERY_WAIVERS.md](FONTBAKERY_WAIVERS.md) for two deliberately narrow,
  Inter-reference-matched waivers.

## Release-review record

1. **Human type-design signoff.** The Sans owner approved the family on
   2026-07-14 after live proof review. The record covers the single-storey
   default `a`, 77/100 proof x-height, and static/variable family.
2. **Manual proof record.** The interactive proof covers UI text, language
   samples, numerals, editable text, and variable controls. Keep this proof
   available for future print and operating-system regression checks.
3. **Warning disposition.** FontBakery reports no errors or failures. The
   remaining warnings are documented for future source maintenance: GDEF mark
   classification, decomposed L/d/l/t-caron outlines, unusual contour counts in
   five inherited glyphs, source construction-part glyphs intentionally
   unreachable at runtime, large variable-file size after component
   decomposition, interpolation diagnostics, and overlapping-path diagnostics.
   The variable has been specifically verified to pass STAT/fvar consistency,
   name-length, nested-component, and transformed-component checks.
4. **Legal/release review.** The official package includes the OFL derivative
   notice. It ships user-facing files without the temporary `-Review-` suffix
   under `release/AsbirSans-1.0.0/`.

## Release claim

Asbir Sans 1.0.0 is the approved production release for this workspace. It is
a distinct OFL derivative of Inter, not a claim to replace Inter's broader
multi-year type-design and maintenance program.
