# FinGPT Indian Mutual Fund Analyzer PoC

This project is a Proof of Concept (PoC) that demonstrates how to combine **Quantitative** financial data from the Indian Mutual Fund market with **Qualitative** AI-driven sentiment analysis using **FinGPT** logic.

## 🏗️ Architecture Logic

The system follows a three-step pipeline to generate an investment recommendation:

1.  **Data Ingestion (mfapi.in):** The server fetches real-time Net Asset Value (NAV) for a specific fund. It calculates the `day_change_pct` to determine if the fund's price is currently dipping or rising.
    
2.  **Contextual Intelligence (Yahoo Finance + FinBERT):** Standard LLMs are "static." To provide live context, the server scrapes the latest news headlines related to the **Nifty 50 (^NSEI)**. It then passes these through a **FinBERT** model (a specialized financial NLP model aligned with FinGPT principles) to categorize the market mood as Positive, Negative, or Neutral.

3.  **Strategic Correlation (The Bridge):** The "magic" happens here. Instead of just showing numbers, the server correlates the two:
    - **NAV Down + Positive Sentiment** = **Accumulate** (Buying opportunity).
    - **NAV Up + Negative Sentiment** = **Caution** (Potential reversal).
    - **Aligned Signals** = **Neutral/Hold**.

## 🛠️ Deployment Instructions

### Prerequisites
- Docker and Docker Compose installed.

### Start the Server
Run the following command in the project directory:
```bash
docker compose up --build
```

---

# 🧠 Core Implementation Logic

The `server.py` file operates as a stateful inference server. Unlike a script, it loads the heavy AI model into memory once and exposes an API for instant analysis.

### 1. The Intelligence Layer (FinGPT/FinBERT)
At startup, the server initializes `ProsusAI/finbert`. 
- **Model Choice:** While FinGPT models are large, FinBERT provides the optimized "Backbone" for sentiment.
- **NLP Pipeline:** The `get_sentiment()` function tokenizes raw text and converts it into a probability tensor. It maps these to `Positive`, `Negative`, or `Neutral`.

### 2. The Quantitative Layer (mfapi.in)
When a request is received, the server calls the `mfapi.in` REST API.
- **NAV Extraction:** It fetches the two most recent data points.
- **Price Action Calculation:** It computes the percentage change between the latest and previous NAV:
  $$Change\% = \frac{Current NAV - Previous NAV}{Previous NAV} \times 100$$

### 3. The Contextual Layer (Nifty 50 News)
To understand *why* the market is moving, the server uses `yfinance` to grab the latest 3 headlines for the **Nifty 50 Index (^NSEI)**. This simulates a real-world scenario where fund performance is judged against macro-economic news.

### 4. The Recommendation Engine (The Bridge)
The system applies a logic matrix to correlate data:
| Price Action | Market Sentiment | Recommendation | Logic |
| :--- | :--- | :--- | :--- |
| **Negative (-)** | **Positive (+)** | **ACCUMULATE** | Market is bullish, but fund is cheap. Buying opportunity. |
| **Positive (+)** | **Negative (-)** | **CAUTION** | Fund is rising despite bad news. Potential correction. |
| **Neutral** | **Any** | **NEUTRAL** | No strong divergence detected. |

---

## 🧪 Testing and Parameter Discovery

To test different funds, you need the **Scheme Code**. You can discover these using the following methods.

### 1. Finding a Scheme Code (Discovery)

#### A. Search for a specific AMC (e.g., HDFC, SBI, ICICI)
Use the search endpoint to find the `schemeCode` for a specific fund name:
- **URL:** `https://api.mfapi.in/mf/search?q=HDFC`
- **Steps:** 1. Open the URL in your browser.
    2. Look for the `"schemeCode"` key (e.g., `119063`).
    3. Use this code in your local server query.

#### B. Browse the Full Master List
If you want to see all available funds in the Indian market:
- **URL:** `https://api.mfapi.in/mf`
- **Usage:** This returns a massive JSON array. Use `Ctrl+F` to search for your preferred fund name and copy the code.

### 2. Running the Analysis (Testing the PoC)

Once you have a code, you can test the server using **Query String Parameters**. The parameter `code` is passed in the URL after a `?`.

#### Method A: Using a Web Browser
Simply enter the following URLs in your address bar:
- **Test HDFC:** `http://localhost:8000/analyze?code=119063`
- **Test Quant:** `http://localhost:8000/analyze?code=120828`

#### Method B: Using Terminal (cURL)
Open your terminal and run:
```bash
curl "http://localhost:8000/analyze?code=118778"
```

## Testing within Docker Container

### Step 1. Connect to the container

```bash
docker exec -it fingpt_mf_server  /bin/bash
```

### Step 2. Run the app

```bash
python app.py
```

### Step 3. Check the output

```
root@thinkpad:/app# python app.py
--- Loading FinGPT Sentiment Engine ---
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 201/201 [00:00<00:00, 42653.94it/s]
BertForSequenceClassification LOAD REPORT from: ProsusAI/finbert
Key                          | Status     |  | 
-----------------------------+------------+--+-
bert.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.
--- Fetching NAV Data for Scheme: 118778 ---
--- Fetching Nifty 50 Market News ---

[MF REPORT]: Nippon India Small Cap Fund - Direct Plan Growth Plan - Growth Option
Latest NAV: ₹171.34850 (-0.05%)
------------------------------
[FINGPT ANALYSIS OF MARKET CONTEXT]:
 - Headline: Trending tickers: Datavault, Novo Nordisk, FedEx, SBI and NatWest
   Sentiment: Neutral
 - Headline: India might be the 'perfect' emerging market, strategist says
   Sentiment: Positive
 - Headline: Analysts' top emerging market fund and trust picks
   Sentiment: Neutral
 - Headline: London Stock Exchange open to dual listing of Indian companies, says LSEG boss
   Sentiment: Neutral
 - Headline: Bernstein says India could benefit if US recession hits
   Sentiment: Positive
------------------------------
STRATEGIC RECOMMENDATION: ACCUMULATE: NAV dip contradicts Bullish market news. Strong buying signal.
root@thinkpad:/app# exit
exit
```

---
