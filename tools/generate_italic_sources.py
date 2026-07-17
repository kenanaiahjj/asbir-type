"""Generate editable Asbir italic UFO/designspace sources.

The existing Asbir UFOs remain the source of truth for feature glyphs and
identity forms. Core glyphs are replaced with the corresponding OFL italic
masters from the approved upstream foundations, while Asbir-only constructions
are transformed and retained. This produces a real italic source family rather
than a CSS or binary-only oblique.
"""
from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

import glyphsLib
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from ufoLib2 import Font

try:
    from release_version import FONT_VERSION
except ModuleNotFoundError:
    from tools.release_version import FONT_VERSION


ROOT = Path(__file__).resolve().parents[1]
INTER_ITALIC = Path('/Users/kenanaiahjolmfc/Downloads/inter-master/src/Inter-Italic.glyphspackage')
GEIST_MONO_ITALIC = ROOT / 'third_party' / 'geist-font' / 'sources' / 'GeistMono-Italic.glyphspackage'
SHEAR = 0.18

FAMILIES = {
    'sans': {
        'base_folder': ROOT / 'sources' / 'asbir-sans',
        'base_designspace': ROOT / 'sources' / 'asbir-sans' / 'AsbirSans.designspace',
        'output_folder': ROOT / 'sources' / 'asbir-sans-italic',
        'output_designspace': 'AsbirSansItalic.designspace',
        'upstream': INTER_ITALIC,
        'prefix': 'AsbirSansItalic',
        'family_name': 'Asbir Sans',
        'source_style_prefix': 'Italic ',
        'upstream_prefix': 'Inter-',
        'custom_bases': {'a', 't', 'G', 'one', 'four'},
    },
    'mono': {
        'base_folder': ROOT / 'sources' / 'asbir-mono',
        'base_designspace': ROOT / 'sources' / 'asbir-mono' / 'AsbirMono.designspace',
        'output_folder': ROOT / 'sources' / 'asbir-mono-italic',
        'output_designspace': 'AsbirMonoItalic.designspace',
        'upstream': GEIST_MONO_ITALIC,
        'prefix': 'AsbirMonoItalic',
        'family_name': 'Asbir Mono',
        'source_style_prefix': 'Italic ',
        'upstream_prefix': 'GeistMono-',
        # Keep the transformed zero and its feature components together so a
        # slashed zero never receives a second italic transform.
        'custom_bases': {'zero'},
    },
}


def load_upstream_masters(source: Path, output: Path) -> dict[tuple[tuple[str, float], ...], Path]:
    output.mkdir(parents=True, exist_ok=True)
    previous_cwd = Path.cwd()
    try:
        # Glyphs packages keep feature includes relative to their source root.
        os.chdir(source.parent)
        font = glyphsLib.load(source)
        for glyph in font.glyphs:
            for layer in glyph.layers:
                layer._background = None
        designspace_path = output / 'upstream.designspace'
        glyphsLib.build_masters(
            font,
            master_dir=output,
            designspace_path=designspace_path,
            minimal=True,
            store_editor_state=False,
            expand_includes=True,
        )
    finally:
        os.chdir(previous_cwd)
    document = DesignSpaceDocument.fromfile(designspace_path)
    result = {}
    for descriptor in document.sources:
        location = tuple(sorted((axis, float(value)) for axis, value in descriptor.location.items()))
        result[location] = output / descriptor.filename
    return result


def transform_glyph(glyph, width: int | None = None) -> None:
    anchors = [(anchor.name, anchor.x, anchor.y, anchor.color) for anchor in glyph.anchors]
    recording = RecordingPen()
    glyph.draw(recording)
    glyph.clearContours()
    glyph.clearComponents()
    glyph.clearAnchors()
    output = TransformPen(glyph.getPen(), (1, 0, SHEAR, 1, 0, 0))
    recording.replay(output)
    for name, x, y, color in anchors:
        glyph.appendAnchor({'name': name, 'x': round(x + SHEAR * y, 4), 'y': y, 'color': color})
    if width is not None:
        glyph.width = width


def depends_on_custom_base(glyph, custom_bases: set[str]) -> bool:
    return any(component.baseGlyph in custom_bases for component in glyph.components)


def copy_raw_glyph(target, source, width: int | None = None) -> None:
    unicode_values = list(target.unicodes)
    target.copyDataFromGlyph(source)
    target.unicodes = unicode_values or list(source.unicodes)
    if width is not None:
        target.width = width


