"""Add practical typographic punctuation, currency, arrows and basic math."""
from pathlib import Path
import argparse

from ufoLib2 import Font

from expand_asbir_sans_sources import CAP, DESC, XH, diagonal, oval, poly, rect, ring

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'sans': ('asbir-sans', 'AsbirSans', (30, 64, 150)),
    'serif': ('asbir-serif', 'AsbirSerif', (24, 48, 118)),
    'mono': ('asbir-mono', 'AsbirMono', (28, 58, 132)),
}
SYMBOLS = (
    0x00A1, 0x00A9, 0x00AE, 0x00B0, 0x00B1, 0x00B5, 0x00B7, 0x00D7, 0x00F7,
    0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015,
    0x2018, 0x2019, 0x201A, 0x201B, 0x201C, 0x201D, 0x201E, 0x201F,
    0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2032, 0x2033, 0x2039, 0x203A,
    0x20AC, 0x2116, 0x2122, 0x2190, 0x2191, 0x2192, 0x2193,
)


def glyph_name(codepoint):
    return f'uni{codepoint:04X}'


def width(family, codepoint):
    if family == 'mono':
        return 600
    if codepoint in (0x2014, 0x2015):
        return 700
    if codepoint in (0x2018, 0x2019, 0x201A, 0x201B, 0x2032):
        return 250
    if codepoint in (0x201C, 0x201D, 0x201E, 0x201F, 0x2033):
        return 360
    return 500


