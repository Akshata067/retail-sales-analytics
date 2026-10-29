# Power BI Dashboard Visual Layout & UX Design Specifications

## 1. Executive Visual Design System

- **Canvas Size**: 16:9 Standard Widescreen (`1280 x 720` px or `1920 x 1080` px)
- **Background**: Soft Executive Gray (`#F8FAFC`)
- **Card Background**: Crisp White (`#FFFFFF`) with 1px border (`#E2E8F0`) and 4px rounded radius
- **Color Palette**:
  - Primary Brand (Navy): `#1E3A8A`
  - Secondary Slate: `#334155`
  - Positive / Profit (Emerald): `#10B981`
  - Moderate / Watch (Blue): `#3B82F6`
  - Warning (Amber): `#F59E0B`
  - Critical / Loss (Crimson): `#EF4444`

---

## 2. Page 1: Executive Overview Dashboard

### Wireframe Layout Grid
```
+----------------------------------------------------------------------------------------------------+
| [Logo] GLOBAL RETAIL CORP - EXECUTIVE PERFORMANCE REPORT                     Date Range | Region | Cat |
+----------------------------------------------------------------------------------------------------+
| [  TOTAL SALES  ]  [  TOTAL PROFIT  ]  [ PROFIT MARGIN % ]  [  TOTAL ORDERS  ]  [ AVG ORDER VALUE  ] |
|     $9.61M              $1.20M              12.49%               10,000               $961.21      |
+------------------------------------------------------------------+---------------------------------+
| Monthly Sales Revenue and Profit Trend (2023 - 2026)             | Sales Share by Product Category |
| [Clustered Column (Sales) + Line (Profit Margin %)]              | [Donut Chart / Treemap]         |
|                                                                  | - Technology: 63.1%             |
|                                                                  | - Furniture: 29.9%              |
|                                                                  | - Office Supplies: 7.0%         |
+------------------------------------------------------------------+---------------------------------+
| Regional Sales & Profit Comparison (West, Central, South, East)  | Shipping Mode SLA Fulfillment   |
| [Grouped Bar Chart: Sales ($k) & Margin %]                       | [Horizontal Bar Chart]          |
+------------------------------------------------------------------+---------------------------------+
```

### Visual Specifications
1. **Global Slicer Header (Top Bar)**:
   - Slicer 1: `dim_date[Date_Key]` (Between Date Slider)
   - Slicer 2: `dim_geography[Region]` (Tile / Pill buttons)
   - Slicer 3: `dim_product[Category]` (Dropdown)
2. **KPI Card Row (Height: 90px)**:
   - Card 1: `[Total Sales]` formatted as `$#,##0,,.00M`
   - Card 2: `[Total Profit]` formatted as `$#,##0,,.00M`
   - Card 3: `[Profit Margin %]` formatted as `0.0%` with conditional text color (`#10B981` if $\ge 12\%$, `#EF4444` if $< 10\%$)
   - Card 4: `[Total Orders]` formatted as `#,##0`
   - Card 5: `[Average Order Value]` formatted as `$#,##0.00`
3. **Monthly Trend Visual (Line and Clustered Column Chart)**:
   - X-Axis: `dim_date[Order_Month_Year]`
   - Column Y-Axis: `[Total Sales]` (Fill: `#3B82F6`)
   - Line Y-Axis: `[Profit Margin %]` (Stroke: `#10B981`, Width: 3)
4. **Category Breakdown (Donut Chart)**:
   - Legend: `dim_product[Category]`
   - Values: `[Total Sales]`
5. **Regional Comparison (Clustered Bar Chart)**:
   - Y-Axis: `dim_geography[Region]`
   - X-Axis: `[Total Sales]` and `[Total Profit]`

---

## 3. Page 2: Product & Profitability Deep-Dive

