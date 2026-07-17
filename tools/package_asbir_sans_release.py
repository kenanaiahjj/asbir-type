"""Package the approved Asbir Sans release without disturbing proof assets."""
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
TARGET = ROOT / 'release' / f'AsbirSans-{VERSION}'
ARCHIVE = SOURCE / f'AsbirSans-{VERSION}.zip'
NOTICES = ROOT / 'THIRD_PARTY_NOTICES.md'
WEIGHTS = ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')


def copy_font(source_name, folder, release_name):
    source = SOURCE / source_name
    if not source.exists():
        raise SystemExit(f'Missing approved binary: {source}')
    destination = TARGET / folder / release_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)


def main():
    if TARGET.exists():
        rmtree(TARGET)
    for weight in WEIGHTS:
        copy_font(f'AsbirSans-Review-{weight}.ttf', 'TTF', f'AsbirSans-{weight}.ttf')
        copy_font(f'AsbirSans-Review-{weight}.otf', 'OTF', f'AsbirSans-{weight}.otf')
    copy_font('AsbirSans-Review-VF.ttf', 'Variable', 'AsbirSans-Variable.ttf')
    italic_variable = SOURCE / 'AsbirSans-Review-Italic-VF.ttf'
    if italic_variable.exists():
        for weight in WEIGHTS:
            copy_font(f'AsbirSans-Review-Italic-{weight}.ttf', 'Italic', f'AsbirSans-Italic-{weight}.ttf')
            copy_font(f'AsbirSans-Review-Italic-{weight}.otf', 'Italic', f'AsbirSans-Italic-{weight}.otf')
        copy_font('AsbirSans-Review-Italic-VF.ttf', 'Italic', 'AsbirSans-Italic-Variable.ttf')
    web_source = SOURCE / 'web' / 'AsbirSans'
    if web_source.exists():
        for path in sorted(web_source.iterdir()):
            if path.is_file():
                destination = TARGET / 'web' / 'AsbirSans' / path.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                copy2(path, destination)
    copy2(NOTICES, TARGET / 'THIRD_PARTY_NOTICES.md')
    (TARGET / 'README.md').write_text(
        f'# Asbir Sans {VERSION}\n\n'
        'Approved production release. Includes nine static Roman and true italic weights '
        'in TTF and CFF OTF, plus separate Roman and italic variable TTFs. The Sans '
        'variable files expose `wght` (100–900) and `opsz` (14–32) axes.\n\n'
        'Install the static fonts for fixed-weight environments, or use '
        '`Variable/AsbirSans-Variable.ttf` or `Italic/AsbirSans-Italic-Variable.ttf` '
        'in variable-font-capable software. The `web/AsbirSans/` folder contains the '
        'WOFF2 and CSS loading kit.\n\n'
        'License and derivative attribution are in `THIRD_PARTY_NOTICES.md`.\n'
    )
    with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(TARGET.rglob('*')):
            if path.is_file():
                archive.write(path, path.relative_to(TARGET.parent).as_posix())
    print(f'Packaged Asbir Sans {VERSION}: {TARGET}')
    print(f'Web download: {ARCHIVE}')


if __name__ == '__main__':
    main()
