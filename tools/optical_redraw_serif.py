"""Redraw the high-frequency Asbir Serif core with a display-serif contrast.

The initial companion source was intentionally a geometric placeholder with
slab details. This pass gives the reading skeleton a proper contrast model:
verticals are authoritative, horizontals and shoulders are lighter, and bowls
keep the high x-height shared with Asbir Sans.
"""
from pathlib import Path

from ufoLib2 import Font

from expand_asbir_sans_sources import (
    ASC, CAP, DESC, XH, arch, diagonal, open_c, oval, rect, ring,
    rounded_rect, smooth_s,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-serif'
MASTERS = (('Thin', 24), ('Regular', 48), ('Black', 118))


def contrast_ring(pen, cx, cy, rx, ry, vertical, horizontal):
    """Upright serif contrast: firm sides, finer top and bottom."""
    oval(pen, cx, cy, rx, ry)
    oval(pen, cx, cy, max(8, rx - vertical), max(8, ry - horizontal), reverse=True)


def hair(stem):
    return max(12, round(stem * .38))


def serif(pen, x, y, width, thickness):
    """Short tapered-ish serif shelf; intentionally quieter than a slab."""
    rect(pen, x, y, width, thickness)


def lower(pen, char, stem):
    t, h = stem, hair(stem)
    if char == 'a':
        contrast_ring(pen, 218, 244, 150, 244, t, h)
        rounded_rect(pen, 344, 0, t, XH, min(14, t*.24))
        serif(pen, 326, 0, t + 36, h); serif(pen, 326, XH-h, t + 36, h)
    elif char == 'o':
        contrast_ring(pen, 250, 278, 180, 278, t, h)
    elif char == 'e':
        contrast_ring(pen, 246, 278, 176, 278, t, h)
        rect(pen, 92, 260, 304, h)
    elif char == 'c':
        open_c(pen, 255, 278, 185, 278, h, .29)
    elif char == 's':
        smooth_s(pen, 250, 278, 330, 555, h)
    elif char == 'n':
        rounded_rect(pen, 60, 0, t, XH, min(14, t*.24)); arch(pen, 124, 344, 0, XH, h)
        serif(pen, 34, 0, t+50, h); serif(pen, 34, XH-h, t+50, h); serif(pen, 318, 0, t+46, h)
    elif char == 'm':
        rounded_rect(pen, 40, 0, t, XH, min(14, t*.24)); arch(pen, 104, 250, 0, XH, h); arch(pen, 239, 374, 0, XH, h)
        serif(pen, 16, 0, t+48, h); serif(pen, 16, XH-h, t+48, h); serif(pen, 348, 0, t+48, h)
    elif char == 'h':
        rounded_rect(pen, 60, 0, t, ASC, min(14, t*.24)); arch(pen, 124, 344, 0, XH, h)
        serif(pen, 34, 0, t+50, h); serif(pen, 34, ASC-h, t+50, h); serif(pen, 318, 0, t+46, h)
    elif char == 'u':
        rounded_rect(pen, 60, 190, t, XH-190, min(14, t*.24)); rounded_rect(pen, 344-t, 0, t, XH, min(14, t*.24))
        pen.moveTo((60, 190)); pen.curveTo((60, 60), (138, 10), (234, 10)); pen.curveTo((318, 10), (344, 76), (344, 190)); pen.lineTo((344-t, 190)); pen.curveTo((344-t, 92), (286, 56), (234, 56)); pen.curveTo((176, 56), (60+t, 96), (60+t, 190)); pen.closePath()
        serif(pen, 34, 190, t+50, h); serif(pen, 318, 0, t+46, h)
    elif char == 'r':
        rounded_rect(pen, 60, 0, t, XH, min(14, t*.24))
        pen.moveTo((124, 300)); pen.curveTo((154, 495), (270, 570), (394, 474)); pen.lineTo((386, 410)); pen.curveTo((292, 463), (208, 420), (188, 300)); pen.closePath()
        serif(pen, 34, 0, t+50, h); serif(pen, 34, XH-h, t+50, h)
    elif char in 'bdpq':
        x = 60 if char in 'bp' else 376-t
        y = 0 if char in 'bd' else DESC
        height = ASC if char in 'bd' else XH-DESC
        rounded_rect(pen, x, y, t, height, min(14, t*.24)); contrast_ring(pen, 250, 278, 180, 278, t, h)
        serif(pen, x-26, y, t+52, h)
        if char in 'bd': serif(pen, x-26, ASC-h, t+52, h)
    elif char == 'g':
        contrast_ring(pen, 228, 260, 150, 240, t, h); rounded_rect(pen, 344, DESC, t, XH-DESC, min(14, t*.24))
        pen.moveTo((408, 0)); pen.curveTo((408, DESC+18), (322, DESC+18), (230, DESC+18)); pen.curveTo((172, DESC+18), (138, DESC+44), (128, DESC+78)); pen.lineTo((192, DESC+78)); pen.curveTo((205, DESC+54), (221, DESC+50), (245, DESC+50)); pen.curveTo((305, DESC+50), (344, DESC+88), (344, 0)); pen.closePath()
    elif char == 't':
        rounded_rect(pen, 215, 0, t, ASC, min(14, t*.24)); rect(pen, 105, 360, 270, h)
        serif(pen, 190, 0, t+50, h); serif(pen, 190, ASC-h, t+50, h)
    elif char == 'f':
        rounded_rect(pen, 215, 0, t, ASC, min(14, t*.24)); rect(pen, 105, 350, 290, h)
        pen.moveTo((215, 500)); pen.curveTo((215, 674), (298, 776), (400, 734)); pen.lineTo((396, 674)); pen.curveTo((326, 690), (279, 628), (279, 500)); pen.closePath()
        serif(pen, 190, 0, t+50, h)
    elif char == 'i':
        rounded_rect(pen, 218, 0, t, XH-100, min(14, t*.24)); oval(pen, 250, XH-30, h*.72, h*.72)
        serif(pen, 192, 0, t+50, h)
    elif char == 'l':
        rounded_rect(pen, 218, 0, t, ASC, min(14, t*.24)); serif(pen, 192, 0, t+50, h); serif(pen, 192, ASC-h, t+50, h)
    elif char == 'v':
        diagonal(pen, 74, XH, 250, 0, h*1.2); diagonal(pen, 426, XH, 250, 0, h*1.2)
    elif char == 'w':
        diagonal(pen, 42, XH, 130, 0, h*1.1); diagonal(pen, 458, XH, 370, 0, h*1.1); diagonal(pen, 130, 0, 250, 300, h); diagonal(pen, 370, 0, 250, 300, h)
    elif char == 'x':
        diagonal(pen, 72, XH, 428, 0, h); diagonal(pen, 428, XH, 72, 0, h)
    elif char == 'y':
        diagonal(pen, 76, XH, 250, 0, h); diagonal(pen, 424, XH, 250, 0, h); rounded_rect(pen, 218, DESC, h, 110, min(12, h*.24))
    else:
        return False
    return True


def upper(pen, char, stem):
    t, h = stem, hair(stem)
    if char == 'A':
        diagonal(pen, 74, 0, 220, CAP, t*.74); diagonal(pen, 426, 0, 280, CAP, t*.74); rect(pen, 150, 282, 200, h)
        serif(pen, 42, 0, 104, h); serif(pen, 354, 0, 104, h)
    elif char in 'OQ':
        contrast_ring(pen, 250, 350, 210, 350, t, h)
        if char == 'Q': diagonal(pen, 286, 142, 462, -40, h*1.2)
    elif char == 'C': open_c(pen, 252, 350, 212, 350, h, .25)
    elif char == 'G':
        open_c(pen, 252, 350, 212, 350, h, .21); rect(pen, 250, 294, 190, h); rounded_rect(pen, 376, 132, t, 168, min(14, t*.24))
    elif char == 'S': smooth_s(pen, 250, 350, 370, 700, h)
    elif char == 'T':
        rect(pen, 40, CAP-h, 420, h); rounded_rect(pen, 218, 0, t, CAP, min(14, t*.24)); serif(pen, 192, 0, t+50, h)
    elif char == 'U':
        rounded_rect(pen, 40, 210, t, CAP-210, min(14, t*.24)); rounded_rect(pen, 396, 210, t, CAP-210, min(14, t*.24))
        pen.moveTo((40, 210)); pen.curveTo((40, 60), (130, 0), (250, 0)); pen.curveTo((370, 0), (460, 60), (460, 210)); pen.lineTo((396, 210)); pen.curveTo((396, 104), (342, 54), (250, 54)); pen.curveTo((158, 54), (104, 104), (104, 210)); pen.closePath()
        serif(pen, 18, 210, t+48, h); serif(pen, 374, 210, t+48, h)
    else:
        return False
    return True


SELECTED_LOWER = set('aobcensmhurbdpqgtfilvwxy')
SELECTED_UPPER = set('AOCGS T UQ'.replace(' ', ''))


def redraw(style, stem):
    path = SOURCE / f'AsbirSerif-{style}.ufo'
    font = Font.open(path)
    for char in sorted(SELECTED_LOWER | SELECTED_UPPER):
        name = char
        if name in font:
            del font[name]
        glyph = font.newGlyph(name)
        glyph.width = 540 if char.isalpha() else 500
        glyph.unicodes = [ord(char)]
        drawn = lower(glyph.getPen(), char, stem) if char.islower() else upper(glyph.getPen(), char, stem)
        if not drawn:
            raise RuntimeError(f'No redraw for {char}')
        for contour in glyph.contours:
            for point in contour.points:
                point.smooth = False
    font.info.xHeight = XH
    font.save(path, overwrite=True)
    print(f'Redrew Serif {style}: {len(font)} glyphs')


def main():
    for style, stem in MASTERS:
        redraw(style, stem)


if __name__ == '__main__':
    main()
