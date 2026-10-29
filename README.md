# Enterprise Retail Sales Data Analytics Project
### End-to-End Commercial Portfolio: Python • SQL • Excel • Power BI

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Database SQLite](https://img.shields.io/badge/Database-SQLite%203-003B57.svg)](https://www.sqlite.org/)
[![Excel Model](https://img.shields.io/badge/Excel-openpyxl%20%26%20Formulas-217346.svg)](https://www.microsoft.com/en-us/microsoft-369/excel)
[![Power BI Desktop](https://img.shields.io/badge/Power%20BI-Star%20Schema%20%26%20DAX-F2C811.svg)](https://powerbi.microsoft.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 1. Executive Summary & Business Problem

**Global Retail Corp** is a nationwide multi-category commercial enterprise operating across four major US geographic regions (**West**, **Central**, **South**, and **East**). The company markets products across three core categories: **Technology**, **Furniture**, and **Office Supplies**, catering to **Consumer**, **Corporate**, and **Home Office** customer segments.

While the enterprise achieved **$9,612,134.87** in gross net sales across **10,000 orders** (10,039 transactions) between 2023 and 2026, leadership identified a critical operational dilemma: **operating profit margin was depressed at 12.49%**, significantly trailing the corporate benchmark of 15.00%.

### Core Business Questions Addressed
1. **Sales & Profitability Trends**: How have revenue and net margins trended month-over-month, and what seasonality patterns emerge during Q4 retail surges?
2. **Product Profitability & Loss Bleed**: Which categories and subcategories drive enterprise cash flow, and which product lines operate as chronic loss-makers?
3. **Discount Elasticity & Thresholds**: At what specific discount rate does transaction profitability collapse into negative margin territory?
4. **Regional Opportunity & Disparities**: Which geographic territories yield the highest sales volume versus highest profit margin efficiency?
5. **Customer Segment Economics**: How do Consumer, Corporate, and Home Office segments compare in Average Order Value (AOV), purchase frequency, and margin contribution?
6. **Executive Action Plan**: What specific, quantified commercial policy changes will eliminate margin erosion and reclaim lost EBITDA?

---

## 2. Standardized Metric Consistency Matrix

To prevent data discrepancies across tools, identical mathematical definitions are enforced across Python, SQL, Excel, and Power BI:

| Metric Name | Business Definition | Formula / Implementation | Python (Pandas) | SQL (SQLite) | Excel Formula | Power BI DAX |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gross Sales** | Total invoiced transaction revenue after item discount | $\sum \text{Sales}$ | `df['Sales'].sum()` | `SUM(Sales)` | `=SUM(Q2:Q10040)` | `SUM(fact_sales[Sales])` |
| **Gross Profit** | Bottom-line profit realized after COGS and freight | $\sum \text{Profit}$ | `df['Profit'].sum()` | `SUM(Profit)` | `=SUM(T2:T10040)` | `SUM(fact_sales[Profit])` |
| **Profit Margin %** | Net profit percentage realized on sales | $\frac{\sum \text{Profit}}{\sum \text{Sales}} \times 100$ | `Profit.sum()/Sales.sum()` | `ROUND((SUM(Profit)/SUM(Sales))*100, 2)`| `=E6/B6` | `DIVIDE([Total Profit], [Total Sales], 0)` |
| **Order Volume** | Total distinct customer purchase orders | $\text{Distinct}(Order\_ID)$ | `df['Order_ID'].nunique()` | `COUNT(DISTINCT Order_ID)` | `=COUNT('Cleaned Data'!A2:A10040)` | `DISTINCTCOUNT(fact_sales[Order_ID])` |
| **Average Order Value (AOV)** | Average sales ticket per discrete order | $\frac{\sum \text{Sales}}{\text{Distinct}(Order\_ID)}$ | `Sales.sum()/Order_ID.nunique()` | `SUM(Sales)/COUNT(DISTINCT Order_ID)` | `=B6/K6` | `DIVIDE([Total Sales], [Total Orders], 0)` |
| **Fulfillment Lead Time** | Elapsed days between order placement and shipping | $\text{Ship\_Date} - \text{Order\_Date}$ | `(Ship - Order).dt.days` | `JULIANDAY(Ship) - JULIANDAY(Order)` | `=AVERAGE(AC2:AC10040)` | `AVERAGE(fact_sales[Order_to_Ship_Days])` |

---

## 3. Project Architecture & Repository Structure

```
retail_sales_analytics/
├── README.md                                 # Master documentation and executive portfolio
├── run_pipeline.py                           # Master 1-click end-to-end pipeline runner
├── requirements.txt                          # Python dependencies list
│
├── data/
│   ├── raw/
│   │   └── retail_sales_raw.csv              # Raw transactions with real-world imperfections (10,150 rows)
│   ├── processed/
│   │   └── retail_sales_clean.csv            # Sanitized, deduplicated, enriched dataset (10,039 rows)
│   └── data_dictionary.md                   # Full attribute definitions, constraints & limitations
│
├── src/
│   ├── generate_raw_data.py                  # Synthesizes realistic 4-year retail dataset with anomalies
│   ├── data_cleaning.py                      # Cleans nulls, duplicates, currency strings & engineers features
│   ├── eda_analysis.py                       # Generates 5 high-resolution analytical figures
│   ├── database_setup.py                     # Initializes SQLite DB and populates Star Schema tables
│   ├── run_sql_queries.py                    # Executes analytical query suite and exports markdown tables
│   └── generate_excel_workbook.py            # Builds multi-tab formatted Excel financial model (.xlsx)
│
├── sql/
│   ├── 01_schema_setup.sql                   # Star Schema DDL, table indexes, and analytical view
│   ├── 02_revenue_profit_trends.sql          # Time-series, MoM growth (LAG), and 3-month moving averages
│   ├── 03_product_performance.sql            # Category & subcategory profitability, loss drag, SKU rankings
│   ├── 04_regional_analysis.sql              # Regional performance, state rankings (DENSE_RANK), shipping SLAs
│   ├── 05_customer_segmentation.sql          # Unit economics, RFM customer tiers, and VIP account analysis
│   └── 06_discount_impact_analysis.sql       # Discount elasticity tiers and EBITDA margin recovery analysis
│
├── database/
│   └── retail_sales.db                       # Relational SQLite database file
│
├── excel/
│   └── Retail_Sales_Analysis.xlsx            # Multi-tab executive workbook with formulas and styled pivots
│
├── power_bi/
│   ├── README_power_bi.md                    # Step-by-step assembly tutorial for Power BI Desktop
│   ├── dax_measures.dax                      # 25+ production DAX formulas (Time Intelligence, KPIs, Filters)
│   ├── data_model_architecture.md            # Star schema diagram, 1:N cardinality, Date Table DAX
│   ├── report_layout_and_visuals.md          # 3-Page visual wireframes and layout design guide
│   └── dashboard_mockup.html                 # Interactive responsive HTML5 dashboard browser preview
│
└── reports/
    ├── figures/                              # High-resolution charts (Matplotlib & Seaborn)
    │   ├── 01_monthly_sales_profit_trend.png
    │   ├── 02_category_subcategory_profit.png
    │   ├── 03_discount_vs_profit_margin.png
    │   ├── 04_regional_performance.png
    │   └── 05_customer_segment_distribution.png
    ├── sql_results_summary.md                # Markdown tabular output of all executed SQL queries
    └── executive_insights_and_recommendations.md # C-suite strategic findings, pro-forma upside & roadmap
```

---

## 4. Setup & Quickstart Guide

### Prerequisites
- Python 3.10+ (Anaconda Python 3.12 recommended)
- Required packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `openpyxl`, `sqlite3`

### Run Complete End-to-End Pipeline in One Command
To execute data generation, cleaning, chart rendering, database ETL, SQL query execution, and Excel model compilation in ~30 seconds:

```powershell
# From the project directory:
python run_pipeline.py
```

### Run Modular Components Individually
```powershell
# 1. Clean raw transactions
python src/data_cleaning.py

# 2. Render EDA figures
python src/eda_analysis.py

# 3. Rebuild SQLite database & star schema
python src/database_setup.py

# 4. Execute SQL queries & update reports/sql_results_summary.md
python src/run_sql_queries.py

# 5. Compile Excel financial workbook
python src/generate_excel_workbook.py
```

---

## 5. Summary of Analysis Stages

### Stage 1: Python Data Cleaning & Feature Engineering
- **Raw Anomalies Handled**: Removed 111 duplicate lines; standardized text casing in Categories and Cities; stripped whitespace; parsed string-formatted currency (`$1,234.50`); resolved 203 missing Postal Codes via geographic state-city lookup; resolved date formatting variations.
- **Engineered Features**: `Profit_Margin`, `Unit_Price`, `Order_Year`, `Order_Quarter`, `Order_Month`, `Order_Month_Year`, `Order_Day_Name`, `Order_to_Ship_Days`, and `Discount_Tier`.
- **EDA Visualizations**:
  - `01_monthly_sales_profit_trend.png`: Visualizes monthly sales & profit time-series demonstrating consistent Q4 volume peaks.
  - `02_category_subcategory_profit.png`: Horizontal diverging bar chart highlighting Copiers (+$1.14M profit) vs. Tables (-$296.1K loss).
  - `03_discount_vs_profit_margin.png`: Box plot highlighting margin collapse beyond 20% discount.
  - `04_regional_performance.png`: Clustered bar chart of regional revenue vs. profit margin.
  - `05_customer_segment_distribution.png`: Donut chart of revenue share and AOV comparison.

### Stage 2: Relational SQL Querying (SQLite)
The database was modeled into a relational **Star Schema** (`fact_sales`, `dim_customer`, `dim_product`, `dim_geography`, `dim_date`) with index optimization.
- **Window Functions Used**:
  - `LAG() OVER (ORDER BY Order_Month_Year)` for Month-over-Month (MoM) Sales & Profit growth.
  - `AVG() OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` for 3-Month Moving Average.
  - `DENSE_RANK() OVER (ORDER BY SUM(Sales) DESC)` for State-level revenue rankings.
  - `SUM() OVER (ORDER BY Order_Month_Year)` for cumulative running totals.
- **Tabular Query Results**: Fully compiled in [sql_results_summary.md](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/reports/sql_results_summary.md).

### Stage 3: Excel Financial & Operational Model (`Retail_Sales_Analysis.xlsx`)
A multi-tab financial model built with `openpyxl`:
1. **Executive Summary**: High-level KPI cards with dynamic `=SUM()` and `=COUNT()` formulas, key findings callouts, and category performance summary.
2. **Cleaned Data**: Formatted table of all 10,039 records with currency, percentage, and date number formats.
3. **Pivot_Monthly_Trends**: Monthly breakdown powered by dynamic `=SUMIFS()` and calculated MoM growth rates.
4. **Pivot_Product_Performance**: Category and subcategory matrix with `=IF()` status flags distinguishing "STAR PERFORMER" from "LOSS MAKER".
5. **Pivot_Regional_Analysis**: Regional sales distribution, margin %, and average shipping delay via `=AVERAGEIF()`.
6. **Customer_Segments**: Segment economics, units purchased, and Average Order Value.

### Stage 4: Power BI Interactive Dashboard
- **Star Schema Data Model**: Documented in [data_model_architecture.md](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/data_model_architecture.md).
- **Custom DAX Library**: 25+ formulas in [dax_measures.dax](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/dax_measures.dax) covering Core KPIs, Time Intelligence (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`), and Loss Bleed calculations.
- **3-Page Report Design**: Wireframes and visual rules documented in [report_layout_and_visuals.md](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/report_layout_and_visuals.md).
- **Live Browser Dashboard**: Open [dashboard_mockup.html](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/dashboard_mockup.html) in any browser to interact with live charts, slicers, and KPI cards.

---

## 6. Key Empirical Findings & Business Impact

| Key Analytical Finding | Empirical Evidence from Dataset | Direct Business Impact | Practical Recommendation |
| :--- | :--- | :--- | :--- |
| **1. Margin Collapse Beyond 20% Discount** | Discounts $>20\%$ experience an average margin of **-8.91% to -38.53%**. 1,585 lines generated **-$253,959 in losses**. | Direct erosion of firm operating margin by **2.64%**. | **Enforce hard discount cap at 20%** in ERP/Salesforce. Reclaims **+$253,959.00 EBITDA**. |
| **2. Severe Profit Drag in Furniture** | Tables (-$296.1K) and Bookcases (-$76.7K) incurred **-$372,783 in cumulative losses**. | Unprofitable freight absorption turns heavy furniture negative. | **Add $35–$60 freight surcharge** on oversized furniture and cap furniture discount at 10%. |
| **3. Copiers Power Enterprise Profit** | Technology Copiers generated **$3.36M in sales** and **$1.14M in profit (33.9% margin)**. | Copiers provide **94.9% of company net profit**. | **Scale Corporate B2B fleet leasing** for Copiers & Phones with multi-year toner contracts. |
| **4. Central Region Yields Highest Margin** | Central achieved **14.23% profit margin** ($413.2K profit) vs. West's 11.42%. | Texas ($1.00M sales) and Michigan ($710.5K sales, 17.1% margin) lead efficiency. | **Expand corporate account reps** in Texas, California, and Michigan hubs. |
| **5. Home Office Drives Highest AOV & Margin** | Home Office achieved **$1,005.23 AOV** and **13.50% profit margin** (highest across segments). | High-value remote professionals buy premium hardware bundles. | **Launch targeted Home Office VIP Loyalty Tier** with specialized hardware bundles. |

### Quantified EBITDA Upside Roadmap
Implementing the recommendations provides an estimated **+$638,959.00 in annual profit expansion (+53.2% increase)**, lifting enterprise operating margin from **12.49% to 17.99%**.

---

## 7. Deliverables & Documentation Index

- **Master Pipeline Runner**: [`run_pipeline.py`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/run_pipeline.py)
- **Data Dictionary**: [`data/data_dictionary.md`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/data/data_dictionary.md)
- **Cleaned Dataset**: [`data/processed/retail_sales_clean.csv`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/data/processed/retail_sales_clean.csv)
- **SQL Scripts Directory**: [`sql/`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/sql/)
- **SQL Results Summary**: [`reports/sql_results_summary.md`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/reports/sql_results_summary.md)
- **Excel Workbook**: [`excel/Retail_Sales_Analysis.xlsx`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/excel/Retail_Sales_Analysis.xlsx)
- **DAX Measures Library**: [`power_bi/dax_measures.dax`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/dax_measures.dax)
- **Data Model Architecture**: [`power_bi/data_model_architecture.md`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/data_model_architecture.md)
- **Power BI Layout & Wireframes**: [`power_bi/report_layout_and_visuals.md`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/report_layout_and_visuals.md)
- **Interactive Browser Mockup**: [`power_bi/dashboard_mockup.html`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/dashboard_mockup.html)
- **Executive Strategic Report**: [`reports/executive_insights_and_recommendations.md`](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/reports/executive_insights_and_recommendations.md)
website deployment setup
