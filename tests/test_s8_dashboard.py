"""8_Dashboard sheet — table layout + DASH_* named range cluster."""
from __future__ import annotations

from lbo_template.layout import SHEET_DASH


def test_dashboard_table_titles(wb):
    ws = wb[SHEET_DASH]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 120)]
    required = [
        "표 1. Valuation 요약",
        "표 2. 이자지급가능성 요약",
        "표 3. 만기상환가능성 요약",
        "표 4. 차주기준 자금수지표",
        "표 5. 시나리오 메타",
        "표 6. 재무약정 준수여부",
        "표 7. 만기시점 LTV 분석",
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
    """Scalar DASH_* names point at the expected Dashboard cells."""
    expected = {
        "DASH_Case": "$B$3",
        "DASH_Version": "$B$4",
        "DASH_ICR_Holdco_Min": "$G$16",
        "DASH_ICR_Opco_Min": "$G$17",
        "DASH_DSCR_Min": "$G$18",
    }
    for name, anchor in expected.items():
        assert name in wb.defined_names
        attr = wb.defined_names[name].attr_text
        assert anchor in attr, f"{name} attr_text {attr!r} missing {anchor}"

    assert wb.defined_names["DASH_IRR_Sponsor"].attr_text.endswith("$B$61")


def test_cftable_ending_cash_formula(wb):
    """기말현금 = 원리금 이후 + 리파이낸싱."""
    ws = wb[SHEET_DASH]
    for col in "BCDEF":
        val = ws[f"{col}53"].value
        assert val == f"={col}51+{col}52", f"{col}53: {val!r}"


def test_cftable_ebitda_capex_reference_overlay(wb):
    """EBITDA·CAPEX 행이 Operating Overlay 스트레스 행을 참조."""
    from lbo_template.sheets.s3_overlay import STRESSED_EBITDA_ROW, STRESSED_CAPEX_ROW

    ws = wb[SHEET_DASH]
    for i, col in enumerate("BCDEF"):
        ov_col = "EFGHI"[i]
        assert ws[f"{col}34"].value == f"='3_Operating_Overlay'!{ov_col}{STRESSED_EBITDA_ROW}"
        assert ws[f"{col}36"].value == f"=-'3_Operating_Overlay'!{ov_col}{STRESSED_CAPEX_ROW}"
