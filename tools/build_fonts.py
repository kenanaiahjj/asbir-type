"""Compile all editable Asbir UFO/designspace sources into review artifacts."""
from pathlib import Path
from shutil import copy2
import argparse
import subprocess
from tempfile import TemporaryDirectory
import time

from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables.ttProgram import Program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public' / 'downloads'
FONTMAKE = Path.home() / 'Library/Python/3.9/bin/fontmake'
FONT_TIMESTAMP = timestampSinceEpoch(time.time())
FONT_VERSION = '1.000'
FAMILIES = {
    # The Sans source is authored at Inter's native 2048 UPM and retains its
    # Text/Display optical-size masters. Do not downscale or clip it using the
    # earlier procedural 1000-UPM review metrics.
    'sans': {
        'folder': 'asbir-sans', 'prefix': 'AsbirSans', 'name': 'Asbir Sans', 'instance_prefix': 'AsbirSans',
        'xheight': 1118, 'capheight': 1490, 'ascender': 1984, 'descender': -494,
        # Keep the compact Inter-derived typo/hhea line metrics, but make the
        # Windows clipping box cover every encoded combining mark, encircled
        # form, and stacked accent in the compiled character set.
        'win_ascent': 2310, 'win_descent': 710,
    },
    'serif': {
        'folder': 'asbir-serif', 'prefix': 'AsbirSerif', 'name': 'Asbir Serif Review', 'instance_prefix': 'AsbirSerifReview',
        'xheight': 555, 'capheight': 700, 'ascender': 840, 'descender': -240,
        'win_ascent': 840, 'win_descent': 210,
    },
    'mono': {
        'folder': 'asbir-mono', 'prefix': 'AsbirMono', 'name': 'Asbir Mono Review', 'instance_prefix': 'AsbirMono',
        # Geist Mono's source has a generous lowercase and a broad Windows
        # clipping box for accents and technical symbols.
        'xheight': 530, 'capheight': 710, 'ascender': 800, 'descender': -150,
        'win_ascent': 1088, 'win_descent': 394,
    },
    'sans-italic': {
        'folder': 'asbir-sans-italic', 'prefix': 'AsbirSans', 'name': 'Asbir Sans',
        'instance_prefix': 'AsbirSansItalic', 'designspace': 'AsbirSansItalic.designspace',
        'output_prefix': 'AsbirSans-Review-Italic', 'italic': True, 'variable_style': 'Italic',
        'xheight': 1118, 'capheight': 1490, 'ascender': 1984, 'descender': -494,
        'win_ascent': 2310, 'win_descent': 710,
    },
    'mono-italic': {
        'folder': 'asbir-mono-italic', 'prefix': 'AsbirMono', 'name': 'Asbir Mono Review',
        'instance_prefix': 'AsbirMonoItalic', 'designspace': 'AsbirMonoItalic.designspace',
        'output_prefix': 'AsbirMono-Review-Italic', 'italic': True, 'variable_style': 'Italic',
        'xheight': 530, 'capheight': 710, 'ascender': 800, 'descender': -150,
        'win_ascent': 1088, 'win_descent': 394,
    },
}
SANS_STATIC_INSTANCES = (
    ('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400),
    ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800), ('Black', 900),
)
STATIC_INSTANCES = {key: SANS_STATIC_INSTANCES for key in FAMILIES}


def run_fontmake(*args):
    executable = str(FONTMAKE) if FONTMAKE.exists() else 'fontmake'
    subprocess.run([executable, *args], check=True, cwd=ROOT)


def normalize_designspace_instances():
    subprocess.run(['python3', str(ROOT / 'tools' / 'normalize_designspace_instances.py')], check=True, cwd=ROOT)


def set_windows_name(font, name_id, value):
    font['name'].setName(value, name_id, 3, 1, 0x409)


def replace_name(font, name_id, value):
    """Set one user-facing name consistently and remove legacy Mac names."""
    font['name'].names = [record for record in font['name'].names if record.nameID != name_id]
    set_windows_name(font, name_id, value)


