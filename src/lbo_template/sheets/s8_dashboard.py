"""8_Dashboard — Word-paste-ready summary tables + DASH_* named range cluster."""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font

from lbo_template.layout import SHEET_DASH, SHEET_OVERLAY
from lbo_template import conventions as c
from lbo_template.sheets.s3_overlay import STRESSED_EBITDA_ROW, STRESSED_CAPEX_ROW

CFTABLE_ROW_LABELS = [
    "기초현금",
    "영업CF (EBITDA)",
    "투자CF (CAPEX)",
    "배당수익",
    "재무CF (기존 차입금 원리금)",
    "본건 인수금융 이자비용",
    "본건 원금상환 (Tr별 합계)",
    "기말현금 (= 원리금 상환재원)",
]

CFTABLE_FIRST_ROW = 28  # row_idx == 1 → ws row 28 (기초현금)
CFTABLE_LAST_ROW = 35  # row_idx == 8 → ws row 35 (기말현금)

# Overlay FY columns (FY_AXIS_COLUMNS = B..I, where E..I = FY1..FY5).
OVERLAY_FY_COLS = ["E", "F", "G", "H", "I"]


def _table_title(ws: Worksheet, cell: str, text: str) -> None:
    ws[cell] = text
    ws[cell].font = Font(name="Calibri", bold=True, size=12)


