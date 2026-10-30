# OmniSight: Autonomous Visual QA & Self-Healing AI Agent

OmniSight is a multimodal AI agent that automatically detects visual layout regressions (such as clipped buttons, overlapping text, or overflow issues) in web/mobile viewports and dynamically injects CSS patches to self-heal the target application.

## 🏗️ Architecture & Pipeline Flow
1. **Browser Engine (`browser_engine.py`)**: Uses Playwright to render local web applications inside headless viewports and capture PNG snapshots.
2. **VLM Audit Engine (`vlm_engine.py`)**: Sends Base64-encoded screenshots along with DOM source code to Vision-Language Models via OpenRouter to evaluate layout anomalies and output strict JSON CSS patches.
3. **Orchestrator (`main.py`)**: Manages the autonomous closed-loop cycle: initial snapshot capture -> visual anomaly detection -> DOM CSS injection -> verification re-rendering.

## 🚀 Setup & Execution

### Prerequisites
* Python 3.10+
* Virtual Environment activated (`venv`)

### Installation
1. Clone the repository and navigate to the project directory:
   ```powershell
   cd omnisight-agent