"""9b_CIQ_Transaction_Raw sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_9B


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9B)
    return ws
