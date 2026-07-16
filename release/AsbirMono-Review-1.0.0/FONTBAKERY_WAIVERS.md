# Asbir Sans FontBakery waivers

These are narrow, evidence-backed waivers for the Asbir Sans OFL derivative.
They are not a substitute for the normal FontBakery suite; all other Universal
profile checks continue to run.

## `base_has_width`

U+0488 and U+0489 are **Cyrillic enclosing combining marks**, so their
zero advance is intentional and required for correct mark attachment. The
Universal profile currently classifies them as base characters. The official
Inter 4.001 variable binary used as the licensed derivative foundation fails
this identical check for the same two glyphs.

## `case_mapping`

The same Inter 4.001 binary reports the identical thirteen missing Unicode
case-pair counterparts. They belong to historic/extended IPA, Greek, Cyrillic,
and turned-letter repertoires outside the foundation's published scope. Adding
placeholder counterpart glyphs purely to silence the heuristic would reduce
the integrity of the family. The declared modern Latin, Greek, Cyrillic, and
Vietnamese release repertoires remain explicitly checked by `font_qa.py` and
the shaping suite.

Both waivers were compared directly against:

`/Users/kenanaiahjolmfc/Downloads/inter-master/docs/font-files/InterVariable.ttf`

Inter identity: `Inter Variable`, version `4.001;git-9221beed3`.

## Asbir Mono review-build notes

The Asbir Mono review binaries are tested independently as static TrueType,
static CFF, and variable TrueType files. The 14 July 2026 Universal-profile
run reports **zero ERROR, FATAL, and FAIL** results. The following warnings are
retained for review rather than suppressed:

- `bad-numberOfHMetrics` (TrueType only): the compiler preserves legitimate
  zero-width combining marks alongside the fixed 600-unit coding cell. Changing
  the compression count just to satisfy the recommendation would risk changing
  those mark advances.
- `alt_caron`, `contour_count`, `typoascender_exceeds_Agrave`,
  `unreachable_glyphs`, and `legacy-long-names`: source-derived construction,
  metadata, or coverage advisories. They do not represent binary errors, and
  the source, binary, and shaping checks independently cover the affected
  outlines and encoded characters.

The CFF mono run excludes `opentype/monospace` because that FontBakery check
assumes a TrueType `glyf` table and crashes on CFF fonts. Its TrueType sibling
and the project’s direct fixed-width checks validate the same monospace
metadata and 600-unit advances.

## Asbir Mono Nerd Font terminal-build notes

The separately named `AsbirMono-NerdFont-Review-Regular.ttf` is an optional
terminal asset, not a replacement for the core variable/static family. Its
14 July 2026 Universal-profile run reports **zero ERROR, FATAL, and FAIL**
results. Along with the source-derived Mono warnings above, FontBakery reports
`large-font` (expected for 10,395 icon/Powerline glyphs) and
`overlapping-path-segments` in imported Nerd Fonts symbol outlines. The build
script maps every imported icon to a 600-unit cell, verifies Powerline/icon
cmap samples, marks the binary fixed-pitch, and writes
`reports/nerd-font-qa.json`.
