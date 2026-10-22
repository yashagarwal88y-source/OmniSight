import os
import json
from vlm_engine import analyze_ui_and_generate_fix

def apply_css_fix(html_file_path: str, css_code: str):
    """Injects the generated CSS fix into the HTML document inside a <style> tag."""
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    style_injection = f"\n<style>\n/* Auto-applied by OmniSight Self-Healing Agent */\n{css_code}\n</style>\n"
    
    # Inject before </head> if it exists, otherwise append at the top
    if "</head>" in html_content:
        updated_html = html_content.replace("</head>", f"{style_injection}</head>")
    else:
        updated_html = style_injection + html_content

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print(f"[+] Successfully injected CSS fix into {html_file_path}")

def run_omnisight_pipeline():
    print("=== OmniSight Autonomous Visual QA & Self-Healing Pipeline ===")
    
    image_path = "ci_viewport.png"
    html_path = os.path.join("mock_app", "index.html")

    # Step 1: Run VLM Engine Audit
    print("\n[*] Step 1: Auditing mobile UI screenshot...")
    audit_result = analyze_ui_and_generate_fix(image_path, html_path)
    
    print("\n[+] VLM Audit Analysis Result:")
    print(json.dumps(audit_result, indent=2))

    # Step 2: Check for Visual Bug
    if audit_result.get("has_visual_bug"):
        print(f"\n[!] Visual Bug Detected: {audit_result.get('bug_description')}")
        css_fix = audit_result.get("css_fix")
        
        if css_fix:
            print("\n[*] Step 2: Applying automated CSS fix to source code...")
            apply_css_fix(html_path, css_fix)
            print("\n[SUCCESS] Self-healing cycle completed!")
        else:
            print("\n[-] Warning: Bug detected but no CSS fix provided in response.")
    else:
        print("\n[+] No visual bugs detected. UI passed QA audit.")

if __name__ == "__main__":
    run_omnisight_pipeline()