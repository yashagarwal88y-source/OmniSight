import asyncio
import os
from playwright.sync_api import sync_playwright

def capture_screenshot_sync(url: str, output_path: str = "screenshot.png"):
    """Synchronous Playwright execution for thread compatibility."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 375, "height": 667},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        )
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)
        page.screenshot(path=output_path, full_page=True)
        print(f"[+] Screenshot captured and saved to: {output_path}")
        browser.close()

async def capture_viewport_screenshot(url: str, output_path: str = "screenshot.png"):
    """Runs the synchronous Playwright capture in a separate worker thread."""
    await asyncio.to_thread(capture_screenshot_sync, url, output_path)

if __name__ == "__main__":
    local_page_path = f"file://{os.path.abspath('mock_app/index.html')}"
    asyncio.run(capture_viewport_screenshot(local_page_path))