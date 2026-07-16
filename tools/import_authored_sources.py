"""Import the approved, authored source foundations into editable Asbir UFOs.

This is deliberately an import step rather than a binary rename.  It keeps
editable masters and the designspace axes, records the upstream origin, and
removes only Glyphs background layers that cannot be represented safely by the
current UFO converter.  No outlines are redrawn or discarded by this step.

The current Sans foundation is Inter Roman, licensed under SIL OFL 1.1.
"""
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

import glyphsLib
from fontTools.designspaceLib import DesignSpaceDocument, InstanceDescriptor
from ufoLib2 import Font


ROOT = Path(__file__).resolve().parents[1]
INTER_SOURCE = Path('/Users/kenanaiahjolmfc/Downloads/inter-master/src/Inter-Roman.glyphspackage')
INTER_LICENSE = Path('/Users/kenanaiahjolmfc/Downloads/inter-master/LICENSE.txt')
SANS_DESTINATION = ROOT / 'sources' / 'asbir-sans'
SANS_PREFIX = 'AsbirSans'
GEIST_MONO_SOURCE = ROOT / 'third_party' / 'geist-font' / 'sources' / 'GeistMono.glyphspackage'
GEIST_MONO_LICENSE = ROOT / 'third_party' / 'geist-font' / 'OFL.txt'
MONO_DESTINATION = ROOT / 'sources' / 'asbir-mono'
MONO_PREFIX = 'AsbirMono'

WEIGHT_INSTANCES = (
    ('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400),
    ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800),
    ('Black', 900),
)
WEIGHT_TO_INTER_DESIGN = {100: 100, 200: 200, 300: 300, 400: 400, 500: 490, 600: 580, 700: 670, 800: 780, 900: 900}


def _load_without_backgrounds(source: Path):
    """Work around glyphsLib's duplicate-background-layer conversion bug.

    Background layers are editor history, not exported outlines. Removing them
    in memory leaves every foreground contour, component, anchor, feature and
    kerning record intact while producing valid UFO masters.
    """
    font = glyphsLib.load(source)
    for glyph in font.glyphs:
        for layer in glyph.layers:
            layer._background = None
    return font


def _style_from_source(filename: str) -> str:
    mapping = {
        'Inter-Thin.ufo': 'Text Thin',
        'Inter-Regular.ufo': 'Text Regular',
        'Inter-Black.ufo': 'Text Black',
        'Inter-DisplayThin.ufo': 'Display Thin',
        'Inter-Display.ufo': 'Display Regular',
        'Inter-DisplayBlack.ufo': 'Display Black',
    }
    try:
        return mapping[filename]
    except KeyError as exc:
        raise ValueError(f'Unexpected Inter master filename: {filename}') from exc


def _postscript_style(style: str) -> str:
    return ''.join(part for part in style.title().split())


