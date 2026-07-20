import json
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
RELEASE_DIR = ROOT / 'release' / 'AsbirIcons-Soft-1.0.0'
ARCHIVE = ROOT / 'release' / 'AsbirIcons-Soft-1.0.0.zip'


class AsbirIconsReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'src' / 'icons' / 'catalog.json').read_text())

    def test_release_directory_contains_only_pack_deliverables(self):
        self.assertTrue(RELEASE_DIR.is_dir())
        required = {'README.md', 'LICENSE', 'CHANGELOG.md', 'manifest.json', 'icons'}
        self.assertTrue(required.issubset({path.name for path in RELEASE_DIR.iterdir()}))
        self.assertFalse(any(path.suffix.lower() in {'.ttf', '.otf', '.woff', '.woff2'} for path in RELEASE_DIR.rglob('*')))

    def test_release_manifest_matches_catalog_and_assets(self):
        manifest = json.loads((RELEASE_DIR / 'manifest.json').read_text())
        self.assertEqual(manifest['version'], '1.0.0')
        self.assertEqual(manifest['license'], 'MIT')
        self.assertEqual(len(manifest['icons']), len(self.catalog['icons']))
        for icon in manifest['icons']:
            for field in ('outlineAsset', 'filledAsset'):
                asset = RELEASE_DIR / icon[field].lstrip('/')
                self.assertTrue(asset.exists(), asset)

    def test_archive_contains_the_release_directory_without_unrelated_files(self):
        self.assertTrue(ARCHIVE.is_file())
        prefix = 'AsbirIcons-Soft-1.0.0/'
        with zipfile.ZipFile(ARCHIVE) as archive:
            names = archive.namelist()
            self.assertTrue(names)
            self.assertTrue(all(name.startswith(prefix) for name in names))
            self.assertIn(f'{prefix}manifest.json', names)
            self.assertIn(f'{prefix}LICENSE', names)
            self.assertFalse(any(name.lower().endswith(('.ttf', '.otf', '.woff', '.woff2')) for name in names))


if __name__ == '__main__':
    unittest.main()
