+---------------------------------------------------------------+

| Portfolio Dashboard |

+---------------------------+-----------------------------------+

| Advisor View | Client View |

|----------------------------|----------------------------------|

| [Pie Chart: Allocation] | [Simplified Pie Chart] |

| Equity 50%, Debt 30%, | Equity-heavy snapshot |

| Hybrid 15%, Liquid 5% | |

| | |

| [Line Chart: NAV Trends] | [Line Chart: NAV Trends] |

| HDFC Top 100, SBI Bluechip | Simple NAV growth view |

| Kotak Emerging Equity | |

| | |

| [Analytics Panel] | [Plain Language Summary] |

| - Sharpe ratio vs NIFTY | "Your portfolio is strong but |

| - Beta values | concentrated in domestic markets |

| - Sector heatmap | and corporate bonds. Add global |

| - Compliance alerts (SEBI) | equity, diversify debt, increase |

| | liquidity." |

| | |

| [LLM Insights] | [Actionable Recommendations] |

| - Risk exposure | - Reduce tech fund exposure |

| - Diversification gaps | - Add international equity fund |

| - Scenario simulations | - Diversify debt into dynamic |

| - Rebalancing strategies | bond funds |

| | - Increase liquid fund allocation|

+----------------------------+----------------------------------+

✅ How It Works

Advisor View → Technical depth: analytics, compliance, sector heatmaps.
Client View → Simplified visuals + easy-to-understand recommendations.
LLM Hybrid Setup → BloombergGPT/FinGPT for backend analytics, GPT‑5 for client-facing clarity.
Would you like me to expand this wireframe into a full dashboard mockup description (colors, layout style, UI elements) so you can imagine how it would look in a real wealth management app?

Great — let’s build a Python script that automatically generates a sample PDF client report using ReportLab (for PDF layout) and Matplotlib (for charts). This way, you’ll have a working example that produces the same portfolio analysis we’ve been designing.

🐍 Python Script: Generate Sample PDF Report

from reportlab.lib.pagesizes import A4

from reportlab.pdfgen import canvas

from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle

import matplotlib.pyplot as plt

# --- Step 1: Create charts with Matplotlib ---

def create_pie_chart():

labels = ['Equity', 'Debt', 'Hybrid', 'Liquid']

sizes = [50, 30, 15, 5]

colors_list = ['#0B3D91', '#28A745', '#FFD700', '#87CEEB']

plt.figure(figsize=(4,4))

plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list)

plt.title("Portfolio Allocation")

plt.savefig("pie_chart.png")

plt.close()

def create_line_chart():

months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

hdfc = [720, 730, 740, 750, 760, 770]

sbi = [65, 66, 67, 68, 69, 70]

kotak = [85, 87, 90, 92, 95, 97]

plt.figure(figsize=(6,4))

plt.plot(months, hdfc, label="HDFC Top 100")

plt.plot(months, sbi, label="SBI Bluechip")

plt.plot(months, kotak, label="Kotak Emerging Equity")

plt.plot(months, [700,710,720,730,740,750], label="NIFTY 50", linestyle="--")

plt.title("NAV Trends vs Benchmark")

plt.xlabel("Month")

plt.ylabel("NAV (₹)")

plt.legend()

plt.savefig("line_chart.png")

plt.close()

# --- Step 2: Generate PDF with ReportLab ---

def generate_pdf():

c = canvas.Canvas("Sample_Client_Report.pdf", pagesize=A4)

width, height = A4

# Cover Page

c.setFont("Helvetica-Bold", 20)

c.drawCentredString(width/2, height-100, "Mutual Fund Portfolio Analysis – Indian Market")

c.setFont("Helvetica", 12)

c.drawCentredString(width/2, height-130, "Client: Mr. A. Sharma | Date: Dec 18, 2025")

c.drawCentredString(width/2, height-150, "Advisor: WealthCare Advisory Pvt. Ltd.")

c.showPage()

# Portfolio Snapshot

c.setFont("Helvetica-Bold", 16)

c.drawString(50, height-50, "Portfolio Snapshot")

c.drawImage("pie_chart.png", 50, height-300, width=200, height=200)

data = [

["Fund Name", "Allocation %", "Latest NAV (₹)"],

["HDFC Top 100 Fund", "20%", "750.25"],

["SBI Bluechip Fund", "15%", "68.40"],

["Kotak Emerging Equity Fund", "10%", "92.15"],

["ICICI Tech Fund", "5%", "45.80"],

["Axis Short Term Fund", "15%", "22.10"],

["HDFC Corporate Bond Fund", "10%", "34.75"],

["SBI Magnum Gilt Fund", "5%", "19.60"],

["ICICI Balanced Advantage Fund", "15%", "78.90"],

["Nippon India Liquid Fund", "5%", "12.05"]

]