def import_sans(replace: bool) -> None:
    if not INTER_SOURCE.exists() or not INTER_LICENSE.exists():
        raise SystemExit('Inter source or its OFL license is unavailable at the approved local source path.')
    if SANS_DESTINATION.exists() and any(SANS_DESTINATION.iterdir()) and not replace:
        raise SystemExit(f'{SANS_DESTINATION} already exists. Use --replace after preserving the review source.')

    staging = ROOT / '.build' / 'inter-ufo-import'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    previous_cwd = Path.cwd()
    try:
        # Inter's hand-authored feature includes are relative to src/.
        os.chdir(INTER_SOURCE.parent)
        glyphsLib.build_masters(
            _load_without_backgrounds(INTER_SOURCE),
            master_dir=staging,
            designspace_path=staging / 'Inter-Roman.designspace',
            minimal=True,
            store_editor_state=False,
            expand_includes=True,
        )
    finally:
        os.chdir(previous_cwd)
    document = DesignSpaceDocument.fromfile(staging / 'Inter-Roman.designspace')
    filename_map: dict[str, str] = {}
    for source in document.sources:
        original = Path(source.filename).name
        style = _style_from_source(original)
        destination_name = f'{SANS_PREFIX}-{_postscript_style(style)}.ufo'
        filename_map[original] = destination_name
        source.filename = destination_name
        # glyphsLib stores an absolute ``path`` in addition to ``filename``.
        # Designspace serialization prefers that path unless it is updated too.
        source.path = str(staging / destination_name)
        source.name = f'Asbir Sans {style}'
        source.familyName = 'Asbir Sans'
        source.styleName = style

        ufo_path = staging / original
        ufo = Font.open(ufo_path)
        ufo.info.familyName = 'Asbir Sans'
        ufo.info.styleName = style
        ufo.info.postscriptFontName = f'{SANS_PREFIX}-{_postscript_style(style)}'
        ufo.info.openTypeNamePreferredFamilyName = 'Asbir Sans'
        ufo.info.openTypeNamePreferredSubfamilyName = style
        ufo.info.openTypeNameCompatibleFullName = f'Asbir Sans {style}'
        ufo.info.openTypeNameVersion = 'Version 0.100; derived from Inter'
        ufo.lib['com.asbir.foundation'] = 'Inter Roman v4 source, SIL OFL 1.1'
        ufo.save(ufo_path, overwrite=True)

    # The variable font retains both Text/Display optical masters. Static
    # releases use the Text optical-size default and one instance per weight.
    document.instances.clear()
    for style, weight in WEIGHT_INSTANCES:
        instance = InstanceDescriptor()
        instance.name = f'Asbir Sans {style}'
        instance.familyName = 'Asbir Sans'
        instance.styleName = style
        instance.filename = f'{SANS_PREFIX}-{style}.ufo'
        # The Inter designspace has a calibrated non-linear weight map. An
        # instance location is in *design* space, so using the user-facing
        # values directly would expose 511/622/727/817 instead of the named
        # 500/600/700/800 locations in the variable font.
        instance.location = {'Optical size': 14, 'Weight': WEIGHT_TO_INTER_DESIGN[weight]}
        document.addInstance(instance)

    for original, destination_name in filename_map.items():
        (staging / original).rename(staging / destination_name)
    destination_designspace = staging / f'{SANS_PREFIX}.designspace'
    document.write(destination_designspace)
    (staging / 'Inter-Roman.designspace').unlink()

    archive = ROOT / 'sources' / 'archive' / 'procedural-asbir-sans-review'
    if SANS_DESTINATION.exists():
        procedural_regular = SANS_DESTINATION / f'{SANS_PREFIX}-Regular.ufo'
        if procedural_regular.exists():
            if archive.exists():
                raise SystemExit(f'Procedural archive already exists: {archive}')
            archive.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(SANS_DESTINATION), archive)
        else:
            # A prior authored import can be recreated from the upstream
            # source; never overwrite the preserved procedural archive.
            shutil.rmtree(SANS_DESTINATION)
    shutil.move(str(staging), SANS_DESTINATION)

    notices = ROOT / 'THIRD_PARTY_NOTICES.md'
    notices.write_text(
        '# Asbir Font Foundations\n\n'
        '## Asbir Sans\n\n'
        'Asbir Sans is derived from Inter Roman source by The Inter Project Authors. '
        'The source foundation and all derivative font software are licensed under the '
        'SIL Open Font License, Version 1.1. The upstream copyright notice and full '
        'license are reproduced below.\n\n---\n\n'
        + INTER_LICENSE.read_text()
    )
    print(f'Imported six editable Inter masters into {SANS_DESTINATION}')
    print(f'Archived procedural review masters at {archive}')


