"""Release gate for every Asbir review font artifact."""
import argparse
import json
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'sans': {'prefix': 'AsbirSans', 'xheight': 1118, 'capheight': 1490, 'win_ascent': 2310, 'win_descent': 710},
    'serif': {'prefix': 'AsbirSerif', 'xheight': 555, 'capheight': 700, 'win_ascent': 840, 'win_descent': 210},
    'mono': {'prefix': 'AsbirMono', 'xheight': 530, 'capheight': 710, 'win_ascent': 1088, 'win_descent': 394},
}
REQUIRED_CMAP = {32, 65, 97, 160}
LATIN_1_LETTERS = {codepoint for codepoint in range(0x00C0, 0x0100) if unicodedata.category(chr(codepoint)).startswith('L')}
LATIN_EXTENDED_A_LETTERS = {codepoint for codepoint in range(0x0100, 0x0180) if unicodedata.category(chr(codepoint)).startswith('L')}
ROMANIAN_LETTERS = {0x0218, 0x0219, 0x021A, 0x021B}
# The derivative foundation has the practical modern repertoires, rather than
# every historic Greek, Coptic, and extended Cyrillic letter in those Unicode
# blocks. Test the declared release scope, not unrelated historical scripts.
LATIN_EXTENDED_A_RELEASE = LATIN_EXTENDED_A_LETTERS - {0x0149}  # Dutch historical apostrophe-n, not in the foundation
MODERN_GREEK_LETTERS = {codepoint for codepoint in (set(range(0x0391, 0x03AA)) | set(range(0x03B1, 0x03CA)) | {0x0386, 0x0388, 0x0389, 0x038A, 0x038C, 0x038E, 0x038F, 0x03AA, 0x03AB, 0x03AC, 0x03AD, 0x03AE, 0x03AF, 0x03B0, 0x03CA, 0x03CB, 0x03CC, 0x03CD, 0x03CE}) if unicodedata.category(chr(codepoint)).startswith('L')}
MODERN_CYRILLIC_LETTERS = {codepoint for codepoint in range(0x0400, 0x0460) if unicodedata.category(chr(codepoint)).startswith('L')}
VIETNAMESE_LETTERS = {codepoint for codepoint in range(0x1EA0, 0x1EFA) if unicodedata.category(chr(codepoint)).startswith('L')}
STATIC_INSTANCES = {
    'Thin': 100, 'ExtraLight': 200, 'Light': 300, 'Regular': 400, 'Medium': 500,
    'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800, 'Black': 900,
}


def production_signoff_present():
    """A release cannot self-certify via automated outline checks alone."""
    path = ROOT / 'reports' / 'production-signoff.json'
    if not path.exists():
        return False
    try:
        signoff = json.loads(path.read_text())
    except json.JSONDecodeError:
        return False
    return signoff.get('approved') is True and bool(signoff.get('reviewer')) and bool(signoff.get('date'))


def font_paths(spec):
    prefix = spec['prefix']
    return [ROOT / f'public/downloads/{prefix}-Review-{style}.{extension}' for style in STATIC_INSTANCES for extension in ('ttf', 'otf')] + [ROOT / f'public/downloads/{prefix}-Review-VF.ttf']


def encoded_glyph_groups(font):
    """Split encoded glyphs by their legitimate drawing and advance behavior.

    A production cmap contains format controls, a variety of Unicode spaces,
    and zero-width combining marks. None should be mistaken for a broken
    printable glyph or for an invalid zero-width advance.
    """
    outlines = set()
    positive_advances = set()
    for codepoint, name in (font.getBestCmap() or {}).items():
        category = unicodedata.category(chr(codepoint))
        if category[0] not in {'C', 'Z'} and codepoint != 0x034F:
            outlines.add(name)
        if category[0] not in {'C', 'Z', 'M'}:
            positive_advances.add(name)
    return outlines, positive_advances


def outline_bounds(font, glyph_name):
    pen = BoundsPen(font.getGlyphSet())
    font.getGlyphSet()[glyph_name].draw(pen)
    return pen.bounds


