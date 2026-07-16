import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_font_qa():
    spec = importlib.util.spec_from_file_location('font_qa', ROOT / 'tools' / 'font_qa.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FontReleaseContractsTests(unittest.TestCase):
    def test_production_signoff_is_family_scoped(self):
        qa = load_font_qa()
        self.assertTrue(qa.production_signoff_present('sans'))
        self.assertTrue(qa.production_signoff_present('mono'))

    def test_italic_release_artifacts_are_present_for_both_families(self):
        weights = ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')
        for prefix in ('AsbirSans', 'AsbirMono'):
            for weight in weights:
                for extension in ('ttf', 'otf'):
                    path = ROOT / 'public' / 'downloads' / f'{prefix}-Review-Italic-{weight}.{extension}'
                    self.assertTrue(path.is_file(), path)
            self.assertTrue((ROOT / 'public' / 'downloads' / f'{prefix}-Review-Italic-VF.ttf').is_file())


if __name__ == '__main__':
    unittest.main()
