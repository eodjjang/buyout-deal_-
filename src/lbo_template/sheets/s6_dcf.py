"""6_DCF_Valuation sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_DCF


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DCF)
    return ws
