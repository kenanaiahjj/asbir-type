"""Package the approved Asbir Sans release without disturbing proof assets."""
from pathlib import Path
from shutil import copy2, rmtree
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public' / 'downloads'
VERSION = '1.0.0'
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
    copy2(NOTICES, TARGET / 'THIRD_PARTY_NOTICES.md')
    (TARGET / 'README.md').write_text(
        '# Asbir Sans 1.0.0\n\n'
        'Approved production release. Includes nine static weights in TTF and CFF OTF, '
        'plus a variable TTF with `wght` (100–900) and `opsz` (14–32) axes.\n\n'
        'Install the static fonts for fixed-weight environments, or use '
        '`Variable/AsbirSans-Variable.ttf` in variable-font-capable software.\n\n'
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
