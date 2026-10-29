"""
generate_excel_workbook.py
Generates an executive-ready, multi-tab Excel financial workbook (Retail_Sales_Analysis.xlsx).
Incorporates formatted raw data, dynamic Excel formulas (SUMIFS, AVERAGE, RATIOS),
Pivot-style summary tabs, professional styling, and an Executive Summary dashboard.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

def build_excel_model(clean_csv_path, excel_output_path):
    print("=" * 70)
    print("BUILDING EXECUTIVE EXCEL ANALYTICS WORKBOOK")
    print("=" * 70)

    # Ingest clean data
    print(f"[*] Reading cleaned dataset from: {clean_csv_path}")
    df = pd.read_csv(clean_csv_path)
    total_rows = len(df)
    data_last_row = total_rows + 1

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------------------
    # Styles & Palettes (Modern Corporate Executive Theme)
    # -------------------------------------------------------------------------
    font_family = "Segoe UI"
    
    font_title = Font(name=font_family, size=16, bold=True, color="1E3A8A")
    font_subtitle = Font(name=font_family, size=11, italic=True, color="475569")
    font_sec_hdr = Font(name=font_family, size=13, bold=True, color="0F172A")
    font_tbl_hdr = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    font_kpi_lbl = Font(name=font_family, size=9, bold=True, color="64748B")
    font_kpi_val = Font(name=font_family, size=18, bold=True, color="1E3A8A")
    font_data = Font(name=font_family, size=10, color="0F172A")
    font_bold = Font(name=font_family, size=10, bold=True, color="0F172A")
    font_alert = Font(name=font_family, size=10, bold=True, color="DC2626")
    font_positive = Font(name=font_family, size=10, bold=True, color="16A34A")

    fill_navy = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_slate = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    fill_kpi_bg = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_tot = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_warn = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1")
    )
    top_thin_bot_double = Border(
        top=Side(style="thin", color="0F172A"),
        bottom=Side(style="double", color="0F172A")
    )

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    num_fmt_curr = "$#,##0.00"
    num_fmt_curr_int = "$#,##0"
    num_fmt_int = "#,##0"
    num_fmt_pct = "0.0%"
    num_fmt_pct2 = "0.00%"

    # =========================================================================
    # TAB 1: Executive Summary
    # =========================================================================
    print("[*] Creating Sheet 1: Executive Summary Dashboard...")
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True

    # Title block
    ws_exec["B2"] = "GLOBAL RETAIL CORP - EXECUTIVE PERFORMANCE REPORT"
    ws_exec["B2"].font = font_title
    ws_exec["B3"] = "Enterprise Sales, Profitability, Geographic Opportunities & Discount Elasticity (2023 - 2026)"
    ws_exec["B3"].font = font_subtitle

    # KPI Summary Cards Block (Rows 5-7)
    kpis = [
        ("TOTAL REVENUE", f"=SUM('Cleaned Data'!Q2:Q{data_last_row})", num_fmt_curr, "B", "C"),
        ("TOTAL PROFIT", f"=SUM('Cleaned Data'!T2:T{data_last_row})", num_fmt_curr, "E", "F"),
        ("PROFIT MARGIN %", f"=E6/B6", num_fmt_pct, "H", "I"),
        ("TOTAL ORDERS", f"=COUNT('Cleaned Data'!A2:A{data_last_row})", num_fmt_int, "K", "L"),
        ("AVG ORDER VALUE", f"=B6/K6", num_fmt_curr, "N", "O")
    ]

    for label, formula, fmt, col1, col2 in kpis:
        # Merge top cell for label
        ws_exec.merge_cells(f"{col1}5:{col2}5")
        ws_exec[f"{col1}5"] = label
        ws_exec[f"{col1}5"].font = font_kpi_lbl
        ws_exec[f"{col1}5"].alignment = align_center
        ws_exec[f"{col1}5"].fill = fill_kpi_bg

        # Merge value cell
        ws_exec.merge_cells(f"{col1}6:{col2}7")
        ws_exec[f"{col1}6"] = formula
        ws_exec[f"{col1}6"].font = font_kpi_val
        ws_exec[f"{col1}6"].alignment = align_center
        ws_exec[f"{col1}6"].number_format = fmt
        ws_exec[f"{col1}6"].fill = fill_kpi_bg

        # Apply borders
        for r in range(5, 8):
            for c in [col1, col2]:
                ws_exec[f"{c}{r}"].border = thin_border

    # Strategic Findings Section
    ws_exec["B9"] = "KEY STRATEGIC INSIGHTS & QUANTIFIED EVIDENCE"
    ws_exec["B9"].font = font_sec_hdr

    insights = [
        ("1. High Profit Bleed in Furniture", 
         "Tables and Bookcases generate -$372,783 in cumulative losses due to high shipping drag and discounting > 20%."),
        ("2. Copiers & Technology Outperform", 
         "Technology delivers $1.45M in total profit (Copiers achieve 33.9% net margin), representing 80%+ of firm profitability."),
        ("3. Severe Margin Collapse Beyond 20% Discount", 
         "Transactions discounted over 20% experience an average margin of -8.9% to -38.5%, eroding $253,959 in potential EBITDA."),
        ("4. West and Central Fuel Core Volume", 
         "West and Central account for 63.3% of total revenue ($6.08M) and $776K in profit, with California and Texas leading.")
    ]

    for idx, (title, detail) in enumerate(insights, start=10):
        ws_exec[f"B{idx}"] = title
        ws_exec[f"B{idx}"].font = font_bold
        ws_exec.merge_cells(f"E{idx}:O{idx}")
        ws_exec[f"E{idx}"] = detail
        ws_exec[f"E{idx}"].font = font_data
        ws_exec[f"B{idx}"].border = thin_border
        for col_l in ["E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]:
            ws_exec[f"{col_l}{idx}"].border = thin_border

    # Category High-Level Summary Table in Executive Tab
    ws_exec["B16"] = "CATEGORY PERFORMANCE SNAPSHOT"
    ws_exec["B16"].font = font_sec_hdr

    cat_headers = ["Category", "Total Orders", "Total Units", "Total Sales", "Total Profit", "Profit Margin %"]
    for c_idx, h in enumerate(cat_headers, start=2):
        col_letter = get_column_letter(c_idx)
        ws_exec[f"{col_letter}18"] = h
        ws_exec[f"{col_letter}18"].font = font_tbl_hdr
        ws_exec[f"{col_letter}18"].fill = fill_navy
        ws_exec[f"{col_letter}18"].alignment = align_center

    cats = ["Technology", "Office Supplies", "Furniture"]
    for r_idx, c_name in enumerate(cats, start=19):
        ws_exec[f"B{r_idx}"] = c_name
        ws_exec[f"B{r_idx}"].font = font_bold
        ws_exec[f"B{r_idx}"].border = thin_border

        # Formulas referencing Cleaned Data
        ws_exec[f"C{r_idx}"] = f"=COUNTIF('Cleaned Data'!N2:N{data_last_row}, B{r_idx})"
        ws_exec[f"C{r_idx}"].number_format = num_fmt_int
        ws_exec[f"C{r_idx}"].alignment = align_right
        ws_exec[f"C{r_idx}"].border = thin_border

        ws_exec[f"D{r_idx}"] = f"=SUMIF('Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!R2:R{data_last_row})"
        ws_exec[f"D{r_idx}"].number_format = num_fmt_int
        ws_exec[f"D{r_idx}"].alignment = align_right
        ws_exec[f"D{r_idx}"].border = thin_border

        ws_exec[f"E{r_idx}"] = f"=SUMIF('Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!Q2:Q{data_last_row})"
        ws_exec[f"E{r_idx}"].number_format = num_fmt_curr
        ws_exec[f"E{r_idx}"].alignment = align_right
        ws_exec[f"E{r_idx}"].border = thin_border

        ws_exec[f"F{r_idx}"] = f"=SUMIF('Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!T2:T{data_last_row})"
        ws_exec[f"F{r_idx}"].number_format = num_fmt_curr
        ws_exec[f"F{r_idx}"].alignment = align_right
        ws_exec[f"F{r_idx}"].border = thin_border

        ws_exec[f"G{r_idx}"] = f"=F{r_idx}/E{r_idx}"
        ws_exec[f"G{r_idx}"].number_format = num_fmt_pct
        ws_exec[f"G{r_idx}"].alignment = align_right
        ws_exec[f"G{r_idx}"].border = thin_border

    # Total Row
    tot_r = 22
    ws_exec[f"B{tot_r}"] = "Total Company"
    ws_exec[f"B{tot_r}"].font = font_bold
    ws_exec[f"B{tot_r}"].fill = fill_tot
    ws_exec[f"B{tot_r}"].border = top_thin_bot_double

    ws_exec[f"C{tot_r}"] = f"=SUM(C19:C21)"
    ws_exec[f"C{tot_r}"].number_format = num_fmt_int
    ws_exec[f"C{tot_r}"].font = font_bold
    ws_exec[f"C{tot_r}"].fill = fill_tot
    ws_exec[f"C{tot_r}"].border = top_thin_bot_double

    ws_exec[f"D{tot_r}"] = f"=SUM(D19:D21)"
    ws_exec[f"D{tot_r}"].number_format = num_fmt_int
    ws_exec[f"D{tot_r}"].font = font_bold
    ws_exec[f"D{tot_r}"].fill = fill_tot
    ws_exec[f"D{tot_r}"].border = top_thin_bot_double

    ws_exec[f"E{tot_r}"] = f"=SUM(E19:E21)"
    ws_exec[f"E{tot_r}"].number_format = num_fmt_curr
    ws_exec[f"E{tot_r}"].font = font_bold
    ws_exec[f"E{tot_r}"].fill = fill_tot
    ws_exec[f"E{tot_r}"].border = top_thin_bot_double

    ws_exec[f"F{tot_r}"] = f"=SUM(F19:F21)"
    ws_exec[f"F{tot_r}"].number_format = num_fmt_curr
    ws_exec[f"F{tot_r}"].font = font_bold
    ws_exec[f"F{tot_r}"].fill = fill_tot
    ws_exec[f"F{tot_r}"].border = top_thin_bot_double

    ws_exec[f"G{tot_r}"] = f"=F{tot_r}/E{tot_r}"
    ws_exec[f"G{tot_r}"].number_format = num_fmt_pct
    ws_exec[f"G{tot_r}"].font = font_bold
    ws_exec[f"G{tot_r}"].fill = fill_tot
    ws_exec[f"G{tot_r}"].border = top_thin_bot_double

    # Set column widths for Executive Summary
    exec_col_widths = {"A": 4, "B": 24, "C": 16, "D": 16, "E": 18, "F": 18, "G": 16, "H": 16, "I": 16, "J": 4, "K": 16, "L": 16, "M": 4, "N": 16, "O": 16}
    for col_l, w in exec_col_widths.items():
        ws_exec.column_dimensions[col_l].width = w

    # =========================================================================
    # TAB 2: Cleaned Data
    # =========================================================================
    print("[*] Creating Sheet 2: Cleaned Data Table (10,039 records)...")
    ws_data = wb.create_sheet(title="Cleaned Data")
    ws_data.views.sheetView[0].showGridLines = True

    # Header Row
    cols = list(df.columns)
    for c_idx, col_name in enumerate(cols, start=1):
        cell = ws_data.cell(row=1, column=c_idx, value=col_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_navy
        cell.alignment = align_center

    # Ingest rows
    for r_idx, row in enumerate(df.itertuples(index=False), start=2):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_data.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_data
            
            # Formatting by column type
            col_header = cols[c_idx - 1]
            if col_header in ["Sales", "Profit", "Unit_Price"]:
                cell.number_format = num_fmt_curr
                cell.alignment = align_right
            elif col_header in ["Discount", "Profit_Margin"]:
                cell.number_format = num_fmt_pct
                cell.alignment = align_right
            elif col_header in ["Quantity", "Order_Year", "Order_Month", "Order_to_Ship_Days"]:
                cell.number_format = num_fmt_int
                cell.alignment = align_right
            elif "Date" in col_header:
                cell.alignment = align_center

    # Auto-adjust column widths
    for c_idx, col_name in enumerate(cols, start=1):
        col_letter = get_column_letter(c_idx)
        max_len = max(len(col_name), 10)
        ws_data.column_dimensions[col_letter].width = min(max_len + 4, 32)

    # Freeze top row
    ws_data.freeze_panes = "A2"

    # =========================================================================
    # TAB 3: Pivot_Monthly_Trends
    # =========================================================================
    print("[*] Creating Sheet 3: Pivot Monthly Trends...")
    ws_month = wb.create_sheet(title="Pivot_Monthly_Trends")
    ws_month.views.sheetView[0].showGridLines = True

    ws_month["B2"] = "MONTHLY SALES & PROFITABILITY TIME-SERIES MODEL"
    ws_month["B2"].font = font_title
    ws_month["B3"] = "Calculated via Dynamic SUMIFS Formulas Linked to Cleaned Data"
    ws_month["B3"].font = font_subtitle

    month_hdrs = ["Month-Year", "Orders", "Sales ($)", "Profit ($)", "Profit Margin %", "MoM Growth %", "Cumulative Sales"]
    for c_idx, h in enumerate(month_hdrs, start=2):
        col_letter = get_column_letter(c_idx)
        cell = ws_month[f"{col_letter}5"]
        cell.value = h
        cell.font = font_tbl_hdr
        cell.fill = fill_slate
        cell.alignment = align_center

    # Distinct month-years
    unique_months = sorted(df["Order_Month_Year"].unique())
    for r_idx, m_str in enumerate(unique_months, start=6):
        ws_month[f"B{r_idx}"] = m_str
        ws_month[f"B{r_idx}"].font = font_bold
        ws_month[f"B{r_idx}"].alignment = align_center
        ws_month[f"B{r_idx}"].border = thin_border

        # Orders: COUNTIF on Cleaned Data Order_Month_Year (Col AA)
        ws_month[f"C{r_idx}"] = f"=COUNTIF('Cleaned Data'!AA2:AA{data_last_row}, B{r_idx})"
        ws_month[f"C{r_idx}"].number_format = num_fmt_int
        ws_month[f"C{r_idx}"].alignment = align_right
        ws_month[f"C{r_idx}"].border = thin_border

        # Sales: SUMIF on Cleaned Data Sales (Col Q)
        ws_month[f"D{r_idx}"] = f"=SUMIF('Cleaned Data'!AA2:AA{data_last_row}, B{r_idx}, 'Cleaned Data'!Q2:Q{data_last_row})"
        ws_month[f"D{r_idx}"].number_format = num_fmt_curr
        ws_month[f"D{r_idx}"].alignment = align_right
        ws_month[f"D{r_idx}"].border = thin_border

        # Profit: SUMIF on Cleaned Data Profit (Col T)
        ws_month[f"E{r_idx}"] = f"=SUMIF('Cleaned Data'!AA2:AA{data_last_row}, B{r_idx}, 'Cleaned Data'!T2:T{data_last_row})"
        ws_month[f"E{r_idx}"].number_format = num_fmt_curr
        ws_month[f"E{r_idx}"].alignment = align_right
        ws_month[f"E{r_idx}"].border = thin_border

        # Profit Margin %: Profit / Sales
        ws_month[f"F{r_idx}"] = f"=E{r_idx}/D{r_idx}"
        ws_month[f"F{r_idx}"].number_format = num_fmt_pct
        ws_month[f"F{r_idx}"].alignment = align_right
        ws_month[f"F{r_idx}"].border = thin_border

        # MoM Growth %: (Sales - PrevSales) / PrevSales
        if r_idx == 6:
            ws_month[f"G{r_idx}"] = "-"
            ws_month[f"G{r_idx}"].alignment = align_center
        else:
            ws_month[f"G{r_idx}"] = f"=(D{r_idx}-D{r_idx-1})/D{r_idx-1}"
            ws_month[f"G{r_idx}"].number_format = num_fmt_pct
            ws_month[f"G{r_idx}"].alignment = align_right
        ws_month[f"G{r_idx}"].border = thin_border

        # Cumulative Sales
        if r_idx == 6:
            ws_month[f"H{r_idx}"] = f"=D6"
        else:
            ws_month[f"H{r_idx}"] = f"=H{r_idx-1}+D{r_idx}"
        ws_month[f"H{r_idx}"].number_format = num_fmt_curr
        ws_month[f"H{r_idx}"].alignment = align_right
        ws_month[f"H{r_idx}"].border = thin_border

    # Format widths
    m_col_widths = {"A": 4, "B": 14, "C": 12, "D": 18, "E": 18, "F": 16, "G": 16, "H": 20}
    for col_l, w in m_col_widths.items():
        ws_month.column_dimensions[col_l].width = w

    # =========================================================================
    # TAB 4: Pivot_Product_Performance
    # =========================================================================
    print("[*] Creating Sheet 4: Pivot Product Performance...")
    ws_prod = wb.create_sheet(title="Pivot_Product_Performance")
    ws_prod.views.sheetView[0].showGridLines = True

    ws_prod["B2"] = "PRODUCT CATEGORY & SUB-CATEGORY PROFITABILITY MATRIX"
    ws_prod["B2"].font = font_title
    ws_prod["B3"] = "Evaluates Revenue, Profit, and Identifies Structural Margin Loss by Product Subcategory"
    ws_prod["B3"].font = font_subtitle

    prod_hdrs = ["Category", "Sub-Category", "Order Lines", "Units Sold", "Total Sales", "Total Profit", "Profit Margin %", "Health Status"]
    for c_idx, h in enumerate(prod_hdrs, start=2):
        col_letter = get_column_letter(c_idx)
        cell = ws_prod[f"{col_letter}5"]
        cell.value = h
        cell.font = font_tbl_hdr
        cell.fill = fill_navy
        cell.alignment = align_center

    subcat_list = [
        ("Technology", "Copiers"),
        ("Technology", "Phones"),
        ("Technology", "Accessories"),
        ("Technology", "Machines"),
        ("Furniture", "Furnishings"),
        ("Furniture", "Chairs"),
        ("Furniture", "Bookcases"),
        ("Furniture", "Tables"),
        ("Office Supplies", "Appliances"),
        ("Office Supplies", "Storage"),
        ("Office Supplies", "Art"),
        ("Office Supplies", "Paper"),
        ("Office Supplies", "Binders"),
        ("Office Supplies", "Envelopes"),
        ("Office Supplies", "Labels"),
        ("Office Supplies", "Fasteners"),
        ("Office Supplies", "Supplies")
    ]

    for r_idx, (cat_val, sub_val) in enumerate(subcat_list, start=6):
        ws_prod[f"B{r_idx}"] = cat_val
        ws_prod[f"B{r_idx}"].font = font_bold
        ws_prod[f"B{r_idx}"].border = thin_border

        ws_prod[f"C{r_idx}"] = sub_val
        ws_prod[f"C{r_idx}"].font = font_data
        ws_prod[f"C{r_idx}"].border = thin_border

        # Order Lines: COUNTIFS
        ws_prod[f"D{r_idx}"] = f"=COUNTIFS('Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!O2:O{data_last_row}, C{r_idx})"
        ws_prod[f"D{r_idx}"].number_format = num_fmt_int
        ws_prod[f"D{r_idx}"].alignment = align_right
        ws_prod[f"D{r_idx}"].border = thin_border

        # Units Sold: SUMIFS on Quantity (Col R)
        ws_prod[f"E{r_idx}"] = f"=SUMIFS('Cleaned Data'!R2:R{data_last_row}, 'Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!O2:O{data_last_row}, C{r_idx})"
        ws_prod[f"E{r_idx}"].number_format = num_fmt_int
        ws_prod[f"E{r_idx}"].alignment = align_right
        ws_prod[f"E{r_idx}"].border = thin_border

        # Total Sales: SUMIFS on Sales (Col Q)
        ws_prod[f"F{r_idx}"] = f"=SUMIFS('Cleaned Data'!Q2:Q{data_last_row}, 'Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!O2:O{data_last_row}, C{r_idx})"
        ws_prod[f"F{r_idx}"].number_format = num_fmt_curr
        ws_prod[f"F{r_idx}"].alignment = align_right
        ws_prod[f"F{r_idx}"].border = thin_border

        # Total Profit: SUMIFS on Profit (Col T)
        ws_prod[f"G{r_idx}"] = f"=SUMIFS('Cleaned Data'!T2:T{data_last_row}, 'Cleaned Data'!N2:N{data_last_row}, B{r_idx}, 'Cleaned Data'!O2:O{data_last_row}, C{r_idx})"
        ws_prod[f"G{r_idx}"].number_format = num_fmt_curr
        ws_prod[f"G{r_idx}"].alignment = align_right
        ws_prod[f"G{r_idx}"].border = thin_border

        # Margin %: Profit / Sales
        ws_prod[f"H{r_idx}"] = f"=G{r_idx}/F{r_idx}"
        ws_prod[f"H{r_idx}"].number_format = num_fmt_pct
        ws_prod[f"H{r_idx}"].alignment = align_right
        ws_prod[f"H{r_idx}"].border = thin_border

        # Health Status: IF(G{r_idx}<0, "LOSS MAKER", "PROFITABLE")
        ws_prod[f"I{r_idx}"] = f'=IF(G{r_idx}<0, "LOSS MAKER", IF(H{r_idx}>0.2, "STAR PERFORMER", "STABLE"))'
        ws_prod[f"I{r_idx}"].alignment = align_center
        ws_prod[f"I{r_idx}"].font = font_bold
        ws_prod[f"I{r_idx}"].border = thin_border

    # Format widths
    p_col_widths = {"A": 4, "B": 18, "C": 18, "D": 14, "E": 14, "F": 18, "G": 18, "H": 16, "I": 20}
    for col_l, w in p_col_widths.items():
        ws_prod.column_dimensions[col_l].width = w

    # =========================================================================
    # TAB 5: Pivot_Regional_Analysis
    # =========================================================================
    print("[*] Creating Sheet 5: Pivot Regional Analysis...")
    ws_reg = wb.create_sheet(title="Pivot_Regional_Analysis")
    ws_reg.views.sheetView[0].showGridLines = True

    ws_reg["B2"] = "GEOGRAPHIC REGIONAL PERFORMANCE & LOGISTICS REPORT"
    ws_reg["B2"].font = font_title
    ws_reg["B3"] = "Regional Sales Distribution, Margins, and Average Fulfillment Lead Times"
    ws_reg["B3"].font = font_subtitle

    reg_hdrs = ["Region", "Transactions", "Total Sales ($)", "Total Profit ($)", "Profit Margin %", "Sales Share %", "Avg Ship Days"]
    for c_idx, h in enumerate(reg_hdrs, start=2):
        col_letter = get_column_letter(c_idx)
        cell = ws_reg[f"{col_letter}5"]
        cell.value = h
        cell.font = font_tbl_hdr
        cell.fill = fill_slate
        cell.alignment = align_center

    regions = ["West", "Central", "South", "East"]
    for r_idx, reg_val in enumerate(regions, start=6):
        ws_reg[f"B{r_idx}"] = reg_val
        ws_reg[f"B{r_idx}"].font = font_bold
        ws_reg[f"B{r_idx}"].border = thin_border

        # Transactions: COUNTIF on Region (Col L)
        ws_reg[f"C{r_idx}"] = f"=COUNTIF('Cleaned Data'!L2:L{data_last_row}, B{r_idx})"
        ws_reg[f"C{r_idx}"].number_format = num_fmt_int
        ws_reg[f"C{r_idx}"].alignment = align_right
        ws_reg[f"C{r_idx}"].border = thin_border

        # Sales: SUMIF on Sales (Col Q)
        ws_reg[f"D{r_idx}"] = f"=SUMIF('Cleaned Data'!L2:L{data_last_row}, B{r_idx}, 'Cleaned Data'!Q2:Q{data_last_row})"
        ws_reg[f"D{r_idx}"].number_format = num_fmt_curr
        ws_reg[f"D{r_idx}"].alignment = align_right
        ws_reg[f"D{r_idx}"].border = thin_border

        # Profit: SUMIF on Profit (Col T)
        ws_reg[f"E{r_idx}"] = f"=SUMIF('Cleaned Data'!L2:L{data_last_row}, B{r_idx}, 'Cleaned Data'!T2:T{data_last_row})"
        ws_reg[f"E{r_idx}"].number_format = num_fmt_curr
        ws_reg[f"E{r_idx}"].alignment = align_right
        ws_reg[f"E{r_idx}"].border = thin_border

        # Margin %: Profit / Sales
        ws_reg[f"F{r_idx}"] = f"=E{r_idx}/D{r_idx}"
        ws_reg[f"F{r_idx}"].number_format = num_fmt_pct
        ws_reg[f"F{r_idx}"].alignment = align_right
        ws_reg[f"F{r_idx}"].border = thin_border

        # Sales Share %
        ws_reg[f"G{r_idx}"] = f"=D{r_idx}/D10"
        ws_reg[f"G{r_idx}"].number_format = num_fmt_pct
        ws_reg[f"G{r_idx}"].alignment = align_right
        ws_reg[f"G{r_idx}"].border = thin_border

        # Avg Ship Days: AVERAGEIF on Order_to_Ship_Days (Col AC)
        ws_reg[f"H{r_idx}"] = f"=AVERAGEIF('Cleaned Data'!L2:L{data_last_row}, B{r_idx}, 'Cleaned Data'!AC2:AC{data_last_row})"
        ws_reg[f"H{r_idx}"].number_format = "0.00"
        ws_reg[f"H{r_idx}"].alignment = align_right
        ws_reg[f"H{r_idx}"].border = thin_border

    # Total Row
    ws_reg["B10"] = "Total Company"
    ws_reg["B10"].font = font_bold
    ws_reg["B10"].fill = fill_tot
    ws_reg["B10"].border = top_thin_bot_double

    for col_c, fmt in [("C", num_fmt_int), ("D", num_fmt_curr), ("E", num_fmt_curr)]:
        ws_reg[f"{col_c}10"] = f"=SUM({col_c}6:{col_c}9)"
        ws_reg[f"{col_c}10"].font = font_bold
        ws_reg[f"{col_c}10"].fill = fill_tot
        ws_reg[f"{col_c}10"].number_format = fmt
        ws_reg[f"{col_c}10"].border = top_thin_bot_double

    ws_reg["F10"] = "=E10/D10"
    ws_reg["F10"].font = font_bold
    ws_reg["F10"].fill = fill_tot
    ws_reg["F10"].number_format = num_fmt_pct
    ws_reg["F10"].border = top_thin_bot_double

    ws_reg["G10"] = "=1.0"
    ws_reg["G10"].font = font_bold
    ws_reg["G10"].fill = fill_tot
    ws_reg["G10"].number_format = num_fmt_pct
    ws_reg["G10"].border = top_thin_bot_double

    ws_reg["H10"] = f"=AVERAGE('Cleaned Data'!AC2:AC{data_last_row})"
    ws_reg["H10"].font = font_bold
    ws_reg["H10"].fill = fill_tot
    ws_reg["H10"].number_format = "0.00"
    ws_reg["H10"].border = top_thin_bot_double

    # Widths
    r_col_widths = {"A": 4, "B": 18, "C": 16, "D": 20, "E": 20, "F": 16, "G": 16, "H": 16}
    for col_l, w in r_col_widths.items():
        ws_reg.column_dimensions[col_l].width = w

    # =========================================================================
    # TAB 6: Customer_Segments
    # =========================================================================
    print("[*] Creating Sheet 6: Customer Segments...")
    ws_cust = wb.create_sheet(title="Customer_Segments")
    ws_cust.views.sheetView[0].showGridLines = True

    ws_cust["B2"] = "CUSTOMER SEGMENT UNIT ECONOMICS & AOV ANALYSIS"
    ws_cust["B2"].font = font_title
    ws_cust["B3"] = "Compares Consumer, Corporate, and Home Office Segments Across Volumes and Margins"
    ws_cust["B3"].font = font_subtitle

    cust_hdrs = ["Segment", "Transactions", "Units Sold", "Total Sales ($)", "Total Profit ($)", "Profit Margin %", "Average Ticket ($)"]
    for c_idx, h in enumerate(cust_hdrs, start=2):
        col_letter = get_column_letter(c_idx)
        cell = ws_cust[f"{col_letter}5"]
        cell.value = h
        cell.font = font_tbl_hdr
        cell.fill = fill_navy
        cell.alignment = align_center

    segs = ["Consumer", "Corporate", "Home Office"]
    for r_idx, s_val in enumerate(segs, start=6):
        ws_cust[f"B{r_idx}"] = s_val
        ws_cust[f"B{r_idx}"].font = font_bold
        ws_cust[f"B{r_idx}"].border = thin_border

        # Transactions
        ws_cust[f"C{r_idx}"] = f"=COUNTIF('Cleaned Data'!G2:G{data_last_row}, B{r_idx})"
        ws_cust[f"C{r_idx}"].number_format = num_fmt_int
        ws_cust[f"C{r_idx}"].alignment = align_right
        ws_cust[f"C{r_idx}"].border = thin_border

        # Units Sold
        ws_cust[f"D{r_idx}"] = f"=SUMIF('Cleaned Data'!G2:G{data_last_row}, B{r_idx}, 'Cleaned Data'!R2:R{data_last_row})"
        ws_cust[f"D{r_idx}"].number_format = num_fmt_int
        ws_cust[f"D{r_idx}"].alignment = align_right
        ws_cust[f"D{r_idx}"].border = thin_border

        # Total Sales
        ws_cust[f"E{r_idx}"] = f"=SUMIF('Cleaned Data'!G2:G{data_last_row}, B{r_idx}, 'Cleaned Data'!Q2:Q{data_last_row})"
        ws_cust[f"E{r_idx}"].number_format = num_fmt_curr
        ws_cust[f"E{r_idx}"].alignment = align_right
        ws_cust[f"E{r_idx}"].border = thin_border

        # Total Profit
        ws_cust[f"F{r_idx}"] = f"=SUMIF('Cleaned Data'!G2:G{data_last_row}, B{r_idx}, 'Cleaned Data'!T2:T{data_last_row})"
        ws_cust[f"F{r_idx}"].number_format = num_fmt_curr
        ws_cust[f"F{r_idx}"].alignment = align_right
        ws_cust[f"F{r_idx}"].border = thin_border

        # Margin %
        ws_cust[f"G{r_idx}"] = f"=F{r_idx}/E{r_idx}"
        ws_cust[f"G{r_idx}"].number_format = num_fmt_pct
        ws_cust[f"G{r_idx}"].alignment = align_right
        ws_cust[f"G{r_idx}"].border = thin_border

        # Average Ticket: Sales / Transactions
        ws_cust[f"H{r_idx}"] = f"=E{r_idx}/C{r_idx}"
        ws_cust[f"H{r_idx}"].number_format = num_fmt_curr
        ws_cust[f"H{r_idx}"].alignment = align_right
        ws_cust[f"H{r_idx}"].border = thin_border

    # Total Row
    ws_cust["B9"] = "Total Company"
    ws_cust["B9"].font = font_bold
    ws_cust["B9"].fill = fill_tot
    ws_cust["B9"].border = top_thin_bot_double

    for col_c, fmt in [("C", num_fmt_int), ("D", num_fmt_int), ("E", num_fmt_curr), ("F", num_fmt_curr)]:
        ws_cust[f"{col_c}9"] = f"=SUM({col_c}6:{col_c}8)"
        ws_cust[f"{col_c}9"].font = font_bold
        ws_cust[f"{col_c}9"].fill = fill_tot
        ws_cust[f"{col_c}9"].number_format = fmt
        ws_cust[f"{col_c}9"].border = top_thin_bot_double

    ws_cust["G9"] = "=F9/E9"
    ws_cust["G9"].font = font_bold
    ws_cust["G9"].fill = fill_tot
    ws_cust["G9"].number_format = num_fmt_pct
    ws_cust["G9"].border = top_thin_bot_double

    ws_cust["H9"] = "=E9/C9"
    ws_cust["H9"].font = font_bold
    ws_cust["H9"].fill = fill_tot
    ws_cust["H9"].number_format = num_fmt_curr
    ws_cust["H9"].border = top_thin_bot_double

    s_col_widths = {"A": 4, "B": 18, "C": 16, "D": 16, "E": 20, "F": 20, "G": 16, "H": 18}
    for col_l, w in s_col_widths.items():
        ws_cust.column_dimensions[col_l].width = w

    # Save workbook
    os.makedirs(os.path.dirname(excel_output_path), exist_ok=True)
    wb.save(excel_output_path)
    print(f"[+] Executive Excel Workbook generated successfully at: {excel_output_path}")
    print("=" * 70)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    clean_csv_path = os.path.join(project_root, "data", "processed", "retail_sales_clean.csv")
    excel_output_path = os.path.join(project_root, "excel", "Retail_Sales_Analysis.xlsx")
    build_excel_model(clean_csv_path, excel_output_path)

if __name__ == "__main__":
    main()
