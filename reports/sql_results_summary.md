# Relational SQL Analytics: Business Query Results & Tabular Evidence

> **Database Engine**: SQLite 3 (Normalized Star Schema & Analytical View)
> **Total Processed Transactions**: 10,039 records across 2023–2026

---

## 1. Revenue, Profit & Growth Trends
*Source File: `sql/02_revenue_profit_trends.sql`*

### Query 1: Monthly Financial Performance with Window Functions (MoM & Cumulative)
```sql
WITH monthly_metrics AS (
    SELECT 
        Order_Month_Year,
        Order_Year,
        Order_Month,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        ROUND(SUM(Sales), 2) AS Monthly_Sales,
        ROUND(SUM(Profit), 2) AS Monthly_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct
    FROM retail_sales
    GROUP BY Order_Month_Year, Order_Year, Order_Month
)
SELECT 
    Order_Month_Year,
    Total_Orders,
    Monthly_Sales,
    Monthly_Profit,
    Profit_Margin_Pct,
    ROUND(
        ((Monthly_Sales - LAG(Monthly_Sales, 1) OVER (ORDER BY Order_Month_Year)) 
        / LAG(Monthly_Sales, 1) OVER (ORDER BY Order_Month_Year)) * 100.0, 2
    ) AS MoM_Sales_Growth_Pct,
    ROUND(
        AVG(Monthly_Sales) OVER (
            ORDER BY Order_Month_Year 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS Rolling_3M_Avg_Sales,
    ROUND(SUM(Monthly_Sales) OVER (ORDER BY Order_Month_Year), 2) AS Cumulative_Sales,
    ROUND(SUM(Monthly_Profit) OVER (ORDER BY Order_Month_Year), 2) AS Cumulative_Profit
FROM monthly_metrics
ORDER BY Order_Month_Year;
```

| Order_Month_Year   |   Total_Orders |   Monthly_Sales |   Monthly_Profit |   Profit_Margin_Pct |   MoM_Sales_Growth_Pct |   Rolling_3M_Avg_Sales |   Cumulative_Sales |   Cumulative_Profit |
|:-------------------|---------------:|----------------:|-----------------:|--------------------:|-----------------------:|-----------------------:|-------------------:|--------------------:|
| 2023-01            |            211 |          183008 |         19527.7  |               10.67 |                 nan    |                 183008 |   183008           |             19527.7 |
| 2023-02            |            156 |          171530 |         33439.3  |               19.49 |                  -6.27 |                 177269 |   354538           |             52967   |
| 2023-03            |            198 |          164139 |         12340.3  |                7.52 |                  -4.31 |                 172893 |   518678           |             65307.2 |
| 2023-04            |            174 |          219545 |         36142.1  |               16.46 |                  33.76 |                 185072 |   738223           |            101449   |
| 2023-05            |            201 |          209211 |         27876.8  |               13.32 |                  -4.71 |                 197632 |   947434           |            129326   |
| 2023-06            |            205 |          252232 |         58911.7  |               23.36 |                  20.56 |                 226996 |        1.19967e+06 |            188238   |
| 2023-07            |            233 |          208910 |         20768.6  |                9.94 |                 -17.18 |                 223451 |        1.40858e+06 |            209006   |
| 2023-08            |            208 |          249863 |         44685.5  |               17.88 |                  19.6  |                 237002 |        1.65844e+06 |            253692   |
| 2023-09            |            220 |          182393 |         42536.6  |               23.32 |                 -27    |                 213722 |        1.84083e+06 |            296228   |
| 2023-10            |            257 |          253233 |         40979.3  |               16.18 |                  38.84 |                 228496 |        2.09406e+06 |            337208   |
| 2023-11            |            289 |          334443 |         56044.4  |               16.76 |                  32.07 |                 256690 |        2.42851e+06 |            393252   |
| 2023-12            |            291 |          337750 |         60054.1  |               17.78 |                   0.99 |                 308476 |        2.76626e+06 |            453306   |
| 2024-01            |            182 |          184188 |         24826.3  |               13.48 |                 -45.47 |                 285461 |        2.95045e+06 |            478133   |
| 2024-02            |            170 |          141489 |         11130.3  |                7.87 |                 -23.18 |                 221143 |        3.09194e+06 |            489263   |
| 2024-03            |            198 |          213722 |         24109.2  |               11.28 |                  51.05 |                 179800 |        3.30566e+06 |            513372   |
| 2024-04            |            190 |          146602 |          9729.17 |                6.64 |                 -31.41 |                 167271 |        3.45226e+06 |            523101   |
| 2024-05            |            227 |          220038 |         29162.8  |               13.25 |                  50.09 |                 193454 |        3.6723e+06  |            552264   |
| 2024-06            |            196 |          236679 |         45984.1  |               19.43 |                   7.56 |                 201106 |        3.90898e+06 |            598248   |
| 2024-07            |            208 |          147748 |         12134    |                8.21 |                 -37.57 |                 201488 |        4.05672e+06 |            610382   |
| 2024-08            |            209 |          190481 |         27169.9  |               14.26 |                  28.92 |                 191636 |        4.24721e+06 |            637552   |

