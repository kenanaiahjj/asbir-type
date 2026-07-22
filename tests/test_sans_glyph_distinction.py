import unittest
from pathlib import Path

from ufoLib2 import Font


ROOT = Path(__file__).resolve().parents[1]


class SansGlyphDistinctionTests(unittest.TestCase):
    def test_uppercase_i_has_terminal_bars_in_every_roman_and_italic_master(self):
        source_folders = (ROOT / 'sources' / 'asbir-sans', ROOT / 'sources' / 'asbir-sans-italic')
        master_paths = sorted(path for folder in source_folders for path in folder.glob('*.ufo'))

        self.assertEqual(len(master_paths), 12)
        for master_path in master_paths:
            with self.subTest(master=master_path.name):
                font = Font.open(master_path)
                glyph = font['I']
                self.assertEqual(len(glyph.contours), 1)
                points = list(glyph.contours[0].points)
                self.assertGreaterEqual(len(points), 8)

                x_values = [point.x for point in points]
                y_values = sorted({point.y for point in points})
                self.assertGreaterEqual(len(y_values), 4)
                self.assertGreaterEqual(len(set(x_values)), 4)


if __name__ == '__main__':
    unittest.main()
