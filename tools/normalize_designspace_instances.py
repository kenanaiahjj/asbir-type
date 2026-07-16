"""Keep named Designspace instances in increasing axis order.

FontBakery treats out-of-order variable-font instances as a release failure.
"""
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument

ROOT = Path(__file__).resolve().parents[1]
DESIGNSPACES = (
    ROOT / 'sources' / 'asbir-sans' / 'AsbirSans.designspace',
    ROOT / 'sources' / 'asbir-serif' / 'AsbirSerif.designspace',
    ROOT / 'sources' / 'asbir-mono' / 'AsbirMono.designspace',
)


def main():
    for path in DESIGNSPACES:
        document = DesignSpaceDocument.fromfile(path)
        document.instances.sort(key=lambda instance: instance.location.get('Weight', 400))
        document.write(path)
        print(f'Normalized {path.name}')


if __name__ == '__main__':
    main()
