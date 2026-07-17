import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'tools' / 'package_asbir_sans_release.py'
WEIGHTS = ('Thin', 'ExtraLight', 'Light', 'Regular', 'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black')


def load_packager():
    spec = importlib.util.spec_from_file_location('package_asbir_sans_release', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageAsbirSansReleaseTests(unittest.TestCase):
    def test_package_uses_format_folders_and_single_archive_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'downloads'
            source.mkdir()
            for weight in WEIGHTS:
                (source / f'AsbirSans-Review-{weight}.ttf').write_bytes(b'ttf')
                (source / f'AsbirSans-Review-{weight}.otf').write_bytes(b'otf')
            (source / 'AsbirSans-Review-VF.ttf').write_bytes(b'variable')
            notices = root / 'THIRD_PARTY_NOTICES.md'
            notices.write_text('notices')

            packager = load_packager()
            packager.SOURCE = source
            packager.TARGET = root / 'release' / 'AsbirSans-1.1.0'
            packager.ARCHIVE = source / 'AsbirSans-1.1.0.zip'
            packager.NOTICES = notices
            packager.main()

            self.assertTrue((packager.TARGET / 'OTF' / 'AsbirSans-Regular.otf').is_file())
            self.assertTrue((packager.TARGET / 'TTF' / 'AsbirSans-Regular.ttf').is_file())
            self.assertTrue((packager.TARGET / 'Variable' / 'AsbirSans-Variable.ttf').is_file())
            self.assertTrue(packager.ARCHIVE.is_file())

            from zipfile import ZipFile

            with ZipFile(packager.ARCHIVE) as archive:
                paths = archive.namelist()
            self.assertIn('AsbirSans-1.1.0/OTF/AsbirSans-Regular.otf', paths)
            self.assertIn('AsbirSans-1.1.0/TTF/AsbirSans-Regular.ttf', paths)
            self.assertIn('AsbirSans-1.1.0/Variable/AsbirSans-Variable.ttf', paths)
            self.assertIn('AsbirSans-1.1.0/README.md', paths)


if __name__ == '__main__':
    unittest.main()
