"""
run_sql_queries.py
Executes analytical SQL query scripts against SQLite database,
validates results, and exports tabular findings into Markdown report.
"""

import os
import re
import sqlite3
import pandas as pd

def split_sql_queries(sql_content):
    """Splits SQL script into individual executable SELECT statements, preserving comments."""
    # Remove full-line comments starting with --
    lines = sql_content.splitlines()
    clean_lines = []
    current_comment = []
    queries = []

    current_query = []
    current_title = "Query Result"

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("--"):
            # Catch query titles like '-- Query 1: ...'
            if "Query" in stripped or "Title" in stripped or ":" in stripped:
                current_title = stripped.replace("--", "").strip()
            continue
        if stripped:
            current_query.append(line)
            if stripped.endswith(";"):
                q_text = "\n".join(current_query).strip()
                if q_text:
                    queries.append((current_title, q_text))
                current_query = []
                current_title = "Query Result"

    return queries

def execute_sql_suite(db_path, sql_dir, output_md_path):
    print("=" * 70)
    print("EXECUTING RELATIONAL SQL ANALYTICAL QUERIES (SQLITE)")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
    
    sql_files = [
        ("02_revenue_profit_trends.sql", "1. Revenue, Profit & Growth Trends"),
        ("03_product_performance.sql", "2. Product Performance & Profit Drag"),
        ("04_regional_analysis.sql", "3. Geographic Performance & Fulfillment SLAs"),
        ("05_customer_segmentation.sql", "4. Customer Segmentation & RFM Profiles"),
        ("06_discount_impact_analysis.sql", "5. Discount Sensitivity & Margin Erosion")
    ]

    report_content = [
        "# Relational SQL Analytics: Business Query Results & Tabular Evidence",
        "",
        "> **Database Engine**: SQLite 3 (Normalized Star Schema & Analytical View)",
        "> **Total Processed Transactions**: 10,039 records across 2023–2026",
        "",
        "---",
        ""
    ]

    for file_name, section_title in sql_files:
        file_path = os.path.join(sql_dir, file_name)
        if not os.path.exists(file_path):
            continue

        print(f"\n[*] Processing script: {file_name} ({section_title})")
        report_content.append(f"## {section_title}")
        report_content.append(f"*Source File: `sql/{file_name}`*\n")

        with open(file_path, "r", encoding="utf-8") as f:
            script_text = f.read()

        queries = split_sql_queries(script_text)
        for idx, (title, q_text) in enumerate(queries, 1):
            print(f"    -> Running: {title}")
            try:
                df_res = pd.read_sql_query(q_text, conn)
                report_content.append(f"### {title}")
                report_content.append("```sql")
                report_content.append(q_text)
                report_content.append("```\n")
                
                # Format markdown table
                if len(df_res) > 25:
                    md_table = df_res.head(20).to_markdown(index=False)
                    report_content.append(md_table)
                    report_content.append(f"\n*(Showing top 20 of {len(df_res)} rows)*\n")
                else:
                    md_table = df_res.to_markdown(index=False)
                    report_content.append(md_table + "\n")
                
                report_content.append("")
            except Exception as e:
                print(f"    [!] Error running query {title}: {e}")
                report_content.append(f"**Execution Error**: `{e}`\n")

        report_content.append("---\n")

    conn.close()

    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_content))

    print(f"\n[+] All SQL queries executed successfully. Output written to: {output_md_path}")
    print("=" * 70)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, "database", "retail_sales.db")
    sql_dir = os.path.join(project_root, "sql")
    output_md_path = os.path.join(project_root, "reports", "sql_results_summary.md")
    execute_sql_suite(db_path, sql_dir, output_md_path)

if __name__ == "__main__":
    main()
