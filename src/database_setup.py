"""
database_setup.py
Initializes SQLite database, builds Star Schema relational structures,
ingests cleaned transaction data, and verifies integrity.
"""

import os
import sqlite3
import pandas as pd

def initialize_database(db_path, clean_csv_path, schema_sql_path):
    print("=" * 70)
    print("SQLITE RELATIONAL DATABASE SETUP & DATA INGESTION")
    print("=" * 70)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[-] Removed pre-existing database at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Execute DDL Schema Setup
    print(f"[*] Executing schema DDL from: {schema_sql_path}")
    with open(schema_sql_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("[+] Table schemas, indexes, and views initialized successfully.")

    # 2. Ingest Cleaned Data into Master Table
    print(f"[*] Ingesting cleaned dataset from: {clean_csv_path}")
    df = pd.read_csv(clean_csv_path)
    df.to_sql("retail_sales", conn, if_exists="append", index=False)
    print(f"[+] Loaded {len(df):,} records into 'retail_sales' table.")

    # 3. Populate Relational Star Schema Tables
    print("[*] Populating Star Schema Dimension and Fact tables...")
    
    # dim_customer
    cursor.execute("""
        INSERT OR IGNORE INTO dim_customer (Customer_ID, Customer_Name, Segment)
        SELECT DISTINCT Customer_ID, Customer_Name, Segment
        FROM retail_sales;
    """)

    # dim_product
    cursor.execute("""
        INSERT OR IGNORE INTO dim_product (Product_ID, Product_Name, Category, Sub_Category, Unit_Price)
        SELECT DISTINCT Product_ID, Product_Name, Category, Sub_Category, Unit_Price
        FROM retail_sales;
    """)

    # dim_geography
    cursor.execute("""
        INSERT OR IGNORE INTO dim_geography (City, State, Postal_Code, Region, Country)
        SELECT DISTINCT City, State, Postal_Code, Region, Country
        FROM retail_sales;
    """)

    # dim_date
    cursor.execute("""
        INSERT OR IGNORE INTO dim_date (Date_Key, Order_Year, Order_Quarter, Order_Month, Order_Month_Name, Order_Month_Year, Order_Day_Name)
        SELECT DISTINCT Order_Date, Order_Year, Order_Quarter, Order_Month, Order_Month_Name, Order_Month_Year, Order_Day_Name
        FROM retail_sales;
    """)

    # fact_sales
    cursor.execute("""
        INSERT INTO fact_sales (
            Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID, Product_ID,
            City, State, Postal_Code, Sales, Quantity, Discount, Profit, Profit_Margin,
            Order_to_Ship_Days, Discount_Tier, Is_Profitable
        )
        SELECT 
            Order_ID, Order_Date, Ship_Date, Ship_Mode, Customer_ID, Product_ID,
            City, State, Postal_Code, Sales, Quantity, Discount, Profit, Profit_Margin,
            Order_to_Ship_Days, Discount_Tier, Is_Profitable
        FROM retail_sales;
    """)

    conn.commit()

    # 4. Integrity Validation
    tables = ["retail_sales", "fact_sales", "dim_customer", "dim_product", "dim_geography", "dim_date"]
    print("-" * 70)
    print("DATABASE TABLE RECORD COUNTS:")
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
        cnt = cursor.fetchone()[0]
        print(f"  - {tbl.ljust(18)}: {cnt:>8,} rows")

    cursor.execute("SELECT ROUND(SUM(Sales), 2), ROUND(SUM(Profit), 2) FROM retail_sales;")
    tot_sales, tot_profit = cursor.fetchone()
    print("-" * 70)
    print(f"Database Total Sales : ${tot_sales:,.2f}")
    print(f"Database Total Profit: ${tot_profit:,.2f}")
    print(f"[+] SQLite database successfully configured at: {db_path}")
    print("=" * 70)

    conn.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, "database", "retail_sales.db")
    clean_csv_path = os.path.join(project_root, "data", "processed", "retail_sales_clean.csv")
    schema_sql_path = os.path.join(project_root, "sql", "01_schema_setup.sql")
    initialize_database(db_path, clean_csv_path, schema_sql_path)

if __name__ == "__main__":
    main()
