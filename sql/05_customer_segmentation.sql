-- ==============================================================================
-- 05_customer_segmentation.sql
-- Customer Segment Economics, RFM Profiling & High-Value Account Analytics
-- ==============================================================================

-- Query 1: Customer Segment High-Level Unit Economics
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

-- Query 2: RFM (Recency, Frequency, Monetary) Customer Profile
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

-- Query 3: Top 10 Most Profitable Customers (Customer LTV Stars)
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
