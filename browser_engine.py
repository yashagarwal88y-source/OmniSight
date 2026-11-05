import os
from playwright.sync_api import sync_playwright

# Preset responsive viewports for multi-device visual testing
VIEWPORTS = {
    "mobile": {"width": 375, "height": 812},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900}
}

def capture_viewport(html_path: str, output_image_path: str, viewport_size: dict = None):
    """
    Launches a headless Chromium browser using Playwright, opens the local HTML file,
    sets a viewport size, and captures a PNG screenshot.
    """
    if viewport_size is None:
        viewport_size = VIEWPORTS["mobile"]

    abs_html_path = os.path.abspath(html_path)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=viewport_size)
        page = context.new_page()
        
        # Navigate to local file
        page.goto(f"file://{abs_html_path}")
        page.wait_for_load_state("networkidle")
        
        # Take screenshot of the viewport
        page.screenshot(path=output_image_path, full_page=False)
        browser.close()

def capture_multi_viewports(html_path: str, output_dir: str = ".") -> dict:
    """
    Captures screenshots across mobile, tablet, and desktop viewports.
    Returns a dictionary mapping device names to image paths.
    """
    captured_files = {}
    for device, size in VIEWPORTS.items():
        out_path = os.path.join(output_dir, f"ci_viewport_{device}.png")
        capture_viewport(html_path, out_path, viewport_size=size)
        captured_files[device] = out_path
        print(f"[+] Captured {device} viewport ({size['width']}x{size['height']}) -> {out_path}")
    return captured_files

if __name__ == "__main__":
    target_html = os.path.join("mock_app", "index.html")
    capture_multi_viewports(target_html)