table = Table(data, colWidths=[200, 100, 100])

table.setStyle(TableStyle([

('BACKGROUND', (0,0), (-1,0), colors.lightblue),

('TEXTCOLOR',(0,0),(-1,0),colors.black),

('ALIGN',(0,0),(-1,-1),'CENTER'),

('GRID',(0,0),(-1,-1),0.5,colors.grey)

]))

table.wrapOn(c, width, height)

table.drawOn(c, 50, height-500)

c.showPage()

# Performance Trends

c.setFont("Helvetica-Bold", 16)

c.drawString(50, height-50, "Performance Trends")

c.drawImage("line_chart.png", 50, height-400, width=400, height=300)

c.showPage()

# Summary Page

c.setFont("Helvetica-Bold", 16)

c.drawString(50, height-50, "Client-Friendly Summary")

c.setFont("Helvetica", 12)

summary_text = (

"Your portfolio is strong in large-cap Indian equities but concentrated in domestic markets "

"and corporate bonds. To reduce risk, we suggest adding global equity exposure, diversifying "

"debt into dynamic bond funds, and increasing liquid fund allocation for emergencies."

)

c.drawString(50, height-100, summary_text)

c.showPage()

c.save()

# --- Run everything ---

create_pie_chart()

create_line_chart()

generate_pdf()

print("Sample_Client_Report.pdf generated successfully!")

✅ What This Script Does

Creates charts (pie chart for allocation, line chart for NAV trends).
Generates a PDF with:
Cover page
Portfolio snapshot (chart + table)
Performance trends (line chart vs benchmark)
Client-friendly summary
👉 To run it:

Install dependencies: pip install reportlab matplotlib
Save the script as report.py
Run: python report.py
You’ll get a file called Sample_Client_Report.pdf in your working directory.
Would you like me to extend this script so it also includes the Risk & Diversification Analysis and Rebalancing Suggestions pages with charts (heatmap + before/after allocation)?

Perfect — let’s extend the C# PDF generator so it includes the Risk & Diversification Analysis and Rebalancing Suggestions pages with additional charts. This will give you a more complete client report.

🖥️ Extended C# Code: Full Client Report

using System;

using System.IO;

using iTextSharp.text;

using iTextSharp.text.pdf;

using System.Windows.Forms.DataVisualization.Charting;

class PortfolioReport

{

static void Main()

{

string pdfPath = "Sample_Client_Report.pdf";

// Step 1: Create charts

CreatePieChart("pie_chart.png");

CreateLineChart("line_chart.png");

CreateHeatmapChart("heatmap.png");

CreateRebalanceCharts("before.png", "after.png");

// Step 2: Generate PDF

Document doc = new Document(PageSize.A4);

PdfWriter.GetInstance(doc, new FileStream(pdfPath, FileMode.Create));

doc.Open();

var titleFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 18);

var normalFont = FontFactory.GetFont(FontFactory.HELVETICA, 12);

// Cover Page

doc.Add(new Paragraph("Mutual Fund Portfolio Analysis – Indian Market", titleFont));

doc.Add(new Paragraph("Client: Mr. A. Sharma | Date: Dec 18, 2025", normalFont));

doc.Add(new Paragraph("Advisor: WealthCare Advisory Pvt. Ltd.", normalFont));

doc.NewPage();

// Portfolio Snapshot

doc.Add(new Paragraph("Portfolio Snapshot", titleFont));

iTextSharp.text.Image pieImg = iTextSharp.text.Image.GetInstance("pie_chart.png");

pieImg.ScaleToFit(250f, 250f);

doc.Add(pieImg);

doc.NewPage();

// Performance Trends

doc.Add(new Paragraph("Performance Trends", titleFont));

iTextSharp.text.Image lineImg = iTextSharp.text.Image.GetInstance("line_chart.png");

lineImg.ScaleToFit(400f, 300f);

doc.Add(lineImg);

doc.NewPage();

// Risk & Diversification

doc.Add(new Paragraph("Risk & Diversification Analysis", titleFont));

iTextSharp.text.Image heatmapImg = iTextSharp.text.Image.GetInstance("heatmap.png");

heatmapImg.ScaleToFit(400f, 300f);

doc.Add(heatmapImg);

doc.Add(new Paragraph("Insight: Portfolio concentrated in domestic equities and corporate bonds. No global diversification.", normalFont));

doc.NewPage();

// Rebalancing Suggestions

doc.Add(new Paragraph("Rebalancing Suggestions", titleFont));

iTextSharp.text.Image beforeImg = iTextSharp.text.Image.GetInstance("before.png");

beforeImg.ScaleToFit(200f, 200f);

iTextSharp.text.Image afterImg = iTextSharp.text.Image.GetInstance("after.png");

afterImg.ScaleToFit(200f, 200f);

PdfPTable rebalanceTable = new PdfPTable(2);

rebalanceTable.AddCell(new PdfPCell(beforeImg));

rebalanceTable.AddCell(new PdfPCell(afterImg));

doc.Add(rebalanceTable);

doc.Add(new Paragraph("✔ Reduce tech sectoral fund exposure\n" +

"🌍 Add international equity exposure\n" +

"↔ Diversify debt into dynamic bond funds\n" +

"💧 Increase liquid fund allocation\n" +

"📊 Maintain hybrid fund but monitor overlap", normalFont));

doc.NewPage();

// Summary

doc.Add(new Paragraph("Client-Friendly Summary", titleFont));

doc.Add(new Paragraph(

"Your portfolio is strong in large-cap Indian equities but concentrated in domestic markets " +

"and corporate bonds. To reduce risk, we suggest adding global equity exposure, diversifying " +

"debt into dynamic bond funds, and increasing liquid fund allocation for emergencies.",

normalFont));

doc.Close();

Console.WriteLine("PDF generated successfully at " + pdfPath);

}

