"""Add an editable Greek and Cyrillic review foundation to all Asbir masters.

Shared skeletons are represented by UFO components, while script-specific forms
remain individual glyphs that can be optically redrawn in a font editor. This
is source work, not Unicode fallback: every encoded character is a compatible
glyph across Thin, Regular, and Black masters.
"""
import argparse
import unicodedata
from pathlib import Path

from ufoLib2 import Font
from ufoLib2.objects import Component

from expand_latin_sources import FAMILIES, accent, glyph_name
from expand_asbir_sans_sources import ASC, CAP, DESC, XH, arch, diagonal, draw_char, open_c, oval, rect, ring, rounded_rect, smooth_s
from generate_companion_sources import add_mono_detail, add_serif_detail

ROOT = Path(__file__).resolve().parents[1]
GREEK = {codepoint for codepoint in range(0x0370, 0x0400) if unicodedata.category(chr(codepoint)).startswith('L')}
CYRILLIC = {codepoint for codepoint in range(0x0400, 0x0530) if unicodedata.category(chr(codepoint)).startswith('L')}

# These forms cannot credibly be represented by a Latin component. They are
# deliberately redrawn as independent outlines; accented derivatives use the
# same base construction plus editable accent contours below.
SCRIPT_SPECIFIC = set('ΓΔΛΠΣΦΨΩαβγδεηθμπρςστφψωДЖЗЦЧШЩЮЯджзцчшщюя')

# Shared skeletons are a useful starting point for a geometric companion, but
# they stay as independent encoded UFO glyphs so a type designer can refine
# Greek/Cyrillic proportions without changing Latin sources.
GREEK_BASES = {
    'ʹ':'uni0027','ʹ':'uni0027',
    'Α':'A','Β':'B','Γ':'T','Δ':'A','Ε':'E','Ζ':'Z','Η':'H','Θ':'O','Ι':'I','Κ':'K','Λ':'A','Μ':'M','Ν':'N','Ξ':'E','Ο':'O','Π':'H','Ρ':'P','Σ':'E','Τ':'T','Υ':'Y','Φ':'O','Χ':'X','Ψ':'Y','Ω':'W',
    'α':'a','β':'b','γ':'y','δ':'d','ε':'e','ζ':'z','η':'n','θ':'o','ι':'i','κ':'k','λ':'l','μ':'u','ν':'v','ξ':'e','ο':'o','π':'n','ρ':'p','ς':'s','σ':'o','τ':'t','υ':'u','φ':'o','χ':'x','ψ':'y','ω':'w',
}
CYRILLIC_BASES = {
    'А':'A','Б':'B','В':'B','Г':'T','Д':'A','Е':'E','Ё':'E','Ж':'X','З':'B','И':'N','Й':'N','К':'K','Л':'A','М':'M','Н':'H','О':'O','П':'H','Р':'P','С':'C','Т':'T','У':'Y','Ф':'O','Х':'X','Ц':'U','Ч':'h','Ш':'W','Щ':'W','Ъ':'B','Ы':'B','Ь':'B','Э':'E','Ю':'O','Я':'R',
    'а':'a','б':'b','в':'b','г':'r','д':'a','е':'e','ё':'e','ж':'x','з':'s','и':'n','й':'n','к':'k','л':'a','м':'m','н':'h','о':'o','п':'n','р':'p','с':'c','т':'t','у':'y','ф':'o','х':'x','ц':'u','ч':'h','ш':'w','щ':'w','ъ':'b','ы':'b','ь':'b','э':'e','ю':'o','я':'r',
    'І':'I','Ї':'I','Є':'E','Ґ':'T','і':'i','ї':'i','є':'e','ґ':'r',
}


def targets():
    # Build decomposed characters after their base so precomposed Greek and
    # Cyrillic accents can use components rather than copied outlines.
    return sorted(GREEK | CYRILLIC, key=lambda codepoint: (len(unicodedata.normalize('NFD', chr(codepoint))), codepoint))


