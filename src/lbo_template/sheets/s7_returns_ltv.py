"""7_Returns_LTV sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_RETURNS


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_RETURNS)
    return ws
