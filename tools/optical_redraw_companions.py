"""Apply the current Asbir construction to editable Serif and Mono masters.

This is deliberately source-first: only Basic Latin contours are replaced.
Language glyphs remain editable component constructions and are refreshed by
the normal feature/language scripts after this pass.
"""
from pathlib import Path

from ufoLib2 import Font

from expand_asbir_sans_sources import draw_char, glyph_name
from generate_companion_sources import (
    FAMILIES,
    add_mono_detail,
    add_serif_detail,
    companion_width,
)

ROOT = Path(__file__).resolve().parents[1]
STEMS = {
    'serif': {'Thin': 24, 'Regular': 48, 'Black': 118},
    'mono': {'Thin': 28, 'Regular': 58, 'Black': 132},
}


def redraw_family(kind):
    folder = ROOT / 'sources' / f'asbir-{kind}'
    prefix = FAMILIES[kind]['prefix']
    for style, stem in STEMS[kind].items():
        path = folder / f'{prefix}-{style}.ufo'
        font = Font.open(path)
        for codepoint in range(32, 127):
            ch = chr(codepoint)
            name = glyph_name(ch)
            if name in font:
                del font[name]
            glyph = font.newGlyph(name)
            glyph.width = companion_width(kind, ch)
            glyph.unicodes = [codepoint]
            draw_char(glyph.getPen(), ch, stem)
            if kind == 'serif':
                add_serif_detail(glyph.getPen(), ch, stem)
            else:
                add_mono_detail(glyph.getPen(), ch, stem)
            for contour in glyph.contours:
                for point in contour.points:
                    point.smooth = False
        font.info.xHeight = 555
        font.save(path, overwrite=True)
        print(f'Redrew {kind} {style}: {len(font)} glyphs')


def main():
    for kind in ('serif', 'mono'):
        redraw_family(kind)


if __name__ == '__main__':
    main()