def source_base(char, script):
    mapping = GREEK_BASES if script == 'greek' else CYRILLIC_BASES
    normalized = unicodedata.normalize('NFD', char)
    base = normalized[0]
    if base in mapping:
        return mapping[base], base, normalized[1:]
    # A decomposed base may itself be a script glyph encoded earlier in the
    # two-pass order; use it directly. Extended historical letters otherwise
    # get an editable case-matched skeleton rather than a missing glyph.
    if base != char:
        # Resolve recursively to an original skeleton, never to another script
        # composite. Static-font renderers can reject nested components.
        resolved_name, _, _ = source_base(base, script)
        return resolved_name, base, normalized[1:]
    return ('A' if char.isupper() else 'a'), base, ()


def script_width(family):
    return 600 if family == 'mono' else 500


def draw_greek(pen, char, stem):
    """A high-x-height Greek layer with its own structural signatures."""
    t = stem
    if char == 'Γ':
        rounded_rect(pen, 58, 0, t, CAP, min(18, t*.28)); rect(pen, 58, CAP-t, 350, t)
    elif char in 'ΔΛ':
        diagonal(pen, 68, 0, 250, CAP, t); diagonal(pen, 432, 0, 250, CAP, t)
        if char == 'Δ': rounded_rect(pen, 72, 0, 356, t, min(18, t*.28))
    elif char == 'Π':
        rounded_rect(pen, 60, 0, t, CAP, min(18, t*.28)); rounded_rect(pen, 376, 0, t, CAP, min(18, t*.28)); rect(pen, 60, CAP-t, 380, t)
    elif char == 'Σ':
        rounded_rect(pen, 82, CAP-t, 340, t, min(18, t*.28)); diagonal(pen, 398, CAP-t*.5, 150, CAP*.5, t); diagonal(pen, 150, CAP*.5, 398, t*.5, t); rounded_rect(pen, 82, 0, 340, t, min(18, t*.28))
    elif char == 'Φ':
        ring(pen, 250, CAP*.5, 178, 250, t); rounded_rect(pen, 250-t*.5, -56, t, CAP+112, min(18, t*.28))
    elif char == 'Ψ':
        ring(pen, 250, 478, 178, 176, t); rounded_rect(pen, 250-t*.5, 0, t, 470, min(18, t*.28))
    elif char == 'Ω':
        rounded_rect(pen, 58, 0, 112, t, min(18, t*.28)); rounded_rect(pen, 330, 0, 112, t, min(18, t*.28));
        pen.moveTo((92, 44)); pen.curveTo((38, 190), (68, CAP+8), (250, CAP+8)); pen.curveTo((432, CAP+8), (462, 190), (408, 44)); pen.lineTo((344, 44)); pen.curveTo((384, 172), (360, 642), (250, 642)); pen.curveTo((140, 642), (116, 172), (156, 44)); pen.closePath()
    elif char == 'α':
        ring(pen, 214, 246, 145, 246, t); rounded_rect(pen, 365, 0, t, XH, min(18, t*.28)); rect(pen, 365, 0, 65, t)
    elif char == 'β':
        rounded_rect(pen, 72, DESC, t, ASC-DESC, min(18, t*.28)); ring(pen, 236, 386, 146, 168, t); ring(pen, 236, 142, 146, 150, t)
    elif char == 'γ':
        diagonal(pen, 74, XH, 244, 114, t); diagonal(pen, 426, XH, 244, 114, t); rounded_rect(pen, 212, DESC, t, 154, min(18, t*.28))
    elif char == 'δ':
        ring(pen, 246, 226, 150, 226, t); pen.moveTo((154, 420)); pen.curveTo((120, 620), (220, 748), (374, 706)); pen.lineTo((356, 642)); pen.curveTo((258, 658), (214, 586), (218, 438)); pen.closePath()
    elif char == 'ε':
        open_c(pen, 250, 278, 174, 244, t, .16); rounded_rect(pen, 220, 246, 160, t, min(16, t*.24))
    elif char == 'η':
        rounded_rect(pen, 60, 0, t, XH, min(18, t*.28)); arch(pen, 124, 344, DESC, XH, t)
    elif char == 'θ':
        ring(pen, 250, 278, 170, 278, t); rounded_rect(pen, 104, 246, 292, t, min(16, t*.24))
    elif char == 'μ':
        rounded_rect(pen, 60, DESC, t, XH-DESC, min(18, t*.28)); rounded_rect(pen, 344-t, 0, t, XH, min(18, t*.28));
        pen.moveTo((124, 180)); pen.curveTo((124, 70), (160, 48), (234, 48)); pen.curveTo((306, 48), (344, 92), (344, 190)); pen.lineTo((280, 190)); pen.curveTo((280, 106), (264, 54), (234, 54)); pen.curveTo((202, 54), (124, 96), (124, 190)); pen.closePath()
    elif char == 'π':
        rounded_rect(pen, 58, XH-t, 384, t, min(18, t*.28)); rounded_rect(pen, 100, 0, t, XH, min(18, t*.28)); rounded_rect(pen, 342, 0, t, XH, min(18, t*.28))
    elif char == 'ρ':
        rounded_rect(pen, 66, DESC, t, XH-DESC, min(18, t*.28)); ring(pen, 232, 278, 150, 246, t)
    elif char in 'ςσ':
        open_c(pen, 250, 278, 180, 278, t, .12)
        if char == 'ς': rounded_rect(pen, 300, DESC, t, 162, min(18, t*.28))
    elif char == 'τ':
        rounded_rect(pen, 72, XH-t, 356, t, min(18, t*.28)); rounded_rect(pen, 218, 0, t, XH, min(18, t*.28))
    elif char == 'φ':
        ring(pen, 250, 278, 178, 242, t); rounded_rect(pen, 250-t*.5, DESC, t, ASC-DESC, min(18, t*.28))
    elif char == 'ψ':
        rounded_rect(pen, 250-t*.5, DESC, t, XH-DESC, min(18, t*.28)); open_c(pen, 158, 340, 105, 210, t, .36); open_c(pen, 342, 340, 105, 210, t, .36)
    elif char == 'ω':
        rounded_rect(pen, 56, 0, t, 250, min(18, t*.28)); rounded_rect(pen, 412-t, 0, t, 250, min(18, t*.28));
        pen.moveTo((56, 248)); pen.curveTo((56, 480), (154, 560), (250, 394)); pen.curveTo((346, 560), (444, 480), (444, 248)); pen.lineTo((380, 248)); pen.curveTo((380, 413), (326, 452), (250, 276)); pen.curveTo((174, 452), (120, 413), (120, 248)); pen.closePath()
    else:
        return False
    return True


