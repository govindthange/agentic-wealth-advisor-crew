import requests
import yfinance as yf
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

# 1. SETUP FINGPT-ALIGNED SENTIMENT ENGINE
print("--- Loading FinGPT Sentiment Engine ---")
# Using FinBERT backbone - lightweight and highly accurate for finance
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def get_sentiment(text):
    if not text: return "Neutral"
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ['Positive', 'Negative', 'Neutral']
    return labels[torch.argmax(prediction)]

# 2. FETCH INDIAN MF DATA (mfapi.in)
def fetch_mf_data(scheme_code):
    print(f"--- Fetching NAV Data for Scheme: {scheme_code} ---")
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url).json()
    meta = response['meta']
    # Get latest two days to calculate change
    current_nav = response['data'][0]['nav']
    prev_nav = response['data'][1]['nav']
    change = ((float(current_nav) - float(prev_nav)) / float(prev_nav)) * 100
    return meta['scheme_name'], current_nav, change

# 3. FETCH MARKET NEWS (The 'Context')
def fetch_market_context():
    print("--- Fetching Nifty 50 Market News ---")
    nifty = yf.Ticker("^NSEI")
    raw_news = nifty.news
    
    refined_headlines = []
    for n in raw_news[:5]: # Take top 5 for better context
        # Check both old and new Yahoo Finance nested structures
        title = n.get('title') or n.get('content', {}).get('title')
        if title:
            refined_headlines.append(title)
            
    # Fallback if news is empty/unavailable
    if not refined_headlines:
        refined_headlines = ["Market showing standard volatility in Nifty 50 indices."]
        
    return refined_headlines

# 4. EXECUTE THE POC RELATION
def run_poc():
    try:
        # Example: Nippon India Small Cap Fund (118778)
        scheme_name, nav, day_change = fetch_mf_data("118778")
        headlines = fetch_market_context()
        
        print(f"\n[MF REPORT]: {scheme_name}")
        print(f"Latest NAV: ₹{nav} ({day_change:.2f}%)")
        print("-" * 30)
        print("[FINGPT ANALYSIS OF MARKET CONTEXT]:")
        
        sentiments = []
        for title in headlines:
            sentiment = get_sentiment(title)
            sentiments.append(sentiment)
            print(f" - Headline: {title}")
            print(f"   Sentiment: {sentiment}")

        # The "Production Relation" Logic
        pos = sentiments.count('Positive')
        neg = sentiments.count('Negative')
        
        if day_change < 0 and pos > neg:
            rec = "ACCUMULATE: NAV dip contradicts Bullish market news. Strong buying signal."
        elif day_change > 0 and neg > pos:
            rec = "CAUTION: NAV is up but Market Sentiment is turning Bearish. Possible correction."
        else:
            rec = "NEUTRAL: Fund performance is currently tracking with broader sentiment."

        print("-" * 30)
        print(f"STRATEGIC RECOMMENDATION: {rec}")
        
    except Exception as e:
        print(f"POC Error: {str(e)}")

if __name__ == "__main__":
    run_poc()