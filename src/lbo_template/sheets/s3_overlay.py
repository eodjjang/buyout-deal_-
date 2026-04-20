"""3_Operating_Overlay sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_OVERLAY


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_OVERLAY)
    return ws
