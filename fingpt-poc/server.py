from fastapi import FastAPI, Query
import requests
import yfinance as yf
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI(title="FinGPT Indian MF Analyzer")

# --- INITIALIZE MODEL (Loaded once in memory) ---
print("--- Loading FinGPT Sentiment Engine ---")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ['Positive', 'Negative', 'Neutral']
    return labels[torch.argmax(prediction)]

@app.get("/analyze")
async def analyze_fund(code: str = Query(..., description="The mfapi.in scheme code (e.g., 118778)")):
    try:
        # 1. Fetch MF Data
        mf_url = f"https://api.mfapi.in/mf/{code}"
        mf_res = requests.get(mf_url).json()
        
        if not mf_res or 'meta' not in mf_res:
            return {"error": "Invalid Scheme Code or API Down"}

        scheme_name = mf_res['meta'].get('scheme_name', 'Unknown Fund')
        nav = mf_res['data'][0]['nav']
        prev_nav = mf_res['data'][1]['nav']
        day_change = ((float(nav) - float(prev_nav)) / float(prev_nav)) * 100

        # 2. Fetch Market Sentiment (Nifty 50 Context)
        nifty = yf.Ticker("^NSEI")
        raw_news = nifty.news if nifty.news else []
        
        analysis = []
        positive_count = 0
        
        # Robustly handle the new yfinance news format
        for item in raw_news[:3]:
            # Use .get() to avoid KeyError if 'title' or 'content' is missing
            title = item.get('title') or item.get('content', {}).get('title', 'No Title Available')
            
            sent = get_sentiment(title)
            if sent == "Positive": 
                positive_count += 1
            analysis.append({"headline": title, "sentiment": sent})

        # 3. Strategy Logic
        if day_change < 0 and positive_count >= 1:
            advice = "ACCUMULATE: NAV dip contradicts Bullish market news. Strong buying signal."
        elif day_change > 0 and positive_count == 0:
            advice = "CAUTION: NAV rising despite Bearish sentiment. Monitor for reversal."
        else:
            advice = "NEUTRAL: Fund performance aligns with market mood."

        return {
            "scheme": scheme_name,
            "nav": nav,
            "day_change_pct": f"{day_change:.2f}%",
            "market_headlines": analysis,
            "recommendation": advice
        }
    except Exception as e:
        # This will now print the actual error to your terminal for better debugging
        print(f"Server Error: {str(e)}")
        return {"error": str(e)}


@app.get("/")
def health_check():
    return {"status": "FinGPT Server is active"}