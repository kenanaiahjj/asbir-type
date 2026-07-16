"""Create independent editable UFO/designspace foundations for Asbir Serif and Mono.

The sources deliberately draw original review glyphs. They do not copy, subset,
or modify any comparison font. They share only the Asbir family metrics and
design intent while each companion makes different structural choices.
"""
from pathlib import Path
import argparse

from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor
from ufoLib2 import Font

from expand_asbir_sans_sources import CAP, XH, ASC, DESC, diagonal, draw_char, glyph_name, rect, width_for
from generate_ufo_sources import a_outline, lower_a_outline

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'serif': {'stem': {100: 24, 400: 48, 900: 118}, 'name': 'Asbir Serif Review', 'prefix': 'AsbirSerif'},
    'mono': {'stem': {100: 28, 400: 58, 900: 132}, 'name': 'Asbir Mono Review', 'prefix': 'AsbirMono'},
}


def add_notdef(font):
    glyph = font.newGlyph('.notdef'); glyph.width = 600
    pen = glyph.getPen(); rect(pen, 80, 0, 440, CAP)


def companion_width(kind, ch):
    if kind == 'mono':
        return 600
    return width_for(ch) + (40 if ch.isalpha() else 0)


def add_serif_detail(pen, ch, stem):
    """Add restrained slab terminals to form the Serif foundation's own voice."""
    serif = max(18, round(stem * .42))
    if ch.isupper():
        rect(pen, 18, 0, 120, serif); rect(pen, 18, CAP-serif, 120, serif)
        rect(pen, 362, 0, 120, serif); rect(pen, 362, CAP-serif, 120, serif)
    elif ch.islower():
        if ch not in 'aceosvwxz': rect(pen, 38, 0, 100, serif)
        if ch in 'bdfhklt': rect(pen, 38, ASC-serif, 100, serif)
        if ch in 'gjpqy': rect(pen, 362, DESC, 100, serif)
        elif ch not in 'aceosvwxz': rect(pen, 362, 0, 100, serif)
    elif ch.isdigit():
        rect(pen, 80, 0, 80, serif); rect(pen, 340, 0, 80, serif)


def add_mono_detail(pen, ch, stem):
    """Build recognisable code forms without relying on a reference source."""
    if ch == '0': diagonal(pen, 150, 90, 350, 610, max(14, stem * .45))
    if ch in 'Il1':
        bar = max(18, stem * .55)
        rect(pen, 180, 0, 140, bar); rect(pen, 180, CAP-bar, 140, bar)
    if ch == 'O':
        rect(pen, 160, CAP // 2 - max(12, stem // 3), 180, max(24, stem * .66))


def make_master(kind, weight, style):
    spec = FAMILIES[kind]
    font = Font()
    font.info.familyName = spec['name']; font.info.styleName = style
    font.info.unitsPerEm = 1000; font.info.ascender = 840; font.info.descender = -240
    font.info.xHeight = XH; font.info.capHeight = CAP
    font.info.openTypeOS2WeightClass = weight
    font.info.openTypeOS2TypoAscender = 840; font.info.openTypeOS2TypoDescender = -240
    font.info.openTypeOS2WinAscent = 840; font.info.openTypeOS2WinDescent = 210
    font.info.postscriptFontName = f"{spec['prefix']}Review-{style}"
    font.info.openTypeNameVersion = 'Version 0.100'
    add_notdef(font)
    stem = spec['stem'][weight]
    for codepoint in range(32, 127):
        ch = chr(codepoint); glyph = font.newGlyph(glyph_name(ch))
        glyph.width = companion_width(kind, ch); glyph.unicodes = [codepoint]
        pen = glyph.getPen()
        if kind == 'serif' and ch == 'z':
            rect(pen, 70, XH-stem, 360, stem)
            diagonal(pen, 393, XH-stem*.66, 107, stem*.66, stem*.8)
            rect(pen, 70, 0, 360, stem)
        elif ch == 'A': a_outline(pen, stem)
        elif ch == 'a': lower_a_outline(pen, stem)
        else: draw_char(pen, ch, stem)
        if kind == 'serif': add_serif_detail(glyph.getPen(), ch, stem)
        if kind == 'mono': add_mono_detail(glyph.getPen(), ch, stem)
    nbsp = font.newGlyph('nbsp'); nbsp.width = companion_width(kind, ' '); nbsp.unicodes = [160]
    font.features.text = """feature kern {
  pos A V -48;
  pos A W -36;
  pos A Y -54;
  pos T o -36;
  pos T a -32;
  pos V a -42;
  pos Y o -52;
} kern;""" if kind == 'serif' else """feature kern {
  # Deliberately neutral: every Mono glyph has a 600-unit advance.
} kern;"""
    return font


def write_family(kind, reset=False):
    spec = FAMILIES[kind]
    source = ROOT / 'sources' / f'asbir-{kind}'
    designspace_path = source / f"{spec['prefix']}.designspace"
    if designspace_path.exists() and not reset:
        print(f'Editable {kind} sources already exist at {source}; refusing to overwrite them. Use --reset only to recreate the review foundation.')
        return
    source.mkdir(parents=True, exist_ok=True)
    masters = []
    for weight, style in ((100, 'Thin'), (400, 'Regular'), (900, 'Black')):
        path = source / f"{spec['prefix']}-{style}.ufo"
        make_master(kind, weight, style).save(path, overwrite=True)
        masters.append((path, weight, style))
    document = DesignSpaceDocument()
    axis = AxisDescriptor(); axis.tag = 'wght'; axis.name = 'Weight'; axis.minimum = 100; axis.default = 400; axis.maximum = 900
    document.addAxis(axis)
    for path, weight, style in masters:
        descriptor = SourceDescriptor(); descriptor.filename = path.name; descriptor.name = style
        descriptor.familyName = spec['name']; descriptor.styleName = style; descriptor.location = {'Weight': weight}
        descriptor.copyInfo = style == 'Regular'; descriptor.copyLib = style == 'Regular'; descriptor.copyFeatures = style == 'Regular'
        document.addSource(descriptor)
    for style, weight in (('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400), ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800), ('Black', 900)):
        instance = InstanceDescriptor(); instance.familyName = spec['name']; instance.styleName = style
        instance.location = {'Weight': weight}; instance.filename = f"{spec['prefix']}Review-{style}.ufo"
        document.addInstance(instance)
    document.write(designspace_path)
    print(f'Wrote independent {kind} sources to {source}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help='Replace existing Serif and Mono review sources. This destroys local UFO edits.')
    args = parser.parse_args()
    for family in FAMILIES:
        write_family(family, reset=args.reset)
