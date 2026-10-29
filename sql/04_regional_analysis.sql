-- ==============================================================================
-- 04_regional_analysis.sql
-- Geographic Sales Distribution, State-Level Profitability & Fulfillment SLAs
-- ==============================================================================

-- Query 1: Macro Regional Performance Breakdown
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

-- Query 2: Top 15 States by Revenue & Profitability (with Dense Rank)
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

-- Query 3: Logistics Fulfillment Lead Time (SLA) by Region and Shipping Tier
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
