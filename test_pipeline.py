"""
OmniSight Automated Pipeline Test Suite
----------------------------------------
Validates end-to-end execution of the visual QA agent:
1. Verifies browser rendering engine output.
2. Asserts CSS injection successfully modifies target HTML.
"""

import os
import unittest
from browser_engine import capture_viewport
from main import apply_css_fix

class TestOmniSightPipeline(unittest.TestCase):
    def setUp(self):
        self.test_html = os.path.join("mock_app", "index.html")
        self.test_img = "test_viewport.png"
        self.dummy_css = ".cta-button { position: static !important; }"

    def test_01_viewport_capture(self):
        """Tests if Playwright correctly generates a screenshot artifact."""
        capture_viewport(self.test_html, self.test_img)
        self.assertTrue(os.path.exists(self.test_img), "Viewport screenshot was not created.")

    def test_02_css_patch_injection(self):
        """Tests if apply_css_fix cleanly modifies the target HTML source."""
        success = apply_css_fix(self.test_html, self.dummy_css)
        self.assertTrue(success, "Failed to apply CSS patch.")

        with open(self.test_html, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(self.dummy_css, content, "Injected CSS not found in HTML target.")

    def tearDown(self):
        # Clean up temporary test artifacts
        if os.path.exists(self.test_img):
            os.remove(self.test_img)

if __name__ == "__main__":
    unittest.main()