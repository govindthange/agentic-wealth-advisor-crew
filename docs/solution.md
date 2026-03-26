This is a sophisticated architecture that bridges traditional financial data ingestion with modern AI-driven analysis.

The diagram [here](./diagrams/aiml-wms-arch.drawio) maps out these three distinct stages: **Ingestion & ETL**, **Analytical Processing**, and **Output & Presentation**.

---

### Key Highlights of the Architecture:

* **Hybrid Storage:** A **MongoDB** instance for high-volume time-series NAV data, **Postgres** for relational user-portfolio data, and **Pinecone** for the vector embeddings extracted from AMC documents.
* **Decoupled Ingestion:** The AMFI scraping and MFCentral syncing are handled by dedicated microservices, ensuring that a delay in the AMFI portal doesn't break the user's ability to see their holdings.
* **Analytical Separation:**
* **ML Engine:** Focuses on the "Quantitative" (Random Forest, Sharpe ratios).
* **RAG Engine:** Focuses on the "Qualitative" (extracting sentiment from PDFs and providing context).


* **Persona-Based UI:** The output is split between a technical **Advisor Dashboard** and a user-friendly **Client Portal**, as requested.
