import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ItalicBuildContractTests(unittest.TestCase):
    def test_italic_variable_fonts_expose_expected_axes(self):
        from fontTools.ttLib import TTFont

        sans = TTFont(ROOT / 'public' / 'downloads' / 'AsbirSans-Review-Italic-VF.ttf')
        mono = TTFont(ROOT / 'public' / 'downloads' / 'AsbirMono-Review-Italic-VF.ttf')
        self.assertEqual({axis.axisTag for axis in sans['fvar'].axes}, {'opsz', 'wght'})
        self.assertEqual({axis.axisTag for axis in mono['fvar'].axes}, {'wght'})

    def test_italic_mono_static_fonts_keep_one_600_unit_cell(self):
        from fontTools.ttLib import TTFont

        font = TTFont(ROOT / 'public' / 'downloads' / 'AsbirMono-Review-Italic-Regular.ttf')
        advances = {font['hmtx'].metrics[name][0] for name in font.getBestCmap().values()}
        self.assertEqual(advances, {600})


if __name__ == '__main__':
    unittest.main()