def set_release_names(font, path, metrics, variable, style_name=None):
    family = metrics['name']
    prefix = metrics['prefix']
    if variable:
        style = style_name or 'Variable'
        subfamily = 'Italic' if style_name == 'Italic' else 'Regular'
        postscript = f"{prefix}-{'-'.join(style.split())}"
    else:
        style = style_name or path.stem.removeprefix(f'{prefix}-Review-').replace('-', ' ')
        subfamily = style
        postscript = f"{prefix}-{'-'.join(style.split())}"
    full_name = f'{family} {style}'
    # Asbir Sans is a renamed OFL derivative; no Inter family, full, preferred,
    # PostScript, or trademark name may leak into a distributed binary. Preserve
    # the original copyright (name ID 0) as required attribution under OFL.
    for name_id, value in (
        (1, family), (2, subfamily), (3, f'{postscript};Version {FONT_VERSION}'),
        (4, full_name), (5, f'Version {FONT_VERSION}'), (6, postscript),
        (16, family), (17, subfamily), (18, full_name), (25, prefix),
    ):
        replace_name(font, name_id, value)
    if prefix in {'AsbirSans', 'AsbirMono'}:
        font['name'].names = [record for record in font['name'].names if record.nameID != 7]
    font['name'].names = [record for record in font['name'].names if record.platformID != 1]
    if 'CFF ' in font:
        font['CFF '].cff.fontNames = [postscript]
        for top_dict in font['CFF '].cff.topDictIndex:
            top_dict.FontName = postscript


def setup_gasp(font):
    gasp = newTable('gasp'); gasp.version = 1; gasp.gaspRange = {65535: 0x000A}
    font['gasp'] = gasp


def setup_smart_dropout(font):
    prep = newTable('prep'); prep.program = Program(); prep.program.fromBytecode(b'\xb8\x01\xff\x85\xb0\x04\x8d')
    font['prep'] = prep


def patch_common(path, metrics, variable=False, weight=400, instances=SANS_STATIC_INSTANCES, style_name=None):
    font = TTFont(path)
    font['head'].fontRevision = float(FONT_VERSION)
    font['head'].created = FONT_TIMESTAMP; font['head'].modified = FONT_TIMESTAMP
    os2 = font['OS/2']
    os2.sxHeight = metrics['xheight']; os2.sCapHeight = metrics['capheight']
    os2.sTypoAscender = metrics['ascender']; os2.sTypoDescender = metrics['descender']; os2.sTypoLineGap = 0
    os2.usWinAscent = metrics['win_ascent']; os2.usWinDescent = metrics['win_descent']; os2.ulCodePageRange1 |= 1
    os2.usWeightClass = weight
    # Use typo metrics in Windows so the unclipped win box does not dictate
    # line spacing; the 840 ascender covers the tallest interpolated accents.
    os2.fsSelection |= 1 << 7
    font['hhea'].ascent = metrics['ascender']; font['hhea'].descent = metrics['descender']; font['hhea'].lineGap = 0
    if metrics.get('italic') or style_name and style_name.startswith('Italic'):
        # Mark the binaries as a real italic face for platform style linking.
        # The outlines are already italic masters; these records keep OS/2/head/
        # post metadata in agreement for CSS, desktop installers, and QA tools.
        os2.fsSelection |= 1
        os2.fsSelection &= ~(1 << 6)
        font['head'].macStyle |= 1 << 1
        font['post'].italicAngle = -12.0
    set_release_names(font, path, metrics, variable, style_name=style_name)
    if 'glyf' in font:
        setup_gasp(font); setup_smart_dropout(font)
    if metrics['prefix'] == 'AsbirMono':
        font['post'].isFixedPitch = 1
        os2.xAvgCharWidth = 600
        panose = os2.panose
        panose.bFamilyType = 2; panose.bSerifStyle = 11; panose.bWeight = min(10, max(2, round(weight / 100) + 1))
        panose.bProportion = 9; panose.bContrast = 2; panose.bStrokeVariation = 2
        panose.bArmStyle = 2; panose.bLetterForm = 4; panose.bMidline = 2; panose.bXHeight = 4
    if variable and metrics['prefix'] == 'AsbirSans':
        # The variable Sans exposes both optical size and weight. A full STAT
        # table is required so fvar named instances resolve correctly in Adobe
        # apps and to avoid FontBakery's fvar/STAT consistency failure.
        buildStatTable(font, [
            {'tag': 'opsz', 'name': 'Optical Size', 'ordering': 0, 'values': [
                {'name': 'Text', 'value': 14, 'flags': 0x2},
                {'name': 'Display', 'value': 32},
            ]},
            {'tag': 'wght', 'name': 'Weight', 'ordering': 1, 'values': [
                {'name': 'Thin', 'value': 100},
                {'name': 'ExtraLight', 'value': 200},
                {'name': 'Light', 'value': 300},
                {'name': 'Regular', 'value': 400, 'flags': 0x2},
                {'name': 'Medium', 'value': 500},
                {'name': 'SemiBold', 'value': 600},
                {'name': 'Bold', 'value': 700, 'linkedValue': 400},
                {'name': 'ExtraBold', 'value': 800},
                {'name': 'Black', 'value': 900},
            ]},
        ], windowsNames=True, macNames=False)
    elif variable and len(font['fvar'].axes) == 1 and font['fvar'].axes[0].axisTag == 'wght':
        values = []
        for style, value in instances:
            entry = {'name': style, 'value': value}
            if value == 400:
                entry['flags'] = 0x2
            if style == 'Bold':
                entry['linkedValue'] = 400
            values.append(entry)
        buildStatTable(font, [{'tag': 'wght', 'name': 'Weight', 'ordering': 0, 'values': values}], windowsNames=True, macNames=False)
        if 'avar' not in font:
            avar = newTable('avar'); avar.majorVersion = 1; avar.minorVersion = 0
            avar.segments = {'wght': {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}}
            font['avar'] = avar
        # Variable-font PostScript instance names are optional. Keeping the
        # variable binary's Name ID 6 as ``AsbirMono-Variable`` while fvar's
        # default instance says ``AsbirMono-Regular`` violates the fvar naming
        # contract, so omit optional instance PS records instead of publishing
        # contradictory names.
        if metrics['prefix'] == 'AsbirMono':
            for instance in font['fvar'].instances:
                instance.postscriptNameID = 0xFFFF
    if variable and metrics.get('italic') and 'fvar' in font:
        # Keep the dedicated italic variable's named instances discoverable by
        # platform tooling (Regular Italic/Bold Italic conventions), while
        # making the default instance point to the file's own name IDs.
        weight_names = {value: style for style, value in instances}
        for instance in font['fvar'].instances:
            weight = round(instance.coordinates.get('wght', 400))
            weight_name = weight_names.get(weight, 'Regular')
            instance_style = 'Italic' if weight == 400 else f'{weight_name} Italic'
            if weight == 400:
                instance.subfamilyNameID = 2
                instance.postscriptNameID = 6 if metrics['prefix'] == 'AsbirSans' else 0xFFFF
            else:
                replace_name(font, instance.subfamilyNameID, instance_style)
                if instance.postscriptNameID != 0xFFFF:
                    replace_name(font, instance.postscriptNameID, f"{metrics['prefix']}-{'-'.join(instance_style.split())}")
    font.save(path)


