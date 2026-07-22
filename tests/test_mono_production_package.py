import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


class MonoProductionPackageTests(unittest.TestCase):
    def test_production_package_contains_clean_roman_italic_and_terminal_folders(self):
        archive_path = ROOT / 'public' / 'downloads' / 'AsbirMono-1.1.1.zip'
        self.assertTrue(archive_path.is_file(), archive_path)
        with ZipFile(archive_path) as archive:
            paths = set(archive.namelist())
        self.assertIn('AsbirMono-1.1.1/OTF/AsbirMono-Regular.otf', paths)
        self.assertIn('AsbirMono-1.1.1/TTF/AsbirMono-Regular.ttf', paths)
        self.assertIn('AsbirMono-1.1.1/Variable/AsbirMono-Variable.ttf', paths)
        self.assertIn('AsbirMono-1.1.1/Italic/AsbirMono-Italic-Variable.ttf', paths)
        self.assertIn('AsbirMono-1.1.1/Terminal/AsbirMono-NerdFont-Regular.ttf', paths)
        self.assertTrue(all('Review' not in path for path in paths if path.endswith(('.ttf', '.otf'))))


if __name__ == '__main__':
    unittest.main()
