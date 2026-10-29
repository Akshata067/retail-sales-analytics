# Power BI Dashboard Build Guide & Setup Instructions

This guide provides end-to-end instructions for assembling the **Retail Sales Analytics Interactive Report** in **Power BI Desktop**, incorporating Star Schema data modeling, custom DAX measures, and interactive visual pages.

---

## Step 1: Ingest Data into Power BI Desktop

1. Launch **Power BI Desktop**.
2. Click **Get Data > Text/CSV**.
3. Select the cleaned data file:
   `c:\Users\Akshatha\OneDrive\Desktop\TIC TAC\retail_sales_analytics\data\processed\retail_sales_clean.csv`
4. In the preview dialog, click **Transform Data** to open the **Power Query Editor**.
5. Verify column data types:
   - `Order_Date` and `Ship_Date` -> **Date**
   - `Sales`, `Profit`, `Unit_Price` -> **Fixed Decimal Number (Currency)**
   - `Quantity`, `Order_Year`, `Order_to_Ship_Days` -> **Whole Number**
   - `Discount`, `Profit_Margin` -> **Percentage**
   - Text fields (`Order_ID`, `Customer_ID`, `City`, `State`, etc.) -> **Text**
6. Rename this query to `fact_sales`.
7. Click **Close & Apply**.

---

## Step 2: Create the Dedicated Date Dimension (`dim_date`)

1. In Power BI Desktop, select the **Table view** or **Modeling** tab in the top ribbon.
2. Click **New Table** and paste the date dimension DAX:
   ```dax
   dim_date = 
   VAR MinDate = DATE(2023, 1, 1)
   VAR MaxDate = DATE(2026, 12, 31)
   RETURN
       ADDCOLUMNS(
           CALENDAR(MinDate, MaxDate),
           "Date_Key", [Date],
           "Order_Year", YEAR([Date]),
           "Order_Quarter", "Q" & FORMAT([Date], "Q"),
           "Order_Month", MONTH([Date]),
           "Order_Month_Name", FORMAT([Date], "mmm"),
           "Order_Month_Year", FORMAT([Date], "yyyy-mm"),
           "Order_Day_Name", FORMAT([Date], "dddd"),
           "Day_Of_Week", WEEKDAY([Date], 2),
           "Is_Weekend", IF(WEEKDAY([Date], 2) IN {6, 7}, TRUE(), FALSE())
       )
   ```
3. Mark as Date Table:
   - Right-click `dim_date` in the Data pane -> **Mark as date table** -> Select `Date_Key`.
4. Configure column sorting:
   - Select `Order_Month_Name` -> Ribbon: **Column tools > Sort by column** -> Choose `Order_Month`.
   - Select `Order_Month_Year` -> Ribbon: **Column tools > Sort by column** -> Choose `Date_Key`.

---

## Step 3: Establish Relationships (Model View)

1. Click on the **Model view** icon on the left navigation bar.
2. Create the relationship between `dim_date` and `fact_sales`:
   - Drag `dim_date[Date_Key]` to `fact_sales[Order_Date]`.
   - Ensure Cardinality is **1 to Many (`1:*`)** and Cross filter direction is **Single**.

---

## Step 4: Add DAX Measures

1. Create a dedicated measures table:
   - Ribbon: **Home > Enter Data** -> Name the table `_Measures` -> Click **Load**.
2. Open `power_bi/dax_measures.dax` in any text editor.
3. For each measure, select `_Measures` -> Ribbon: **Table tools > New Measure**, then paste the DAX formula:
   - `[Total Sales]`
   - `[Total Profit]`
   - `[Profit Margin %]`
   - `[Total Orders]`
   - `[Average Order Value]`
   - `[Sales YTD]`, `[YoY Sales Growth %]`, `[MoM Sales Growth %]`
   - `[Gross Margin Bleed]`, `[Potential Margin Reclaimed]`
   - `[Orders Per Customer]`, `[Dynamic Report Title]`
4. Format each measure appropriately in the ribbon (Currency `$` for sales/profit, Percentage `%` with 1 decimal for margins, Whole Number for counts).

---

## Step 5: Build Visual Pages

Follow the detailed visual wireframes in [report_layout_and_visuals.md](file:///c:/Users/Akshatha/OneDrive/Desktop/TIC%20TAC/retail_sales_analytics/power_bi/report_layout_and_visuals.md):
- **Page 1: Executive Overview** (High-level KPI cards, Monthly Sales & Profit combo chart, Category donut chart, Regional comparison).
- **Page 2: Product & Profitability Deep-Dive** (Discount vs Margin scatter plot, Sub-Category diverging profit bar, SKU matrix).
- **Page 3: Customer & Regional Opportunities** (Segment metrics, State-level rankings, VIP customer account table).

---

## Step 6: Interactive Web Mockup (Browser-Based)

To immediately preview and test the complete interactive dashboard without launching Power BI Desktop, open:
`power_bi/dashboard_mockup.html` in Google Chrome, Microsoft Edge, or any modern web browser.
It features responsive KPI cards, dynamic interactive charts, filtering toggles, and data tables matching the Power BI report.
