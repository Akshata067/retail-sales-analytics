"""
eda_analysis.py
Exploratory Data Analysis (EDA) & Visualization Suite.
Generates 5 publication-quality business figures exploring revenue trends,
profitability drivers, discount elasticity, geographic performance, and customer segmentation.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Style settings for publication-grade executive visuals
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Arial"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8

def generate_eda_figures(csv_path, figures_dir):
    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS (EDA) & CHART GENERATION")
    print("=" * 70)
    
    os.makedirs(figures_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    
    # -------------------------------------------------------------------------
    # Chart 1: Monthly Sales & Profit Trend (Seasonality)
    # -------------------------------------------------------------------------
    print("[*] Generating Chart 1: Monthly Revenue & Profit Time Series...")
    monthly = df.groupby("Order_Month_Year").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    monthly["Sales_k"] = monthly["Sales"] / 1000
    monthly["Profit_k"] = monthly["Profit"] / 1000

    fig, ax1 = plt.subplots(figsize=(14, 6))
    x_indices = np.arange(len(monthly))

    # Sales bars
    bars = ax1.bar(x_indices - 0.15, monthly["Sales_k"], width=0.4, label="Sales ($k)", color="#3B82F6", alpha=0.85)
    ax1.set_ylabel("Sales ($ Thousands)", color="#1E3A8A", fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#1E3A8A")

    # Profit line on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x_indices + 0.15, monthly["Profit_k"], color="#10B981", linewidth=2.5, marker="o", label="Profit ($k)")
    ax2.set_ylabel("Profit ($ Thousands)", color="#065F46", fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#065F46")
    ax2.grid(False)

    # Format X-axis ticks (sample every 2-3 months for legibility)
    step = 2
    ax1.set_xticks(x_indices[::step])
    ax1.set_xticklabels(monthly["Order_Month_Year"].iloc[::step], rotation=45, ha="right", fontsize=9)
    ax1.set_title("Monthly Sales Revenue and Net Profit Trend (2023 - 2026)\nClear Q4 Holiday Surges & Consistent Profitability", fontsize=13, fontweight="bold", pad=15)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

    plt.tight_layout()
    chart1_path = os.path.join(figures_dir, "01_monthly_sales_profit_trend.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"    Saved: {chart1_path}")

    # -------------------------------------------------------------------------
    # Chart 2: Sub-Category Profitability Matrix (Profitable vs Loss-Makers)
    # -------------------------------------------------------------------------
    print("[*] Generating Chart 2: Sub-Category Profit Performance...")
    subcat = df.groupby(["Category", "Sub_Category"]).agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    subcat["Profit_Margin_%"] = (subcat["Profit"] / subcat["Sales"]) * 100
    subcat = subcat.sort_values(by="Profit", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ["#EF4444" if p < 0 else "#0EA5E9" for p in subcat["Profit"]]
    
    bars = ax.barh(subcat["Sub_Category"], subcat["Profit"] / 1000, color=colors, height=0.65, edgecolor="#334155", linewidth=0.5)
    ax.axvline(0, color="#64748B", linewidth=1.2, linestyle="--")
    
    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ha = "left" if width >= 0 else "right"
        offset = 5 if width >= 0 else -5
        ax.annotate(f"${width:,.1f}k",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(offset, 0), textcoords="offset points",
                    ha=ha, va="center", fontsize=8.5, fontweight="bold",
                    color="#0F172A")

    ax.set_xlabel("Net Cumulative Profit ($ Thousands)", fontsize=11, fontweight="bold")
    ax.set_title("Product Sub-Category Profitability Ranking\nRed Highlights Sub-Categories Operating at a Cumulative Loss", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    chart2_path = os.path.join(figures_dir, "02_category_subcategory_profit.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"    Saved: {chart2_path}")

    # -------------------------------------------------------------------------
    # Chart 3: Discount vs Profit Margin Box Plot (Elasticity & Thresholds)
    # -------------------------------------------------------------------------
    print("[*] Generating Chart 3: Discount Tier vs Profit Margin Distribution...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tier_order = ["0% None", "1-10% Low", "11-20% Moderate", "21-40% High", ">40% Deep"]
    palette = ["#10B981", "#3B82F6", "#F59E0B", "#F97316", "#EF4444"]
    
    sns.boxplot(x="Discount_Tier", y=df["Profit_Margin"] * 100, hue="Discount_Tier", data=df, order=tier_order, palette=palette, ax=ax, width=0.5, fliersize=2, legend=False)
    ax.axhline(0, color="#DC2626", linestyle="--", linewidth=1.5, label="Break-Even Threshold (0% Margin)")
    
    ax.set_ylabel("Profit Margin (%)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Discount Tier Applied", fontsize=11, fontweight="bold")
    ax.set_title("Impact of Discount Tiers on Transaction Profit Margin\nMargins Erode Precipitous into Negative Territory Beyond 20% Discount", fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower left", frameon=True)
    
    plt.tight_layout()
    chart3_path = os.path.join(figures_dir, "03_discount_vs_profit_margin.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"    Saved: {chart3_path}")

    # -------------------------------------------------------------------------
    # Chart 4: Regional Revenue and Profit Margin Comparison
    # -------------------------------------------------------------------------
    print("[*] Generating Chart 4: Regional Performance Comparison...")
    region_summary = df.groupby("Region").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    region_summary["Profit_Margin_%"] = (region_summary["Profit"] / region_summary["Sales"]) * 100
    region_summary = region_summary.sort_values(by="Sales", ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    x = np.arange(len(region_summary))
    width = 0.45

    rects1 = ax1.bar(x, region_summary["Sales"] / 1000, width, label="Sales ($k)", color="#6366F1", alpha=0.9)
    ax1.set_ylabel("Total Sales ($ Thousands)", color="#312E81", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(region_summary["Region"], fontsize=11, fontweight="bold")

    # Margin percentage on secondary axis
    ax2 = ax1.twinx()
    rects2 = ax2.plot(x, region_summary["Profit_Margin_%"], color="#F59E0B", marker="D", markersize=8, linewidth=2.5, label="Profit Margin %")
    ax2.set_ylabel("Profit Margin (%)", color="#B45309", fontsize=11, fontweight="bold")
    ax2.grid(False)

    for i, v in enumerate(region_summary["Profit_Margin_%"]):
        ax2.annotate(f"{v:.1f}%", (x[i], v + 0.5), ha="center", fontsize=10, fontweight="bold", color="#B45309")

    ax1.set_title("Geographic Performance: Sales Revenue vs. Net Profit Margin %\nWest and East Regions Drive Core Volume & Higher Margins", fontsize=13, fontweight="bold", pad=15)
    
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right")

    plt.tight_layout()
    chart4_path = os.path.join(figures_dir, "04_regional_performance.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"    Saved: {chart4_path}")

    # -------------------------------------------------------------------------
    # Chart 5: Customer Segment Metrics (Revenue, Profit, AOV)
    # -------------------------------------------------------------------------
    print("[*] Generating Chart 5: Customer Segment Distribution...")
    seg = df.groupby("Segment").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Total_Customers=("Customer_ID", "nunique")
    ).reset_index()
    seg["AOV"] = seg["Total_Sales"] / seg["Total_Orders"]
    seg["Margin_%"] = (seg["Total_Profit"] / seg["Total_Sales"]) * 100

    fig, (ax_donut, ax_aov) = plt.subplots(1, 2, figsize=(14, 6))

    # Donut Chart for Sales Share
    colors_seg = ["#3B82F6", "#10B981", "#8B5CF6"]
    wedges, texts, autotexts = ax_donut.pie(
        seg["Total_Sales"],
        labels=seg["Segment"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_seg,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_color("white")
        at.set_weight("bold")
    ax_donut.set_title("Sales Share by Customer Segment", fontsize=12, fontweight="bold")

    # Bar chart for AOV and Margin
    bars_aov = ax_aov.bar(seg["Segment"], seg["AOV"], color=colors_seg, width=0.5, edgecolor="#334155")
    ax_aov.set_ylabel("Average Order Value ($)", fontsize=11, fontweight="bold")
    ax_aov.set_title("Average Order Value (AOV) by Segment", fontsize=12, fontweight="bold")
    
    for bar in bars_aov:
        yval = bar.get_height()
        ax_aov.annotate(f"${yval:,.2f}",
                        xy=(bar.get_x() + bar.get_width() / 2, yval),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.suptitle("Customer Segment Analysis: Volume vs. Transaction Ticket Size\nConsumer Leads Total Volume While Corporate & Home Office Drive Strong AOV", fontsize=14, fontweight="bold")
    plt.tight_layout()
    chart5_path = os.path.join(figures_dir, "05_customer_segment_distribution.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"    Saved: {chart5_path}")

    print("=" * 70)
    print("[+] All 5 EDA figures generated and saved successfully!")
    print("=" * 70)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "processed", "retail_sales_clean.csv")
    figures_dir = os.path.join(project_root, "reports", "figures")
    generate_eda_figures(csv_path, figures_dir)

if __name__ == "__main__":
    main()
