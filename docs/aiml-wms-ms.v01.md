This second `.drawio` file shifts from a high-level architecture to a granular **internal process flow**. I have expanded each microservice into a dedicated swimlane to visualize the logic, data transformations, and specific API interactions.

### Detailed Internal Logic .drawio Code

Copy this code, save it as `Microservice_Internals.drawio`, and import it into **[app.diagrams.net](https://app.diagrams.net)**.

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="internal_logic" name="Microservice Deep Dive">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="lane1" value="AMC SCHEME MS (FinGPT/OCR)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;startSize=30;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="340" height="740" as="geometry" />
        </mxCell>
        <mxCell id="a1" value="Input: PDF Factsheets&#10;(Monthly/SID)" style="shape=note;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane1">
          <mxGeometry x="100" y="50" width="140" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a2" value="PyMuPDF / OCR Extraction&#10;(Text + Table Parsing)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane1">
          <mxGeometry x="90" y="150" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a3" value="FinGPT Prompting:&#10;Extract Sector Exposure &amp; Risk" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane1">
          <mxGeometry x="90" y="250" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a4" value="Chunking &amp; Text-to-Vector&#10;(OpenAI Embeddings)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane1">
          <mxGeometry x="90" y="350" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a5" value="API Call: gRPC Upsert&#10;Target: Pinecone" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="lane1">
          <mxGeometry x="85" y="450" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a6" value="Vector Store&#10;(Metadata: SchemeID)" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="lane1">
          <mxGeometry x="130" y="550" width="80" height="80" as="geometry" />
        </mxCell>

        <mxCell id="lane2" value="NAV MS (DAILY SCRAPER)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#d5e8d4;startSize=30;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="410" y="40" width="340" height="740" as="geometry" />
        </mxCell>
        <mxCell id="b1" value="Trigger: Cron Job&#10;(Daily 9:00 PM IST)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane2">
          <mxGeometry x="100" y="50" width="140" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b2" value="API Call: HTTP GET&#10;Source: amfiindia.com" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#fff2cc;" vertex="1" parent="lane2">
          <mxGeometry x="85" y="150" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b3" value="Validation: Spike Detection&#10;(Current vs Prev NAV)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane2">
          <mxGeometry x="110" y="250" width="120" height="100" as="geometry" />
        </mxCell>
        <mxCell id="b4" value="Rolling Feature Calculation&#10;(Volatility/Sharpe)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane2">
          <mxGeometry x="90" y="390" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b5" value="Bulk Insert: NoSQL Driver&#10;Format: BSON/JSON" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="lane2">
          <mxGeometry x="85" y="490" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b6" value="MongoDB&#10;(Time-Series Collection)" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="lane2">
          <mxGeometry x="130" y="590" width="80" height="80" as="geometry" />
        </mxCell>

        <mxCell id="lane3" value="MFCENTRAL SYNC MS (JWT/OTP)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fff2cc;startSize=30;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="780" y="40" width="340" height="740" as="geometry" />
        </mxCell>
        <mxCell id="c1" value="Trigger: Client Consent&#10;(User PAN + OTP)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane3">
          <mxGeometry x="100" y="50" width="140" height="60" as="geometry" />
        </mxCell>
        <mxCell id="c2" value="API Call: POST /auth&#10;Protocol: REST (JSON)" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#f8cecc;" vertex="1" parent="lane3">
          <mxGeometry x="85" y="150" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="c3" value="Secure Store: JWT Token&#10;(Redis/Session)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane3">
          <mxGeometry x="100" y="250" width="140" height="60" as="geometry" />
        </mxCell>
        <mxCell id="c4" value="API Call: GET /cas_fetch&#10;Header: Bearer JWT" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#f8cecc;" vertex="1" parent="lane3">
          <mxGeometry x="85" y="350" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="c5" value="Data Normalization:&#10;Map Folios to AMFI Codes" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;" vertex="1" parent="lane3">
          <mxGeometry x="100" y="450" width="140" height="60" as="geometry" />
        </mxCell>
        <mxCell id="c6" value="JDBC Write: SQL DB&#10;(User Assets)" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="lane3">
          <mxGeometry x="130" y="550" width="80" height="80" as="geometry" />
        </mxCell>

        <mxCell id="e1" edge="1" parent="1" source="a1" target="a2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="a2" target="a3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3" edge="1" parent="1" source="a3" target="a4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4" edge="1" parent="1" source="a4" target="a5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="a5" target="a6"><mxGeometry relative="1" as="geometry" /></mxCell>
        
        <mxCell id="e6" edge="1" parent="1" source="b1" target="b2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e7" edge="1" parent="1" source="b2" target="b3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e8" edge="1" parent="1" source="b3" target="b4" value="Valid"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e9" edge="1" parent="1" source="b4" target="b5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e10" edge="1" parent="1" source="b5" target="b6"><mxGeometry relative="1" as="geometry" /></mxCell>
        
        <mxCell id="e11" edge="1" parent="1" source="c1" target="c2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e12" edge="1" parent="1" source="c2" target="c3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e13" edge="1" parent="1" source="c3" target="c4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e14" edge="1" parent="1" source="c4" target="c5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e15" edge="1" parent="1" source="c5" target="c6"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

```

---

### Internal Process Highlights

#### 1. AMC Scheme MS: Unstructured-to-Vector

* **OCR Stage:** Because factsheets are often image-heavy PDFs, we use PyMuPDF or Amazon Textract to ensure tables (sector weightings) are accurately parsed.
* **FinGPT Prompting:** The text isn't just stored; it's passed through FinGPT with a specific prompt: *"Identify sectoral risks and credit quality trends for [Fund Name]"*.
* **Vectorization:** The resulting qualitative summary is turned into an embedding (e.g., `text-embedding-3-small`) and pushed via **gRPC** to Pinecone for sub-millisecond retrieval during RAG.

#### 2. NAV MS: High-Performance Pipeline

* **Spike Detection:** A critical "if/then" logic branch. If the NAV fluctuates by more than a set threshold (e.g., 20% in 24 hours), the process halts and triggers an alert, preventing the **Random Forest** from being trained on bad data.
* **Feature Engineering:** Before database insertion, the service calculates rolling 30/90-day volatility and Sharpe ratios as pre-computed features for the ML layer.
* **Bulk Driver:** Uses the MongoDB native driver to perform batch inserts, minimizing connection overhead.

#### 3. MFCentral Sync MS: JWT/OTP Handshake

* **Auth Flow:** The process begins with a POST request to MFCentral’s `/auth` endpoint. The service manages the short-lived session by storing the **JWT** in an internal Redis cache or secure session store.
* **Data Fetch:** The `/cas_fetch` call retrieves the Consolidated Account Statement.
* **Normalization:** The most complex internal step—mapping MFCentral's scheme names to the standardized AMFI codes. This ensures that the portfolio holdings can be correctly joined with the historical NAV data in the SQL DB.

