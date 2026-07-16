"""Build self-contained WOFF2 and CSS loading kits for the two web families."""
from pathlib import Path
from shutil import rmtree

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public' / 'downloads'
WEB = SOURCE / 'web'

FAMILIES = {
    'AsbirSans': {'family': 'Asbir Sans', 'folder': 'AsbirSans', 'opsz': True},
    'AsbirMono': {'family': 'Asbir Mono', 'folder': 'AsbirMono', 'opsz': False},
}


def convert(source_name, destination):
    source = SOURCE / source_name
    if not source.exists():
        raise SystemExit(f'Missing font for web kit: {source}')
    font = TTFont(source, lazy=False)
    font.flavor = 'woff2'
    destination.parent.mkdir(parents=True, exist_ok=True)
    font.save(destination)


def css_for(spec):
    family = spec['family']
    prefix = spec['folder']
    optical = '  font-optical-sizing: auto;\n' if spec['opsz'] else ''
    return (
        '/* Asbir web loading kit. Self-host these files beside this stylesheet. */\n'
        '@font-face {\n'
        f"  font-family: '{family}';\n"
        f"  src: url('./{prefix}-Variable.woff2') format('woff2');\n"
        '  font-style: normal;\n'
        '  font-weight: 100 900;\n'
        '  font-display: swap;\n'
        f'{optical}'
        '}\n\n'
        '@font-face {\n'
        f"  font-family: '{family}';\n"
        f"  src: url('./{prefix}-Italic-Variable.woff2') format('woff2');\n"
        '  font-style: italic;\n'
        '  font-weight: 100 900;\n'
        '  font-display: swap;\n'
        f'{optical}'
        '}\n\n'
        '@font-face {\n'
        f"  font-family: '{family}';\n"
        f"  src: url('./{prefix}-Regular.woff2') format('woff2');\n"
        '  font-style: normal;\n'
        '  font-weight: 400;\n'
        '  font-display: swap;\n'
        '}\n\n'
        '@font-face {\n'
        f"  font-family: '{family}';\n"
        f"  src: url('./{prefix}-Italic-Regular.woff2') format('woff2');\n"
        '  font-style: italic;\n'
        '  font-weight: 400;\n'
        '  font-display: swap;\n'
        '}\n'
    )


def package_family(prefix, spec):
    target = WEB / spec['folder']
    if target.exists():
        rmtree(target)
    convert(f'{prefix}-Review-VF.ttf', target / f'{prefix}-Variable.woff2')
    convert(f'{prefix}-Review-Italic-VF.ttf', target / f'{prefix}-Italic-Variable.woff2')
    convert(f'{prefix}-Review-Regular.ttf', target / f'{prefix}-Regular.woff2')
    convert(f'{prefix}-Review-Italic-Regular.ttf', target / f'{prefix}-Italic-Regular.woff2')
    (target / f'{prefix}.css').write_text(css_for(spec))
    print(f'Packaged {spec["family"]} web kit in {target}')


def main():
    for prefix, spec in FAMILIES.items():
        package_family(prefix, spec)


if __name__ == '__main__':
    main()
