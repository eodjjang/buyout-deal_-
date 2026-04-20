"""9b_CIQ_Transaction_Raw — Transaction Comps zone (500 rows)."""
from __future__ import annotations

from openpyxl.styles import Font
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from lbo_template import conventions as c
from lbo_template.layout import SHEET_9B, S9B_DATA_END_ROW

HEADERS = [
    "Transaction ID",
    "Announced Date",
    "Closed Date",
    "Target Company Name",
    "Target Country",
    "Target Primary Industry",
    "Buyer Name",
    "Buyer Type",
    "Transaction Currency",
    "Implied Enterprise Value",
    "Target LTM Revenue",
    "Target LTM EBITDA",
    "Implied EV / LTM Revenue",
    "Implied EV / LTM EBITDA",
    "Deal Status",
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9B)
    for col_idx in range(15):
        col = chr(ord("A") + col_idx)
        ws.column_dimensions[col].width = 16

    ws["A1"] = "Mode"
    ws["A1"].font = Font(name="Calibri", bold=True)
    ws["B1"] = '=IF(ISFORMULA(D3),"Plug-in","⚠ Paste Fallback — 마스터 재배포 필요")'
    c.apply_calc(ws["B1"])

    ws["C1"] = (
        '=IF(COUNTA(A:A)-1>500,"⚠ Export 500행 초과 — Paste 잘림 위험. 필터 좁히거나 범위 확장 필요","OK")'
    )
    c.apply_calc(ws["C1"])

    for idx, h in enumerate(HEADERS):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}2"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    for r in range(3, 6):
        cell = ws[f"A{r}"]
        cell.value = f'=IFERROR(CIQTRANSACTION("KR_TRANS_{r-2}","TR_ID"),"")'
        c.apply_ciq(cell)

    for r in range(3, S9B_DATA_END_ROW + 1):
        for col_idx in range(15):
            col = chr(ord("A") + col_idx)
            cell = ws[f"{col}{r}"]
            if r > 5:
                c.apply_input(cell)

    return ws