def build_family(key, spec):
    source = ROOT / 'sources' / spec['folder']
    designspace = source / spec.get('designspace', f"{spec['prefix']}.designspace")
    if not designspace.exists():
        raise SystemExit(f'Missing editable Asbir {key} sources in {source}.')
    output_prefix = spec.get('output_prefix', f"{spec['prefix']}-Review")
    variable = OUT / f"{output_prefix}-VF.ttf"
    variable_filters = ()
    if spec['prefix'] in {'AsbirSans', 'AsbirMono'}:
        # Variable-font renderers have historically been less robust with
        # nested or transformed components. Decompose them at compile time;
        # static instances already receive the equivalent processing.
        variable_filters = ('--filter', '...', '--filter', 'DecomposeComponentsFilter')
    run_fontmake('-m', str(designspace), '-o', 'variable', '--output-path', str(variable), *variable_filters)
    instances = STATIC_INSTANCES[key]
    patch_common(variable, spec, variable=True, instances=instances, style_name=spec.get('variable_style'))
    # Build every named static instance from the same designspace. This creates
    # real CFF OTFs and TrueType TTFs, not renamed copies of a single Regular.
    with TemporaryDirectory(prefix=f'{spec["prefix"]}-instances-') as temp_dir:
        instance_dir = Path(temp_dir)
        run_fontmake('-m', str(designspace), '-i', '-o', 'ttf', 'otf', '--output-dir', str(instance_dir))
        for style, weight in instances:
            for extension in ('ttf', 'otf'):
                built = instance_dir / f'{spec["instance_prefix"]}-{style}.{extension}'
                # The Geist Mono source retains its original instance filename
                # metadata even after family/postscript records are renamed.
                # Fontmake uses that filename only for its temporary output;
                # every copied review binary is renamed and patched below.
                if not built.exists() and spec['prefix'] == 'AsbirMono':
                    built = instance_dir / f'GeistMono-{style}.{extension}'
                target = OUT / f'{output_prefix}-{style}.{extension}'
                if not built.exists():
                    raise SystemExit(f'Missing {style} {extension} instance from {designspace}.')
                copy2(built, target)
                static_style = f"Italic {style}" if spec.get('italic') else None
                patch_common(target, spec, weight=weight, instances=instances, style_name=static_style)
    print(f'Compiled {key} review fonts from {source}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=tuple(FAMILIES), action='append')
    parser.add_argument('--italic', action='store_true', help='Build italic variants for Sans and Mono too')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    normalize_designspace_instances()
    selected = list(args.family or ('sans', 'serif', 'mono'))
    if args.italic:
        selected.extend(f'{base}-italic' for base in tuple(selected) if f'{base}-italic' in FAMILIES)
    for key in selected:
        spec = FAMILIES[key]
        build_family(key, spec)


if __name__ == '__main__':
    main()