def draw(pen, codepoint, stem, advance):
    t = max(18, stem)
    cx = advance / 2
    if codepoint == 0x00A1:
        rect(pen, cx - t / 2, 0, t, XH - 130); oval(pen, cx, XH - 35, t / 2, t / 2)
    elif codepoint in (0x00A9, 0x00AE):
        # Symbol counters must stay open even at the Black master.
        ring(pen, cx, 350, 190, 260, min(t, 54))
        if codepoint == 0x00A9:
            rect(pen, cx - 55, 180, t, 340); rect(pen, cx - 10, 180, 110, t); rect(pen, cx - 10, 480, 110, t)
        else:
            # Keep the inner R well inside the counter of the registration ring.
            rect(pen, cx - 62, 225, t, 225); rect(pen, cx - 62, 410, 88, t)
            rect(pen, cx + 8, 340, t, 95); diagonal(pen, cx - 4, 340, cx + 58, 225, t)
    elif codepoint == 0x00B0: ring(pen, cx, 500, 70, 70, t)
    elif codepoint == 0x00B1:
        rect(pen, cx - 150, 410, 300, t); rect(pen, cx - t / 2, 270, t, 280); rect(pen, cx - 150, 120, 300, t)
    elif codepoint == 0x00B5:
        rect(pen, 80, 0, t, XH); rect(pen, advance - 80 - t, DESC, t, XH - DESC); rect(pen, 145, 0, advance - 225, t)
    elif codepoint == 0x00B7: oval(pen, cx, 280, t / 2, t / 2)
    elif codepoint == 0x00D7:
        diagonal(pen, cx - 130, 210, cx + 130, 470, t); diagonal(pen, cx + 130, 210, cx - 130, 470, t)
    elif codepoint == 0x00F7:
        rect(pen, cx - 150, 320, 300, t); oval(pen, cx, 500, t / 2, t / 2); oval(pen, cx, 140, t / 2, t / 2)
    elif codepoint in (0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015):
        lengths = {0x2010: 180, 0x2011: 180, 0x2012: 260, 0x2013: 340, 0x2014: 600, 0x2015: 600}
        length = lengths[codepoint]; y = 280 if codepoint != 0x2015 else 350
        rect(pen, cx - length / 2, y, length, t)
    elif codepoint in (0x2018, 0x2019, 0x201A, 0x201B):
        up = codepoint in (0x2018, 0x201B)
        diagonal(pen, cx + (20 if up else -20), XH if up else 80, cx - (35 if up else -35), XH - 100 if up else DESC / 2, t / 2)
    elif codepoint in (0x201C, 0x201D, 0x201E, 0x201F):
        up = codepoint in (0x201C, 0x201F); y = XH if up else 80
        diagonal(pen, cx - 70 + (20 if up else -20), y, cx - 125 - (35 if up else -35), y - 100 if up else DESC / 2, t / 2)
        diagonal(pen, cx + 70 + (20 if up else -20), y, cx + 15 - (35 if up else -35), y - 100 if up else DESC / 2, t / 2)
    elif codepoint == 0x2020:
        rect(pen, cx - 130, 400, 260, t); rect(pen, cx - t / 2, 80, t, 520)
    elif codepoint == 0x2021:
        rect(pen, cx - 130, 460, 260, t); rect(pen, cx - 130, 230, 260, t); rect(pen, cx - t / 2, 80, t, 610)
    elif codepoint == 0x2022: oval(pen, cx, 330, t, t)
    elif codepoint == 0x2026:
        for x in (cx - 110, cx, cx + 110): oval(pen, x, 35, t / 2, t / 2)
    elif codepoint == 0x2030:
        oval(pen, 135, 520, 50, 50); oval(pen, 365, 180, 50, 50); oval(pen, 365, 520, 50, 50); diagonal(pen, 118, 86, 382, 614, t)
    elif codepoint == 0x2032: diagonal(pen, cx, XH, cx - 35, XH - 105, t / 2)
    elif codepoint == 0x2033:
        diagonal(pen, cx - 48, XH, cx - 83, XH - 105, t / 2); diagonal(pen, cx + 48, XH, cx + 13, XH - 105, t / 2)
    elif codepoint in (0x2039, 0x203A):
        left = codepoint == 0x2039
        diagonal(pen, cx + (70 if left else -70), 160, cx - (70 if left else -70), 350, t)
        diagonal(pen, cx - (70 if left else -70), 350, cx + (70 if left else -70), 540, t)
    elif codepoint == 0x20AC:
        rect(pen, cx - 150, 120, t, 460); rect(pen, cx - 95, 580, 230, t); rect(pen, cx - 95, 120, 230, t); rect(pen, cx - 180, 300, 260, t); rect(pen, cx - 180, 410, 260, t)
    elif codepoint == 0x2116:
        rect(pen, 55, 180, t, 350); diagonal(pen, 55 + t, 530, 195, 180, t); rect(pen, 215, 260, t, 260); rect(pen, 355, 260, t, 260); rect(pen, 255, 260, 100, t); rect(pen, 255, 480, 100, t)
    elif codepoint == 0x2122:
        rect(pen, 60, 560, 150, t); rect(pen, 125 - t / 2, 390, t, 170)
        poly(pen, [(250, 390), (250, 560), (276, 560), (320, 470), (364, 560), (390, 560),
                   (390, 390), (365, 390), (365, 500), (334, 390), (306, 390), (275, 500), (275, 390)])
    elif codepoint in (0x2190, 0x2192):
        right = codepoint == 0x2192
        rect(pen, 90, 320, advance - 180, t)
        tip = advance - 80 if right else 80; tail = 180 if right else advance - 180
        diagonal(pen, tail, 430, tip, 350, t); diagonal(pen, tail, 270, tip, 350, t)
    elif codepoint in (0x2191, 0x2193):
        up = codepoint == 0x2191
        rect(pen, cx - t / 2, 90, t, 530)
        tip = 620 if up else 80; tail = 510 if up else 190
        diagonal(pen, cx - 100, tail, cx, tip, t); diagonal(pen, cx + 100, tail, cx, tip, t)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--redraw', action='append', default=[], metavar='CODEPOINT', help='Redraw a generated Unicode glyph, e.g. 00AE.')
    args = parser.parse_args()
    redraw = {int(value.removeprefix('U+'), 16) for value in args.redraw}
    for family, (folder, prefix, stems) in FAMILIES.items():
        for style, stem in zip(('Thin', 'Regular', 'Black'), stems):
            path = ROOT / 'sources' / folder / f'{prefix}-{style}.ufo'
            font = Font.open(path)
            for codepoint in SYMBOLS:
                name = glyph_name(codepoint)
                if codepoint in redraw and name in font:
                    del font[name]
                if name in font:
                    continue
                glyph = font.newGlyph(name)
                glyph.width = width(family, codepoint)
                glyph.unicodes = [codepoint]
                draw(glyph.getPen(), codepoint, stem, glyph.width)
            font.save(path, overwrite=True)
            print(f'Expanded {family} {style} to {len(font)} glyphs')


if __name__ == '__main__':
    main()
