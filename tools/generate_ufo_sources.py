"""Generate editable UFO/designspace sources for the current Asbir Sans slice.

The UFOs are the canonical editable source. They deliberately mirror the current
small glyph set while the family is being drawn; do not ship from this source
until the production gate has passed.
"""
import argparse
from pathlib import Path
from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor
from ufoLib2 import Font

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-sans'

def a_outline(pen, stem):
    pen.moveTo((80, 0)); pen.lineTo((220, 700)); pen.lineTo((260, 700)); pen.lineTo((400, 0)); pen.lineTo((400-stem, 0)); pen.lineTo((330, 210)); pen.lineTo((150, 210)); pen.lineTo((80+stem, 0)); pen.closePath()
    pen.moveTo((185, 320)); pen.lineTo((295, 320)); pen.lineTo((240, 520)); pen.closePath()

def lower_a_outline(pen, stem):
    pen.moveTo((104, 86)); pen.lineTo((104, 392)); pen.lineTo((104 + stem, 392)); pen.lineTo((104 + stem, 86)); pen.closePath()
    pen.moveTo((214, 90)); pen.lineTo((330, 90)); pen.lineTo((380, 142)); pen.lineTo((380, 276)); pen.lineTo((330, 328)); pen.lineTo((214, 328)); pen.lineTo((164, 276)); pen.lineTo((164, 142)); pen.closePath()

def add_glyph(font, name, width, unicode=None, outline=None):
    glyph = font.newGlyph(name)
    glyph.width = width
    if unicode is not None:
        glyph.unicodes = [unicode]
    if outline:
        outline(glyph.getPen())

def make_master(weight, style):
    font = Font()
    font.info.familyName = 'Asbir Sans Review'
    font.info.styleName = style
    font.info.unitsPerEm = 1000
    font.info.ascender = 840
    font.info.descender = -240
    font.info.xHeight = 555
    font.info.capHeight = 700
    font.info.openTypeOS2WeightClass = weight
    font.info.openTypeOS2TypoAscender = 840
    font.info.openTypeOS2TypoDescender = -240
    font.info.openTypeOS2WinAscent = 840
    font.info.openTypeOS2WinDescent = 210
    font.info.postscriptFontName = f'AsbirSansReview-{style}'
    font.info.openTypeNameVersion = 'Version 0.100'
    stem = {100: 30, 400: 64, 900: 150}[weight]
    add_glyph(font, '.notdef', 600, outline=lambda pen: (pen.moveTo((80, 0)), pen.lineTo((80, 700)), pen.lineTo((520, 700)), pen.lineTo((520, 0)), pen.closePath()))
    add_glyph(font, 'space', 250, 32)
    add_glyph(font, 'nbsp', 250, 160)
    add_glyph(font, 'A', 480, 65, lambda pen: a_outline(pen, stem))
    add_glyph(font, 'a', 440, 97, lambda pen: lower_a_outline(pen, stem))
    return font

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help='Replace the starter source tree. This destroys local UFO edits.')
    args = parser.parse_args()
    designspace_path = SOURCE / 'AsbirSans.designspace'
    if designspace_path.exists() and not args.reset:
        print(f'Editable sources already exist at {SOURCE}; refusing to overwrite them. Use --reset only to recreate the starter slice.')
        return
    SOURCE.mkdir(parents=True, exist_ok=True)
    masters = []
    for weight, style in [(100, 'Thin'), (400, 'Regular'), (900, 'Black')]:
        path = SOURCE / f'AsbirSans-{style}.ufo'
        make_master(weight, style).save(path, overwrite=True)
        masters.append((path, weight, style))
    designspace = DesignSpaceDocument()
    axis = AxisDescriptor(); axis.tag = 'wght'; axis.name = 'Weight'; axis.minimum = 100; axis.default = 400; axis.maximum = 900
    designspace.addAxis(axis)
    for path, weight, style in masters:
        source = SourceDescriptor(); source.filename = path.name; source.name = style; source.familyName = 'Asbir Sans Review'; source.styleName = style; source.location = {'Weight': weight}
        source.copyInfo = style == 'Regular'; source.copyLib = style == 'Regular'; source.copyFeatures = style == 'Regular'
        designspace.addSource(source)
    for style, weight in [('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400), ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800), ('Black', 900)]:
        instance = InstanceDescriptor(); instance.familyName = 'Asbir Sans Review'; instance.styleName = style; instance.location = {'Weight': weight}; instance.filename = f'AsbirSansReview-{style}.ufo'
        designspace.addInstance(instance)
    designspace.write(designspace_path)
    print(f'Wrote editable sources to {SOURCE}')

if __name__ == '__main__':
    main()
