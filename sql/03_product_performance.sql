-- ==============================================================================
-- 03_product_performance.sql
-- Product Category, Sub-Category Profitability, Loss Makers, and SKU Rankings
-- ==============================================================================

-- Query 1: Category & Sub-Category Full Financial Performance Matrix
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

-- Query 2: Sub-Category Loss-Maker Diagnosis (Identifying Profit Bleed)
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

-- Query 3: Top 10 Revenue-Generating Products
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

-- Query 4: Bottom 10 Loss-Incurring Products
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