### Wireframe Layout Grid
```
+----------------------------------------------------------------------------------------------------+
| PRODUCT PROFITABILITY & DISCOUNT ELASTICITY DEEP-DIVE                        Category | Subcategory |
+----------------------------------------------------------------------------------------------------+
| [ LOSS-MAKING LINES ]  [ GROSS MARGIN BLEED ]  [ PROFIT DRAG (TABLES) ]  [ POTENTIAL EBITDA GAIN ] |
|        1,585                 -$253.96K                 -$296.06K                 +$253.96K         |
+------------------------------------------------------------------+---------------------------------+
| Discount Rate vs. Profit Margin % Scatter Plot                   | Sub-Category Profit Matrix      |
| [Inflection Curve showing margin collapse beyond 20% discount]   | [Horizontal Diverging Bar]      |
|                                                                  | Copiers:  +$1.14M [====]        |
|                                                                  | Phones:   +$289.8K [==]         |
|                                                                  | Tables:   -$296.1K [====] Red   |
|                                                                  | Bookcases:-$76.7K  [==]   Red   |
+------------------------------------------------------------------+---------------------------------+
| Top 10 Best Sellers vs. Bottom 10 Loss Incurring Products (SKUs)                                   |
| [Interactive Matrix with In-Cell Data Bars & Margin Alert Flags]                                   |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications
1. **Discount Elasticity Scatter Plot**:
   - X-Axis: `fact_sales[Discount]` (formatted as `0%`)
   - Y-Axis: `[Profit Margin %]`
   - Legend / Details: `fact_sales[Order_ID]` or `dim_product[Sub_Category]`
   - Reference Line: Horizontal line at `0.0%` (Break-Even Threshold)
2. **Sub-Category Profitability Diverging Bar Chart**:
   - Y-Axis: `dim_product[Sub_Category]` (Sorted by Profit descending)
   - X-Axis: `[Total Profit]`
   - Conditional Color: Hex `#EF4444` if `[Total Profit] < 0`, else `#0EA5E9`
3. **SKU Matrix Table**:
   - Rows: `Product_Name`
   - Columns: `Sales`, `Quantity`, `Avg Discount`, `Profit`, `Margin %`
   - Conditional Formatting: Background color scale on `Margin %`

---

## 4. Page 3: Customer & Regional Opportunities

### Wireframe Layout Grid
```
+----------------------------------------------------------------------------------------------------+
| CUSTOMER SEGMENTATION & REGIONAL OPPORTUNITY DASHBOARD                               Region | State |
+----------------------------------------------------------------------------------------------------+
| [ TOTAL CUSTOMERS ]  [ ORDERS / CUSTOMER ]  [ CONSUMER SALES ]  [ CORPORATE SALES ]  [ HOME OFFICE ] |
|         650                 15.44                 $5.03M               $2.87M             $1.72M     |
+------------------------------------------------------------------+---------------------------------+
| Customer Segment Unit Economics (Sales, Profit, AOV)             | Top 15 States by Sales Volume   |
| [Clustered Column Chart: AOV by Segment]                         | [Horizontal Bar Chart]          |
| - Consumer: $950.98 | Margin: 12.35%                             | 1. California: $1.29M (13.1%)   |
| - Corporate: $954.22 | Margin: 12.12%                            | 2. Texas:      $1.00M (13.5%)   |
| - Home Office: $1,005.23 | Margin: 13.50% (Leader)               | 3. Florida:    $729.5K (11.7%)  |
+------------------------------------------------------------------+---------------------------------+
| Top 20 High-Value VIP Customer Accounts (RFM Profile & Lifetime Spend)                             |
| [Table: Customer Name | Segment | Region | Lifetime Orders | Total Sales | Total Profit | Tier]     |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications
1. **Segment Comparison Visuals**:
   - Donut Chart: Sales contribution by `dim_customer[Segment]`
   - Clustered Bar: `[Average Order Value]` by `Segment` (highlighting Home Office lead at $1,005.23)
2. **State Revenue Ranking**:
   - Y-Axis: `dim_geography[State]`
   - X-Axis: `[Total Sales]`
   - Data Labels: Show revenue and profit margin percentage
3. **VIP Customer Account Table**:
   - Fields: `Customer_Name`, `Segment`, `State`, `Lifetime Orders`, `Total Sales`, `Total Profit`, `Profit Margin %`, `RFM Tier`