def prepare_master(base_path: Path, raw_path: Path, output_path: Path, spec: dict, source_style: str) -> None:
    shutil.copytree(base_path, output_path)
    base = Font.open(output_path)
    raw = Font.open(raw_path)
    for glyph in base:
        transform_glyph(glyph, width=600 if spec['prefix'].startswith('AsbirMono') else None)

    feature_suffixes = ('.pnum', '.onum', '.numr', '.dnom', '.sups', '.subs', '.ordn', '.slash')
    for name in raw.keys():
        raw_glyph = raw[name]
        if name not in base or name in spec['custom_bases']:
            continue
        if name.endswith(feature_suffixes) or name.startswith(('f_f', 'f_i', 'f_l')):
            continue
        if depends_on_custom_base(raw_glyph, spec['custom_bases']):
            continue
        copy_raw_glyph(base[name], raw_glyph, width=600 if spec['prefix'].startswith('AsbirMono') else None)

    base.info.familyName = spec['family_name']
    base.info.styleName = source_style
    base.info.postscriptFontName = f"{spec['prefix']}-{source_style.replace(' ', '')}"
    base.info.openTypeNamePreferredFamilyName = spec['family_name']
    base.info.openTypeNamePreferredSubfamilyName = source_style
    base.info.openTypeNameCompatibleFullName = f"{spec['family_name']} {source_style}"
    base.info.openTypeNameVersion = f'Version {FONT_VERSION}; Asbir italic source'
    base.lib['com.asbir.italicSource'] = 'OFL upstream italic masters with Asbir identity and feature constructions'
    base.save(output_path, overwrite=True)


def source_map(document: DesignSpaceDocument, prefix: str) -> dict[tuple[tuple[str, float], ...], tuple[str, str]]:
    result = {}
    for source in document.sources:
        location = tuple(sorted((key, float(value)) for key, value in source.location.items()))
        result[location] = (source.filename, source.styleName or source.name or '')
    return result


def generate_family(key: str, replace: bool = False) -> None:
    spec = FAMILIES[key]
    if not spec['upstream'].exists():
        raise SystemExit(f'Missing upstream italic source: {spec["upstream"]}')
    if spec['output_folder'].exists():
        if not replace:
            raise SystemExit(f'{spec["output_folder"]} already exists; use --replace to regenerate it.')
        shutil.rmtree(spec['output_folder'])
    spec['output_folder'].mkdir(parents=True)
    base_document = DesignSpaceDocument.fromfile(spec['base_designspace'])
    base_by_location = source_map(base_document, spec['prefix'])
    with tempfile.TemporaryDirectory(prefix=f'{key}-italic-upstream-') as temp:
        raw_by_location = load_upstream_masters(spec['upstream'], Path(temp))
        output_sources = []
        for location, (base_filename, base_style) in base_by_location.items():
            raw_path = raw_by_location.get(location)
            if raw_path is None:
                raise SystemExit(f'No upstream italic master matches {key} location {location}')
            style = f'{spec["source_style_prefix"]}{base_style.removeprefix("Asbir Sans ").removeprefix("Asbir Mono ")}'
            output_filename = f'{spec["prefix"]}-{style.replace(" ", "")}.ufo'
            prepare_master(
                spec['base_folder'] / base_filename,
                raw_path,
                spec['output_folder'] / output_filename,
                spec,
                style,
            )
            output_sources.append((location, output_filename, style))

    output_document = DesignSpaceDocument()
    for axis in base_document.axes:
        output_document.addAxis(axis)
    for location, filename, style in output_sources:
        source = next(item for item in base_document.sources if tuple(sorted((key, float(value)) for key, value in item.location.items())) == location)
        descriptor = type(source)()
        descriptor.filename = filename
        descriptor.name = f'{spec["family_name"]} {style}'
        descriptor.familyName = spec['family_name']
        descriptor.styleName = style
        descriptor.location = dict(source.location)
        descriptor.copyInfo = source.copyInfo
        descriptor.copyLib = source.copyLib
        descriptor.copyGroups = source.copyGroups
        descriptor.copyFeatures = source.copyFeatures
        output_document.addSource(descriptor)
    for instance in base_document.instances:
        style = f'{spec["source_style_prefix"]}{instance.styleName}'
        descriptor = type(instance)()
        descriptor.name = f'{spec["family_name"]} {style}'
        descriptor.familyName = spec['family_name']
        descriptor.styleName = style
        descriptor.location = dict(instance.location)
        descriptor.filename = f'{spec["prefix"]}-{instance.styleName}.ufo'
        descriptor.postScriptFontName = f'{spec["prefix"]}-{instance.styleName}'
        descriptor.styleMapFamilyName = f'{spec["family_name"]} {instance.styleName}'
        descriptor.styleMapStyleName = 'italic'
        output_document.addInstance(descriptor)
    output_document.write(spec['output_folder'] / spec['output_designspace'])
    print(f'Generated {key} italic sources in {spec["output_folder"]}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('sans', 'mono'), action='append')
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    for family in args.family or ('sans', 'mono'):
        generate_family(family, replace=args.replace)


if __name__ == '__main__':
    main()
