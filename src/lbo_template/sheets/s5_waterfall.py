"""5_CF_Waterfall sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_WATERFALL


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_WATERFALL)
    return ws
