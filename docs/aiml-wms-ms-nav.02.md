The **NAV MS (Daily Scraper)** bridges the gap between "Raw Data Ingestion" and "Model Readiness." In this logic, the microservice doesn't just store data; it acts as a **Feature Factory** and a **Training Orchestrator**.

The flowchart [here](../diagrams/aiml-wms-ms-nav.02.drawio) illustrates the transition from the AMFI scrape to the **Random Forest Regressor**, including the validation loops and the output of prediction residuals used for identifying "off-track" funds.

### Logic Breakdown of the NAV MS Expansion

#### 1. Inputs and Pre-processing

* **The Ingestor:** Fetches 5 years of historical NAV files (as specified in Phase 2) using session-based requests to handle the bulk payload from AMFI.
* **The Guardrail:** A **Spike Detection** rhombus acts as a data-quality gate. It ensures that the Random Forest isn't trained on outliers caused by AMFI reporting errors or text-file corruption.

#### 2. The Feature Factory

Before training, the raw NAV is transformed into high-order features:

* **Rolling Volatility:** Standard deviation of returns over 30/90 day windows.
* **Sharpe/Treynor:** Risk-adjusted return metrics.
* **External Context:** The MS pulls "Expense Ratio" or "Exit Load" from the SQL DB via a cross-service join to use as independent variables in the model.

#### 3. Training Logic (Random Forest Regressor)

* **Validation:** Instead of standard K-Fold, it uses **TimeSeriesSplit**. This ensures that the model is always validated on a "chronological future" relative to the training set—vital for financial forecasting.
* **The "Refit" Cycle:** The model is refetched daily with the latest AMFI scrape to ensure the decision trees reflect current market regimes (e.g., high-interest-rate environments).

#### 4. Outputs and "Off-Track" Logic

* **The Residual Signal:** The primary output isn't just a predicted NAV, but the **Residual** ().
* **Interpretation:** If a fund's actual performance deviates significantly from the Random Forest's prediction based on historical features, the **Off-Track Tester** flags it.
* **Downstream Impact:** This signal is passed via **JSON** to the Output Stage, triggering a compliance alert or a "Rebalance Recommendation" on the Client Portal.
