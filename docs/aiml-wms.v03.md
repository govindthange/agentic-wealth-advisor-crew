### Technical Breakdown: APIs and Protocols

#### 1. MFCentral Microservice (JWT Flow)

The communication with MFCentral follows a secure **JWT-based Bearer Token** flow over HTTPS.

* **Step A (Consent):** User triggers an OTP request via the Client Portal.
* **Step B (Auth):** The MS calls MFCentral with the OTP. If valid, MFCentral returns a JWT.
* **Step C (Data Fetch):** Subsequent requests use the JWT in the Authorization Header.

**API Example:**

```http
GET /api/v1/portfolio/sync
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

Response:
{
  "pan": "ABCDE1234F",
  "holdings": [
    { "scheme_name": "Quant Small Cap", "units": 450.25, "folio": "9102345/0" }
  ]
}

```

#### 2. AMC Scheme Construction MS (Qualitative Data)

This service handles unstructured PDF ingestion from various AMC websites (HDFC, SBI, etc.).

* **Extraction:** Uses an LLM (like GPT-4o or Claude) to parse PDFs and identify **Qualitative Risks** (e.g., "high churn rate," "credit downgrade of underlying bond").
* **Storage:** These text chunks are converted into vectors and stored in **Pinecone**.

**API Example:**

```http
POST /api/v1/scheme/extract
{
  "source_url": "https://www.hdfcfund.com/factsheet.pdf",
  "fund_house": "HDFC"
}

Internal Pipeline: PDF -> OCR -> LLM Parsing -> Vectorization -> Pinecone

```

#### 3. AMFI NAV MS (High-Performance Ingestion)

This service utilizes session-based requests to scrape the daily text files from AMFI.

* **Batching:** Instead of one-by-one inserts, it uses `bulkWrite()` in MongoDB to handle the 15,000+ daily price points efficiently.
* **Validation:** It performs a "delta check" against the previous day's NAV. If a price jumps >20% (possible data error), it flags a compliance alert.

**Would you like me to provide the specific MongoDB schema for the Time-Series NAV data or a sample LLM prompt used for the AMC PDF extraction?**

### Logic Integration Breakdown

* **Ingestion (Scheme & NAV):** I’ve represented the Factsheets as a primary input to the **AMC Scheme MS**, where OCR and FinGPT process them for the Vector DB. The 5-year NAV data flows into the **NAV Microservice** for feature engineering.
* **The ML Training Loop:** Inside the Analytical Stage, the **ML Engine** specifically notes the use of **TimeSeriesSplit** for validation—critical for financial data to prevent data leakage from the "future" into the "past."
* **The Scenario Simulator:** Below the RAG engine, I added a "Tester" component that injects interest rate and sector correction simulations. This is where the "off-track" identification logic lives.
* **Expert-in-the-loop:** The **Output Stage** doesn't just display data; it flows through a **GPT-5 Summary Engine**, into a **PDF Generator**, and then into an **Expert Analyst Scoring** node to ensure regulatory compliance before reaching the final UI.

**Would you like me to detail the specific data schema for the "Expert Scoring" feedback loop to show how it retrains the GPT-5 summary prompts?**


### Protocol and Connection Details:

1. **MFCentral to SQL DB (JDBC):** The Portfolio MS now correctly persists the retrieved Consolidated Account Statement (CAS) data into the SQL DB using standard **JDBC** or an ORM (like SQLAlchemy/Sequelize).
2. **SQL DB to UI (JDBC/REST):** A direct line is established to the UI layer to ensure that user-specific folio details are available for display without passing through the heavy AI engines.
3. **Tester Component (Internal):** The Off-track Logic Tester pulls actual user holdings from the **SQL DB** and historical volatility from the **Analytical Engines** to run the sector correction simulations.
4. **JWT/REST Flow:** The connection between the MFCentral API and its microservice is explicitly labeled **REST/JWT**, highlighting the secure handshake required for fetching PAN-based data.
5. **Scraping vs. Vectors:** The **NAV MS** uses **HTTPS Scraping** for AMFI, while the **Scheme MS** utilizes **gRPC** or specialized Vector client protocols for high-speed embedding storage in Pinecone.
