"""Add the editable Latin-1 and Latin Extended-A language foundation.

Precomposed letters are built as components over the original ASCII base and
small, editable accent contours. This retains compatible topology across the
three weight masters and keeps the work transparent for a type designer to
refine in a UFO editor.
"""
import unicodedata
import argparse
from pathlib import Path

from ufoLib2 import Font
from ufoLib2.objects import Component

from expand_asbir_sans_sources import ASC, CAP, DESC, XH, diagonal, oval, poly, rect

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'sans': ('asbir-sans', 'AsbirSans'),
    'serif': ('asbir-serif', 'AsbirSerif'),
    'mono': ('asbir-mono', 'AsbirMono'),
}
SPECIAL_BASES = {
    0x00C6: 'A', 0x00E6: 'a', 0x00D0: 'D', 0x00F0: 'd', 0x00D8: 'O', 0x00F8: 'o',
    0x00DE: 'P', 0x00FE: 'p', 0x00DF: 's', 0x0131: 'i', 0x0132: 'I', 0x0133: 'i',
    0x0138: 'k', 0x0141: 'L', 0x0142: 'l', 0x014A: 'N', 0x014B: 'n', 0x0152: 'O',
    0x0153: 'o', 0x0166: 'T', 0x0167: 't', 0x017F: 's', 0x0110: 'D', 0x0111: 'd',
    0x0126: 'H', 0x0127: 'h', 0x013F: 'L', 0x0140: 'l', 0x0149: 'n',
    0x0218: 'S', 0x0219: 's', 0x021A: 'T', 0x021B: 't',
}
STROKED = {0x00D0, 0x00F0, 0x00D8, 0x00F8, 0x0110, 0x0111, 0x0126, 0x0127, 0x0141, 0x0142, 0x0166, 0x0167}
LIGATURES = {0x00C6: 'E', 0x00E6: 'e', 0x0132: 'J', 0x0133: 'j', 0x0152: 'E', 0x0153: 'e'}


def glyph_name(codepoint):
    return f'uni{codepoint:04X}'


def latin_targets():
    for codepoint in range(0x00C0, 0x0180):
        char = chr(codepoint)
        normalized = unicodedata.normalize('NFD', char)
        if codepoint in SPECIAL_BASES or (len(normalized) > 1 and normalized[0].isascii() and normalized[0].isalpha()):
            yield codepoint
    yield from (0x0218, 0x0219, 0x021A, 0x021B)


def accent(pen, mark, center, uppercase, stem, top_offset=0):
    """Draw a compatible accent contour, with room for stacked marks."""
    top = (CAP + 46 if uppercase else XH + 42) + top_offset
    thickness = max(18, round(stem * .58))
    if mark == '\u0300': diagonal(pen, center + 38, top + 36, center - 38, top - 42, thickness)
    elif mark == '\u0301': diagonal(pen, center - 38, top - 42, center + 38, top + 36, thickness)
    elif mark == '\u0302':
        diagonal(pen, center - 58, top - 25, center, top + 42, thickness)
        diagonal(pen, center, top + 42, center + 58, top - 25, thickness)
    elif mark == '\u0303':
        # One continuous contour avoids overlapping diagonal strokes at Black.
        h = thickness * .58
        poly(pen, [
            (center - 62, top + 8), (center - 38, top + 34), (center - 14, top + 34),
            (center + 10, top + 8), (center + 34, top + 8), (center + 62, top + 34),
            (center + 62, top + 34 - h), (center + 34, top + 8 - h),
            (center + 10, top + 8 - h), (center - 14, top + 34 - h),
            (center - 38, top + 34 - h), (center - 62, top + 8 - h),
        ])
    elif mark == '\u0304': rect(pen, center - 68, top, 136, thickness)
    elif mark == '\u0306':
        oval(pen, center, top + 18, 64, 35, thickness)
        rect(pen, center - 70, top - 18, 140, 38)
    elif mark == '\u0307': oval(pen, center, top + 18, thickness / 2, thickness / 2)
    elif mark == '\u0308':
        oval(pen, center - 38, top + 18, thickness / 2, thickness / 2)
        oval(pen, center + 38, top + 18, thickness / 2, thickness / 2)
    elif mark == '\u030A':
        oval(pen, center, top + 18, 42, 42)
        oval(pen, center, top + 18, 21, 21, reverse=True)
    elif mark == '\u030B':
        diagonal(pen, center - 55, top - 25, center - 8, top + 42, thickness)
        diagonal(pen, center + 8, top - 25, center + 55, top + 42, thickness)
    elif mark == '\u030C':
        diagonal(pen, center - 58, top + 42, center, top - 25, thickness)
        diagonal(pen, center, top - 25, center + 58, top + 42, thickness)
    elif mark == '\u0309':
        # Vietnamese hook above: deliberately a hook, not an apostrophe.
        diagonal(pen, center - 28, top + 24, center + 10, top + 52, thickness)
        oval(pen, center + 18, top + 6, thickness / 2, thickness / 2)
    elif mark == '\u031B':
        # Vietnamese horn, held to the right of the bowl/stem as a single
        # contour. Keeping it continuous avoids overlapping path segments in
        # heavy interpolated instances.
        h = max(12, thickness * .45)
        poly(pen, [
            (center + 62, top + 6), (center + 84, top + 14),
            (center + 116, top + 48), (center + 116 - h, top + 48),
            (center + 80 - h, top + 20), (center + 62, top + 6 - h),
        ])
    elif mark == '\u0327':
        oval(pen, center, DESC / 2, thickness / 2, thickness / 2)
        diagonal(pen, center, -12, center - 32, DESC + 12, thickness)
    elif mark == '\u0326':
        oval(pen, center, DESC / 2, thickness / 2, thickness / 2)
        diagonal(pen, center + 4, -12, center - 20, DESC + 12, thickness)
    elif mark == '\u0328':
        diagonal(pen, center + 12, 10, center + 56, DESC + 35, thickness)
    elif mark == '\u0323':
        oval(pen, center, -42, thickness / 2, thickness / 2)


