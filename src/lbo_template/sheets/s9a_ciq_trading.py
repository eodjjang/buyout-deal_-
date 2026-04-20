"""9a_CIQ_Trading_Raw sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_9A


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9A)
    return ws
