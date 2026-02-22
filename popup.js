document.getElementById('scanBtn').addEventListener('click', async () => {
    const googleKey = document.getElementById('googleKey').value;
    const vtKey = document.getElementById('vtKey').value;
    const resultDiv = document.getElementById('result');

    if (!googleKey || !vtKey) {
        resultDiv.innerHTML = "⚠️ Please enter both API keys.";
        return;
    }

    resultDiv.innerHTML = "⏳ AI-Guard is scanning... Please wait.";

    // Get the URL of the current active tab
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let url = tab.url;

    try {
        const response = await fetch('http://127.0.0.1:8000/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, google_key: googleKey, vt_key: vtKey })
        });

        const data = await response.json();
        
        if (data.status === "success") {
            // 1. Clean the markdown ticks from the LLM response
            let cleanText = data.analysis.replace(/```json/gi, '').replace(/```/g, '').trim();
            
            try {
                // 2. Parse the JSON
                let parsedData = JSON.parse(cleanText);
                
                // 3. Set colors based on the verdict
                let verdictColor = parsedData.verdict === "BLOCK" ? "#ff4d4d" : "#00cc66"; // Red or Green
                
                // 4. Inject beautiful HTML
                resultDiv.innerHTML = `
                    <div style="margin-bottom: 8px;">
                        <span style="font-size: 14px; font-weight: bold; color: #aaa;">VERDICT:</span><br>
                        <span style="font-size: 22px; font-weight: bold; color: ${verdictColor};">${parsedData.verdict}</span>
                    </div>
                    <div style="line-height: 1.5; color: #ddd;">
                        <strong>Reason:</strong> ${parsedData.reason}
                    </div>
                `;
                
                // Change the border color to match the verdict
                resultDiv.style.borderLeft = `4px solid ${verdictColor}`;

            } catch (parseError) {
                // Fallback just in case the AI writes something weird
                resultDiv.innerText = cleanText;
            }

        } else {
            resultDiv.innerText = "Error: " + data.detail;
        }
    } catch (error) {
        resultDiv.innerHTML = "❌ Connection Failed. Is your Python engine running?";
    }
});