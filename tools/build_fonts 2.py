"""Build true, traceable review-font artifacts from the Asbir Sans source parameters.

The generated TTF, CFF OTF, and wght variable TTF are deliberately labelled *Review*.
They contain a deliberately small source slice used by this prototype. Production release
requires completed outlines, feature engineering, interpolation checks, and proofing
for every planned glyph before the name can lose its Review suffix.
"""
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.designspaceLib import AxisDescriptor, AxisLabelDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor
from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools import varLib
from fontTools.ttLib import newTable
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.otlLib.builder import buildStatTable
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "downloads"
OUT.mkdir(parents=True, exist_ok=True)
FONT_TIMESTAMP = timestampSinceEpoch(time.time())

def setup_gasp(fb):
    gasp = newTable('gasp')
    gasp.version = 1
    gasp.gaspRange = {65535: 0x000A}
    fb.font['gasp'] = gasp

def setup_smart_dropout(fb):
    prep = newTable('prep')
    prep.program = Program()
    prep.program.fromBytecode(b'\xb8\x01\xff\x85\xb0\x04\x8d')
    fb.font['prep'] = prep

def a_glyph(stem=70):
    pen = TTGlyphPen(None)
    pen.moveTo((80, 0)); pen.lineTo((220, 700)); pen.lineTo((260, 700)); pen.lineTo((400, 0)); pen.lineTo((400-stem, 0)); pen.lineTo((330, 210)); pen.lineTo((150, 210)); pen.lineTo((80+stem, 0)); pen.closePath()
    pen.moveTo((185, 320)); pen.lineTo((295, 320)); pen.lineTo((240, 520)); pen.closePath()
    return pen.glyph()

def lower_a_glyph(stem=64):
    """A single-storey, high-x-height a for review of the shared Sans direction."""
    pen = TTGlyphPen(None)
    pen.moveTo((104, 86)); pen.lineTo((104, 392)); pen.lineTo((104 + stem, 392)); pen.lineTo((104 + stem, 86)); pen.closePath()
    pen.moveTo((214, 90)); pen.lineTo((330, 90)); pen.lineTo((380, 142)); pen.lineTo((380, 276)); pen.lineTo((330, 328)); pen.lineTo((214, 328)); pen.lineTo((164, 276)); pen.lineTo((164, 142)); pen.closePath()
    return pen.glyph()

def empty_glyph():
    return TTGlyphPen(None).glyph()

def notdef():
    pen = TTGlyphPen(None); pen.moveTo((80, 0)); pen.lineTo((80, 700)); pen.lineTo((520, 700)); pen.lineTo((520, 0)); pen.closePath(); return pen.glyph()

def names(weight, style):
    suffix = {100: 'Thin', 400: 'Regular', 900: 'Black'}.get(weight, f'Weight {weight}')
    return {
        'familyName': 'Asbir Sans Review', 'styleName': suffix,
        'fullName': f'Asbir Sans Review {suffix}',
        'uniqueFontIdentifier': f'AsbirSansReview-{style}-{weight}',
        'version': 'Version 0.100',
        'psName': f'AsbirSansReview-{suffix}',
    }

def build_ttf(path: Path, weight=400):
    fb = FontBuilder(1000, isTTF=True)
    order = ['.notdef', 'space', 'nbsp', 'A', 'a']
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({32: 'space', 65: 'A', 97: 'a', 160: 'nbsp'})
    stem = {100: 30, 400: 64, 900: 150}.get(weight, 64)
    fb.setupGlyf({'.notdef': notdef(), 'space': empty_glyph(), 'nbsp': empty_glyph(), 'A': a_glyph(stem), 'a': lower_a_glyph(stem)})
    fb.setupHorizontalMetrics({'.notdef': (600, 0), 'space': (250, 0), 'nbsp': (250, 0), 'A': (480, 0), 'a': (440, 0)})
    fb.setupHorizontalHeader(ascent=760, descent=-240)
    fb.setupHead(fontRevision=0.100, created=FONT_TIMESTAMP, modified=FONT_TIMESTAMP)
    fb.setupNameTable(names(weight, 'TTF'), mac=False)
    fb.setupOS2(sTypoAscender=760, sTypoDescender=-240, usWinAscent=760, usWinDescent=0, usWeightClass=weight, sxHeight=555, sCapHeight=700, fsSelection=0x40, ulCodePageRange1=1)
    setup_gasp(fb); setup_smart_dropout(fb); fb.setupPost(); fb.setupMaxp(); fb.save(path)

def cff_charstring(points):
    pen = T2CharStringPen(480, None)
    for command, values in points:
        getattr(pen, command)(*values)
    return pen.getCharString(private=None, globalSubrs=None)

