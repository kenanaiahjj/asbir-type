"""Add editable Vietnamese Latin composites to each Asbir review source.

The existing ASCII base is retained as a UFO component. Vietnamese-specific
structural and tone marks are drawn as compatible contours in every master so
the result remains editable and interpolatable rather than a cmap-only patch.
"""
import argparse
import unicodedata
from pathlib import Path

from ufoLib2 import Font
from ufoLib2.objects import Component

from expand_latin_sources import FAMILIES, accent, glyph_name

ROOT = Path(__file__).resolve().parents[1]
VIETNAMESE = {codepoint for codepoint in range(0x0102, 0x01B1)} | set(range(0x1EA0, 0x1EFA))
VIETNAMESE = {
    codepoint for codepoint in VIETNAMESE
    if unicodedata.category(chr(codepoint)).startswith('L')
    and any(mark in unicodedata.normalize('NFD', chr(codepoint)) for mark in ('\u0306', '\u0302', '\u031B', '\u0300', '\u0301', '\u0303', '\u0309', '\u0323'))
}
STRUCTURAL_MARKS = {'\u0306', '\u0302', '\u031B'}
TONE_MARKS = {'\u0300', '\u0301', '\u0303', '\u0309'}


def add_vietnamese_glyph(font, codepoint, stem, redraw=False):
    name = glyph_name(codepoint)
    if name in font:
        if not redraw:
            return
        del font[name]
    normalized = unicodedata.normalize('NFD', chr(codepoint))
    base, marks = normalized[0], normalized[1:]
    if base not in font:
        return
    glyph = font.newGlyph(name)
    glyph.width = font[base].width
    glyph.unicodes = [codepoint]
    glyph.components.append(Component(baseGlyph=base))
    pen = glyph.getPen()
    has_tone_mark = any(mark in TONE_MARKS for mark in marks)
    for mark in marks:
        # Lower the structural mark slightly when it shares a cap with a tone.
        # This creates a readable stack without pushing the heaviest outlines
        # beyond the 840-unit ascender.
        offset = -26 if mark in STRUCTURAL_MARKS and has_tone_mark else 0
        accent(pen, mark, glyph.width / 2, base.isupper(), stem, top_offset=offset)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--redraw', action='store_true', help='Redraw existing Vietnamese review glyphs.')
    args = parser.parse_args()
    stems = {
        'sans': (30, 64, 150),
        'serif': (24, 48, 118),
        'mono': (28, 58, 132),
    }
    for family, (folder, prefix) in FAMILIES.items():
        for style, stem in zip(('Thin', 'Regular', 'Black'), stems[family]):
            path = ROOT / 'sources' / folder / f'{prefix}-{style}.ufo'
            font = Font.open(path)
            before = len(font)
            for codepoint in sorted(VIETNAMESE):
                add_vietnamese_glyph(font, codepoint, stem, redraw=args.redraw)
            font.save(path, overwrite=True)
            print(f'{family} {style}: {before} -> {len(font)} glyphs')


if __name__ == '__main__':
    main()
