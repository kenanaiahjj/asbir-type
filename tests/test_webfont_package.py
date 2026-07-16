import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebfontPackageTests(unittest.TestCase):
    def test_web_kits_include_normal_and_italic_faces(self):
        for family in ('AsbirSans', 'AsbirMono'):
            folder = ROOT / 'public' / 'downloads' / 'web' / family
            css = folder / f'{family}.css'
            self.assertTrue(css.is_file(), css)
            text = css.read_text()
            self.assertIn('font-style: normal', text)
            self.assertIn('font-style: italic', text)
            self.assertTrue((folder / f'{family}-Variable.woff2').is_file())
            self.assertTrue((folder / f'{family}-Italic-Variable.woff2').is_file())
            self.assertTrue((folder / f'{family}-Regular.woff2').is_file())
            self.assertTrue((folder / f'{family}-Italic-Regular.woff2').is_file())


if __name__ == '__main__':
    unittest.main()