*(Showing top 20 of 46 rows)*


### Query 2: Annual Year-over-Year (YoY) Growth Summary
```sql
WITH annual_metrics AS (
    SELECT 
        Order_Year,
        COUNT(DISTINCT Order_ID) AS Total_Orders,
        ROUND(SUM(Sales), 2) AS Annual_Sales,
        ROUND(SUM(Profit), 2) AS Annual_Profit,
        ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct
    FROM retail_sales
    GROUP BY Order_Year
)
SELECT 
    Order_Year,
    Total_Orders,
    Annual_Sales,
    ROUND(
        ((Annual_Sales - LAG(Annual_Sales, 1) OVER (ORDER BY Order_Year)) 
        / LAG(Annual_Sales, 1) OVER (ORDER BY Order_Year)) * 100.0, 2
    ) AS YoY_Sales_Growth_Pct,
    Annual_Profit,
    ROUND(
        ((Annual_Profit - LAG(Annual_Profit, 1) OVER (ORDER BY Order_Year)) 
        / LAG(Annual_Profit, 1) OVER (ORDER BY Order_Year)) * 100.0, 2
    ) AS YoY_Profit_Growth_Pct,
    Profit_Margin_Pct
FROM annual_metrics
ORDER BY Order_Year;
```

|   Order_Year |   Total_Orders |   Annual_Sales |   YoY_Sales_Growth_Pct |   Annual_Profit |   YoY_Profit_Growth_Pct |   Profit_Margin_Pct |
|-------------:|---------------:|---------------:|-----------------------:|----------------:|------------------------:|--------------------:|
|         2023 |           2643 |    2.76626e+06 |                 nan    |          453306 |                  nan    |               16.39 |
|         2024 |           2697 |    2.52675e+06 |                  -8.66 |          277415 |                  -38.8  |               10.98 |
|         2025 |           2698 |    2.37082e+06 |                  -6.17 |          241702 |                  -12.87 |               10.19 |
|         2026 |           1962 |    1.94831e+06 |                 -17.82 |          227796 |                   -5.75 |               11.69 |


---

## 2. Product Performance & Profit Drag
*Source File: `sql/03_product_performance.sql`*

### Query 1: Category & Sub-Category Full Financial Performance Matrix
```sql
SELECT 
    Category,
    Sub_Category,
    COUNT(*) AS Total_Order_Lines,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct,
    ROUND(AVG(Discount) * 100.0, 2) AS Avg_Discount_Pct,
    DENSE_RANK() OVER (PARTITION BY Category ORDER BY SUM(Profit) DESC) AS Profit_Rank_In_Category
FROM retail_sales
GROUP BY Category, Sub_Category
ORDER BY Category, Total_Profit DESC;
```