def _write_headers(ws: Worksheet, row: int, headers: list[str]) -> None:
    for idx, h in enumerate(headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}{row}"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DASH)
    ws.column_dimensions["A"].width = 40
    for col in "BCDEFGHIJ":
        ws.column_dimensions[col].width = 14

    ws["A1"] = "8. Dashboard — Word 심사보고서 복붙용"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:J1")

    # ---- Scenario meta scalars (rows 3–4) ----
    ws["A3"] = "Case"
    ws["B3"] = "=Case_Switch"
    c.define_name(wb, "DASH_Case", f"'{SHEET_DASH}'!$B$3")
    ws["A4"] = "Template Version"
    ws["B4"] = "v0.5"
    c.define_name(wb, "DASH_Version", f"'{SHEET_DASH}'!$B$4")

    # ---- 표 1. Valuation 요약 (title A6, headers row 7, data rows 8–10) ----
    _table_title(ws, "A6", "표 1. Valuation 요약")
    _write_headers(
        ws,
        7,
        ["방식", "Label", "Multiple", "EV (담보지분가치)", "Opco LTV", "누적 LTV"],
    )
    for i in (1, 2, 3):
        r = 7 + i
        ws[f"A{r}"] = f"방식 {i}"
        ws[f"B{r}"] = f"=DASH_Valuation_Method{i}_Label"
        ws[f"C{r}"] = f"=DASH_Valuation_Method{i}_Multiple"
        ws[f"D{r}"] = f"=DASH_Valuation_Method{i}_EV"
        ws[f"E{r}"] = f"=DASH_LTV_Method{i}_Opco"
        ws[f"F{r}"] = f"=DASH_LTV_Method{i}_Cumulative"
        for col in "BCDEF":
            c.apply_key_output(ws[f"{col}{r}"])
        ws[f"C{r}"].number_format = c.NUM_FMT_MULTIPLE
        ws[f"D{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"E{r}"].number_format = c.NUM_FMT_PERCENT
        ws[f"F{r}"].number_format = c.NUM_FMT_PERCENT

    # ---- 표 2. 이자지급가능성 요약 (title A13, headers row 14, data 15–18, Net Lev row 20) ----
    _table_title(ws, "A13", "표 2. 이자지급가능성 요약")
    _write_headers(ws, 14, ["구분", "FY1", "FY2", "FY3", "FY4", "FY5", "Min"])

    # row 15: Dividend Received
    ws["A15"] = "Dividend Received"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}15"] = f"=INDEX(Dividend_Row,{i + 1})"
        ws[f"{col}15"].number_format = c.NUM_FMT_ACCOUNTING
        c.define_name(wb, f"DASH_Div_FY{i + 1}", f"'{SHEET_DASH}'!${col}$15")

    # row 16: Holdco ICR
    ws["A16"] = "Holdco ICR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}16"] = f"=INDEX(Holdco_ICR_Row,{i + 1})"
        ws[f"{col}16"].number_format = c.NUM_FMT_MULTIPLE
    ws["G16"] = "=MIN(Holdco_ICR_Row)"
    ws["G16"].number_format = c.NUM_FMT_MULTIPLE
    c.apply_key_output(ws["G16"])
    c.define_name(wb, "DASH_ICR_Holdco_Min", f"'{SHEET_DASH}'!$G$16")

    # row 17: Opco ICR
    ws["A17"] = "Opco ICR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}17"] = f"=INDEX(Opco_ICR_Row,{i + 1})"
        ws[f"{col}17"].number_format = c.NUM_FMT_MULTIPLE
    ws["G17"] = "=MIN(Opco_ICR_Row)"
    ws["G17"].number_format = c.NUM_FMT_MULTIPLE
    c.apply_key_output(ws["G17"])
    c.define_name(wb, "DASH_ICR_Opco_Min", f"'{SHEET_DASH}'!$G$17")

    # row 18: Opco DSCR
    ws["A18"] = "Opco DSCR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}18"] = f"=INDEX(Opco_DSCR_Row,{i + 1})"
        ws[f"{col}18"].number_format = c.NUM_FMT_MULTIPLE
    ws["G18"] = "=MIN(Opco_DSCR_Row)"
    ws["G18"].number_format = c.NUM_FMT_MULTIPLE
    c.apply_key_output(ws["G18"])
    c.define_name(wb, "DASH_DSCR_Min", f"'{SHEET_DASH}'!$G$18")

    # row 20: Net Leverage
    ws["A20"] = "Net Leverage"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}20"] = f"=INDEX(Net_Leverage_Row,{i + 1})"
        ws[f"{col}20"].number_format = c.NUM_FMT_MULTIPLE
        c.define_name(
            wb, f"DASH_Lev_NetLeverage_FY{i + 1}", f"'{SHEET_DASH}'!${col}$20"
        )

    # ---- 표 3. 만기상환가능성 요약 (title A22, data row 23) ----
    _table_title(ws, "A22", "표 3. 만기상환가능성 요약")
    ws["A23"] = "Exit Multiple (+ Active Δ)"
    # CORRECTION E: Method 2 Multiple (numeric) + Active delta. C11 in the LTV grid is
    # the Base-metric text label, which is unsuitable arithmetic input.
    ws["B23"] = "=DASH_Valuation_Method2_Multiple+Active_Exit_Multiple_Delta"
    ws["B23"].number_format = c.NUM_FMT_MULTIPLE
    c.apply_calc(ws["B23"])

    # ---- 표 4. 차주기준 자금수지표 (title A26, headers row 27, data rows 28–35) ----
    _table_title(ws, "A26", "표 4. 차주기준 자금수지표")
    _write_headers(ws, 27, ["구분"] + [f"FY{i}" for i in range(1, 6)])

    # Main CFTable loop: row_idx 1..8 → rows 28..35, FY1..FY5 → cols B..F.
    # row_idx == 1 (기초현금) is filled in a dedicated loop below (CORRECTION D).
    for row_idx, label in enumerate(CFTABLE_ROW_LABELS, start=1):
        r = 27 + row_idx
        ws[f"A{r}"] = label
        c.define_name(
            wb, f"DASH_CFTable_Row{row_idx}_Label", f"'{SHEET_DASH}'!$A${r}"
        )
        for fy_idx, col in enumerate("BCDEF", start=1):
            cell = ws[f"{col}{r}"]
            ov_col = OVERLAY_FY_COLS[fy_idx - 1]
            if row_idx == 1:
                # 기초현금: filled in the follow-up loop for clarity.
                cell.value = None
            elif row_idx == 2:  # 영업CF = Stressed EBITDA (CORRECTION B: row 11)
                cell.value = f"='{SHEET_OVERLAY}'!{ov_col}{STRESSED_EBITDA_ROW}"
            elif row_idx == 3:  # 투자CF = -Stressed Capex (CORRECTION C: row 13)
                cell.value = f"=-'{SHEET_OVERLAY}'!{ov_col}{STRESSED_CAPEX_ROW}"
            elif row_idx == 4:  # 배당수익 (Holdco 관점)
                cell.value = f"=INDEX(Dividend_Row,{fy_idx})"
            elif row_idx == 5:  # 재무CF (기존 차입금 — MVP는 0)
                cell.value = 0
            elif row_idx == 6:  # 본건 이자비용 합계 (Sr + 2L + Holdco)
                cell.value = (
                    f"=INDEX(Opco_Sr_Interest,{fy_idx})"
                    f"+INDEX(Opco_2L_Interest,{fy_idx})"
                    f"+INDEX(Holdco_Interest,{fy_idx})"
                )
            elif row_idx == 7:  # 본건 원금상환 (Mandatory only)
                cell.value = (
                    f"=INDEX(Opco_Sr_Mand,{fy_idx})"
                    f"+INDEX(Opco_2L_Mand,{fy_idx})"
                )
            elif row_idx == 8:  # 기말현금 = 기초 + 영업 + 투자 + 배당 + 재무 - 이자 - 원금
                cell.value = (
                    f"={col}{CFTABLE_FIRST_ROW}"
                    f"+{col}{CFTABLE_FIRST_ROW + 1}"
                    f"+{col}{CFTABLE_FIRST_ROW + 2}"
                    f"+{col}{CFTABLE_FIRST_ROW + 3}"
                    f"+{col}{CFTABLE_FIRST_ROW + 4}"
                    f"-{col}{CFTABLE_FIRST_ROW + 5}"
                    f"-{col}{CFTABLE_FIRST_ROW + 6}"
                )
            if cell.value is not None:
                c.apply_key_output(cell)
                cell.number_format = c.NUM_FMT_ACCOUNTING
            c.define_name(
                wb,
                f"DASH_CFTable_Row{row_idx}_FY{fy_idx}",
                f"'{SHEET_DASH}'!${col}${r}",
            )

    # CORRECTION D — 기초현금 dedicated loop:
    #   FY1 = 0, FY2..FY5 = previous column's 기말현금 (row 35).
    for fy_idx, col in enumerate("BCDEF", start=1):
        cell = ws[f"{col}{CFTABLE_FIRST_ROW}"]
        if fy_idx == 1:
            cell.value = 0
        else:
            prev = chr(ord(col) - 1)
            cell.value = f"={prev}{CFTABLE_LAST_ROW}"
        c.apply_key_output(cell)
        cell.number_format = c.NUM_FMT_ACCOUNTING

    # ---- 표 5. 시나리오 메타 (title A38, data rows 39–42) ----
    _table_title(ws, "A38", "표 5. 시나리오 메타")
    ws["A39"] = "Revenue Growth Δ"
    ws["B39"] = "=Active_Revenue_Growth_Delta"
    ws["B39"].number_format = c.NUM_FMT_PERCENT
    ws["A40"] = "EBITDA Margin Δ"
    ws["B40"] = "=Active_EBITDA_Margin_Delta"
    ws["B40"].number_format = c.NUM_FMT_PERCENT
    ws["A41"] = "WACC Uplift (bp)"
    ws["B41"] = "=Active_WACC_Uplift"
    ws["B41"].number_format = c.NUM_FMT_BPS
    ws["A42"] = "Exit Multiple Δ"
    ws["B42"] = "=Active_Exit_Multiple_Delta"
    ws["B42"].number_format = c.NUM_FMT_MULTIPLE

    # Sponsor IRR placeholder — name reserved per design v0.5, populated in v1.1+.
    ws["A44"] = "Sponsor IRR (v1.1+)"
    ws["B44"] = None
    c.define_name(wb, "DASH_IRR_Sponsor", f"'{SHEET_DASH}'!$B$44")

    return ws
