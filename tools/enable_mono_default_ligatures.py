"""Expose Asbir Mono's core coding ligatures through default `liga` too."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-mono'
MASTERS = ('Thin', 'Regular', 'Black')
MARKER = '# Asbir Mono core coding ligatures (default on)'

# Keep `ss11` as the broader opt-in programming set. These seven are the
# high-frequency operators that the product team asked to be active by
# default. Disabling the standard-ligature feature restores literal ASCII.
LOOKUPS = (
    'hyphen_greater.liga',      # ->
    'equal_greater.liga',       # =>
    'exclam_equal.liga',        # !=
    'equal_equal.liga',         # ==
    'equal_equal_equal.liga',   # ===
    'less_equal.liga',          # <=
    'greater_equal.liga',       # >=
)


def default_feature():
    lookups = '\n'.join(f'  lookup {name};' for name in LOOKUPS)
    return f'''\n\n{MARKER}\n# Disable `liga` in an editor or stylesheet to show the literal operators.\nfeature liga {{\n{lookups}\n}} liga;\n'''


def main():
    for master in MASTERS:
        path = SOURCE / f'AsbirMono-{master}.ufo' / 'features.fea'
        contents = path.read_text()
        if MARKER in contents:
            before, _, remainder = contents.partition(MARKER)
            # Remove the generated feature through its closing marker so the
            # operation stays deterministic if its lookup order ever changes.
            closing = remainder.find('} liga;')
            if closing < 0:
                raise SystemExit(f'{path}: generated liga feature is incomplete')
            contents = before.rstrip() + '\n'
        if 'feature liga {' in contents:
            raise SystemExit(f'{path}: a non-generated liga feature already exists')
        path.write_text(contents.rstrip() + default_feature())
        print(f'Enabled default core coding ligatures in {path.parent.name}')


if __name__ == '__main__':
    main()
