# 🛡️ AI-Guard: Zero-Trust Browser Extension

AI-Guard is a custom Chrome browser extension designed to provide real-time, Zero-Trust threat analysis. It acts as an intelligent web filter, combining traditional Threat Intelligence with Large Language Model (LLM) context analysis to detect phishing, malware distribution, and suspicious web content dynamically.

## 📖 Overview

Standard ad-blockers and web filters rely on static blocklists that can easily be bypassed by zero-day phishing domains. AI-Guard solves this by utilizing a **Single-Shot Architecture** that scrapes the visible context of a webpage and cross-references it with VirusTotal analytics. This combined intelligence is then processed by Google's Gemini 2.5 Flash Lite engine to deliver an immediate, context-aware security verdict.

## 🚀 Key Features

* **Real-Time Context Analysis:** Scrapes the DOM and visible text of the active webpage to understand the actual content and intent of the site.
* **Threat Intelligence Integration:** Automatically queries the VirusTotal API v3 for historical reputation data and malicious flags.
* **LLM-Powered Verdicts:** Uses Gemini 2.5 Flash Lite to analyze both the VT stats and the page context, preventing false positives and catching sophisticated phishing attempts.
* **Decoupled Architecture:** Powered by a local FastAPI backend, ensuring that sensitive API keys and processing logic remain secure and completely out of the browser environment.
* **Rate-Limit Optimized:** Engineered with a single-shot payload delivery system to operate seamlessly within free-tier API constraints without triggering 429 Resource Exhausted errors.

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript (Chrome Extension V3 API)
* **Backend:** Python, FastAPI, Uvicorn
* **APIs:** Google Gemini 2.5 Flash Lite, VirusTotal API v3
* **Libraries:** `BeautifulSoup4` (Web Scraping), `Requests` (Network routing), `LangChain` (LLM orchestration), `Pydantic` (Data validation)

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.8+ installed on your system.
* Google Chrome or any Chromium-based browser.
* A free [Google AI Studio API Key](https://aistudio.google.com/).
* A free [VirusTotal API Key](https://www.virustotal.com/).

### 2. Backend Setup (Local Engine)
Clone this repository and install the required Python dependencies:
```bash
git clone [https://github.com/YourUsername/AI-Guard.git](https://github.com/YourUsername/AI-Guard.git)
cd AI-Guard
pip install fastapi uvicorn requests beautifulsoup4 langchain-google-genai pydantic

---

Start the FastAPI local engine:

Bash
python -m uvicorn api:app --reload
The engine will run locally on http://127.0.0.1:8000.

3. Frontend Setup (Chrome Extension)
Open Google Chrome and navigate to chrome://extensions/.

Toggle Developer mode on (top right corner).

Click Load unpacked (top left corner).

Select the Escudo_Navegador folder from the cloned repository.

The AI-Guard icon will now appear in your browser extensions toolbar!

🕵️‍♂️ Usage
Navigate to any website you want to analyze.

Click the AI-Guard extension icon in your toolbar.

Enter your Google API Key and VirusTotal API Key (these are kept locally and sent directly to your Python engine).

Click Scan Current Page.

Within seconds, the extension will return a clear BLOCK (Red) or ALLOW (Green) verdict along with a specific justification from the LLM.

👨‍💻 About the Developer
AI-Guard was built to bridge the gap between theoretical knowledge and practical security engineering. As I make a 10-year career transition from physical security into the cybersecurity space, I wanted to build a tool that actively applies modern defense concepts rather than just reading about them.

This extension serves as a practical, hands-on application of the principles and methodologies I have mastered through the Google Cybersecurity Certificate, the TryHackMe SOC Level 1 pathways, and my CompTIA Security+ studies.

Note: This is Version 1.0. Future updates (V2.0) will include background service workers for automated, invisible scanning and local Redis caching to further optimize API consumption.


Once you have this saved in your repository, your project will immediately look like it was structured by an experienced developer. Let me know if you would like to start working on the automated Version 2.0 next!