| Category        | Sub_Category   |   Total_Order_Lines |   Total_Units_Sold |      Total_Sales |      Total_Profit |   Profit_Margin_Pct |   Avg_Discount_Pct |   Profit_Rank_In_Category |
|:----------------|:---------------|--------------------:|-------------------:|-----------------:|------------------:|--------------------:|-------------------:|--------------------------:|
| Furniture       | Furnishings    |                 883 |               2705 | 114498           |   26179.4         |               22.86 |              14    |                         1 |
| Furniture       | Chairs         |                 861 |               2542 |      1.02493e+06 |   23137.8         |                2.26 |              14.74 |                         2 |
| Furniture       | Bookcases      |                 544 |               1662 | 382555           |  -76722.6         |              -20.06 |              14.72 |                         3 |
| Furniture       | Tables         |                 857 |               2537 |      1.36935e+06 | -296061           |              -21.62 |              14.39 |                         4 |
| Office Supplies | Appliances     |                 611 |               1750 | 214891           |   25718.3         |               11.97 |              15.27 |                         1 |
| Office Supplies | Storage        |                 551 |               1693 |  58687.8         |    9534.33        |               16.25 |              13.74 |                         2 |
| Office Supplies | Art            |                 333 |               1009 |  36277.3         |    8901.37        |               24.54 |              13.69 |                         3 |
| Office Supplies | Paper          |                 555 |               1741 |  26644.3         |    6966.62        |               26.15 |              14.77 |                         4 |
| Office Supplies | Binders        |                 525 |               1703 |  22170.4         |    6958.16        |               31.38 |              14.4  |                         5 |
| Office Supplies | Envelopes      |                 298 |                923 |  22157.8         |    5797.23        |               26.16 |              14.5  |                         6 |
| Office Supplies | Labels         |                 294 |                849 |  11894.4         |    4132.2         |               34.74 |              12.65 |                         7 |
| Office Supplies | Fasteners      |                 297 |                907 |  18553           |    3886.57        |               20.95 |              15.39 |                         8 |
| Office Supplies | Supplies       |                 543 |               1703 | 100460           |     219.01        |                0.22 |              14.07 |                         9 |
| Technology      | Copiers        |                 581 |               1712 |      3.35982e+06 |       1.13894e+06 |               33.9  |              15.87 |                         1 |
| Technology      | Phones         |                 833 |               2514 |      1.89132e+06 |  289776           |               15.32 |              14.86 |                         2 |
| Technology      | Accessories    |                 849 |               2624 | 144008           |   45212.1         |               31.4  |              14.78 |                         3 |
| Technology      | Machines       |                 624 |               1820 | 813918           |  -22355.5         |               -2.75 |              14.49 |                         4 |


### Query 2: Sub-Category Loss-Maker Diagnosis (Identifying Profit Bleed)
```sql
SELECT 
    Category,
    Sub_Category,
    COUNT(*) AS Total_Orders,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS Unprofitable_Orders,
    ROUND((SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS Unprofitable_Order_Pct,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Net_Profit,
    ROUND(SUM(CASE WHEN Profit < 0 THEN Profit ELSE 0 END), 2) AS Gross_Loss_Incurred
FROM retail_sales
GROUP BY Category, Sub_Category
HAVING Net_Profit < 0 OR Unprofitable_Order_Pct > 20.0
ORDER BY Net_Profit ASC;
```

| Category        | Sub_Category   |   Total_Orders |   Unprofitable_Orders |   Unprofitable_Order_Pct |      Total_Sales |   Net_Profit |   Gross_Loss_Incurred |
|:----------------|:---------------|---------------:|----------------------:|-------------------------:|-----------------:|-------------:|----------------------:|
| Furniture       | Tables         |            857 |                   857 |                   100    |      1.36935e+06 |   -296061    |            -296061    |
| Furniture       | Bookcases      |            544 |                   544 |                   100    | 382555           |    -76722.6  |             -76722.6  |
| Technology      | Machines       |            624 |                   293 |                    46.96 | 813918           |    -22355.5  |             -56720.2  |
| Office Supplies | Supplies       |            543 |                   212 |                    39.04 | 100460           |       219.01 |              -5600.86 |
| Furniture       | Chairs         |            861 |                   350 |                    40.65 |      1.02493e+06 |     23137.8  |             -50136.5  |
| Office Supplies | Appliances     |            611 |                   137 |                    22.42 | 214891           |     25718.3  |              -4918.24 |
| Technology      | Phones         |            833 |                   190 |                    22.81 |      1.89132e+06 |    289776    |             -36179.9  |


### Query 3: Top 10 Revenue-Generating Products
```sql
SELECT 
    Product_Name,
    Category,
    Sub_Category,
    COUNT(DISTINCT Order_ID) AS Order_Count,
    SUM(Quantity) AS Total_Units,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct
FROM retail_sales
GROUP BY Product_Name, Category, Sub_Category
ORDER BY Total_Sales DESC
LIMIT 10;
```

