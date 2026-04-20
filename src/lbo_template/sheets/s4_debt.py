"""4_Debt_Schedule sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_DEBT


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DEBT)
    return ws