def import_mono(replace: bool) -> None:
    if not GEIST_MONO_SOURCE.exists() or not GEIST_MONO_LICENSE.exists():
        raise SystemExit('Geist Mono source or its OFL license is unavailable in third_party/geist-font.')
    if MONO_DESTINATION.exists() and any(MONO_DESTINATION.iterdir()) and not replace:
        raise SystemExit(f'{MONO_DESTINATION} already exists. Use --replace after preserving the review source.')

    staging = ROOT / '.build' / 'geist-mono-ufo-import'
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    previous_cwd = Path.cwd()
    try:
        os.chdir(GEIST_MONO_SOURCE.parent)
        glyphsLib.build_masters(
            _load_without_backgrounds(GEIST_MONO_SOURCE),
            master_dir=staging,
            designspace_path=staging / 'GeistMono.designspace',
            minimal=True,
            store_editor_state=False,
            expand_includes=True,
        )
    finally:
        os.chdir(previous_cwd)

    document = DesignSpaceDocument.fromfile(staging / 'GeistMono.designspace')
    filename_map: dict[str, str] = {}
    for source in document.sources:
        original = Path(source.filename).name
        style = {'GeistMono-Thin.ufo': 'Thin', 'GeistMono-Regular.ufo': 'Regular', 'GeistMono-UltraBlack.ufo': 'Black'}[original]
        destination_name = f'{MONO_PREFIX}-{style}.ufo'
        filename_map[original] = destination_name
        source.filename = destination_name
        source.path = str(staging / destination_name)
        source.name = f'Asbir Mono {style}'
        source.familyName = 'Asbir Mono'
        source.styleName = style
        ufo_path = staging / original
        ufo = Font.open(ufo_path)
        ufo.info.familyName = 'Asbir Mono'
        ufo.info.styleName = style
        ufo.info.postscriptFontName = f'{MONO_PREFIX}-{style}'
        ufo.info.openTypeNamePreferredFamilyName = 'Asbir Mono'
        ufo.info.openTypeNamePreferredSubfamilyName = style
        ufo.info.openTypeNameCompatibleFullName = f'Asbir Mono {style}'
        ufo.info.openTypeNameVersion = 'Version 0.100; derived from Geist Mono'
        ufo.lib['com.asbir.foundation'] = 'Geist Mono source, SIL OFL 1.1'
        ufo.save(ufo_path, overwrite=True)
    for instance in document.instances:
        instance.name = f'Asbir Mono {instance.styleName}'
        instance.familyName = 'Asbir Mono'
        instance.filename = f'{MONO_PREFIX}-{instance.styleName}.ufo'
        instance.postScriptFontName = f'{MONO_PREFIX}-{instance.styleName}'
    for original, destination_name in filename_map.items():
        (staging / original).rename(staging / destination_name)
    document.write(staging / f'{MONO_PREFIX}.designspace')
    (staging / 'GeistMono.designspace').unlink()

    archive = ROOT / 'sources' / 'archive' / 'procedural-asbir-mono-review'
    if MONO_DESTINATION.exists():
        if (MONO_DESTINATION / f'{MONO_PREFIX}-Regular.ufo').exists():
            current = Font.open(MONO_DESTINATION / f'{MONO_PREFIX}-Regular.ufo')
            # An already imported authored foundation can be re-imported from
            # its tracked upstream source. Preserve only the original
            # procedural masters, which cannot be reconstructed.
            if current.lib.get('com.asbir.foundation'):
                shutil.rmtree(MONO_DESTINATION)
            else:
                if archive.exists():
                    raise SystemExit(f'Procedural archive already exists: {archive}')
                archive.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(MONO_DESTINATION), archive)
        else:
            shutil.rmtree(MONO_DESTINATION)
    shutil.move(str(staging), MONO_DESTINATION)
    # Recreate the concise distribution notice from the foundations actually
    # shipped. This also prevents a previously evaluated, but unused, source
    # from appearing as a claim about the released Mono binaries.
    notices = ROOT / 'THIRD_PARTY_NOTICES.md'
    notices.write_text(
        '# Asbir Font Foundations\n\n'
        '## Asbir Sans\n\n'
        'Asbir Sans is derived from Inter Roman source by The Inter Project Authors. '
        'The source foundation and all derivative font software are licensed under the '
        'SIL Open Font License, Version 1.1. The upstream copyright notice and full '
        'license are reproduced below.\n\n---\n\n' + INTER_LICENSE.read_text().strip() +
        '\n\n---\n\n## Asbir Mono\n\n'
        'Asbir Mono is derived from Geist Mono source by The Geist Project Authors. '
        'The source foundation and all derivative font software are licensed under the '
        'SIL Open Font License, Version 1.1. The upstream copyright notice and full '
        'license are reproduced below.\n\n---\n\n' + GEIST_MONO_LICENSE.read_text().strip() + '\n'
    )
    print(f'Imported three editable Geist Mono masters into {MONO_DESTINATION}')
    print(f'Archived procedural review masters at {archive}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('sans', 'mono'), default='sans')
    parser.add_argument('--replace', action='store_true', help='Archive the current procedural source and replace it.')
    args = parser.parse_args()
    if args.family == 'sans':
        import_sans(args.replace)
    else:
        import_mono(args.replace)


if __name__ == '__main__':
    main()