| Product_Name                        | Category   | Sub_Category   |   Order_Count |   Total_Units |      Total_Sales |   Total_Profit |   Profit_Margin_Pct |
|:------------------------------------|:-----------|:---------------|--------------:|--------------:|-----------------:|---------------:|--------------------:|
| Canon ImageRunner Enterprise Copier | Technology | Copiers        |           291 |           860 |      2.05875e+06 |      778036    |               37.79 |
| HP LaserJet Enterprise MFP 500      | Technology | Copiers        |           287 |           852 |      1.30108e+06 |      360903    |               27.74 |
| Samsung Galaxy S23 Ultra            | Technology | Phones         |           282 |           879 | 726968           |      117656    |               16.18 |
| Apple iPhone 14 Pro 128GB           | Technology | Phones         |           268 |           831 | 628642           |      109086    |               17.35 |
| Bush Business Conference Table 8ft  | Furniture  | Tables         |           276 |           771 | 599521           |     -142111    |              -23.7  |
| Herman Miller Aeron Ergonomic Chair | Furniture  | Chairs         |           279 |           808 | 584114           |       17280.6  |                2.96 |
| Google Pixel 8 Pro                  | Technology | Phones         |           281 |           804 | 535707           |       63034.4  |               11.77 |
| Uplift V2 Standing Executive Desk   | Furniture  | Tables         |           305 |           859 | 499046           |      -97654.6  |              -19.57 |
| Cisco Catalyst 24-Port Switch       | Technology | Machines       |           299 |           836 | 438517           |       -8034.53 |               -1.83 |
| Zebra Thermal Barcode Printer       | Technology | Machines       |           324 |           984 | 375401           |      -14321    |               -3.81 |


### Query 4: Bottom 10 Loss-Incurring Products
```sql
SELECT 
    Product_Name,
    Category,
    Sub_Category,
    COUNT(DISTINCT Order_ID) AS Order_Count,
    ROUND(AVG(Discount) * 100.0, 2) AS Avg_Discount_Pct,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Loss
FROM retail_sales
GROUP BY Product_Name, Category, Sub_Category
HAVING Total_Loss < 0
ORDER BY Total_Loss ASC
LIMIT 10;
```

| Product_Name                            | Category        | Sub_Category   |   Order_Count |   Avg_Discount_Pct |   Total_Sales |   Total_Loss |
|:----------------------------------------|:----------------|:---------------|--------------:|-------------------:|--------------:|-------------:|
| Bush Business Conference Table 8ft      | Furniture       | Tables         |           276 |              16.19 |      599521   |   -142111    |
| Uplift V2 Standing Executive Desk       | Furniture       | Tables         |           305 |              15.13 |      499046   |    -97654.6  |
| Safco Training Seminar Flip Table       | Furniture       | Tables         |           272 |              11.72 |      270779   |    -56294.6  |
| Sauder Heritage Library Bookcase        | Furniture       | Bookcases      |           278 |              14.57 |      233633   |    -46989.7  |
| Bush Furniture 5-Shelf Bookcase         | Furniture       | Bookcases      |           264 |              14.89 |      148923   |    -29733    |
| Zebra Thermal Barcode Printer           | Technology      | Machines       |           324 |              14.44 |      375401   |    -14321    |
| Cisco Catalyst 24-Port Switch           | Technology      | Machines       |           299 |              14.53 |      438517   |     -8034.53 |
| HON Volt Armless Mesh Office Chair      | Furniture       | Chairs         |           277 |              14.37 |      110889   |      -792.26 |
| Dahle Professional Rolling Trimmer 18in | Office Supplies | Supplies       |           271 |              14.23 |       81325.6 |      -348.84 |


---

## 3. Geographic Performance & Fulfillment SLAs
*Source File: `sql/04_regional_analysis.sql`*

### Query 1: Macro Regional Performance Breakdown
```sql
SELECT 
    Region,
    COUNT(DISTINCT Customer_ID) AS Total_Customers,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND((SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM retail_sales)), 2) AS Sales_Share_Pct,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct,
    ROUND(AVG(Discount) * 100.0, 2) AS Avg_Discount_Pct,
    ROUND(AVG(Order_to_Ship_Days), 2) AS Avg_Ship_Days
FROM retail_sales
GROUP BY Region
ORDER BY Total_Sales DESC;
```

| Region   |   Total_Customers |   Total_Orders |   Total_Sales |   Sales_Share_Pct |   Total_Profit |   Profit_Margin_Pct |   Avg_Discount_Pct |   Avg_Ship_Days |
|:---------|------------------:|---------------:|--------------:|------------------:|---------------:|--------------------:|-------------------:|----------------:|
| West     |               182 |           3266 |   3.17686e+06 |             33.05 |         362931 |               11.42 |              14.96 |            3.5  |
| Central  |               172 |           2993 |   2.90345e+06 |             30.21 |         413196 |               14.23 |              14.12 |            3.53 |
| South    |               142 |           1942 |   1.836e+06   |             19.1  |         211699 |               11.53 |              14.64 |            3.56 |
| East     |               154 |           1799 |   1.69582e+06 |             17.64 |         212393 |               12.52 |              14.42 |            3.59 |


