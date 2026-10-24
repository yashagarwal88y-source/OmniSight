import os

DEFAULT_MODEL = "openrouter/free"
VIEWPORT_SIZE = {"width": 375, "height": 812}  # iPhone X/12 Mobile Viewport
TARGET_HTML = os.path.join("mock_app", "index.html")
INITIAL_SCREENSHOT = "ci_viewport.png"
FIXED_SCREENSHOT = "ci_viewport_fixed.png"