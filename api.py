from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
import base64
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware

# --- API INITIALIZATION ---
app = FastAPI(title="AI-Guard Browser Engine", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str
    google_key: str
    vt_key: str

# --- NATIVE FUNCTIONS (No longer AI Tools) ---
def scrape_web(url: str) -> str:
    """Extrae el texto de la web de forma local."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            return soup.get_text(separator=' ', strip=True)[:2000]
        return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

def check_vt(url: str, vt_key: str) -> str:
    """Consulta VirusTotal de forma local."""
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        headers = {"accept": "application/json", "x-apikey": vt_key}
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return f"Malicious: {stats.get('malicious', 0)}, Suspicious: {stats.get('suspicious', 0)}, Harmless: {stats.get('harmless', 0)}"
        return "No prior scan found or API Error."
    except Exception as e:
        return f"VT Connection Failed: {str(e)}"

# --- API ENDPOINT ---
@app.post("/scan")
def scan_website(request: ScanRequest):
    try:
        os.environ["GOOGLE_API_KEY"] = request.google_key
        
        # 1. Tu ordenador recopila la información primero (Sin gastar IA)
        vt_data = check_vt(request.url, request.vt_key)
        scrape_data = scrape_web(request.url)
        
        # 2. Construimos UN SOLO PROMPT con toda la información
        prompt = f"""
        You are a Senior Threat Intelligence Analyst. Analyze this URL: {request.url}
        
        Context 1 (VirusTotal Stats): {vt_data}
        Context 2 (Website Visible Text): {scrape_data}
        
        Provide a final security verdict (BLOCK or ALLOW) and a 1-sentence justification.
        Respond ONLY with a JSON string exactly like this:
        {{"verdict": "BLOCK", "reason": "Your explanation here."}}
        """

        # 3. Hacemos UN SOLO DISPARO a Gemini 2.5
        gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.2)
        response = gemini_llm.invoke(prompt)

        return {"status": "success", "analysis": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))