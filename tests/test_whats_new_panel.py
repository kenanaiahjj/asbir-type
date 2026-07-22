import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WhatsNewPanelTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / 'src' / 'main.js').read_text()

    def test_panel_has_versioned_copy_links_and_storage_key(self):
        for expected in (
            "What’s new · 1.1.1",
            'asbir-whats-new-1.1.1-dismissed',
            '/downloads/AsbirSans-1.1.1.zip',
            '/downloads/AsbirMono-1.1.1.zip',
            'True italic family',
            'WOFF2 + CSS kit',
            'Approved production family',
            'Fixed-cell terminal companion',
        ):
            self.assertIn(expected, self.source)

    def test_panel_has_open_state_and_keyboard_close_contract(self):
        self.assertIn('aria-expanded', self.source)
        self.assertIn("event.key === 'Escape'", self.source)
        self.assertIn('localStorage.setItem', self.source)

    def test_family_release_has_explicit_italic_guard(self):
        self.assertIn("const hasItalic = state.family === 'sans' || state.family === 'mono';", self.source)


if __name__ == '__main__':
    unittest.main()
