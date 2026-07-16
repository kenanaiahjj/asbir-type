"""Apply the selected Asbir Sans character system to the authored foundation.

Inter supplies the robust, multilingual interpolation and drawing discipline.
This pass changes the default forms that establish Asbir's voice, using the
foundation's own professionally drawn alternate constructions across every
master. It is intentionally small and high-impact: the alphabet remains a
coherent text family instead of a collection of procedurally rebuilt glyphs.
"""
from pathlib import Path

from ufoLib2 import Font


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-sans'
MASTERS = tuple(sorted(SOURCE.glob('*.ufo')))

# Single-storey a, more geometric t/G, and open construction figures create a
# recognisable neo-grotesk voice while retaining production-quality contours.
DEFAULT_FORMS = {
    'a': 'a.1',
    't': 't.1',
    'G': 'G.1',
    'one': 'one.ss01',
    'four': 'four.ss01',
}


def copy_default_form(font: Font, target_name: str, alternate_name: str) -> None:
    target = font[target_name]
    alternate = font[alternate_name]
    unicode_values = list(target.unicodes)
    target.copyDataFromGlyph(alternate)
    target.unicodes = unicode_values
    target.lib['com.asbir.identitySource'] = alternate_name


def main() -> None:
    if not MASTERS:
        raise SystemExit(f'No editable masters found in {SOURCE}')
    for path in MASTERS:
        font = Font.open(path)
        missing = [(target, alternate) for target, alternate in DEFAULT_FORMS.items() if target not in font or alternate not in font]
        if missing:
            raise SystemExit(f'{path.name} is missing identity forms: {missing}')
        for target, alternate in DEFAULT_FORMS.items():
            copy_default_form(font, target, alternate)
        font.lib['com.asbir.characterSystem'] = 'geometric-neogrotesk-v1'
        font.save(path, overwrite=True)
        print(f'Applied Asbir character system to {path.name}')


if __name__ == '__main__':
    main()