def draw_cyrillic(pen, char, stem):
    """Direct forms for Cyrillic structures that differ materially from Latin."""
    t = stem
    if char == 'Д':
        diagonal(pen, 92, 0, 214, CAP, t); diagonal(pen, 408, 0, 286, CAP, t); rounded_rect(pen, 52, 0, 396, t, min(18, t*.28))
    elif char == 'Ж':
        rounded_rect(pen, 250-t*.5, 0, t, CAP, min(18, t*.28)); diagonal(pen, 74, CAP, 426, 0, t); diagonal(pen, 426, CAP, 74, 0, t)
    elif char == 'З': smooth_s(pen, 250, 350, 350, 700, t)
    elif char == 'Ц':
        rounded_rect(pen, 58, 150, t, CAP-150, min(18, t*.28)); rounded_rect(pen, 376, 0, t, CAP, min(18, t*.28)); rect(pen, 58, 0, 382, t); rounded_rect(pen, 376, DESC, t, 160, min(18, t*.28))
    elif char == 'Ч':
        rounded_rect(pen, 58, 330, t, CAP-330, min(18, t*.28)); rounded_rect(pen, 376, 0, t, CAP, min(18, t*.28)); rounded_rect(pen, 58, 300, 382, t, min(18, t*.28))
    elif char in 'ШЩ':
        for x in (58, 218, 376): rounded_rect(pen, x, 0, t, CAP, min(18, t*.28))
        rect(pen, 58, 0, 382, t)
        if char == 'Щ': rounded_rect(pen, 376, DESC, t, 160, min(18, t*.28))
    elif char == 'Ю':
        rounded_rect(pen, 54, 0, t, CAP, min(18, t*.28)); rounded_rect(pen, 54, 320, 138, t, min(18, t*.28)); ring(pen, 306, 350, 132, 250, t)
    elif char == 'Я':
        rounded_rect(pen, 376-t, 0, t, CAP, min(18, t*.28)); ring(pen, 246, 512, 160, 156, t); diagonal(pen, 262, 354, 72, 0, t)
    elif char == 'д':
        # Leave an interpolation margin above the -210 Windows descender;
        # quadratic conversion rounds the heavy diagonal slightly outward.
        ring(pen, 250, 234, 142, 234, t); diagonal(pen, 148, 0, 94, DESC+28, t); diagonal(pen, 352, 0, 406, DESC+28, t); rounded_rect(pen, 72, DESC+20, 356, t, min(18, t*.28))
    elif char == 'ж':
        rounded_rect(pen, 250-t*.5, 0, t, XH, min(18, t*.28)); diagonal(pen, 70, XH, 430, 0, t); diagonal(pen, 430, XH, 70, 0, t)
    elif char == 'з': smooth_s(pen, 250, 278, 330, 555, t)
    elif char == 'ц':
        rounded_rect(pen, 58, 150, t, XH-150, min(18, t*.28)); rounded_rect(pen, 376-t, 0, t, XH, min(18, t*.28)); rect(pen, 58, 0, 382, t); rounded_rect(pen, 376-t, DESC, t, 160, min(18, t*.28))
    elif char == 'ч':
        rounded_rect(pen, 58, 250, t, XH-250, min(18, t*.28)); rounded_rect(pen, 376-t, 0, t, XH, min(18, t*.28)); rounded_rect(pen, 58, 220, 382, t, min(18, t*.28))
    elif char in 'шщ':
        for x in (58, 218, 376-t): rounded_rect(pen, x, 0, t, XH, min(18, t*.28))
        rect(pen, 58, 0, 382, t)
        if char == 'щ': rounded_rect(pen, 376-t, DESC, t, 160, min(18, t*.28))
    elif char == 'ю':
        rounded_rect(pen, 54, 0, t, XH, min(18, t*.28)); rounded_rect(pen, 54, 246, 120, t, min(18, t*.28)); ring(pen, 306, 278, 126, 244, t)
    elif char == 'я':
        rounded_rect(pen, 376-t, 0, t, XH, min(18, t*.28)); ring(pen, 246, 398, 152, 150, t); diagonal(pen, 250, 246, 82, 0, t)
    else:
        return False
    return True


