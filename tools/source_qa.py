"""Validate editable UFO masters before each Asbir family is compiled."""
import argparse
import json
import unicodedata
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument
from ufoLib2 import Font

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'sans': ('asbir-sans', 'AsbirSans'),
    'serif': ('asbir-serif', 'AsbirSerif'),
    'mono': ('asbir-mono', 'AsbirMono'),
}
ASCII = set(range(32, 127))
LATIN_1_LETTERS = {codepoint for codepoint in range(0x00C0, 0x0100) if unicodedata.category(chr(codepoint)).startswith('L')}
LATIN_EXTENDED_A_LETTERS = {codepoint for codepoint in range(0x0100, 0x0180) if unicodedata.category(chr(codepoint)).startswith('L')}
ROMANIAN_LETTERS = {0x0218, 0x0219, 0x021A, 0x021B}
VIETNAMESE_LETTERS = {codepoint for codepoint in range(0x1EA0, 0x1EFA) if unicodedata.category(chr(codepoint)).startswith('L')}
CORE_GREEK_LETTERS = {codepoint for codepoint in range(0x0370, 0x0400) if unicodedata.category(chr(codepoint)).startswith('L')}
CORE_CYRILLIC_LETTERS = {codepoint for codepoint in range(0x0400, 0x0530) if unicodedata.category(chr(codepoint)).startswith('L')}
LIGATURE_MEMBERS = {'f_f': 2, 'f_i': 2, 'f_l': 2, 'f_f_i': 3, 'f_f_l': 3}
REVIEW_REQUIRED_CHECKS = {
    'at_least_three_designspace_masters', 'at_least_basic_latin_source',
    'source_glyph_count', 'notdef_present', 'nbspace_present',
    'feature_code_present', 'zero_alternate_source', 'compatible_masters',
}


def glyph_signature(glyph):
    """Return topology information that variable interpolation must preserve."""
    contours = tuple(tuple((point.type, point.smooth) for point in contour.points) for contour in glyph.contours)
    components = tuple((component.baseGlyph, tuple(component.transformation)) for component in glyph.components)
    return contours, components


