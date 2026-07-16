"""Add editable ligature and slashed-zero source glyphs to every Asbir family."""
from pathlib import Path

from ufoLib2 import Font
from ufoLib2.objects import Anchor, Component

from expand_asbir_sans_sources import diagonal, figure

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    'sans': ('asbir-sans', 'AsbirSans', (30, 64, 150)),
    'serif': ('asbir-serif', 'AsbirSerif', (24, 48, 118)),
    'mono': ('asbir-mono', 'AsbirMono', (28, 58, 132)),
}
LIGATURES = {
    'f_f': ('f', 'f'),
    'f_i': ('f', 'i'),
    'f_l': ('f', 'l'),
    'f_f_i': ('f', 'f', 'i'),
    'f_f_l': ('f', 'f', 'l'),
}
FIGURE_NAMES = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
PNUM_WIDTHS = (500, 310, 470, 470, 500, 470, 500, 440, 500, 500)
ONUM_Y = (65, 0, 65, 65, 85, 65, 0, 95, 65, 0)


def substitution_rules(suffix):
    return '\n  '.join(f'sub uni003{index} by {name}.{suffix};' for index, name in enumerate(FIGURE_NAMES))


NUMR_RULES = substitution_rules('numr')
DNOM_RULES = substitution_rules('dnom')
SUPS_RULES = substitution_rules('sups')
SUBS_RULES = substitution_rules('subs')
FEATURES = """@KernLeftA = [A V W Y T L F P R uni0391 uni0394 uni039B uni0410 uni0414 uni041B];
@KernLeftT = [T uni03A4 uni0422 uni0413];
@KernLeftDiagonal = [V W Y uni03A5 uni0423];
@KernRightRound = [O C G Q o c e g q d uni039F uni0398 uni03BF uni03B8 uni03C6 uni041E uni0424 uni043E uni0444];
@KernRightLower = [a e o u y uni03B1 uni03B5 uni03BF uni03C3 uni03C9 uni0430 uni0435 uni043E uni0441 uni044D];
@KernPunctuation = [uni002C uni002E uni003A uni003B];

feature kern {
  pos A [V W Y] -55;
  pos A @KernRightRound -20;
  pos A @KernPunctuation -18;
  pos L [T V W Y] -35;
  pos T [A O C G Q a e o u y] -45;
  pos T @KernPunctuation -35;
  pos V [A a e o u] -52;
  pos V @KernPunctuation -42;
  pos W [A a e o u] -40;
  pos W @KernPunctuation -30;
  pos Y [A a e o u] -60;
  pos Y @KernPunctuation -48;
  pos F [A a e o] -24;
  pos P [A a e o] -18;
  pos R [V W Y] -18;
  # Greek and Cyrillic are kerned with their own structural groups rather
  # than inheriting Latin fallback spacing. This covers the pairs encountered
  # in editorial Greek/Cyrillic text at display and text sizes.
  pos [A uni0391 uni0394 uni039B uni0410 uni0414 uni041B] @KernLeftDiagonal -55;
  pos [A uni0391 uni0394 uni039B uni0410 uni0414 uni041B] @KernRightRound -20;
  pos @KernLeftT [A uni0391 uni0410] -42;
  pos @KernLeftT @KernRightRound -45;
  pos @KernLeftT @KernRightLower -38;
  pos @KernLeftDiagonal [A uni0391 uni0410] -52;
  pos @KernLeftDiagonal @KernRightLower -48;
  pos @KernLeftDiagonal @KernPunctuation -42;
} kern;

feature liga {
  sub f f i by f_f_i;
  sub f f l by f_f_l;
  sub f f by f_f;
  sub f i by f_i;
  sub f l by f_l;
} liga;

feature pnum {
  sub uni0030 by zero.pnum;
  sub uni0031 by one.pnum;
  sub uni0032 by two.pnum;
  sub uni0033 by three.pnum;
  sub uni0034 by four.pnum;
  sub uni0035 by five.pnum;
  sub uni0036 by six.pnum;
  sub uni0037 by seven.pnum;
  sub uni0038 by eight.pnum;
  sub uni0039 by nine.pnum;
} pnum;

feature onum {
  sub uni0030 by zero.onum;
  sub uni0031 by one.onum;
  sub uni0032 by two.onum;
  sub uni0033 by three.onum;
  sub uni0034 by four.onum;
  sub uni0035 by five.onum;
  sub uni0036 by six.onum;
  sub uni0037 by seven.onum;
  sub uni0038 by eight.onum;
  sub uni0039 by nine.onum;
} onum;

feature tnum {
  sub zero.pnum by uni0030;
  sub one.pnum by uni0031;
  sub two.pnum by uni0032;
  sub three.pnum by uni0033;
  sub four.pnum by uni0034;
  sub five.pnum by uni0035;
  sub six.pnum by uni0036;
  sub seven.pnum by uni0037;
  sub eight.pnum by uni0038;
  sub nine.pnum by uni0039;
} tnum;

feature zero {
  sub uni0030 by zero.slash;
  sub zero.pnum by zero.pnum.slash;
  sub zero.onum by zero.onum.slash;
} zero;

feature numr {
  __NUMR_RULES__
} numr;

feature dnom {
  __DNOM_RULES__
} dnom;

feature sups {
  __SUPS_RULES__
} sups;

feature subs {
  __SUBS_RULES__
} subs;

feature ordn {
  sub a by a.ordn;
  sub o by o.ordn;
} ordn;"""
FEATURES = (FEATURES.replace('__NUMR_RULES__', NUMR_RULES).replace('__DNOM_RULES__', DNOM_RULES)
                    .replace('__SUPS_RULES__', SUPS_RULES).replace('__SUBS_RULES__', SUBS_RULES))