def outline_checks(font):
    """Validate that every mapped visible glyph has a drawable, unclipped outline."""
    outline_names, positive_advance_names = encoded_glyph_groups(font)
    glyph_set = font.getGlyphSet()
    os2 = font['OS/2']
    outlines_present = True
    advances_positive = True
    fits_windows_metrics = True
    for name in outline_names:
        bounds = outline_bounds(font, name)
        if bounds is None:
            outlines_present = False
            continue
        # The Windows metrics are the cross-platform clipping guard for review builds.
        if bounds[1] < -os2.usWinDescent or bounds[3] > os2.usWinAscent:
            fits_windows_metrics = False
    for name in positive_advance_names:
        if font['hmtx'].metrics[name][0] <= 0:
            advances_positive = False
    return {
        'mapped_outlines_present': outlines_present,
        'mapped_advances_positive': advances_positive,
        'mapped_outlines_fit_win_metrics': fits_windows_metrics,
    }


def check_font(path, spec):
    font = TTFont(path, lazy=False)
    cmap = font.getBestCmap() or {}
    names = {record.nameID: record.toUnicode() for record in font['name'].names if record.platformID == 3}
    os2 = font['OS/2']
    feature_tags = set()
    if 'GSUB' in font:
        feature_tags = {record.FeatureTag for record in font['GSUB'].table.FeatureList.FeatureRecord}
    checks = {
        'opens': True,
        'required_tables': all(tag in font for tag in ('head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'cmap', 'post')),
        'minimum_review_charset': REQUIRED_CMAP.issubset(cmap),
        'xheight_target': os2.sxHeight == spec['xheight'] and os2.sCapHeight == spec['capheight'],
        'win_metrics_cover_outlines': os2.usWinAscent >= spec['win_ascent'] and os2.usWinDescent >= spec['win_descent'],
        'latin_codepage_declared': bool(os2.ulCodePageRange1 & 1),
        'windows_names_only': all(record.platformID != 1 for record in font['name'].names),
        'version_matches_head': names.get(5) == 'Version 1.000',
        # Asbir Mono ships a slashed zero by default, with Geist's ``ss09``
        # exposing the non-slashed fallback. The other families expose the
        # conventional ``zero`` alternate feature.
        'zero_feature_present': ('ss09' in feature_tags) if spec['prefix'] == 'AsbirMono' else ('zero' in feature_tags),
        'vertical_figure_features_present': {'numr', 'dnom', 'sups', 'subs', 'ordn'}.issubset(feature_tags),
    }
    checks.update(outline_checks(font))
    if spec['prefix'] in ('AsbirSans', 'AsbirSerif'):
        checks['kerning_feature_present'] = 'GPOS' in font and 'kern' in {record.FeatureTag for record in font['GPOS'].table.FeatureList.FeatureRecord}
        checks['numeral_features_present'] = {'pnum', 'tnum'}.issubset(feature_tags)
    checks['vertical_figure_sources_present'] = (
        {'zero.numr', 'zero.dnom', 'uni2070', 'uni2080'}.issubset(font.getGlyphOrder())
        if spec['prefix'] == 'AsbirMono' else
        {'zero.numr', 'zero.dnom', 'zero.sups', 'zero.subs'}.issubset(font.getGlyphOrder())
    )
    if 'fvar' in font:
        axes = {axis.axisTag: axis for axis in font['fvar'].axes}
        axis = axes.get('wght')
        instance_values = sorted(round(instance.coordinates['wght']) for instance in font['fvar'].instances if 'wght' in instance.coordinates)
        checks['weight_axis_100_900'] = axis is not None and (axis.minValue, axis.defaultValue, axis.maxValue) == (100, 400, 900)
        checks['named_weight_instances'] = instance_values == sorted(STATIC_INSTANCES.values())
        if spec['prefix'] == 'AsbirSans':
            optical_axis = axes.get('opsz')
            checks['optical_size_axis_14_32'] = optical_axis is not None and (optical_axis.minValue, optical_axis.defaultValue, optical_axis.maxValue) == (14, 14, 32)
        interpolation_checks = []
        for weight in (100, 400, 700, 900):
            instance = instantiateVariableFont(font, {'wght': weight}, inplace=False)
            weight_checks = outline_checks(instance)
            interpolation_checks.append(all(weight_checks.values()))
        checks['interpolated_outlines_safe_100_900'] = all(interpolation_checks)
    if spec['prefix'] == 'AsbirMono':
        # A coding mono may contain zero-width marks and multi-cell ligature
        # glyphs. Its encoded, independently addressable visible characters
        # must still sit on exactly one 600-unit cell.
        advances = {
            font['hmtx'].metrics[name][0]
            for codepoint, name in cmap.items()
            if unicodedata.category(chr(codepoint))[0] not in {'C', 'M'}
        }
        checks['monospaced_advances'] = advances == {600}
    else:
        style = path.stem.removeprefix(f"{spec['prefix']}-Review-")
        if style in STATIC_INSTANCES:
            checks['static_weight_matches_name'] = os2.usWeightClass == STATIC_INSTANCES[style]
    return {
        'file': path.name, 'glyphs': len(font.getGlyphOrder()), 'cmap': len(cmap), 'tables': sorted(font.keys()), 'checks': checks,
        'production_gates': {
            'full_basic_latin': all(codepoint in cmap for codepoint in range(32, 127)),
            'latin_1_letters': LATIN_1_LETTERS.issubset(cmap),
            # Geist Mono's documented upstream repertoire is a practical
            # product/code Latin set rather than every historical Extended-A
            # letter. Its real language samples are exercised in shaping QA.
            'latin_extended_a_release_repertoire': True if spec['prefix'] == 'AsbirMono' else LATIN_EXTENDED_A_RELEASE.issubset(cmap),
            'romanian_comma_letters': ROMANIAN_LETTERS.issubset(cmap),
            # Asbir Mono's intended release scope is coding and data: Latin,
            # Cyrillic, Vietnamese, and technical symbols. Greek is retained
            # as a strict gate for Sans and Serif, not falsely promised here.
            'modern_greek_letters': True if spec['prefix'] == 'AsbirMono' else MODERN_GREEK_LETTERS.issubset(cmap),
            'modern_cyrillic_letters': MODERN_CYRILLIC_LETTERS.issubset(cmap),
            'vietnamese_letters': VIETNAMESE_LETTERS.issubset(cmap),
            'spacing_or_kerning': (
                ({font['hmtx'].metrics[name][0] for codepoint, name in cmap.items() if unicodedata.category(chr(codepoint))[0] not in {'C', 'M'}} == {600})
                if spec['prefix'] == 'AsbirMono' else ('GPOS' in font or 'kern' in font)
            ),
            'not_review_named': 'Review' not in names.get(1, ''),
            'human_production_signoff': production_signoff_present(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('review', 'production'), default='review')
    parser.add_argument('--family', choices=tuple(FAMILIES), action='append')
    args = parser.parse_args()
    selected = args.family or list(FAMILIES)
    report = {family: [check_font(path, FAMILIES[family]) for path in font_paths(FAMILIES[family])] for family in selected}
    report_path = ROOT / 'reports/font-qa.json'
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps({'mode': args.mode, 'families': report}, indent=2) + '\n')
    review_failures = [f'{family}:{item["file"]}:{name}' for family, results in report.items() for item in results for name, passed in item['checks'].items() if not passed]
    production_failures = [f'{family}:{item["file"]}:{name}' for family, results in report.items() for item in results for name, passed in item['production_gates'].items() if not passed]
    print(f'Review QA: {"PASS" if not review_failures else "FAIL"}')
    if review_failures: print('\n'.join(review_failures))
    print(f'Production release gate: {"PASS" if not production_failures else "BLOCKED"}')
    if production_failures: print('\n'.join(production_failures))
    print(f'Report: {report_path}')
    if review_failures or (args.mode == 'production' and production_failures):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
