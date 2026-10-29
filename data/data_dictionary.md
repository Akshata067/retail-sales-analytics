# Retail Sales Analytics Data Dictionary & Schema Documentation

## 1. Project Overview & Business Domain
This dataset represents transactional order lines for **Global Retail Corp**, a nationwide omnichannel retailer selling products across three core categories: **Technology**, **Furniture**, and **Office Supplies**. The dataset covers transactions from January 2023 through December 2026 across four primary geographic regions in the United States: **East**, **West**, **Central**, and **South**.

---

## 2. Entity Attribute Definitions

| Column Name | Data Type (Raw) | Data Type (Clean) | Description | Example Values | Constraints / Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Order_ID` | String | String | Unique identifier for the customer order. An order may contain multiple line items. | `CA-2024-152156`, `US-2025-108966` | Format: `[Country]-[Year]-[6 Digits]` |
| `Order_Date` | String | Date (YYYY-MM-DD) | Date when the customer placed the order. | `2024-11-08` | Cannot be after `Ship_Date`. |
| `Ship_Date` | String | Date (YYYY-MM-DD) | Date when the order was fulfilled and shipped from warehouse. | `2024-11-11` | Must be $\ge$ `Order_Date`. |
| `Ship_Mode` | String | String | Logistics shipping tier selected by customer. | `Standard Class`, `Second Class`, `First Class`, `Same Day` | 4 distinct values. |
| `Customer_ID` | String | String | Unique alphanumeric identifier for each customer. | `CG-12520`, `DV-13045` | Unique per customer entity. |
| `Customer_Name` | String | String | Full name of the purchasing customer or account manager. | `Claire Gute`, `Darrin Van Huff` | Title Cased. |
| `Segment` | String | String | Market segment classification of the customer. | `Consumer`, `Corporate`, `Home Office` | 3 distinct values. |
| `Country` | String | String | Country where the order was placed / delivered. | `United States` | Standardized to United States. |
| `City` | String | String | City of delivery. | `New York City`, `Los Angeles`, `Seattle`, `Chicago` | Capitalized city names. |
| `State` | String | String | US State of delivery. | `California`, `New York`, `Texas`, `Washington` | 50 US States + DC. |
| `Postal_Code` | String / Float | String | 5-digit US Postal ZIP Code. | `90036`, `10024`, `77095` | Zero-padded 5 digits. |
| `Region` | String | String | Macro sales territory division. | `East`, `West`, `Central`, `South` | 4 distinct regions. |
| `Product_ID` | String | String | Unique SKU identifier for the product line item. | `FUR-BO-10001798`, `TEC-PH-10002310` | Category-Subcategory prefix. |
| `Category` | String | String | Top-level product category classification. | `Technology`, `Furniture`, `Office Supplies` | 3 distinct categories. |
| `Sub_Category` | String | String | Specific product taxonomy group. | `Phones`, `Chairs`, `Storage`, `Binders`, `Tables`, `Copiers` | 17 standard subcategories. |
| `Product_Name` | String | String | Full commercial item description. | `Apple iPhone 14 Pro, 128GB`, `Herman Miller Ergonomic Task Chair` | Non-empty string. |
| `Sales` | String / Float | Float | Total gross transaction revenue (after discount applied). | `261.96`, `731.94`, `14.62` | Currency ($), positive float. |
| `Quantity` | Integer | Integer | Number of units purchased in the order line. | `2`, `3`, `7` | Positive integer ($1 \le Q \le 14$). |
| `Discount` | Float | Float | Discount percentage applied to the order line. | `0.00`, `0.10`, `0.20`, `0.70` | Range: $0.00$ to $0.80$ ($0\% - 80\%$). |
| `Profit` | Float | Float | Net bottom-line profit or loss realized on the transaction line. | `41.91`, `-62.15`, `219.58` | Can be negative (loss). |

---

## 3. Derived & Feature Engineered Fields

| Column Name | Data Type | Formula / Business Logic | Purpose |
| :--- | :--- | :--- | :--- |
| `Profit_Margin` | Float | `Profit / Sales` | Normalized transaction profitability ratio. |
| `Unit_Price` | Float | `Sales / (Quantity * (1 - Discount))` | Estimated baseline list price per unit before discount. |
| `Order_Year` | Integer | `YEAR(Order_Date)` | Calendar year grouping for YoY trend analysis. |
| `Order_Quarter` | String | `CONCAT('Q', QUARTER(Order_Date))` | Financial quarter grouping. |
| `Order_Month` | Integer | `MONTH(Order_Date)` | Calendar month (1–12) for seasonality curves. |
| `Order_Month_Year` | String | `YYYY-MM` format | Granular time-series continuity. |
| `Order_Day_Name` | String | Day of week (`Monday`, `Tuesday`, etc.) | Intra-week demand profiling. |
| `Order_to_Ship_Days`| Integer | `Ship_Date - Order_Date` | Fulfillment SLA lead time. |
| `Discount_Tier` | String | `0% None`, `1-10% Low`, `11-20% Moderate`, `21-40% High`, `>40% Deep` | Granular elasticity segmentation. |
| `Is_Profitable` | Boolean | `Profit > 0` | Binary flag for loss-making order diagnostics. |

---

## 4. Data Quality Inconsistencies Handled in Raw Pipeline

The raw source dataset (`retail_sales_raw.csv`) intentionally includes realistic data quality anomalies encountered in enterprise ERP/CRM dumps:
1. **Duplicate Order Lines**: Exact duplicate line items requiring deduplication based on transaction keys.
2. **Missing Postal Codes**: Unpopulated ZIP codes for certain regional accounts requiring fallback imputation.
3. **Dirty Text Formatting**: Inconsistent casing in customer names, categories, and cities (e.g. `technology`, `FURNITURE`, `Los angeles`).
4. **String-Encoded Currency**: Dollar symbols (`$`) and comma thousands separators in `Sales` and `Profit` fields requiring regex parsing.
5. **Inconsistent Date Formats**: Mixed string dates (`YYYY-MM-DD`, `MM/DD/YYYY`, `DD-MM-YYYY`) requiring unified datetime parsing.
6. **Trailing Whitespace**: Padded spaces in category and subcategory string keys.

---

## 5. Documented Data Limitations

1. **No Granular COGS Breakdown**: Cost of goods sold is represented implicitly as `Sales - Profit`, without itemized bill-of-materials, warehousing, or labor cost breakdowns.
2. **Attribution Blindness**: Marketing acquisition channel and promotional campaign attribution are not tracked per order line.
3. **Delivery Feedback**: Order tracking terminates at `Ship_Date`; final carrier delivery timestamp and return/refund tracking post-delivery are not represented.
4. **Inflation Non-Adjustment**: Currency values are nominal USD and not adjusted for CPI inflation across the 2023–2026 timeline.
