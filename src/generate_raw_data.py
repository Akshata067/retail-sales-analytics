"""
generate_raw_data.py
Synthesizes a realistic, high-fidelity retail sales dataset (~10,000 transactions)
spanning 2023 to 2026 with intentional real-world data quality anomalies for cleaning.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_retail_dataset(num_records=10000, random_seed=42):
    random.seed(random_seed)
    np.random.seed(random_seed)

    # 1. Product Catalog Definition
    catalog = [
        # Technology
        ("Technology", "Phones", "Apple iPhone 14 Pro 128GB", 899.0, 0.28),
        ("Technology", "Phones", "Samsung Galaxy S23 Ultra", 949.0, 0.26),
        ("Technology", "Phones", "Google Pixel 8 Pro", 799.0, 0.24),
        ("Technology", "Accessories", "Logitech MX Master 3S Mouse", 99.0, 0.42),
        ("Technology", "Accessories", "Anker USB-C Multi-Port Hub", 49.0, 0.45),
        ("Technology", "Accessories", "Belkin Wireless Charging Stand", 39.0, 0.38),
        ("Technology", "Copiers", "Canon ImageRunner Enterprise Copier", 2800.0, 0.48),
        ("Technology", "Copiers", "HP LaserJet Enterprise MFP 500", 1850.0, 0.40),
        ("Technology", "Machines", "Zebra Thermal Barcode Printer", 450.0, 0.15),
        ("Technology", "Machines", "Cisco Catalyst 24-Port Switch", 620.0, 0.18),

        # Furniture
        ("Furniture", "Chairs", "Herman Miller Aeron Ergonomic Chair", 850.0, 0.22),
        ("Furniture", "Chairs", "Steelcase Series 1 Task Chair", 420.0, 0.20),
        ("Furniture", "Chairs", "HON Volt Armless Mesh Office Chair", 160.0, 0.18),
        ("Furniture", "Tables", "Uplift V2 Standing Executive Desk", 680.0, 0.08),
        ("Furniture", "Tables", "Bush Business Conference Table 8ft", 920.0, 0.05),
        ("Furniture", "Tables", "Safco Training Seminar Flip Table", 340.0, 0.06),
        ("Furniture", "Bookcases", "Bush Furniture 5-Shelf Bookcase", 220.0, 0.07),
        ("Furniture", "Bookcases", "Sauder Heritage Library Bookcase", 310.0, 0.08),
        ("Furniture", "Furnishings", "Deflecto Floor Chair Mat 48x60", 45.0, 0.32),
        ("Furniture", "Furnishings", "3M Privacy Filter for 27in Monitor", 65.0, 0.35),
        ("Furniture", "Furnishings", "Globe Electric LED Task Desk Lamp", 38.0, 0.30),

        # Office Supplies
        ("Office Supplies", "Storage", "Fellowes Bankers Heavy-Duty Boxes 12pk", 48.0, 0.25),
        ("Office Supplies", "Storage", "Akro-Mils Industrial Plastic Storage Bins", 32.0, 0.28),
        ("Office Supplies", "Binders", "Avery Heavy-Duty 3-Ring Binder 2in", 12.0, 0.40),
        ("Office Supplies", "Binders", "Wilson Jones ClearVue Locking Binder", 18.0, 0.42),
        ("Office Supplies", "Paper", "Hammermill Copy Plus Paper 20lb 500ct", 14.0, 0.35),
        ("Office Supplies", "Paper", "HP Premium Multi-Purpose Laser Paper", 22.0, 0.38),
        ("Office Supplies", "Appliances", "Keurig K-Elite Office Coffee Maker", 160.0, 0.22),
        ("Office Supplies", "Appliances", "Fellowes Powershred Cross-Cut Shredder", 130.0, 0.25),
        ("Office Supplies", "Envelopes", "Quality Park Security Tint Envelopes 500pk", 28.0, 0.36),
        ("Office Supplies", "Labels", "Avery Address Mailing Labels 750pk", 16.0, 0.44),
        ("Office Supplies", "Art", "Prismacolor Premier Colored Pencils 48ct", 42.0, 0.35),
        ("Office Supplies", "Fasteners", "Swingline Heavy-Duty Desk Stapler", 24.0, 0.32),
        ("Office Supplies", "Supplies", "Fiskars Heavy Duty Precision Titanium Shears", 26.0, 0.12),
        ("Office Supplies", "Supplies", "Dahle Professional Rolling Trimmer 18in", 110.0, 0.10)
    ]

    # 2. Regional Geography
    geography = [
        ("West", "California", "Los Angeles", "90036"),
        ("West", "California", "San Francisco", "94107"),
        ("West", "California", "San Diego", "92101"),
        ("West", "Washington", "Seattle", "98101"),
        ("West", "Washington", "Spokane", "99201"),
        ("West", "Arizona", "Phoenix", "85001"),
        ("West", "Colorado", "Denver", "80202"),
        ("West", "Nevada", "Las Vegas", "89101"),
        ("West", "Oregon", "Portland", "97201"),

        ("East", "New York", "New York City", "10024"),
        ("East", "New York", "Buffalo", "14201"),
        ("East", "Pennsylvania", "Philadelphia", "19104"),
        ("East", "Pennsylvania", "Pittsburgh", "15213"),
        ("East", "Massachusetts", "Boston", "02115"),
        ("East", "Ohio", "Columbus", "43215"),
        ("East", "New Jersey", "Newark", "07102"),

        ("Central", "Illinois", "Chicago", "60605"),
        ("Central", "Illinois", "Naperville", "60540"),
        ("Central", "Texas", "Houston", "77095"),
        ("Central", "Texas", "Dallas", "75201"),
        ("Central", "Texas", "Austin", "78701"),
        ("Central", "Michigan", "Detroit", "48201"),
        ("Central", "Indiana", "Indianapolis", "46204"),
        ("Central", "Wisconsin", "Milwaukee", "53202"),

        ("South", "Florida", "Miami", "33101"),
        ("South", "Florida", "Orlando", "32801"),
        ("South", "Florida", "Tampa", "33602"),
        ("South", "North Carolina", "Charlotte", "28202"),
        ("South", "Georgia", "Atlanta", "30303"),
        ("South", "Virginia", "Richmond", "23219"),
        ("South", "Tennessee", "Nashville", "37201")
    ]

    # 3. Customer Base (~600 distinct customers)
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young"
    ]
    segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.52, 0.30, 0.18]

    customers = []
    for i in range(1, 651):
        c_id = f"CG-{10000 + i}"
        c_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        c_seg = np.random.choice(segments, p=segment_weights)
        c_geo = random.choice(geography)
        customers.append((c_id, c_name, c_seg, c_geo))

    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_mode_weights = [0.60, 0.20, 0.15, 0.05]
    ship_delay_map = {
        "Same Day": (0, 0),
        "First Class": (1, 2),
        "Second Class": (2, 4),
        "Standard Class": (3, 6)
    }

    # 4. Generate Order Line Records
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 10, 20)
    total_days = (end_date - start_date).days

    records = []
    order_seq = 100000

    # Monthly seasonality weights (Jan to Dec: index 0 to 11)
    month_weights = [0.65, 0.60, 0.75, 0.70, 0.80, 0.85, 0.80, 0.90, 1.15, 1.05, 1.40, 1.50]

    for _ in range(num_records):
        # Pick date with seasonal weighting
        day_offset = random.randint(0, total_days)
        curr_date = start_date + timedelta(days=day_offset)
        # Apply rejection sampling for seasonality
        m_weight = month_weights[curr_date.month - 1]
        if random.random() > (m_weight / 1.50):
            day_offset = random.randint(0, total_days)
            curr_date = start_date + timedelta(days=day_offset)

        # Customer selection (Pareto distribution: top 20% order more frequently)
        if random.random() < 0.60:
            cust = random.choice(customers[:130])  # VIP pool
        else:
            cust = random.choice(customers[130:])

        c_id, c_name, c_seg, c_geo = cust
        reg, state, city, post = c_geo

        # Product selection
        prod = random.choice(catalog)
        cat, subcat, prod_name, base_price, base_margin = prod
        prod_id = f"{cat[:3].upper()}-{subcat[:2].upper()}-{random.randint(1000, 9999)}"

        # Quantity
        qty = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=[0.25, 0.25, 0.20, 0.10, 0.08, 0.04, 0.03, 0.02, 0.02, 0.01])

        # Discount (elasticity and promo dynamics)
        discount_choice = np.random.choice(
            [0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.70, 0.80],
            p=[0.45, 0.15, 0.20, 0.08, 0.05, 0.03, 0.02, 0.02]
        )

        # Calculate Sales & Profit
        # Price variation (+/- 5%)
        price_fluct = np.random.uniform(0.95, 1.05)
        item_unit_price = round(base_price * price_fluct, 2)
        gross_sales = round(item_unit_price * qty * (1.0 - discount_choice), 2)

        # Profit logic: COGS is fixed base cost. Heavy items incur higher shipping drag.
        # Heavy categories: Tables, Bookcases, Supplies, Chairs
        shipping_drag_factor = 0.0
        if subcat in ["Tables", "Bookcases"]:
            shipping_drag_factor = 0.18
        elif subcat in ["Chairs", "Machines"]:
            shipping_drag_factor = 0.08

        effective_margin = base_margin - discount_choice - shipping_drag_factor
        # Calculate line item profit
        profit = round(gross_sales * effective_margin, 2)

        # Ship date
        s_mode = np.random.choice(ship_modes, p=ship_mode_weights)
        min_d, max_d = ship_delay_map[s_mode]
        s_date = curr_date + timedelta(days=random.randint(min_d, max_d))

        order_seq += 1
        order_id = f"CA-{curr_date.year}-{order_seq}"

        records.append({
            "Order_ID": order_id,
            "Order_Date": curr_date.strftime("%Y-%m-%d"),
            "Ship_Date": s_date.strftime("%Y-%m-%d"),
            "Ship_Mode": s_mode,
            "Customer_ID": c_id,
            "Customer_Name": c_name,
            "Segment": c_seg,
            "Country": "United States",
            "City": city,
            "State": state,
            "Postal_Code": post,
            "Region": reg,
            "Product_ID": prod_id,
            "Category": cat,
            "Sub_Category": subcat,
            "Product_Name": prod_name,
            "Sales": gross_sales,
            "Quantity": int(qty),
            "Discount": float(discount_choice),
            "Profit": profit
        })

    df = pd.DataFrame(records)

    # 5. Inject Real-World Raw Data Imperfections
    # A) Duplicates (~150 duplicate rows)
    dup_sample = df.sample(n=150, random_state=random_seed)
    df = pd.concat([df, dup_sample], ignore_index=True)

    # B) Missing Postal Codes (~2%)
    missing_zip_indices = df.sample(frac=0.02, random_state=random_seed).index
    df.loc[missing_zip_indices, "Postal_Code"] = np.nan

    # C) Dirty Casing in Text Fields (Category, City)
    dirty_cat_idx = df.sample(frac=0.05, random_state=random_seed).index
    df.loc[dirty_cat_idx, "Category"] = df.loc[dirty_cat_idx, "Category"].apply(
        lambda x: x.lower() if random.random() < 0.5 else x.upper()
    )

    dirty_city_idx = df.sample(frac=0.04, random_state=random_seed).index
    df.loc[dirty_city_idx, "City"] = df.loc[dirty_city_idx, "City"].str.lower()

    # D) Whitespace Padding in Sub_Category
    pad_idx = df.sample(frac=0.06, random_state=random_seed).index
    df.loc[pad_idx, "Sub_Category"] = df.loc[pad_idx, "Sub_Category"].apply(lambda x: f"  {x}  ")

    # E) String formatting on currency for a subset (~5%)
    currency_str_idx = df.sample(frac=0.05, random_state=random_seed).index
    df.loc[currency_str_idx, "Sales"] = df.loc[currency_str_idx, "Sales"].apply(lambda x: f"${x:,.2f}")

    # F) Inconsistent Date Formatting (~5% formatted as MM/DD/YYYY)
    date_format_idx = df.sample(frac=0.05, random_state=random_seed).index
    df.loc[date_format_idx, "Order_Date"] = pd.to_datetime(df.loc[date_format_idx, "Order_Date"]).dt.strftime("%m/%d/%Y")

    return df

def main():
    print("[*] Generating realistic retail sales dataset...")
    df_raw = generate_retail_dataset(num_records=10000, random_seed=42)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    raw_path = os.path.join(project_root, "data", "raw", "retail_sales_raw.csv")

    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    df_raw.to_csv(raw_path, index=False)
    print(f"[+] Successfully wrote {len(df_raw):,} raw records to: {raw_path}")

if __name__ == "__main__":
    main()