// --- Chart Generators ---

static void CreatePieChart(string filename)

{

Chart chart = new Chart { Width = 400, Height = 400 };

chart.ChartAreas.Add(new ChartArea());

Series series = new Series { ChartType = SeriesChartType.Pie };

series.Points.AddXY("Equity", 50);

series.Points.AddXY("Debt", 30);

series.Points.AddXY("Hybrid", 15);

series.Points.AddXY("Liquid", 5);

chart.Series.Add(series);

chart.SaveImage(filename, ChartImageFormat.Png);

}

static void CreateLineChart(string filename)

{

Chart chart = new Chart { Width = 600, Height = 400 };

chart.ChartAreas.Add(new ChartArea());

Series hdfc = new Series("HDFC Top 100") { ChartType = SeriesChartType.Line };

hdfc.Points.AddXY("Jul", 720); hdfc.Points.AddXY("Aug", 730); hdfc.Points.AddXY("Sep", 740);

hdfc.Points.AddXY("Oct", 750); hdfc.Points.AddXY("Nov", 760); hdfc.Points.AddXY("Dec", 770);

chart.Series.Add(hdfc);

chart.SaveImage(filename, ChartImageFormat.Png);

}

static void CreateHeatmapChart(string filename)

{

Chart chart = new Chart { Width = 600, Height = 400 };

chart.ChartAreas.Add(new ChartArea());

Series series = new Series("Sector Exposure") { ChartType = SeriesChartType.Column };

series.Points.AddXY("Financials", 40);

series.Points.AddXY("FMCG", 25);

series.Points.AddXY("IT", 20);

series.Points.AddXY("Others", 15);

chart.Series.Add(series);

chart.SaveImage(filename, ChartImageFormat.Png);

}

static void CreateRebalanceCharts(string beforeFile, string afterFile)

{

Chart before = new Chart { Width = 400, Height = 400 };

before.ChartAreas.Add(new ChartArea());

Series s1 = new Series { ChartType = SeriesChartType.Pie };

s1.Points.AddXY("Equity", 50);

s1.Points.AddXY("Debt", 30);

s1.Points.AddXY("Hybrid", 15);

s1.Points.AddXY("Liquid", 5);

before.Series.Add(s1);

before.SaveImage(beforeFile, ChartImageFormat.Png);

Chart after = new Chart { Width = 400, Height = 400 };

after.ChartAreas.Add(new ChartArea());

Series s2 = new Series { ChartType = SeriesChartType.Pie };

s2.Points.AddXY("Equity", 47);

s2.Points.AddXY("Debt", 30);

s2.Points.AddXY("Hybrid", 13);

s2.Points.AddXY("Liquid", 10);

after.Series.Add(s2);

after.SaveImage(afterFile, ChartImageFormat.Png);

}

}

