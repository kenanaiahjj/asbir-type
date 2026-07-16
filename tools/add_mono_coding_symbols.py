"""Add editable Unicode technical-arrow glyphs to every Asbir Mono master."""
from pathlib import Path

from ufoLib2 import Font
from ufoLib2.objects import Component

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-mono'
MASTERS = ('Thin', 'Regular', 'Black')

# The source already has carefully drawn, single-cell coding-ligature forms.
# Reusing those as components keeps the Unicode arrows visually identical to
# their ASCII coding counterparts and, crucially, preserves the 600-unit grid.
ARROWS = {
    'uni21D0': (0x21D0, 'less_equal.liga'),       # ⇐
    'uni21D2': (0x21D2, 'equal_greater.liga'),    # ⇒
    'uni21D4': (0x21D4, 'less_equal_greater.liga'),  # ⇔
}


def rebuild_arrow(font, name, codepoint, source):
    if name in font:
        del font[name]
    glyph = font.newGlyph(name)
    glyph.width = 600
    glyph.unicodes = [codepoint]
    glyph.components.append(Component(baseGlyph=source))


def main():
    for master in MASTERS:
        path = SOURCE / f'AsbirMono-{master}.ufo'
        font = Font.open(path)
        for name, (codepoint, source) in ARROWS.items():
            if source not in font:
                raise SystemExit(f'{path}: missing required source glyph {source}')
            rebuild_arrow(font, name, codepoint, source)
        font.save(path, overwrite=True)
        print(f'Added Unicode technical arrows to {path.name}')


if __name__ == '__main__':
    main()
