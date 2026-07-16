"""Release gate for Asbir review fonts.

Review mode verifies binary integrity, metadata and variation structure.
Production mode additionally rejects incomplete character coverage, missing
layout engineering, and review-only naming.
"""
import argparse
import json
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = [
    ROOT / 'public/downloads/AsbirSans-Review-Regular.ttf',
    ROOT / 'public/downloads/AsbirSans-Review-Regular.otf',
    ROOT / 'public/downloads/AsbirSans-Review-VF.ttf',
]
REQUIRED_CMAP = {32, 65, 97, 160}

def check_font(path):
    font = TTFont(path, lazy=False)
    cmap = font.getBestCmap() or {}
    names = {record.nameID: record.toUnicode() for record in font['name'].names if record.platformID == 3}
    os2 = font['OS/2']
    checks = {
        'opens': True,
        'required_tables': all(tag in font for tag in ('head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'cmap', 'post')),
        'minimum_review_charset': REQUIRED_CMAP.issubset(cmap),
        'xheight_target': os2.sxHeight == 555 and os2.sCapHeight == 700,
        'win_metrics_cover_outlines': os2.usWinAscent >= 700 and os2.usWinDescent >= 210,
        'latin_codepage_declared': bool(os2.ulCodePageRange1 & 1),
        'windows_names_only': all(record.platformID != 1 for record in font['name'].names),
        'version_matches_head': names.get(5) == 'Version 0.100',
    }
    if 'fvar' in font:
        axis = font['fvar'].axes[0]
        instance_values = sorted(instance.coordinates['wght'] for instance in font['fvar'].instances)
        checks['weight_axis_100_900'] = axis.axisTag == 'wght' and (axis.minValue, axis.defaultValue, axis.maxValue) == (100, 400, 900)
        checks['named_weight_instances'] = instance_values == [100, 400, 700, 900]
    return {
        'file': path.name,
        'glyphs': len(font.getGlyphOrder()),
        'cmap': len(cmap),
        'tables': sorted(font.keys()),
        'checks': checks,
        'production_gates': {
            'full_basic_latin': all(codepoint in cmap for codepoint in range(32, 127)),
            'broad_latin_minimum': len(cmap) >= 374,
            'kerning_or_gpos': 'GPOS' in font or 'kern' in font,
            'not_review_named': 'Review' not in names.get(1, ''),
        },
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('review', 'production'), default='review')
    args = parser.parse_args()
    results = [check_font(path) for path in FONTS]
    report_path = ROOT / 'reports/font-qa.json'
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps({'mode': args.mode, 'fonts': results}, indent=2) + '\n')
    review_failures = [f"{item['file']}:{name}" for item in results for name, passed in item['checks'].items() if not passed]
    production_failures = [f"{item['file']}:{name}" for item in results for name, passed in item['production_gates'].items() if not passed]
    print(f'Review QA: {"PASS" if not review_failures else "FAIL"}')
    if review_failures: print('\n'.join(review_failures))
    print(f'Production release gate: {"PASS" if not production_failures else "BLOCKED"}')
    if production_failures: print('\n'.join(production_failures))
    print(f'Report: {report_path}')
    if review_failures or (args.mode == 'production' and production_failures):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