MONO_FEATURES = """feature zero {
  sub uni0030 by zero.slash;
} zero;

feature numr {
  __NUMR_RULES__
} numr;

feature dnom {
  __DNOM_RULES__
} dnom;

feature sups {
  __SUPS_RULES__
} sups;

feature subs {
  __SUBS_RULES__
} subs;

feature ordn {
  sub a by a.ordn;
  sub o by o.ordn;
} ordn;"""
MONO_FEATURES = (MONO_FEATURES.replace('__NUMR_RULES__', NUMR_RULES).replace('__DNOM_RULES__', DNOM_RULES)
                              .replace('__SUPS_RULES__', SUPS_RULES).replace('__SUBS_RULES__', SUBS_RULES))


def add_ligature(font, name, members, monospaced=False):
    if name in font:
        del font[name]
    glyph = font.newGlyph(name)
    advance = 0
    for member in members:
        glyph.components.append(Component(baseGlyph=member, transformation=(1, 0, 0, 1, advance, 0)))
        advance += font[member].width if monospaced else font[member].width * .62
    glyph.width = advance if monospaced else round(advance + font[members[-1]].width * .38)
    for index in range(1, len(members)):
        glyph.anchors.append(Anchor(round(glyph.width * index / len(members)), 0, name=f'caret_{index}'))


def reset_mono_zero(font, stem):
    """The default Mono zero is plain; the slashed form uses the zero feature."""
    if 'uni0030' in font:
        del font['uni0030']
    glyph = font.newGlyph('uni0030')
    glyph.width = 600
    glyph.unicodes = [0x0030]
    figure(glyph.getPen(), '0', stem)


def add_slashed_zero(font, stem):
    if 'zero.slash' in font:
        return
    glyph = font.newGlyph('zero.slash')
    glyph.width = font['uni0030'].width
    glyph.components.append(Component(baseGlyph='uni0030'))
    diagonal(glyph.getPen(), glyph.width * .30, 90, glyph.width * .70, 610, max(14, stem * .45))