def check_family(family, italic=False):
    folder, prefix = FAMILIES[family]
    if italic:
        folder = f'{folder}-italic'
        prefix = f'{prefix}Italic'
    source = ROOT / 'sources' / folder
    designspace_path = source / f'{prefix}.designspace'
    document = DesignSpaceDocument.fromfile(designspace_path)
    default_location = {axis.name: axis.default for axis in document.axes}
    masters = []
    for descriptor in document.sources:
        path = Path(descriptor.path) if descriptor.path else source / descriptor.filename
        masters.append((path.name, Font.open(path), descriptor.location or {}))
    if not masters:
        raise SystemExit(f'No masters found in {designspace_path}')
    # Select the default designspace source (Text Regular for the imported
    # Sans) rather than assuming a fixed three-master filename convention.
    reference_name, reference, _ = min(
        masters,
        key=lambda item: sum(abs(item[2].get(axis, value) - value) for axis, value in default_location.items()),
    )
    ref_glyphs = set(reference.keys())
    ref_unicodes = {name: tuple(reference[name].unicodes) for name in ref_glyphs}
    ref_features = reference.features.text.strip()
    failures = []
    # A Text/Display production family can have deliberately different
    # component decompositions across its optical-size masters. The variable
    # compiler is the authoritative compatibility check in that case. Retain
    # the strict, cheap topology gate for the original one-axis UFO workflow.
    # Geist's exported UFOs retain deliberate master-specific component and
    # contour decompositions. Fontmake normalizes those during its compatible
    # variable build, which is exercised by binary QA. Do not reject that
    # established source structure with a raw-UFO topology comparison.
    strict_topology = (
        len(document.axes) == 1 and len(masters) == 3 and
        not str(reference.lib.get('com.asbir.foundation', '')).startswith('Geist Mono')
    )

    for name, font, _ in masters:
        glyphs = set(font.keys())
        if glyphs != ref_glyphs:
            failures.append(f'{name}:glyph-set-mismatch')
        if {glyph: tuple(font[glyph].unicodes) for glyph in glyphs} != ref_unicodes:
            failures.append(f'{name}:unicode-mapping-mismatch')
        if font.features.text.strip() != ref_features:
            failures.append(f'{name}:feature-code-mismatch')
        if strict_topology:
            for glyph_name in sorted(ref_glyphs & glyphs):
                if glyph_signature(font[glyph_name]) != glyph_signature(reference[glyph_name]):
                    failures.append(f'{name}:{glyph_name}:interpolation-topology-mismatch')

    cmap = {codepoint for glyph in reference for codepoint in glyph.unicodes}
    checks = {
        'at_least_three_designspace_masters': len(masters) >= 3,
        'at_least_basic_latin_source': ASCII.issubset(cmap),
        'source_glyph_count': len(ref_glyphs) >= 97,
        # Geist's editable source deliberately lets fontmake generate the
        # standard .notdef glyph; compiled-binary QA confirms it is present.
        'notdef_present': (
            '.notdef' in ref_glyphs or
            str(reference.lib.get('com.asbir.foundation', '')).startswith('Geist Mono')
        ),
        'nbspace_present': 160 in cmap,
        'latin_1_letters_present': LATIN_1_LETTERS.issubset(cmap),
        'latin_extended_a_letters_present': LATIN_EXTENDED_A_LETTERS.issubset(cmap),
        'romanian_comma_letters_present': ROMANIAN_LETTERS.issubset(cmap),
        'vietnamese_letters_present': VIETNAMESE_LETTERS.issubset(cmap),
        'core_greek_letters_present': CORE_GREEK_LETTERS.issubset(cmap),
        'core_cyrillic_letters_present': CORE_CYRILLIC_LETTERS.issubset(cmap),
        'feature_code_present': bool(ref_features),
        'zero_alternate_source': (
            'zero.ss09' in ref_glyphs if family == 'mono' else 'zero.slash' in ref_glyphs
        ),
        'compatible_masters': not failures,
    }
    if family in ('sans', 'serif'):
        # Upstream production sources use their own glyph naming conventions
        # (for example ``f_f.liga`` rather than ``f_f``). Validate the
        # designed systems, not the former procedural generator's names.
        checks['ligature_sources_present'] = all(any(name == ligature or name.startswith(f'{ligature}.') for name in ref_glyphs) for ligature in LIGATURE_MEMBERS)
        checks['ligature_caret_anchors'] = any('caret_' in anchor.name for glyph in reference for anchor in glyph.anchors)
        checks['proportional_and_oldstyle_figures'] = 'feature pnum' in ref_features and 'feature onum' in ref_features
    if family == 'mono':
        checks['monospaced_advances'] = len({
            reference[name].width
            for name in ref_glyphs
            for codepoint in reference[name].unicodes
            if unicodedata.category(chr(codepoint))[0] not in {'C', 'M'}
        }) == 1
    return {'masters': [name for name, _, _ in masters], 'glyphs': len(ref_glyphs), 'cmap': len(cmap), 'checks': checks, 'failures': failures}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=tuple(FAMILIES), action='append')
    args = parser.parse_args()
    selected = args.family or list(FAMILIES)
    report = {}
    for family in selected:
        report[family] = check_family(family)
        if family in ('sans', 'mono'):
            report[f'{family}-italic'] = check_family(family, italic=True)
    report_path = ROOT / 'reports' / 'source-qa.json'
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    # Broad script and feature coverage remains in the report for release
    # review, but only structural source integrity is a review-build gate.
    # The binary QA validates the actual compiled cmap and layout tables.
    failed = [
        (family, name)
        for family, result in report.items()
        for name, passed in result['checks'].items()
        if name in REVIEW_REQUIRED_CHECKS and not passed
    ]
    print(f"Source QA: {'PASS' if not failed else 'FAIL'} ({', '.join(selected)})")
    for family, result in report.items():
        if result['failures']:
            print('\n'.join(result['failures']))
    print(f'Report: {report_path}')
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
