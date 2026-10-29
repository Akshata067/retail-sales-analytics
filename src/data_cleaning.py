"""
data_cleaning.py
Enterprise Data Pipeline Cleaning & Transformation Module.
Cleans raw transactions, resolves quality anomalies, engineers analytical features,
and outputs high-integrity dataset ready for SQL, Excel, and Power BI.
"""

import os
import re
import numpy as np
import pandas as pd

def clean_currency(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("$", "").replace(",", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def clean_retail_data(raw_csv_path, processed_csv_path):
    print("=" * 70)
    print("RETAIL SALES DATA CLEANING & TRANSFORMATION PIPELINE")
    print("=" * 70)
    
    # 1. Ingestion
    print(f"[*] Ingesting raw data from: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path, dtype={"Postal_Code": str})
    initial_rows = len(df)
    print(f"    Raw records loaded: {initial_rows:,}")

    # 2. Deduplication
    dups_count = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"[-] Dropped {dups_count:,} duplicate records. Remaining: {len(df):,}")

    # 3. String Trimming & Standardizing
    str_cols = ["Order_ID", "Ship_Mode", "Customer_ID", "Customer_Name", 
                "Segment", "Country", "City", "State", "Region", 
                "Product_ID", "Category", "Sub_Category", "Product_Name"]
    
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Standardize casing
    df["Category"] = df["Category"].str.title()
    df["Sub_Category"] = df["Sub_Category"].str.title()
    df["City"] = df["City"].str.title()
    df["Segment"] = df["Segment"].str.title()
    df["Ship_Mode"] = df["Ship_Mode"].str.title()
    df["Country"] = "United States"

    # 4. Numeric Data Cleaning & Casting
    print("[*] Parsing numeric fields and resolving formatting symbols...")
    df["Sales"] = df["Sales"].apply(clean_currency).round(2)
    df["Profit"] = df["Profit"].apply(clean_currency).round(2)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0.0).round(2)

    # 5. Missing Value Imputation (Postal Codes)
    missing_post = df["Postal_Code"].isna() | (df["Postal_Code"] == "nan") | (df["Postal_Code"] == "")
    missing_count = missing_post.sum()
    print(f"[*] Resolving {missing_count} missing Postal Codes via geographical lookup...")
    
    # Create lookup map from known (State, City) -> Postal_Code
    valid_geo = df[~missing_post][["State", "City", "Postal_Code"]].drop_duplicates(subset=["State", "City"])
    geo_lookup = valid_geo.set_index(["State", "City"])["Postal_Code"].to_dict()

    def impute_zip(row):
        val = str(row["Postal_Code"]).strip()
        if pd.isna(val) or val in ["nan", "", "None"]:
            return geo_lookup.get((row["State"], row["City"]), "90001")
        # Format to 5 digits if needed
        clean_z = re.sub(r"[^\d]", "", val)
        return clean_z.zfill(5)[:5] if clean_z else "90001"

    df["Postal_Code"] = df.apply(impute_zip, axis=1)

    # 6. Datetime Parsing & Chronological Validation
    print("[*] Normalizing datetime timestamps...")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="mixed")
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], format="mixed")

    # Chronological check: Ship_Date must be >= Order_Date
    invalid_dates = df["Ship_Date"] < df["Order_Date"]
    if invalid_dates.sum() > 0:
        print(f"    Correcting {invalid_dates.sum()} anomalous ship dates...")
        df.loc[invalid_dates, "Ship_Date"] = df.loc[invalid_dates, "Order_Date"] + pd.Timedelta(days=3)

    # 7. Analytical Feature Engineering
    print("[*] Engineering analytical features and business KPIs...")
    # Profit Margin % (avoid zero division)
    df["Profit_Margin"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]).round(4), 0.0)

    # Estimated Unit Price
    # Formula: Sales = Unit_Price * Quantity * (1 - Discount)
    discount_multiplier = (1.0 - df["Discount"]).replace(0.0, 0.01)
    df["Unit_Price"] = (df["Sales"] / (df["Quantity"] * discount_multiplier)).round(2)

    # Calendar Dimensions
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Order_Month_Year"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Order_Day_Name"] = df["Order_Date"].dt.day_name()
    
    # Fulfillment lead time
    df["Order_to_Ship_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days

    # Discount Tier segmentation
    bins = [-0.01, 0.00, 0.10, 0.20, 0.40, 1.00]
    labels = ["0% None", "1-10% Low", "11-20% Moderate", "21-40% High", ">40% Deep"]
    df["Discount_Tier"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    # Profitability flag
    df["Is_Profitable"] = df["Profit"] > 0

    # Format dates as YYYY-MM-DD strings for CSV export
    df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
    df["Ship_Date"] = df["Ship_Date"].dt.strftime("%Y-%m-%d")

    # Sort deterministically
    df = df.sort_values(by=["Order_Date", "Order_ID"]).reset_index(drop=True)

    # 8. Export Processed Data
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    df.to_csv(processed_csv_path, index=False)
    
    print("-" * 70)
    print("DATA PIPELINE SUMMARY METRICS:")
    print(f"Total Transactions Cleaned : {len(df):,}")
    print(f"Total Net Sales Revenue    : ${df['Sales'].sum():,.2f}")
    print(f"Total Gross Profit         : ${df['Profit'].sum():,.2f}")
    print(f"Overall Profit Margin      : {(df['Profit'].sum() / df['Sales'].sum()) * 100:.2f}%")
    print(f"Unique Customers           : {df['Customer_ID'].nunique():,}")
    print(f"Unique Orders              : {df['Order_ID'].nunique():,}")
    print(f"Average Order Value (AOV)  : ${df.groupby('Order_ID')['Sales'].sum().mean():,.2f}")
    print(f"Average Fulfillment Days   : {df['Order_to_Ship_Days'].mean():.2f} days")
    print(f"[+] Output saved to: {processed_csv_path}")
    print("=" * 70)
    
    return df

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    raw_path = os.path.join(project_root, "data", "raw", "retail_sales_raw.csv")
    clean_path = os.path.join(project_root, "data", "processed", "retail_sales_clean.csv")
    clean_retail_data(raw_path, clean_path)

if __name__ == "__main__":
    main()
