"""9c_Manual_Supplement sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_9C


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9C)
    return ws