### Query 2: Top 15 States by Revenue & Profitability (with Dense Rank)
```sql
SELECT 
    State,
    Region,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct,
    DENSE_RANK() OVER (ORDER BY SUM(Sales) DESC) AS Revenue_Rank
FROM retail_sales
GROUP BY State, Region
ORDER BY Total_Sales DESC
LIMIT 15;
```

| State          | Region   |   Total_Orders |      Total_Sales |   Total_Profit |   Profit_Margin_Pct |   Revenue_Rank |
|:---------------|:---------|---------------:|-----------------:|---------------:|--------------------:|---------------:|
| California     | West     |           1216 |      1.28816e+06 |       168088   |               13.05 |              1 |
| Texas          | Central  |           1025 |      1.00409e+06 |       135896   |               13.53 |              2 |
| Florida        | South    |            754 | 729527           |        85121   |               11.67 |              3 |
| Michigan       | Central  |            714 | 710491           |       121626   |               17.12 |              4 |
| Illinois       | Central  |            696 | 661849           |        81171.7 |               12.26 |              5 |
| Pennsylvania   | East     |            619 | 568727           |        50772.8 |                8.93 |              6 |
| Oregon         | West     |            582 | 544620           |        60446.1 |               11.1  |              7 |
| Washington     | West     |            488 | 472863           |        44237.5 |                9.36 |              8 |
| Ohio           | East     |            360 | 380427           |        63857.4 |               16.79 |              9 |
| New York       | East     |            444 | 363461           |        45894.3 |               12.63 |             10 |
| North Carolina | South    |            371 | 346328           |        33865   |                9.78 |             11 |
| Nevada         | West     |            402 | 338932           |        28466.8 |                8.4  |             12 |
| Wisconsin      | Central  |            326 | 302375           |        47692.5 |               15.77 |             13 |
| Colorado       | West     |            318 | 288800           |        34911   |               12.09 |             14 |
| Georgia        | South    |            294 | 282737           |        27846.1 |                9.85 |             15 |


### Query 3: Logistics Fulfillment Lead Time (SLA) by Region and Shipping Tier
```sql
SELECT 
    Region,
    Ship_Mode,
    COUNT(*) AS Total_Shipments,
    ROUND(AVG(Order_to_Ship_Days), 2) AS Avg_Fulfillment_Days,
    MIN(Order_to_Ship_Days) AS Min_Days,
    MAX(Order_to_Ship_Days) AS Max_Days
FROM retail_sales
GROUP BY Region, Ship_Mode
ORDER BY Region, Avg_Fulfillment_Days ASC;
```

| Region   | Ship_Mode      |   Total_Shipments |   Avg_Fulfillment_Days |   Min_Days |   Max_Days |
|:---------|:---------------|------------------:|-----------------------:|-----------:|-----------:|
| Central  | Same Day       |               146 |                   0    |          0 |          0 |
| Central  | First Class    |               443 |                   1.51 |          1 |          2 |
| Central  | Second Class   |               589 |                   2.98 |          2 |          4 |
| Central  | Standard Class |              1828 |                   4.47 |          3 |          6 |
| East     | Same Day       |                86 |                   0    |          0 |          0 |
| East     | First Class    |               261 |                   1.49 |          1 |          2 |
| East     | Second Class   |               358 |                   3.07 |          2 |          4 |
| East     | Standard Class |              1100 |                   4.53 |          3 |          6 |
| South    | Same Day       |                87 |                   0    |          0 |          0 |
| South    | First Class    |               286 |                   1.53 |          1 |          2 |
| South    | Second Class   |               376 |                   2.94 |          2 |          4 |
| South    | Standard Class |              1200 |                   4.5  |          3 |          6 |
| West     | Same Day       |               175 |                   0    |          0 |          0 |
| West     | First Class    |               527 |                   1.49 |          1 |          2 |
| West     | Second Class   |               655 |                   3.05 |          2 |          4 |
| West     | Standard Class |              1922 |                   4.52 |          3 |          6 |


---

## 4. Customer Segmentation & RFM Profiles
*Source File: `sql/05_customer_segmentation.sql`*

### Query 1: Customer Segment High-Level Unit Economics
```sql
SELECT 
    Segment,
    COUNT(DISTINCT Customer_ID) AS Total_Customers,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(COUNT(DISTINCT Order_ID) * 1.0 / COUNT(DISTINCT Customer_ID), 2) AS Orders_Per_Customer,
    SUM(Quantity) AS Total_Units_Purchased,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Average_Order_Value_AOV,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct
FROM retail_sales
GROUP BY Segment
ORDER BY Total_Sales DESC;
```