def build_otf(path: Path):
    fb = FontBuilder(1000, isTTF=False)
    order = ['.notdef', 'space', 'nbsp', 'A', 'a']
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({32: 'space', 65: 'A', 97: 'a', 160: 'nbsp'})
    a_points = [
      ('moveTo', ((80, 0),)), ('lineTo', ((220, 700),)), ('lineTo', ((260, 700),)), ('lineTo', ((400, 0),)),
      ('lineTo', ((336, 0),)), ('lineTo', ((330, 210),)), ('lineTo', ((150, 210),)), ('lineTo', ((144, 0),)), ('closePath', ()),
      ('moveTo', ((185, 320),)), ('lineTo', ((295, 320),)), ('lineTo', ((240, 520),)), ('closePath', ()),
    ]
    lower_a_points = [
      ('moveTo', ((104, 86),)), ('lineTo', ((104, 392),)), ('lineTo', ((168, 392),)), ('lineTo', ((168, 86),)), ('closePath', ()),
      ('moveTo', ((214, 90),)), ('lineTo', ((330, 90),)), ('lineTo', ((380, 142),)), ('lineTo', ((380, 276),)), ('lineTo', ((330, 328),)), ('lineTo', ((214, 328),)), ('lineTo', ((164, 276),)), ('lineTo', ((164, 142),)), ('closePath', ()),
    ]
    notdef_points = [('moveTo', ((80, 0),)), ('lineTo', ((80, 700),)), ('lineTo', ((520, 700),)), ('lineTo', ((520, 0),)), ('closePath', ())]
    empty_points = []
    fb.setupCFF('AsbirSansReview-Regular', {'FullName': 'Asbir Sans Review Regular', 'FamilyName': 'Asbir Sans Review', 'Weight': 'Regular', 'version': '0.100'}, {'.notdef': cff_charstring(notdef_points), 'space': cff_charstring(empty_points), 'nbsp': cff_charstring(empty_points), 'A': cff_charstring(a_points), 'a': cff_charstring(lower_a_points)}, {})
    fb.setupHorizontalMetrics({'.notdef': (600, 0), 'space': (250, 0), 'nbsp': (250, 0), 'A': (480, 0), 'a': (440, 0)})
    fb.setupHorizontalHeader(ascent=760, descent=-240)
    fb.setupHead(fontRevision=0.100, created=FONT_TIMESTAMP, modified=FONT_TIMESTAMP)
    fb.setupNameTable(names(400, 'CFF'), mac=False)
    fb.setupOS2(sTypoAscender=760, sTypoDescender=-240, usWinAscent=760, usWinDescent=0, usWeightClass=400, sxHeight=555, sCapHeight=700, fsSelection=0x40, ulCodePageRange1=1)
    fb.setupPost(); fb.setupMaxp(); fb.save(path)

def build_variable(thin, regular, black, output):
    designspace = DesignSpaceDocument()
    axis = AxisDescriptor(); axis.tag = 'wght'; axis.name = 'Weight'; axis.minimum = 100; axis.default = 400; axis.maximum = 900
    axis.axisLabels = [
        AxisLabelDescriptor(name='Thin', userValue=100),
        AxisLabelDescriptor(name='Regular', userValue=400, elidable=True),
        AxisLabelDescriptor(name='Bold', userValue=700, linkedUserValue=400),
        AxisLabelDescriptor(name='Black', userValue=900),
    ]
    designspace.addAxis(axis)
    for source_path, location, name in [(thin, 100, 'Thin'), (regular, 400, 'Regular'), (black, 900, 'Black')]:
        source = SourceDescriptor(); source.path = str(source_path); source.name = name; source.location = {'Weight': location}; source.copyLib = True; source.copyInfo = True; source.copyFeatures = True
        designspace.addSource(source)
    for style_name, location in [('Thin', 100), ('Regular', 400), ('Bold', 700), ('Black', 900)]:
        instance = InstanceDescriptor(); instance.familyName = 'Asbir Sans Review'; instance.styleName = style_name; instance.postScriptFontName = f'AsbirSansReview-{style_name}'; instance.location = {'Weight': location}
        designspace.addInstance(instance)
    designspace_path = OUT / 'AsbirSans-Review.designspace'
    designspace.write(designspace_path)
    variable_font, _, _ = varLib.build(str(designspace_path))
    buildStatTable(variable_font, [{'tag': 'wght', 'name': 'Weight', 'ordering': 0, 'values': [
        {'name': 'Thin', 'value': 100},
        {'name': 'Regular', 'value': 400, 'flags': 0x2},
        {'name': 'Bold', 'value': 700, 'linkedValue': 400},
        {'name': 'Black', 'value': 900},
    ]}], windowsNames=True, macNames=False)
    avar = newTable('avar'); avar.majorVersion = 1; avar.minorVersion = 0; avar.segments = {'wght': {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}}
    variable_font['avar'] = avar
    variable_font.save(output)

if __name__ == '__main__':
    masters = OUT / 'masters'; masters.mkdir(exist_ok=True)
    thin = masters / 'AsbirSans-Review-Thin.ttf'; regular = masters / 'AsbirSans-Review-Regular.ttf'; black = masters / 'AsbirSans-Review-Black.ttf'
    build_ttf(thin, 100); build_ttf(regular, 400); build_ttf(black, 900)
    build_ttf(OUT / 'AsbirSans-Review-Regular.ttf', 400)
    build_otf(OUT / 'AsbirSans-Review-Regular.otf')
    build_variable(thin, regular, black, OUT / 'AsbirSans-Review-VF.ttf')
    print(f'Wrote review artifacts to {OUT}')
