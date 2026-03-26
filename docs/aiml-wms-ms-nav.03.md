To move the **Random Forest Regressor (RFR)** from a training experiment to a production-ready component, we must treat it as an active inference service. In production, the model acts as a "benchmark generator" to determine if a fund is behaving according to its historical risk-reward profile or if it has gone "off-track."

### How the Model is Used in Production

Once the model is trained on the 5-year historical AMFI data, it is serialized (e.g., as a `.joblib` or `.pkl` file) and loaded into an inference pipeline.

1. **Production Input (The Feature Vector):** To generate a prediction for "Today," the model doesn't just need the price. It expects a **Current State Vector** consisting of:
* **Rolling Stats:** Volatility, Sharpe, and Sortino ratios calculated over the *last* 30, 90, and 180 days.
* **Benchmark Context:** Current NIFTY 50 or SENSEX performance.
* **Static Metadata:** Expense ratio and fund category (Large Cap, Mid Cap, etc.).


2. **Inference:** The model takes this vector and outputs a **Predicted NAV**.
3. **The "Off-Track" Logic:** We compare the **Actual NAV** (from the daily AMFI scrape) with the **Predicted NAV**.
* If  (beyond a 2-sigma threshold), the fund is flagged as **underperforming** relative to its historical risk profile.
* If , we check the **RAG Engine** to see if this is "Alpha" (good) or "Style Drift" (risky).



---

### Revised NAV MS Internal Flowchart

This version includes the **Model Registry** (for production deployment) and the **Inference Loop**.

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="nav_ms_production" name="Production NAV MS">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="s1" value="INGESTION &amp; FEATURE FACTORY" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="300" height="740" as="geometry" />
        </mxCell>
        <mxCell id="a1" value="Daily AMFI Scrape&#10;(Current NAV)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;" vertex="1" parent="s1">
          <mxGeometry x="75" y="50" width="150" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a2" value="Feature Engineering:&#10;Map Rolling Volatility,&#10;Sharpe, and Momentum" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;" vertex="1" parent="s1">
          <mxGeometry x="75" y="160" width="150" height="80" as="geometry" />
        </mxCell>
        <mxCell id="a3" value="Construct State Vector&#10;[X1, X2... Xn]" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#d5e8d4;" vertex="1" parent="s1">
          <mxGeometry x="65" y="290" width="170" height="60" as="geometry" />
        </mxCell>

        <mxCell id="s2" value="MODEL OPS (TRAINING &amp; INFERENCE)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;" vertex="1" parent="1">
          <mxGeometry x="340" y="40" width="400" height="740" as="geometry" />
        </mxCell>
        <mxCell id="b1" value="Model Registry&#10;(Loaded .joblib RF Model)" style="shape=dataStorage;whiteSpace=wrap;html=1;fillColor=#e1d5e7;" vertex="1" parent="s2">
          <mxGeometry x="125" y="50" width="150" height="80" as="geometry" />
        </mxCell>
        <mxCell id="b2" value="INFERENCE ENGINE:&#10;RF_Model.predict(StateVector)" style="shape=process;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1" vertex="1" parent="s2">
          <mxGeometry x="100" y="180" width="200" height="70" as="geometry" />
        </mxCell>
        <mxCell id="b3" value="Calculate Residual:&#10;Delta = Actual - Predicted" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="s2">
          <mxGeometry x="100" y="300" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b4" value="Retraining Loop:&#10;TimeSeriesSplit Refit&#10;(Weekly/Monthly)" style="rounded=1;whiteSpace=wrap;html=1;dashed=1;" vertex="1" parent="s2">
          <mxGeometry x="100" y="450" width="200" height="70" as="geometry" />
        </mxCell>

        <mxCell id="s3" value="DECISION &amp; ALERTING" style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;" vertex="1" parent="1">
          <mxGeometry x="740" y="40" width="300" height="740" as="geometry" />
        </mxCell>
        <mxCell id="c1" value="Delta &gt; Threshold?&#10;(Significant Drift)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;" vertex="1" parent="s3">
          <mxGeometry x="85" y="280" width="130" height="100" as="geometry" />
        </mxCell>
        <mxCell id="c2" value="Output: JSON Alert to&#10;Advisor Dashboard" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#dae8fc;" vertex="1" parent="s3">
          <mxGeometry x="65" y="450" width="170" height="60" as="geometry" />
        </mxCell>

        <mxCell id="e1" edge="1" parent="1" source="a1" target="a2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="a2" target="a3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3" value="Input Vector" edge="1" parent="1" source="a3" target="b2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4" value="Load Model" edge="1" parent="1" source="b1" target="b2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="b2" target="b3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e6" value="Actual NAV" edge="1" parent="1" source="a1" target="b3" style="edgeStyle=orthogonalEdgeStyle;curved=1;"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e7" edge="1" parent="1" source="b3" target="c1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e8" value="Yes" edge="1" parent="1" source="c1" target="c2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e9" value="New Training Data" edge="1" parent="1" source="a2" target="b4" style="edgeStyle=orthogonalEdgeStyle;curved=1;"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e10" value="Update Model" edge="1" parent="1" source="b4" target="b1" style="edgeStyle=orthogonalEdgeStyle;curved=1;dashed=1;"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

```

### Summary of Production Inputs:

To get a prediction from the model in the production environment, the `NAV MS` must pass a JSON payload that looks like this:

```json
{
  "fund_id": "120344",
  "state_vector": {
    "volatility_30d": 0.12,
    "sharpe_ratio": 1.45,
    "category_average_return": 0.08,
    "expense_ratio": 0.0075,
    "benchmark_correlation": 0.89
  }
}

```