def add_numeral_variant(font, name, base, width, transform, stem, slash=False):
    if name in font:
        del font[name]
    glyph = font.newGlyph(name)
    glyph.width = width
    glyph.components.append(Component(baseGlyph=base, transformation=transform))
    if slash:
        diagonal(glyph.getPen(), width * .30, 90, width * .70, 610, max(14, stem * .45))


def add_figure_features(font, stem):
    """Create editable pnum/onum sources; defaults remain tabular lining."""
    for index, name in enumerate(FIGURE_NAMES):
        base = f'uni003{index}'
        pnum_width = PNUM_WIDTHS[index]
        shift = round((pnum_width - font[base].width) / 2)
        add_numeral_variant(font, f'{name}.pnum', base, pnum_width, (1, 0, 0, 1, shift, 0), stem)
        onum_width = pnum_width
        scale = .78
        onum_shift = round((onum_width - font[base].width * scale) / 2)
        add_numeral_variant(font, f'{name}.onum', base, onum_width, (scale, 0, 0, scale, onum_shift, ONUM_Y[index]), stem)
    pnum_shift = round((PNUM_WIDTHS[0] - font['uni0030'].width) / 2)
    onum_shift = round((PNUM_WIDTHS[0] - font['uni0030'].width * .78) / 2)
    add_numeral_variant(font, 'zero.pnum.slash', 'uni0030', font['zero.pnum'].width, (1, 0, 0, 1, pnum_shift, 0), stem, slash=True)
    add_numeral_variant(font, 'zero.onum.slash', 'uni0030', font['zero.onum'].width, (.78, 0, 0, .78, onum_shift, ONUM_Y[0]), stem, slash=True)


def add_ordinal_variant(font, name, base, width, mono=False):
    if name in font:
        del font[name]
    glyph = font.newGlyph(name)
    glyph.width = width
    scale = .62
    source_width = font[base].width
    x_shift = 0 if mono else round((width - source_width * scale) / 2)
    glyph.components.append(Component(baseGlyph=base, transformation=(scale, 0, 0, scale, x_shift, 350)))


def add_vertical_figure_features(font, mono=False):
    """Build superior/inferior and fraction-part digit sources from the masters.

    They preserve Mono advances, while proportional families use compact,
    centered editorial figures. All remain editable component constructions.
    """
    for index, name in enumerate(FIGURE_NAMES):
        base = f'uni003{index}'
        width = font[base].width if mono else max(260, round(font[base].width * .62))
        scale = .62
        x_shift = 0 if mono else round((width - font[base].width * scale) / 2)
        for suffix, y in (('numr', 360), ('dnom', 0), ('sups', 360), ('subs', -145)):
            add_numeral_variant(font, f'{name}.{suffix}', base, width, (scale, 0, 0, scale, x_shift, y), 0)
    ordinal_width = font['a'].width if mono else 300
    add_ordinal_variant(font, 'a.ordn', 'a', ordinal_width, mono)
    add_ordinal_variant(font, 'o.ordn', 'o', ordinal_width, mono)


def main():
    for family, (folder, prefix, stems) in FAMILIES.items():
        for style, stem in zip(('Thin', 'Regular', 'Black'), stems):
            path = ROOT / 'sources' / folder / f'{prefix}-{style}.ufo'
            font = Font.open(path)
            if family == 'mono':
                reset_mono_zero(font, stem)
                for name in LIGATURES:
                    if name in font:
                        del font[name]
            else:
                for name, members in LIGATURES.items():
                    add_ligature(font, name, members)
                add_figure_features(font, stem)
            add_vertical_figure_features(font, mono=family == 'mono')
            add_slashed_zero(font, stem)
            font.features.text = MONO_FEATURES if family == 'mono' else FEATURES
            font.save(path, overwrite=True)
            print(f'Updated {family} {style}: {len(font)} glyphs')


if __name__ == '__main__':
    main()
