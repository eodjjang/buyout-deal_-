from openpyxl import Workbook


def test_build_returns_workbook(wb: Workbook) -> None:
    assert isinstance(wb, Workbook)


def test_default_sheet_removed(wb: Workbook) -> None:
    assert "Sheet" not in wb.sheetnames
