"""Package the approved Asbir Mono Roman, italic, and terminal release."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from shutil import copy2, rmtree
from zipfile import ZIP_DEFLATED, ZipFile

from fontTools.ttLib import TTFont

try:
    from release_version import RELEASE_VERSION
except ModuleNotFoundError:
    from tools.release_version import RELEASE_VERSION

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public' / 'downloads'
VERSION = RELEASE_VERSION
PACKAGE_NAME = f'AsbirMono-{VERSION}'
TARGET = ROOT / 'release' / PACKAGE_NAME
ARCHIVE = ROOT / 'release' / f'{PACKAGE_NAME}.zip'
DOWNLOAD = SOURCE / f'{PACKAGE_NAME}.zip'
WEIGHTS = ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')

_build_spec = spec_from_file_location('asbir_build_fonts', ROOT / 'tools' / 'build_fonts.py')
_build = module_from_spec(_build_spec)
_build_spec.loader.exec_module(_build)

METRICS = {
    'prefix': 'AsbirMono', 'name': 'Asbir Mono', 'xheight': 530, 'capheight': 710,
    'ascender': 800, 'descender': -150, 'win_ascent': 1088, 'win_descent': 394,
}
STATIC_INSTANCES = _build.SANS_STATIC_INSTANCES


def clean_font(source_name, folder, release_name, *, weight=400, italic=False, variable=False):
    source = SOURCE / source_name
    if not source.exists():
        raise SystemExit(f'Missing Mono binary: {source}')
    destination = TARGET / folder / release_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)
    metrics = {**METRICS, 'italic': italic}
    base_style = release_name.rsplit('.', 1)[0].removeprefix('AsbirMono-')
    if base_style.startswith('Italic-'):
        base_style = base_style.removeprefix('Italic-')
    style_name = 'Italic' if variable and italic else ('Italic ' if italic else '') + base_style
    _build.patch_common(
        destination,
        metrics,
        variable=variable,
        weight=weight,
        instances=STATIC_INSTANCES,
        style_name=style_name,
    )


def copy_web_kit():
    source = SOURCE / 'web' / 'AsbirMono'
    if not source.exists():
        raise SystemExit(f'Missing Mono web kit: {source}')
    for path in sorted(source.iterdir()):
        if path.is_file():
            destination = TARGET / 'web' / 'AsbirMono' / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(path, destination)


def make_archive():
    with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED) as archive:
        for file in sorted(TARGET.rglob('*')):
            if file.is_file():
                archive.write(file, file.relative_to(TARGET.parent).as_posix())
    copy2(ARCHIVE, DOWNLOAD)


def main():
    if TARGET.exists():
        rmtree(TARGET)
    TARGET.mkdir(parents=True)
    for weight, value in STATIC_INSTANCES:
        clean_font(f'AsbirMono-Review-{weight}.ttf', 'TTF', f'AsbirMono-{weight}.ttf', weight=value)
        clean_font(f'AsbirMono-Review-{weight}.otf', 'OTF', f'AsbirMono-{weight}.otf', weight=value)
        clean_font(f'AsbirMono-Review-Italic-{weight}.ttf', 'Italic', f'AsbirMono-Italic-{weight}.ttf', weight=value, italic=True)
        clean_font(f'AsbirMono-Review-Italic-{weight}.otf', 'Italic', f'AsbirMono-Italic-{weight}.otf', weight=value, italic=True)
    clean_font('AsbirMono-Review-VF.ttf', 'Variable', 'AsbirMono-Variable.ttf', variable=True)
    clean_font('AsbirMono-Review-Italic-VF.ttf', 'Italic', 'AsbirMono-Italic-Variable.ttf', italic=True, variable=True)
    clean_font('AsbirMono-NerdFont-Review-Regular.ttf', 'Terminal', 'AsbirMono-NerdFont-Regular.ttf', weight=400)
    copy_web_kit()
    copy2(ROOT / 'THIRD_PARTY_NOTICES.md', TARGET / 'THIRD_PARTY_NOTICES.md')
    copy2(ROOT / 'FONTBAKERY_WAIVERS.md', TARGET / 'FONTBAKERY_WAIVERS.md')
    copy2(ROOT / 'reports' / 'mono-production-signoff.json', TARGET / 'MONO_PRODUCTION_SIGNOFF.json')
    copy2(ROOT / 'reports' / 'nerd-font-qa.json', TARGET / 'NERD_FONT_QA.json')
    (TARGET / 'README.md').write_text(
        f'# Asbir Mono {VERSION}\n\n'
        'Approved production release for Asbir Mono. Includes nine Roman and true italic '
        'static weights in TTF and CFF OTF, separate `wght` 100–900 Roman and italic '
        'variable TTFs, and a fixed-cell Nerd Font terminal companion.\n\n'
        'Every encoded core glyph uses a 600-unit cell. Coding ligatures `->`, `=>`, '
        '`!=`, `==`, `===`, `<=`, and `>=` are enabled by default through `liga`; disable '
        'standard ligatures to show literal ASCII operators.\n\n'
        '`Terminal/AsbirMono-NerdFont-Regular.ttf` is intended for terminals and developer '
        'tooling. The `web/AsbirMono/` folder contains the WOFF2 and CSS loading kit.\n\n'
        'License, attribution, approval, and QA notes are included alongside this README.\n'
    )
    make_archive()
    print(f'Packaged {PACKAGE_NAME}: {ARCHIVE}')
    print(f'Web download: {DOWNLOAD}')


if __name__ == '__main__':
    main()