def draw_script_specific(pen, char, stem):
    return draw_greek(pen, char, stem) if char in GREEK_BASES else draw_cyrillic(pen, char, stem)


def add_glyph(font, codepoint, stem, family, redraw=False):
    name = glyph_name(codepoint)
    if name in font:
        if not redraw:
            return
        del font[name]
    char = chr(codepoint)
    script = 'greek' if codepoint in GREEK else 'cyrillic'
    base_name, base_char, marks = source_base(char, script)
    direct = base_char in SCRIPT_SPECIFIC
    if base_name not in font:
        return
    glyph = font.newGlyph(name)
    glyph.width = script_width(family) if direct else font[base_name].width
    glyph.unicodes = [codepoint]
    pen = glyph.getPen()
    if direct:
        draw_script_specific(pen, base_char, stem)
        if family == 'serif': add_serif_detail(pen, base_char, stem)
        if family == 'mono': add_mono_detail(pen, base_char, stem)
    else:
        glyph.components.append(Component(baseGlyph=base_name))
    for mark in marks:
        accent(pen, mark, glyph.width / 2, char.isupper(), stem)
    # Keep editor-only smooth flags identical across masters. The curve handles
    # carry the interpolation; inferred smooth flags can differ at Black.
    for contour in glyph.contours:
        for point in contour.points:
            point.smooth = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--redraw', action='store_true', help='Redraw existing Greek/Cyrillic review glyphs.')
    args = parser.parse_args()
    stems = {'sans': (30, 64, 150), 'serif': (24, 48, 118), 'mono': (28, 58, 132)}
    for family, (folder, prefix) in FAMILIES.items():
        for style, stem in zip(('Thin', 'Regular', 'Black'), stems[family]):
            path = ROOT / 'sources' / folder / f'{prefix}-{style}.ufo'
            font = Font.open(path)
            before = len(font)
            for codepoint in targets():
                add_glyph(font, codepoint, stem, family, redraw=args.redraw)
            font.save(path, overwrite=True)
            print(f'{family} {style}: {before} -> {len(font)} glyphs')


if __name__ == '__main__':
    main()
