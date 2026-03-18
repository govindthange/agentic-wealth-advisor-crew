import os
import torch
import requests
import pandas as pd
import yfinance as yf
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from curl_cffi import requests as curl_requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load environment variables
load_dotenv()

app = FastAPI(title="FinGPT Indian MF Analyzer")

# --- MODEL PATH CONFIGURATION ---
MODEL_NAME = "ProsusAI/finbert"
LOCAL_MODEL_PATH = "./models/finbert"

def load_finbert():
    """Checks for local model, downloads if missing, and returns (tokenizer, model)."""
    if os.path.exists(LOCAL_MODEL_PATH):
        print(f"--- Loading FinGPT Sentiment Engine from LOCAL disk ({LOCAL_MODEL_PATH}) ---")
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(LOCAL_MODEL_PATH)
    else:
        print(f"--- Local model not found. Downloading {MODEL_NAME}... ---")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        
        os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)
        tokenizer.save_pretrained(LOCAL_MODEL_PATH)
        model.save_pretrained(LOCAL_MODEL_PATH)
        
    return tokenizer, model

# Global initialization
tokenizer, model = load_finbert()

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ['Positive', 'Negative', 'Neutral']
    return labels[torch.argmax(prediction)]

@app.get("/analyze")
async def analyze_fund(code: str = Query(..., description="The mfapi.in scheme code")):
    try:
        # 1. Fetch MF Data
        mf_url = f"https://api.mfapi.in/mf/{code}"
        mf_res = requests.get(mf_url).json()
        
        if not mf_res or 'meta' not in mf_res:
            return {"error": "Invalid Scheme Code or API Down"}

        # Initialize core variables to avoid NameErrors
        scheme_name = mf_res['meta'].get('scheme_name', 'Unknown Fund')
        nav = mf_res['data'][0]['nav']
        prev_nav = mf_res['data'][1]['nav']
        day_change = ((float(nav) - float(prev_nav)) / float(prev_nav)) * 100

        # 2. Fetch Market Sentiment using curl_cffi (Impersonating Chrome)
        curl_session = curl_requests.Session(impersonate="chrome")
        nifty = yf.Ticker("^NSEI", session=curl_session)
        raw_news = nifty.news if nifty.news else []
        
        analysis = []
        positive_count = 0
        
        # Process news
        for item in raw_news[:3]:
            # Handle both common yfinance news formats
            title = item.get('title') or item.get('content', {}).get('title', 'No Title Available')
            sent = get_sentiment(title)
            if sent == "Positive": 
                positive_count += 1
            analysis.append({"headline": title, "sentiment": sent})

        # 3. Strategy Logic (Correlation)
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
        print(f"Server Error: {str(e)}")
        # If any variables weren't defined due to early failure, we catch it here
        return {"error": "Processing Failed", "details": str(e)}

@app.get("/")
def health_check():
    return {
        "status": "FinGPT Server is active",
        "model_source": "Local" if os.path.exists(LOCAL_MODEL_PATH) else "Cloud",
        "host": os.getenv("SERVER_HOST", "0.0.0.0"),
        "port": os.getenv("SERVER_PORT", "8000")
    }