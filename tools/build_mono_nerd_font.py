"""Create the separately named, fixed-cell Asbir Mono Nerd Font terminal build.

The core Asbir Mono family stays unpatched. This tool adds Nerd Fonts' public
symbol-only glyphs to the Regular TTF as direct outlines, scales every icon to
the 600-unit Mono cell, and gives the result a distinct installable family
name. Keeping this process separate avoids adding thousands of terminal PUA
glyphs to the normal product/code font.
"""
from pathlib import Path
import json

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'public' / 'downloads' / 'AsbirMono-Review-Regular.ttf'
SYMBOLS = ROOT / 'third_party' / 'nerd-fonts-symbols' / 'SymbolsNerdFontMono-Regular.ttf'
OUTPUT = ROOT / 'public' / 'downloads' / 'AsbirMono-NerdFont-Review-Regular.ttf'
REPORT = ROOT / 'reports' / 'nerd-font-qa.json'
NOTICE = ROOT / 'THIRD_PARTY_NOTICES.md'
NOTICE_MARKER = '## Asbir Mono Nerd Font terminal patch'
TARGET_ADVANCE = 600


def is_nerd_symbol(codepoint):
    """Keep the official Nerd Fonts PUA ranges used by patched terminals."""
    return 0xE000 <= codepoint <= 0xF8FF or 0xF0000 <= codepoint <= 0xF2FFF


def set_name(font, name_id, value):
    table = font['name']
    table.names = [record for record in table.names if record.nameID != name_id]
    table.setName(value, name_id, 3, 1, 0x409)


def set_terminal_names(font):
    family = 'Asbir Mono Nerd Font Review'
    full_name = f'{family} Regular'
    postscript = 'AsbirMonoNerdFont-Review'
    for name_id, value in (
        (1, family), (2, 'Regular'), (3, f'{postscript};Version 1.000'),
        (4, full_name), (5, 'Version 1.000'), (6, postscript),
        (16, family), (17, 'Regular'), (18, full_name), (25, 'AsbirMonoNerdFont'),
    ):
        set_name(font, name_id, value)
    font['name'].names = [record for record in font['name'].names if record.platformID != 1]


def transformed_glyph(source, glyph_name, target_center_y):
    glyph_set = source.getGlyphSet()
    bounds_pen = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(bounds_pen)
    bounds = bounds_pen.bounds
    if bounds is None:
        return None
    x_min, y_min, x_max, y_max = bounds
    source_advance = source['hmtx'].metrics[glyph_name][0]
    scale = TARGET_ADVANCE / source_advance
    x_shift = TARGET_ADVANCE / 2 - (x_min + x_max) * scale / 2
    y_shift = target_center_y - (y_min + y_max) * scale / 2
    recording_pen = DecomposingRecordingPen(glyph_set)
    glyph_set[glyph_name].draw(recording_pen)
    output_pen = TTGlyphPen(None)
    recording_pen.replay(TransformPen(output_pen, (scale, 0, 0, scale, x_shift, y_shift)))
    return output_pen.glyph()


def update_cmaps(font, mappings):
    base = font.getBestCmap().copy()
    base.update(mappings)
    for table in font['cmap'].tables:
        if table.format == 4:
            table.cmap.update({codepoint: name for codepoint, name in mappings.items() if codepoint <= 0xFFFF})
    for platform_id, encoding_id in ((0, 4), (3, 10)):
        table = CmapSubtable.newSubtable(12)
        table.platformID = platform_id
        table.platEncID = encoding_id
        table.language = 0
        table.cmap = base.copy()
        font['cmap'].tables.append(table)


def append_notice():
    contents = NOTICE.read_text()
    if NOTICE_MARKER in contents:
        contents = contents[:contents.index(NOTICE_MARKER)].rstrip() + '\n'
    license_text = (ROOT / 'third_party' / 'nerd-fonts-symbols' / 'LICENSE').read_text().strip()
    contents += f'''\n\n---\n\n{NOTICE_MARKER}\n\nThe optional `AsbirMono-NerdFont-Review-Regular.ttf` terminal build includes symbols from Nerd Fonts Symbols Only v3.4.0. Nerd Fonts symbols are provided under the MIT License; the full notice is reproduced below.\n\n---\n\n{license_text}\n'''
    NOTICE.write_text(contents)


def main():
    if not CORE.exists() or not SYMBOLS.exists():
        raise SystemExit('Build the core Mono Regular TTF and extract NerdFontsSymbolsOnly first.')
    target = TTFont(CORE)
    source = TTFont(SYMBOLS)
    source_cmap = source.getBestCmap()
    existing = target.getBestCmap()
    target_center_y = (target['OS/2'].sCapHeight or 710) / 2
    glyph_order = target.getGlyphOrder()
    mappings = {}
    skipped = 0
    for codepoint, source_name in sorted(source_cmap.items()):
        if not is_nerd_symbol(codepoint) or codepoint in existing:
            continue
        glyph = transformed_glyph(source, source_name, target_center_y)
        if glyph is None:
            skipped += 1
            continue
        name = f'nf{codepoint:05X}'
        target['glyf'].glyphs[name] = glyph
        target['hmtx'].metrics[name] = (TARGET_ADVANCE, 0)
        glyph_order.append(name)
        mappings[codepoint] = name
    target.setGlyphOrder(glyph_order)
    target['maxp'].numGlyphs = len(glyph_order)
    update_cmaps(target, mappings)
    set_terminal_names(target)
    target['post'].isFixedPitch = 1
    target['OS/2'].xAvgCharWidth = TARGET_ADVANCE
    target.recalcBBoxes = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    target.save(OUTPUT)
    append_notice()
    final = TTFont(OUTPUT)
    cmap = final.getBestCmap()
    samples = {f'U+{codepoint:04X}': cmap.get(codepoint) for codepoint in (0xE0B0, 0xE0B1, 0xE0B2, 0xF0C4, 0xEA60)}
    report = {
        'file': OUTPUT.name,
        'source': SYMBOLS.name,
        'added_symbols': len(mappings),
        'skipped_empty_symbols': skipped,
        'glyph_count': len(final.getGlyphOrder()),
        'fixed_pitch': final['post'].isFixedPitch == 1,
        'all_added_symbols_fixed_width': all(final['hmtx'].metrics[name][0] == TARGET_ADVANCE for name in mappings.values()),
        'sample_codepoints': samples,
    }
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    if not all((report['fixed_pitch'], report['all_added_symbols_fixed_width'], all(samples.values()))):
        raise SystemExit('Nerd Font terminal build did not pass its fixed-cell QA.')
    print(f'Built {OUTPUT.name}: {len(mappings)} Nerd Font / Powerline symbols added')
    print(f'QA report: {REPORT}')


if __name__ == '__main__':
    main()
