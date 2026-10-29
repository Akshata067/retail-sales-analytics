"""
run_pipeline.py
Master Pipeline Orchestrator for Retail Sales Analytics Project.
Executes end-to-end data generation, cleaning, exploratory visualization,
relational SQLite ingestion, SQL reporting, and Excel workbook compilation.
"""

import os
import sys
import time
import subprocess

def run_step(step_num, title, script_rel_path, project_root, python_exe):
    print("\n" + "=" * 78)
    print(f"STAGE {step_num}: {title.upper()}")
    print("=" * 78)
    script_path = os.path.join(project_root, script_rel_path)
    start_time = time.time()
    
    cmd = [python_exe, script_path]
    result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        # Filter benign warnings
        filtered_err = "\n".join([line for line in result.stderr.splitlines() if "FutureWarning" not in line and "UserWarning" not in line])
        if filtered_err.strip():
            print(f"[!] Warning/Stderr:\n{filtered_err.strip()}")

    if result.returncode != 0:
        print(f"\n[X] STAGE {step_num} FAILED with return code {result.returncode}!")
        sys.exit(result.returncode)

    elapsed = time.time() - start_time
    print(f"[+] Completed Stage {step_num} in {elapsed:.2f} seconds.")

def main():
    start_total = time.time()
    project_root = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable

    print("\n" + "#" * 78)
    print("# GLOBAL RETAIL CORP - MASTER ANALYTICS PIPELINE RUNNER")
    print("# Python, SQLite (SQL), Excel (.xlsx), Power BI & Executive Reporting")
    print("#" * 78)

    # Stage 1: Data Generation
    run_step(1, "Synthesizing Raw Transactions with Quality Imperfections", 
             os.path.join("src", "generate_raw_data.py"), project_root, python_exe)

    # Stage 2: Data Cleaning & Feature Engineering
    run_step(2, "Cleaning Data, Handling Nulls/Duplicates & Feature Engineering", 
             os.path.join("src", "data_cleaning.py"), project_root, python_exe)

    # Stage 3: Exploratory Data Analysis & Visual Generation
    run_step(3, "Generating Publication-Grade EDA Figures (Matplotlib & Seaborn)", 
             os.path.join("src", "eda_analysis.py"), project_root, python_exe)

    # Stage 4: SQLite Database ETL & Star Schema Setup
    run_step(4, "Building SQLite Database & Ingesting Relational Star Schema", 
             os.path.join("src", "database_setup.py"), project_root, python_exe)

    # Stage 5: SQL Query Suite Execution & Tabular Export
    run_step(5, "Executing Advanced SQL Analytical Queries & Compiling Report", 
             os.path.join("src", "run_sql_queries.py"), project_root, python_exe)

    # Stage 6: Excel Financial Model Workbook Generation
    run_step(6, "Compiling Formatted Multi-Tab Excel Financial Workbook (.xlsx)", 
             os.path.join("src", "generate_excel_workbook.py"), project_root, python_exe)

    total_time = time.time() - start_total
    print("\n" + "#" * 78)
    print(f"# PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN {total_time:.2f} SECONDS!")
    print("#" * 78)
    print("\nDELIVERABLE ARTIFACT LOCATIONS:")
    print(f"  1. Cleaned CSV       : {os.path.join(project_root, 'data', 'processed', 'retail_sales_clean.csv')}")
    print(f"  2. EDA Charts (5)    : {os.path.join(project_root, 'reports', 'figures')}")
    print(f"  3. SQLite Database   : {os.path.join(project_root, 'database', 'retail_sales.db')}")
    print(f"  4. SQL Results Doc   : {os.path.join(project_root, 'reports', 'sql_results_summary.md')}")
    print(f"  5. Excel Workbook    : {os.path.join(project_root, 'excel', 'Retail_Sales_Analysis.xlsx')}")
    print(f"  6. Power BI Mockup   : {os.path.join(project_root, 'power_bi', 'dashboard_mockup.html')}")
    print(f"  7. Executive Insights: {os.path.join(project_root, 'reports', 'executive_insights_and_recommendations.md')}")
    print(f"  8. Project README    : {os.path.join(project_root, 'README.md')}\n")

if __name__ == "__main__":
    main()
