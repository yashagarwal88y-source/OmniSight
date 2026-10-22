import base64
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load key from .env file into os.environ
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY missing! Please set it in your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def encode_image_to_base64(image_path: str) -> str:
    """Converts a local image file to a Base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_ui_and_generate_fix(image_path: str, html_path: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    base64_image = encode_image_to_base64(image_path)
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    system_instruction = (
        "You are OmniSight, an Autonomous Visual QA and Frontend Self-Healing AI Agent. "
        "Analyze the provided screenshot and raw HTML. Identify visual bugs "
        "(such as off-screen elements, clipping, bad contrast, overlapping text). "
        "Return your analysis strictly in raw JSON format matching the schema."
    )

    user_prompt = (
        "Here is the source HTML code of the web page:\n\n"
        "```html\n"
        + html_content +
        "\n```\n\n"
        "Perform a visual audit using the attached mobile screenshot:\n"
        "1. Is there a visual UI bug affecting user interaction?\n"
        "2. Explain what the visual anomaly is.\n"
        "3. Provide the exact CSS code replacement or override needed to fix the issue cleanly.\n\n"
        "Respond strictly in valid JSON format:\n"
        "{\n"
        '  "has_visual_bug": true,\n'
        '  "bug_description": "Detailed explanation of visual error",\n'
        '  "affected_selector": ".css-class-or-id",\n'
        '  "css_fix": "Exact CSS rules to resolve the issue"\n'
        "}"
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role": "system", "content": system_instruction},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    test_image = "ci_viewport.png"
    test_html = os.path.join("mock_app", "index.html")
    
    print("[*] Sending screenshot and HTML to OpenRouter Vision for visual audit...")
    analysis = analyze_ui_and_generate_fix(test_image, test_html)
    print("\n[+] Visual Audit Analysis Result:")
    print(json.dumps(analysis, indent=2))