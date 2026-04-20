"""9_Peer_Summary sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_PEER


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_PEER)
    return ws