| Segment     |   Total_Customers |   Total_Orders |   Orders_Per_Customer |   Total_Units_Purchased |   Total_Sales |   Average_Order_Value_AOV |   Total_Profit |   Profit_Margin_Pct |
|:------------|------------------:|---------------:|----------------------:|------------------------:|--------------:|--------------------------:|---------------:|--------------------:|
| Consumer    |               335 |           5287 |                 15.78 |                   15978 |   5.02783e+06 |                    950.98 |         620901 |               12.35 |
| Corporate   |               196 |           3006 |                 15.34 |                    9071 |   2.86838e+06 |                    954.22 |         347689 |               12.12 |
| Home Office |               119 |           1707 |                 14.34 |                    5345 |   1.71592e+06 |                   1005.23 |         231630 |               13.5  |


### Query 2: RFM (Recency, Frequency, Monetary) Customer Profile
```sql
WITH max_date_cte AS (
    SELECT MAX(Order_Date) AS Max_Snapshot_Date FROM retail_sales
),
customer_rfm_raw AS (
    SELECT 
        r.Customer_ID,
        r.Customer_Name,
        r.Segment,
        r.Region,
        ROUND((JULIANDAY(m.Max_Snapshot_Date) - JULIANDAY(MAX(r.Order_Date)))) AS Recency_Days,
        COUNT(DISTINCT r.Order_ID) AS Frequency_Orders,
        ROUND(SUM(r.Sales), 2) AS Monetary_Sales,
        ROUND(SUM(r.Profit), 2) AS Total_Profit
    FROM retail_sales r
    CROSS JOIN max_date_cte m
    GROUP BY r.Customer_ID, r.Customer_Name, r.Segment, r.Region, m.Max_Snapshot_Date
)
SELECT 
    Customer_ID,
    Customer_Name,
    Segment,
    Region,
    Recency_Days,
    Frequency_Orders,
    Monetary_Sales,
    Total_Profit,
    CASE 
        WHEN Frequency_Orders >= 20 AND Recency_Days <= 60 THEN 'VIP / Champion'
        WHEN Frequency_Orders >= 15 AND Recency_Days <= 120 THEN 'Loyal Core'
        WHEN Recency_Days > 180 THEN 'At Risk / Churn Candidate'
        ELSE 'Active Regular'
    END AS RFM_Customer_Tier
FROM customer_rfm_raw
ORDER BY Monetary_Sales DESC
LIMIT 20;
```

| Customer_ID   | Customer_Name     | Segment     | Region   |   Recency_Days |   Frequency_Orders |   Monetary_Sales |   Total_Profit | RFM_Customer_Tier   |
|:--------------|:------------------|:------------|:---------|---------------:|-------------------:|-----------------:|---------------:|:--------------------|
| CG-10097      | Christopher Brown | Corporate   | West     |             15 |                 57 |          84758.2 |       11131.1  | VIP / Champion      |
| CG-10057      | Karen Thomas      | Consumer    | West     |             35 |                 48 |          81244.6 |        8569.6  | VIP / Champion      |
| CG-10105      | Jennifer Clark    | Home Office | Central  |            126 |                 44 |          80752.6 |       29834.5  | Active Regular      |
| CG-10068      | Nancy Johnson     | Corporate   | Central  |             30 |                 54 |          76234   |       15195.1  | VIP / Champion      |
| CG-10003      | William Miller    | Corporate   | Central  |             14 |                 61 |          75092.2 |       12833.4  | VIP / Champion      |
| CG-10121      | Michael Rodriguez | Corporate   | West     |             26 |                 62 |          74835.4 |        8075.56 | VIP / Champion      |
| CG-10053      | Lisa Hernandez    | Home Office | Central  |             13 |                 55 |          74665.4 |        9025.08 | VIP / Champion      |
| CG-10106      | Donna Lee         | Consumer    | South    |              2 |                 45 |          73382.4 |       13401.2  | VIP / Champion      |
| CG-10107      | Thomas Wilson     | Consumer    | Central  |              7 |                 55 |          71976.4 |       14101.1  | VIP / Champion      |
| CG-10101      | Barbara Jones     | Consumer    | Central  |             39 |                 56 |          68446.6 |        6661.92 | VIP / Champion      |
| CG-10005      | Margaret Williams | Consumer    | West     |             10 |                 56 |          68322.5 |       16215.5  | VIP / Champion      |
| CG-10035      | Sandra Martinez   | Home Office | West     |              8 |                 49 |          67831.4 |        8718.38 | VIP / Champion      |
| CG-10020      | Richard Jones     | Consumer    | West     |            105 |                 48 |          67621.8 |       18302.4  | Loyal Core          |
| CG-10027      | David Thomas      | Consumer    | West     |             64 |                 52 |          67506.8 |        5927.61 | Loyal Core          |
| CG-10017      | Linda Harris      | Consumer    | West     |             34 |                 48 |          66355.3 |       14121.3  | VIP / Champion      |
| CG-10054      | Kimberly Smith    | Home Office | Central  |             32 |                 54 |          66338.7 |       14383    | VIP / Champion      |
| CG-10103      | Linda Thomas      | Consumer    | Central  |              3 |                 51 |          64050.7 |        9954.91 | VIP / Champion      |
| CG-10023      | Sarah Robinson    | Consumer    | Central  |             27 |                 50 |          63653.1 |        8749.21 | VIP / Champion      |
| CG-10007      | Steven Johnson    | Consumer    | Central  |             44 |                 55 |          62306.2 |       13644.1  | VIP / Champion      |
| CG-10130      | William Taylor    | Consumer    | West     |             37 |                 52 |          62276.6 |       10533.1  | VIP / Champion      |


