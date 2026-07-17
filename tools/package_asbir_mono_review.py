"""Package the complete Asbir Mono review family and terminal companion."""
from pathlib import Path
from shutil import copy2, rmtree
from zipfile import ZIP_DEFLATED, ZipFile

try:
    from release_version import RELEASE_VERSION
except ModuleNotFoundError:
    from tools.release_version import RELEASE_VERSION

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public' / 'downloads'
VERSION = RELEASE_VERSION
PACKAGE_NAME = f'AsbirMono-Review-{VERSION}'
TARGET = ROOT / 'release' / PACKAGE_NAME
ARCHIVE = ROOT / 'release' / f'{PACKAGE_NAME}.zip'
DOWNLOAD = SOURCE / f'{PACKAGE_NAME}.zip'
WEIGHTS = ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')


def copy_font(source_name, folder, release_name):
    source = SOURCE / source_name
    if not source.exists():
        raise SystemExit(f'Missing review binary: {source}')
    destination = TARGET / 'fonts' / folder / release_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)


def make_archive():
    with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED) as archive:
        for file in sorted(TARGET.rglob('*')):
            if file.is_file():
                archive.write(file, file.relative_to(TARGET.parent))
    copy2(ARCHIVE, DOWNLOAD)


def main():
    if TARGET.exists():
        rmtree(TARGET)
    TARGET.mkdir(parents=True)
    for weight in WEIGHTS:
        copy_font(f'AsbirMono-Review-{weight}.ttf', 'ttf', f'AsbirMono-{weight}.ttf')
        copy_font(f'AsbirMono-Review-{weight}.otf', 'otf', f'AsbirMono-{weight}.otf')
    copy_font('AsbirMono-Review-VF.ttf', 'variable', 'AsbirMono-Variable.ttf')
    copy_font('AsbirMono-NerdFont-Review-Regular.ttf', 'terminal', 'AsbirMono-NerdFont-Regular.ttf')
    copy2(ROOT / 'THIRD_PARTY_NOTICES.md', TARGET / 'THIRD_PARTY_NOTICES.md')
    copy2(ROOT / 'FONTBAKERY_WAIVERS.md', TARGET / 'FONTBAKERY_WAIVERS.md')
    copy2(ROOT / 'reports' / 'nerd-font-qa.json', TARGET / 'NERD_FONT_QA.json')
    (TARGET / 'README.md').write_text(
        f'# Asbir Mono Review {VERSION}\n\n'
        'This is the complete **review** package for Asbir Mono. It is not an '
        'approved production release. The core family includes nine static weights '
        'in TTF and CFF OTF plus a `wght` 100–900 variable TTF.\n\n'
        'The coding ligatures `->`, `=>`, `!=`, `==`, `===`, `<=`, and `>=` are '
        'enabled by default through `liga`; disable standard ligatures to show '
        'literal ASCII operators. The core font also includes `⇐`, `⇒`, and `⇔`.\n\n'
        '`fonts/terminal/AsbirMono-NerdFont-Regular.ttf` is a separately named, '
        'fixed-cell Regular terminal font with Nerd Font / Powerline symbols. '
        'Use it for terminals and developer tooling, not as a substitute for the '
        'core variable family.\n\n'
        'License and third-party attribution: `THIRD_PARTY_NOTICES.md`. '\
        'Review-check notes: `FONTBAKERY_WAIVERS.md` and `NERD_FONT_QA.json`.\n'
    )
    make_archive()
    print(f'Packaged {PACKAGE_NAME}: {ARCHIVE}')
    print(f'Web download: {DOWNLOAD}')


if __name__ == '__main__':
    main()
