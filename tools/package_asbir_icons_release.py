#!/usr/bin/env python3
"""Build a deterministic, source-only Asbir Icons release archive."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
CATALOG_PATH = ROOT / 'src' / 'icons' / 'catalog.json'
SOURCE_ASSETS = ROOT / 'public' / 'icons'
RELEASE_ROOT = ROOT / 'release'
MIT_LICENSE = """MIT License

Copyright (c) 2026 Asbir Tech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack', default='soft', choices=('soft',))
    parser.add_argument('--version', default='1.0.0')
    return parser.parse_args()


def read_catalog(pack: str, version: str) -> dict:
    catalog = json.loads(CATALOG_PATH.read_text())
    selected = [item for item in catalog['packs'] if item['id'] == pack]
    if not selected:
        raise SystemExit(f'Unknown pack: {pack}')
    if catalog['version'] != version or selected[0]['version'] != version:
        raise SystemExit(
            f'Catalog version mismatch: requested {version}, found {catalog["version"]}'
        )
    if any(icon['pack'] != pack for icon in catalog['icons']):
        raise SystemExit('The release pack must contain only its selected pack records')
    return catalog


def write_release_files(target: Path, catalog: dict, pack: str, version: str) -> None:
    target.mkdir(parents=True)
    asset_source = SOURCE_ASSETS / pack
    asset_target = target / 'icons' / pack
    if not asset_source.is_dir():
        raise SystemExit(f'Missing generated assets: {asset_source}')
    shutil.copytree(asset_source, asset_target)

    (target / 'manifest.json').write_text(json.dumps(catalog, indent=2) + '\n')
    (target / 'LICENSE').write_text(MIT_LICENSE)
    (target / 'README.md').write_text(
        f'''# Asbir Icons — {catalog['packs'][0]['name']} {version}

Asbir Icons is an original, soft-rounded SVG icon pack for general web and product UI. This release contains {len(catalog['icons'])} semantic icons, each with matched `outline` and `filled` variants.

## Contents

- `icons/{pack}/<slug>/outline.svg` — canonical outline artwork.
- `icons/{pack}/<slug>/filled.svg` — canonical filled artwork.
- `manifest.json` — names, categories, aliases, keywords, relationships, and asset paths.
- `LICENSE` — MIT license for the icon artwork and metadata.
- `CHANGELOG.md` — release history.

## Usage

Use an SVG directly in HTML:

```html
<img src="icons/{pack}/search/outline.svg" alt="Search">
```

Or inline the SVG when you want to control its color with CSS. The canonical files use `currentColor`, a `24 24` viewBox, and rounded construction. Preserve the `viewBox` when resizing.

Stable names use lowercase kebab-case slugs. Search the manifest for aliases and keywords when mapping product concepts to icons. Outline and filled are semantic variants of the same icon; choose one consistently within a UI surface.

## License

The icons and metadata in this archive are released under the MIT License. See `LICENSE` for the full text.
'''
    )
    (target / 'CHANGELOG.md').write_text(
        f'''# Changelog

## {version} — 2026-07-20

- Initial Asbir Icons Soft pack release.
- Added {len(catalog['icons'])} semantic web and product UI icons.
- Added outline and filled SVG variants for every icon.
- Added manifest metadata, related-icon references, and contextual usage labels.
'''
    )


def write_deterministic_zip(source: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in sorted(source.rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(source.parent).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 7, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, path.read_bytes())


def main() -> None:
    args = parse_args()
    catalog = read_catalog(args.pack, args.version)
    folder = RELEASE_ROOT / f'AsbirIcons-{catalog["packs"][0]["name"]}-{args.version}'
    archive = folder.parent / f'{folder.name}.zip'
    if folder.exists():
        shutil.rmtree(folder)
    write_release_files(folder, catalog, args.pack, args.version)
    write_deterministic_zip(folder, archive)
    print(f'Packaged Asbir Icons {catalog["packs"][0]["name"]} {args.version}: {len(catalog["icons"])} icons')
    print(f'  {folder.relative_to(ROOT)}')
    print(f'  {archive.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