### Query 3: Top 10 Most Profitable Customers (Customer LTV Stars)
```sql
SELECT 
    Customer_ID,
    Customer_Name,
    Segment,
    Region,
    COUNT(DISTINCT Order_ID) AS Lifetime_Orders,
    ROUND(SUM(Sales), 2) AS Lifetime_Sales,
    ROUND(SUM(Profit), 2) AS Lifetime_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct
FROM retail_sales
GROUP BY Customer_ID, Customer_Name, Segment, Region
ORDER BY Lifetime_Profit DESC
LIMIT 10;
```

| Customer_ID   | Customer_Name     | Segment     | Region   |   Lifetime_Orders |   Lifetime_Sales |   Lifetime_Profit |   Profit_Margin_Pct |
|:--------------|:------------------|:------------|:---------|------------------:|-----------------:|------------------:|--------------------:|
| CG-10105      | Jennifer Clark    | Home Office | Central  |                44 |          80752.6 |           29834.5 |               36.95 |
| CG-10020      | Richard Jones     | Consumer    | West     |                48 |          67621.8 |           18302.4 |               27.07 |
| CG-10005      | Margaret Williams | Consumer    | West     |                56 |          68322.5 |           16215.5 |               23.73 |
| CG-10068      | Nancy Johnson     | Corporate   | Central  |                54 |          76234   |           15195.1 |               19.93 |
| CG-10054      | Kimberly Smith    | Home Office | Central  |                54 |          66338.7 |           14383   |               21.68 |
| CG-10045      | Joshua Robinson   | Consumer    | Central  |                52 |          62261.7 |           14336.6 |               23.03 |
| CG-10017      | Linda Harris      | Consumer    | West     |                48 |          66355.3 |           14121.3 |               21.28 |
| CG-10107      | Thomas Wilson     | Consumer    | Central  |                55 |          71976.4 |           14101.1 |               19.59 |
| CG-10122      | Linda Miller      | Home Office | Central  |                44 |          57558.5 |           13997.7 |               24.32 |
| CG-10007      | Steven Johnson    | Consumer    | Central  |                55 |          62306.2 |           13644.1 |               21.9  |


---

## 5. Discount Sensitivity & Margin Erosion
*Source File: `sql/06_discount_impact_analysis.sql`*

### Query 1: Discount Tier Profitability Matrix
```sql
SELECT 
    Discount_Tier,
    COUNT(*) AS Total_Transactions,
    SUM(Quantity) AS Total_Units,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND((SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM retail_sales)), 2) AS Sales_Share_Pct,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Profit_Margin_Pct,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS Unprofitable_Lines,
    ROUND(SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Unprofitable_Line_Pct,
    ROUND(SUM(CASE WHEN Profit < 0 THEN Profit ELSE 0 END), 2) AS Total_Loss_Incurred
FROM retail_sales
GROUP BY Discount_Tier
ORDER BY 
    CASE Discount_Tier
        WHEN '0% None' THEN 1
        WHEN '1-10% Low' THEN 2
        WHEN '11-20% Moderate' THEN 3
        WHEN '21-40% High' THEN 4
        WHEN '>40% Deep' THEN 5
    END;
```

