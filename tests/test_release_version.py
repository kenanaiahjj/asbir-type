import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_release_version():
    spec = importlib.util.spec_from_file_location('release_version', ROOT / 'tools' / 'release_version.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseVersionTests(unittest.TestCase):
    def test_current_release_uses_semver_1_1_1_and_font_revision_1_101(self):
        version = load_release_version()
        self.assertEqual(version.RELEASE_VERSION, '1.1.1')
        self.assertEqual(version.FONT_VERSION, '1.101')


if __name__ == '__main__':
    unittest.main()
