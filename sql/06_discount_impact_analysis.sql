-- ==============================================================================
-- 06_discount_impact_analysis.sql
-- Discount Elasticity, Margin Erosion, and Profit Reclamation Opportunity
-- ==============================================================================

-- Query 1: Discount Tier Profitability Matrix
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

-- Query 2: Category x Discount Tier Vulnerability Matrix
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

-- Query 3: Capping Analysis (Financial Opportunity of Capping Discounts at 20%)
SELECT 
    COUNT(CASE WHEN Discount > 0.20 AND Profit < 0 THEN 1 END) AS Distressed_Transaction_Lines,
    ROUND(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Sales ELSE 0 END), 2) AS Distressed_Sales_Volume,
    ROUND(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Profit ELSE 0 END), 2) AS Total_Margin_Bleed,
    ROUND(ABS(SUM(CASE WHEN Discount > 0.20 AND Profit < 0 THEN Profit ELSE 0 END)), 2) AS Potential_EBITDA_Reclaimed
FROM retail_sales;
