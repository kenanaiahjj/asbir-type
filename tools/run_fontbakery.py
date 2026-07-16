"""Run FontBakery one file at a time.

The Universal profile's family-axis check groups static and variable inputs in
this lightweight project, which produces a false range mismatch. Running each
artifact independently preserves the relevant checks for its own format.
"""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {'sans': 'AsbirSans', 'serif': 'AsbirSerif', 'mono': 'AsbirMono'}
SANS_REFERENCE_MATCHED_WAIVERS = ('base_has_width', 'case_mapping')
FILES = [
    ROOT / 'public/downloads' / f'{prefix}-Review-Regular.{extension}'
    for prefix in ('AsbirSans', 'AsbirSerif', 'AsbirMono')
    for extension in ('ttf', 'otf')
] + [
    ROOT / 'public/downloads' / f'{prefix}-Review-VF.ttf'
    for prefix in ('AsbirSans', 'AsbirSerif', 'AsbirMono')
] + [
    ROOT / 'public/downloads' / f'{prefix}-Review-Italic-Regular.{extension}'
    for prefix in ('AsbirSans', 'AsbirMono')
    for extension in ('ttf', 'otf')
] + [
    ROOT / 'public/downloads' / f'{prefix}-Review-Italic-VF.ttf'
    for prefix in ('AsbirSans', 'AsbirMono')
]

parser = argparse.ArgumentParser()
parser.add_argument('--family', choices=tuple(FAMILIES), action='append')
args = parser.parse_args()
prefixes = {FAMILIES[family] for family in (args.family or list(FAMILIES))}

for file in (candidate for candidate in FILES if any(candidate.name.startswith(prefix) for prefix in prefixes)):
    print(f'\n=== FontBakery: {file.name} ===')
    command = [sys.executable, '-m', 'fontbakery', 'check-universal', str(file), '--loglevel', 'WARN', '--succinct']
    # These two Universal-profile failures are verified to be identical in
    # Inter 4.001, the licensed derivative foundation. See
    # FONTBAKERY_WAIVERS.md; never apply this to Serif or Mono.
    if file.name.startswith('AsbirSans-'):
        for check_id in SANS_REFERENCE_MATCHED_WAIVERS:
            command.extend(['--exclude-checkid', check_id])
    # Roman and italic are deliberately separate variable files in Asbir. The
    # universal profile's ital_axis check assumes a single Roman/Italic axis
    # family and reports a false missing-Roman failure for the dedicated
    # italic file; the dedicated italic name/style metadata is checked in
    # tools/font_qa.py instead.
    if '-Italic-' in file.name:
        command.extend(['--exclude-checkid', 'opentype/STAT/ital_axis'])
    # FontBakery's mono check assumes TrueType outlines and crashes on CFF.
    # The Mono TTF still receives that check; the CFF receives all others.
    if file.name.startswith('AsbirMono-Review') and file.suffix == '.otf':
        command.extend(['--exclude-checkid', 'opentype/monospace'])
    subprocess.run(command, check=True)
