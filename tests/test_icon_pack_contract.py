import json
import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).parents[1]


class IconPackContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog_path = ROOT / 'src/icons/catalog.json'
        cls.catalog = json.loads(catalog_path.read_text()) if catalog_path.exists() else {'icons': []}
        cls.icons = cls.catalog['icons']

    def test_soft_pack_has_150_to_250_semantic_icons(self):
        self.assertGreaterEqual(len(self.icons), 150)
        self.assertLessEqual(len(self.icons), 250)
        self.assertEqual({icon['pack'] for icon in self.icons}, {'soft'})

    def test_every_record_has_unique_slug_and_required_metadata(self):
        slugs = [icon['slug'] for icon in self.icons]
        self.assertEqual(len(slugs), len(set(slugs)))
        required = {
            'pack', 'slug', 'name', 'category', 'aliases', 'keywords',
            'outlineAsset', 'filledAsset', 'related', 'contextExamples',
            'introducedIn',
        }
        for icon in self.icons:
            self.assertTrue(required.issubset(icon))
            self.assertRegex(icon['slug'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

    def test_every_record_has_valid_outline_and_filled_svg(self):
        for icon in self.icons:
            for field in ('outlineAsset', 'filledAsset'):
                path = ROOT / 'public' / icon[field].lstrip('/')
                self.assertTrue(path.exists(), path)
                root = ElementTree.fromstring(path.read_text())
                self.assertEqual(root.attrib.get('viewBox'), '0 0 24 24')
                source = path.read_text()
                self.assertIn('currentColor', source)
                self.assertNotRegex(source, r'(?:href|xlink:href|url\()\s*=|(?:href|xlink:href)="https?://')

    def test_related_references_resolve(self):
        slugs = {icon['slug'] for icon in self.icons}
        for icon in self.icons:
            self.assertTrue(set(icon['related']).issubset(slugs), icon['slug'])


if __name__ == '__main__':
    unittest.main()
