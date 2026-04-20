"""8_Dashboard sheet — table layout + DASH_* named range cluster."""
from __future__ import annotations

from lbo_template.layout import SHEET_DASH


def test_dashboard_five_tables(wb):
    ws = wb[SHEET_DASH]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 80)]
    required = [
        "표 1. Valuation 요약",
        "표 2. 이자지급가능성 요약",
        "표 3. 만기상환가능성 요약",
        "표 4. 차주기준 자금수지표",
        "표 5. 시나리오 메타",
    ]
    for e in required:
        assert e in col_a, f"missing table: {e}"


def test_dash_cftable_40_named_ranges(wb):
    for row in range(1, 9):
        for fy in range(1, 6):
            name = f"DASH_CFTable_Row{row}_FY{fy}"
            assert name in wb.defined_names, f"missing: {name}"


def test_dash_cftable_row_labels(wb):
    for row in range(1, 9):
        name = f"DASH_CFTable_Row{row}_Label"
        assert name in wb.defined_names, f"missing: {name}"


def test_dash_all_required_scalars(wb):
    expected_scalars = [
        "DASH_Case",
        "DASH_Version",
        "DASH_DSCR_Min",
        "DASH_ICR_Opco_Min",
        "DASH_ICR_Holdco_Min",
    ]
    for e in expected_scalars:
        assert e in wb.defined_names, f"missing: {e}"
