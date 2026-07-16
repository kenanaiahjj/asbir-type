"""Write the browser glyph manifest from the current core review binaries."""
from pathlib import Path
import json

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = {
    'sans': ROOT / 'public' / 'downloads' / 'AsbirSans-Review-Regular.ttf',
    'serif': ROOT / 'public' / 'downloads' / 'AsbirSerif-Review-Regular.ttf',
    'mono': ROOT / 'public' / 'downloads' / 'AsbirMono-Review-Regular.ttf',
}
OUTPUT = ROOT / 'src' / 'glyphs.js'


def main():
    manifest = {}
    for family, path in FONTS.items():
        if not path.exists():
            raise SystemExit(f'Missing core review font: {path}')
        manifest[family] = sorted(TTFont(path).getBestCmap())
    OUTPUT.write_text(f'export const glyphCodepoints = {json.dumps(manifest, separators=(",", ":"))};\n')
    print(f'Wrote {OUTPUT}')


if __name__ == '__main__':
    main()