| Discount_Tier   |   Total_Transactions |   Total_Units |      Total_Sales |   Sales_Share_Pct |      Total_Profit |   Profit_Margin_Pct |   Unprofitable_Lines |   Unprofitable_Line_Pct |   Total_Loss_Incurred |
|:----------------|---------------------:|--------------:|-----------------:|------------------:|------------------:|--------------------:|---------------------:|------------------------:|----------------------:|
| 0% None         |                 4535 |         13878 |      5.09959e+06 |             53.05 |       1.17182e+06 |               22.98 |                  652 |                   14.38 |             -112289   |
| 1-10% Low       |                 1456 |          4321 |      1.32994e+06 |             13.84 |  149971           |               11.28 |                  251 |                   17.24 |              -56247.1 |
| 11-20% Moderate |                 2003 |          5993 |      1.83766e+06 |             19.12 |   85930.7         |                4.68 |                  649 |                   32.4  |             -127787   |
| 21-40% High     |                 1321 |          4043 |      1.04894e+06 |             10.91 |  -93430.2         |               -8.91 |                  861 |                   65.18 |             -139892   |
| >40% Deep       |                  724 |          2159 | 296011           |              3.08 | -114067           |              -38.53 |                  724 |                  100    |             -114067   |


### Query 2: Category x Discount Tier Vulnerability Matrix
```sql
SELECT 
    Category,
    Discount_Tier,
    COUNT(*) AS Order_Count,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100.0, 2) AS Margin_Pct
FROM retail_sales
GROUP BY Category, Discount_Tier
ORDER BY Category, 
    CASE Discount_Tier
        WHEN '0% None' THEN 1
        WHEN '1-10% Low' THEN 2
        WHEN '11-20% Moderate' THEN 3
        WHEN '21-40% High' THEN 4
        WHEN '>40% Deep' THEN 5
    END;
```

| Category        | Discount_Tier   |   Order_Count |      Total_Sales |      Total_Profit |   Margin_Pct |
|:----------------|:----------------|--------------:|-----------------:|------------------:|-------------:|
| Furniture       | 0% None         |          1437 |      1.57897e+06 |  -23783.1         |        -1.51 |
| Furniture       | 1-10% Low       |           465 | 433388           |  -45796           |       -10.57 |
| Furniture       | 11-20% Moderate |           638 | 523341           | -106659           |       -20.38 |
| Furniture       | 21-40% High     |           366 | 259655           |  -87115.3         |       -33.55 |
| Furniture       | >40% Deep       |           239 |  95977.6         |  -60113.1         |       -62.63 |
| Office Supplies | 0% None         |          1800 | 268350           |   66321.3         |        24.71 |
| Office Supplies | 1-10% Low       |           597 |  72966.5         |   11230.4         |        15.39 |
| Office Supplies | 11-20% Moderate |           816 |  96822.2         |    4786.4         |         4.94 |
| Office Supplies | 21-40% High     |           516 |  58520           |   -5135.51        |        -8.78 |
| Office Supplies | >40% Deep       |           278 |  15077.3         |   -5088.81        |       -33.75 |
| Technology      | 0% None         |          1298 |      3.25227e+06 |       1.12928e+06 |        34.72 |
| Technology      | 1-10% Low       |           394 | 823582           |  184537           |        22.41 |
| Technology      | 11-20% Moderate |           549 |      1.21749e+06 |  187803           |        15.43 |
| Technology      | 21-40% High     |           439 | 730763           |   -1179.35        |        -0.16 |
| Technology      | >40% Deep       |           207 | 184956           |  -48865.2         |       -26.42 |


### Query 3: Capping Analysis (Financial Opportunity of Capping Discounts at 20%)
```sql
SELECT 
    COUNT(CASE WHEN Discount > 0.20 AND Profit < 0 THEN 1 END) AS Distressed_Transaction_Lines,
    ROUND(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Sales ELSE 0 END), 2) AS Distressed_Sales_Volume,
    ROUND(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Profit ELSE 0 END), 2) AS Total_Margin_Bleed,
    ROUND(ABS(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Profit ELSE 0 END)), 2) AS Potential_EBITDA_Reclaimed
FROM retail_sales;
```

|   Distressed_Transaction_Lines |   Distressed_Sales_Volume |   Total_Margin_Bleed |   Potential_EBITDA_Reclaimed |
|-------------------------------:|--------------------------:|---------------------:|-----------------------------:|
|                           1585 |                    953273 |              -253959 |                       253959 |


---
