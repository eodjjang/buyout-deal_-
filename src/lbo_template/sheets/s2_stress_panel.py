"""2_Stress_Panel sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_STRESS


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_STRESS)
    return ws