def add_glyph(font, codepoint, stem):
    name = glyph_name(codepoint)
    if name in font:
        return
    char = chr(codepoint)
    normalized = unicodedata.normalize('NFD', char)
    base = SPECIAL_BASES.get(codepoint, normalized[0])
    if base not in font:
        return
    glyph = font.newGlyph(name)
    glyph.width = font[base].width
    glyph.unicodes = [codepoint]
    glyph.components.append(Component(baseGlyph=base))
    pen = glyph.getPen()
    if codepoint in LIGATURES:
        second = LIGATURES[codepoint]
        glyph.components.append(Component(baseGlyph=second, transformation=(.64, 0, 0, 1, glyph.width * .37, 0)))
    if codepoint in STROKED:
        diagonal(pen, glyph.width * .27, 100, glyph.width * .73, CAP - 80, max(18, stem * .55))
    if codepoint == 0x013F or codepoint == 0x0140:
        oval(pen, glyph.width * .73, XH * .48, max(12, stem * .3), max(12, stem * .3))
    if codepoint == 0x0149:
        diagonal(pen, glyph.width * .31, XH + 15, glyph.width * .23, XH + 85, max(16, stem * .45))
    for mark in normalized[1:]:
        accent(pen, mark, glyph.width / 2, base.isupper(), stem)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--redraw', action='append', default=[], metavar='CODEPOINT', help='Redraw a previously generated Unicode glyph, e.g. 00C3.')
    args = parser.parse_args()
    redraw = {int(value.removeprefix('U+'), 16) for value in args.redraw}
    for family, (folder, prefix) in FAMILIES.items():
        source = ROOT / 'sources' / folder
        for style, stem in (('Thin', 30 if family == 'sans' else 24 if family == 'serif' else 28), ('Regular', 64 if family == 'sans' else 48 if family == 'serif' else 58), ('Black', 150 if family == 'sans' else 118 if family == 'serif' else 132)):
            path = source / f'{prefix}-{style}.ufo'
            font = Font.open(path)
            font.info.ascender = 840
            font.info.openTypeOS2TypoAscender = 840
            font.info.openTypeOS2WinAscent = 840
            before = len(font)
            for codepoint in latin_targets():
                if codepoint in redraw and glyph_name(codepoint) in font:
                    del font[glyph_name(codepoint)]
                add_glyph(font, codepoint, stem)
            font.save(path, overwrite=True)
            print(f'{family} {style}: {before} -> {len(font)} glyphs')


if __name__ == '__main__':
    main()
