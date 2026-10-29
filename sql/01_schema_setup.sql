-- ==============================================================================
-- 01_schema_setup.sql
-- Star Schema Relational Architecture & Analytical Views for Retail Sales
-- ==============================================================================

-- 1. Master Flat Analytical Table
CREATE TABLE IF NOT EXISTS retail_sales (
    Order_ID VARCHAR(30),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(20),
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Segment VARCHAR(30),
    Country VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(10),
    Region VARCHAR(20),
    Product_ID VARCHAR(30),
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name VARCHAR(150),
    Sales DECIMAL(12, 2),
    Quantity INT,
    Discount DECIMAL(4, 2),
    Profit DECIMAL(12, 2),
    Profit_Margin DECIMAL(6, 4),
    Unit_Price DECIMAL(10, 2),
    Order_Year INT,
    Order_Quarter VARCHAR(5),
    Order_Month INT,
    Order_Month_Name VARCHAR(10),
    Order_Month_Year VARCHAR(7),
    Order_Day_Name VARCHAR(15),
    Order_to_Ship_Days INT,
    Discount_Tier VARCHAR(20),
    Is_Profitable BOOLEAN
);

-- 2. Indexes for Query Optimization
CREATE INDEX IF NOT EXISTS idx_sales_order_date ON retail_sales(Order_Date);
CREATE INDEX IF NOT EXISTS idx_sales_category ON retail_sales(Category, Sub_Category);
CREATE INDEX IF NOT EXISTS idx_sales_region ON retail_sales(Region, State);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON retail_sales(Customer_ID, Segment);
CREATE INDEX IF NOT EXISTS idx_sales_discount_tier ON retail_sales(Discount_Tier);

-- 3. Dimension & Fact Tables (Star Schema)
CREATE TABLE IF NOT EXISTS dim_customer (
    Customer_ID VARCHAR(20) PRIMARY KEY,
    Customer_Name VARCHAR(100),
    Segment VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS dim_product (
    Product_ID VARCHAR(30) PRIMARY KEY,
    Product_Name VARCHAR(150),
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Unit_Price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS dim_geography (
    Geography_Key INTEGER PRIMARY KEY AUTOINCREMENT,
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(10),
    Region VARCHAR(20),
    Country VARCHAR(50),
    UNIQUE(City, State, Postal_Code)
);

CREATE TABLE IF NOT EXISTS dim_date (
    Date_Key DATE PRIMARY KEY,
    Order_Year INT,
    Order_Quarter VARCHAR(5),
    Order_Month INT,
    Order_Month_Name VARCHAR(10),
    Order_Month_Year VARCHAR(7),
    Order_Day_Name VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS fact_sales (
    Sales_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Order_ID VARCHAR(30),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(20),
    Customer_ID VARCHAR(20),
    Product_ID VARCHAR(30),
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(10),
    Sales DECIMAL(12, 2),
    Quantity INT,
    Discount DECIMAL(4, 2),
    Profit DECIMAL(12, 2),
    Profit_Margin DECIMAL(6, 4),
    Order_to_Ship_Days INT,
    Discount_Tier VARCHAR(20),
    Is_Profitable BOOLEAN,
    FOREIGN KEY (Customer_ID) REFERENCES dim_customer(Customer_ID),
    FOREIGN KEY (Product_ID) REFERENCES dim_product(Product_ID),
    FOREIGN KEY (Order_Date) REFERENCES dim_date(Date_Key)
);

-- 4. Analytical Summary View
CREATE VIEW IF NOT EXISTS v_sales_analytics AS
SELECT 
    Order_ID,
    Order_Date,
    Order_Month_Year,
    Order_Year,
    Customer_ID,
    Customer_Name,
    Segment,
    Region,
    State,
    City,
    Category,
    Sub_Category,
    Product_Name,
    Sales,
    Quantity,
    Discount,
    Profit,
    ROUND((Profit / Sales) * 100.0, 2) AS Profit_Margin_Pct,
    Order_to_Ship_Days,
    Discount_Tier,
    CASE WHEN Profit > 0 THEN 1 ELSE 0 END AS Profitable_Flag
FROM retail_sales;
