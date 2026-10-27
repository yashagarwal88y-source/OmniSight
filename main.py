import os
import json
import time  
from browser_engine import capture_viewport
from vlm_engine import analyze_ui_and_generate_fix

def apply_css_fix(html_file_path: str, css_code: str) -> bool:
    """Safely injects generated CSS fix into HTML file inside a style block."""
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        style_injection = f"\n<style>\n/* Auto-applied by OmniSight Agent */\n{css_code}\n</style>\n"
        
        if "</head>" in html_content:
            updated_html = html_content.replace("</head>", f"{style_injection}</head>")
        else:
            updated_html = style_injection + html_content

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(updated_html)
        return True
    except Exception as e:
        print(f"[-] Failed to apply CSS patch: {e}")
        return False


def log_audit_summary(start_time: float, bug_found: bool):
    """Prints execution time and final patch status."""
    duration = round(time.time() - start_time, 2)
    status = "SUCCESS - Patch Applied" if bug_found else "PASSED - No Bugs"
    print(f"\n[SUMMARY] Execution finished in {duration}s | Status: {status}")

def run_omnisight_pipeline():
    start_time = time.time()  # 👈 3. Start timing here
    
    print("=== OmniSight Autonomous Visual QA & Self-Healing Pipeline ===")
    
    image_path = "ci_viewport.png"
    html_path = os.path.join("mock_app", "index.html")
    fixed_image_path = "ci_viewport_fixed.png"

    # Step 1: Render and Capture Initial State
    print("\n[Step 1] Capturing initial mobile viewport screenshot...")
    capture_viewport(html_path, image_path)

    # Step 2: Multimodal Visual QA Audit
    print("\n[Step 2] Sending image + DOM source to VLM for visual audit...")
    audit_result = analyze_ui_and_generate_fix(image_path, html_path)
    print("\n[+] Audit Analysis Received:")
    print(json.dumps(audit_result, indent=2))

    bug_detected = audit_result.get("has_visual_bug", False)

    # Step 3: Self-Healing CSS Patch Injection
    if bug_detected and audit_result.get("css_fix"):
        print("\n[Step 3] Visual bug detected! Injecting CSS patch into target app...")
        success = apply_css_fix(html_path, audit_result["css_fix"])
        
        if success:
            print("[+] Self-healing CSS patch successfully injected.")
            
            # Step 4: Re-render and Verify Fix
            print("\n[Step 4] Re-rendering viewport to verify patch...")
            capture_viewport(html_path, fixed_image_path)
            print(f"[+] Post-fix verification image saved: {fixed_image_path}")
    else:
        print("\n[+] No visual UI bugs detected. Web application layout is clean.")

    # 👈 4. Call the Day 4 logger at the very end of the pipeline
    log_audit_summary(start_time, bug_detected)

if __name__ == "__main__":
    run_omnisight_pipeline()