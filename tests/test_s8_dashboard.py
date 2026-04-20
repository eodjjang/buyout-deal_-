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
        "DASH_IRR_Sponsor",
    ]
    for e in expected_scalars:
        assert e in wb.defined_names, f"missing: {e}"


def test_dash_scalar_attr_text(wb):
    """6 scalar DASH_* names point at the exact expected Dashboard cells."""
    expected = {
        "DASH_Case": "$B$3",
        "DASH_Version": "$B$4",
        "DASH_ICR_Holdco_Min": "$G$16",
        "DASH_ICR_Opco_Min": "$G$17",
        "DASH_DSCR_Min": "$G$18",
        "DASH_IRR_Sponsor": "$B$44",
    }
    for name, anchor in expected.items():
        assert name in wb.defined_names
        attr = wb.defined_names[name].attr_text
        assert anchor in attr, f"{name} attr_text {attr!r} missing {anchor}"


def test_cftable_row8_uses_sum(wb):
    """기말현금 row uses SUM(B28:B34) shape — sign convention contract."""
    ws = wb[SHEET_DASH]
    for col in "BCDEF":
        val = ws[f"{col}35"].value
        assert val == f"=SUM({col}28:{col}34)", f"{col}35: {val!r}"


def test_cftable_rows_2_3_reference_correct_overlay_rows(wb):
    """영업CF → STRESSED_EBITDA_ROW, 투자CF → STRESSED_CAPEX_ROW (protects against row drift)."""
    from lbo_template.sheets.s3_overlay import STRESSED_EBITDA_ROW, STRESSED_CAPEX_ROW
    ws = wb[SHEET_DASH]
    for i, col in enumerate("BCDEF"):
        ov_col = "EFGHI"[i]
        assert ws[f"{col}29"].value == f"='3_Operating_Overlay'!{ov_col}{STRESSED_EBITDA_ROW}"
        assert ws[f"{col}30"].value == f"=-'3_Operating_Overlay'!{ov_col}{STRESSED_CAPEX_ROW}"
