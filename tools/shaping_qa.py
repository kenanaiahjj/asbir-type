"""Exercise each built font with real Latin-language text through HarfBuzz."""
import json
import argparse
from pathlib import Path

import uharfbuzz as hb

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    'English': 'The quick brown fox jumps over the lazy dog.',
    'French': "A l'ete, le garcon deja la.",
    'German': 'Fuenf grosse Buecher, Straße.',
    'Polish': 'Zażółć gęślą jaźń.',
    'Czech': 'Příliš žluťoučký kůň úpěl ďábelské ódy.',
    'Turkish': 'İstanbul, ıslak yağmur, Şeker.',
    'Romanian': 'Știință și țară.',
    'Hungarian': 'Árvíztűrő tükörfúrógép.',
    'Icelandic': 'Þórður á Ðórshöfn.',
    'Vietnamese': 'Tiếng Việt: Trăm năm trong cõi người ta.',
    'Greek': 'Καλημέρα κόσμε. Τα γράμματα έχουν ρυθμό.',
    'Cyrillic': 'Съешь же ещё этих мягких французских булок, да выпей чаю.',
    'Typography': '“Quotes”—dash… €50 ± 10% →',
    'Symbols': '© ® ™ № · × ÷ ± ⇒ ⇐ ⇔',
}
FAMILY_PREFIXES = {'sans': 'AsbirSans', 'serif': 'AsbirSerif', 'mono': 'AsbirMono'}
FILES = [
    ROOT / 'public' / 'downloads' / f'{prefix}-Review-{style}.{extension}'
    for prefix in ('AsbirSans', 'AsbirSerif', 'AsbirMono')
    for style in ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')
    for extension in ('ttf', 'otf')
] + [
    ROOT / 'public' / 'downloads' / f'{prefix}-Review-VF.ttf'
    for prefix in ('AsbirSans', 'AsbirSerif', 'AsbirMono')
]


def shape(path, text, weight=None):
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    if weight is not None:
        font.set_variations({'wght': weight})
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer)
    infos = buffer.glyph_infos
    return {'glyphs': len(infos), 'missing': [info.cluster for info in infos if info.codepoint == 0]}


def glyph_ids(path, text, weight=None, features=None):
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    if weight is not None:
        font.set_variations({'wght': weight})
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer, features or {})
    return [info.codepoint for info in buffer.glyph_infos]


def advance(path, text, weight=None, features=None):
    data = path.read_bytes()
    font = hb.Font(hb.Face(data))
    if weight is not None:
        font.set_variations({'wght': weight})
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer, features or {})
    return sum(position.x_advance for position in buffer.glyph_positions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=tuple(FAMILY_PREFIXES), action='append')
    args = parser.parse_args()
    selected = args.family or list(FAMILY_PREFIXES)
    prefixes = {FAMILY_PREFIXES[family] for family in selected}
    results = []
    failures = []
    for path in (candidate for candidate in FILES if any(candidate.name.startswith(prefix) for prefix in prefixes)):
        weights = (100, 400, 700, 900) if path.name.endswith('-VF.ttf') else (None,)
        for weight in weights:
            samples = SAMPLES.items()
            if path.name.startswith('AsbirMono'):
                # Mono's documented release scope deliberately prioritizes
                # code/data Latin and Cyrillic; do not turn absent Greek into
                # an unhelpful false release failure.
                samples = ((language, sample) for language, sample in SAMPLES.items() if language != 'Greek')
            for language, sample in samples:
                result = shape(path, sample, weight)
                record = {'file': path.name, 'weight': weight, 'language': language, **result}
                results.append(record)
                if result['missing']:
                    failures.append(record)
            default_zero = glyph_ids(path, '0', weight)
            # Mono's coding default is already slashed; its ss09 feature gives
            # data-heavy contexts a deliberately non-slashed fallback.
            zero_feature = 'ss09' if path.name.startswith('AsbirMono') else 'zero'
            alternate_zero = glyph_ids(path, '0', weight, {zero_feature: 1})
            zero_record = {'file': path.name, 'weight': weight, 'feature': zero_feature, 'passes': default_zero != alternate_zero}
            results.append(zero_record)
            if not zero_record['passes']:
                failures.append(zero_record)
            if path.name.startswith('AsbirMono'):
                code_sample = 'O0 Il1 {}[]() @% /\\ <> := =>'
                mono_record = {
                    'file': path.name,
                    'weight': weight,
                    'feature': 'code-advance-grid',
                    'passes': advance(path, code_sample, weight) == len(code_sample) * 600,
                }
                results.append(mono_record)
                if not mono_record['passes']:
                    failures.append(mono_record)
                for operator in ('->', '=>', '!=', '==', '===', '<=', '>='):
                    default = glyph_ids(path, operator, weight)
                    literal = glyph_ids(path, operator, weight, {'liga': 0})
                    ligature_record = {
                        'file': path.name,
                        'weight': weight,
                        'feature': 'liga-default',
                        'operator': operator,
                        'passes': default != literal and advance(path, operator, weight) == len(operator) * 600,
                    }
                    results.append(ligature_record)
                    if not ligature_record['passes']:
                        failures.append(ligature_record)
            else:
                default_figures = glyph_ids(path, '0123456789', weight)
                tabular_figures = glyph_ids(path, '0123456789', weight, {'tnum': 1})
                # Proportional figures are the designed default in Asbir Sans;
                # explicitly enabling pnum is therefore allowed to be a no-op.
                # The tnum substitution proves that both numeral systems work.
                figure_record = {'file': path.name, 'weight': weight, 'feature': 'tnum', 'passes': tabular_figures != default_figures}
                results.append(figure_record)
                if not figure_record['passes']:
                    failures.append(figure_record)
                for label, pair in (('kern', 'AV'), ('kern-greek', 'Το'), ('kern-cyrillic', 'То')):
                    kerned_advance = advance(path, pair, weight)
                    unkerned_advance = advance(path, pair, weight, {'kern': 0})
                    kern_record = {'file': path.name, 'weight': weight, 'feature': label, 'pair': pair, 'passes': kerned_advance < unkerned_advance}
                    results.append(kern_record)
                    if not kern_record['passes']:
                        failures.append(kern_record)
            for tag, sample in (('numr', '0123'), ('dnom', '0123'), ('sups', '0123'), ('subs', '0123'), ('ordn', '1a')):
                default = glyph_ids(path, sample, weight)
                alternate = glyph_ids(path, sample, weight, {tag: 1})
                record = {'file': path.name, 'weight': weight, 'feature': tag, 'passes': alternate != default}
                results.append(record)
                if not record['passes']:
                    failures.append(record)
    report_path = ROOT / 'reports' / 'shaping-qa.json'
    report_path.write_text(json.dumps({'samples': SAMPLES, 'results': results, 'failures': failures}, indent=2) + '\n')
    print(f"Shaping QA: {'PASS' if not failures else 'FAIL'} ({len(results)} cases)")
    if failures:
        for failure in failures:
            print(f"{failure}")
    print(f'Report: {report_path}')
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
