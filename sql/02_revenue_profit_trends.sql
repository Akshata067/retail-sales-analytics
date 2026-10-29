-- ==============================================================================
-- 02_revenue_profit_trends.sql
-- Time-Series Revenue, Profit Trends, MoM/YoY Growth, and Moving Averages
-- ==============================================================================

-- Query 1: Monthly Financial Performance with Window Functions (MoM & Cumulative)
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

-- Query 2: Annual Year-over-Year (YoY) Growth Summary
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
